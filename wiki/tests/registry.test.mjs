import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, cp, writeFile, readFile, rm } from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { createServer } from "node:http";
import { EventEmitter } from "node:events";
import { compileRegistry } from "../server/registry.mjs";
import { registryPlugin } from "../server/registry-plugin.mjs";
const content = fileURLToPath(new URL("../content/", import.meta.url));
async function workspace(t) {
  const temp = await mkdtemp(path.join(os.tmpdir(), "kamaen-registry-"));
  await cp(content, temp, { recursive: true });
  t.after(() => rm(temp, { recursive: true, force: true }));
  return temp;
}
test("new entity, Markdown and scene files register without a frontend change; duplicate and broken refs fail", async (t) => {
  const root = await workspace(t),
    initial = await compileRegistry(root);
  const e = {
    schemaVersion: 1,
    id: "test:new_item",
    kind: "item",
    title: "新建测试条目",
    status: "示例",
    summary: "文件注册验证",
    tags: [],
    description: "descriptions/new-test.md",
    visual: { type: "sprite", asset: "assets/seed.svg" },
    scene: "impact",
  };
  await writeFile(
    path.join(root, "descriptions/new-test.md"),
    "# 文件正文\n\n![预览](asset:assets/seed.svg)",
  );
  await writeFile(path.join(root, "entities/new-test.json"), JSON.stringify(e));
  const registry = await compileRegistry(root);
  assert.equal(registry.entities.length, initial.entities.length + 1);
  assert.match(registry.entities.find((v) => v.id === e.id).body, /文件正文/);
  assert.match(
    registry.assets["assets/seed.svg"],
    /^data:image\/svg\+xml;base64,/,
  );
  await writeFile(
    path.join(root, "entities/new-test.json"),
    JSON.stringify({
      ...e,
      relations: [{ target: "missing", label: "broken" }],
    }),
  );
  await assert.rejects(compileRegistry(root), /未知关联/);
  await writeFile(
    path.join(root, "entities/new-test.json"),
    JSON.stringify({ ...e, id: initial.entities[0].id }),
  );
  await assert.rejects(compileRegistry(root), /重复 ID/);
  await writeFile(
    path.join(root, "entities/new-test.json"),
    JSON.stringify({ ...e, description: "../outside.md" }),
  );
  await assert.rejects(compileRegistry(root));
});
test("map API saves atomically, rejects stale external edits even with same revision, validates refs and origins", async (t) => {
  const root = await workspace(t),
    plugin = registryPlugin(root);
  let handler;
  const watcher = new EventEmitter();
  watcher.add = () => {};
  plugin.configureServer({
    watcher,
    middlewares: { use: (_route, fn) => (handler = fn) },
    moduleGraph: { getModuleById: () => null },
    ws: { send: () => {} },
  });
  const server = createServer((req, res) => {
    req.url = req.url.slice("/api/maps".length);
    handler(req, res);
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  t.after(() => new Promise((r) => server.close(r)));
  const origin = `http://127.0.0.1:${server.address().port}`,
    url = origin + "/api/maps/development";
  const before = await (await fetch(url)).json();
  const put = (doc, etag, from = origin) =>
    fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "If-Match": etag,
        Origin: from,
      },
      body: JSON.stringify(doc),
    });
  const changed = { ...before.document, title: "API test" };
  const results = await Promise.all([
    put(changed, before.etag),
    put(changed, before.etag),
  ]);
  assert.deepEqual(results.map((r) => r.status).sort(), [200, 409]);
  const saved = await (await fetch(url)).json();
  assert.equal(saved.document.revision, before.document.revision + 1);
  const filename = path.join(root, "maps/development.json");
  await writeFile(
    filename,
    JSON.stringify({ ...saved.document, title: "外部文件编辑" }),
  );
  assert.equal((await put(changed, saved.etag)).status, 409);
  const fresh = await (await fetch(url)).json();
  assert.equal(
    (await put(changed, fresh.etag, "https://example.com")).status,
    403,
  );
  assert.equal(
    (
      await put(
        {
          ...changed,
          nodes: [
            {
              id: "bad",
              type: "entity",
              ref: "not-registered",
              x: 0,
              y: 0,
              width: 10,
              height: 10,
            },
          ],
        },
        fresh.etag,
      )
    ).status,
    400,
  );
  assert.equal(
    JSON.parse(await readFile(filename, "utf8")).title,
    "外部文件编辑",
  );
});

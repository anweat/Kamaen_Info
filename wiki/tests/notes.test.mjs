import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, writeFile, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { createServer } from "node:http";
import { notesPlugin, validateNotes } from "../server/notes.mjs";
const note = {
  id: "test",
  title: "测试记录",
  body: "## 想法\n\n晶体与产线",
  stage: "E1",
  status: "想法",
  refs: ["scene~impact"],
  updatedAt: "2026-09-07",
};
test("record validation rejects bad shape, duplicates and unbounded content", () => {
  assert.equal(validateNotes({ revision: 0, notes: [note] }), true);
  for (const v of [
    { revision: -1, notes: [] },
    { revision: 0, notes: [note, note] },
    { revision: 0, notes: [{ ...note, title: "" }] },
    { revision: 0, notes: [{ ...note, refs: ["x", 3] }] },
    { revision: 0, notes: [{ ...note, body: "a".repeat(100001) }] },
  ])
    assert.ok(!validateNotes(v));
});
test("local notes persist atomically; concurrent stale writes cannot overwrite; external origins rejected", async () => {
  const dir = await mkdtemp(path.join(tmpdir(), "kamaen-notes-test-"));
  const file = path.join(dir, "notes.json");
  await writeFile(file, JSON.stringify({ revision: 0, notes: [] }));
  let handler;
  notesPlugin(file).configureServer({
    middlewares: {
      use(_path, fn) {
        handler = fn;
      },
    },
  });
  const server = createServer((req, res) => handler(req, res));
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const url = `http://127.0.0.1:${server.address().port}`;
  try {
    const put = (payload, origin = url) =>
      fetch(url + "/api/notes", {
        method: "PUT",
        headers: { "Content-Type": "application/json", Origin: origin },
        body: JSON.stringify(payload),
      });
    assert.equal(
      (await put({ revision: 0, notes: [note] }, "http://example.com")).status,
      403,
    );
    assert.equal(
      (await put({ revision: 0, notes: [{ ...note, title: "" }] })).status,
      400,
    );
    const responses = await Promise.all([
      put({ revision: 0, notes: [note] }),
      put({ revision: 0, notes: [{ ...note, title: "stale" }] }),
    ]);
    assert.deepEqual(responses.map((r) => r.status).sort(), [200, 409]);
    const stored = await (await fetch(url + "/api/notes")).json();
    assert.equal(stored.revision, 1);
    assert.equal(stored.notes.length, 1);
    assert.deepEqual(JSON.parse(await readFile(file, "utf8")), stored);
    const next = {
      ...stored,
      notes: [{ ...stored.notes[0], body: "更新正文" }],
    };
    assert.equal((await put(next)).status, 200);
    assert.equal(
      JSON.parse(await readFile(file, "utf8")).notes[0].body,
      "更新正文",
    );
  } finally {
    await new Promise((resolve) => server.close(resolve));
    await rm(dir, { recursive: true, force: true });
  }
});

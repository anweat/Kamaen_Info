import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import http from "node:http";
import { workbenchMiddleware } from "../server/workbench.mjs";
test("desktop bridge launches only configured targets and rejects cross-origin commands", async () => {
  const root = await mkdtemp(path.join(tmpdir(), "kamaen-tools-"));
  await mkdir(path.join(root, "tooling"));
  await writeFile(
    path.join(root, "gradle.properties"),
    "minecraft_version=1.21.1\nneo_version=21.1.222\n",
  );
  await writeFile(path.join(root, "tool.exe"), "fixture");
  await writeFile(path.join(root, "model.bbmodel"), "{}");
  await writeFile(
    path.join(root, "tooling/workbench.json"),
    JSON.stringify({
      tools: [
        {
          id: "model",
          kind: "app",
          title: "Model",
          executable: "model",
          target: "model.bbmodel",
        },
        { id: "absent", kind: "app", executable: "absent" },
      ],
    }),
  );
  await writeFile(
    path.join(root, "tooling/local.json"),
    JSON.stringify({ executables: { model: "tool.exe" } }),
  );
  const launched = [];
  const server = http.createServer(
    workbenchMiddleware(root, {
      launch: async (...args) => launched.push(args),
    }),
  );
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const url = `http://127.0.0.1:${server.address().port}`;
  const post = (route, body = "{}", origin = url) =>
    fetch(url + route, {
      method: "POST",
      headers: { Origin: origin, "Content-Type": "application/json" },
      body,
    });
  try {
    const status = await (await fetch(url)).json();
    assert.equal(status.tools[0].available, true);
    assert.equal(status.tools[1].available, false);
    assert.equal(status.neoForge, "21.1.222");
    assert.equal(
      (await post("/launch/model", "{}", "https://example.com")).status,
      403,
    );
    assert.equal((await post("/launch/unknown")).status, 404);
    assert.equal(
      (await post("/launch/model", '{"path":"C:/secret"}')).status,
      400,
    );
    assert.equal((await post("/launch/model", "x".repeat(1025))).status, 413);
    assert.equal((await post("/launch/absent")).status, 409);
    assert.equal(launched.length, 0);
    assert.equal((await post("/launch/model")).status, 200);
    assert.deepEqual(launched, [
      [
        path.join(root, "tool.exe"),
        [path.join(root, "model.bbmodel")],
        root,
        {},
      ],
    ]);
    const foreignHostStatus = await new Promise((resolve, reject) => {
      const request = http.get(
        url,
        { headers: { Host: "attacker.example" } },
        (response) => {
          response.resume();
          resolve(response.statusCode);
        },
      );
      request.on("error", reject);
    });
    assert.equal(foreignHostStatus, 403);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    await rm(root, { recursive: true, force: true });
  }
});

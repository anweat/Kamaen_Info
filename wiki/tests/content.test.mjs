import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const data = JSON.parse(
  await readFile(
    new URL("../src/generated/content.json", import.meta.url),
    "utf8",
  ),
);
test("imported objects remain unique and source linked, including multi-stage rows", () => {
  assert.equal(new Set(data.items.map((i) => i.id)).size, data.items.length);
  assert.equal(data.items.filter((i) => i.version === "E1").length, 100);
  assert.ok(data.items.some((i) => i.stage === "E0/E5"));
  for (const item of data.items)
    assert.ok(
      data.docs.some((d) => d.id === item.source),
      item.id,
    );
});
test("recipes preserve station, consumed materials, non-consumed tools and research references", () => {
  for (const r of data.recipes) {
    assert.ok(data.stations[r.station]);
    for (const id of [
      ...Object.keys(r.inputs),
      ...Object.keys(r.outputs),
      ...r.tools,
    ])
      assert.ok(
        data.items.some((i) => i.id === "r4:" + id),
        id,
      );
    for (const id of r.evidence) assert.ok(data.evidence[id]);
  }
  const endpoint = data.recipes.find((r) => r.id === "endpoint_chip");
  assert.equal(endpoint.inputs.gate, 2);
  assert.deepEqual(endpoint.evidence, ["endpoint"]);
});

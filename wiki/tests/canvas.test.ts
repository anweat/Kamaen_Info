import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resizeInFlow } from "../src/canvas-layout";
import type { CanvasDocument } from "../src/canvas-types";
// @ts-ignore Server uses plain JavaScript for the Vite middleware.
import { validateCanvas } from "../server/canvas.mjs";
const seed: CanvasDocument = JSON.parse(
  await readFile(new URL("../content/canvas.json", import.meta.url), "utf8"),
);
test("canvas seed is valid; every sprite and narrative link resolves", async () => {
  const data = JSON.parse(
    await readFile(
      new URL("../src/generated/content.json", import.meta.url),
      "utf8",
    ),
  );
  assert.equal(validateCanvas(seed), true);
  for (const n of seed.nodes) {
    for (const group of n.groups)
      for (const id of group.items)
        assert.ok(
          data.items.some((i: { id: string }) => i.id === id),
          id,
        );
    if (n.source)
      assert.ok(data.docs.some((d: { id: string }) => d.id === n.source));
  }
  assert.equal(
    validateCanvas({ ...seed, nodes: [{ ...seed.nodes[0], width: -1 }] }),
    false,
  );
  assert.equal(
    validateCanvas({
      ...seed,
      edges: [
        { from: "missing", to: "chapter-1", label: "bad", kind: "story" },
      ],
    }),
    false,
  );
});
test("inline expansion pushes only downstream overlapping columns; collapse restores positions", () => {
  const first = seed.nodes.find((n) => n.id === "chapter-1")!;
  const beforeScene = seed.nodes.find((n) => n.id === "impact-scene")!;
  const bigger = resizeInFlow(seed, first.id, first.height + 320);
  assert.equal(
    bigger.nodes.find((n) => n.id === "impact-scene")!.y,
    beforeScene.y + 320,
  );
  assert.deepEqual(
    bigger.nodes.find((n) => n.id === "chapter-2"),
    seed.nodes.find((n) => n.id === "chapter-2"),
  );
  assert.equal(
    bigger.nodes.find((n) => n.id === "field-note")!.y,
    seed.nodes.find((n) => n.id === "field-note")!.y,
  );
  const restored = resizeInFlow(bigger, first.id, first.height);
  assert.deepEqual(restored.nodes, seed.nodes);
});
test("replacing inline details recomputes height without accumulating offsets", () => {
  const first = seed.nodes[0];
  const a = resizeInFlow(seed, first.id, first.height + 300);
  const b = resizeInFlow(a, first.id, first.height + 200);
  assert.equal(
    b.nodes.find((n) => n.id === "impact-scene")!.y,
    seed.nodes.find((n) => n.id === "impact-scene")!.y + 200,
  );
  assert.equal(seed.nodes[0].height, first.height);
});

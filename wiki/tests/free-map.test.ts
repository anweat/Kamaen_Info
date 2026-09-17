import test from "node:test";
import assert from "node:assert/strict";
import {
  normalizeStroke,
  worldPoint,
  linePoints,
  resizeNode,
  removeNode,
} from "../src/world/geometry";
import { evaluate } from "../src/world/ModelView";
import type { MapNode } from "../src/world/types";
import { validExpression, validateMap } from "../shared/contracts.mjs";
test("free drawing preserves fractional coordinates and converts zoom without snapping", () => {
  const p = worldPoint(
    { x: 189.3, y: 241.5 },
    { x: 20, y: 30 },
    { x: 40, y: 10, zoom: 0.5 },
  );
  assert.equal(p.x, 258.6);
  assert.equal(p.y, 403);
  const shape = normalizeStroke([
    { x: 105.7, y: 204.3 },
    { x: 37.2, y: 89.8 },
    { x: 55.3, y: 181.25 },
  ]);
  assert.equal(shape.x, 37.2);
  assert.equal(shape.y, 89.8);
  assert.equal(shape.points[0].x, 68.5);
});
test("attached lines follow object geometry; deletion preserves visible endpoints; resize scales ink", () => {
  const a: MapNode = {
      id: "a",
      type: "entity",
      x: 0,
      y: 0,
      width: 100,
      height: 100,
      ref: "item",
    },
    b: MapNode = { ...a, id: "b", x: 400 };
  const edge: MapNode = {
    id: "edge",
    type: "arrow",
    x: 0,
    y: 0,
    width: 500,
    height: 1,
    points: [
      { x: 0, y: 0 },
      { x: 500, y: 0 },
    ],
    from: "a",
    to: "b",
  };
  const before = linePoints(edge, [a, b, edge]);
  assert.deepEqual(before, [
    { x: 110, y: 50 },
    { x: 390, y: 50 },
  ]);
  assert.equal(linePoints(edge, [a, { ...b, x: 450 }, edge])[1].x, 440);
  const remaining = removeNode([a, b, edge], "b"),
    detached = remaining.find((n) => n.id === "edge")!;
  assert.equal(detached.to, undefined);
  assert.deepEqual(linePoints(detached, remaining), before);
  const ink: MapNode = {
    id: "ink",
    type: "pen",
    ...normalizeStroke([
      { x: 3, y: 7 },
      { x: 23, y: 47 },
    ]),
  };
  assert.deepEqual(resizeNode(ink, 40, 80).points, [
    { x: 0, y: 0 },
    { x: 40, y: 80 },
  ]);
});
test("file expressions reject executable or invalid forms and retain undefined mathematical regions", () => {
  const names = new Set(["x"]);
  assert.equal(validExpression({ op: "constructor", args: [] }, names), false);
  assert.equal(validExpression("globalThis", names), false);
  assert.equal(validExpression({ op: "mul", args: ["x", 2] }, names), true);
  assert.equal(evaluate({ op: "mul", args: ["x", 2] }, { x: 3 }), 6);
  assert.ok(Number.isNaN(evaluate({ op: "div", args: [1, 0] }, {})));
  assert.equal(
    validateMap({
      schemaVersion: 1,
      id: "map",
      title: "Map",
      revision: 0,
      nodes: [
        {
          id: "bad",
          type: "pen",
          x: 0,
          y: 0,
          width: 20,
          height: 20,
          points: [
            { x: NaN, y: 0 },
            { x: 2, y: 2 },
          ],
        },
      ],
    }),
    false,
  );
});

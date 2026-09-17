import type { WorldMap, Registry } from "../src/world/types";
export function validateMap(
  value: unknown,
  registry?: Registry,
): value is WorldMap;
export function validExpression(
  exp: unknown,
  names: Set<string>,
  depth?: number,
): boolean;

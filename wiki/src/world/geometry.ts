import type { MapNode, Point } from "./types";
export const clamp = (n: number, min: number, max: number) =>
  Math.max(min, Math.min(max, n));
export function worldPoint(
  client: Point,
  origin: Point,
  view: Point & { zoom: number },
): Point {
  return {
    x: (client.x - origin.x - view.x) / view.zoom,
    y: (client.y - origin.y - view.y) / view.zoom,
  };
}
export function normalizeStroke(points: Point[]) {
  const x = Math.min(...points.map((p) => p.x)),
    y = Math.min(...points.map((p) => p.y));
  return {
    x,
    y,
    width: Math.max(1, ...points.map((p) => p.x - x)),
    height: Math.max(1, ...points.map((p) => p.y - y)),
    points: points.map((p) => ({ x: p.x - x, y: p.y - y })),
  };
}
export function linePoints(node: MapNode, nodes: MapNode[]): Point[] {
  const own = (
    node.points || [
      { x: 0, y: 0 },
      { x: node.width, y: node.height },
    ]
  ).map((p) => ({ x: p.x + node.x, y: p.y + node.y }));
  const from = nodes.find((n) => n.id === node.from),
    to = nodes.find((n) => n.id === node.to);
  const center = (n: MapNode) => ({
    x: n.x + n.width / 2,
    y: n.y + n.height / 2,
  });
  const boundary = (n: MapNode, t: Point) => {
    const c = center(n),
      dx = t.x - c.x,
      dy = t.y - c.y;
    if (!dx && !dy) return c;
    const scale = Math.min(
      (n.width / 2 + 10) / (Math.abs(dx) || 0.0001),
      (n.height / 2 + 10) / (Math.abs(dy) || 0.0001),
    );
    return { x: c.x + dx * scale, y: c.y + dy * scale };
  };
  if (from) own[0] = boundary(from, to ? center(to) : own.at(-1)!);
  if (to) own[own.length - 1] = boundary(to, from ? center(from) : own[0]);
  return own;
}
export function resizeNode(
  node: MapNode,
  width: number,
  height: number,
): MapNode {
  return {
    ...node,
    width,
    height,
    points: node.points?.map((p) => ({
      x: (p.x * width) / node.width,
      y: (p.y * height) / node.height,
    })),
  };
}
export function removeNode(nodes: MapNode[], id: string): MapNode[] {
  return nodes
    .filter((n) => n.id !== id)
    .map((n) => {
      if (n.from !== id && n.to !== id) return n;
      const stroke = normalizeStroke(linePoints(n, nodes));
      return {
        ...n,
        ...stroke,
        from: n.from === id ? undefined : n.from,
        to: n.to === id ? undefined : n.to,
      };
    });
}

import { clamp, type CanvasDocument, type CanvasNode } from "./canvas-types";
export function resizeInFlow(
  doc: CanvasDocument,
  id: string,
  height: number,
): CanvasDocument {
  if (!Number.isFinite(height)) return doc;
  const anchor = doc.nodes.find((n) => n.id === id);
  if (!anchor) return doc;
  const target = clamp(height, 120, 1600);
  const delta = target - anchor.height;
  if (Math.abs(delta) < 2) return doc;
  const nodes = doc.nodes.map((n) => ({ ...n }));
  const current = nodes.find((n) => n.id === id)!;
  current.height = target;
  // Only components below the changed frame, in overlapping columns, follow its flow.
  const moved = new Set([id]);
  for (const node of nodes
    .filter((n) => n.id !== id)
    .sort((a, b) => a.y - b.y)) {
    if (node.y < anchor.y + anchor.height - 2) continue;
    const blockers = nodes.filter(
      (n) =>
        moved.has(n.id) &&
        node.x < n.x + n.width + 24 &&
        node.x + node.width > n.x - 24,
    );
    if (!blockers.length) continue;
    const oldTop = doc.nodes.find((n) => n.id === node.id)!.y;
    const closeToFlow = blockers.some((n) => {
      const original = doc.nodes.find((o) => o.id === n.id)!;
      return (
        oldTop >= original.y + (original.collapsed ? 58 : original.height) - 2
      );
    });
    if (closeToFlow) {
      node.y = clamp(oldTop + delta, -10000, 10000);
      moved.add(node.id);
    }
  }
  return { ...doc, nodes };
}
export function canvasBounds(nodes: CanvasNode[]) {
  return {
    left: Math.min(...nodes.map((n) => n.x), 0) - 50,
    top: Math.min(...nodes.map((n) => n.y), 0) - 50,
    right: Math.max(...nodes.map((n) => n.x + n.width), 100) + 50,
    bottom:
      Math.max(...nodes.map((n) => n.y + (n.collapsed ? 58 : n.height)), 100) +
      50,
  };
}

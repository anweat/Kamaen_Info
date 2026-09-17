export function validateCanvas(value) {
  const bounded = (v, min, max) => Number.isFinite(v) && v >= min && v <= max;
  if (
    value?.openItems &&
    !Object.entries(value.openItems).every(
      ([key, id]) =>
        typeof id === "string" &&
        value.nodes?.some(
          (n) => n.id === key && n.groups?.some((g) => g.items?.includes(id)),
        ),
    )
  )
    return false;
  if (
    value?.baseHeights &&
    !Object.entries(value.baseHeights).every(
      ([key, height]) =>
        bounded(height, 120, 1600) && value.nodes?.some((n) => n.id === key),
    )
  )
    return false;
  return (
    !!value &&
    Number.isSafeInteger(value.revision) &&
    value.revision >= 0 &&
    Array.isArray(value.nodes) &&
    value.nodes.length <= 150 &&
    new Set(value.nodes.map((n) => n?.id)).size === value.nodes.length &&
    value.nodes.every(
      (n) =>
        n &&
        typeof n.id === "string" &&
        n.id.length < 100 &&
        typeof n.title === "string" &&
        n.title.length <= 200 &&
        ["cluster", "text", "scene", "recipe"].includes(n.type) &&
        bounded(n.x, -10000, 10000) &&
        bounded(n.y, -10000, 10000) &&
        bounded(n.width, 260, 1400) &&
        bounded(n.height, 120, 1600) &&
        typeof n.collapsed === "boolean" &&
        typeof n.body === "string" &&
        n.body.length <= 50000 &&
        Array.isArray(n.groups) &&
        n.groups.length <= 20 &&
        n.groups.every(
          (g) =>
            typeof g.title === "string" &&
            g.title.length <= 200 &&
            Array.isArray(g.items) &&
            g.items.length <= 300 &&
            g.items.every((i) => typeof i === "string" && i.length <= 200),
        ) &&
        ["chapter", "source", "scene", "recipe"].every(
          (k) => typeof n[k] === "string" && n[k].length <= 200,
        ),
    ) &&
    Array.isArray(value.edges) &&
    value.edges.length <= 300 &&
    value.edges.every(
      (e) =>
        e &&
        typeof e.label === "string" &&
        e.label.length <= 200 &&
        ["story", "feedback"].includes(e.kind) &&
        value.nodes.some((n) => n.id === e.from) &&
        value.nodes.some((n) => n.id === e.to),
    )
  );
}

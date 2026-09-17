const kinds = ["item", "block", "multiblock", "nbt", "model"];
const types = [
  "entity",
  "text",
  "arrow",
  "line",
  "rect",
  "pen",
  "space3d",
  "space2d",
  "custom",
];
const finite = (v) => Number.isFinite(v) && Math.abs(v) <= 100000;
const text = (v, max = 100000) => typeof v === "string" && v.length <= max;
const identifier = (v) => text(v, 150) && /^[a-zA-Z0-9_:.\/-]+$/.test(v);
function check(ok, message) {
  if (!ok) throw new Error(message);
}
export function validateMap(value, registry) {
  if (
    !value ||
    value.schemaVersion !== 1 ||
    !identifier(value.id) ||
    !text(value.title, 200) ||
    !Number.isSafeInteger(value.revision) ||
    value.revision < 0 ||
    !Array.isArray(value.nodes) ||
    value.nodes.length > 2000
  )
    return false;
  const ids = new Set(value.nodes.map((n) => n?.id));
  if (ids.size !== value.nodes.length) return false;
  return value.nodes.every((n) => {
    if (
      !n ||
      !identifier(n.id) ||
      !types.includes(n.type) ||
      ![n.x, n.y, n.width, n.height].every(finite) ||
      n.width < 1 ||
      n.height < 1 ||
      n.width > 10000 ||
      n.height > 10000
    )
      return false;
    if (
      ["title", "body", "ref", "color"].some(
        (k) => n[k] !== undefined && !text(n[k]),
      )
    )
      return false;
    if (
      n.fontSize !== undefined &&
      (!finite(n.fontSize) || n.fontSize < 10 || n.fontSize > 120)
    )
      return false;
    if (n.color !== undefined && !/^#[\da-f]{6}$/i.test(n.color)) return false;
    if (
      n.from !== undefined &&
      (!ids.has(n.from) ||
        n.from === n.id ||
        !["arrow", "line"].includes(n.type))
    )
      return false;
    if (
      n.to !== undefined &&
      (!ids.has(n.to) || n.to === n.id || !["arrow", "line"].includes(n.type))
    )
      return false;
    if (
      (n.points !== undefined || ["arrow", "line", "pen"].includes(n.type)) &&
      (!Array.isArray(n.points) ||
        n.points.length < 2 ||
        n.points.length > 10000 ||
        !n.points.every((p) => p && finite(p.x) && finite(p.y)))
    )
      return false;
    if (registry) {
      const list = {
        entity: registry.entities,
        space3d: registry.scenes,
        space2d: registry.models,
        custom: registry.renderers,
      }[n.type];
      if (list && !list.some((e) => e.id === n.ref)) return false;
    }
    return true;
  });
}
export function validExpression(exp, names, depth = 0) {
  if (depth > 20) return false;
  if (typeof exp === "number") return Number.isFinite(exp);
  if (typeof exp === "string") return names.has(exp);
  const arity = { add: 2, sub: 2, mul: 2, div: 2, pow: 2, sin: 1, exp: 1 };
  return (
    !!exp &&
    Object.hasOwn(arity, exp.op) &&
    Array.isArray(exp.args) &&
    exp.args.length === arity[exp.op] &&
    exp.args.every((a) => validExpression(a, names, depth + 1))
  );
}

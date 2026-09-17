import { readdir, readFile, realpath } from "node:fs/promises";
import path from "node:path";
import { validateMap, validExpression } from "../shared/contracts.mjs";
export { validateMap, validExpression } from "../shared/contracts.mjs";
const kinds = ["item", "block", "multiblock", "nbt", "model"];
const finite = (v) => Number.isFinite(v) && Math.abs(v) <= 100000;
const text = (v, max = 100000) => typeof v === "string" && v.length <= max;
const identifier = (v) => text(v, 150) && /^[a-zA-Z0-9_:.\/-]+$/.test(v);
function check(ok, message) {
  if (!ok) throw new Error(message);
}
export async function compileRegistry(root) {
  const base = await realpath(root);
  async function local(file) {
    check(
      text(file) && !path.isAbsolute(file),
      `必须使用 content 内的相对路径：${file}`,
    );
    const resolved = await realpath(path.resolve(base, file));
    check(
      resolved.startsWith(base + path.sep),
      `引用不能离开 content：${file}`,
    );
    return resolved;
  }
  async function files(folder) {
    const all = [];
    async function visit(dir) {
      for (const entry of await readdir(dir, { withFileTypes: true })) {
        const file = path.join(dir, entry.name);
        if (entry.isSymbolicLink())
          throw Error(`注册目录不接受符号链接：${file}`);
        if (entry.isDirectory()) await visit(file);
        else if (entry.name.endsWith(".json")) all.push(file);
      }
    }
    await visit(path.join(base, folder));
    return Promise.all(
      all.sort().map(async (file) => {
        try {
          return {
            ...JSON.parse(await readFile(file, "utf8")),
            file: path.relative(base, file).replaceAll("\\", "/"),
          };
        } catch (e) {
          throw Error(`${file}: ${e.message}`);
        }
      }),
    );
  }
  const [entities, maps, scenes, models, renderers] = await Promise.all(
    ["entities", "maps", "scenes", "models", "renderers"].map(files),
  );
  const registry = { entities, maps, scenes, models, renderers, assets: {} };
  for (const [category, list] of Object.entries({
    entities,
    maps,
    scenes,
    models,
    renderers,
  })) {
    const ids = new Set();
    for (const row of list) {
      check(
        identifier(row.id) && text(row.title, 200) && row.title.trim(),
        `${row.file}: id/title 无效`,
      );
      check(!ids.has(row.id), `${category}: 重复 ID ${row.id}`);
      ids.add(row.id);
    }
  }
  async function asset(file) {
    if (!file || registry.assets[file]) return;
    const mime = {
      ".png": "image/png",
      ".svg": "image/svg+xml",
      ".webp": "image/webp",
      ".jpg": "image/jpeg",
    }[path.extname(file).toLowerCase()];
    check(mime, `不支持的图片类型：${file}`);
    registry.assets[file] =
      `data:${mime};base64,${(await readFile(await local(file))).toString("base64")}`;
  }
  for (const e of entities) {
    check(
      e.schemaVersion === 1 &&
        kinds.includes(e.kind) &&
        text(e.summary, 2000) &&
        text(e.status, 100) &&
        Array.isArray(e.tags) &&
        e.tags.every((t) => text(t, 100)),
      `${e.file}: 实体字段无效`,
    );
    e.body = e.description
      ? await readFile(await local(e.description), "utf8")
      : "";
    if (e.designRefs !== undefined)
      check(
        Array.isArray(e.designRefs) && e.designRefs.every((r) =>
          r && typeof r.document === "string" && /^[A-Za-z0-9_-]+\.md$/.test(r.document) &&
          text(r.label, 200) && r.label.trim() &&
          (r.legacyId === undefined || identifier(r.legacyId))),
        `${e.file}: designRefs 无效`,
      );
    if (e.runtimeRef !== undefined && e.runtimeRef !== null)
      check(typeof e.runtimeRef === "string" && /^[a-z0-9_.-]+:[a-z0-9_./-]+$/.test(e.runtimeRef),
        `${e.file}: runtimeRef 无效`);
    if (e.lifecycle !== undefined)
      check(e.lifecycle && ["design", "runtime", "art", "verification"].every(
        (key) => text(e.lifecycle[key], 100) && e.lifecycle[key].trim()),
        `${e.file}: lifecycle 必须分别声明设计、游戏、贴图和验证状态`);
    for (const match of e.body.matchAll(/asset:([^\s)]+)/g))
      await asset(match[1]);
    if (e.visual) {
      check(
        ["sprite", "block"].includes(e.visual.type),
        `${e.file}: visual.type 无效`,
      );
      for (const k of ["asset", "top", "side"]) await asset(e.visual[k]);
      if (e.visual.color)
        check(
          /^#[\da-f]{6}$/i.test(e.visual.color),
          `${e.file}: visual.color 无效`,
        );
    }
    for (const image of e.gallery || []) {
      check(text(image.caption), `${e.file}: 图注无效`);
      await asset(image.asset);
    }
    for (const r of e.relations || [])
      check(
        entities.some((x) => x.id === r.target) && text(r.label, 200),
        `${e.file}: 未知关联 ${r.target}`,
      );
    for (const [key, list] of [
      ["scene", scenes],
      ["model", models],
      ["renderer", renderers],
    ])
      if (e[key])
        check(
          list.some((x) => x.id === e[key]),
          `${e.file}: 未知 ${key} ${e[key]}`,
        );
    if (e.fields)
      check(
        Array.isArray(e.fields) &&
          e.fields.every(
            (f) =>
              text(f.name, 150) && text(f.type, 100) && text(f.description),
          ),
        `${e.file}: NBT 字段无效`,
      );
  }
  for (const s of scenes) {
    check(s.schemaVersion === 1, `${s.file}: scene.schemaVersion 必须为 1`);
    check(
      Array.isArray(s.steps) &&
        s.steps.length > 0 &&
        s.steps.every((s) => text(s.title) && text(s.text)) &&
        Array.isArray(s.voxels) &&
        s.voxels.length > 0 &&
        s.voxels.length <= 2000,
      `${s.file}: 场景必须有步骤和体素`,
    );
    check(
      s.voxels.every(
        (v) =>
          Array.isArray(v.position) &&
          v.position.length === 3 &&
          v.position.every(finite) &&
          (!v.size ||
            (v.size.length === 3 && v.size.every((n) => finite(n) && n > 0))) &&
          /^#[\da-f]{6}$/i.test(v.color) &&
          text(v.label) &&
          text(v.detail) &&
          Number.isInteger(v.step) &&
          v.step >= 0 &&
          v.step < s.steps.length,
      ),
      `${s.file}: 体素字段无效`,
    );
  }
  for (const m of models) {
    check(m.schemaVersion === 1, `${m.file}: model.schemaVersion 必须为 1`);
    check(
      m.x &&
        identifier(m.x.id) &&
        finite(m.x.min) &&
        finite(m.x.max) &&
        m.x.max > m.x.min &&
        Array.isArray(m.parameters) &&
        m.parameters.length <= 20,
      `${m.file}: 模型坐标无效`,
    );
    const names = new Set([m.x.id, ...m.parameters.map((p) => p.id)]);
    check(
      names.size === m.parameters.length + 1 &&
        m.parameters.every(
          (p) =>
            identifier(p.id) &&
            text(p.label) &&
            [p.min, p.max, p.step, p.value].every(finite) &&
            p.min < p.max &&
            p.step > 0 &&
            p.value >= p.min &&
            p.value <= p.max,
        ) &&
        text(m.formula) &&
        text(m.output) &&
        validExpression(m.expression, names),
      `${m.file}: 模型参数或表达式无效`,
    );
  }
  for (const r of renderers) {
    check(
      r.schemaVersion === 1 && text(r.entry),
      `${r.file}: 缺少 schemaVersion / entry`,
    );
    r.html = await readFile(await local(r.entry), "utf8");
  }
  for (const m of maps)
    check(validateMap(m, registry), `${m.file}: 画布字段或实体引用无效`);
  return registry;
}

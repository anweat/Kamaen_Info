import { readFile, writeFile, mkdir, readdir, cp } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { createHash } from "node:crypto";
const root = fileURLToPath(new URL("../../", import.meta.url));
const wiki = path.join(root, "wiki");
const source = path.join(root, "docs/system-rebuild");
const read = async (f) => readFile(path.join(source, f), "utf8");
const r4 = JSON.parse(await read("r4-stage-content.json"));
const graph = JSON.parse(await read("late-l3-tech-tree.json"));
const legacyGraph = JSON.parse(await read("review-tech-tree.json"));
const docs = [];
for (const file of (await readdir(source))
  .filter((f) => f.endsWith(".md"))
  .sort()) {
  const body = await read(file);
  const group = file.startsWith("LATE_L3_")
    ? "L3"
    : /^(DEVELOPMENT_PLAN|EARLY_DEVELOPMENT_FLOW|EARLY_F01_)/.test(file)
      ? "开发试作"
    : file.startsWith("EARLY_E1")
    ? "E1"
    : file.startsWith("R4_")
      ? "R4"
      : /^(REVIEW_|PROGRESSION_)/.test(file)
        ? "R1"
        : "历史 / 依据";
  docs.push({
    id: file,
    title: body.match(/^# (.+)/m)?.[1] || file,
    body,
    group,
  });
}
const e1 = [];
let section = 0;
const lines = (await read("EARLY_E1_CONTENT.md")).split(/\r?\n/);
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (/^## [1-4]\./.test(line)) section = Number(line[3]);
  else if (/^## /.test(line)) section = 0;
  if (!section || !line.startsWith("|")) continue;
  const cells = line
    .split("|")
    .slice(1, -1)
    .map((s) => s.trim());
  if (!/^E[0-5](\/E[0-5])*$/.test(cells[1])) continue;
  const legacy = cells[0].match(/`([^`]+)`/)?.[1];
  const name = cells[0]
    .replace(/`[^`]+`/g, "")
    .replace(/\*\*/g, "")
    .trim();
  e1.push({
    id: `e1:${legacy || "entry-" + createHash("sha256").update(name).digest("hex").slice(0, 10)}`,
    name,
    stage: cells[1],
    kind: ["", "原料 / 中间物", "构件 / 接口", "生产工位", "工具 / 数据"][
      section
    ],
    note: section === 1 ? cells[3] : cells[4],
    acquisition: cells[2],
    state: section === 1 ? cells[4] : "操作 / 配置：" + cells[3],
    source: "EARLY_E1_CONTENT.md",
    line: i + 1,
    version: "E1",
    legacy: legacy || "",
  });
}
const declaredCount = Number(
  (await read("EARLY_E1_CONTENT.md")).match(/目录共(\d+)条/)?.[1],
);
if (declaredCount && e1.length !== declaredCount)
  throw new Error(
    `E1 table changed: declares ${declaredCount}, parsed ${e1.length}; review importer.`,
  );
const items = [
  ...e1,
  ...r4.items.map((i) => ({
    ...i,
    id: `r4:${i.id}`,
    legacy: i.id,
    stage: `A${i.stage}`,
    version: "R4",
    source: "R4_MATERIALS_MACHINES.md",
    acquisition: "见关联的候选配方",
    state: "",
  })),
];
items.push(
  ...legacyGraph.dictionary_entities
    .filter((i) => Number(i.milestone.slice(1)) >= 16)
    .map((i) => ({
      id: `r1:${i.id}`,
      name: i.name.replace(/（原.*$/, ""),
      legacy: i.id,
      stage: i.milestone,
      kind: "后期内容候选",
      note: i.role,
      version: "R1",
      source: "REVIEW_CONTENT_COVERAGE.md",
      acquisition: "R1发展线预填充，具体配方待讨论。",
      state: "概念候选，非注册实体",
    })),
);
const ids = new Set(r4.items.map((i) => i.id));
for (const recipe of r4.recipes) {
  for (const id of [
    ...Object.keys(recipe.inputs),
    ...Object.keys(recipe.outputs),
    ...recipe.tools,
  ])
    if (!ids.has(id)) throw new Error(`Unknown item ${id}`);
  if (!r4.stations[recipe.station])
    throw new Error(`Unknown station ${recipe.station}`);
}
for (const node of graph.nodes)
  for (const id of node.requires_all)
    if (!graph.nodes.some((n) => n.id === id))
      throw new Error(`Unknown prerequisite ${id}`);
await mkdir(path.join(wiki, "src/generated"), { recursive: true });
await mkdir(path.join(wiki, "public/textures"), { recursive: true });
await cp(
  path.join(root, "src/main/resources/assets/kamaeninfo/textures"),
  path.join(wiki, "public/textures"),
  { recursive: true },
);
await writeFile(
  path.join(wiki, "src/generated/content.json"),
  JSON.stringify(
    {
      items,
      recipes: r4.recipes,
      stations: r4.stations,
      evidence: r4.evidence,
      nodes: graph.nodes,
      graphSource: { file: "late-l3-tech-tree.json", version: graph.version },
      docs,
    },
    null,
    2,
  ),
  "utf8",
);
console.log(
  `Synced ${e1.length} E1 + ${r4.items.length} R4 entries, ${r4.recipes.length} recipes, ${graph.nodes.length} capabilities, ${docs.length} documents. Source documents unchanged.`,
);

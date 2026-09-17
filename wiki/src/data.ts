import raw from "./generated/content.json";
export type Item = {
  id: string;
  name: string;
  stage: string;
  kind: string;
  note: string;
  acquisition: string;
  state: string;
  source: string;
  version: string;
  legacy: string;
  line?: number;
};
export type Recipe = {
  id: string;
  station: string;
  inputs: Record<string, number>;
  outputs: Record<string, number>;
  seconds: number;
  energy: number;
  tools: string[];
  evidence: string[];
};
export type Doc = { id: string; title: string; body: string; group: string };
export type Capability = {
  id: string;
  title: string;
  milestone: string;
  requires_all: string[];
  track: string;
  outcome: string;
};
export const data = raw as unknown as {
  items: Item[];
  recipes: Recipe[];
  nodes: Capability[];
  docs: Doc[];
  stations: Record<
    string,
    { name: string; item: string | null; modes: string }
  >;
  evidence: Record<
    string,
    { needs: string[]; objects: string[]; experiment: string }
  >;
};
export const href = (page: string, id?: string) =>
  `#/${page}${id ? "/" + encodeURIComponent(id) : ""}`;
export const itemById = (id: string) => data.items.find((i) => i.id === id);
export const itemName = (id: string) => itemById("r4:" + id)?.name || id;
export const chapters = [
  {
    id: "01",
    title: "从石头里，找到第一份差异",
    short: "发现与晶体",
    range: "P01—P05",
    version: "E1",
    file: "EARLY_E1_GAMEPLAY.md",
    story: "PROGRESSION_WORKING_DRAFT.md",
    description:
      "从普通生产出发，留下参考晶种。测量、冲击、特化，再让晶体回到产线。",
    items: [
      "e1:white_noise_seed",
      "e1:raw_kamaen_crystal",
      "e1:waveguide_kamaen_crystal",
    ],
    scene: "impact",
  },
  {
    id: "02",
    title: "让材料的响应成为功能",
    short: "材料与光电",
    range: "P06—P08",
    version: "R4",
    file: "R4_MODELS_AND_FACTORS.md",
    story: "PROGRESSION_02_MATERIALS_OPTOELECTRONICS.md",
    description: "在同一批晶片上试装门控与光路，用重复实验界定器件的工作窗口。",
    items: ["r4:gate", "r4:filter", "r4:reader"],
    scene: "impact",
  },
  {
    id: "03",
    title: "把一次实验，变成研究设施",
    short: "计算与发现",
    range: "P09—P15",
    version: "R4",
    file: "R4_STAGE_DESIGN.md",
    story: "PROGRESSION_03_COMPUTING_AND_DISCOVERY.md",
    description: "从封装芯片到两柜研究站，让数据、模型与下一次实验持续连接。",
    items: ["r4:endpoint_chip", "r4:populated_board", "r4:rack_node"],
    scene: "rack",
  },
  {
    id: "04",
    title: "向内测量，向外观测",
    short: "微观与宇观",
    range: "P16—P22",
    version: "R1",
    file: "PROGRESSION_04_MICRO_AND_COSMOS.md",
    story: "PROGRESSION_04_MICRO_AND_COSMOS.md",
    description: "低温材料与远方谱线沿两条路径前进，最终约束同一个未知量。",
    items: [],
    scene: "rack",
  },
  {
    id: "05",
    title: "一个世界，以及它的边界",
    short: "边界与创世",
    range: "P23—P28",
    version: "R1",
    file: "PROGRESSION_05_BOUNDARY_AND_GENESIS.md",
    story: "PROGRESSION_05_BOUNDARY_AND_GENESIS.md",
    description: "从戈古尔斯弦、可停止的视界，到能够点燃并持续维护的新世界。",
    items: [],
    scene: "impact",
  },
];
export function textureFor(item: Item) {
  if (/粗卡玛恩晶体/.test(item.name)) return "item/item_kamaen_crystal_raw.png";
  if (/导波型|稳谱型|偏振|抗压型/.test(item.name))
    return "item/item_kamaen_crystal_tuned.png";
  if (/信息探针/.test(item.name)) return "item/item_info_probe.png";
  if (/分馏塔/.test(item.name))
    return "block/block_fractionating_tower_front.png";
  if (/爆炸室/.test(item.name))
    return "block/block_explosion_chamber_controller_front.png";
  return null;
}

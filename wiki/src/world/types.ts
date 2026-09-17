export type Point = { x: number; y: number };
export type Expression =
  | number
  | string
  | {
      op: "add" | "sub" | "mul" | "div" | "pow" | "sin" | "exp";
      args: Expression[];
    };
export type ModelSpec = {
  formula: string;
  x: { id: string; label: string; min: number; max: number };
  parameters: {
    id: string;
    label: string;
    min: number;
    max: number;
    step: number;
    value: number;
  }[];
  expression: Expression;
  output: string;
};
export type Entity = {
  schemaVersion: 1;
  id: string;
  kind: "item" | "block" | "multiblock" | "nbt" | "model";
  title: string;
  summary: string;
  status: string;
  tags: string[];
  body: string;
  file: string;
  description?: string;
  designRefs?: { document: string; label: string; legacyId?: string }[];
  runtimeRef?: string | null;
  lifecycle?: { design: string; runtime: string; art: string; verification: string };
  visual?: {
    type: "sprite" | "block";
    asset?: string;
    color?: string;
    top?: string;
    side?: string;
  };
  relations?: { target: string; label: string }[];
  gallery?: { asset: string; caption: string }[];
  scene?: string;
  model?: string;
  renderer?: string;
  fields?: {
    name: string;
    type: string;
    default: unknown;
    description: string;
  }[];
};
export type MapNode = {
  id: string;
  type:
    | "entity"
    | "text"
    | "arrow"
    | "line"
    | "rect"
    | "pen"
    | "space3d"
    | "space2d"
    | "custom";
  x: number;
  y: number;
  width: number;
  height: number;
  title?: string;
  body?: string;
  ref?: string;
  color?: string;
  fontSize?: number;
  points?: Point[];
  from?: string;
  to?: string;
};
export type WorldMap = {
  schemaVersion: 1;
  id: string;
  title: string;
  revision: number;
  nodes: MapNode[];
};
export type RendererSpec = {
  id: string;
  title: string;
  html: string;
  file: string;
};
export type Registry = {
  entities: Entity[];
  maps: WorldMap[];
  assets: Record<string, string>;
  scenes: import("../scenes").SceneSpec[];
  models: (ModelSpec & { id: string; title: string })[];
  renderers: RendererSpec[];
};

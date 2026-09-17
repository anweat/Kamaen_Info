export type CanvasNode = {
  id: string;
  type: "cluster" | "text" | "scene" | "recipe";
  title: string;
  chapter: string;
  x: number;
  y: number;
  width: number;
  height: number;
  collapsed: boolean;
  body: string;
  source: string;
  scene: string;
  recipe: string;
  groups: { title: string; items: string[] }[];
};
export type CanvasEdge = {
  from: string;
  to: string;
  label: string;
  kind: "story" | "feedback";
};
export type CanvasDocument = {
  revision: number;
  nodes: CanvasNode[];
  edges: CanvasEdge[];
  openItems?: Record<string, string>;
  baseHeights?: Record<string, number>;
};
export const clamp = (v: number, min: number, max: number) =>
  Math.max(min, Math.min(max, v));

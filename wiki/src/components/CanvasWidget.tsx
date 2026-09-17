import { Grip, Minus, Plus, Pencil, Expand, ArrowUpRight } from "lucide-react";
import { data, href, itemById } from "../data";
import type { CanvasNode } from "../canvas-types";
import ItemVisual from "./ItemVisual";
import Markdown from "./Markdown";
import SceneViewer from "./SceneViewer";
import { RecipeCard } from "./Catalog";
import { useLayoutEffect, useRef } from "react";
import CanvasItemDetails from "./CanvasItemDetails";
export default function CanvasWidget({
  node,
  selected,
  move,
  resize,
  patch,
  edit,
  pick,
  select,
  activeItem,
  autoSize,
  onAutoHeight,
  guide,
}: {
  node: CanvasNode;
  selected: boolean;
  move: (e: React.PointerEvent, node: CanvasNode) => void;
  resize: (e: React.PointerEvent, node: CanvasNode) => void;
  patch: (id: string, value: Partial<CanvasNode>) => void;
  edit: () => void;
  pick: (id: string) => void;
  select: () => void;
  activeItem?: string;
  autoSize: boolean;
  onAutoHeight: (height: number) => void;
  guide: (id: string) => void;
}) {
  const inner = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    if (activeItem && autoSize && inner.current)
      onAutoHeight(inner.current.scrollHeight + 78);
  }, [activeItem, autoSize, node.width, node.groups, node.body]);
  const total = node.groups.reduce((sum, g) => sum + g.items.length, 0);
  const recipe = data.recipes.find((r) => r.id === node.recipe);
  return (
    <section
      className={`canvas-widget widget-${node.type} chapter-color-${node.chapter || "01"} ${selected ? "widget-selected" : ""} ${node.collapsed ? "collapsed" : ""}`}
      style={{
        left: node.x,
        top: node.y,
        width: node.width,
        height: node.collapsed ? 58 : node.height,
      }}
      aria-label={node.title}
      onPointerDown={select}
    >
      <div
        className="widget-topline"
        onPointerDown={(e) => {
          if (!(e.target as HTMLElement).closest("button")) move(e, node);
        }}
      >
        <button
          className="widget-grip"
          aria-label={`移动${node.title}，方向键调整`}
          onPointerDown={(e) => move(e, node)}
          onKeyDown={(e) => {
            const keys: Record<string, [number, number]> = {
              ArrowLeft: [-20, 0],
              ArrowRight: [20, 0],
              ArrowUp: [0, -20],
              ArrowDown: [0, 20],
            };
            if (keys[e.key]) {
              e.preventDefault();
              patch(node.id, {
                x: node.x + keys[e.key][0],
                y: node.y + keys[e.key][1],
              });
            }
          }}
        >
          <Grip size={13} />
        </button>
        <span className="widget-type">
          {node.type === "cluster"
            ? "CHAPTER " + node.chapter
            : node.type === "text"
              ? "FIELD NOTE"
              : node.type === "scene"
                ? "3D SCENE"
                : "RECIPE"}
        </span>
        <div className="widget-actions">
          <button
            title="编辑组件内容"
            aria-label={`编辑${node.title}`}
            onClick={edit}
          >
            <Pencil size={13} />
          </button>
          <button
            title="展开或收起"
            aria-label={`${node.collapsed ? "展开" : "收起"}${node.title}`}
            onClick={() => patch(node.id, { collapsed: !node.collapsed })}
          >
            {node.collapsed ? <Plus size={14} /> : <Minus size={14} />}
          </button>
        </div>
      </div>
      {node.collapsed ? (
        <div className="collapsed-title">
          {node.title}
          <span>{total ? `${total} 个对象` : ""}</span>
        </div>
      ) : (
        <div className="widget-body">
          <div ref={inner}>
            <div className="widget-title">
              <h2>{node.title}</h2>
              {node.type === "cluster" && (
                <span>{total.toString().padStart(2, "0")}</span>
              )}
            </div>
            {node.type === "text" ? (
              <Markdown>{node.body}</Markdown>
            ) : (
              <p className="widget-description">{node.body}</p>
            )}
            {node.type === "cluster" && (
              <div className="cluster-groups">
                {node.groups.map((group, index) => (
                  <div className="cluster-group" key={index}>
                    <h3>
                      {group.title}
                      <span>{group.items.length}</span>
                    </h3>
                    <div className="cluster-sprites">
                      {group.items.map((id, i) => {
                        const item = itemById(id);
                        return item ? (
                          <button
                            className={`cluster-sprite ${activeItem === id ? "sprite-active" : ""}`}
                            aria-expanded={activeItem === id}
                            key={`${id}-${i}`}
                            aria-label={`查看${item.name}`}
                            onClick={() => pick(id)}
                          >
                            <ItemVisual item={item} />
                            <span>{item.name}</span>
                            <span className="sprite-hover">
                              <strong>{item.name}</strong>
                              <small>
                                {item.stage} · {item.kind}
                              </small>
                              {item.note}
                            </span>
                          </button>
                        ) : (
                          <span className="missing-sprite" key={id}>
                            待补
                            <br />
                            {id}
                          </span>
                        );
                      })}
                    </div>
                    {activeItem &&
                      group.items.includes(activeItem) &&
                      itemById(activeItem) && (
                        <CanvasItemDetails
                          item={itemById(activeItem)!}
                          close={() => pick(activeItem)}
                          guide={guide}
                        />
                      )}
                  </div>
                ))}
              </div>
            )}
            {node.type === "scene" && (
              <SceneViewer key={node.scene} sceneId={node.scene} compact />
            )}
            {node.type === "recipe" &&
              (recipe ? (
                <RecipeCard recipe={recipe} full />
              ) : (
                <p className="muted">在组件设置中选择一条配方。</p>
              ))}
            {node.source && (
              <a className="widget-source" href={href("docs", node.source)}>
                展开来源与完整说明 <ArrowUpRight size={12} />
              </a>
            )}
          </div>
        </div>
      )}
      {!node.collapsed && (
        <button
          className="widget-resize"
          aria-label={`调整${node.title}大小，方向键调整`}
          onPointerDown={(e) => resize(e, node)}
          onKeyDown={(e) => {
            const keys: Record<string, [number, number]> = {
              ArrowLeft: [-40, 0],
              ArrowRight: [40, 0],
              ArrowUp: [0, -40],
              ArrowDown: [0, 40],
            };
            if (keys[e.key]) {
              e.preventDefault();
              patch(node.id, {
                width: Math.max(260, node.width + keys[e.key][0]),
                height: Math.max(120, node.height + keys[e.key][1]),
              });
            }
          }}
        >
          <Expand size={12} />
        </button>
      )}
    </section>
  );
}

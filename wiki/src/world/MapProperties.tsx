import { useState } from "react";
import { X, Trash2, Copy, ArrowUp, ArrowDown } from "lucide-react";
import type { MapNode } from "./types";
import registry from "./registry";
import { resizeNode } from "./geometry";
export default function MapProperties({
  node,
  nodes,
  onApply,
  onClose,
  onDelete,
  onDuplicate,
  onLayer,
}: {
  node: MapNode;
  nodes: MapNode[];
  onApply: (node: MapNode) => void;
  onClose: () => void;
  onDelete: () => void;
  onDuplicate: () => void;
  onLayer: (top: boolean) => void;
}) {
  const [draft, setDraft] = useState(node);
  const options = {
    entity: registry.entities,
    space3d: registry.scenes,
    space2d: registry.models,
    custom: registry.renderers,
  }[node.type as "entity" | "space3d" | "space2d" | "custom"];
  return (
    <aside className="map-properties" aria-label="组件属性">
      <header>
        <strong>组件属性</strong>
        <button aria-label="关闭组件属性" onClick={onClose}>
          <X size={16} />
        </button>
      </header>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onApply(draft);
        }}
      >
        <small>
          {node.type} · {node.id}
        </small>
        <label>
          标注标题
          <input
            value={draft.title || ""}
            maxLength={200}
            onChange={(e) => setDraft({ ...draft, title: e.target.value })}
          />
        </label>
        {options && (
          <label>
            引用文件
            <select
              value={draft.ref}
              onChange={(e) => setDraft({ ...draft, ref: e.target.value })}
            >
              {options.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.title}
                </option>
              ))}
            </select>
          </label>
        )}
        {node.type === "text" && (
          <>
            <label>
              正文
              <textarea
                rows={5}
                value={draft.body || ""}
                onChange={(e) => setDraft({ ...draft, body: e.target.value })}
              />
            </label>
            <label>
              字号
              <input
                type="number"
                min="10"
                max="120"
                value={draft.fontSize || 18}
                onChange={(e) =>
                  setDraft({ ...draft, fontSize: Number(e.target.value) })
                }
              />
            </label>
          </>
        )}
        <div className="map-numeric">
          {(["x", "y", "width", "height"] as const).map((k) => (
            <label key={k}>
              {{ x: "X", y: "Y", width: "宽", height: "高" }[k]}
              <input
                required
                type="number"
                step="any"
                min={k === "width" || k === "height" ? 1 : -100000}
                max={k === "width" || k === "height" ? 10000 : 100000}
                value={draft[k]}
                onChange={(e) => {
                  const value = Number(e.target.value);
                  setDraft(
                    k === "width" || k === "height"
                      ? resizeNode(
                          draft,
                          k === "width" ? value : draft.width,
                          k === "height" ? value : draft.height,
                        )
                      : { ...draft, [k]: value },
                  );
                }}
              />
            </label>
          ))}
        </div>
        {["text", "rect", "pen", "line", "arrow"].includes(node.type) && (
          <label>
            颜色
            <input
              type="color"
              value={draft.color || "#829076"}
              onChange={(e) => setDraft({ ...draft, color: e.target.value })}
            />
          </label>
        )}
        {["line", "arrow"].includes(node.type) &&
          (["from", "to"] as const).map((k) => (
            <label key={k}>
              {k === "from" ? "起点跟随" : "终点跟随"}
              <select
                value={draft[k] || ""}
                onChange={(e) =>
                  setDraft({ ...draft, [k]: e.target.value || undefined })
                }
              >
                <option value="">自由端点</option>
                {nodes
                  .filter(
                    (n) =>
                      n.id !== node.id &&
                      !["line", "arrow", "pen", "rect"].includes(n.type),
                  )
                  .map((n) => (
                    <option key={n.id} value={n.id}>
                      {n.title || n.ref || n.id}
                    </option>
                  ))}
              </select>
            </label>
          ))}
        <button className="primary" type="submit">
          应用修改
        </button>
      </form>
      <div className="map-property-actions">
        <button onClick={onDuplicate}>
          <Copy size={15} />
          复制
        </button>
        <button onClick={() => onLayer(true)}>
          <ArrowUp size={15} />
          置顶
        </button>
        <button onClick={() => onLayer(false)}>
          <ArrowDown size={15} />
          置底
        </button>
        <button onClick={onDelete}>
          <Trash2 size={15} />
          删除
        </button>
      </div>
      <small>坐标不吸附格点。框线是标注，不承载内部对象。</small>
    </aside>
  );
}

import { useState } from "react";
import { X, Plus, Check } from "lucide-react";
import { data, itemById } from "../data";
import type { CanvasNode } from "../canvas-types";
import ItemVisual from "./ItemVisual";

import { scenes } from "../scenes";
export function CanvasNodeEditor({
  node,
  apply,
  close,
}: {
  node: CanvasNode;
  apply: (node: CanvasNode) => void;
  close: () => void;
}) {
  const [draft, setDraft] = useState<CanvasNode>(structuredClone(node));
  const [query, setQuery] = useState("");
  const [targetGroup, setTargetGroup] = useState(0);
  const results = query
    ? data.items
        .filter((i) =>
          `${i.name} ${i.id}`.toLowerCase().includes(query.toLowerCase()),
        )
        .slice(0, 35)
    : data.items.filter((i) => i.version === "E1").slice(15, 35);
  const update = (value: Partial<CanvasNode>) =>
    setDraft((d) => ({ ...d, ...value }));
  return (
    <aside className="canvas-inspector node-editor" aria-label="组件设置">
      <header>
        <span>COMPONENT / 组件设置</span>
        <button aria-label="关闭组件设置" onClick={close}>
          <X size={17} />
        </button>
      </header>
      <form
        className="inspector-scroll"
        onSubmit={(e) => {
          e.preventDefault();
          apply(draft);
        }}
      >
        <label>
          组件标题
          <input
            value={draft.title}
            maxLength={200}
            required
            onChange={(e) => update({ title: e.target.value })}
          />
        </label>
        <label>
          说明 / 故事正文 · Markdown
          <textarea
            rows={5}
            value={draft.body}
            maxLength={50000}
            onChange={(e) => update({ body: e.target.value })}
          />
        </label>
        <div className="editor-size">
          <label>
            宽度
            <input
              type="number"
              min={260}
              max={1400}
              value={draft.width}
              onChange={(e) => update({ width: Number(e.target.value) })}
            />
          </label>
          <label>
            高度
            <input
              type="number"
              min={120}
              max={1600}
              value={draft.height}
              onChange={(e) => update({ height: Number(e.target.value) })}
            />
          </label>
        </div>
        <label>
          关联文档
          <select
            value={draft.source}
            onChange={(e) => update({ source: e.target.value })}
          >
            <option value="">不关联</option>
            {data.docs.map((d) => (
              <option key={d.id} value={d.id}>
                {d.title}
              </option>
            ))}
          </select>
        </label>
        {draft.type === "scene" && (
          <label>
            演示场景
            <select
              value={draft.scene}
              onChange={(e) => update({ scene: e.target.value })}
            >
              {scenes.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.title}
                </option>
              ))}
            </select>
          </label>
        )}
        {draft.type === "recipe" && (
          <label>
            配方
            <select
              value={draft.recipe}
              onChange={(e) => update({ recipe: e.target.value })}
            >
              {data.recipes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.id}
                </option>
              ))}
            </select>
          </label>
        )}
        {draft.type === "cluster" && (
          <>
            <h3>团簇里的分组</h3>
            {draft.groups.map((g, index) => (
              <div className="group-editor" key={index}>
                <input
                  aria-label={`第${index + 1}组名称`}
                  value={g.title}
                  maxLength={200}
                  onChange={(e) =>
                    update({
                      groups: draft.groups.map((v, i) =>
                        i === index ? { ...v, title: e.target.value } : v,
                      ),
                    })
                  }
                />
                <div className="chosen-sprites">
                  {g.items.map((id, i) => {
                    const item = itemById(id);
                    return (
                      <button
                        type="button"
                        key={id + i}
                        title={`移除${item?.name || id}`}
                        aria-label={`从分组移除${item?.name || id}`}
                        onClick={() =>
                          update({
                            groups: draft.groups.map((v, n) =>
                              n === index
                                ? {
                                    ...v,
                                    items: v.items.filter((_, k) => k !== i),
                                  }
                                : v,
                            ),
                          })
                        }
                      >
                        {item && <ItemVisual item={item} />}
                        <span>×</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={() =>
                update({
                  groups: [...draft.groups, { title: "新的分组", items: [] }],
                })
              }
            >
              <Plus size={13} />
              添加分组
            </button>
            <label>
              将物品加入
              <select
                value={targetGroup}
                onChange={(e) => setTargetGroup(Number(e.target.value))}
              >
                {draft.groups.map((g, i) => (
                  <option key={i} value={i}>
                    {g.title}
                  </option>
                ))}
              </select>
            </label>
            <input
              aria-label="搜索要添加的物品"
              placeholder="搜索物品名称或 ID…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="item-picker">
              {results.map((i) => (
                <button
                  type="button"
                  key={i.id}
                  disabled={
                    !draft.groups[targetGroup] ||
                    draft.groups[targetGroup].items.includes(i.id)
                  }
                  onClick={() =>
                    update({
                      groups: draft.groups.map((g, index) =>
                        index === targetGroup
                          ? { ...g, items: [...g.items, i.id] }
                          : g,
                      ),
                    })
                  }
                >
                  <ItemVisual item={i} />
                  <span>
                    {i.name}
                    <small>{i.version}</small>
                  </span>
                  <Plus size={12} />
                </button>
              ))}
            </div>
          </>
        )}
        <button type="submit" className="primary editor-apply">
          <Check size={15} />
          应用到画布
        </button>
        <p className="small muted">应用后点击画布“保存”，记录到项目文件。</p>
      </form>
    </aside>
  );
}

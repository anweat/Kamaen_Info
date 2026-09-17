import {
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from "react";
import {
  Plus,
  Minus,
  Maximize,
  Save,
  Undo2,
  Download,
  Link2,
  X,
  Check,
  Move,
  Grid3X3,
  Layers3,
  NotebookPen,
  GitBranch,
  Compass,
} from "lucide-react";
import seed from "../../content/canvas.json";
import { data, chapters } from "../data";
import { clamp, type CanvasDocument, type CanvasNode } from "../canvas-types";
import { resizeInFlow, canvasBounds } from "../canvas-layout";
import CanvasWidget from "./CanvasWidget";
import { CanvasNodeEditor } from "./CanvasInspector";
const cacheKey = "kamaen-canvas-draft-v1";
const initial = seed as CanvasDocument;
export default function CanvasPage() {
  const [doc, setDoc] = useState<CanvasDocument>(initial);
  const [view, setView] = useState({ x: 35, y: 60, zoom: 0.78 });
  const viewRef = useRef(view);
  viewRef.current = view;
  const [ready, setReady] = useState(false);
  const [local, setLocal] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const [editor, setEditor] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);
  const [linking, setLinking] = useState(false);
  const [history, setHistory] = useState<CanvasDocument[]>([]);
  const [expanded, setExpanded] = useState<Record<string, string>>({});
  const [autosize, setAutosize] = useState<Record<string, boolean>>({});
  const baseHeights = useRef<Record<string, number>>({});
  const stage = useRef<HTMLDivElement>(null);
  const [link, setLink] = useState({
    from: "chapter-1",
    to: "chapter-2",
    label: "新的发展线索",
    kind: "story" as "story" | "feedback",
  });
  const liveDoc = useRef(doc);
  liveDoc.current = doc;
  useEffect(() => {
    let active = true;
    fetch("./api/canvas")
      .then(async (r) => {
        if (
          !r.ok ||
          !r.headers.get("content-type")?.includes("application/json")
        )
          throw Error();
        return r.json();
      })
      .then((server) => {
        if (!active) return;
        let next = server;
        try {
          const cached = JSON.parse(localStorage.getItem(cacheKey) || "null");
          if (cached && cached.revision === server.revision) {
            next = cached;
            setDirty(true);
            setMessage("已恢复上次未保存的画布布局。");
          } else if (cached)
            setMessage(
              "项目画布已有更新，已加载项目版本；旧草稿仍保留在浏览器。",
            );
        } catch {}
        setDoc(next);
        setExpanded(next.openItems || {});
        baseHeights.current = next.baseHeights || {};
      })
      .catch(() => {
        if (!active) return;
        setLocal(true);
        try {
          const next =
            JSON.parse(localStorage.getItem(cacheKey) || "null") || initial;
          setDoc(next);
          setExpanded(next.openItems || {});
          baseHeights.current = next.baseHeights || {};
        } catch {}
      })
      .finally(() => {
        if (active) setReady(true);
      });
    return () => {
      active = false;
    };
  }, []);
  useEffect(() => {
    if (dirty && ready) {
      try {
        localStorage.setItem(
          cacheKey,
          JSON.stringify({
            ...doc,
            openItems: expanded,
            baseHeights: baseHeights.current,
          }),
        );
      } catch {
        setMessage("草稿缓存失败，请及时保存或导出。");
      }
    }
  }, [doc, dirty, ready, expanded]);
  function checkpoint() {
    setHistory((h) => [
      ...h.slice(-29),
      structuredClone({
        ...liveDoc.current,
        openItems: expanded,
        baseHeights: baseHeights.current,
      }),
    ]);
  }
  function change(
    updater: (d: CanvasDocument) => CanvasDocument,
    record = true,
  ) {
    if (record) checkpoint();
    setDoc((d) => updater(d));
    setDirty(true);
  }
  function patch(id: string, value: Partial<CanvasNode>, record = true) {
    change(
      (d) => ({
        ...d,
        nodes: d.nodes.map((n) =>
          n.id === id
            ? {
                ...n,
                ...value,
                x: clamp(value.x ?? n.x, -10000, 10000),
                y: clamp(value.y ?? n.y, -10000, 10000),
                width: clamp(value.width ?? n.width, 260, 1400),
                height: clamp(value.height ?? n.height, 120, 1600),
              }
            : n,
        ),
      }),
      record,
    );
  }
  function fit(nodes = liveDoc.current.nodes) {
    const bounds = canvasBounds(nodes);
    const width = stage.current?.clientWidth || 1000,
      height = stage.current?.clientHeight || 700;
    const zoom = clamp(
      Math.min(
        (width - 100) / (bounds.right - bounds.left),
        (height - 90) / (bounds.bottom - bounds.top),
      ),
      0.22,
      1.25,
    );
    setView({
      zoom,
      x: (width - (bounds.right - bounds.left) * zoom) / 2 - bounds.left * zoom,
      y: (height - (bounds.bottom - bounds.top) * zoom) / 2 - bounds.top * zoom,
    });
  }
  function focusNode(id: string) {
    const n = liveDoc.current.nodes.find((n) => n.id === id);
    if (!n) return;
    setSelected(id);
    const width = stage.current?.clientWidth || 1000;
    const z = width < 600 ? 0.78 : 0.95;
    setView({
      zoom: z,
      x: Math.max(25, (width - n.width * z) / 2) - n.x * z,
      y: 70 - n.y * z,
    });
  }
  function zoomBy(factor: number) {
    setView((v) => {
      const width = stage.current?.clientWidth || 1000,
        height = stage.current?.clientHeight || 700,
        z = clamp(v.zoom * factor, 0.22, 1.65);
      return {
        x: width / 2 - ((width / 2 - v.x) * z) / v.zoom,
        y: height / 2 - ((height / 2 - v.y) * z) / v.zoom,
        zoom: z,
      };
    });
  }
  useEffect(() => {
    const host = stage.current;
    if (!host) return;
    const wheel = (e: WheelEvent) => {
      if ((e.target as HTMLElement).closest(".widget-body") && !e.ctrlKey)
        return;
      e.preventDefault();
      const rect = host.getBoundingClientRect();
      const x = e.clientX - rect.left,
        y = e.clientY - rect.top;
      setView((v) => {
        const z = clamp(v.zoom * Math.exp(-e.deltaY * 0.0015), 0.22, 1.65);
        return {
          x: x - ((x - v.x) * z) / v.zoom,
          y: y - ((y - v.y) * z) / v.zoom,
          zoom: z,
        };
      });
    };
    host.addEventListener("wheel", wheel, { passive: false });
    return () => host.removeEventListener("wheel", wheel);
  }, []);
  function gesture(
    e: ReactPointerEvent,
    node: CanvasNode | null,
    mode: "pan" | "move" | "resize",
  ) {
    if (e.button !== 0 || !ready) return;
    e.preventDefault();
    e.stopPropagation();
    const target = e.currentTarget as HTMLElement;
    target.setPointerCapture(e.pointerId);
    const start = {
      x: e.clientX,
      y: e.clientY,
      view: viewRef.current,
      node: node ? { ...node } : null,
    };
    if (node) {
      checkpoint();
      setSelected(node.id);
      if (mode === "resize") setAutosize((a) => ({ ...a, [node.id]: false }));
    }
    const onMove = (event: PointerEvent) => {
      const dx = event.clientX - start.x,
        dy = event.clientY - start.y;
      if (mode === "pan") {
        setView({ ...start.view, x: start.view.x + dx, y: start.view.y + dy });
        return;
      }
      if (!start.node) return;
      const n = start.node;
      if (mode === "move")
        patch(
          n.id,
          { x: n.x + dx / start.view.zoom, y: n.y + dy / start.view.zoom },
          false,
        );
      else
        patch(
          n.id,
          {
            width: n.width + dx / start.view.zoom,
            height: n.height + dy / start.view.zoom,
          },
          false,
        );
    };
    const stop = () => {
      target.removeEventListener("pointermove", onMove);
      target.removeEventListener("pointerup", stop);
      target.removeEventListener("pointercancel", stop);
    };
    target.addEventListener("pointermove", onMove);
    target.addEventListener("pointerup", stop);
    target.addEventListener("pointercancel", stop);
  }
  function toggleItem(nodeId: string, itemId: string) {
    const n = liveDoc.current.nodes.find((n) => n.id === nodeId)!;
    setSelected(nodeId);
    checkpoint();
    if (expanded[nodeId] === itemId) {
      setExpanded((e) => {
        const next = { ...e };
        delete next[nodeId];
        return next;
      });
      if (baseHeights.current[nodeId]) {
        const restoredHeight = baseHeights.current[nodeId];
        setDoc((d) => resizeInFlow(d, nodeId, restoredHeight));
        delete baseHeights.current[nodeId];
        setDirty(true);
      }
    } else {
      if (!expanded[nodeId]) baseHeights.current[nodeId] = n.height;
      setExpanded((e) => ({ ...e, [nodeId]: itemId }));
      setAutosize((e) => ({ ...e, [nodeId]: true }));
    }
  }
  function guide(itemId: string) {
    const n = liveDoc.current.nodes.find((n) =>
      n.groups.some((g) => g.items.includes(itemId)),
    );
    if (n) {
      if (n.collapsed) patch(n.id, { collapsed: false });
      focusNode(n.id);
      if (expanded[n.id] !== itemId) toggleItem(n.id, itemId);
      setMessage("已定位关联对象，在对应团簇内展开。");
    } else {
      add("cluster", itemId);
      setMessage("关联对象尚未放入画布，已创建一个可编辑的补充团簇。");
    }
  }
  function add(type: CanvasNode["type"], itemId?: string) {
    const width = stage.current?.clientWidth || 1000,
      height = stage.current?.clientHeight || 700,
      v = viewRef.current;
    const node: CanvasNode = {
      id: crypto.randomUUID(),
      type,
      title:
        type === "cluster"
          ? "新的物品团簇"
          : type === "text"
            ? "一条新的想法"
            : type === "scene"
              ? "新的结构演示"
              : "新的配方组件",
      chapter: "",
      x: (width / 2 - v.x) / v.zoom - 190,
      y: (height / 2 - v.y) / v.zoom - 120,
      width: 400,
      height: type === "scene" ? 490 : 320,
      collapsed: false,
      body: "在这里记录这组内容之间的关系。",
      source: "",
      scene: "impact",
      recipe: "endpoint_chip",
      groups:
        type === "cluster"
          ? [{ title: "新的分组", items: itemId ? [itemId] : [] }]
          : [],
    };
    change((d) => ({ ...d, nodes: [...d.nodes, node] }));
    setAdding(false);
    setSelected(node.id);
    if (!itemId) setEditor(node.id);
  }
  function undo() {
    const previous = history.at(-1);
    if (!previous) return;
    setDoc({ ...previous, revision: liveDoc.current.revision });
    setHistory((h) => h.slice(0, -1));
    setExpanded(previous.openItems || {});
    baseHeights.current = previous.baseHeights || {};
    setAutosize({});
    setDirty(true);
  }
  async function save() {
    setSaving(true);
    try {
      if (local) {
        localStorage.setItem(
          cacheKey,
          JSON.stringify({
            ...doc,
            openItems: expanded,
            baseHeights: baseHeights.current,
          }),
        );
        setMessage("布局已保存到当前浏览器，请导出 JSON 备份。");
      } else {
        const r = await fetch("./api/canvas", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ...doc,
            openItems: expanded,
            baseHeights: baseHeights.current,
          }),
        });
        const next = await r.json();
        if (!r.ok) throw Error(next.error || "保存失败");
        setDoc(next);
        localStorage.removeItem(cacheKey);
        setMessage("已保存到项目 wiki/content/canvas.json。");
      }
      setDirty(false);
    } catch (e) {
      setMessage(String(e));
    } finally {
      setSaving(false);
    }
  }
  function exportLayout() {
    const url = URL.createObjectURL(
      new Blob(
        [
          JSON.stringify(
            { ...doc, openItems: expanded, baseHeights: baseHeights.current },
            null,
            2,
          ),
        ],
        { type: "application/json" },
      ),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "kamaen-canvas.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  const bounds = canvasBounds(doc.nodes);
  const minimapScale = 180 / (bounds.right - bounds.left);
  const editNode = doc.nodes.find((n) => n.id === editor);
  return (
    <div className="canvas-page">
      <div className="canvas-toolbar">
        <div className="canvas-heading">
          <span className="live-dot" />
          <strong>世界的线索</strong>
          <span>章节与物品画布</span>
        </div>
        <div className="canvas-tools">
          <button
            aria-label="添加画布组件"
            onClick={() => setAdding((v) => !v)}
            disabled={!ready}
          >
            <Plus size={15} />
            组件
          </button>
          <button
            title="添加故事线或反馈线"
            aria-label="添加连线"
            onClick={() => setLinking((v) => !v)}
          >
            <Link2 size={15} />
          </button>
          <button
            title="撤销布局更改"
            aria-label="撤销布局更改"
            disabled={!history.length}
            onClick={undo}
          >
            <Undo2 size={15} />
          </button>
          <button title="导出画布" aria-label="导出画布" onClick={exportLayout}>
            <Download size={15} />
          </button>
          <button
            className="primary"
            disabled={!ready || saving}
            onClick={save}
          >
            <Save size={14} />
            {saving ? "保存中" : "保存"}
            {dirty && " ·"}
          </button>
        </div>
      </div>
      <div className="canvas-chapter-bar">
        <span>发展线</span>
        {chapters.map((c) => (
          <button
            key={c.id}
            onClick={() => focusNode("chapter-" + Number(c.id))}
          >
            {c.id}
            <span>{c.short}</span>
          </button>
        ))}
        <button
          className="all-chapters"
          onClick={() => fit(doc.nodes.filter((n) => n.type === "cluster"))}
        >
          <Compass size={13} />
          整条主线
        </button>
      </div>
      {adding && (
        <div className="canvas-add-menu">
          {(
            [
              { type: "cluster", title: "物品贴图团簇", icon: Grid3X3 },
              { type: "text", title: "故事 / 研究文字", icon: NotebookPen },
              { type: "scene", title: "可交互结构", icon: Layers3 },
              { type: "recipe", title: "配方与工艺", icon: GitBranch },
            ] as const
          ).map((t) => (
            <button key={t.type} onClick={() => add(t.type)}>
              <t.icon size={18} />
              <span>{t.title}</span>
              <Plus size={13} />
            </button>
          ))}
        </div>
      )}
      {linking && (
        <form
          className="canvas-link-form"
          onSubmit={(e) => {
            e.preventDefault();
            if (link.from === link.to)
              return setMessage("请选择不同的两个组件。");
            change((d) => ({ ...d, edges: [...d.edges, link] }));
            setLinking(false);
          }}
        >
          <header>
            连接两组内容
            <button
              type="button"
              aria-label="关闭连线设置"
              onClick={() => setLinking(false)}
            >
              <X size={14} />
            </button>
          </header>
          <label>
            起点
            <select
              value={link.from}
              onChange={(e) => setLink({ ...link, from: e.target.value })}
            >
              {doc.nodes.map((n) => (
                <option value={n.id} key={n.id}>
                  {n.title}
                </option>
              ))}
            </select>
          </label>
          <label>
            终点
            <select
              value={link.to}
              onChange={(e) => setLink({ ...link, to: e.target.value })}
            >
              {doc.nodes.map((n) => (
                <option value={n.id} key={n.id}>
                  {n.title}
                </option>
              ))}
            </select>
          </label>
          <label>
            关系说明
            <input
              value={link.label}
              maxLength={200}
              onChange={(e) => setLink({ ...link, label: e.target.value })}
            />
          </label>
          <label>
            线条语义
            <select
              value={link.kind}
              onChange={(e) =>
                setLink({
                  ...link,
                  kind: e.target.value as "story" | "feedback",
                })
              }
            >
              <option value="story">发展线 / 实线</option>
              <option value="feedback">研究反馈 / 虚线</option>
            </select>
          </label>
          <button type="submit" className="primary">
            <Check size={14} />
            添加连线
          </button>
        </form>
      )}
      <div
        ref={stage}
        className="canvas-stage"
        aria-label="可缩放的章节物品画布"
        style={{
          backgroundSize: `${24 * view.zoom}px ${24 * view.zoom}px`,
          backgroundPosition: `${view.x}px ${view.y}px`,
        }}
        onPointerDown={(e) => {
          if (
            !(e.target as HTMLElement).closest(
              ".canvas-widget,.canvas-controls,.canvas-minimap,.canvas-message",
            )
          )
            gesture(e, null, "pan");
        }}
      >
        <div
          className="canvas-world"
          style={{
            transform: `translate(${view.x}px,${view.y}px) scale(${view.zoom})`,
          }}
        >
          <svg className="canvas-edges" aria-label="章节关系线">
            <defs>
              <marker
                id="edge-arrow"
                markerWidth="7"
                markerHeight="7"
                refX="6"
                refY="3.5"
                orient="auto"
              >
                <path d="M0,0 L7,3.5 L0,7" fill="#9aaa85" />
              </marker>
            </defs>
            {doc.edges.map((edge, i) => {
              const a = doc.nodes.find((n) => n.id === edge.from),
                b = doc.nodes.find((n) => n.id === edge.to);
              if (!a || !b) return null;
              const feedback = edge.kind === "feedback";
              const x1 = a.x + (feedback ? a.width / 2 : a.width),
                y1 = a.y + (feedback ? -12 : a.collapsed ? 29 : 100),
                x2 = b.x + (feedback ? b.width / 2 : 0),
                y2 = b.y + (feedback ? -12 : b.collapsed ? 29 : 100);
              const middle = feedback ? Math.min(a.y, b.y) - 140 : 0;
              const path = feedback
                ? `M${x1},${y1} C${x1},${middle} ${x2},${middle} ${x2},${y2}`
                : `M${x1},${y1} C${x1 + 65},${y1} ${x2 - 65},${y2} ${x2},${y2}`;
              return (
                <g
                  key={i}
                  className={feedback ? "edge-feedback" : "edge-story"}
                >
                  <path d={path} markerEnd="url(#edge-arrow)" />
                  <text
                    x={(x1 + x2) / 2}
                    y={feedback ? middle + 20 : (y1 + y2) / 2 - 12}
                    textAnchor="middle"
                  >
                    {edge.label}
                  </text>
                </g>
              );
            })}
          </svg>
          {doc.nodes.map((node) => (
            <CanvasWidget
              key={node.id}
              node={node}
              selected={selected === node.id}
              select={() => setSelected(node.id)}
              move={(e, n) => gesture(e, n, "move")}
              resize={(e, n) => gesture(e, n, "resize")}
              patch={patch}
              edit={() => setEditor(node.id)}
              pick={(id) => toggleItem(node.id, id)}
              activeItem={expanded[node.id]}
              autoSize={!!autosize[node.id]}
              onAutoHeight={(height) => {
                const target = Math.max(
                  baseHeights.current[node.id] || node.height,
                  height,
                );
                setDoc((d) => resizeInFlow(d, node.id, target));
                setDirty(true);
              }}
              guide={guide}
            />
          ))}
        </div>
        <div className="canvas-empty-hint">
          <Move size={12} />
          拖动画布 · 滚轮缩放 · 点击贴图展开 · 拖动组件边角调整大小
        </div>
        <div className="canvas-controls">
          <button aria-label="缩小画布" onClick={() => zoomBy(1 / 1.2)}>
            <Minus size={15} />
          </button>
          <span>{Math.round(view.zoom * 100)}%</span>
          <button aria-label="放大画布" onClick={() => zoomBy(1.2)}>
            <Plus size={15} />
          </button>
          <i />
          <button aria-label="查看整个画布" onClick={() => fit()}>
            <Maximize size={15} />
          </button>
        </div>
        <div className="canvas-minimap" aria-label="画布导航缩略图">
          <span>THE WORLD / 点击定位</span>
          <svg
            viewBox={`0 0 180 ${(bounds.bottom - bounds.top) * minimapScale}`}
            role="img"
            aria-label="所有章节位置"
          >
            {doc.nodes.map((n) => (
              <rect
                key={n.id}
                x={(n.x - bounds.left) * minimapScale}
                y={(n.y - bounds.top) * minimapScale}
                width={n.width * minimapScale}
                height={(n.collapsed ? 58 : n.height) * minimapScale}
                className={selected === n.id ? "selected" : ""}
                onClick={() => focusNode(n.id)}
              >
                <title>{n.title}</title>
              </rect>
            ))}
          </svg>
        </div>
        {message && (
          <div className="canvas-message" role="status">
            <span>{message}</span>
            <button aria-label="关闭画布提示" onClick={() => setMessage("")}>
              <X size={13} />
            </button>
          </div>
        )}
        {!ready && <div className="canvas-loading">正在读取项目画布…</div>}
      </div>
      <div className="canvas-status">
        <span>
          {doc.nodes.length} 个组件 · {doc.edges.length} 条线索
        </span>
        <span>
          {local ? "浏览器草稿模式" : "项目画布"} ·{" "}
          {dirty ? "有未保存更改" : "已保存"}
          <i />
          E1 / R4 / R1 · 预填充示例
        </span>
      </div>
      {editNode && (
        <CanvasNodeEditor
          key={editNode.id}
          node={editNode}
          close={() => setEditor(null)}
          apply={(value) => {
            checkpoint();
            const openItem = expanded[value.id];
            if (
              openItem &&
              !value.groups.some((g) => g.items.includes(openItem))
            ) {
              const restored = baseHeights.current[value.id];
              if (restored && value.height === editNode.height)
                value = { ...value, height: restored };
              setExpanded((items) => {
                const next = { ...items };
                delete next[value.id];
                return next;
              });
              delete baseHeights.current[value.id];
            }
            const current = liveDoc.current.nodes.find(
              (n) => n.id === value.id,
            )!;
            const nextValue = { ...value, x: current.x, y: current.y };
            change((d) => {
              const flowed = resizeInFlow(d, value.id, nextValue.height);
              return {
                ...flowed,
                nodes: flowed.nodes.map((n) =>
                  n.id === value.id ? nextValue : n,
                ),
              };
            }, false);
            setEditor(null);
          }}
        />
      )}
    </div>
  );
}

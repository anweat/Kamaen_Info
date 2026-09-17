import {
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
  type KeyboardEvent,
} from "react";
import {
  MousePointer2,
  Hand,
  Type,
  MoveUpRight,
  Minus,
  SquareDashed,
  Pencil,
  Box,
  Cuboid,
  ChartNoAxesCombined,
  Code,
  Save,
  Download,
  Upload,
  Undo2,
  Settings2,
  X,
  Scan,
  Plus,
  Maximize2,
  Minimize2,
} from "lucide-react";
import registry, { entityById } from "./registry";
import type { MapNode, Point, WorldMap } from "./types";
import {
  clamp,
  linePoints,
  normalizeStroke,
  removeNode,
  resizeNode,
  worldPoint,
} from "./geometry";
import { validateMap } from "../../shared/contracts.mjs";
import useMapDocument, { downloadMap } from "./useMapDocument";
import EntityArt from "./EntityArt";
import EntityDialog, { type Spotlight } from "./EntityDialog";
import WorldNode from "./WorldNode";
import MapProperties from "./MapProperties";
import SpaceField from "../visual/SpaceField";
import { useSignal } from "../visual/SignalState";
import { displayInk } from "../visual/ink";

type Tool = "select" | "hand" | "text" | "arrow" | "line" | "rect" | "pen";
type View = Point & { zoom: number };
type Gesture = {
  mode: "pan" | "move" | "resize" | "draw";
  start: Point;
  world: Point;
  view: View;
  node?: MapNode;
  points: Point[];
  moved: boolean;
  trigger: HTMLElement | null;
  from?: string;
};
const palette = [
  { id: "select", label: "选择 V", icon: MousePointer2 },
  { id: "hand", label: "平移 H", icon: Hand },
  { id: "text", label: "文字 T", icon: Type },
  { id: "arrow", label: "箭头 A", icon: MoveUpRight },
  { id: "line", label: "线条 L", icon: Minus },
  { id: "rect", label: "虚线框 R", icon: SquareDashed },
  { id: "pen", label: "虚线画笔 P", icon: Pencil },
] as const;
const drawTypes = ["arrow", "line", "rect", "pen"];
const id = () => crypto.randomUUID();
export default function FreeCanvas({ requestedMap }: { requestedMap?: string }) {
  const map = registry.maps.find((m) => m.id === requestedMap) || registry.maps[0];
  if (!registry.maps.length)
    return <p>请在 content/maps 添加地图 JSON 文件。</p>;
  if (requestedMap && map.id !== requestedMap)
    return <p>未找到地图「{requestedMap}」。<a href="#/canvas">返回地图列表</a></p>;
  return (
    <MapEditor
      key={map.id}
      seed={map}
      onMapChange={(id) => { location.hash = `#/canvas/${encodeURIComponent(id)}`; }}
    />
  );
}
function MapEditor({
  seed,
  onMapChange,
}: {
  seed: WorldMap;
  onMapChange: (id: string) => void;
}) {
  const state = useMapDocument(seed),
    { doc, update, ref: docRef } = state;
  const { seen } = useSignal();
  const [hovered, setHovered] = useState<string | null>(null);
  const [view, setView] = useState<View>({ x: 32, y: 24, zoom: 0.72 }),
    viewRef = useRef(view);
  const [tool, setTool] = useState<Tool>("select"),
    [selected, setSelected] = useState<string | null>(null),
    [settings, setSettings] = useState(false);
  const [library, setLibrary] = useState<
      "entity" | "space3d" | "space2d" | "custom" | null
    >(null),
    [query, setQuery] = useState("");
  const [preview, setPreview] = useState<MapNode | null>(null),
    [spotlight, setSpotlight] = useState<Spotlight | null>(null),
    [wide, setWide] = useState(false);
  const host = useRef<HTMLDivElement>(null),
    gesture = useRef<Gesture | null>(null),
    file = useRef<HTMLInputElement>(null),
    spaceHeld = useRef(false);
  const changeView = (next: View) => {
    viewRef.current = next;
    setView(next);
  };
  const point = (x: number, y: number) => {
    const r = host.current!.getBoundingClientRect();
    return worldPoint({ x, y }, { x: r.left, y: r.top }, viewRef.current);
  };
  const selectedNode = doc.nodes.find((n) => n.id === selected);
  function openEntity(node: MapNode, trigger: HTMLElement | null) {
    if (!node.ref || !entityById(node.ref)) return;
    const r = host.current!.getBoundingClientRect(),
      v = viewRef.current;
    setSpotlight({
      id: node.ref,
      anchor: new DOMRect(
        r.left + v.x + node.x * v.zoom,
        r.top + v.y + node.y * v.zoom,
        node.width * v.zoom,
        node.height * v.zoom,
      ),
      trigger,
    });
  }
  function patchNode(next: MapNode) {
    update({
      ...docRef.current,
      nodes: docRef.current.nodes.map((n) => (n.id === next.id ? next : n)),
    });
  }
  function addNode(node: MapNode) {
    update({ ...docRef.current, nodes: [...docRef.current.nodes, node] });
    setSelected(node.id);
    setTool("select");
  }
  function addReference(
    type: "entity" | "space3d" | "space2d" | "custom",
    ref: string,
  ) {
    const r = host.current!.getBoundingClientRect(),
      p = point(r.left + r.width * 0.55, r.top + r.height * 0.43);
    const isEntity = type === "entity";
    addNode({
      id: id(),
      type,
      ref,
      x: p.x - (isEntity ? 60 : 200),
      y: p.y - (isEntity ? 60 : 130),
      width: isEntity ? 128 : 430,
      height: isEntity ? 150 : type === "custom" ? 260 : 390,
    });
    setLibrary(null);
  }
  function zoom(next: number, center?: Point) {
    const h = host.current!,
      c = center || { x: h.clientWidth / 2, y: h.clientHeight / 2 },
      v = viewRef.current,
      z = clamp(next, 0.2, 2.5);
    changeView({
      x: c.x - ((c.x - v.x) * z) / v.zoom,
      y: c.y - ((c.y - v.y) * z) / v.zoom,
      zoom: z,
    });
  }
  useEffect(() => {
    const el = host.current!;
    const wheel = (e: WheelEvent) => {
      if (
        (e.target as HTMLElement).closest(
          ".map-library,.map-properties,.world-space-content",
        )
      )
        return;
      const text = (e.target as HTMLElement).closest(".world-text");
      if (text && text.scrollHeight > text.clientHeight && !e.ctrlKey) return;
      e.preventDefault();
      const r = el.getBoundingClientRect();
      zoom(viewRef.current.zoom * Math.exp(-e.deltaY * 0.001), {
        x: e.clientX - r.left,
        y: e.clientY - r.top,
      });
    };
    el.addEventListener("wheel", wheel, { passive: false });
    return () => el.removeEventListener("wheel", wheel);
  }, []);
  function fit() {
    if (!doc.nodes.length) {
      changeView({ x: 40, y: 40, zoom: 1 });
      return;
    }
    const minX = Math.min(...doc.nodes.map((n) => n.x)),
      minY = Math.min(...doc.nodes.map((n) => n.y)),
      maxX = Math.max(...doc.nodes.map((n) => n.x + n.width)),
      maxY = Math.max(...doc.nodes.map((n) => n.y + n.height));
    const z = clamp(
      Math.min(
        (host.current!.clientWidth - 120) / (maxX - minX),
        (host.current!.clientHeight - 100) / (maxY - minY),
      ),
      0.2,
      1,
    );
    changeView({
      x: (host.current!.clientWidth - (maxX - minX) * z) / 2 - minX * z,
      y: 50 - minY * z,
      zoom: z,
    });
  }
  function begin(e: ReactPointerEvent, node?: MapNode, resize = false) {
    if (!state.ready || e.button > 1) return;
    e.stopPropagation();
    const p = point(e.clientX, e.clientY);
    const pan = e.button === 1 || spaceHeld.current || tool === "hand";
    if (!pan && tool === "text") {
      addNode({
        id: id(),
        type: "text",
        x: p.x,
        y: p.y,
        width: 320,
        height: 150,
        title: "写下一条线索",
        body: "在属性中编辑文字、大小和颜色。",
        fontSize: 20,
      });
      setSettings(true);
      return;
    }
    const drawing = !pan && drawTypes.includes(tool);
    const mode = pan
      ? "pan"
      : drawing
        ? "draw"
        : resize
          ? "resize"
          : node
            ? "move"
            : "pan";
    if (node && !drawing && !pan) setSelected(node.id);
    else if (!drawing) setSelected(null);
    const trigger =
      node?.type === "entity"
        ? ((e.currentTarget.querySelector(".world-entity") ||
            e.currentTarget) as HTMLElement)
        : null;
    gesture.current = {
      mode,
      start: { x: e.clientX, y: e.clientY },
      world: p,
      view: viewRef.current,
      node,
      points: [p],
      moved: false,
      trigger,
      from:
        drawing && node && !["rect", "line", "arrow", "pen"].includes(node.type)
          ? node.id
          : undefined,
    };
    host.current!.focus({ preventScroll: true });
    host.current!.setPointerCapture(e.pointerId);
    e.preventDefault();
  }
  function move(e: ReactPointerEvent) {
    const g = gesture.current;
    if (!g) return;
    const dx = e.clientX - g.start.x,
      dy = e.clientY - g.start.y;
    if (!g.moved && Math.hypot(dx, dy) < 4) return;
    if (!g.moved && (g.mode === "move" || g.mode === "resize"))
      state.remember();
    g.moved = true;
    if (g.mode === "pan") {
      changeView({ ...g.view, x: g.view.x + dx, y: g.view.y + dy });
      return;
    }
    if (g.mode === "move" || g.mode === "resize") {
      const n = g.node!,
        next =
          g.mode === "move"
            ? { ...n, x: n.x + dx / g.view.zoom, y: n.y + dy / g.view.zoom }
            : resizeNode(
                n,
                clamp(n.width + dx / g.view.zoom, 24, 3000),
                clamp(n.height + dy / g.view.zoom, 24, 3000),
              );
      update(
        {
          ...docRef.current,
          nodes: docRef.current.nodes.map((v) => (v.id === n.id ? next : v)),
        },
        false,
      );
      return;
    }
    const p = point(e.clientX, e.clientY);
    if (tool === "pen") {
      const last = g.points.at(-1)!;
      if (Math.hypot(last.x - p.x, last.y - p.y) > 2 && g.points.length < 9999)
        g.points.push(p);
    } else g.points = [g.world, p];
    const shape = normalizeStroke(g.points);
    setPreview({
      id: "drawing-preview",
      type: tool as MapNode["type"],
      ...shape,
      color: "#869574",
      from: tool === "arrow" || tool === "line" ? g.from : undefined,
    });
  }
  function finish(e: ReactPointerEvent, cancel = false) {
    const g = gesture.current;
    if (!g) return;
    gesture.current = null;
    if (host.current?.hasPointerCapture(e.pointerId))
      host.current.releasePointerCapture(e.pointerId);
    if (cancel) {
      if (g.moved && (g.mode === "move" || g.mode === "resize")) state.undo();
      setPreview(null);
      return;
    }
    if (g.mode === "draw" && g.moved) {
      const p = point(e.clientX, e.clientY),
        target = [...docRef.current.nodes]
          .reverse()
          .find(
            (n) =>
              !["rect", "line", "arrow", "pen"].includes(n.type) &&
              n.id !== g.from &&
              p.x >= n.x &&
              p.x <= n.x + n.width &&
              p.y >= n.y &&
              p.y <= n.y + n.height,
          );
      const linked = tool === "arrow" || tool === "line";
      addNode({
        id: id(),
        type: tool as MapNode["type"],
        ...normalizeStroke(g.points.length > 1 ? g.points : [g.world, p]),
        color: "#869574",
        from: linked ? g.from : undefined,
        to: linked ? target?.id : undefined,
        ...(tool === "rect" ? { title: "关系标注" } : {}),
      });
    } else if (g.mode === "move" && !g.moved && g.node?.type === "entity")
      openEntity(g.node, g.trigger);
    setPreview(null);
  }
  function deleteSelection() {
    if (selected) {
      update({
        ...docRef.current,
        nodes: removeNode(docRef.current.nodes, selected),
      });
      setSelected(null);
      setSettings(false);
    }
  }
  function keyboard(e: KeyboardEvent) {
    if (
      (e.target as HTMLElement).closest("input,textarea,select,dialog,iframe")
    )
      return;
    if (e.code === "Space") {
      e.preventDefault();
      spaceHeld.current = true;
      return;
    }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
      e.preventDefault();
      state.undo();
      return;
    }
    if (e.key === "Delete" || e.key === "Backspace") {
      e.preventDefault();
      deleteSelection();
      return;
    }
    if (e.key === "Escape") {
      setSelected(null);
      setSettings(false);
      setLibrary(null);
      setTool("select");
    }
    const shortcut: Record<string, Tool> = {
      v: "select",
      h: "hand",
      t: "text",
      a: "arrow",
      l: "line",
      r: "rect",
      p: "pen",
    };
    if (shortcut[e.key.toLowerCase()] && !e.ctrlKey && !e.metaKey)
      setTool(shortcut[e.key.toLowerCase()]);
    if (e.key === "Enter" && selectedNode?.type === "entity") {
      e.preventDefault();
      openEntity(selectedNode, document.activeElement as HTMLElement);
    }
    if (e.key.startsWith("Arrow") && selectedNode) {
      e.preventDefault();
      const step = e.shiftKey ? 20 : 1;
      patchNode({
        ...selectedNode,
        x:
          selectedNode.x +
          (e.key === "ArrowRight" ? step : e.key === "ArrowLeft" ? -step : 0),
        y:
          selectedNode.y +
          (e.key === "ArrowDown" ? step : e.key === "ArrowUp" ? -step : 0),
      });
    }
  }
  const shapes = [...doc.nodes, ...(preview ? [preview] : [])].filter((n) =>
    ["rect", "line", "arrow", "pen"].includes(n.type),
  );
  const content = doc.nodes.filter(
    (n) => !["rect", "line", "arrow", "pen"].includes(n.type),
  );
  const libraryRows =
    library === "entity"
      ? registry.entities
      : library === "space3d"
        ? registry.scenes
        : library === "space2d"
          ? registry.models
          : registry.renderers;
  return (
    <section
      className={`free-map ${wide ? "free-map-wide" : ""}`}
      onKeyDown={keyboard}
      onKeyUp={(e) => {
        if (e.code === "Space") spaceHeld.current = false;
      }}
      onBlur={() => {
        spaceHeld.current = false;
      }}
    >
      <header className="free-map-header">
        <div>
          <h1>发展地图</h1>
          <select
            aria-label="选择地图文件"
            value={seed.id}
            onChange={(e) => onMapChange(e.target.value)}
          >
            {registry.maps.map((m) => (
              <option key={m.id} value={m.id}>
                {m.title}
              </option>
            ))}
          </select>
        </div>
        <div className="free-map-actions">
          <button
            aria-label="撤销地图操作"
            disabled={!state.undoCount}
            onClick={state.undo}
          >
            <Undo2 size={17} />
          </button>
          <button
            aria-label="导入地图 JSON"
            disabled={!state.ready || state.busy}
            onClick={() => file.current?.click()}
          >
            <Upload size={17} />
          </button>
          <input
            hidden
            type="file"
            disabled={!state.ready || state.busy}
            ref={file}
            accept=".json"
            onChange={(e) => {
              if (e.target.files?.[0]) void state.importFile(e.target.files[0]);
              e.target.value = "";
            }}
          />
          <button aria-label="导出地图 JSON" onClick={() => downloadMap(doc)}>
            <Download size={17} />
          </button>
          <button
            aria-label={wide ? "退出专注画布" : "专注画布"}
            onClick={() => setWide(!wide)}
          >
            {wide ? <Minimize2 size={17} /> : <Maximize2 size={17} />}
          </button>
          <button
            className="primary"
            disabled={!state.ready || state.busy}
            onClick={() => void state.save()}
          >
            <Save size={16} />
            <span>{state.busy ? "保存中" : "保存"}</span>
          </button>
        </div>
      </header>
      <div
        className={`free-map-viewport tool-${tool}`}
        ref={host}
        tabIndex={0}
        aria-label="自由格点画布"
        style={{
          backgroundSize: `${24 * view.zoom}px ${24 * view.zoom}px`,
          backgroundPosition: `${view.x}px ${view.y}px`,
        }}
        onPointerDown={(e) => begin(e)}
        onPointerMove={(e) => {
          const bounds = host.current!.getBoundingClientRect();
          host.current!.style.setProperty(
            "--pointer-x",
            `${e.clientX - bounds.left}px`,
          );
          host.current!.style.setProperty(
            "--pointer-y",
            `${e.clientY - bounds.top}px`,
          );
          move(e);
        }}
        onPointerUp={(e) => finish(e)}
        onPointerCancel={(e) => finish(e, true)}
      >
        <SpaceField />
        {!state.ready && (
          <div className="map-loading" role="status">
            正在读取地图文件…
          </div>
        )}
        <div
          className="free-map-world"
          style={{
            transform: `translate(${view.x}px, ${view.y}px) scale(${view.zoom})`,
          }}
        >
          {shapes.map((n) => {
            const ink = displayInk(n.color || "#859477"),
              isSelected = selected === n.id;
            const points = linePoints(n, doc.nodes),
              path = points
                .map((p, i) => `${i ? "L" : "M"}${p.x},${p.y}`)
                .join(" "),
              a = points.at(-2)!,
              b = points.at(-1)!,
              angle = Math.atan2(b.y - a.y, b.x - a.x);
            return (
              <svg
                key={n.id}
                className="world-ink"
                data-signal={
                  n.from === hovered ||
                  n.to === hovered ||
                  n.from === selected ||
                  n.to === selected
                    ? "active"
                    : undefined
                }
                width="1"
                height="1"
                style={{
                  zIndex:
                    n.id === "drawing-preview"
                      ? 999
                      : doc.nodes.findIndex((v) => v.id === n.id) + 1,
                }}
              >
                <g
                  role="button"
                  tabIndex={n.id === "drawing-preview" ? -1 : 0}
                  aria-label={`${n.type === "rect" ? "虚线关系框" : n.type === "pen" ? "虚线笔迹" : "关系线"} ${n.title || n.id}`}
                  onPointerDown={(e) => begin(e, n)}
                  onFocus={() => setSelected(n.id)}
                  onDoubleClick={() => setSettings(true)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      setSelected(n.id);
                      setSettings(true);
                    }
                  }}
                >
                  {n.type === "rect" ? (
                    <>
                      <rect
                        x={n.x}
                        y={n.y}
                        width={n.width}
                        height={n.height}
                        className="ink-hit"
                      />
                      <rect
                        x={n.x}
                        y={n.y}
                        width={n.width}
                        height={n.height}
                        fill="none"
                        stroke={ink}
                        strokeWidth={isSelected ? 2.5 : 1.5}
                        strokeDasharray="7 7"
                      />
                      <text x={n.x + 16} y={n.y - 12} fill={ink} fontSize="14">
                        {n.title}
                      </text>
                    </>
                  ) : (
                    <>
                      <path d={path} className="ink-hit" />
                      <path
                        d={path}
                        fill="none"
                        stroke={ink}
                        strokeWidth={isSelected ? 3 : 2}
                        strokeDasharray={n.type === "pen" ? "5 7" : undefined}
                        strokeLinecap="round"
                      />
                      {n.type === "arrow" && (
                        <path
                          className="carrier-trace"
                          d={path}
                          pathLength="100"
                        />
                      )}
                      {n.type === "arrow" && (
                        <path
                          d={`M${b.x - 12 * Math.cos(angle - 0.5)},${b.y - 12 * Math.sin(angle - 0.5)} L${b.x},${b.y} L${b.x - 12 * Math.cos(angle + 0.5)},${b.y - 12 * Math.sin(angle + 0.5)}`}
                          fill="none"
                          stroke={ink}
                          strokeWidth="2"
                        />
                      )}
                      {n.title && (
                        <text
                          x={(points[0].x + b.x) / 2}
                          y={(points[0].y + b.y) / 2 - 14}
                          textAnchor="middle"
                          fill={ink}
                          fontSize="13"
                        >
                          {n.title}
                        </text>
                      )}
                    </>
                  )}
                </g>
              </svg>
            );
          })}
          {content.map((n) => (
            <div
              key={n.id}
              className={`world-object world-${n.type} ${selected === n.id ? "selected" : ""}`}
              data-node-id={n.id}
              data-observed={n.ref && seen.includes(n.ref) ? "true" : undefined}
              onPointerEnter={() => setHovered(n.id)}
              onPointerLeave={() => setHovered(null)}
              tabIndex={n.type === "entity" ? -1 : 0}
              role="group"
              aria-label={`${n.title || n.ref || n.id}组件`}
              onFocus={() => setSelected(n.id)}
              style={{
                left: n.x,
                top: n.y,
                width: n.width,
                height: n.height,
                zIndex: doc.nodes.findIndex((v) => v.id === n.id) + 1,
              }}
              onPointerDown={(e) => begin(e, n)}
              onDoubleClick={() => {
                setSelected(n.id);
                setSettings(true);
              }}
              onKeyDown={(e) => {
                if (
                  e.key === "Enter" &&
                  e.target === e.currentTarget &&
                  n.type !== "entity"
                ) {
                  e.preventDefault();
                  setSettings(true);
                }
              }}
            >
              <WorldNode
                node={n}
                onOpen={(element) => openEntity(n, element)}
              />
            </div>
          ))}
          {selectedNode && (
            <div
              className="world-selection"
              style={{
                left: selectedNode.x - 5,
                top: selectedNode.y - 5,
                width: selectedNode.width + 10,
                height: selectedNode.height + 10,
              }}
            >
              <button
                className="world-settings"
                aria-label="编辑选中组件"
                onPointerDown={(e) => e.stopPropagation()}
                onClick={() => setSettings(!settings)}
              >
                <Settings2 size={16} />
              </button>
              <button
                className="world-resize"
                aria-label="调整选中组件大小"
                onPointerDown={(e) => begin(e, selectedNode, true)}
                onKeyDown={(e) => {
                  if (e.key.startsWith("Arrow")) {
                    e.preventDefault();
                    e.stopPropagation();
                    const s = e.shiftKey ? 20 : 1;
                    patchNode(
                      resizeNode(
                        selectedNode,
                        clamp(
                          selectedNode.width +
                            (e.key === "ArrowRight"
                              ? s
                              : e.key === "ArrowLeft"
                                ? -s
                                : 0),
                          24,
                          3000,
                        ),
                        clamp(
                          selectedNode.height +
                            (e.key === "ArrowDown"
                              ? s
                              : e.key === "ArrowUp"
                                ? -s
                                : 0),
                          24,
                          3000,
                        ),
                      ),
                    );
                  }
                }}
              />
            </div>
          )}
        </div>
        <div
          className="map-tools"
          inert={!state.ready}
          role="toolbar"
          aria-label="画布工具"
          onPointerDown={(e) => e.stopPropagation()}
        >
          {palette.map((t) => (
            <button
              key={t.id}
              aria-label={t.label}
              title={t.label}
              aria-pressed={tool === t.id}
              onClick={() => {
                setTool(t.id);
                setLibrary(null);
              }}
            >
              <t.icon size={19} />
            </button>
          ))}
          <span />
          <button
            aria-label="添加物品或方块"
            title="物品 / 方块"
            onClick={() => setLibrary(library === "entity" ? null : "entity")}
          >
            <Box size={20} />
          </button>
          <button
            aria-label="添加 3D 空间"
            title="3D 空间"
            onClick={() => setLibrary("space3d")}
          >
            <Cuboid size={20} />
          </button>
          <button
            aria-label="添加 2D 模型"
            title="2D 模型"
            onClick={() => setLibrary("space2d")}
          >
            <ChartNoAxesCombined size={20} />
          </button>
          <button
            aria-label="添加自定义渲染"
            title="自定义渲染"
            onClick={() => setLibrary("custom")}
          >
            <Code size={20} />
          </button>
        </div>
        {library && (
          <aside
            className="map-library"
            aria-label="组件库"
            onPointerDown={(e) => e.stopPropagation()}
            onWheel={(e) => e.stopPropagation()}
          >
            <header>
              <strong>
                {library === "entity"
                  ? "物品与方块"
                  : library === "space3d"
                    ? "3D 空间"
                    : library === "space2d"
                      ? "2D 模型"
                      : "自定义渲染"}
              </strong>
              <button aria-label="关闭组件库" onClick={() => setLibrary(null)}>
                <X size={16} />
              </button>
            </header>
            <input
              aria-label="筛选注册内容"
              placeholder="按名称或 ID 搜索"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="map-library-list">
              {libraryRows
                .filter((r) =>
                  `${r.title} ${r.id}`
                    .toLowerCase()
                    .includes(query.toLowerCase()),
                )
                .map((r) => (
                  <button
                    key={r.id}
                    onClick={() => addReference(library, r.id)}
                  >
                    {library === "entity" && (
                      <EntityArt entity={entityById(r.id)!} />
                    )}
                    <span>
                      {r.title}
                      <small>{r.id}</small>
                    </span>
                    <Plus size={15} />
                  </button>
                ))}
            </div>
            <small>内容随注册文件自动出现</small>
          </aside>
        )}
        {settings && selectedNode && (
          <div
            onPointerDown={(e) => e.stopPropagation()}
            onWheel={(e) => e.stopPropagation()}
          >
            <MapProperties
              key={JSON.stringify(selectedNode)}
              node={selectedNode}
              nodes={doc.nodes}
              onApply={(n) => {
                const next = {
                  ...docRef.current,
                  nodes: docRef.current.nodes.map((v) =>
                    v.id === n.id ? n : v,
                  ),
                };
                if (validateMap(next, registry)) update(next);
                else state.setMessage("属性无效，请检查尺寸或引用。");
              }}
              onClose={() => setSettings(false)}
              onDelete={deleteSelection}
              onDuplicate={() => {
                addNode({
                  ...selectedNode,
                  id: id(),
                  x: selectedNode.x + 32,
                  y: selectedNode.y + 32,
                });
              }}
              onLayer={(top) =>
                update({
                  ...docRef.current,
                  nodes: top
                    ? [
                        ...doc.nodes.filter((n) => n.id !== selectedNode.id),
                        selectedNode,
                      ]
                    : [
                        selectedNode,
                        ...doc.nodes.filter((n) => n.id !== selectedNode.id),
                      ],
                })
              }
            />
          </div>
        )}
        {!doc.nodes.length && (
          <div className="free-map-empty">
            <strong>从一个对象开始</strong>
            <p>添加贴图、文字或空间组件，在格点画布上自由组织线索。</p>
            <button
              onPointerDown={(e) => e.stopPropagation()}
              onClick={() => setLibrary("entity")}
            >
              <Plus size={16} />
              添加第一个对象
            </button>
          </div>
        )}
        <div className="map-zoom" onPointerDown={(e) => e.stopPropagation()}>
          <button aria-label="缩小地图" onClick={() => zoom(view.zoom / 1.2)}>
            <Minus size={16} />
          </button>
          <output>{Math.round(view.zoom * 100)}%</output>
          <button aria-label="放大地图" onClick={() => zoom(view.zoom * 1.2)}>
            <Plus size={16} />
          </button>
          <button aria-label="适配整张地图" onClick={fit}>
            <Scan size={17} />
          </button>
        </div>
      </div>
      <footer className="free-map-status">
        <span>
          {doc.nodes.length} 个组件 ·{" "}
          {state.local
            ? "静态 / 离线模式"
            : state.dirty
              ? "有未保存修改"
              : "文件已同步"}
        </span>
        <span>空白拖动平移 · 滚轮缩放 · 点击查看 · 拖动物体摆放 · 无吸附</span>
      </footer>
      {state.message && (
        <div className="map-message" role="status">
          {state.message}
          <button
            aria-label="关闭地图消息"
            onClick={() => state.setMessage("")}
          >
            <X size={15} />
          </button>
        </div>
      )}
      {state.recovery && (
        <div className="map-recovery">
          <p>旧草稿与当前文件不同</p>
          <button onClick={() => downloadMap(state.recovery!)}>
            导出旧草稿
          </button>
          <button onClick={state.clearRecovery}>使用当前文件</button>
        </div>
      )}
      {spotlight && (
        <EntityDialog value={spotlight} onClose={() => setSpotlight(null)} />
      )}
    </section>
  );
}

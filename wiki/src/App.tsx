import { useEffect, useRef, useState } from "react";
import {
  Grid3X3,
  BookOpen,
  Box,
  GitBranch,
  Orbit,
  Layers3,
  NotebookPen,
  Library,
  Search,
  Plus,
  ArrowUpRight,
  Menu,
  X,
  ChevronRight,
} from "lucide-react";
import { data, href } from "./data";
import { Items, Recipes } from "./components/Catalog";
import { Overview, Story, Structures, Documents } from "./components/Pages";
import Notes from "./components/Notes";
import CanvasPage from "./components/CanvasPage";
import FreeCanvas from "./world/FreeCanvas";
import Development from "./world/Development";
import { EntityLibrary, SpatialLibrary, ModelLab } from "./world/RegistryPages";
import registry, { entityById } from "./world/registry";
import { SignalConsole, SignalStatus } from "./visual/SignalConsole";
const navigation = [
  { id: "canvas", label: "发展地图", icon: Grid3X3 },
  { id: "overview", label: "档案总览", icon: BookOpen },
  { id: "items", label: "物品与方块", icon: Box },
  { id: "recipes", label: "配方与路线", icon: GitBranch },
  { id: "story", label: "故事与发展线", icon: Orbit },
  { id: "structures", label: "3D 查看", icon: Layers3 },
  { id: "models", label: "模型实验台", icon: Orbit },
  { id: "development", label: "开发工作台", icon: Box },
  { id: "nbt", label: "NBT 与状态", icon: Box },
  { id: "notes", label: "研究记录", icon: NotebookPen },
  { id: "docs", label: "文档书架", icon: Library },
];
function route() {
  const [, page = "canvas", ...parts] = location.hash.split("/");
  return {
    page,
    id: parts.length ? decodeURIComponent(parts.join("/")) : undefined,
  };
}
export default function App() {
  const [current, setCurrent] = useState(route);
  const [menu, setMenu] = useState(false);
  const [query, setQuery] = useState("");
  const dialog = useRef<HTMLDialogElement>(null);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const change = () => {
      setCurrent(route());
      setMenu(false);
      window.scrollTo(0, 0);
    };
    window.addEventListener("hashchange", change);
    const shortcut = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        dialog.current?.showModal();
        input.current?.focus();
      }
    };
    window.addEventListener("keydown", shortcut);
    return () => {
      window.removeEventListener("hashchange", change);
      window.removeEventListener("keydown", shortcut);
    };
  }, []);
  const title =
    navigation.find((n) => n.id === current.page)?.label || "档案总览";
  const found = query.trim()
    ? [
        ...registry.entities
          .filter((e) =>
            `${e.title} ${e.id}`.toLowerCase().includes(query.toLowerCase()),
          )
          .map((e) => ({
            title: e.title,
            meta: "文件实体",
            url: href("entities", e.id),
          })),
        ...data.items
          .filter((i) =>
            `${i.name} ${i.legacy}`.toLowerCase().includes(query.toLowerCase()),
          )
          .map((i) => ({
            title: i.name,
            meta: `物品 · ${i.version}`,
            url: href("items", i.id),
          })),
        ...data.docs
          .filter((d) => d.title.includes(query))
          .map((d) => ({
            title: d.title,
            meta: `文档 · ${d.group}`,
            url: href("docs", d.id),
          })),
        ...data.recipes
          .filter((r) =>
            `${r.id} ${Object.keys(r.outputs).map((id) => data.items.find((i) => i.id === "r4:" + id)?.name)}`
              .toLowerCase()
              .includes(query.toLowerCase()),
          )
          .map((r) => ({
            title: r.id,
            meta: "配方 · R4",
            url: href("recipes", r.id),
          })),
      ].slice(0, 40)
    : [];
  return (
    <>
      <a
        className="skip-link"
        href="#main"
        onClick={(e) => {
          e.preventDefault();
          document.getElementById("main")?.focus();
        }}
      >
        跳到主要内容
      </a>
      <aside className={`sidebar ${menu ? "open" : ""}`}>
        <a className="brand" href={href("canvas")}>
          <span className="brand-block">
            <span />
          </span>
          <span>
            KAMAEN<small>信息与频率 · 研究档案</small>
          </span>
        </a>
        <button
          className="sidebar-search"
          onClick={() => {
            dialog.current?.showModal();
            input.current?.focus();
          }}
        >
          <Search size={15} />
          <span>搜索档案</span>
          <kbd>Ctrl K</kbd>
        </button>
        <div className="nav-label">探索档案</div>
        <nav>
          {navigation.map((n) => (
            <a
              href={href(n.id)}
              aria-current={current.page === n.id ? "page" : undefined}
              className={current.page === n.id ? "active" : ""}
              key={n.id}
            >
              <n.icon size={18} strokeWidth={1.7} />
              {n.label}
              {n.id === "notes" && <span className="nav-plus">＋</span>}
            </a>
          ))}
        </nav>
        <div className="sidebar-divider" />
        <div className="nav-label">当前工作稿</div>
        <a
          className="revision-link"
          href={href("docs", "EARLY_E1_GAMEPLAY.md")}
        >
          <i className="revision-dot" /> E1 · 前期探索<span>讨论中</span>
        </a>
        <a className="revision-link" href={href("docs", "R4_STAGE_DESIGN.md")}>
          <i /> R4 · 计算与研究
        </a>
        <a className="revision-link" href={href("docs", "REVIEW_SYSTEM.md")}>
          <i /> R1 · 全局发展线
        </a>
        <div className="sidebar-bottom">
          <SignalConsole />
          <a href={href("notes", "new")}>
            <Plus size={16} /> 记下一点想法
          </a>
        </div>
      </aside>
      {menu && (
        <button
          className="menu-backdrop"
          aria-label="关闭导航"
          onClick={() => setMenu(false)}
        />
      )}
      <div className="workspace">
        <header className="topbar">
          <button
            className="mobile-menu"
            aria-label="展开导航"
            onClick={() => setMenu((v) => !v)}
          >
            <Menu size={20} />
          </button>
          <div className="breadcrumbs">
            <span>研究档案</span>
            <ChevronRight size={13} />
            <strong>{title}</strong>
          </div>
          <div className="topbar-right">
            <span className="topbar-date">KAMAEN / RESEARCH ATLAS</span>
            <SignalStatus />
          </div>
        </header>
        <main
          id="main"
          className={
            ["canvas", "legacy-canvas"].includes(current.page)
              ? "main-canvas"
              : ""
          }
          tabIndex={-1}
          key={current.page + "/" + (current.id || "")}
        >
          <div className="page-enter">
            {current.page === "canvas" ? (
              <FreeCanvas requestedMap={current.id} />
            ) : current.page === "legacy-canvas" ? (
              <CanvasPage />
            ) : current.page === "items" ? (
              current.id && !entityById(current.id) ? (
                <Items id={current.id} />
              ) : (
                <EntityLibrary id={current.id} />
              )
            ) : current.page === "entities" ? (
              <EntityLibrary id={current.id} />
            ) : current.page === "archive-items" ? (
              <Items id={current.id} />
            ) : current.page === "nbt" ? (
              <EntityLibrary id={current.id} nbt />
            ) : current.page === "models" ? (
              <ModelLab />
            ) : current.page === "development" ? (
              <Development />
            ) : current.page === "recipes" ? (
              <Recipes id={current.id} />
            ) : current.page === "story" ? (
              <Story id={current.id} />
            ) : current.page === "structures" ? (
              <SpatialLibrary />
            ) : current.page === "legacy-structures" ? (
              <Structures id={current.id} />
            ) : current.page === "notes" ? (
              <Notes id={current.id} />
            ) : current.page === "docs" ? (
              <Documents id={current.id} />
            ) : (
              <Overview />
            )}
          </div>
          {!["canvas", "legacy-canvas"].includes(current.page) && (
            <footer>
              <span>
                KAMAEN INFO <span className="muted">/ 研究档案</span>
              </span>
              <span>发现 → 测量 → 理解 → 再创造</span>
              <a href={href("docs", "README.md")}>
                关于这份工作稿 <ArrowUpRight size={12} />
              </a>
            </footer>
          )}
        </main>
      </div>
      <dialog
        ref={dialog}
        className="search-dialog"
        onClick={(e) => {
          if (e.target === dialog.current) dialog.current.close();
        }}
      >
        <div className="dialog-search">
          <Search size={20} />
          <input
            ref={input}
            aria-label="全局搜索"
            placeholder="搜索物品、配方、文档…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button aria-label="关闭搜索" onClick={() => dialog.current?.close()}>
            <X size={19} />
          </button>
        </div>
        <div className="search-results">
          {found.map((r, i) => (
            <a href={r.url} key={i} onClick={() => dialog.current?.close()}>
              <span>
                {r.title}
                <small>{r.meta}</small>
              </span>
              <ArrowUpRight size={17} />
            </a>
          ))}
          {!found.length && (
            <p>
              {query
                ? "没有找到结果，试试“晶体”“机柜”或“模型”。"
                : "输入关键词，沿着名字寻找线索。"}
            </p>
          )}
        </div>
      </dialog>
    </>
  );
}

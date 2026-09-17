import { useEffect, useRef, useState } from "react";
import { Plus, Download, Upload, Save, ArrowUpRight } from "lucide-react";
import { data, href, itemById } from "../data";
import { scenes } from "../scenes";
import Markdown from "./Markdown";
import SceneViewer from "./SceneViewer";
import { ItemCard, RecipeCard } from "./Catalog";
import savedNotebook from "../../content/notes.json";
export type Note = {
  id: string;
  title: string;
  body: string;
  stage: string;
  status: string;
  updatedAt: string;
  refs: string[];
};
type Notebook = { revision: number; notes: Note[] };
const draftKey = "kamaen-editor-draft-v1";
function readDraft(): Note | null {
  try {
    return JSON.parse(sessionStorage.getItem(draftKey) || "null");
  } catch {
    return null;
  }
}
const emptyNote = (): Note => ({
  id: crypto.randomUUID(),
  title: "",
  body: "",
  stage: "E1",
  status: "想法",
  updatedAt: new Date().toISOString(),
  refs: [],
});
const template: Note = {
  id: "example-research-loop",
  title: "第一批晶体，怎样回到产线？",
  stage: "E1",
  status: "讨论中",
  updatedAt: "2026-09-07",
  body: "> 示例记录 · 可以复制为自己的研究笔记。\n\n## 想验证的事\n让同一批晶体的加工、测量和实际用途连成一条线，而不是三份独立教程。\n\n## 一次小实验\n1. 保留一枚参考晶种，记录另一份晶坯的朝向。\n2. 只改变一处冲击或缓冲设置。\n3. 复测工作窗，安装到已有分离设备。\n4. 比较目标回收、混入、时间与能量。\n\n## 留待讨论\n- 首次只展示哪些参数？\n- 怎样让失败留下有价值的记录？\n- 第一次改善应该怎样呈现？",
  refs: [
    "item~e1:raw_kamaen_crystal",
    "scene~impact",
    "doc~EARLY_E1_GAMEPLAY.md",
  ],
};
export function EmbeddedRef({ value }: { value: string }) {
  const [type, ...parts] = value.split("~");
  const id = parts.join("~");
  if (type === "item") {
    const item = itemById(id);
    return item ? <ItemCard item={item} /> : <p>待补条目：{id}</p>;
  }
  if (type === "recipe") {
    const recipe = data.recipes.find((r) => r.id === id);
    return recipe ? <RecipeCard recipe={recipe} full /> : <p>待补配方：{id}</p>;
  }
  if (type === "scene")
    return scenes.some((s) => s.id === id) ? (
      <SceneViewer sceneId={id} />
    ) : (
      <p>待补场景：{id}</p>
    );
  return (
    <a className="document-link" href={href("docs", id)}>
      {data.docs.find((d) => d.id === id)?.title || id}
      <ArrowUpRight size={16} />
    </a>
  );
}
export default function Notes({ id }: { id?: string }) {
  const [book, setBook] = useState<Notebook>({ revision: 0, notes: [] });
  const [draft, setDraft] = useState<Note | null>(null);
  const [recovery, setRecovery] = useState(readDraft);
  const [local, setLocal] = useState(false);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [refType, setRefType] = useState("item");
  const [refId, setRefId] = useState("");
  const file = useRef<HTMLInputElement>(null);
  useEffect(() => {
    let active = true;
    fetch("./api/notes")
      .then(async (r) => {
        if (
          !r.ok ||
          !r.headers.get("content-type")?.includes("application/json")
        )
          throw Error();
        return r.json();
      })
      .then((v) => {
        if (active) setBook(v);
      })
      .catch(() => {
        if (!active) return;
        setLocal(true);
        try {
          const cached = JSON.parse(
            localStorage.getItem("kamaen-notes-v1") ||
              JSON.stringify(savedNotebook),
          );
          setBook(cached);
        } catch {
          setMessage("本地记录读取失败，可通过 JSON 备份恢复。");
        }
      })
      .finally(() => {
        if (active) setReady(true);
      });
    return () => {
      active = false;
    };
  }, []);
  useEffect(() => {
    if (!ready) return;
    if (id?.startsWith("new")) {
      const n = readDraft() || emptyNote();
      const ref = id.split("~").slice(1).join("~");
      if (ref && !n.refs.includes(ref)) n.refs = [...n.refs, ref];
      setDraft(n);
    } else setDraft(null);
  }, [id, ready]);
  useEffect(() => {
    if (draft) {
      try {
        sessionStorage.setItem(draftKey, JSON.stringify(draft));
      } catch {
        setMessage("当前浏览器无法缓存草稿，请及时保存或导出。");
      }
    }
  }, [draft]);
  useEffect(() => {
    const warn = (e: BeforeUnloadEvent) => {
      if (draft) {
        e.preventDefault();
      }
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [draft]);
  async function persist(next: Notebook) {
    if (local) {
      localStorage.setItem("kamaen-notes-v1", JSON.stringify(next));
      setBook(next);
      return;
    }
    const response = await fetch("./api/notes", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(next),
    });
    const value = await response.json();
    if (!response.ok) throw Error(value.error || "保存失败");
    setBook(value);
  }
  async function save() {
    if (!draft?.title.trim()) return setMessage("请先写一个标题。");
    setBusy(true);
    try {
      const note = { ...draft, updatedAt: new Date().toISOString() };
      await persist({
        ...book,
        notes: [note, ...book.notes.filter((n) => n.id !== note.id)],
      });
      sessionStorage.removeItem(draftKey);
      setRecovery(null);
      setDraft(null);
      location.hash = href("notes", note.id);
      setMessage(
        local
          ? "已保存到当前浏览器，请导出 JSON 留存。"
          : "已保存到 wiki/content/notes.json。",
      );
    } catch (e) {
      setMessage(String(e));
    } finally {
      setBusy(false);
    }
  }
  function exportBook() {
    const notes = draft
      ? [
          { ...draft, title: draft.title || "未命名草稿" },
          ...book.notes.filter((n) => n.id !== draft.id),
        ]
      : book.notes;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify({ ...book, notes }, null, 2)], {
        type: "application/json",
      }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "kamaen-notes.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function importBook(input: File) {
    setBusy(true);
    try {
      if (input.size > 2000000) throw Error("文件超过 2 MB");
      const incoming = JSON.parse(await input.text());
      if (
        !Array.isArray(incoming.notes) ||
        !incoming.notes.every(
          (n: Note) =>
            n &&
            ["id", "title", "body", "stage", "status", "updatedAt"].every(
              (k) => typeof n[k as keyof Note] === "string",
            ) &&
            Array.isArray(n.refs) &&
            n.refs.every((r) => typeof r === "string") &&
            n.title.trim() &&
            ["想法", "讨论中", "待验证", "已记录"].includes(n.status),
        )
      )
        throw Error("记录格式无效");
      const existing = new Set(book.notes.map((n) => n.id));
      const imported = incoming.notes.map((n: Note) =>
        existing.has(n.id)
          ? { ...n, id: crypto.randomUUID(), title: n.title + "（导入副本）" }
          : n,
      );
      await persist({ ...book, notes: [...imported, ...book.notes] });
      setMessage(`已导入 ${imported.length} 条，同 ID 保留为副本。`);
    } catch (e) {
      setMessage(String(e));
    } finally {
      setBusy(false);
      if (file.current) file.current.value = "";
    }
  }
  const note =
    book.notes.find((n) => n.id === id) || (id === "example" ? template : null);
  const options =
    refType === "item"
      ? data.items.map((i) => ({ id: i.id, title: `${i.version} · ${i.name}` }))
      : refType === "recipe"
        ? data.recipes.map((r) => ({ id: r.id, title: r.id }))
        : refType === "scene"
          ? scenes.map((s) => ({ id: s.id, title: s.title }))
          : data.docs.map((d) => ({ id: d.id, title: d.title }));
  return (
    <>
      <div className="eyebrow">05 / RESEARCH JOURNAL</div>
      <div className="title-row">
        <h1>研究记录</h1>
        <div className="button-row">
          <button disabled={!ready || busy} onClick={exportBook}>
            <Download size={15} />
            导出
          </button>
          <button
            disabled={!ready || busy || !!draft}
            onClick={() => file.current?.click()}
          >
            <Upload size={15} />
            导入
          </button>
          <button
            className="primary"
            disabled={!ready || !!draft}
            onClick={() => {
              setDraft(emptyNote());
              setMessage("");
            }}
          >
            <Plus size={16} />
            新记录
          </button>
          <input
            ref={file}
            type="file"
            accept="application/json"
            hidden
            onChange={(e) =>
              e.target.files?.[0] && importBook(e.target.files[0])
            }
          />
        </div>
      </div>
      <p className="lead">
        保留问题、推演与阶段结论，把分散的内容放回同一条线索。
      </p>
      <div className="save-location">
        {!ready
          ? "正在读取记录…"
          : local
            ? "静态预览模式 · 保存到当前浏览器，使用 JSON 导出备份。"
            : "本地记录模式 · 保存到项目 wiki/content/notes.json，可随 Git 版本管理。"}
      </div>
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      {recovery && !draft && (
        <div className="notice">
          有一份尚未保存的编辑草稿：{recovery.title || "未命名"}{" "}
          <button onClick={() => setDraft(recovery)}>恢复草稿</button>
        </div>
      )}
      {draft ? (
        <div className="editor-layout">
          <form
            className="note-editor"
            onSubmit={(e) => {
              e.preventDefault();
              save();
            }}
          >
            <label>
              记录标题
              <input
                required
                maxLength={200}
                value={draft.title}
                onChange={(e) => setDraft({ ...draft, title: e.target.value })}
                placeholder="一个问题、一个实验，或一段新想法"
              />
            </label>
            <div className="filter-bar">
              <label>
                阶段
                <select
                  value={draft.stage}
                  onChange={(e) =>
                    setDraft({ ...draft, stage: e.target.value })
                  }
                >
                  {["E1", "R4", "R1", "跨阶段"].map((s) => (
                    <option key={s}>{s}</option>
                  ))}
                </select>
              </label>
              <label>
                状态
                <select
                  value={draft.status}
                  onChange={(e) =>
                    setDraft({ ...draft, status: e.target.value })
                  }
                >
                  {["想法", "讨论中", "待验证", "已记录"].map((s) => (
                    <option key={s}>{s}</option>
                  ))}
                </select>
              </label>
            </div>
            <label>
              正文 · Markdown
              <textarea
                rows={16}
                maxLength={100000}
                value={draft.body}
                onChange={(e) => setDraft({ ...draft, body: e.target.value })}
                placeholder="## 想法\n\n## 玩家操作\n\n## 待验证的问题"
              />
            </label>
            <h3>关联并嵌入内容</h3>
            <div className="reference-controls">
              <select
                aria-label="关联内容类型"
                value={refType}
                onChange={(e) => {
                  setRefType(e.target.value);
                  setRefId("");
                }}
              >
                <option value="item">物品 / 方块</option>
                <option value="recipe">配方</option>
                <option value="scene">结构演示</option>
                <option value="doc">来源文档</option>
              </select>
              <select
                aria-label="关联对象"
                value={refId}
                onChange={(e) => setRefId(e.target.value)}
              >
                <option value="">选择内容…</option>
                {options.map((o) => (
                  <option key={o.id} value={o.id}>
                    {o.title}
                  </option>
                ))}
              </select>
              <button
                type="button"
                disabled={!refId}
                onClick={() => {
                  const ref = refType + "~" + refId;
                  if (!draft.refs.includes(ref))
                    setDraft({ ...draft, refs: [...draft.refs, ref] });
                }}
              >
                添加
              </button>
            </div>
            <div className="ref-chips">
              {draft.refs.map((r) => (
                <button
                  title="移除此引用"
                  key={r}
                  type="button"
                  onClick={() =>
                    setDraft({
                      ...draft,
                      refs: draft.refs.filter((v) => v !== r),
                    })
                  }
                >
                  {r} ×
                </button>
              ))}
            </div>
            <button className="primary" type="submit" disabled={busy}>
              <Save size={16} />
              {busy ? "保存中…" : "保存记录"}
            </button>
          </form>
          <aside className="note-preview">
            <span className="eyebrow">LIVE PREVIEW</span>
            <h2>{draft.title || "等待一个新想法"}</h2>
            <Markdown>{draft.body || "正文预览会出现在这里。"}</Markdown>
            {draft.refs.map((r) => (
              <EmbeddedRef key={r} value={r} />
            ))}
          </aside>
        </div>
      ) : note ? (
        <article className="journal-article">
          <div className="title-row">
            <span className="status-tag">
              {note.stage} · {note.status}
            </span>
            <button
              onClick={() =>
                setDraft(
                  note === template
                    ? {
                        ...template,
                        id: crypto.randomUUID(),
                        title: template.title + "（我的记录）",
                      }
                    : { ...note },
                )
              }
            >
              {note === template ? "复制为新记录" : "编辑记录"}
            </button>
          </div>
          <h2>{note.title}</h2>
          <Markdown>{note.body}</Markdown>
          <h3>这篇记录里的对象</h3>
          {note.refs.map((r) => (
            <EmbeddedRef key={r} value={r} />
          ))}
        </article>
      ) : (
        <>
          <a className="example-note" href={href("notes", "example")}>
            <span className="eyebrow">示例 / E1</span>
            <h2>{template.title}</h2>
            <p>把物品、结构和思路组合在一起，看看一篇研究记录可以怎样展开。</p>
            <span>
              打开组合示例 <ArrowUpRight size={16} />
            </span>
          </a>
          {book.notes.length === 0 ? (
            <div className="empty-state">
              还没有正式记录。从“新记录”开始，或复制上方示例。
            </div>
          ) : (
            <div className="journal-list">
              {book.notes.map((n) => (
                <a key={n.id} href={href("notes", n.id)}>
                  <span>
                    {n.stage} · {n.status}
                  </span>
                  <strong>{n.title}</strong>
                  <small>{n.updatedAt.slice(0, 10)}</small>
                  <ArrowUpRight size={16} />
                </a>
              ))}
            </div>
          )}
        </>
      )}
    </>
  );
}

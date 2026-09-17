import { useEffect, useRef, useState } from "react";
import registry from "./registry";
import { validateMap } from "../../shared/contracts.mjs";
import type { WorldMap } from "./types";
const cacheKey = (id: string) => `kamaen-free-map-v1:${id}`;
export function downloadMap(doc: WorldMap) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(doc, null, 2) + "\n"], {
      type: "application/json",
    }),
  );
  const a = document.createElement("a");
  a.href = url;
  a.download = `${doc.id}.json`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export default function useMapDocument(seed: WorldMap) {
  const [doc, setState] = useState(seed),
    ref = useRef(seed);
  const [ready, setReady] = useState(false),
    [dirty, setDirty] = useState(false),
    [local, setLocal] = useState(false),
    [busy, setBusy] = useState(false),
    [message, setMessage] = useState("");
  const [recovery, setRecovery] = useState<WorldMap | null>(null);
  const [undoCount, setUndoCount] = useState(0),
    history = useRef<WorldMap[]>([]),
    etag = useRef("");
  function update(next: WorldMap, checkpoint = true) {
    if (!ready) return;
    if (checkpoint) remember();
    ref.current = next;
    setState(next);
    setDirty(true);
  }
  function remember() {
    history.current = [...history.current.slice(-49), ref.current];
    setUndoCount(history.current.length);
  }
  function undo() {
    const next = history.current.pop();
    if (next) {
      update(next, false);
      setUndoCount(history.current.length);
    }
  }
  useEffect(() => {
    let active = true;
    (async () => {
      let next = seed,
        stamp = "static",
        staticMode = false;
      try {
        const response = await fetch(
          `./api/maps/${encodeURIComponent(seed.id)}`,
        );
        if (
          !response.headers.get("content-type")?.includes("application/json")
        ) {
          staticMode = true;
        } else {
          const result = await response.json();
          if (!response.ok) throw Error(result.error);
          if (!validateMap(result.document, registry))
            throw Error("地图格式无效");
          next = result.document;
          stamp = result.etag;
        }
      } catch (e) {
        if (active) {
          setMessage(
            `文件读取失败：${e}。可查看构建时内容并导出；重新读取成功前禁止写入文件。`,
          );
          staticMode = true;
        }
      }
      if (!active) return;
      etag.current = stamp;
      setLocal(staticMode);
      ref.current = next;
      setState(next);
      try {
        const saved = JSON.parse(
          localStorage.getItem(cacheKey(seed.id)) || "null",
        );
        if (saved && validateMap(saved.document, registry)) {
          if (saved.etag === stamp) {
            ref.current = saved.document;
            setState(saved.document);
            setDirty(true);
            setMessage("已恢复未保存的画布草稿。");
          } else {
            setRecovery(saved.document);
            setMessage("检测到旧草稿与文件版本不同，可以先导出旧草稿。");
          }
        }
      } catch {
        setMessage("草稿无法读取，当前显示文件中的地图。");
      }
      setReady(true);
    })();
    return () => {
      active = false;
    };
  }, [seed]);
  useEffect(() => {
    if (!ready || !dirty) return;
    try {
      localStorage.setItem(
        cacheKey(seed.id),
        JSON.stringify({ document: doc, etag: etag.current }),
      );
    } catch {
      setMessage("浏览器草稿空间不足，请保存文件或导出。");
    }
  }, [doc, dirty, ready, seed.id]);
  useEffect(() => {
    if (!dirty) return;
    const warn = (e: BeforeUnloadEvent) => e.preventDefault();
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);
  async function save() {
    const snapshot = ref.current;
    if (!validateMap(snapshot, registry)) {
      setMessage("地图中存在无效字段或引用，请修正后保存。");
      return;
    }
    if (local) {
      downloadMap(snapshot);
      setMessage("当前为静态/离线模式，已导出文件；浏览器仍保留草稿。");
      return;
    }
    setBusy(true);
    try {
      const response = await fetch(
        `./api/maps/${encodeURIComponent(seed.id)}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "If-Match": etag.current,
          },
          body: JSON.stringify(snapshot),
        },
      );
      const result = await response.json();
      if (!response.ok) throw Error(result.error);
      etag.current = result.etag;
      if (ref.current === snapshot) {
        ref.current = result.document;
        setState(result.document);
        setDirty(false);
        localStorage.removeItem(cacheKey(seed.id));
      } else {
        update({ ...ref.current, revision: result.document.revision }, false);
      }
      setMessage("已保存到当前地图文件。");
    } catch (e) {
      setMessage(String(e));
    } finally {
      setBusy(false);
    }
  }
  async function importFile(file: File) {
    if (!ready || busy) return;
    try {
      if (file.size > 2000000) throw Error("文件超过 2 MB");
      const next = JSON.parse(await file.text());
      if (!validateMap(next, registry)) throw Error("文件字段或引用无效");
      update({ ...next, id: seed.id, revision: ref.current.revision });
      setMessage("已载入为当前地图草稿；保存后写入当前地图文件。");
    } catch (e) {
      setMessage(String(e));
    }
  }
  return {
    doc,
    ref,
    update,
    remember,
    undo,
    undoCount,
    save,
    ready,
    dirty,
    local,
    busy,
    message,
    setMessage,
    recovery,
    clearRecovery: () => {
      setRecovery(null);
      localStorage.removeItem(cacheKey(seed.id));
    },
    importFile,
  };
}

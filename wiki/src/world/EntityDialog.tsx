import { useLayoutEffect, useRef, useState } from "react";
import { X, ArrowUpRight } from "lucide-react";
import { entityById } from "./registry";
import EntityContent from "./EntityContent";
import { clamp } from "./geometry";
export type Spotlight = {
  id: string;
  anchor: DOMRect;
  trigger: HTMLElement | null;
};
export default function EntityDialog({
  value,
  onClose,
}: {
  value: Spotlight;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const [id, setId] = useState(value.id);
  const [viewport, setViewport] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });
  useLayoutEffect(() => {
    const resize = () =>
      setViewport({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, []);
  const entity = entityById(id);
  useLayoutEffect(() => {
    const d = ref.current!;
    const trigger = value.trigger;
    d.showModal();
    d.querySelector<HTMLButtonElement>("button")?.focus();
    return () => {
      d.close();
      trigger?.focus({ preventScroll: true });
    };
  }, [value]);
  if (!entity) return null;
  const width = Math.min(520, viewport.width - 24),
    height = Math.min(650, viewport.height - 32);
  const left = clamp(value.anchor.left - 20, 12, viewport.width - width - 12);
  const below = value.anchor.bottom + 12;
  const top =
    below + height < viewport.height - 16
      ? below
      : clamp(value.anchor.top - 28, 16, viewport.height - height - 16);
  return (
    <dialog
      className="entity-dialog"
      ref={ref}
      aria-label={`${entity.title}详情`}
      style={{
        left,
        top,
        width,
        maxHeight: height,
        transformOrigin: `${clamp(value.anchor.left - left, 0, width)}px ${clamp(value.anchor.top - top, 0, height)}px`,
      }}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
      onClick={(e) => {
        if (e.target === ref.current) {
          const r = e.currentTarget.getBoundingClientRect();
          if (
            e.clientX < r.left ||
            e.clientX > r.right ||
            e.clientY < r.top ||
            e.clientY > r.bottom
          )
            onClose();
        }
      }}
    >
      <div className="entity-dialog-bar">
        <span>对象详情</span>
        <a href={`#/entities/${encodeURIComponent(id)}`} onClick={onClose}>
          完整档案 <ArrowUpRight size={14} />
        </a>
        <button aria-label="关闭对象详情" onClick={onClose}>
          <X size={18} />
        </button>
      </div>
      <div className="entry-acquisition" key={id} aria-hidden="true">
        <i />
      </div>
      <div className="entity-dialog-content">
        <EntityContent
          entity={entity}
          onRelated={(next) => {
            setId(next);
            ref.current?.scrollTo(0, 0);
          }}
        />
      </div>
    </dialog>
  );
}

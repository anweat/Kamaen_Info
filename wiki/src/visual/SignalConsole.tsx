import { useRef } from "react";
import { Activity, Pause, Play, X } from "lucide-react";
import registry from "../world/registry";
import { useSignal } from "./SignalState";
export function SignalConsole() {
  const { seen, frequency, motion, setFrequency, setMotion, clear, revision } =
    useSignal();
  const known = registry.entities.filter((e) => seen.includes(e.id)),
    count = known.length,
    total = registry.entities.length;
  const amplitude = 10 + (total ? count / total : 0) * 9;
  const wave = Array.from(
    { length: 441 },
    (_, x) =>
      `${x ? "L" : "M"}${x},${36 - amplitude * Math.sin((x / 220) * Math.PI * 2) - 3 * Math.sin((x / 220) * Math.PI * 6)}`,
  ).join(" ");
  return (
    <section className="signal-console" aria-label="信息积累与显示频率">
      <div className="signal-console-title">
        <span>
          <i /> OBSERVATION
        </span>
        <button
          aria-label={motion ? "暂停环境动效" : "启用环境动效"}
          aria-pressed={motion}
          onClick={() => setMotion(!motion)}
        >
          {motion ? <Pause size={12} /> : <Play size={12} />}
        </button>
      </div>
      <div className="signal-measure">
        <span>观测索引</span>
        <strong key={revision}>
          {String(count).padStart(2, "0")}
          <small> / {String(total).padStart(2, "0")}</small>
        </strong>
      </div>
      <svg className="signal-scope" viewBox="0 0 220 72" aria-hidden="true">
        {[16, 36, 56].map((y) => (
          <line key={y} x1="0" x2="220" y1={y} y2={y} className="scope-grid" />
        ))}
        <path className="signal-wave" d={wave} />
        <line x1="180" x2="180" y1="6" y2="66" className="scope-cursor" />
        <circle cx="180" cy="46" r="2" className="scope-dot" />
      </svg>
      <div
        className="information-cells"
        role="img"
        aria-label={`已观测 ${count} / ${total} 个实体`}
      >
        {registry.entities.map((e) => (
          <i
            key={e.id}
            title={
              seen.includes(e.id)
                ? `已观测 · ${e.title}`
                : `未观测 · ${e.title}`
            }
            className={seen.includes(e.id) ? "recorded" : ""}
          />
        ))}
      </div>
      <label className="frequency-control">
        <span>显示频率</span>
        <output>
          {frequency.toFixed(1)} <small>Hz</small>
        </output>
        <input
          aria-label="显示频率"
          type="range"
          min=".2"
          max="1.6"
          step=".1"
          value={frequency}
          onChange={(e) => setFrequency(Number(e.target.value))}
        />
      </label>
      <div className="signal-footnote">
        <span>打开实体，留下观测痕迹</span>
        <button onClick={clear}>重置</button>
      </div>
    </section>
  );
}
export function SignalStatus() {
  const ref = useRef<HTMLDialogElement>(null),
    { seen } = useSignal();
  const count = registry.entities.filter((e) => seen.includes(e.id)).length;
  return (
    <>
      <button
        className="signal-status"
        aria-label="打开观测与频率设置"
        onClick={() => ref.current?.showModal()}
      >
        <Activity size={14} />
        <span>观测索引</span>
        <b>{String(count).padStart(2, "0")}</b>
        <small> / {String(registry.entities.length).padStart(2, "0")}</small>
      </button>
      <dialog
        ref={ref}
        className="signal-settings"
        aria-label="观测与频率设置"
        onClick={(e) => {
          if (e.target === ref.current) {
            const r = e.currentTarget.getBoundingClientRect();
            if (
              e.clientX < r.left ||
              e.clientX > r.right ||
              e.clientY < r.top ||
              e.clientY > r.bottom
            )
              ref.current.close();
          }
        }}
      >
        <button
          className="signal-close"
          aria-label="关闭频率设置"
          onClick={() => ref.current?.close()}
        >
          <X size={17} />
        </button>
        <SignalConsole />
        <p>这是当前浏览器的阅读痕迹与视觉节律，不参与模组数值或地图保存。</p>
      </dialog>
    </>
  );
}

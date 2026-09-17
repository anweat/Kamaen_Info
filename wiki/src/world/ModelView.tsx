import { useState } from "react";
import type { Expression, ModelSpec } from "./types";
export function evaluate(
  exp: Expression,
  values: Record<string, number>,
): number {
  if (typeof exp === "number") return exp;
  if (typeof exp === "string") return values[exp] ?? NaN;
  const [a, b] = exp.args.map((e) => evaluate(e, values));
  switch (exp.op) {
    case "add":
      return a + b;
    case "sub":
      return a - b;
    case "mul":
      return a * b;
    case "div":
      return b === 0 ? NaN : a / b;
    case "pow":
      return Math.pow(a, b);
    case "sin":
      return Math.sin(a);
    case "exp":
      return Math.exp(a);
  }
}
export default function ModelView({ spec }: { spec: ModelSpec }) {
  const [values, setValues] = useState(() =>
    Object.fromEntries(spec.parameters.map((p) => [p.id, p.value])),
  );
  const samples = Array.from({ length: 121 }, (_, i) => {
    const x = spec.x.min + ((spec.x.max - spec.x.min) * i) / 120;
    return { x, y: evaluate(spec.expression, { ...values, [spec.x.id]: x }) };
  });
  const valid = samples.filter((p) => Number.isFinite(p.y));
  const min = Math.min(0, ...valid.map((p) => p.y)),
    max = Math.max(1, ...valid.map((p) => p.y));
  let previous = false;
  const path = samples
    .map((p, i) => {
      if (!Number.isFinite(p.y)) {
        previous = false;
        return "";
      }
      const cmd = previous ? "L" : "M";
      previous = true;
      return `${cmd}${42 + (i / 120) * 390},${162 - ((p.y - min) / (max - min)) * 135}`;
    })
    .join(" ");
  return (
    <div
      className="model-view"
      onPointerDown={(e) => e.stopPropagation()}
      onWheel={(e) => e.stopPropagation()}
    >
      <code className="model-formula">{spec.formula}</code>
      <svg
        viewBox="0 0 460 200"
        role="img"
        aria-label={`${spec.output}随${spec.x.label}变化的曲线`}
      >
        {[0, 1, 2, 3].map((i) => (
          <line
            key={i}
            x1="42"
            x2="432"
            y1={27 + i * 45}
            y2={27 + i * 45}
            stroke="#d8dfd0"
            strokeDasharray="3 5"
          />
        ))}
        <path d="M42 18V162H438" stroke="#80927a" fill="none" />
        <text x="8" y="31">
          {max.toFixed(1)}
        </text>
        <text x="9" y="165">
          {min.toFixed(1)}
        </text>
        <text x="38" y="185">
          {spec.x.min}
        </text>
        <text x="420" y="185">
          {spec.x.max}
        </text>
        <text x="180" y="190">
          {spec.x.label}
        </text>
        <path
          className="model-curve"
          d={path}
          fill="none"
          stroke="#607f58"
          strokeWidth="2.5"
        />
      </svg>
      {!valid.length && <p role="status">当前参数没有有限结果，请调整参数。</p>}
      {spec.parameters.map((p) => (
        <label className="model-parameter" key={p.id}>
          <span>{p.label}</span>
          <input
            aria-label={p.label}
            type="range"
            min={p.min}
            max={p.max}
            step={p.step}
            value={values[p.id]}
            onChange={(e) =>
              setValues({ ...values, [p.id]: Number(e.target.value) })
            }
          />
          <output>{values[p.id].toFixed(2)}</output>
        </label>
      ))}
      <small>示例模型 · 参数只影响当前预览</small>
    </div>
  );
}

// Projected reference lattice, built from geometry so it stays crisp at any resolution.
const project = (u: number, v: number) => {
  const r = 155 + 54 * Math.cos(v),
    x = r * Math.cos(u),
    y = r * Math.sin(u),
    z = 54 * Math.sin(v);
  return `${(350 + x * 0.95 + y * 0.24).toFixed(2)},${(260 - y * 0.4 + z * 0.9 + x * 0.12).toFixed(2)}`;
};
const rings = Array.from({ length: 18 }, (_, i) =>
  Array.from(
    { length: 101 },
    (_, j) =>
      `${j ? "L" : "M"}${project((j / 100) * Math.PI * 2, (i / 18) * Math.PI * 2)}`,
  ).join(" "),
);
const spokes = Array.from({ length: 32 }, (_, i) =>
  Array.from(
    { length: 51 },
    (_, j) =>
      `${j ? "L" : "M"}${project((i / 32) * Math.PI * 2, (j / 50) * Math.PI * 2)}`,
  ).join(" "),
);
export default function SpaceField() {
  return (
    <div className="space-field" aria-hidden="true">
      <div className="pointer-field" />
      <svg className="spacetime-lattice" viewBox="0 0 700 520">
        <g>
          {rings.map((d, i) => (
            <path d={d} key={`r${i}`} />
          ))}
          {spokes.map((d, i) => (
            <path d={d} key={`s${i}`} />
          ))}
        </g>
        <circle cx="350" cy="260" r="234" className="orbit-reference" />
        <path d="M350 9v28M350 483v28M99 260h28M573 260h28" />
        <text x="348" y="24">
          τ
        </text>
        <text x="615" y="265">
          λ
        </text>
      </svg>
      <div className="field-crosshair field-crosshair-a" />
      <div className="field-crosshair field-crosshair-b" />
      <div className="temporal-ruler">
        {Array.from({ length: 61 }, (_, i) => (
          <i key={i} className={i % 5 === 0 ? "major" : ""} />
        ))}
        <span>SPACETIME / INFORMATION FIELD</span>
      </div>
    </div>
  );
}

import { useRef, useState, type CSSProperties } from "react";
import { RotateCcw, ChevronLeft, ChevronRight } from "lucide-react";
import { textureFor, type Item } from "../data";
export default function BlockPreview({ item }: { item: Item }) {
  const [angle, setAngle] = useState(-35);
  const drag = useRef<number | null>(null);
  const texture = textureFor(item);
  const style = {
    "--block-texture": texture
      ? `url("${import.meta.env.BASE_URL}textures/${texture}")`
      : "none",
    "--block-angle": `${angle}deg`,
  } as CSSProperties;
  return (
    <section className="block-preview" style={style}>
      <div
        className="block-stage"
        onPointerDown={(e) => {
          drag.current = e.clientX;
          e.currentTarget.setPointerCapture(e.pointerId);
        }}
        onPointerMove={(e) => {
          if (drag.current !== null) {
            setAngle((a) => a + (e.clientX - drag.current!) * 0.6);
            drag.current = e.clientX;
          }
        }}
        onPointerUp={() => (drag.current = null)}
        onPointerCancel={() => (drag.current = null)}
      >
        <div className="block-cube" aria-label={`${item.name} 三维方块示意`}>
          {["front", "back", "left", "right", "top", "bottom"].map((face) => (
            <div key={face} className={"cube-" + face} />
          ))}
        </div>
      </div>
      <div className="button-row">
        <button
          aria-label="向左旋转方块"
          onClick={() => setAngle((a) => a - 30)}
        >
          <ChevronLeft size={15} />
        </button>
        <button aria-label="重置方块视角" onClick={() => setAngle(-35)}>
          <RotateCcw size={15} />
        </button>
        <button
          aria-label="向右旋转方块"
          onClick={() => setAngle((a) => a + 30)}
        >
          <ChevronRight size={15} />
        </button>
      </div>
      <p>
        拖动旋转 · 六面使用示例表面
        <br />
        外形与材质均待后续补充
      </p>
    </section>
  );
}

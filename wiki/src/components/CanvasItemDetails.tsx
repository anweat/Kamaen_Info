import { ArrowUpRight, X, LocateFixed } from "lucide-react";
import { data, href, itemById, type Item } from "../data";
import ItemVisual from "./ItemVisual";
const earlyGuides: Record<string, string[]> = {
  white_noise_seed: ["e1:raw_kamaen_crystal", "e1:thermal_noise_crucible"],
  raw_kamaen_crystal: [
    "e1:waveguide_kamaen_crystal",
    "e1:compression_kamaen_crystal",
    "e1:explosion_chamber_controller",
  ],
  waveguide_kamaen_crystal: ["e1:fractionating_tower", "r4:guide"],
  compression_kamaen_crystal: ["e1:tier1_mechanical_framework"],
  stable_spectrum_kamaen_crystal: ["e1:basic_spectroscope", "r4:light_source"],
};
export default function CanvasItemDetails({
  item,
  close,
  guide,
}: {
  item: Item;
  close: () => void;
  guide: (id: string) => void;
}) {
  const produced = data.recipes.filter(
    (r) => item.version === "R4" && r.outputs[item.legacy],
  );
  const used = data.recipes.filter(
    (r) => item.version === "R4" && r.inputs[item.legacy],
  );
  const refs =
    earlyGuides[item.legacy] ||
    [
      ...new Set([
        ...produced.flatMap((r) => Object.keys(r.inputs)),
        ...used.flatMap((r) => Object.keys(r.outputs)),
      ]),
    ]
      .slice(0, 8)
      .map((id) => "r4:" + id);
  return (
    <div
      className="canvas-item-detail"
      role="region"
      aria-label={`${item.name}详情`}
    >
      <div className="inline-item-title">
        <ItemVisual item={item} />
        <div>
          <h3>{item.name}</h3>
          <span>
            {item.stage} · {item.kind} · 示例
          </span>
        </div>
        <button aria-label="收起物品详情" onClick={close}>
          <X size={13} />
        </button>
      </div>
      <p className="inline-item-effect">{item.note || "作用说明待补充。"}</p>
      <dl>
        <dt>如何取得</dt>
        <dd>{item.acquisition}</dd>
        <dt>状态 / 操作</dt>
        <dd>{item.state || "后续讨论补充。"}</dd>
      </dl>
      {refs.length > 0 && (
        <>
          <div className="inline-guide-heading">
            <LocateFixed size={12} />
            沿着物品继续{item.version === "E1" && <small>关系示例</small>}
          </div>
          <div className="inline-item-guides">
            {refs.map((id) => {
              const target = itemById(id);
              return target ? (
                <button key={id} onClick={() => guide(id)}>
                  <ItemVisual item={target} />
                  <span>{target.name}</span>
                  <ArrowUpRight size={12} />
                </button>
              ) : null;
            })}
          </div>
        </>
      )}
      <div className="inline-detail-links">
        <a href={href("items", item.id)}>
          完整条目 <ArrowUpRight size={12} />
        </a>
        <a href={href("notes", "new~item~" + item.id)}>关联研究记录 ＋</a>
      </div>
    </div>
  );
}

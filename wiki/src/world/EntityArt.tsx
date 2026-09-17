import type { CSSProperties } from "react";
import registry from "./registry";
import type { Entity } from "./types";
export default function EntityArt({ entity }: { entity: Entity }) {
  const v = entity.visual,
    asset = v?.asset && registry.assets[v.asset];
  if (v?.type === "block")
    return (
      <span
        className="entity-art block-art"
        style={{ "--voxel-color": v.color || "#8da490" } as CSSProperties}
        aria-label={`${entity.title}斜视方块`}
      >
        <span className="iso-cube">
          <span className="iso-top">
            {(v.top || asset) && (
              <img
                src={registry.assets[v.top || ""] || asset || undefined}
                alt=""
              />
            )}
          </span>
          <span className="iso-left">
            {asset && <img src={asset} alt="" />}
          </span>
          <span className="iso-right">
            {(v.side || asset) && (
              <img
                src={registry.assets[v.side || ""] || asset || undefined}
                alt=""
              />
            )}
          </span>
        </span>
      </span>
    );
  return (
    <span className="entity-art sprite-art">
      {asset ? (
        <img src={asset} alt={entity.title} />
      ) : (
        <svg viewBox="0 0 32 32" aria-label={`${entity.title}占位贴图`}>
          <path
            fill={v?.color || "#8da490"}
            d="M14 3h5v5h5v15h-5v6h-7v-7H7V10h7z"
          />
          <path fill="#dae4bc" d="M14 7h3v13h-5V11h2z" />
        </svg>
      )}
    </span>
  );
}

import registry, { entityById } from "./registry";
import type { MapNode } from "./types";
import EntityArt from "./EntityArt";
import { CustomView, FileMarkdown } from "./EntityContent";
import SceneViewer from "../components/SceneViewer";
import ModelView from "./ModelView";
import { displayInk } from "../visual/ink";
export default function WorldNode({
  node,
  onOpen,
}: {
  node: MapNode;
  onOpen: (element: HTMLElement) => void;
}) {
  if (node.type === "entity") {
    const entity = entityById(node.ref);
    return entity ? (
      <button
        className="world-entity"
        aria-label={`打开${entity.title}详情`}
        onClick={(e) => {
          if (e.detail === 0) onOpen(e.currentTarget);
        }}
      >
        <EntityArt entity={entity} />
        <span>{node.title || entity.title}</span>
      </button>
    ) : (
      <span>未注册：{node.ref}</span>
    );
  }
  if (node.type === "text")
    return (
      <div
        className="world-text"
        style={{ fontSize: node.fontSize || 18, color: displayInk(node.color) }}
      >
        {node.title && <h2>{node.title}</h2>}
        <FileMarkdown body={node.body || ""} />
      </div>
    );
  if (node.type === "rect")
    return (
      <span className="world-rect-label" style={{ color: node.color }}>
        {node.title}
      </span>
    );
  const scene = registry.scenes.find((s) => s.id === node.ref),
    model = registry.models.find((s) => s.id === node.ref);
  return (
    <div className="world-space">
      <div className="world-space-title">
        {node.title || node.ref}
        <small>
          {node.type === "space3d"
            ? "3D"
            : node.type === "space2d"
              ? "2D"
              : "CUSTOM"}
        </small>
      </div>
      <div
        className="world-space-content"
        onPointerDown={(e) => e.stopPropagation()}
        onWheel={(e) => e.stopPropagation()}
      >
        {node.type === "space3d" && scene ? (
          <SceneViewer key={scene.id} scene={scene} compact />
        ) : node.type === "space2d" && model ? (
          <ModelView key={model.id} spec={model} />
        ) : node.type === "custom" ? (
          <CustomView id={node.ref || ""} />
        ) : (
          <p>内容引用尚未注册</p>
        )}
      </div>
    </div>
  );
}

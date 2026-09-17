import { useState } from "react";
import registry, { entityById, kindNames } from "./registry";
import EntityArt from "./EntityArt";
import EntityContent, { CustomView } from "./EntityContent";
import ModelView from "./ModelView";
import SceneViewer from "../components/SceneViewer";
export function EntityLibrary({
  id,
  nbt = false,
}: {
  id?: string;
  nbt?: boolean;
}) {
  const [query, setQuery] = useState(""),
    [kind, setKind] = useState(nbt ? "nbt" : "all");
  const entity = entityById(id);
  if (id)
    return entity ? (
      <article className="entity-document">
        <a href="#/entities">← 实体总览</a>
        <EntityContent entity={entity} />
      </article>
    ) : (
      <p>
        未找到实体：{id}。<a href="#/entities">返回总览</a>
      </p>
    );
  const entries = registry.entities.filter(
    (e) =>
      (kind === "all" || e.kind === kind) &&
      `${e.title} ${e.id} ${e.tags.join(" ")}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  return (
    <>
      <div className="eyebrow">OBJECT ATLAS / 注册实体</div>
      <h1>{nbt ? "NBT 与实体状态" : "方块、物品与实体"}</h1>
      <p className="lead">同一个对象，可以出现在地图、说明和实验空间中。</p>
      <div className="filter-bar">
        <input
          aria-label="搜索文件实体"
          placeholder="名称、标签或 ID…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          aria-label="实体类型"
          value={kind}
          onChange={(e) => setKind(e.target.value)}
        >
          <option value="all">全部类型</option>
          {Object.entries(kindNames).map(([id, label]) => (
            <option key={id} value={id}>
              {label}
            </option>
          ))}
        </select>
        <span>{entries.length} 个文件实体</span>
        <a className="text-link" href="#/archive-items">
          查看 rebuild 导入目录 ↗
        </a>
      </div>
      <div className="file-entity-grid">
        {entries.map((e) => (
          <a key={e.id} href={`#/entities/${encodeURIComponent(e.id)}`}>
            <EntityArt entity={e} />
            <strong>{e.title}</strong>
            <small>{kindNames[e.kind]}</small>
          </a>
        ))}
      </div>
      {!entries.length && <p>没有匹配内容，尝试其他名称或类型。</p>}
      <p className="muted">
        新建实体文件后自动加入此目录；材质和机制仍为示例。
      </p>
    </>
  );
}
export function SpatialLibrary() {
  const [id, setId] = useState(registry.scenes[0]?.id || "");
  const scene = registry.scenes.find((s) => s.id === id);
  return (
    <>
      <div className="eyebrow">SPATIAL ATLAS / 空间档案</div>
      <h1>3D 查看</h1>
      <p className="lead">从不同角度查看部件，以及它们构成的关系。</p>
      <div className="filter-bar">
        <label>
          场景
          <select value={id} onChange={(e) => setId(e.target.value)}>
            {registry.scenes.map((s) => (
              <option key={s.id} value={s.id}>
                {s.title}
              </option>
            ))}
          </select>
        </label>
      </div>
      {scene ? (
        <div className="spatial-page">
          <SceneViewer key={id} scene={scene} />
          <aside>
            <h2>{scene.title}</h2>
            <p>{scene.subtitle}</p>
            <h3>关联实体</h3>
            {registry.entities
              .filter((e) => e.scene === id)
              .map((e) => (
                <a
                  className="spatial-related"
                  key={e.id}
                  href={`#/entities/${encodeURIComponent(e.id)}`}
                >
                  <EntityArt entity={e} />
                  <span>{e.title}</span>
                </a>
              ))}
          </aside>
        </div>
      ) : (
        <p>添加场景文件后即可开始查看。</p>
      )}
    </>
  );
}
export function ModelLab() {
  const [id, setId] = useState(registry.models[0]?.id || "");
  const model = registry.models.find((m) => m.id === id);
  return (
    <>
      <div className="eyebrow">MODEL WORKBENCH / 假设与推演</div>
      <h1>模型实验台</h1>
      <p className="lead">
        移动参数，看关系如何变化；把下一次实验的问题留下来。
      </p>
      <div className="filter-bar">
        <label>
          模型
          <select value={id} onChange={(e) => setId(e.target.value)}>
            {registry.models.map((m) => (
              <option key={m.id} value={m.id}>
                {m.title}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="model-lab-grid">
        {model ? (
          <section>
            <h2>{model.title}</h2>
            <ModelView key={id} spec={model} />
            <p>预填充公式用于讨论交互，尚未与游戏物理或实测数据校准。</p>
          </section>
        ) : (
          <p>添加模型 JSON 后自动出现。</p>
        )}
        <aside>
          <h2>独立渲染实验</h2>
          {registry.renderers.map((r) => (
            <div key={r.id}>
              <h3>{r.title}</h3>
              <CustomView id={r.id} />
            </div>
          ))}
        </aside>
      </div>
    </>
  );
}

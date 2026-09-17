import ReactMarkdown, { defaultUrlTransform } from "react-markdown";
import remarkGfm from "remark-gfm";
import registry, { entityById, kindNames } from "./registry";
import type { Entity } from "./types";
import EntityArt from "./EntityArt";
import SceneViewer from "../components/SceneViewer";
import ModelView from "./ModelView";
import { useEffect } from "react";
import { useSignal } from "../visual/SignalState";
export function FileMarkdown({ body }: { body: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        urlTransform={(url) =>
          url.startsWith("asset:")
            ? registry.assets[url.slice(6)] || ""
            : defaultUrlTransform(url)
        }
        components={{
          img: ({ src, alt }) => (
            <img className="entity-inline-image" src={src} alt={alt || ""} />
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              {...(href?.startsWith("http")
                ? { target: "_blank", rel: "noreferrer" }
                : {})}
            >
              {children}
            </a>
          ),
        }}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}
export function CustomView({ id }: { id: string }) {
  const r = registry.renderers.find((r) => r.id === id);
  return r ? (
    <iframe
      className="custom-view"
      title={r.title}
      sandbox="allow-scripts"
      referrerPolicy="no-referrer"
      srcDoc={r.html}
    />
  ) : (
    <p>渲染文件未注册：{id}</p>
  );
}
export default function EntityContent({
  entity,
  onRelated,
}: {
  entity: Entity;
  onRelated?: (id: string) => void;
}) {
  const { observe } = useSignal();
  useEffect(() => {
    observe(entity.id);
  }, [entity.id, observe]);
  const scene = registry.scenes.find((s) => s.id === entity.scene),
    model = registry.models.find((m) => m.id === entity.model);
  return (
    <>
      <div className="entity-heading">
        <EntityArt entity={entity} />
        <div>
          <small>
            {kindNames[entity.kind]} / {entity.status}
          </small>
          <h2>{entity.title}</h2>
          <p>{entity.summary}</p>
        </div>
      </div>
      {entity.lifecycle && (
        <dl className="entity-lifecycle">
          {([
            ["design", "设计"], ["runtime", "游戏行为"],
            ["art", "美术"], ["verification", "验证"],
          ] as const).map(([key, label]) => (
            <div key={key}><dt>{label}</dt><dd>{entity.lifecycle![key]}</dd></div>
          ))}
        </dl>
      )}
      <FileMarkdown body={entity.body} />
      {!!entity.gallery?.length && (
        <div className="entity-gallery">
          {entity.gallery.map((g) => (
            <figure key={g.asset}>
              <img src={registry.assets[g.asset]} alt={g.caption} />
              <figcaption>{g.caption}</figcaption>
            </figure>
          ))}
        </div>
      )}
      {entity.fields && (
        <div className="table-scroll">
          <table>
            <caption>NBT 字段草案</caption>
            <thead>
              <tr>
                <th>字段 / 类型</th>
                <th>默认值</th>
                <th>描述</th>
              </tr>
            </thead>
            <tbody>
              {entity.fields.map((f) => (
                <tr key={f.name}>
                  <td>
                    <code>{f.name}</code>
                    <br />
                    <small>{f.type}</small>
                  </td>
                  <td>
                    <code>{JSON.stringify(f.default)}</code>
                  </td>
                  <td>{f.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {scene && <SceneViewer key={scene.id} scene={scene} />}
      {model && <ModelView key={model.id} spec={model} />}
      {entity.renderer && <CustomView id={entity.renderer} />}
      {!!entity.relations?.length && (
        <div className="entity-relations">
          <h3>沿着关系继续</h3>
          {entity.relations.map((r) => {
            const e = entityById(r.target)!;
            return (
              <button
                key={r.target}
                onClick={() =>
                  onRelated
                    ? onRelated(e.id)
                    : (location.hash = `#/entities/${encodeURIComponent(e.id)}`)
                }
              >
                <EntityArt entity={e} />
                <span>
                  {e.title}
                  <small>{r.label} ↗</small>
                </span>
              </button>
            );
          })}
        </div>
      )}
      <details className="entity-source">
        <summary>内容来源与注册信息</summary>
        <code>{entity.id}</code>
        <p>content/{entity.file}</p>
        <p>说明：content/{entity.description || "无"}</p>
        {entity.runtimeRef !== undefined && (
          <p>游戏注册对应：{entity.runtimeRef || "尚未确定"}；行为完成度见上方状态。</p>
        )}
        {!!entity.designRefs?.length && <ul>{entity.designRefs.map((ref) => (
          <li key={`${ref.document}:${ref.legacyId || ""}`}>
            <a href={`#/docs/${encodeURIComponent(ref.document)}`}>{ref.label}</a>
            {ref.legacyId && <> · <code>{ref.legacyId}</code></>}
          </li>
        ))}</ul>}
      </details>
    </>
  );
}

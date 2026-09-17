import { useState } from "react";
import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Box,
  GitBranch,
  Sparkles,
  ArrowLeft,
} from "lucide-react";
import { chapters, data, href, itemById } from "../data";
import { scenes } from "../scenes";
import SceneViewer from "./SceneViewer";
import { ItemCard, RecipeCard } from "./Catalog";
import Markdown from "./Markdown";
export function Overview() {
  return (
    <>
      <div className="eyebrow">
        <span className="live-dot" /> KAMAEN INFO / A LIVING FIELD GUIDE
      </div>
      <div className="title-row">
        <h1>
          世界的线索，
          <br />
          <span className="soft-title">从一枚晶体开始。</span>
        </h1>
        <span className="edition-stamp">
          FIELD
          <br />
          NOTES<span>VOL. 01 / 工作稿</span>
        </span>
      </div>
      <p className="lead overview-lead">
        记录物质的变化，理解信息的流动。
        <br />
        一份从初步想法，生长为完整世界的交互档案。
      </p>
      <div className="intro-actions">
        <a className="primary button-link" href={href("story", "01")}>
          从第一章开始 <ArrowRight size={16} />
        </a>
        <a className="text-link" href={href("notes", "new")}>
          记下一个新想法 <span>＋</span>
        </a>
      </div>
      <div className="featured-layout">
        <div className="feature-scene">
          <SceneViewer compact />
          <div className="feature-scene-footer">
            <span>
              <span className="tiny-code">SCENE 001</span>
              <strong>从晶坯到第一份响应</strong>
            </span>
            <a
              className="icon-link"
              aria-label="进入结构演示"
              href={href("structures", "impact")}
            >
              <ArrowUpRight size={22} />
            </a>
          </div>
        </div>
        <article className="feature-note">
          <span className="eyebrow">当前探索 / E1</span>
          <div className="pixel-spark">✦</div>
          <h2>
            让晶体的构造，
            <br />
            真正回到生产。
          </h2>
          <p>
            保留参考、改变一次加工、重新测量。研究的结果，应当改善一项已经存在的工作。
          </p>
          <div className="note-rule" />
          <span className="small muted">本轮的三个问题</span>
          <ol>
            <li>最早的晶种如何被发现？</li>
            <li>结构与方向怎样改变响应？</li>
            <li>怎样留下可验证的记录？</li>
          </ol>
          <a href={href("notes", "example")}>
            打开这条研究线索 <ArrowRight size={16} />
          </a>
        </article>
      </div>
      <div className="section-heading">
        <div>
          <span className="eyebrow">THE THREAD THROUGH EVERYTHING</span>
          <h2>沿着一条线索，走进整个世界</h2>
        </div>
        <a href={href("story")}>
          完整发展线 <ArrowUpRight size={15} />
        </a>
      </div>
      <div className="chapter-road">
        {chapters.map((c, i) => (
          <a href={href("story", c.id)} className="road-node" key={c.id}>
            <span className="road-marker">{c.id}</span>
            <small>{c.range}</small>
            <strong>{c.short}</strong>
            <span>{i === 0 ? "当前讨论" : c.version + " 工作稿"}</span>
          </a>
        ))}
      </div>
      <div className="section-heading">
        <div>
          <span className="eyebrow">COLLECT, CONNECT, UNDERSTAND</span>
          <h2>档案入口</h2>
        </div>
        <span className="small muted">示例先行 · 持续补全</span>
      </div>
      <div className="portal-grid">
        {[
          {
            page: "items",
            icon: Box,
            title: "物品与方块",
            sub: "材料、构件与它们的用途",
            meta: "E1 / R4 预填充目录",
          },
          {
            page: "recipes",
            icon: GitBranch,
            title: "配方与路线",
            sub: "从取得到制造，再到交互反馈",
            meta: "124 条候选配方",
          },
          {
            page: "structures",
            icon: Sparkles,
            title: "结构实验室",
            sub: "旋转、拆解与逐步理解",
            meta: "2 个可交互示例",
          },
          {
            page: "docs",
            icon: BookOpen,
            title: "文档书架",
            sub: "源文档、版本与思路依据",
            meta: `${data.docs.length} 份原文`,
          },
        ].map((p) => (
          <a className="portal" href={href(p.page)} key={p.page}>
            <p.icon size={22} strokeWidth={1.5} />
            <h3>{p.title}</h3>
            <p>{p.sub}</p>
            <span>
              {p.meta}
              <ArrowUpRight size={14} />
            </span>
          </a>
        ))}
      </div>
      <div className="section-heading">
        <h2>工作台上的几件东西</h2>
        <a href={href("items")}>
          翻开图鉴 <ArrowUpRight size={15} />
        </a>
      </div>
      <div className="catalog-grid featured-items">
        {[
          "e1:white_noise_seed",
          "e1:raw_kamaen_crystal",
          "e1:waveguide_kamaen_crystal",
          "r4:endpoint_chip",
        ].map(
          (id) => itemById(id) && <ItemCard key={id} item={itemById(id)!} />,
        )}
      </div>
      <div className="bottom-note">
        <span>✦</span>
        <p>
          这里保存正在形成的想法。示例材质、结构布局与配方数值，都可以在后续讨论中替换。
        </p>
        <a href={href("docs", "README.md")}>
          了解文档版本 <ArrowRight size={14} />
        </a>
      </div>
    </>
  );
}
export function Story({ id }: { id?: string }) {
  const chapter = chapters.find((c) => c.id === id);
  const [expanded, setExpanded] = useState(false);
  if (chapter)
    return (
      <>
        <a className="back-link" href={href("story")}>
          <ArrowLeft size={15} /> 故事与发展线
        </a>
        <div className="eyebrow">
          CHAPTER {chapter.id} / {chapter.range} / {chapter.version}
        </div>
        <h1>{chapter.title}</h1>
        <p className="lead">{chapter.description}</p>
        <div className="chapter-reading">
          <article>
            <span className="status-tag">组合讲述示例 · 持续讨论</span>
            <h2>这一段，我们要理解什么</h2>
            <p>
              {chapter.description}{" "}
              每个发现都保留玩家的操作、记录和仍未解释的问题。
            </p>
            <div className="button-row">
              <a className="button-link" href={href("docs", chapter.file)}>
                当前玩法来源 <ArrowUpRight size={14} />
              </a>
              <a className="button-link" href={href("docs", chapter.story)}>
                故事与思想底稿 <ArrowUpRight size={14} />
              </a>
            </div>
            <h2>把内容放回同一段讲述</h2>
            <p>
              下面组合了这一阶段的对象和示例。可在研究记录中自由嵌入物品、配方与场景，继续延伸同一条线索。
            </p>
            {chapter.items.length > 0 ? (
              <div className="catalog-grid">
                {chapter.items.map(
                  (id) =>
                    itemById(id) && <ItemCard key={id} item={itemById(id)!} />,
                )}
              </div>
            ) : (
              <div className="empty-state">
                本阶段物品与结构尚待讨论。先保留叙事与来源，后续逐步添加。
              </div>
            )}
            {chapter.id === "03" && (
              <RecipeCard
                recipe={data.recipes.find((r) => r.id === "endpoint_chip")!}
                full
              />
            )}
            {["01", "03"].includes(chapter.id) && (
              <SceneViewer key={chapter.scene} sceneId={chapter.scene} />
            )}
            <button
              className="expand-button"
              aria-expanded={expanded}
              onClick={() => setExpanded((v) => !v)}
            >
              {expanded ? "收起" : "展开"}当前玩法原文
            </button>
            {expanded && (
              <Markdown>
                {data.docs.find((d) => d.id === chapter.file)?.body || ""}
              </Markdown>
            )}
          </article>
          <aside className="chapter-aside">
            <span className="eyebrow">沿着这条线继续</span>
            {chapters.map((c) => (
              <a
                key={c.id}
                className={c.id === id ? "selected" : ""}
                href={href("story", c.id)}
              >
                <span>{c.id}</span>
                {c.short}
              </a>
            ))}
            <p>
              版本优先级
              <br />
              前期 E1 → 中期 R4 → 全局 R1
            </p>
            <a
              className="text-link"
              href={href("notes", "new~doc~" + chapter.file)}
            >
              为本章写记录 ＋
            </a>
          </aside>
        </div>
      </>
    );
  return (
    <>
      <div className="eyebrow">03 / THE WORLD UNFOLDS</div>
      <h1>故事与发展线</h1>
      <p className="lead">让科技的推进，也是一次认识世界的过程。</p>
      <div className="story-list">
        {chapters.map((c) => (
          <a key={c.id} href={href("story", c.id)}>
            <span className="chapter-number">{c.id}</span>
            <div>
              <span className="eyebrow">
                {c.range} · {c.version}
              </span>
              <h2>{c.title}</h2>
              <p>{c.description}</p>
            </div>
            <ArrowUpRight />
          </a>
        ))}
      </div>
      <h2>全局能力依赖</h2>
      <p className="muted">
        R1 的 75 个能力节点，AND 前置单独列出。P01–05的实际操作与早期供电按
        E1，图中早期安排保留为R1基线。
      </p>
      <div className="capability-grid">
        {data.nodes.map((n) => (
          <article id={"node-" + n.id} key={n.id}>
            <span className="tiny-code">
              {n.milestone} · {n.track === "core" ? "主线" : "深化"}
            </span>
            <h3>{n.title}</h3>
            <p>{n.outcome}</p>
            <small>
              全部前置：
              {n.requires_all.length
                ? n.requires_all.map((r) => (
                    <a
                      key={r}
                      href={"#node-" + r}
                      onClick={(e) => {
                        e.preventDefault();
                        document
                          .getElementById("node-" + r)
                          ?.scrollIntoView({
                            behavior: "smooth",
                            block: "center",
                          });
                      }}
                    >
                      {data.nodes.find((x) => x.id === r)?.title} /{" "}
                    </a>
                  ))
                : "开局"}
            </small>
          </article>
        ))}
      </div>
    </>
  );
}
export function Structures({ id }: { id?: string }) {
  const selected = scenes.find((s) => s.id === id) || scenes[0];
  return (
    <>
      <div className="eyebrow">04 / THE STRUCTURE LAB</div>
      <h1>结构实验室</h1>
      <p className="lead">不只看见外形，也看见每个部件为什么在这里。</p>
      <div className="notice">
        交互示例 ·
        使用程序化像素材质。几何与部件排布用于说明，不是最终多方块定义或物理模拟。
      </div>
      <div className="scene-tabs">
        {scenes.map((s) => (
          <a
            className={selected.id === s.id ? "active" : ""}
            key={s.id}
            href={href("structures", s.id)}
          >
            {s.subtitle}
          </a>
        ))}
      </div>
      <div className="section-heading">
        <h2>{selected.title}</h2>
        <a href={href("docs", selected.source)}>
          设计来源 <ArrowUpRight size={15} />
        </a>
      </div>
      <SceneViewer key={selected.id} sceneId={selected.id} />
      <div className="bottom-note">
        <p>
          场景由部件坐标、说明、关联条目和演示步骤组成。后续可替换材质、增加结构，或嵌入任意研究记录。
        </p>
        <a href={href("notes", "new~scene~" + selected.id)}>
          围绕这个结构写记录 ＋
        </a>
      </div>
    </>
  );
}
export function Documents({ id }: { id?: string }) {
  const [query, setQuery] = useState("");
  const [group, setGroup] = useState("当前");
  const doc = data.docs.find((d) => d.id === id);
  if (id)
    return doc ? (
      <>
        <a className="back-link" href={href("docs")}>
          <ArrowLeft size={14} /> 文档书架
        </a>
        <div className="source-header">
          <span className="status-tag">{doc.group}</span>
          <code>docs/system-rebuild/{doc.id}</code>
        </div>
        {doc.group === "历史 / 依据" && (
          <div className="notice">
            历史 / 依据材料，当前规则以 E1、R4 与 R1 入口的覆盖关系为准。
          </div>
        )}
        <Markdown>{doc.body}</Markdown>
      </>
    ) : (
      <p>
        此文档尚未导入。<a href={href("docs")}>返回书架</a>
      </p>
    );
  const docs = data.docs.filter(
    (d) =>
      (group === "全部" ||
        (group === "当前" && d.group !== "历史 / 依据") ||
        d.group === group) &&
      `${d.title} ${d.id}`.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <>
      <div className="eyebrow">06 / SOURCES & REVISIONS</div>
      <h1>文档书架</h1>
      <p className="lead">回到原文，保留思路是怎样变化的。</p>
      <div className="notice">
        当前阅读顺序：E1 前期工作稿 → R4 计算研究阶段 → R1
        全局发展线。原文由构建时同步，网页记录独立保存。
      </div>
      <div className="filter-bar">
        <input
          aria-label="搜索文档"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索标题或文件名…"
        />
        <select
          aria-label="文档版本"
          value={group}
          onChange={(e) => setGroup(e.target.value)}
        >
          {["当前", "E1", "R4", "R1", "历史 / 依据", "全部"].map((g) => (
            <option key={g}>{g}</option>
          ))}
        </select>
        <span>{docs.length} 份</span>
      </div>
      <div className="doc-list">
        {docs.map((d) => (
          <a key={d.id} href={href("docs", d.id)}>
            <BookOpen size={19} />
            <div>
              <strong>{d.title}</strong>
              <code>{d.id}</code>
            </div>
            <span className="status-tag">{d.group}</span>
            <ArrowUpRight size={16} />
          </a>
        ))}
      </div>
      {!docs.length && <p className="empty-state">没有找到匹配文档。</p>}
    </>
  );
}

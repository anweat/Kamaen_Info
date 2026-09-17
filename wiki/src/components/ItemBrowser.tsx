import { Fragment, useState } from "react";
import {
  Search,
  List,
  Grid3X3,
  ArrowUpRight,
  ChevronDown,
  Pin,
} from "lucide-react";
import { data, href, itemById, type Item } from "../data";
import ItemVisual from "./ItemVisual";
export function ItemMention({ id }: { id: string }) {
  const item = itemById(id);
  return item ? (
    <a className="item-mention" href={href("items", id)}>
      <ItemVisual item={item} />
      <span>{item.name}</span>
      <span className="mention-tooltip" role="tooltip">
        <strong>
          {item.name} · {item.stage}
        </strong>
        <span>{item.note || "用途待补充"}</span>
      </span>
    </a>
  ) : (
    <span>{id}</span>
  );
}
export function LinkedText({
  text,
  version = "E1",
  exclude,
}: {
  text: string;
  version?: string;
  exclude?: string;
}) {
  const names = data.items
    .filter(
      (i) =>
        i.version === version &&
        i.id !== exclude &&
        i.name.length > 2 &&
        text.includes(i.name),
    )
    .sort((a, b) => b.name.length - a.name.length);
  if (!names.length) return <>{text}</>;
  const parts: React.ReactNode[] = [];
  let rest = text;
  for (let count = 0; count < 12 && rest; count++) {
    const next = names
      .map((i) => ({ item: i, at: rest.indexOf(i.name) }))
      .filter((x) => x.at >= 0)
      .sort((a, b) => a.at - b.at)[0];
    if (!next) break;
    parts.push(
      rest.slice(0, next.at),
      <ItemMention key={parts.length} id={next.item.id} />,
    );
    rest = rest.slice(next.at + next.item.name.length);
  }
  parts.push(rest);
  return <>{parts}</>;
}
function QuickInfo({ item }: { item: Item }) {
  return (
    <>
      <div className="quick-heading">
        <ItemVisual item={item} />
        <div>
          <span className="tiny-code">
            {item.version} · {item.stage}
          </span>
          <h2>{item.name}</h2>
          <span className="small muted">{item.kind}</span>
        </div>
      </div>
      <dl className="quick-facts">
        <dt>作用 / 用途</dt>
        <dd>
          <LinkedText
            text={item.note || "待补充具体用途"}
            version={item.version}
            exclude={item.id}
          />
        </dd>
        <dt>取得方式</dt>
        <dd>
          <LinkedText
            text={item.acquisition}
            version={item.version}
            exclude={item.id}
          />
        </dd>
        <dt>操作与状态</dt>
        <dd>{item.state || "待补充"}</dd>
      </dl>
      <div className="quick-links">
        <a href={href("items", item.id)}>
          完整条目与关联配方 <ArrowUpRight size={14} />
        </a>
        <a href={href("notes", "new~item~" + item.id)}>记录一个想法 ＋</a>
      </div>
    </>
  );
}
export default function ItemBrowser() {
  const [query, setQuery] = useState("");
  const [version, setVersion] = useState("E1");
  const [kind, setKind] = useState("全部");
  const [view, setView] = useState("atlas");
  const [open, setOpen] = useState<string | null>(null);
  const [preview, setPreview] = useState<Item | null>(null);
  const [pinned, setPinned] = useState(false);
  const list = data.items.filter(
    (i) =>
      (version === "全部" || i.version === version) &&
      (kind === "全部" || i.kind === kind) &&
      `${i.name} ${i.legacy} ${i.note}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  const current =
    preview && list.some((i) => i.id === preview.id) ? preview : list[0];
  return (
    <>
      <div className="eyebrow">01 / OBJECTS, AT A GLANCE</div>
      <h1>物品与方块</h1>
      <p className="lead">认出一件东西，了解它的作用，再沿着它找到下一件。</p>
      <div className="catalog-intro">
        <span className="status-tag">预填充图鉴</span>
        <p>
          点击贴图就地展开，点击名称进入完整条目。贴图均为临时示例，后续逐项替换。
        </p>
      </div>
      <div className="filter-bar">
        <label className="search-field">
          <Search size={17} />
          <input
            aria-label="搜索物品"
            placeholder="名称、用途或 ID…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <select
          aria-label="内容版本"
          value={version}
          onChange={(e) => {
            setVersion(e.target.value);
            setKind("全部");
            setPreview(null);
            setPinned(false);
          }}
        >
          <option>E1</option>
          <option>R4</option>
          <option>R1</option>
          <option>全部</option>
        </select>
        <select
          aria-label="物品分类"
          value={kind}
          onChange={(e) => setKind(e.target.value)}
        >
          {[
            "全部",
            ...new Set(
              data.items
                .filter((i) => version === "全部" || i.version === version)
                .map((i) => i.kind),
            ),
          ].map((k) => (
            <option key={k}>{k}</option>
          ))}
        </select>
      </div>
      <div className="catalog-toolbar">
        <span>
          {list.length} 个条目{" "}
          <span className="muted">/ 工作稿，非注册清单</span>
        </span>
        <div className="view-toggle">
          <button
            aria-pressed={view === "list"}
            onClick={() => setView("list")}
          >
            <List size={15} />
            图文列表
          </button>
          <button
            aria-pressed={view === "atlas"}
            onClick={() => setView("atlas")}
          >
            <Grid3X3 size={15} />
            贴图索引
          </button>
        </div>
      </div>
      {view === "list" ? (
        <div className="item-table-wrap">
          <table className="item-table">
            <thead>
              <tr>
                <th className="sprite-col">贴图</th>
                <th>名称 / 标识</th>
                <th>最早阶段</th>
                <th>作用与下一步</th>
                <th>取得方式</th>
              </tr>
            </thead>
            <tbody>
              {list.map((item) => (
                <Fragment key={item.id}>
                  <tr className={open === item.id ? "row-open" : ""}>
                    <td>
                      <button
                        className="sprite-button"
                        aria-label={`展开${item.name}`}
                        aria-expanded={open === item.id}
                        onClick={() =>
                          setOpen(open === item.id ? null : item.id)
                        }
                      >
                        <ItemVisual item={item} />
                        <ChevronDown size={10} />
                      </button>
                    </td>
                    <td>
                      <a
                        className="item-name-link"
                        href={href("items", item.id)}
                      >
                        {item.name}
                      </a>
                      <code>{item.legacy || "标识待定"}</code>
                      <span className="table-kind">{item.kind}</span>
                    </td>
                    <td>
                      <span className="stage-cell">{item.stage}</span>
                      <small>{item.version}</small>
                    </td>
                    <td>
                      <LinkedText
                        text={item.note || "用途待补充"}
                        version={item.version}
                        exclude={item.id}
                      />
                    </td>
                    <td>
                      <LinkedText
                        text={item.acquisition}
                        version={item.version}
                        exclude={item.id}
                      />
                    </td>
                  </tr>
                  {open === item.id && (
                    <tr className="expanded-item">
                      <td colSpan={5}>
                        <div className="inline-detail">
                          <QuickInfo item={item} />
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="atlas-layout">
          <div>
            <div className="atlas-hint">悬停 / 键盘聚焦查看 · 点击固定说明</div>
            <div className="sprite-atlas">
              {list.map((item) => (
                <button
                  key={item.id}
                  className={current?.id === item.id ? "selected" : ""}
                  aria-label={`${item.name} · ${item.stage}`}
                  aria-pressed={pinned && current?.id === item.id}
                  onMouseEnter={() => {
                    if (!pinned) setPreview(item);
                  }}
                  onFocus={() => {
                    if (!pinned) setPreview(item);
                  }}
                  onClick={() => {
                    setPreview(item);
                    setPinned(true);
                  }}
                >
                  <ItemVisual item={item} />
                </button>
              ))}
            </div>
          </div>
          {current && (
            <aside className="atlas-inspector">
              <div className="inspector-status">
                <span>{pinned ? "说明已固定" : "快速查看"}</span>
                <button
                  onClick={() => setPinned((v) => !v)}
                  aria-pressed={pinned}
                >
                  <Pin size={13} />
                  {pinned ? "取消固定" : "固定"}
                </button>
              </div>
              <QuickInfo item={current} />
            </aside>
          )}
        </div>
      )}
      {!list.length && (
        <div className="empty-state">
          没有匹配的物品。试着换个关键词或分类。
        </div>
      )}
    </>
  );
}

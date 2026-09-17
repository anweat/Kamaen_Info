import { useState } from "react";
import { ArrowLeft, ArrowRight, ArrowUpRight, Search } from "lucide-react";
import {
  data,
  href,
  itemById,
  itemName,
  textureFor,
  type Item,
  type Recipe,
} from "../data";
import ItemVisual from "./ItemVisual";
import BlockPreview from "./BlockPreview";
import ItemBrowser from "./ItemBrowser";
export function ItemCard({ item }: { item: Item }) {
  return (
    <a className="item-card" href={href("items", item.id)}>
      <div className="item-card-top">
        <ItemVisual item={item} />
        <span className="tiny-code">{item.stage}</span>
      </div>
      <strong>{item.name}</strong>
      <span>{item.kind}</span>
      <div className="item-card-bottom">
        <span className="status-tag">{item.version} 工作稿</span>
        <ArrowUpRight size={15} />
      </div>
    </a>
  );
}
export function RecipeCard({
  recipe,
  full = false,
}: {
  recipe: Recipe;
  full?: boolean;
}) {
  const entries = (values: Record<string, number>) =>
    Object.entries(values).map(([id, count]) => (
      <a className="ingredient" key={id} href={href("items", "r4:" + id)}>
        {itemById("r4:" + id) && <ItemVisual item={itemById("r4:" + id)!} />}
        <span>{itemName(id)}</span>
        <b>×{count}</b>
      </a>
    ));
  return (
    <article className="recipe-card">
      <div className="section-label">
        <a href={href("recipes", recipe.id)}>
          {Object.keys(recipe.outputs).map(itemName).join(" / ")}
        </a>
        <span>R4 候选</span>
      </div>
      <div className="recipe-flow">
        <div>{entries(recipe.inputs)}</div>
        <div className="recipe-station">
          <ArrowRight size={24} />
          <strong>{data.stations[recipe.station]?.name}</strong>
          <small>
            {recipe.seconds} s · {recipe.energy} E
          </small>
        </div>
        <div>{entries(recipe.outputs)}</div>
      </div>
      {full && (
        <>
          <div className="recipe-meta">
            <b>不消耗工装：</b>
            {recipe.tools.length
              ? recipe.tools.map(itemName).join("、")
              : "无登记工装"}
            <br />
            <b>研究条件：</b>
            {recipe.evidence.length
              ? recipe.evidence
                  .map((e) => data.evidence[e]?.experiment || e)
                  .join("；")
              : "无额外登记条件"}
          </div>
          <p className="muted small">
            候选名义成功配方；不表示 E1 新前期成本，也不代表游戏配方已实现。
          </p>
        </>
      )}
    </article>
  );
}
export function Items({ id }: { id?: string }) {
  if (id) {
    const item = itemById(id);
    if (!item)
      return (
        <p>
          未找到条目。<a href={href("items")}>返回图鉴</a>
        </p>
      );
    const recipes =
      item.version === "R4"
        ? data.recipes.filter((r) => r.outputs[item.legacy])
        : [];
    const uses =
      item.version === "R4"
        ? data.recipes.filter(
            (r) => r.inputs[item.legacy] || r.tools.includes(item.legacy),
          )
        : [];
    const related = data.items.filter(
      (i) => i.id !== item.id && i.name === item.name,
    );
    return (
      <>
        <a className="back-link" href={href("items")}>
          <ArrowLeft size={15} /> 物品与方块
        </a>
        <div className="detail-hero">
          <ItemVisual item={item} large />
          <div>
            <div className="eyebrow">
              {item.version} / {item.stage} / {item.kind}
            </div>
            <h1>{item.name}</h1>
            <code>{item.legacy || item.id}</code>
            <p className="muted">
              {textureFor(item)
                ? "已有资源用于预填充展示，尚未核定与设计条目的对应。"
                : "概念图标示例 · 专属材质待补充"}
            </p>
          </div>
        </div>
        <div className="detail-columns">
          <article className="reading-card">
            <h2>用途与设计说明</h2>
            <p>{item.note || "用途说明待补充，可先在研究记录中关联此条目。"}</p>
            <h3>如何取得</h3>
            <p>{item.acquisition}</p>
            <h3>需要记录的状态</h3>
            <p>{item.state || "母批、加工与测试状态将在后续讨论中补齐。"}</p>
            <a href={href("docs", item.source)}>
              阅读来源文档 <ArrowUpRight size={14} />
            </a>
          </article>
          <aside className="margin-note">
            {(/生产工位|设备/.test(item.kind) || /塔|机柜/.test(item.name)) && (
              <BlockPreview item={item} />
            )}
            <span className="eyebrow">DESIGN NOTE</span>
            <h3>先留下问题，再补齐答案。</h3>
            <p>这是一份持续生长的设计条目，名称不代表已注册的物品或方块。</p>
            <a href={href("notes", "new~item~" + item.id)}>
              为这个条目写记录 <ArrowRight size={14} />
            </a>
            {related.length > 0 && (
              <>
                <h3>另一版同名条目</h3>
                {related.map((i) => (
                  <a key={i.id} href={href("items", i.id)}>
                    {i.version} · {i.name}
                  </a>
                ))}
                <small>仅按同名关联，不自动合并两版语义。</small>
              </>
            )}
          </aside>
        </div>
        {recipes.length > 0 && (
          <>
            <h2>获得它的配方</h2>
            {recipes.map((r) => (
              <RecipeCard key={r.id} recipe={r} full />
            ))}
          </>
        )}
        {uses.length > 0 && (
          <>
            <h2>接下来用在哪里</h2>
            {uses.map((r) => (
              <RecipeCard key={r.id} recipe={r} />
            ))}
          </>
        )}
      </>
    );
  }
  return <ItemBrowser />;
}
export function Recipes({ id }: { id?: string }) {
  const [query, setQuery] = useState("");
  const [station, setStation] = useState("all");
  const list = data.recipes.filter(
    (r) =>
      (!id || r.id === id) &&
      (station === "all" || r.station === station) &&
      `${r.id} ${Object.keys(r.inputs).map(itemName)} ${Object.keys(r.outputs).map(itemName)}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  return (
    <>
      <div className="eyebrow">02 / PROCESS & CONNECTIONS</div>
      <h1>配方与路线</h1>
      <p className="lead">材料怎样变成器件，器件又怎样改变下一次实验。</p>
      <div className="notice">
        R4 候选配方示例 · 早期条目尚未纳入 E1
        新工装与供电平衡。当前不是最终合成表。
      </div>
      <div className="route-strip">
        原料 <ArrowRight /> 晶体实验 <ArrowRight /> 封装与计算 <ArrowRight />{" "}
        测量与模型 <ArrowRight /> 回到生产
      </div>
      {id ? (
        <a className="back-link" href={href("recipes")}>
          <ArrowLeft size={14} /> 全部配方
        </a>
      ) : (
        <div className="filter-bar">
          <label className="search-field">
            <Search size={17} />
            <input
              aria-label="搜索配方"
              placeholder="按原料、产物或配方 ID 搜索…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </label>
          <select
            aria-label="配方工位"
            value={station}
            onChange={(e) => setStation(e.target.value)}
          >
            <option value="all">全部工位</option>
            {Object.entries(data.stations).map(([id, s]) => (
              <option value={id} key={id}>
                {s.name}
              </option>
            ))}
          </select>
          <span>{list.length} 条</span>
        </div>
      )}
      {list.slice(0, id ? 1 : 40).map((r) => (
        <RecipeCard recipe={r} key={r.id} full />
      ))}
      {list.length > 40 && (
        <p className="muted">显示前40条。通过产物或工位筛选继续查阅。</p>
      )}
      {list.length === 0 && <p className="empty-state">没有匹配的配方。</p>}
    </>
  );
}

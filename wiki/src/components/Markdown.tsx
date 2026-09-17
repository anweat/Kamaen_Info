import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { data, href } from "../data";
import { ItemMention } from "./ItemBrowser";
export default function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href: target, children }) => {
            if (!target) return <span>{children}</span>;
            if (/^https?:/.test(target))
              return (
                <a href={target} target="_blank" rel="noreferrer">
                  {children} ↗
                </a>
              );
            if (target.startsWith("#/items/"))
              return <ItemMention id={decodeURIComponent(target.slice(8))} />;
            if (target.startsWith("#/")) return <a href={target}>{children}</a>;
            const file = decodeURIComponent(
              target.split("#")[0].split("/").pop() || "",
            );
            if (data.docs.some((d) => d.id === file))
              return <a href={href("docs", file)}>{children}</a>;
            return (
              <span
                title={`原文引用：${target}，尚未导入网页`}
                className="source-unavailable"
              >
                {children} <small>〔原文引用〕</small>
              </span>
            );
          },
          pre: ({ children }) => <pre tabIndex={0}>{children}</pre>,
          table: ({ children }) => (
            <div className="table-scroll">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}

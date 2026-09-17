import { useEffect, useState } from "react";
import {
  ArrowUpRight,
  RefreshCw,
  FolderOpen,
  ExternalLink,
  Terminal,
} from "lucide-react";
import "./development.css";
type Tool = {
  id: string;
  title: string;
  description: string;
  available: boolean;
  target: string | null;
  kind: string;
  executable: string | null;
};
type Workbench = {
  root: string;
  minecraft: string;
  neoForge: string;
  java: number;
  javaAvailable: boolean;
  javaHome: string;
  tools: Tool[];
  reference: {
    repository: string;
    commit: string;
    neoForge: string;
    role: string;
  };
};
export default function Development() {
  const [data, setData] = useState<Workbench | null>(null),
    [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [busy, setBusy] = useState("");
  async function refresh() {
    setError("");
    try {
      const response = await fetch("/api/workbench");
      if (
        !response.ok ||
        !response.headers.get("content-type")?.includes("application/json")
      )
        throw Error(
          "请通过本地 npm run dev 启动，静态预览不提供桌面工具入口。",
        );
      setData(await response.json());
    } catch (e) {
      setError((e as Error).message);
    }
  }
  useEffect(() => {
    void refresh();
  }, []);
  async function open(tool: Tool) {
    setBusy(tool.id);
    setNotice("");
    try {
      const response = await fetch(`/api/workbench/launch/${tool.id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
      const result = await response.json();
      if (!response.ok) throw Error(result.error);
      setNotice(result.message);
    } catch (e) {
      setNotice((e as Error).message);
    } finally {
      setBusy("");
    }
  }
  return (
    <section className="development-page">
      <header className="development-heading">
        <div>
          <p className="eyebrow">DEVELOPMENT / 从档案进入制作</p>
          <h1>开发工作台</h1>
          <p>
            在这里进入工程、模型与资源文件，让每一条想法逐步成为游戏中的内容。
          </p>
        </div>
        <button onClick={refresh} aria-label="刷新开发工具状态">
          <RefreshCw size={16} />
        </button>
      </header>
      {error && (
        <p role="alert" className="workbench-notice">
          {error}
        </p>
      )}
      {data && (
        <>
          <div className="development-version">
            <span>
              MINECRAFT <b>{data.minecraft}</b>
            </span>
            <span>
              NEOFORGE <b>{data.neoForge}</b>
            </span>
            <span>
              JAVA <b>{data.java}</b>
              <small>
                {data.javaAvailable ? "本机 JDK 已配置" : "需要配置 JDK"}
              </small>
            </span>
          </div>
          <div className="development-origin">
            <span>当前开发工程</span>
            <code>{data.root}</code>
            <small>沿用现有 Java / Gradle 工程，按流程逐项开发。</small>
          </div>
          <div className="development-tools">
            {data.tools.map((tool) => (
              <article key={tool.id}>
                <div className="tool-top">
                  <span>
                    {tool.kind === "folder" ? (
                      <FolderOpen size={20} />
                    ) : (
                      <ExternalLink size={20} />
                    )}
                  </span>
                  <small data-ready={tool.available}>
                    {tool.available ? "已就绪" : "未配置"}
                  </small>
                </div>
                <h2>{tool.title}</h2>
                <p>{tool.description}</p>
                <button
                  disabled={!tool.available || !!busy}
                  onClick={() => open(tool)}
                >
                  {busy === tool.id
                    ? "正在打开…"
                    : tool.kind === "folder"
                      ? "打开目录"
                      : "打开工具"}
                  <ArrowUpRight size={15} />
                </button>
                <details>
                  <summary>文件位置</summary>
                  <code>
                    {tool.target || tool.executable || "tooling/local.json"}
                  </code>
                </details>
              </article>
            ))}
          </div>
          <p className="workbench-notice" role="status">
            {notice ||
              "工具在桌面打开；资源保存在当前工程，Wiki 负责说明与关联。"}
          </p>
          <section className="development-pipeline">
            <h2>一次完整的制作流程</h2>
            <ol>
              <li>
                <b>01 / 定义</b>
                <span>明确用途、注册 ID、交互和最小验收条件。</span>
              </li>
              <li>
                <b>02 / 绘制</b>
                <span>
                  Blockbench 使用 Java Block/Item；源文件保存到 art/models。
                </span>
              </li>
              <li>
                <b>03 / 导出</b>
                <span>
                  PNG → textures；模型 JSON → models；补充 blockstates
                  与语言文件。
                </span>
              </li>
              <li>
                <b>04 / 实现</b>
                <span>接入 Java 注册、交互和数据组件，用开发客户端验证。</span>
              </li>
              <li>
                <b>05 / 记录</b>
                <span>
                  将实际注册 ID、贴图和验证结果关联回 Wiki 实体与发展地图。
                </span>
              </li>
            </ol>
          </section>
          <section className="development-commands">
            <h2>
              <Terminal size={18} /> 工程命令
            </h2>
            <p>在工程根目录运行；脚本只为当前进程选用 JDK 21。</p>
            {[
              ["环境检查", "doctor"],
              ["构建 Mod", "build"],
              ["启动客户端", "client"],
              ["生成数据", "data"],
            ].map(([label, action]) => (
              <div key={action}>
                <span>{label}</span>
                <code>
                  powershell -ExecutionPolicy Bypass -File .\tooling\dev.ps1{" "}
                  {action}
                </code>
              </div>
            ))}
          </section>
          <div className="development-reference">
            <h2>官方基底参考</h2>
            <p>
              已固定上游提交 <code>{data.reference.commit.slice(0, 12)}</code>
              ，模板使用 NeoForge {data.reference.neoForge}。
              {data.reference.role}。
            </p>
            <a
              href={data.reference.repository}
              target="_blank"
              rel="noreferrer"
            >
              NeoForge 1.21.1 MDK <ArrowUpRight size={14} />
            </a>
            <a
              href="https://github.com/tryashtar/nbt-studio/releases/tag/v1.15.3"
              target="_blank"
              rel="noreferrer"
            >
              NBT Studio 1.15.3 <ArrowUpRight size={14} />
            </a>
            <p>
              格式与制作约定见工程中的 tooling/README.md。NBT
              样本仅用于验证工具链，尚未定义游戏数据契约。
            </p>
          </div>
        </>
      )}
    </section>
  );
}

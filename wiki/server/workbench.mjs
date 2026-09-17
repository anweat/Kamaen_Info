import { readFile, access } from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const exists = async (p) => {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
};
export function launchProcess(executable, args, cwd, environment = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(executable, args, {
      cwd,
      detached: true,
      stdio: "ignore",
      shell: false,
      // These allowlisted GUI apps are opened by an explicit user action.
      windowsHide: false,
      env: { ...process.env, ...environment },
    });
    child.once("error", reject);
    child.once("spawn", () => {
      child.unref();
      resolve();
    });
  });
}
export function workbenchMiddleware(root, { launch = launchProcess } = {}) {
  const localPath = (value) =>
    path.isAbsolute(value) ? value : path.resolve(root, value);
  const targetPath = (value) => {
    const target = path.resolve(root, value),
      relative = path.relative(root, target);
    if (
      relative === ".." ||
      relative.startsWith(`..${path.sep}`) ||
      path.isAbsolute(relative)
    )
      throw Error("入口目标必须位于当前工程");
    return target;
  };
  return async (req, res) => {
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", "no-store");
    const reply = (status, body) => {
      res.statusCode = status;
      res.end(JSON.stringify(body));
    };
    if (!/^127\.0\.0\.1:\d+$/.test(req.headers.host || ""))
      return reply(403, { error: "开发工具仅限本地访问" });
    try {
      const config = JSON.parse(
        await readFile(path.join(root, "tooling/workbench.json"), "utf8"),
      );
      const properties = await readFile(
        path.join(root, "gradle.properties"),
        "utf8",
      );
      const property = (name) =>
        properties.match(new RegExp(`^${name}=(.+)$`, "m"))?.[1].trim();
      let local = { executables: {} };
      try {
        local = JSON.parse(
          await readFile(path.join(root, "tooling/local.json"), "utf8"),
        );
      } catch {}
      const tools = await Promise.all(
        config.tools.map(async (tool) => {
          const target = tool.target ? targetPath(tool.target) : null;
          const configured = local.executables?.[tool.executable];
          const executable =
            tool.kind === "folder"
              ? path.join(process.env.WINDIR || "C:\\Windows", "explorer.exe")
              : configured
                ? localPath(configured)
                : null;
          return {
            ...tool,
            target,
            executable,
            available:
              !!executable &&
              (await exists(executable)) &&
              (!target || (await exists(target))),
          };
        }),
      );
      if (req.method === "GET" && (req.url === "/" || req.url === ""))
        return reply(200, {
          ...config,
          minecraft: property("minecraft_version"),
          neoForge: property("neo_version"),
          root,
          local: true,
          tools,
          javaHome: local.javaHome || null,
          javaAvailable:
            !!local.javaHome &&
            (await exists(
              path.join(localPath(local.javaHome), "bin/java.exe"),
            )),
        });
      if (req.method !== "POST")
        return reply(405, { error: "Method not allowed" });
      if (
        req.headers.origin !== `http://${req.headers.host}` ||
        req.headers["content-type"] !== "application/json"
      )
        return reply(403, { error: "仅接受本地页面的同源工具操作" });
      const match = /^\/launch\/([a-z0-9-]+)$/.exec(req.url || "");
      const tool = match && tools.find((t) => t.id === match[1]);
      if (!tool) return reply(404, { error: "未知工具入口" });
      let body = "";
      for await (const chunk of req) {
        body += chunk;
        if (Buffer.byteLength(body) > 1024)
          return reply(413, { error: "请求过大" });
      }
      if (body.trim() && body.trim() !== "{}")
        return reply(400, { error: "入口不接受任意路径或命令参数" });
      if (!tool.available)
        return reply(409, {
          error: "工具或目标文件不存在，请检查 tooling/local.json",
        });
      const environment =
        tool.id === "nbt" && local.nbtRollForward
          ? { DOTNET_ROLL_FORWARD: local.nbtRollForward }
          : {};
      await launch(
        tool.executable,
        tool.target ? [tool.target] : [],
        root,
        environment,
      );
      reply(200, { message: `已向 ${tool.title} 发送打开请求。`, id: tool.id });
    } catch (error) {
      reply(500, { error: error.message || "开发入口不可用" });
    }
  };
}
export function workbenchPlugin(root) {
  return {
    name: "local-development-workbench",
    configureServer(server) {
      server.middlewares.use("/api/workbench", workbenchMiddleware(root));
    },
  };
}

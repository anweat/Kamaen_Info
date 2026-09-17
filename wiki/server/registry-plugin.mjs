import { readFile, writeFile, rename } from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";
import { compileRegistry, validateMap } from "./registry.mjs";
export const fingerprint = (raw) =>
  createHash("sha256").update(raw).digest("hex");
export function registryPlugin(root) {
  const virtual = "\0virtual:kamaen-registry";
  let registry;
  let queue = Promise.resolve();
  const compile = async () => (registry = await compileRegistry(root));
  return {
    name: "kamaen-file-registry",
    async buildStart() {
      await compile();
    },
    resolveId(id) {
      if (id === "virtual:kamaen-registry") return virtual;
    },
    async load(id) {
      if (id === virtual)
        return `export default ${JSON.stringify(await compile())}`;
    },
    configureServer(server) {
      server.watcher.add(root);
      let timer;
      server.watcher.on("all", (event, file) => {
        const rel = path.relative(root, file).replaceAll("\\", "/");
        if (
          rel.startsWith("../") ||
          !/^(entities|scenes|models|renderers|descriptions|assets|maps)\//.test(
            rel,
          ) ||
          file.endsWith(".tmp")
        )
          return;
        clearTimeout(timer);
        timer = setTimeout(async () => {
          try {
            await compile();
            const module = server.moduleGraph.getModuleById(virtual);
            if (module) server.moduleGraph.invalidateModule(module);
            // Maps have their own draft/conflict flow; saving a map must not remount the editor.
            if (
              !rel.startsWith("maps/") ||
              event === "add" ||
              event === "unlink"
            )
              server.ws.send({ type: "full-reload" });
          } catch (e) {
            server.ws.send({
              type: "error",
              err: {
                message: e.message,
                stack: e.stack,
                plugin: "kamaen-file-registry",
              },
            });
          }
        }, 180);
      });
      server.middlewares.use("/api/maps", async (req, res) => {
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.setHeader("Cache-Control", "no-store");
        const reply = (status, value) => {
          res.statusCode = status;
          res.end(JSON.stringify(value));
        };
        try {
          let id;
          try {
            id = decodeURIComponent((req.url || "").split("?")[0].slice(1));
          } catch {
            return reply(400, { error: "地图 ID 无效" });
          }
          const currentRegistry = await compile();
          const map = currentRegistry.maps.find((m) => m.id === id);
          if (!map) return reply(404, { error: "找不到已注册地图" });
          const file = path.join(root, map.file);
          const read = async () => {
            const raw = await readFile(file, "utf8");
            return { document: JSON.parse(raw), etag: fingerprint(raw) };
          };
          if (req.method === "GET") return reply(200, await read());
          if (req.method !== "PUT")
            return reply(405, { error: "Method not allowed" });
          if (
            !/^127\.0\.0\.1:\d+$/.test(req.headers.host || "") ||
            req.headers.origin !== `http://${req.headers.host}`
          )
            return reply(403, { error: "只接受本地同源保存" });
          let body = "";
          for await (const chunk of req) {
            body += chunk;
            if (Buffer.byteLength(body) > 2000000)
              return reply(413, { error: "地图超过 2 MB" });
          }
          let incoming;
          try {
            incoming = JSON.parse(body);
          } catch {
            return reply(400, { error: "JSON 格式错误" });
          }
          if (incoming.id !== id || !validateMap(incoming, currentRegistry))
            return reply(400, { error: "地图字段或引用无效" });
          queue = queue
            .catch(() => {})
            .then(async () => {
              const current = await read();
              if (req.headers["if-match"] !== current.etag)
                return reply(409, {
                  error: "地图文件已更改。请导出草稿，再重新读取文件后合并。",
                });
              const next = {
                ...incoming,
                revision: current.document.revision + 1,
              };
              const raw = JSON.stringify(next, null, 2) + "\n";
              await writeFile(file + ".tmp", raw);
              await rename(file + ".tmp", file);
              reply(200, { document: next, etag: fingerprint(raw) });
            });
          await queue;
        } catch (e) {
          if (!res.writableEnded) reply(500, { error: e.message });
        }
      });
    },
  };
}

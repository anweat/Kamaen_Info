import { readFile, writeFile, rename } from "node:fs/promises";

export function validateNotes(value) {
  return (
    value &&
    Number.isSafeInteger(value.revision) &&
    value.revision >= 0 &&
    Array.isArray(value.notes) &&
    value.notes.length <= 1000 &&
    new Set(value.notes.map((n) => n?.id)).size === value.notes.length &&
    value.notes.every(
      (n) =>
        n &&
        ["id", "title", "body", "stage", "status", "updatedAt"].every(
          (k) => typeof n[k] === "string",
        ) &&
        n.id.length > 0 &&
        n.id.length < 100 &&
        n.title.trim().length > 0 &&
        n.title.length <= 200 &&
        n.body.length <= 100000 &&
        ["想法", "讨论中", "待验证", "已记录"].includes(n.status) &&
        Array.isArray(n.refs) &&
        n.refs.length <= 50 &&
        n.refs.every((r) => typeof r === "string" && r.length < 300),
    )
  );
}

export function notesPlugin(
  file,
  { route = "/api/notes", validate = validateNotes } = {},
) {
  let queue = Promise.resolve();
  return {
    name: "local-research-notes",
    configureServer(server) {
      server.middlewares.use(route, async (req, res) => {
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.setHeader("Cache-Control", "no-store");
        const reply = (status, value) => {
          res.statusCode = status;
          res.end(JSON.stringify(value));
        };
        if (req.method === "GET") {
          try {
            reply(200, JSON.parse(await readFile(file, "utf8")));
          } catch {
            reply(500, { error: "读取研究记录失败。" });
          }
          return;
        }
        if (req.method !== "PUT")
          return reply(405, { error: "Method not allowed" });
        if (
          !req.headers.origin ||
          req.headers.origin !== `http://${req.headers.host}` ||
          !/^127\.0\.0\.1:\d+$/.test(req.headers.host || "")
        )
          return reply(403, { error: "只接受本地网页的同源保存。" });
        let body = "";
        try {
          for await (const chunk of req) {
            body += chunk;
            if (Buffer.byteLength(body) > 2000000)
              return reply(413, { error: "记录超过 2 MB，请拆分。" });
          }
          const incoming = JSON.parse(body);
          if (!validate(incoming))
            return reply(400, { error: "记录格式无效。" });
          queue = queue
            .catch(() => {})
            .then(async () => {
              const current = JSON.parse(await readFile(file, "utf8"));
              if (incoming.revision !== current.revision)
                return reply(409, {
                  error:
                    "记录已在另一页面更新。请先导出当前草稿，再刷新并合并。",
                });
              const next = { ...incoming, revision: current.revision + 1 };
              await writeFile(
                `${file}.tmp`,
                JSON.stringify(next, null, 2) + "\n",
                "utf8",
              );
              await rename(`${file}.tmp`, file);
              reply(200, next);
            });
          await queue;
        } catch {
          if (!res.writableEnded)
            reply(500, { error: "保存失败，当前编辑内容仍保留，请导出备份。" });
        }
      });
    },
  };
}

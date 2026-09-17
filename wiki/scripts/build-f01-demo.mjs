import { readFile, writeFile } from "node:fs/promises";
const root = new URL("../content/renderers/", import.meta.url);
const engine = (await readFile(new URL("f01-separation.mjs", root), "utf8"))
  .replace(/^export \{[^\n]+\};\r?$/m, "");
if (/\bexport\b/.test(engine)) throw Error("F01 engine must remain self-contained");
const template = await readFile(new URL("f01-separation.template.html", root), "utf8");
await writeFile(new URL("f01-separation.html", root),
  template.replace("/*__F01_ENGINE__*/", () => engine), "utf8");

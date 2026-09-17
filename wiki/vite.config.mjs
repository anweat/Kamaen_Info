import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { notesPlugin } from "./server/notes.mjs";
import { validateCanvas } from "./server/canvas.mjs";
import { registryPlugin } from "./server/registry-plugin.mjs";
import { workbenchPlugin } from "./server/workbench.mjs";
export default defineConfig({
  base: "./",
  plugins: [
    react(),
    workbenchPlugin(fileURLToPath(new URL("..", import.meta.url))),
    registryPlugin(fileURLToPath(new URL("./content", import.meta.url))),
    notesPlugin(
      fileURLToPath(new URL("./content/notes.json", import.meta.url)),
    ),
    notesPlugin(
      fileURLToPath(new URL("./content/canvas.json", import.meta.url)),
      { route: "/api/canvas", validate: validateCanvas },
    ),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/three/")) return "three";
          if (
            /node_modules\/(react-markdown|remark|rehype|micromark|mdast|hast|unist|unified)/.test(
              id,
            )
          )
            return "markdown";
          if (id.includes("/generated/content.json")) return "content";
        },
      },
    },
  },
});

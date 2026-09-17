import { fileURLToPath } from "node:url";
import { compileRegistry } from "../server/registry.mjs";
const registry = await compileRegistry(
  fileURLToPath(new URL("../content/", import.meta.url)),
);
console.log(
  `Validated ${registry.entities.length} entities, ${registry.maps.length} maps, ${registry.scenes.length} scenes, ${registry.models.length} models, ${registry.renderers.length} custom renderers.`,
);

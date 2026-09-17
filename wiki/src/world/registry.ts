import registry from "virtual:kamaen-registry";
export default registry;
export const entityById = (id?: string) =>
  registry.entities.find((e) => e.id === id);
export const kindNames = {
  item: "物品",
  block: "方块",
  multiblock: "多方块",
  nbt: "NBT 标签",
  model: "模型",
};

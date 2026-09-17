import { textureFor, type Item } from "../data";
import PixelSprite from "./PixelSprite";
export default function ItemVisual({
  item,
  large = false,
}: {
  item: Item;
  large?: boolean;
}) {
  const texture = textureFor(item);
  return (
    <span
      className={`item-visual ${large ? "large" : ""} ${texture ? "textured" : ""}`}
    >
      {texture ? (
        <img
          src={`${import.meta.env.BASE_URL}textures/${texture}`}
          alt={`${item.name}，已有资源示意，非新增专属贴图`}
        />
      ) : (
        <PixelSprite item={item} />
      )}
    </span>
  );
}

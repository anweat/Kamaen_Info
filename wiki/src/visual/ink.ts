// Preserve authored hues while lifting dark annotations against the instrument surface.
export function displayInk(hex?: string): string | undefined {
  if (!hex || !/^#[\da-f]{6}$/i.test(hex)) return hex;
  const original = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
  const light = [217, 231, 237];
  let rgb = original;
  const linear = (n: number) => {
    const s = n / 255;
    return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  for (let t = 0; t <= 1; t += 0.025) {
    rgb = original.map((v, i) => Math.round(v + (light[i] - v) * t));
    if (
      rgb.reduce(
        (sum, v, i) => sum + linear(v) * [0.2126, 0.7152, 0.0722][i],
        0,
      ) >= 0.36
    )
      break;
  }
  return `rgb(${rgb.join(" ")})`;
}

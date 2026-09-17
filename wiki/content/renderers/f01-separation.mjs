// F01 UI study only: artificial mother batch; not a Minecraft process model.
const programs = {
  coarse: { title: "粗分流", finePass: 0.8, mixedPass: 0.15, water: 25 },
  wash: { title: "分级复洗", finePass: 0.9, mixedPass: 0.05, water: 37.5 },
};
const emptyBins = () => ({ powderFine: 0, powderMixed: 0, slagFine: 0, slagMixed: 0, water: 0 });
function createTrial(mode = "coarse", capacity = 50) {
  if (!Object.hasOwn(programs, mode) || ![25, 50, 100].includes(capacity))
    throw Error("Unknown demonstration setup");
  return { mode, capacity, step: 0, filter: false,
    remaining: { fine: 60, mixed: 40, water: 150 },
    bins: emptyBins(), collected: emptyBins(),
    message: "已放入测试母批与水。先安装滤框。" };
}
function toggleFilter(s) {
  return { ...s, filter: !s.filter, message: s.filter
    ? "滤框已取下，槽内余料保留；装回后可继续。" : "滤框已装好，可以推进一段。" };
}
function advance(s) {
  if (s.step >= 4) return { ...s, message: "这批已完成。收取产物，或重置试验比较另一种工况。" };
  if (!s.filter) return { ...s, message: "先安装滤框，原料仍留在槽内。" };
  const p = programs[s.mode];
  const portion = { powderFine: 15 * p.finePass, powderMixed: 10 * p.mixedPass,
    slagFine: 15 * (1 - p.finePass), slagMixed: 10 * (1 - p.mixedPass), water: p.water };
  if (s.bins.powderFine + s.bins.powderMixed + portion.powderFine + portion.powderMixed > s.capacity ||
      s.bins.slagFine + s.bins.slagMixed + portion.slagFine + portion.slagMixed > s.capacity)
    return { ...s, message: "收料盘空间不足。先收料；本段没有扣除原料。" };
  if (s.remaining.water < p.water)
    return { ...s, message: "可用水不足，原料保持原状。" };
  return { ...s, step: s.step + 1,
    remaining: { fine: s.remaining.fine - 15, mixed: s.remaining.mixed - 10, water: s.remaining.water - p.water },
    bins: Object.fromEntries(Object.keys(portion).map(k => [k, s.bins[k] + portion[k]])),
    message: `第 ${s.step + 1} / 4 段已完成。${s.step === 3 ? "这批固料已全部分流，请收料。" : "可以继续，也可以先收料或取下滤框。"}` };
}
function collect(s) {
  return { ...s, bins: emptyBins(),
    collected: Object.fromEntries(Object.keys(s.bins).map(k => [k, s.collected[k] + s.bins[k]])),
    message: "盘内产物和回收液已移入已收取记录。收料不会复制实物。" };
}
function balance(s) {
  return {
    fine: s.remaining.fine + s.bins.powderFine + s.bins.slagFine + s.collected.powderFine + s.collected.slagFine,
    mixed: s.remaining.mixed + s.bins.powderMixed + s.bins.slagMixed + s.collected.powderMixed + s.collected.slagMixed,
    water: s.remaining.water + s.bins.water + s.collected.water,
  };
}
export { programs, createTrial, toggleFilter, advance, collect, balance };

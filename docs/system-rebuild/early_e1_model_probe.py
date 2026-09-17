"""Finite author examples for E1; no game, real material, or blast simulation."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKS: list[dict] = []


def check(name: str, condition: bool) -> None:
    CHECKS.append({"name": name, "passed": bool(condition)})
    if not condition:
        raise AssertionError(name)


def near(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def write_structure(a: list[float], dose: list[float], fraction: float) -> list[float]:
    """Diagonal restriction of the E1 tensor example, in crystal coordinates."""
    if any(v < 0 for v in dose) or not 0 <= fraction <= 1:
        raise ValueError("outside this compressive writing template")
    total = sum(dose)
    if total == 0:
        return a.copy()
    return [(1 - fraction) * v + fraction * d / total for v, d in zip(a, dose)]


def peak(a: list[float], axis: int) -> float:
    # One mechanical test domain: f/f_ref. Fixed temperature and relaxed stress.
    return 1.0 + 0.5 * (a[axis] - 1 / 3)


def separate(a: list[float], axis: int, path: float, source_frequency: float) -> dict:
    # Calibrated candidate for ONE feed and apparatus; not a universal quality stat.
    if not 0 <= path <= 1:
        raise ValueError("invalid energy path fraction")
    f_peak = peak(a, axis)
    overlap = max(0.0, 1.0 - abs(source_frequency - f_peak) / 0.05)
    working_fraction = path * overlap
    feed = {"copper": 10.0, "iron": 10.0, "other": 80.0}
    base = {"copper": 0.40, "iron": 0.10, "other": 0.05}
    change = {"copper": 0.30, "iron": -0.04, "other": -0.03}
    target = {k: m * (base[k] + change[k] * working_fraction) for k, m in feed.items()}
    residue = {k: m - target[k] for k, m in feed.items()}
    return {"axis": axis, "path": path, "source_frequency": source_frequency,
            "peak": f_peak, "working_fraction": working_fraction,
            "feed": feed, "target": target, "mixed_residue": residue,
            "copper_recovery": target["copper"] / feed["copper"],
            "copper_purity": target["copper"] / sum(target.values())}


def line_fit(rows: list[dict]) -> dict:
    if not 2 <= len(rows) <= 16:
        raise ValueError("sample capacity/count")
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("duplicate observation")
    if any(not r["valid"] for r in rows):
        raise ValueError("invalid observation")
    if len({r["condition"] for r in rows}) != 1:
        raise ValueError("different conditions require separate analysis")
    x_mean = sum(r["x"] for r in rows) / len(rows)
    y_mean = sum(r["y"] for r in rows) / len(rows)
    variance = sum((r["x"] - x_mean) ** 2 for r in rows)
    if variance <= 1e-12:
        raise ValueError("no identifiable slope")
    slope = sum((r["x"] - x_mean) * (r["y"] - y_mean) for r in rows) / variance
    return {"a": y_mean - slope * x_mean, "b": slope, "count": len(rows),
            "x_window": [min(r["x"] for r in rows), max(r["x"] for r in rows)],
            "condition": rows[0]["condition"]}


def rejects(rows: list[dict]) -> bool:
    try:
        line_fit(rows)
    except ValueError:
        return True
    return False


def response(load: float, temperature: float = 20.0) -> float:
    # Authored higher-order curve underlying an early first-order player model.
    return 1 + 0.4 * load + 0.08 * load ** 2 + 0.02 * (temperature - 20)


def main() -> None:
    # Directional deposition and net push are different quantities.
    a0 = [1 / 3] * 3
    incoming = 80.0
    absorbed, other_output, loss = 48.0, 16.0, 16.0
    net_impulse = 5.0 - 5.0  # Independently specified impulse units, not energy.
    dose = [absorbed, 0.0, 0.0]  # Unit sample volume; +/- x both add to xx.
    a1 = write_structure(a0, dose, 0.3)
    check("相向冲量为零但定向沉积非零", near(net_impulse, 0) and sum(dose) > 0)
    check("该路径例子的输入能量闭合", near(incoming, absorbed + other_output + loss))
    check("写入后的结构非负且迹为1", all(v >= 0 for v in a1) and near(sum(a1), 1))
    check("零剂量与可恢复加载不改写结构",
          write_structure(a0, [0, 0, 0], 0.3) == a0 and write_structure(a0, dose, 0) == a0)
    relaxed_stress = [v * math.exp(-math.log(2)) for v in dose]
    annealed_a = a1.copy()  # Structure recovery window has not been entered.
    check("残余应力松弛可与持久结构分开", near(relaxed_stress[0], 24) and annealed_a == a1)

    production = {
        "before_writing": separate(a0, 0, 1.0, 1.1),
        "written_aligned": separate(a1, 0, 1.0, 1.1),
        "same_crystal_rotated": separate(a1, 1, 1.0, 1.1),
        "disconnected_excitation": separate(a1, 0, 0.0, 1.1),
        "retuned_before_writing": separate(a0, 0, 1.0, 1.0),
    }
    before, after = production["before_writing"], production["written_aligned"]
    check("安装方向改变同一晶体的机械峰位", near(peak(a1, 0), 1.1) and near(peak(a1, 1), 0.95))
    check("该分离工况的铜回收从4增至7", near(before["target"]["copper"], 4) and near(after["target"]["copper"], 7))
    check("各工况逐组分守恒且各流非负", all(
        near(r["target"][k] + r["mixed_residue"][k], m)
        and r["target"][k] >= 0 and r["mixed_residue"][k] >= 0
        for r in production.values() for k, m in r["feed"].items()))
    check("旋转或断开路径会失去这个工况的改善", all(
        near(production[k]["target"]["copper"], 4)
        for k in ("same_crystal_rotated", "disconnected_excitation")))
    check("可调源也能匹配旧晶体且不强制材料升级", near(
        production["retuned_before_writing"]["target"]["copper"], 7))

    rows = [{"id": f"training-{i}-{j}", "x": x, "y": response(x) + noise,
             "condition": "fixed_batch_axis_T20", "valid": True}
            for i, x in enumerate([0.0, 0.5, 1.0, 1.5])
            for j, noise in enumerate([-0.01, 0.0, 0.01])]
    fit = line_fit(rows)
    comparisons = []
    for name, x, temperature in [("留样", 1.25, 20), ("超出载荷窗", 2.5, 20), ("升温后", 1.25, 30)]:
        predicted = fit["a"] + fit["b"] * x
        observed = response(x, temperature)
        comparisons.append({"name": name, "load": x, "temperature": temperature,
                            "prediction": predicted, "observation": observed,
                            "absolute_error": abs(observed - predicted),
                            "inside_validated_conditions": 0 <= x <= 1.5 and temperature == 20})
    check("12条训练记录得到实际最小二乘结果", fit["count"] == 12 and near(fit["a"], 0.98) and near(fit["b"], 0.52))
    check("独立留样在窗内误差较小", near(comparisons[0]["absolute_error"], 0.005))
    check("外推与改变温度会暴露模型边界", all(
        r["absolute_error"] > 0.15 and not r["inside_validated_conditions"] for r in comparisons[1:]))
    check("相同x不能伪造可识别斜率", rejects([{**r, "x": 1} for r in rows]))
    check("重复无效混条件及超容量记录被拒绝", all([
        rejects(rows + [rows[0]]), rejects([{**rows[0], "valid": False}, *rows[1:]]),
        rejects([{**rows[0], "condition": "T30"}, *rows[1:]]),
        rejects([{**rows[i % 12], "id": f"large-{i}"} for i in range(17)]),
    ]))
    power = {"crushing": 0.20, "mixing": 0.15, "heating": 0.30, "measurement_aux": 0.05}
    check("候选首套产线保留30%发电余量", near(sum(power.values()), 0.70))
    results = {"scope": "E1有限作者算例，非完整材料、能量动力学、随机实验或游戏验证",
               "structure": {"initial": a0, "written": a1, "dose": dose,
                             "net_impulse": net_impulse, "relaxed_stress": relaxed_stress},
               "energy": {"incoming": incoming, "absorbed": absorbed, "other_output": other_output, "loss": loss},
               "production": production, "training_records": rows, "fit": fit,
               "comparisons": comparisons, "power_relative_G": power, "checks": CHECKS}
    (ROOT / "early-e1-model-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# E1：晶体—生产反馈与早期拟合的有限例子", "",
             "由 `early_e1_model_probe.py` 生成，2026-09-07。入口：[前期玩法](EARLY_E1_GAMEPLAY.md)、[模型定义](EARLY_E1_CRYSTAL_MODEL.md)。",
             "", f"**{len(CHECKS)}项指定检查通过。** 所有材料系数、曲线和扰动均为作者给定的游戏候选；没有完成游戏运行、完整物理、空间路径或随机分布验证。",
             "", "E1.1已修订力学合成，见[有序过程模型](EARLY_E11_MECHANICAL_SYNTHESIS.md)。下列D及压缩为正的残余应力更新是历史局部算例，不能用于判定完整合成；分离与拟合例继续作为有限候选。",
             "", "## 1. 两侧加工不会因净推动为零而失效", "",
             "两侧等量相向冲量各为5个示例冲量单位；两源总能量80，晶体吸收48、其他输出16、损耗16。冲量与能量分别指定，不把二者数值等同。单位体积内定向剂量为diag(48,0,0)。",
             "", "有效写入份额0.3使A从diag(1/3,1/3,1/3)变为diag(0.5333,0.2333,0.2333)。结构仍非负且迹为1；后续只进入应力松弛窗时，残余应力可减半而A保留。未模拟强度上限、裂纹传播和完整反射寻路。",
             "", "## 2. 同一晶体的结构和安装回到分离生产", "",
             "本例限定同一泥浆、温度、机械激励域和已供能的普通分离设备。机械频率以该域f_ref归一化，不与光频谱共轴。改变A后，同一晶体两方向峰位分别为1.10和0.95。",
             "", "`f_peak = 1 + 0.5*(uᵀAu - 1/3)`；`w = η_path * max(0, 1-|f_drive-f_peak|/0.05)`。本例w只是此分离工况中新增激励作用的份额，零时回到普通分离基线。",
             "", "目标口分配概率为铜`0.40+0.30w`、铁`0.10-0.04w`、其他`0.05-0.03w`；其余各组分仍在混合余料中。输入始终为铜10、铁10、其他80。",
             "", "| 工况 | 铜进入目标口 | 铜回收率 | 目标口铜纯度 | 混合余料总量 |",
             "| --- | --- | --- | --- | --- |"]
    names = ["写入前，源1.10", "写入后对正，源1.10", "同一晶体转向，源1.10", "激励路径断开", "保留旧晶体，源改为1.00"]
    for name, row in zip(names, production.values()):
        lines.append(f"| {name} | {row['target']['copper']:.2f} | {row['copper_recovery']:.1%} | {row['copper_purity']:.1%} | {sum(row['mixed_residue'].values()):.2f} |")
    lines += ["", "铜从4增至7来自余料回收，未增加输入铜总量。安装朝向或实际传递路径会改变结果；增加发电机不能替代缺失的耦合。",
              "", "这里也暴露一个应保留的开放解：若现有驱动可改频，旧晶体也能匹配这个单工况。不能仅凭此算例宣称特化晶体全面胜出。材料改造的价值要由驱动可达窗、多腔共用源、选择性/温漂或空间等实际任务体现；这些额外限制尚未在本例求解。",
              "", "## 3. 玩家做出一个有用、但并不全对的小模型", "",
              "作者曲线为`y=1+0.4s+0.08s²+0.02(T-20)`。玩家只得到T=20、s为0/0.5/1/1.5的12条记录，每条件三条指定扰动-0.01/0/+0.01；这些是确定性算例，不是随机采样有效性证明。拟合不访问作者系数，也不使用留样记录。",
              "", f"固定统计台得到`y_hat={fit['a']:.2f}+{fit['b']:.2f}s`。拟合样本与完整值见[原始算例结果](early-e1-model-results.json)。",
              "", "| 检验 | 载荷s | 温度 | 模型预测 | 新读数 | 绝对误差 |",
              "| --- | --- | --- | --- | --- | --- |"]
    for row in comparisons:
        lines.append(f"| {row['name']} | {row['load']} | {row['temperature']} | {row['prediction']:.3f} | {row['observation']:.3f} | {row['absolute_error']:.3f} |")
    lines += ["", "第一次留样说明模型在已试局部有用；更大载荷或更热工况提示需要新变量/高阶项。不能因一次留样通过就把模型标为全域正确。相同x、重复记录、无效读数、混工况与超16条容量均有独立拒绝路径。",
              "", "## 4. 早期供电与检查范围", "",
              "破碎0.20G、搅拌0.15G、加热0.30G、测量辅助0.05G，共0.70G，保留0.30G。这里只核对候选持续功率比例，未计算燃料平衡、启动峰值、线路瞬态、热平衡或批次调度。",
              "", "| 指定检查 | 结果 |", "| --- | --- |"]
    lines += [f"| {c['name']} | 通过 |" for c in CHECKS]
    (ROOT / "EARLY_E1_MODEL_EXAMPLES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(CHECKS), "passed": all(c["passed"] for c in CHECKS),
                      "fit": fit, "copper_purity_after": after["copper_purity"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

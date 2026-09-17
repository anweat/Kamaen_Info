"""Authored boundary-history examples; not a source, shock or thermal solver."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_case(name: str, right_start: float = 2, amplitude: float = 2,
             hot_start: float = 0, seeded: bool = True,
             regions: dict[str, float] | None = None, dt: float = 0.25) -> dict:
    regions = regions or {"sample": 1.0}
    progress = {region: 0.0 for region in regions}
    damage = {region: 0.0 for region in regions}
    longest = {region: 0.0 for region in regions}
    streak = {region: 0.0 for region in regions}
    work = net_impulse = unsigned_impulse = 0.0
    records = []
    for step in range(round(12 / dt)):
        t = (step + 0.5) * dt
        left = amplitude if 2 <= t < 6 else 0.0
        right = amplitude if right_start <= t < right_start + 4 else 0.0
        # Signed opposing forces and prescribed compatible sign velocities.
        forces = [left, -right]
        velocities = [0.5 if left else 0.0, -0.5 if right else 0.0]
        power = sum(f * v for f, v in zip(forces, velocities))
        work += power * dt
        net_impulse += sum(forces) * dt
        unsigned_impulse += sum(abs(f) for f in forces) * dt
        temperature = 1.0 if t >= hot_start else 0.5
        local = {}
        for region, response_fraction in regions.items():
            # A deliberately restricted opposed-loading proxy, NOT pressure/stress.
            opposed = min(left, right) * response_fraction
            peak_load = max(left, right) * response_fraction
            active = seeded and 1.5 <= opposed <= 3.0 and 0.8 <= temperature <= 1.2
            if active:
                progress[region] = 1 - (1 - progress[region]) * math.exp(-0.5 * dt)
                streak[region] += dt
                longest[region] = max(longest[region], streak[region])
            else:
                streak[region] = 0.0
            damage[region] += max(0, peak_load - 3.0) * dt
            local[region] = {"opposed_load_proxy": opposed, "active": active,
                             "phase_fraction": progress[region], "damage_proxy": damage[region]}
        records.append({"t": t, "forces": forces, "power": power,
                        "temperature_proxy": temperature, "regions": local})
    # Equal regional masses for this finite example only.
    mean_fraction = sum(progress.values()) / len(progress)
    return {"name": name, "mechanical_work_input": work, "net_impulse": net_impulse,
            "unsigned_impulse": unsigned_impulse, "phase_fraction": progress,
            "longest_valid_hold": longest, "damage_proxy": damage,
            "mass": {"input": 100.0, "changed_phase": 100 * mean_fraction,
                     "unchanged_phase": 100 * (1 - mean_fraction)},
            "meets_this_spec": all(v >= 0.8 for v in progress.values()) and all(v == 0 for v in damage.values()),
            "records": records}


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def main() -> None:
    cases = [run_case("同时到达"), run_case("先后到达", right_start=6),
             run_case("仅重叠一半", right_start=4), run_case("先冲击后加热", hot_start=7),
             run_case("峰值过高", amplitude=4), run_case("缺少晶种接触", seeded=False),
             run_case("表层可达但内部不足", regions={"left_surface": 0.8, "core": 0.6, "right_surface": 0.8})]
    aligned, delayed, partial, late, overload, no_seed, spatial = cases
    checks = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    check("时间平移不改变本例两源总功与整段冲量", all(
        close(c["mechanical_work_input"], 8) and close(c["net_impulse"], 0)
        and close(c["unsigned_impulse"], 16) for c in [aligned, delayed, partial]))
    check("相同总量能产生不同转变历程", aligned["meets_this_spec"] and delayed["phase_fraction"]["sample"] == 0)
    check("四单位保持得到指定动力学解", close(aligned["phase_fraction"]["sample"], 1 - math.exp(-2)))
    check("缩短共同作用时间留下半成品", close(partial["phase_fraction"]["sample"], 1 - math.exp(-1)) and not partial["meets_this_spec"])
    check("热与加载的顺序影响材料变化", late["phase_fraction"]["sample"] == 0 and not late["meets_this_spec"])
    check("增加输入功不能替代有效加工窗口", overload["mechanical_work_input"] > aligned["mechanical_work_input"] and overload["damage_proxy"]["sample"] > 0 and not overload["meets_this_spec"])
    check("晶种诱导要求实际接触条件", no_seed["phase_fraction"]["sample"] == 0)
    check("表层合格不能代表内部合格", spatial["phase_fraction"]["left_surface"] >= 0.8 and spatial["phase_fraction"]["core"] == 0 and not spatial["meets_this_spec"])
    check("同组成相态变化保留全部质量", all(
        close(c["mass"]["changed_phase"] + c["mass"]["unchanged_phase"], c["mass"]["input"])
        and 0 <= c["mass"]["changed_phase"] <= 100 for c in cases))
    finer = run_case("较细时间步", dt=0.125)
    check("本例边界对齐矩形历程在细分时间步下结果一致", close(
        finer["phase_fraction"]["sample"], aligned["phase_fraction"]["sample"]))
    payload = {"scope": "E1.1人为给定边界与温程的有限功能例子；未求解源可达性、局部应力、热平衡或裂纹",
               "time_and_load_units": "dimensionless game example",
               "cases": cases, "checks": checks}
    (ROOT / "early-e11-process-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# E1.1：力学工艺的有限过程例子", "",
             "由 `early_e11_process_probe.py` 生成，2026-09-07。配套：[力学合成](EARLY_E11_MECHANICAL_SYNTHESIS.md)、[工艺制造](EARLY_E11_PROCESS_MANUFACTURING.md)。",
             "", f"**{len(checks)}项指定检查通过。** 本例验证过程依赖，未完成动力学、热力学或游戏实现。",
             "", "## 1. 给定条件与算例边界", "",
             "时间、温度、载荷均为无量纲游戏量。人为给定两面力与接触速度：每面载荷大小2、持续4、速度大小0.5，向内为各自运动方向；按ΣF·v积分，总机械功8，整段净冲量0，逐源冲量大小之和16。没有验证此边界历程在某个真实源/工件上是否可实现。",
             "", "两面同时作用的代理量为`min(F_left,F_right)*region_response`，不是局部真实压力或应力。已预压实且有晶种接触时，代理量在[1.5,3]、温度代理量在[0.8,1.2]才令`dξ/dt=0.5*(1-ξ)`；其他时间本例令ξ不变。过高载荷另累积损伤代理量。",
             "", "这些阈值、矩形包络、区域响应与动力学均为指定反例，不能当成最终配方或现实工艺参数；本例也没有求解相变能、逆转变、实际冷却与卸载。",
             "", "## 2. 同总量，结果仍不同", "",
             "| 操作 | 总机械功 | 共同有效保持 | 晶态比例 | 当前规格 |",
             "| --- | --- | --- | --- | --- |"]
    for c in cases:
        holds = ", ".join(f"{k}:{v:.2f}" for k, v in c["longest_valid_hold"].items())
        phase = ", ".join(f"{k}:{v:.1%}" for k, v in c["phase_fraction"].items())
        lines.append(f"| {c['name']} | {c['mechanical_work_input']:.2f} | {holds} | {phase} | {'达到' if c['meets_this_spec'] else '未达到'} |")
    lines += ["", "当前示例规格要求每个区域晶态比例≥80%且无该损伤代理量。玩家看到的报告仍取决于已有仪器；表中全区域值是作者视图。",
              "", "第一组和第二组具有相同总功、源方向和整段冲量，却有不同的有效过程。第三组留下可继续处理的部分转变料。第四组表明在冲击结束后才升温，不能补回曾经缺失的共同窗口。第五组说明更高输入可能进入另一个损伤过程。",
              "", "质量示例取100单位同组成基材（含实际投入晶种），只在相态间重新分配；不是产生100单位新材料。区域按等质量处理，仅供检查“表层成功不能代替内部成功”。",
              "", "## 3. 检查与尚未证明的事情", "", "| 检查 | 结果 |", "| --- | --- |"]
    lines += [f"| {c['name']} | 通过 |" for c in checks]
    lines += ["", "半时间步一致只针对边界落在网格上的这些矩形例子，不是任意脉冲或刚性材料积分器的收敛证明。输入功已积分，但能量最终进入何处没有求解，不能据此宣称完整能量账通过。下一步空间原型仍需把实际源、接触、时延、局部状态和收料连接起来。",
              "", "完整离散记录：[算例数据](early-e11-process-results.json)。"]
    (ROOT / "EARLY_E11_PROCESS_EXAMPLES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(checks), "passed": True, "aligned_phase": aligned["phase_fraction"],
                      "delayed_phase": delayed["phase_fraction"], "input_work": aligned["mechanical_work_input"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

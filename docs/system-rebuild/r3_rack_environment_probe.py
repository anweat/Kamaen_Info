"""Finite authored design examples. No Minecraft, CFD, FEM or EM solver."""
from __future__ import annotations

import cmath
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def thermal_step(temperatures, capacities, powers, edges, boundaries, dt):
    """Explicit conservative step; boundaries are fixed temperature reservoirs."""
    n = len(temperatures)
    if not (n == len(capacities) == len(powers)) or dt <= 0:
        raise ValueError("invalid thermal dimensions/time")
    if not all(math.isfinite(v) for v in (*temperatures, *capacities, *powers, dt)):
        raise ValueError("nonfinite thermal input")
    if any(c <= 0 for c in capacities) or any(p < 0 for p in powers):
        raise ValueError("capacity must be positive; this probe accepts heat sources only")
    flux = list(powers)
    outgoing = [0.0] * n
    seen = set()
    for i, j, conductance in edges:
        if not (0 <= i < n and 0 <= j < n and i != j):
            raise ValueError("invalid thermal edge")
        key = tuple(sorted((i, j)))
        if key in seen:
            raise ValueError("parallel contacts must first form one equivalent edge")
        seen.add(key)
        if not math.isfinite(conductance) or conductance < 0:
            raise ValueError("invalid conductance")
        q = conductance * (temperatures[i] - temperatures[j])
        flux[i] -= q
        flux[j] += q
        outgoing[i] += conductance
        outgoing[j] += conductance
    boundary_out = 0.0
    for i, ambient, conductance in boundaries:
        if not 0 <= i < n or not math.isfinite(ambient) or not math.isfinite(conductance) or conductance < 0:
            raise ValueError("invalid thermal boundary")
        q = conductance * (temperatures[i] - ambient)
        boundary_out += q
        flux[i] -= q
        outgoing[i] += conductance
    if any(dt * g / c > 0.95 for g, c in zip(outgoing, capacities)):
        raise ValueError("explicit step exceeds this probe's monotone step bound")
    after = [t + dt * q / c for t, q, c in zip(temperatures, flux, capacities)]
    delta_energy = sum(c * (b - a) for c, a, b in zip(capacities, temperatures, after))
    return after, delta_energy, dt * (sum(powers) - boundary_out)


def lump_temperature(initial, ambient, power, conductance, capacity, elapsed):
    if conductance <= 0 or capacity <= 0 or elapsed < 0:
        raise ValueError("invalid lump model")
    equilibrium = ambient + power / conductance
    return equilibrium + (initial - equilibrium) * math.exp(-elapsed * conductance / capacity)


def recirculation(supply, heat, flow_capacity, fraction):
    """Steady, single air-stream example with a maintained external supply."""
    if not (0 <= fraction < 1) or flow_capacity <= 0 or heat < 0:
        raise ValueError("no valid maintained-flow steady boundary")
    rise = heat / flow_capacity
    inlet = supply + fraction * rise / (1 - fraction)
    return inlet, inlet + rise


def transmissibility(ratio, damping):
    if ratio < 0 or damping <= 0:
        raise ValueError("invalid base-excited oscillator")
    term = (2 * damping * ratio) ** 2
    return math.sqrt((1 + term) / ((1 - ratio**2)**2 + term))


def band_power(paths):
    """Same source: combine complex RMS response. Distinct sources: independent."""
    grouped = {}
    for source, response in paths:
        grouped[source] = grouped.get(source, 0j) + response
    return sum(abs(response)**2 for response in grouped.values())


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm(v):
    return math.sqrt(sum(x*x for x in v))


def unit(v):
    length = norm(v)
    if length <= 1e-12:
        raise ValueError("zero vector")
    return tuple(x / length for x in v)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def port_directions_match(points, source_normal, target_normal):
    outgoing = unit(subtract(points[1], points[0]))
    arriving = unit(subtract(points[-1], points[-2]))
    return (dot(outgoing, unit(source_normal)) > 1 - 1e-9
            and dot(arriving, unit(target_normal)) < -1 + 1e-9)


def rounded_length(points, radius, minimum_radius, lead_a=0.0, lead_b=0.0):
    """Line/fillet length, checking local fit only; no obstacle/collision solver."""
    if len(points) < 2 or radius < minimum_radius or minimum_radius <= 0 or min(lead_a, lead_b) < 0:
        raise ValueError("invalid route/radius")
    directions = [unit(subtract(b, a)) for a, b in zip(points, points[1:])]
    lengths = [norm(subtract(b, a)) for a, b in zip(points, points[1:])]
    trims = [0.0] * len(points)
    angles = []
    for i, (a, b) in enumerate(zip(directions, directions[1:]), start=1):
        angle = math.acos(max(-1.0, min(1.0, dot(a, b))))
        if angle >= math.pi - 1e-9:
            raise ValueError("foldback needs an explicit valid loop")
        trims[i] = radius * math.tan(angle / 2)
        angles.append(angle)
    for i, length in enumerate(lengths):
        remaining = length - trims[i] - trims[i+1]
        lead = (lead_a if i == 0 else 0) + (lead_b if i == len(lengths)-1 else 0)
        if remaining + 1e-9 < lead:
            raise ValueError("fillet/connector straight section does not fit")
    return sum(lengths) - 2 * sum(trims) + radius * sum(angles)


def main():
    checks = []

    def check(name, outcome):
        checks.append({"name": name, "passed": bool(outcome)})

    def rejected(name, function):
        try:
            function()
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    temps, de, expected = thermal_step([60, 20], [100, 200], [0, 0], [(0, 1, 2)], [], 1)
    check("封闭两节点内部导热不产生或消灭热量", math.isclose(de, 0, abs_tol=1e-10))
    check("热接触同时使热端降温、冷端升温", temps[0] < 60 and temps[1] > 20)
    _, de, expected = thermal_step([60, 20], [100, 200], [120, 0], [(0, 1, 2)], [(1, 10, 1)], 1)
    check("储热变化等于输入热量减外部净输出", math.isclose(de, expected, abs_tol=1e-10))
    isolated, _, _ = thermal_step([20], [100], [100], [], [], 1)
    check("无冷却时热量留在局部储热中", math.isclose(isolated[0], 21))
    rejected("步长过大被拒绝，不能伪装成物理失稳", lambda: thermal_step([60, 20], [1, 1], [0, 0], [(0, 1, 2)], [], 1))
    rejected("负导热不作为被动接触", lambda: thermal_step([60, 20], [100, 200], [0, 0], [(0, 1, -2)], [], 1))
    t60 = lump_temperature(20, 20, 120, 6, 600, 60)
    t300 = lump_temperature(20, 20, 120, 6, 600, 300)
    after_off = lump_temperature(t300, 20, 0, 6, 600, 60)
    check("同一负载下短时温度与持续温度不同", 20 < t60 < t300 < 40)
    check("停机60模型秒后仍有余热", 20 < after_off < t300)
    check("增大热容延缓升温但不改变此模型的稳态", lump_temperature(20, 20, 120, 6, 1200, 60) < t60)
    a = recirculation(20, 120, 12, 0.25)
    b = recirculation(20, 120, 18, 0.05)
    check("回流入口满足新风与回流混合条件", math.isclose(a[0], .75*20 + .25*a[1]))
    check("流体温升携带指定热量", math.isclose(12 * (a[1] - a[0]), 120))
    check("指定改善边界下入口出口温度均降低", b[0] < a[0] and b[1] < a[1])
    rejected("零流量不能调用有流稳态式", lambda: recirculation(20, 120, 0, .25))
    rejected("完全回流不能伪装成有新风稳态", lambda: recirculation(20, 120, 12, 1))

    resonant = transmissibility(1, .1)
    high = transmissibility(3, .1)
    check("低频极限为跟随基座", math.isclose(transmissibility(0, .1), 1))
    check("指定隔振系统在共振处放大", resonant > 5)
    check("同一系统在频率比3处隔离", high < .15)
    check("增加阻尼降低该系统的共振峰", transmissibility(1, .3) < resonant)
    shared = band_power([("fan", .6), ("fan", .4)])
    independent = band_power([("fan_a", .6), ("fan_b", .4)])
    check("同源同相路径先合成再求功率", math.isclose(shared, 1))
    check("明确独立源按功率相加", math.isclose(independent, .52))
    check("同源等幅反相路径可相消", math.isclose(band_power([("source", 1), ("source", cmath.exp(1j*math.pi))]), 0, abs_tol=1e-20))
    check("共架同位移两点的相对运动为零", norm(subtract((.1, .2, .3), (.1, .2, .3))) == 0)

    points = [(0, 0, 0), (4, 0, 0), (4, 4, 0)]
    length = rounded_length(points, .5, .4, .75, .75)
    check("圆弧线路长度包含裁去直段和实际弧长", math.isclose(length, 7 + math.pi/4))
    check("端口出入方向一致", port_directions_match(points, (1, 0, 0), (0, -1, 0)))
    check("目标法线反向错误会被发现", not port_directions_match(points, (1, 0, 0), (0, 1, 0)))
    rotated = [(-y, x, z) for x, y, z in points]
    check("整体刚体旋转不改变内部线长", math.isclose(rounded_length(rotated, .5, .4, .75, .75), length))
    rejected("低于线材最小半径的拐弯被拒绝", lambda: rounded_length(points, .2, .4))
    rejected("两相邻弯曲挤占同一短段被拒绝", lambda: rounded_length([(0, 0, 0), (2, 0, 0), (2, .5, 0), (4, .5, 0)], .5, .4))
    rejected("端口直出空间不足被拒绝", lambda: rounded_length(points, .5, .4, 3.75, .75))

    results = {
        "scope": "独立、作者指定的有限模型示例；非真实参数拟合、非联合机柜仿真、非游戏验证",
        "thermal": {"isolated_pair_after": temps, "lump_at_60": t60, "lump_at_300": t300, "after_60_off": after_off,
                    "before_route_change_air": a, "after_route_change_air": b},
        "vibration": {"at_resonance": resonant, "at_ratio_3": high, "same_source_power": shared, "independent_source_power": independent},
        "cable": {"points": points, "radius": .5, "minimum_radius": .4, "length": length},
        "checks": checks,
    }
    failed = [row["name"] for row in checks if not row["passed"]]
    if failed:
        raise AssertionError(failed)
    (ROOT / "r3-rack-environment-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# R3.3局部验算：热、振动源与线缆路径", "",
        "日期：2026-09-07。由[r3_rack_environment_probe.py](r3_rack_environment_probe.py)生成；[机器可读结果](r3-rack-environment-results.json)。", "",
        "配套[机柜环境与工程玩法](COMPUTING_R3_RACK_ENVIRONMENT_AND_ENGINEERING.md)。下列三个工况彼此独立，所有参数均由作者指定，没有拟合真实硬件。", "",
        "## 热模型", "",
        "封闭两节点：C分别为100、200 J/K，初始60、20°C，G=2 W/K，步长1模型秒，结果为59.2、20.4°C；内部交换不改变总储热。", "",
        "单节点热阶跃：C=600 J/K，G=6 W/K，持续耗散120 W，固定外部20°C，时间常数100模型秒，稳态40°C。该例直接计算解析解；一般热网络例子采用有步长约束的显式更新。", "",
        "| 工况 | 结果 |", "| --- | --- |",
        f"| 开机60模型秒 | {t60:.4f}°C |", f"| 开机300模型秒 | {t300:.4f}°C |", f"| 此后停机60模型秒 | {after_off:.4f}°C |", "",
        "空气回流是另一个独立稳态例子：固定新风20°C、气流接收120 W，T_out=T_in+P/H，T_in=(1-r)T_supply+rT_out。H和r是给定边界，未由柜体几何求解。", "",
        "| 给定风路 | 入口 | 出口 |", "| --- | --- | --- |",
        f"| H=12 W/K，r=0.25 | {a[0]:.4f}°C | {a[1]:.4f}°C |",
        f"| H=18 W/K，r=0.05 | {b[0]:.4f}°C | {b[1]:.4f}°C |", "",
        "## 振动与相关源", "",
        f"单自由度基座激励，阻尼比0.1：频率比1的幅度传递率为{resonant:.6f}；频率比3为{high:.6f}。这不是任意支撑串接后的乘积模型。", "",
        f"同一频段的复RMS响应：同源同相0.6、0.4先相加，得到功率{shared:.2f}；明确独立的两个源得到功率{independent:.2f}。只有此处明确独立的源才做平方和。", "",
        "共架相对位移为零的例子不证明晶振对整体加速度不敏感。未求多自由度装配、机械回路或真实冲击。", "",
        "## 线缆几何", "",
        "用三个点(0,0,0)→(4,0,0)→(4,4,0)，拐角圆弧半径0.5、最小允许0.4；两端各要求0.75直出长度。单位为本例局部长度单位，不等于世界方块或毫米。", "",
        f"原折线长8；裁去两段各0.5，加入四分之一圆弧，实际曲线长7+π/4={length:.6f}。校验与未来渲染应使用同一曲线定义。", "",
        "本例只检查圆弧局部容纳、最小半径、直出段、端口切向和旋转不变性；没有实现曲线生成渲染、障碍碰撞、线束容量或寻路。", "",
        "## 检查结果", "", f"共{len(checks)}项指定检查通过。", "",
        "| 检查 | 结果 |", "| --- | --- |",
    ]
    lines.extend(f"| {row['name']} | 通过 |" for row in checks)
    lines.extend(["", "## 范围", "",
                  "没有EM/供电求解、流路压力/阻力求解、完整机柜耦合或区块存储实现；也没有验证真实物理精度、任务吞吐和任意设计可用。这里用于排除明显计量错误并帮助讨论玩法。", ""])
    (ROOT / "R3_RACK_ENVIRONMENT_PROBE.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"passed": len(checks), "failed": 0, "written": ["R3_RACK_ENVIRONMENT_PROBE.md", "r3-rack-environment-results.json"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

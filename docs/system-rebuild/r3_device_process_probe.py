"""R3.1 candidate game rules: bounded deterministic design probes, not device physics.

Checks causal process order, tuning limits, packaging, and explicit gate/state roles.
No game runtime, real manufacturing, random batches, or learned model is exercised.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import itertools
import json
import math

BASE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Slice:
    dopant_fraction: float = 0.1
    residual_stress: float = 0.0
    scatter_defect: float = 0.4


def write_stress(s, amount):
    return replace(s, residual_stress=s.residual_stress + amount,
                   scatter_defect=s.scatter_defect + 0.1 * abs(amount))


def anneal(s, dose=math.log(4)):
    # This fixture stays in a registered moderate window. No overheat branch here.
    return replace(s, residual_stress=s.residual_stress * math.exp(-dose),
                   scatter_defect=s.scatter_defect * math.exp(-dose))


def center(s, live_tuning=0.0, package_stress=0.0):
    return 0.42 + 0.2 * s.dopant_fraction + 0.1 * (
        s.residual_stress + package_stress + live_tuning)


def transmission(s, f, live_tuning=0.0, package_stress=0.0):
    # One passive, intensity-only, fitted port model; not a general complex spectrum.
    d = s.scatter_defect
    floor = 0.02 + 0.03 * d
    peak = 0.9 * math.exp(-d)
    width = 0.025 + 0.06 * d
    assert 0 <= floor < peak <= 1 and width > 0
    fc = center(s, live_tuning, package_stress)
    return floor + (peak - floor) / (1 + ((f - fc) / width) ** 2)


def characterize(label, s, package_stress=0.0):
    # Author-side best possible trim, not an omniscient in-game auto-calibration.
    trim = max(-0.15, min(0.15, (0.5 - center(s, 0, package_stress)) / 0.1))
    fc = center(s, trim, package_stress)
    wanted = transmission(s, 0.5, trim, package_stress)
    unwanted = transmission(s, 0.65, trim, package_stress)
    return dict(name=label, state=s.__dict__, package_stress=package_stress,
                best_trim=trim, center=fc, center_error=abs(fc - 0.5),
                wanted_transmission=wanted, unwanted_transmission=unwanted,
                passes=abs(fc - 0.5) <= 0.005 + 1e-12 and wanted >= 0.70
                and unwanted <= 0.10)


def powered_gate(a, b, threshold, enabled=True):
    # a,b are normalized control signals, not unconstrained summed optical power.
    q = (a + b) / 2
    return int(q >= threshold) if enabled else None


def hold_trace(drives, supplies):
    state = None
    rows = []
    for step, (drive, powered) in enumerate(zip(drives, supplies), 1):
        if not powered:
            state = None  # this volatile teaching fixture loses validity in one step
        elif drive >= 0.70:
            state = 1
        elif drive <= 0.30:
            state = 0
        # Holding input in (0.30,0.70) preserves state, including unknown initial state.
        rows.append(dict(step=step, drive=drive, powered=powered, state=state))
    return rows


def feedback_step(state, drive, coupling):
    # Powered nonlinear response plus an actual one-step feedback path.
    # drive is a signed differential control value, not negative optical power.
    return 1 / (1 + math.exp(-8 * (drive + coupling * state - .4)))


def relax_feedback(start, coupling, steps=40):
    state = start
    for _ in range(steps):
        state = feedback_step(state, 0, coupling)
    return state


seed = Slice()
route_a = anneal(write_stress(seed, 0.6))
route_b = write_stress(anneal(seed), 0.6)
cases = [characterize('先写应力，再退火', route_a),
         characterize('先退火，再写应力', route_b),
         characterize('路线B＋高应力封装', route_b, -0.30),
         characterize('路线B＋缓冲封装', route_b, -0.05)]
truth = [dict(a=a, b=b, OR=powered_gate(a, b, .25),
              AND=powered_gate(a, b, .75)) for a, b in itertools.product((0, 1), repeat=2)]
memory = hold_trace([.5, .15, .85, .5, .5, .5, .5, .15],
                    [True, True, True, True, True, False, True, True])
eta, visibility = .8, .9
phase = [dict(phase_pi=p, out_a=eta * (1 + visibility * math.cos(p * math.pi)) / 2,
              out_b=eta * (1 - visibility * math.cos(p * math.pi)) / 2)
         for p in (0, .5, 1)]
feedback = [dict(coupling=kappa, from_low=relax_feedback(0, kappa),
                 from_high=relax_feedback(1, kappa)) for kappa in (.2, .8)]
written_high = relax_feedback(feedback_step(feedback[1]['from_low'], .5, .8), .8)
written_low = relax_feedback(feedback_step(feedback[1]['from_high'], -.5, .8), .8)
checks = {
    '工序顺序同时改变残余应力与散射缺陷': route_a.residual_stress < route_b.residual_stress
        and route_a.scatter_defect < route_b.scatter_defect,
    '最佳可逆调谐仍不能挽救路线A': not cases[0]['passes'] and cases[0]['best_trim'] == .15,
    '路线B在此任务工作窗内合格': cases[1]['passes'],
    '封装变化能使原合格结构失效': not cases[2]['passes'],
    '缓冲封装配合范围内调谐恢复合格': cases[3]['passes'],
    '有限采样频带内被动传输不产生增益': all(0 <= transmission(s, f/100, u) <= 1
        for s in (route_a, route_b) for f in range(101) for u in (-.15, 0, .15)),
    '同一实际混合与门控结构实现OR及AND': all(
        x['OR'] == int(bool(x['a'] or x['b'])) and x['AND'] == x['a']*x['b'] for x in truth),
    '主动门缺供给时标无效': powered_gate(1, 1, .75, False) is None,
    '保持需显式写入与维持条件': [x['state'] for x in memory] == [None, 0, 1, 1, 1, None, None, 0],
    '两端干涉输出总和守住给定透过预算': all(
        math.isclose(x['out_a'] + x['out_b'], eta) for x in phase),
    '相同非线性件弱反馈不能维持两种可分状态': abs(
        feedback[0]['from_high'] - feedback[0]['from_low']) < 1e-6,
    '强反馈在本窗口可保持并显式改写两种状态': feedback[1]['from_low'] < .2
        and feedback[1]['from_high'] > .8 and written_low < .2 and written_high > .8,
}
assert all(checks.values()), checks
result = dict(version='R3.1-candidate-probe', warning=__doc__.strip(),
              process_cases=cases, gate_truth_table=truth, hold_trace=memory,
              phase_outputs=phase, nonlinear_feedback=feedback,
              feedback_write_result=dict(write_high=written_high, reset_low=written_low), checks=checks)
(BASE/'r3-device-process-results.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# R3.1：性质、功能与制程的有限数值推演', '',
         '本文件由[r3_device_process_probe.py](r3_device_process_probe.py)生成，配套[R3.1讨论稿](COMPUTING_R3_PROPERTIES_AND_PROCESS.md)。', '',
         '所有系数、归一化频率、调谐范围和判据均为作者设定的游戏候选。没有模拟真实器件、随机批次、训练或Minecraft运行。仅检查指定例子的因果、状态与预算是否自洽。', '',
         '## 1. 工序顺序与封装', '',
         '同一初始片：掺杂留存比例0.1、残余应力0、散射缺陷0.4。先后改变“写应力0.6”和“退火至原值的1/4”。允许可逆调谐u在[-0.15,0.15]。', '',
         '验收：目标中心0.50±0.005；目标频带透过≥0.70；干扰频带0.65透过≤0.10。下表调谐取作者侧最佳值，用来判断能力上限；游戏中的校准需要实际测量。', '',
         '| 路线 | 残余应力 | 散射缺陷 | 封装加载 | 最佳调谐u | 中心 | 目标透过 | 干扰透过 | 合格 |',
         '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
for c in cases:
    lines.append(f"| {c['name']} | {c['state']['residual_stress']:.3f} | {c['state']['scatter_defect']:.3f} | {c['package_stress']:.3f} | {c['best_trim']:.3f} | {c['center']:.3f} | {c['wanted_transmission']:.3f} | {c['unwanted_transmission']:.3f} | {'是' if c['passes'] else '否'} |")
lines += ['', '路线A的散射缺陷更低，却因中心偏离且调谐范围不足而不适合本任务；它仍可用于其他频段。路线B初版合格，换封装后可能失效。结果不能推广为“永远先退火再应力”，只适用于本模型的材料、结构与工艺窗口。', '',
          '## 2. 功能需要明确结构与条件', '',
          '门控例子：归一化控制输入经实际混合结构q=(a+b)/2，再由有供给的阈值/恢复输出级处理。阈值0.25是OR，0.75是AND；调节范围必须由器件实测支持。', '',
          '| a | b | OR | AND |', '| --- | --- | --- | --- |']
for r in truth: lines.append(f"| {r['a']} | {r['b']} | {r['OR']} | {r['AND']} |")
lines += ['', '保持例子：上阈值0.70、下阈值0.30；中间维持输入0.50。未知初态保持未知，断供后恢复供给不会恢复丢失信息。这仅是单步失效的易失教学器件，不是所有存储器的统一寿命。', '',
          '| 步骤 | 驱动 | 供给 | 状态 |', '| --- | --- | --- | --- |']
for r in memory: lines.append(f"| {r['step']} | {r['drive']:.2f} | {'有' if r['powered'] else '无'} | {r['state'] if r['state'] is not None else '无效/未初始化'} |")
lines += ['', '干涉例子：同一来源的教学双路模板，η=0.8、V=0.9，两个输出总和为0.8；剩余0.2列为损耗。这里没有用相位变化凭空制造额外光功率。', '',
          '| 相位差/π | 输出A | 输出B |', '| --- | --- | --- |']
for r in phase: lines.append(f"| {r['phase_pi']:.1f} | {r['out_a']:.3f} | {r['out_b']:.3f} |")
lines += ['', '非线性与实际延迟反馈的补充例子：z[n+1]=sigmoid(8*(x[n]+κ*z[n]-0.4))。固定相同非线性件和偏置，只改变耦合κ；每一步代表声明的器件响应时间，有实际供给。x为写/复位的差分控制，保持时x=0。', '',
          '| 耦合κ | 从低态保持40步 | 从高态保持40步 |', '| --- | --- | --- |']
for r in feedback: lines.append(f"| {r['coupling']:.1f} | {r['from_low']:.4f} | {r['from_high']:.4f} |")
lines += ['', f'κ=0.8时，单步写入控制+0.5后保持得到{written_high:.4f}；单步复位控制-0.5后保持得到{written_low:.4f}。两条轨迹只是在指定条件下保持可分的数值证据，尚未分析随机扰动、参数漂移与所有初态。']
lines += ['', '## 3. 推演检查', '']
for name in checks: lines.append('- 通过：'+name+'。')
lines += ['', f'以上{len(checks)}项仅针对本脚本中的有限假设与例子。完整材料模型、噪声/批间统计、通用工艺曲线、任意电路和游戏实现均未验证。']
(BASE/'R3_DEVICE_PROCESS_PROBE.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(dict(checks_passed=len(checks), process_cases=[
    dict(name=c['name'], center=round(c['center'], 3), transmission=round(c['wanted_transmission'], 3),
         passes=c['passes']) for c in cases]), ensure_ascii=False))

"""Finite author-side counterexamples for L1; not a game or physics simulator."""
from pathlib import Path
import cmath
import json
import math

BASE = Path(__file__).resolve().parent
checks = []


def check(name, passed, evidence):
    checks.append((name, bool(passed), evidence))
    if not passed:
        raise AssertionError(name)


def close(a, b, tol=1e-10):
    return abs(a - b) <= tol


# Integrate actual synthetic samples, including interference in different bands.
angles = [2 * math.pi * k / 64 for k in range(64)]
trace = [0.03 * math.cos(t) + 0.04 * math.sin(t)
         + 0.2 * math.cos(3*t) + 0.1 for t in angles]


def demod(samples, ref_phase=0):
    x = 2 * sum(v * math.cos(t + ref_phase)
                for v, t in zip(samples, angles)) / len(angles)
    y = -2 * sum(v * math.sin(t + ref_phase)
                 for v, t in zip(samples, angles)) / len(angles)
    return complex(x, y)


h = demod(trace)
check('整周期例中分开指定离频成分',
      close(h.real, 0.03) and close(h.imag, -0.04) and close(abs(h), 0.05),
      f'X={h.real:.5f}, Y={h.imag:.5f}, magnitude={abs(h):.5f}')
rotated = demod(trace, math.pi/2)
check('参考转相不让本例振幅消失', close(abs(rotated), abs(h)),
      f'转相90度后幅值={abs(rotated):.5f}，单通道数值改变')
polluted = demod([v + 0.02 * math.cos(t) for v, t in zip(trace, angles)])
check('同频干扰不能由同步检波自动消除',
      close(polluted.real, 0.05) and abs(polluted) > abs(h),
      f'X={polluted.real:.5f}, magnitude={abs(polluted):.5f}')

# A finite damped response; the displayed phase is not a hidden material label.
response = [0.1 / complex(1-r*r, 2*0.1*r) for r in (0.5, 1, 2)]
check('有限单模响应具有幅值和相位变化',
      abs(response[1]) > max(abs(response[0]), abs(response[2]))
      and all(math.isfinite(v.real) and math.isfinite(v.imag) for v in response),
      '; '.join(f'f/f0={r}: abs={abs(v):.5f}, phase={math.degrees(cmath.phase(v)):.2f}deg'
                for r, v in zip((0.5, 1, 2), response)))

# A memoryless material can exhibit apparent hysteresis against plate setpoint.
def resistance(t_sample):
    return 2 + 0.04 * (t_sample - 290)


apparent = (resistance(295), resistance(285))
check('无记忆材料也能产生设定温度回线',
      close(apparent[0], 2.2) and close(apparent[1], 1.8),
      '冷板均290 K，样品295/285 K时为2.2/1.8 Ohm')
settled = [resistance(290 + sign * 5 * math.exp(-12/2)) for sign in (1, -1)]
check('热等待可使本例假回线收拢', abs(settled[0]-settled[1]) < 0.001,
      f'等待6个tau后：{settled[0]:.6f}/{settled[1]:.6f} Ohm')

r_sample, current, offset, r_lead = 2, 0.1, 0.03, 0.5
v_plus = current*r_sample + offset
v_minus = -current*r_sample + offset
r_four = (v_plus-v_minus)/(2*current)
r_two = (current*(r_sample+r_lead)+offset)/current
check('四端反向示例恢复样品电阻', close(r_four, r_sample),
      f'V+={v_plus:.2f}, V-={v_minus:.2f}, R={r_four:.2f} Ohm')
check('两线单向示例含接触和偏置误差', close(r_two, 2.8),
      f'两线单次测量得到{r_two:.2f} Ohm')
r_drift = (v_plus - (-current*r_sample + 0.04))/(2*current)
check('反向期间偏置变化仍污染结果', close(r_drift, 1.95),
      f'偏置0.03变0.04 V后R={r_drift:.2f} Ohm')

# Independently calibrate axis, then predict a held-out target line.
lab_lambda, lab_u = (4, 7), (4.28, 7.34)
a = (lab_u[1]-lab_u[0])/(lab_lambda[1]-lab_lambda[0])
b = lab_u[0] - a*lab_lambda[0]
rest = (4, 5, 6)
observed = (4.688, 5.810, 6.932)
naive_z = [u/lam-1 for u, lam in zip(observed, rest)]
corrected_z = [(u-b)/(a*lam)-1 for u, lam in zip(observed, rest)]
check('直接把读出刻度当波长给出冲突谱移',
      max(naive_z)-min(naive_z) > 0.01,
      'naive z=' + ', '.join(f'{v:.5f}' for v in naive_z))
check('独立谱轴校准后各线相容',
      close(a, 1.02) and close(b, 0.2) and all(close(v, 0.1) for v in corrected_z),
      f'a={a:.2f}, b={b:.2f}, z=' + ', '.join(f'{v:.5f}' for v in corrected_z))
fit_z = sum(corrected_z[:2])/2
predicted_last = a*(1+fit_z)*rest[-1]+b
check('前两条目标线的解释预测第三条', close(predicted_last, observed[-1]),
      f'留出峰心预测={predicted_last:.5f}, 观察={observed[-1]:.5f}')
check('没有独立参考时倍率与谱移退化',
      all(close(1.1*lam, 1.0*(1+0.1)*lam) for lam in rest),
      '(a=1.1,z=0)与(a=1,z=0.1)，b=0时所有目标线都相同')

# Calibrated two-band model: test rank and a new band, not only training residual.
obs = (5, 7)
f_component = obs[1]-obs[0]
b_component = obs[0]-f_component
check('指定可辨识双模板能解开两个分量',
      close(b_component, 3) and close(f_component, 2),
      f'B={b_component:.1f}, F={f_component:.1f}')
check('新波段提供未用约束', close(b_component+3*f_component, 9),
      '第三波段模板(1,3)，预测读数9；实际游戏仍须再观测')
degenerate_a = (3+2, 3+2)
degenerate_b = (4+1, 4+1)
check('共线模板不能靠重复观测唯一分解', degenerate_a == degenerate_b,
      '(B,F)=(3,2)与(4,1)在两个(1,1)模板上完全相同')

sigma_cal, sigma_rand, count = 0.02, 0.1, 100
common_uncertainty = math.sqrt(sigma_cal**2 + sigma_rand**2/count)
wrong_independent = math.sqrt((sigma_cal**2 + sigma_rand**2)/count)
check('共同校准误差不能按独立样本平均消掉',
      common_uncertainty > sigma_cal and common_uncertainty > 2*wrong_independent,
      f'N={count}：共同项模型{common_uncertainty:.5f}，误当独立则{wrong_independent:.5f}')

# A cold-side success is not a complete refrigerator success.
cop = 0.2*280/(320-280)
drive, capacity, load = 10, 16, 12
q_cool = min(capacity, cop*drive)
q_hot = q_cool+drive
check('制冷示例冷端能力有上限且够当前负载',
      close(cop, 1.4) and close(q_cool, 14) and q_cool > load,
      f'COP={cop:.2f}, Qcool={q_cool:.1f}, load={load} E/s')
check('热端散热不足不能宣称稳态', close(q_hot, 24) and q_hot > 20,
      f'需要排热{q_hot:.1f}，散热能力20 E/s')
ram = 8*32 + 2*128 + 512 + 16*4
check('指定小任务工作集可放入B01', ram == 1088 and ram < 3584,
      f'{ram} B / 3584 B；完整元数据与更长原始记录另占持久载体')

lines = [
    '# L1：有限模型与反例复算', '',
    '2026-09-08。来源：[实验与仪器](LATE_L1_EXPERIMENTS_AND_INSTRUMENTS.md)。', '',
    '脚本：[late_l1_model_probe.py](late_l1_model_probe.py)。运行：', '',
    '```powershell', 'python -X utf8 docs/system-rebuild/late_l1_model_probe.py', '```', '',
    f'结果：**{len(checks)}/{len(checks)}项指定检查通过**。', '',
    '这些检查使用作者给定的有限信号和数值，验证候选例子中的混淆、退化和边界。'
    '它们没有验证真实材料、完整统计估计、制冷制程、B01完整程序、Minecraft性能或玩家体验。', '',
    '| 检查 | 结果 | 有限证据 |', '| --- | --- | --- |',
]
lines.extend(f'| {name} | 通过 | {evidence} |' for name, _, evidence in checks)
lines += ['',
          '实际原型仍需测试非整周期/时钟漂移、前端饱和、非稳定偏置、'
          '有噪声谱线匹配、校准协方差、未知前景、热端动态与真实运行资源。'
          '当前没有把这些未验证情形当作通过。', '']
(BASE / 'LATE_L1_MODEL_PROBE.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'checks': len(checks), 'all_pass': all(c[1] for c in checks)}, ensure_ascii=False))

"""Finite author-side L1.2 examples; no Minecraft, full material model, or sky renderer."""
from pathlib import Path
import cmath
import math

BASE = Path(__file__).resolve().parent
checks = []


def check(name, passed, evidence):
    checks.append((name, bool(passed), evidence))


def close(a, b, tol=1e-8):
    return abs(a - b) <= tol


def ledger(energy, angle, count=100, gap=2):
    probability = 0.2 * math.cos(math.radians(angle)) ** 2
    return (count * (1 - probability) * energy,
            count * probability * (energy - gap),
            count * probability * gap)


balances = [ledger(e, a) for e, a in [(6, 0), (8, 0), (6, 60)]]
check('方向与换源例子的完整能量账',
      all(close(sum(row), total) for row, total in zip(balances, [600, 800, 600]))
      and all(close(a, b) for a, b in zip(balances[2], [570, 20, 10])),
      '; '.join(str(tuple(round(v, 6) for v in row)) for row in balances))
check('同次观测可兼容两个解释，换源才产生峰位分歧',
      (6 - 2) == 4 and (8 - 2) != 4,
      '输入6: 固定差/固定发光均4；输入8: 预测6/4，不涉及唯一机制判定')
wavelengths = [(24 / e, 24 / (e - 2)) for e in (6, 8)]
check('固定能量差不等于固定波长差',
      not close(wavelengths[0][1] - wavelengths[0][0],
                wavelengths[1][1] - wavelengths[1][0]),
      f'仅此单位例取e*λ*=24，两组输入/输出波长={wavelengths}；非L1谱尺')
detected = balances[0][1] * 0.5
uncollected = balances[0][1] - detected
check('收集损耗不能全部计入样品热',
      close(detected, 40) and close(uncollected, 40)
      and close(balances[0][0] + detected + uncollected + balances[0][2], 600),
      '检测40，未收集转换光40，未转换480，材料模式40；仍为600')


def pulse_step(stored, injection, dt, lifetime):
    after_relax = stored * math.exp(-dt / lifetime)
    return after_relax + injection, stored - after_relax


stored, heat = 0.0, 0.0
for injection in [40, 10, 40, 0]:
    stored, released = pulse_step(stored, injection, 1, 2)
    heat += released
check('步末注入的模式弛豫只向热流转移一次', close(stored + heat, 90),
      f'累计注入90，残余模式={stored:.6f}，累计释热={heat:.6f}')
one_step = pulse_step(40, 0, 4, 2)[0]
four_steps = 40
for _ in range(4):
    four_steps = pulse_step(four_steps, 0, 1, 2)[0]
check('无新注入时改变弛豫划分不改变残余能量', close(one_step, four_steps),
      f'一次4秒/四次1秒均剩余{one_step:.6f}；不验证连续泵浦离散化')

coherent = [abs(0.4 + 0.3 * cmath.exp(1j * phase)) ** 2
            for phase in [0, math.pi / 2, math.pi]]
check('可选相干例与非相干例确有不同预测',
      all(close(x, y) for x, y in zip(coherent, [0.49, 0.25, 0.01]))
      and all(0 <= p <= 1 for p in coherent),
      f'同一完整末态的三个相位概率={coherent}；可区分贡献的和=0.25')


def lens_equation(theta, b, s, beta):
    return theta - b * theta / math.hypot(theta, s) - beta


def tau(theta, b, s, beta):
    return 0.5 * (theta - beta) ** 2 - b * math.hypot(theta, s)


def mu(theta, b, s):
    r = math.hypot(theta, s)
    return 1 / ((1 - b / r) * (1 - b * s * s / r ** 3))


def roots(b, s, beta):
    found = []
    left = -4.0
    fl = lens_equation(left, b, s, beta)
    for index in range(1, 1601):
        right = -4 + index * 0.005
        fr = lens_equation(right, b, s, beta)
        root = None
        if close(fl, 0, 1e-14):
            root = left
        elif fl * fr < 0:
            lo, hi, flo = left, right, fl
            for _ in range(55):
                mid = (lo + hi) / 2
                fm = lens_equation(mid, b, s, beta)
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            root = (lo + hi) / 2
        if root is not None and not any(close(root, x, 1e-7) for x in found):
            found.append(root)
        left, fl = right, fr
    return sorted(found, key=lambda theta: tau(theta, b, s, beta))


b, s, beta = 2.0, 0.5, 0.2
world = roots(b, s, beta)
check('指定有限势由求根得到三个像', len(world) == 3
      and max(abs(lens_equation(x, b, s, beta)) for x in world) < 1e-10,
      f'按到达时间排序θ={world}；只覆盖本例扫描范围')
theta_a, theta_b, theta_c = world
scale = 120 / (tau(theta_b, b, s, beta) - tau(theta_a, b, s, beta))
delay_c = scale * (tau(theta_c, b, s, beta) - tau(theta_a, b, s, beta))
check('第三像时延来自同一时间面', close(delay_c, 238.6996995197791, 1e-6)
      and scale > 0,
      f'以AB=120定K={scale:.9f}，推得AC={delay_c:.9f}秒')
eps = 1e-5
stationarity = [(tau(x + eps, b, s, beta) - tau(x - eps, b, s, beta))
                / (2 * eps) for x in world]
check('求得像位置也是时间面的数值驻点', max(map(abs, stationarity)) < 1e-7,
      f'独立有限差分dτ/dθ={stationarity}')


def source_2d(x, y, b, s):
    radius = math.sqrt(x*x + y*y + s*s)
    return (x - b*x/radius, y - b*y/radius)


numerical_magnifications = []
for x in world:
    radial = (source_2d(x + eps, 0, b, s)[0]
              - source_2d(x - eps, 0, b, s)[0]) / (2 * eps)
    tangential = (source_2d(x, eps, b, s)[1]
                  - source_2d(x, -eps, b, s)[1]) / (2 * eps)
    numerical_magnifications.append(1 / (radial * tangential))
check('放大率与二维映射的数值雅可比一致',
      all(close(num, mu(x, b, s), 1e-5)
          for x, num in zip(world, numerical_magnifications)),
      f'有限差分μ={numerical_magnifications}')
check('奇偶符号不产生负通量', mu(theta_b, b, s) < 0
      and all(abs(mu(x, b, s)) > 0 for x in world),
      f'B的μ={mu(theta_b, b, s):.6f}，亮度使用绝对值；不测试焦散附近')

# Fit each candidate from two measured image positions and their measured delay.
# No use of the world s/b/beta in this fitter.
def candidate_fit(a, other, measured_delay, core):
    strength = ((a - other)
                / (a/math.hypot(a, core) - other/math.hypot(other, core)))
    source = a - strength*a/math.hypot(a, core)
    time_scale = measured_delay / (tau(other, strength, core, source)
                                  - tau(a, strength, core, source))
    candidate_roots = roots(strength, core, source)
    central = min(candidate_roots, key=abs)
    prediction = time_scale * (tau(central, strength, core, source)
                               - tau(a, strength, core, source))
    ratio = abs(mu(central, strength, core) / mu(a, strength, core))
    return dict(core=core, b=strength, beta=source, scale=time_scale,
                theta_c=central, delay_c=prediction, ratio=ratio,
                roots=candidate_roots)


candidates = [candidate_fit(theta_a, theta_b, 120, core)
              for core in [0.35, 0.5, 0.65]]
check('三套候选都通过相同AB观测',
      all(abs(lens_equation(x, c['b'], c['core'], c['beta'])) < 1e-9
          for c in candidates for x in [theta_a, theta_b])
      and all(close(c['scale'] * (tau(theta_b, c['b'], c['core'], c['beta'])
                                 - tau(theta_a, c['b'], c['core'], c['beta'])), 120)
              for c in candidates),
      '拟合器只接收AB角位置、AB时延和候选核尺度，不接收世界核尺度')
check('已拟合的候选产生不同未来观测',
      max(c['delay_c'] for c in candidates) - min(c['delay_c'] for c in candidates) > 38
      and max(c['theta_c'] for c in candidates) - min(c['theta_c'] for c in candidates) > 0.04,
      '; '.join(f"s={c['core']}: θC={c['theta_c']:.6f}, Δt={c['delay_c']:.6f}, "
                f"C/A={100*c['ratio']:.6f}%" for c in candidates))

mass = -theta_a * theta_b
point_beta = theta_a + theta_b
point_roots = [(point_beta + sign * math.sqrt(point_beta**2 + 4*mass)) / 2
               for sign in [1, -1]]
point_tau = lambda x: 0.5*(x - point_beta)**2 - mass*math.log(abs(x))
point_scale = 120 / (point_tau(theta_b) - point_tau(theta_a))
check('两像点质量模板也可拟合已有观测而无中心像',
      mass > 0 and point_scale > 0
      and all(close(x, y) for x, y in zip(point_roots, [theta_a, theta_b])),
      f'二次方程恰有两个非零根，m={mass:.6f}, β={point_beta:.6f}, K={point_scale:.6f}')
check('2%理想硬检出限不足以排除任一有限核候选',
      all(c['ratio'] < 0.02 for c in candidates),
      '仅演示低于阈值的可能性，不等于真实假阳性/漏检率计算')
above = [c['core'] for c in candidates if c['ratio'] > 0.008]
check('0.8%理想硬检出限下仍有较暗候选', above == [0.5, 0.65],
      f'亮于检出限的核尺度={above}，0.35仍可未检出；假设时窗位置覆盖完整')
gains = [(0.01*g)/(0.005*g) for g in [1, 10, 100]]
check('同时放大已有信号与噪声不提高信噪比', all(close(v, 2) for v in gains),
      '输入信号0.01、噪声0.005，增益1/10/100时信噪比均2；不含后级新增噪声')


def pulse(t):
    return math.exp(-((t-20)/3)**2) + 0.6*math.exp(-((t-31)/5)**2)


first_trace = [pulse(t) for t in range(300)]
second_trace = [pulse(t-120-15) for t in range(300)]
correlations = [(lag, sum(first_trace[t] * second_trace[t+lag]
                          for t in range(300-lag))) for lag in range(80, 161)]
observed_lag = max(correlations, key=lambda pair: pair[1])[0]
check('互相关无法自动消除两个时钟的相对偏移', observed_lag == 135,
      f'同一无噪光变，物理延迟120、B钟快15，匹配峰={observed_lag}；校正后120')
periodic = [1.0 if t % 16 == 0 else 0.0 for t in range(64)]
shifted = [periodic[(t-3) % 64] for t in range(64)]
scores = [sum(periodic[t] * shifted[(t+lag) % 64] for t in range(64))
          for lag in range(64)]
aliases = [lag for lag, score in enumerate(scores) if close(score, max(scores))]
check('纯周期有限记录可以给出多个相同匹配峰', aliases == [3, 19, 35, 51],
      f'64点循环边界例的等高峰={aliases}；实际缺测/有限窗须另处理')

passed = sum(result for _, result, _ in checks)
lines = [
    '# L1.2两条任务的有限复算', '',
    '生成脚本：[late_l12_task_probe.py](late_l12_task_probe.py)。运行：'
    '`python -X utf8 docs/system-rebuild/late_l12_task_probe.py`。', '',
    f'结果：**{passed}/{len(checks)}项通过**。作者指定的期望值、数值求根和反例；'
    '不是Minecraft运行、物理发现、硬件制备或完整随机实验验证。', '',
    '任务说明：[材料过程](LATE_L12_PROCESS_GAMEPLAY.md)、'
    '[错时天区](LATE_L12_SKY_EXPLORATION.md)。', '',
    '| 检查 | 结果 | 有限证据 |', '| --- | --- | --- |',
]
for name, result, evidence in checks:
    lines.append(f"| {name} | {'通过' if result else '失败'} | {evidence} |")
lines += ['', '## 验证边界', '',
          '- 没有验证完整材料状态到响应的映射、制程数量、封装求解、随机光子统计或实际实验界面。',
          '- 天区例只验证给定轴对称势的有限根、时间面及候选分歧；未做全参数误差传播、PSF渲染、有限源焦散或真实天体反演。',
          '- 检出限为无误差硬阈值反例，实际判读必须给覆盖、背景、噪声及假阳性/漏检条件。',
          '- 时序例使用合成数据；未验证真实调度、分布式校时、区块加载或数据防重复机制。',
          '- B01数据布局只是任务稿中的容量预算，未运行程序；全局科技图与Java均未修改。', '']
(BASE / 'LATE_L12_TASK_PROBE.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'L1.2 finite task checks: {passed}/{len(checks)} passed')
print(f'AB delay=120; AC delay={delay_c:.9f}; C/A={abs(mu(theta_c,b,s)/mu(theta_a,b,s)):.9f}')
if passed != len(checks):
    raise SystemExit(1)

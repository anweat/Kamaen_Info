"""Bounded design experiments, not game code or full physical simulation.

Uses only the Python standard library. Writes MODEL_LAB_RESULTS.md beside itself.
Truth values in the report are developer diagnostics, not proposed player UI.
"""
from pathlib import Path
import cmath
import hashlib
import math
import random
import statistics as st


OUT = Path(__file__).resolve().parent


def solve(matrix, rhs):
    a = [row[:] + [v] for row, v in zip(matrix, rhs)]
    n = len(rhs)
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(a[r][i]))
        if abs(a[pivot][i]) < 1e-9:
            raise ValueError("unidentifiable design")
        a[i], a[pivot] = a[pivot], a[i]
        scale = a[i][i]
        a[i] = [v / scale for v in a[i]]
        for r in range(n):
            if r != i:
                scale = a[r][i]
                a[r] = [x - scale*y for x, y in zip(a[r], a[i])]
    return [row[-1] for row in a]


def fit(rows):
    n = len(rows[0][0])
    gram = [[sum(x[i]*x[j] for x, _ in rows) for j in range(n)] for i in range(n)]
    rhs = [sum(x[i]*y for x, y in rows) for i in range(n)]
    return solve(gram, rhs)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rms(xs):
    return math.sqrt(st.mean(x*x for x in xs))


def indexed_noise(seed, stream, epoch):
    key = f"D1/{seed}/{stream}/{epoch}".encode()
    value = int.from_bytes(hashlib.sha256(key).digest()[:8], "big")
    uniform = (value + 0.5) / (2**64)
    return (2*uniform - 1)*math.sqrt(3)


def correlated(seed, stream, epoch):
    weights = [0.8**k for k in range(8)]
    return sum(w*indexed_noise(seed, stream, epoch-k) for k, w in enumerate(weights)) / math.sqrt(sum(w*w for w in weights))


def crystal_experiment(seed):
    rng = random.Random(seed)
    truth = [8 + rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.5), rng.uniform(1, 2), rng.uniform(0.1, 0.4)]
    # Production data changes composition and pressure together, fixed direction.
    bad = []
    for i in range(100):
        pressure = rng.uniform(-1, 1)
        x = [1, pressure, 0.3*pressure, pressure]
        bad.append((x, dot(x, truth) + rng.gauss(0, 0.008)))
    try:
        fit(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("confounded design was accepted")

    # Fresh manufactured samples, factorial interventions, randomized read order.
    settings = [(s, c, theta) for s in (-1, 0, 1) for c in (-0.3, 0, 0.3)
                for theta in (0, math.pi/2) for _ in range(4)]
    rng.shuffle(settings)
    train = []
    for s, c, theta in settings:
        x = [1, s, c, s*math.cos(2*theta)]
        train.append((x, dot(x, truth) + rng.gauss(0, 0.008)))
    estimate = fit(train)
    constant = st.mean(y for _, y in train)
    # Distinct specimens and unseen settings, no validation labels used for fit.
    validation = []
    for _ in range(40):
        s, c, theta = rng.uniform(-1, 1), rng.uniform(-0.3, 0.3), rng.uniform(0, math.pi)
        x = [1, s, c, s*math.cos(2*theta)]
        validation.append((x, dot(x, truth) + rng.gauss(0, 0.008)))
    error = rms(dot(x, estimate)-y for x, y in validation)
    baseline = rms(constant-y for _, y in validation)
    assert error < 0.025 and error < baseline/5, (seed, error, baseline)
    return error, baseline, max(abs(a-b) for a, b in zip(truth, estimate))


def background_experiment(seed):
    rng = random.Random(10000 + seed)
    amplitude = rng.uniform(1, 2)
    by_state = {0: [], 1: []}
    naive = []
    for block in range(128):
        states = [0, 1]
        rng.shuffle(states)
        for offset, active in enumerate(states):
            epoch = 1000 + 2*block + offset
            shared = correlated(seed, "shared", epoch)
            readings = []
            for station, distance, background, bias in (("near", 1, 1.2, 0.5), ("far", 3, 2.0, -0.1)):
                local = 0.2*correlated(seed, station, epoch)
                instrument = 0.02*indexed_noise(seed, "instrument/"+station, epoch)
                y = background + bias + 5*shared + local + amplitude*active/(1+distance**2) + instrument
                readings.append(y)
            by_state[active].append(readings[0]-readings[1])
            if active:
                naive.append(readings[0]/0.5)
    # Independent background/bias terms cancel across balanced on/off conditions;
    # common field cancels between simultaneous sites, local noise remains.
    estimate = (st.mean(by_state[1])-st.mean(by_state[0]))/(0.5-0.1)
    error = abs(estimate-amplitude)
    naive_error = abs(st.mean(naive)-amplitude)
    assert error < 0.16 and error < naive_error, (seed, error, naive_error)
    return error, naive_error


def response_checks():
    # Passive, normalized two-mode response; not a nonlinear crystal solver.
    maximum = 0
    for angle in (0, math.pi/4, math.pi/2):
        centers = [4+0.3*math.cos(2*angle), 7-0.2*math.cos(2*angle)]
        for i in range(1001):
            f = i/100
            h = sum(w/(1+1j*(f-center)/width)
                    for w, center, width in zip((0.4, 0.6), centers, (0.3, 0.6)))
            maximum = max(maximum, abs(h))
            assert math.isfinite(abs(h)) and abs(h) <= 1+1e-12
    assert abs(cmath.phase(1/(1+1j))) > 0
    # Noise-free approach to mean is distinct from later purposeful specialization.
    delta = [0.4, -0.3, 0.2]
    initial = rms(delta)
    for _ in range(20):
        delta = [0.8*x for x in delta]
    assert rms(delta) < initial/50
    return maximum, rms(delta)/initial


def correlation_check():
    # Disjoint history blocks; compare variance of eight consecutive means.
    means_correlated, means_independent = [], []
    for block in range(500):
        start = block*32
        means_correlated.append(st.mean(correlated(91, "corr", start+i) for i in range(8)))
        means_independent.append(st.mean(indexed_noise(91, "iid", start+i) for i in range(8)))
    ratio = st.variance(means_correlated)/st.variance(means_independent)
    assert ratio > 2, ratio
    a = correlated(1, "physical", 100)
    assert a == correlated(1, "physical", 100)
    assert a != correlated(1, "physical", 101)
    assert indexed_noise(1, "instrument/A", 100) != indexed_noise(1, "instrument/B", 100)
    return ratio


def main():
    crystals = [crystal_experiment(seed) for seed in range(20)]
    backgrounds = [background_experiment(seed) for seed in range(20)]
    maximum, contraction = response_checks()
    variance_ratio = correlation_check()
    report = f"""# 模型发现原型检查

讨论稿D1；纯Python离线设计实验，不是Minecraft实现或真实物理验证。
固定测试20组种子，未挑选个别成功案例。真实参数只用于开发验证，不属于玩家仪器输出。

| 检查 | 结果 |
| --- | --- |
| 共线组成/应力数据 | 20/20不能独立辨识，明确拒绝拟合 |
| 交叉干预后的未见样品RMSE | 平均 {st.mean(r[0] for r in crystals):.5f}，最大 {max(r[0] for r in crystals):.5f} |
| 同数据常数基准RMSE | 平均 {st.mean(r[1] for r in crystals):.5f} |
| 系数最大误差（20组最坏） | {max(r[2] for r in crystals):.5f} |
| 底噪近远/开关对照的源强绝对误差 | 平均 {st.mean(r[0] for r in backgrounds):.5f}，最大 {max(r[0] for r in backgrounds):.5f} |
| 不分背景的单点估计误差 | 平均 {st.mean(r[1] for r in backgrounds):.5f} |
| 8次相关采样均值方差 / 独立采样均值方差 | {variance_ratio:.3f}；重复次数不能直接当独立样本数 |
| 同物理索引重读、不同仪器随机流 | 一致性/分离检查通过 |
| 被动双峰响应最大模 | {maximum:.5f}，未超过1 |
| 无扰动均值化20步后的偏差比例 | {contraction:.5f} |

晶体使用理想化峰位摘要与已知线性模型族，不含实际扫谱/峰提取、缺陷混叠和仪器漂移。
底噪使用一个共同场、两站局部场、固定偏差和瞬时机器开关，不含真实热惯性、空间连续插值或区块卸载。
本检查表明候选简化机制能产生可区分实验；不证明全部参数可辨识、玩法有趣、研究时长合理或现实科学成立。

复现：`python docs/system-rebuild/model_lab.py`。只写本目录的MODEL_LAB_RESULTS.md。
"""
    (OUT/"MODEL_LAB_RESULTS.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()

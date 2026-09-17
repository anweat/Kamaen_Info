"""R3.2 finite design probes for frames, ports, bridges and factor accounting.

These are authored game-contract examples, not a Minecraft integration, geometry
router, thermal solver, or real electro-optical device simulator.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import json
import math

BASE = Path(__file__).resolve().parent
IDENTITY = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
YAW90 = ((0, 0, 1), (0, 1, 0), (-1, 0, 0))


def rotate(r, v):
    return tuple(sum(r[i][j] * v[j] for j in range(3)) for i in range(3))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def near(a, b):
    return all(math.isclose(x, y, abs_tol=1e-9) for x, y in zip(a, b))


@dataclass(frozen=True)
class Frame:
    rotation: tuple = IDENTITY
    translation: tuple = (0, 0, 0)
    scale: float = 1

    def __post_init__(self):
        r = self.rotation
        if not math.isfinite(self.scale) or self.scale <= 0:
            raise ValueError('scale must be positive')
        if len(r) != 3 or any(len(row) != 3 for row in r):
            raise ValueError('rotation must be 3 by 3')
        if not all(math.isclose(dot(r[i], r[j]), int(i == j), abs_tol=1e-9)
                   for i in range(3) for j in range(3)):
            raise ValueError('rotation must preserve lengths and angles')
        det = (r[0][0]*(r[1][1]*r[2][2]-r[1][2]*r[2][1])
               -r[0][1]*(r[1][0]*r[2][2]-r[1][2]*r[2][0])
               +r[0][2]*(r[1][0]*r[2][1]-r[1][1]*r[2][0]))
        if not math.isclose(det, 1, abs_tol=1e-9):
            raise ValueError('reflection is not an installation rotation')

    def point(self, p):
        return tuple(t + self.scale*v for t, v in zip(self.translation, rotate(self.rotation, p)))

    def normal(self, n):
        return rotate(self.rotation, n)  # Only positive uniform scale in this fixture.


@dataclass(frozen=True)
class Port:
    position: tuple
    normal: tuple
    medium: str
    representation: str
    flow: str
    connector: str
    selected_band: str = 'band_A'


def dock(source, target):
    # Simplified contact test at a common coordinate scale, not full collision checking.
    return (near(source.position, target.position)
            and math.isclose(dot(source.normal, target.normal), -1, abs_tol=1e-9)
            and source.connector == target.connector
            and source.medium == target.medium
            and source.representation == target.representation
            and source.selected_band == target.selected_band
            and source.flow in ('out', 'duplex') and target.flow in ('in', 'duplex'))


def bridge(source_representation, target_representation, installed, powered, reference):
    profiles = {
        'intensity_encoder': ('electronic_samples', 'optical_intensity', False),
        'coherent_encoder': ('electronic_samples', 'optical_coherent', True),
        'intensity_reader': ('optical_intensity', 'electronic_samples', False),
        'phase_reader': ('optical_coherent', 'electronic_phase_samples', True),
        'packet_receiver': ('optical_packets', 'electronic_packets', False),
    }
    if installed not in profiles or not powered:
        return False
    src, dst, requires_reference = profiles[installed]
    return src == source_representation and dst == target_representation and (
        not requires_reference or reference)


def transmission_product(records):
    # Records represent disjoint contributions in one passive intensity path,
    # at the same declared frequency/conditions. Coherent branches need another model.
    seen, value = set(), 1.0
    for name, covered_effects, transmission in records:
        if seen & covered_effects:
            raise ValueError('duplicate physical contribution: ' + name)
        if not 0 <= transmission <= 1:
            raise ValueError('not a passive intensity factor: ' + name)
        seen |= covered_effects
        value *= transmission
    return value


frames = [Frame(translation=(.5, 0, .5)), Frame(translation=(0, 1, 0)),
          Frame(rotation=YAW90, translation=(10, 0, 5))]
p, n = (0, 0, .5), (0, 0, 1)
for f in frames:
    p, n = f.point(p), f.normal(n)
output = Port(p, n, 'optical', 'optical_packets', 'out', 'fiber_pair')
input_port = Port(p, tuple(-x for x in n), 'optical', 'optical_packets', 'in', 'fiber_pair')
cycle = (1, 2, 3)
for _ in range(4):
    cycle = rotate(YAW90, cycle)
axis, excitation = (1, 0, 0), (1/math.sqrt(2), 0, 1/math.sqrt(2))
effects = {'inlet_loss', 'region_loss', 'outlet_loss'}
inlet, region, outlet, external = .9, .8, .9, .95
flat_records = [('inlet_coupler', {'inlet_loss'}, inlet), ('filter_region', {'region_loss'}, region),
                ('outlet_coupler', {'outlet_loss'}, outlet), ('external_path', {'outside_loss'}, external)]
summary_records = [('sealed_module', effects, inlet*region*outlet),
                   ('external_path', {'outside_loss'}, external)]
duplicate_rejected = False
try:
    transmission_product(summary_records + [('inlet_again', {'inlet_loss'}, inlet)])
except ValueError:
    duplicate_rejected = True
invalid_frames_rejected = 0
for kwargs in [dict(scale=-1), dict(rotation=((-1, 0, 0), (0, 1, 0), (0, 0, 1)))]:
    try:
        Frame(**kwargs)
    except ValueError:
        invalid_frames_rejected += 1

checks = {
    '器件到封装到板柜的坐标变换可追溯': near(p, (11, 1, 4.5)) and near(n, (1, 0, 0)),
    '四次直角旋转恢复坐标': near(cycle, (1, 2, 3)),
    '共同刚体旋转保持相对晶轴投影': math.isclose(dot(axis, excitation), dot(
        rotate(YAW90, axis), rotate(YAW90, excitation))),
    '尺度换算不把单位法线放大': near(Frame(scale=2).point((1, 0, 0)), (2, 0, 0))
        and near(Frame(scale=2).normal((1, 0, 0)), (1, 0, 0)),
    '镜像或负尺度不能伪装成普通安装旋转': invalid_frames_rejected == 2,
    '对接条件齐备的端口连接': dock(output, input_port),
    '同位置但同向法线不直接对接': not dock(output, replace(input_port, normal=n)),
    '朝向相对但位置不对不能直接对接': not dock(output, replace(input_port, position=(12, 1, 4.5))),
    '旋转不改变信号输入输出职责': output.flow == 'out'
        and not dock(output, replace(input_port, flow='out')),
    '相同光介质与连接头不保证同种信号': not dock(output, replace(
        input_port, representation='optical_coherent')),
    '选定频带不兼容时不能直接对接': not dock(output, replace(input_port, selected_band='band_B')),
    '没有实体桥接器无法转域': not bridge('electronic_samples', 'optical_intensity', None, True, False),
    '强度编码桥有供给即可按自身契约工作': bridge(
        'electronic_samples', 'optical_intensity', 'intensity_encoder', True, False),
    '相干编码需所声明参考': not bridge(
        'electronic_samples', 'optical_coherent', 'coherent_encoder', True, False)
        and bridge('electronic_samples', 'optical_coherent', 'coherent_encoder', True, True),
    '普通强度读出不能冒充相位读取': not bridge(
        'optical_coherent', 'electronic_phase_samples', 'intensity_reader', True, True),
    '包光链路接收无需整网相位参考': bridge(
        'optical_packets', 'electronic_packets', 'packet_receiver', True, False),
    '失去桥接供给时路径不可用': not bridge(
        'electronic_samples', 'optical_intensity', 'intensity_encoder', False, False),
    '展开与封装报告的同一物理路径损耗一致': math.isclose(
        transmission_product(flat_records), transmission_product(summary_records)),
    '报告已含的内部贡献禁止重复叠加': duplicate_rejected,
    '无源转接后的带宽仍受实际窄段限制': min(64, 16, 64) == 16,
    '共享上联不能按节点数重复分配': math.ceil((64+64)/64) == 2,
}
assert all(checks.values()), checks
result = dict(version='R3.2-adaptation-probe', boundary=__doc__.strip(),
              world_port=dict(position=p, normal=n, flow=output.flow),
              loss_example=dict(expanded=transmission_product(flat_records),
                                summarized=transmission_product(summary_records),
                                duplicate_rejected=duplicate_rejected),
              bottleneck_example=dict(link_capacity_bytes_per_tick=64,
                                      transfer_bytes_per_request=[64, 64], minimum_transfer_ticks=2,
                                      right_angle_adapter_capacity_bytes_per_tick=16),
              checks=checks)
(BASE/'r3-hardware-adaptation-results.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# R3.2：空间、接口与因子传递的有限检查', '',
         '配套[R3.2适配讨论稿](COMPUTING_R3_HARDWARE_SPATIAL_ADAPTATION.md)，由[r3_hardware_adaptation_probe.py](r3_hardware_adaptation_probe.py)生成。', '',
         '这是作者侧的游戏契约例子。未实现Minecraft坐标/方块、碰撞寻路、完整光电响应、热仿真或真实调度器；数值不是器件出厂规格。', '',
         '## 空间与端口', '',
         '器件局部端口(0,0,0.5)、外法线+Z，经封装偏移(0.5,0,0.5)、托盘偏移(0,1,0)、机柜绕Y旋转90°及世界偏移(10,0,5)，得到世界位置(11,1,4.5)、外法线+X。信号职责仍为输出。', '',
         '本例使用统一示意长度单位；尺度测试只覆盖正的均匀缩放。真实各层需明确尺寸单位与安装转换，不能把芯片微结构长度当世界方块长度。', '',
         '## 贡献与容量', '',
         f'固定工况下，同一无源强度路径的输入耦合、选频区域、输出耦合与外部路径展开为0.9×0.8×0.9×0.95={transmission_product(flat_records):.4f}；模块报告0.648已经包含前三项，再接外部0.95得到相同结果。重复追加内部输入耦合0.9会被拒绝。此乘法不适用于任意相干分支或有源转换。', '',
         '数据路径有64、16、64 B/tick三个串联限额时，上限为16 B/tick。两份各64 B数据共用64 B/tick上联，在此仅含传输的示例里至少需要2 tick；两个节点不把该共享上联复制为两条。', '',
         '## 检查结果', '']
for label in checks:
    lines.append('- 通过：'+label+'。')
lines += ['', f'共{len(checks)}项指定检查通过；这里只验证这些有限变换、接口条件与计费反例，不能据此声称整套硬件或任意布局可运行。']
(BASE/'R3_HARDWARE_ADAPTATION_PROBE.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(dict(checks_passed=len(checks), world_port=result['world_port'],
                      path_transmission=result['loss_example']['expanded']), ensure_ascii=False))

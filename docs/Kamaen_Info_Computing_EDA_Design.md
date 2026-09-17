# Kamaen Info 算力系统与多工艺 EDA 设计

版本：v0.1 Concept Baseline
状态：当前算力系统设计基线。本文用于收束“芯片/主板/算力设计”玩法：电、光、量子微逻辑门都可以作为 EDA 元件库中的可选工艺族，但不同物理环境的逻辑门必须通过芯片、封装和接口边界隔离。第 6 阶段全光五件套仍以 `Kamaen_Info_Optical_Computing_Design.md` 为详细规范。

---

## 1. 设计目标

算力系统不是让玩家真实画晶体管或模拟电磁场，而是提供一套“可设计、可封装、可诊断、可升级”的抽象 EDA 玩法。玩家设计的不是单个万能 CPU，而是一组受材料、工艺、相干性、温度和封装约束的计算芯片与算力板。

核心循环：

```text
选择工艺族和制程节点
-> 画逻辑原理图（功能块、门、存储、I/O）
-> 进入微结构版图（层、器件、波导、管线、端口）
-> 执行规则检查（DRC）和抽象仿真
-> 编译为掩膜 / 流片蓝图
-> 按工艺制造裸片
-> 封装并声明接口
-> 装入主板 / 光背板 / 低温框架
-> 诊断瓶颈
-> 调整蓝图、材料、制程和环境
```

设计边界：

- 不做门级实时仿真；EDA 只结算抽象画像。
- 允许玩家设计“微结构版图”，但微结构只在保存、编译和诊断时结算，不在每 tick 逐元件模拟。
- 不要求玩家做真实电路均衡、电平设计、阻抗匹配、晶体管级建立/保持时间、寄生参数补偿或供电完整性分析。
- 玩家主要关注逻辑输出、元件布局、端口连接、系统级时序参数、热处理、能源/相干能供应、封装方式、洁净度和环境隔离。
- 静电防护、颗粒污染、防火/绝缘、封装应力、接触质量、暗电流等细节作为隐含工艺参数进入 DRC、良率和可靠性公式，不作为手动微操项目。
- 不允许不同物理环境的门在同一裸片内直接混放。
- 可以在同一主板、同一封装模块或同一算力节点中集成多种芯片，但必须通过明确接口连接。
- 电力可以供能；信息通路按芯片工艺族决定。全光计算阶段的信息通路仍以光为主。
- 量子/单光子级逻辑不是通用早期 CPU，而是后期高成本协处理路线。

---

## 2. EDA 工艺族

| 工艺族 | 代表元件 | 工作环境 | 主要优势 | 主要限制 |
|---|---|---|---|---|
| 电逻辑 | 晶体管门、寄存器、SRAM、I/O 控制 | 常温/散热即可 | 低门槛、控制和接口稳定 | 发热、频率上限、与主线晶体叙事弱 |
| 光逻辑 | 光逻辑门、MZI、双稳态晶胞、光RAM | 相干光路、低噪封装 | 高带宽、矩阵运算、与晶体/费曼线连续 | 需要相干能、校准和光路稳定 |
| 量子微逻辑 | 单光子门、纠缠耦合、测量门、误差校验片 | 低温、屏蔽、相干控制 | 后期采样、优化、蓝图求解能力强 | 非通用早期算力；测量会破坏状态；成本高 |
| 存储元件 | SRAM/内存页、光RAM、波函数缓存页、全息膜 | 随工艺变化 | 承载 State、Parameter、Activation | 寿命、刷新、读出损耗不同 |
| 互连元件 | 电互连、频率总线、硅光波导、相干控制线 | 随信号介质变化 | 决定带宽、延迟、同步域 | 跨介质必须用桥接器 |
| 热/冷却元件 | 热界面、液冷管、低温控制片、熵流泵 | 常温到低温 | 提升稳定性和良率 | 占面积、占接口、增加维护成本 |

EDA 编辑器中的“逻辑门”应是元件级抽象，而不是服务端 tick 内的真实门级电路。元件数量、布局密度、工艺质量和接口拓扑共同生成性能画像。

---

## 3. EDA 编辑体验

目标体验应接近“轻量微电子/光电子设计软件”，而不是单纯表单合成。玩家在芯片蓝图台中可以在两个视图间切换。

### 3.1 原理图视图

原理图视图解决“芯片要做什么”：

```text
输入端口
-> 逻辑门 / 功能块 / 存储块 / 桥接器
-> 输出端口
-> 频率域 / 时钟域 / 相干域声明
```

可放置对象：

- 门级：AND、OR、NOT、NAND、XOR、比较器、门控、选择器。
- 功能块：ALU、寄存器组、路由单元、MZI 阵列、脉冲阈值单元、采样测量阵列。
- 存储块：电 SRAM、光RAM、波函数缓存页接口、全息页接口。
- 接口块：电端口、光端口、频率总线端口、低温控制端口、桥接端口。

原理图不要求玩家画每一个晶体管。一个“ALU 块”可以展开成若干门簇，也可以保持宏单元形式。高阶玩家可以进入宏单元内部细化布局，普通玩家可以使用预设宏单元。

原理图的输出只关心逻辑语义：

```text
输入类型
-> 逻辑/算子功能
-> 输出类型
-> 消耗的算力、带宽、存储、热和能源预算
```

不暴露电平高低、阈值电压、阻抗匹配、晶体管级建立/保持时间等真实电路参数。这些参数只通过“工艺质量”“封装质量”“噪声裕量”“热裕量”等抽象指标影响成功率。

系统级时序是可设计参数：

```text
clock_domain
pipeline_stage
latency_budget
refresh_period
sample_window
phase_window
sync_boundary
```

玩家要决定“什么时候采样、什么时候刷新、哪些模块同频、哪些模块跨域同步”，但不需要手动计算每条导线的电气时序。

### 3.2 版图视图

版图视图解决“芯片怎么制造”：

```text
工艺层选择
-> 放置微结构
-> 布线 / 导波 / 冷却 / 相干线
-> 端口对齐
-> 面积、密度、串扰、热、相干损耗评分
```

版图采用格点或半格点，不做像素级自由绘图。每个元件有 footprint、方向、层需求和 keepout 区域。

典型层：

| 层 | 电芯片含义 | 光芯片含义 | 量子/低温含义 |
|---|---|---|---|
| substrate | 晶圆/基底 | 硅光基底/卡玛恩导波基底 | 低温载片/拓扑基底 |
| active | PN 结、晶体管沟道 | 非线性腔、探测结 | 单光子源、量子点 |
| metal_1/2/3 | 电互连 | 加热/控制辅助线 | 低温控制与屏蔽线 |
| optical | 无或光电接口 | 波导、MZI、分束器 | 单光子波导 |
| memory | SRAM/缓存阵列 | 光RAM 循环腔 | 波函数缓存接口 |
| cooling | 热界面、微流道 | 光源散热、稳相温控 | 低温管线、热隔离槽 |
| shield | EMI 屏蔽 | 杂散光隔离 | 量子屏蔽、观测隔离 |
| ports | 引脚、焊盘 | 光栅耦合器、光纤口 | 低温排线、测量口 |

### 3.3 微结构库

微结构是版图中的最小可玩单位。它不是实时模拟单位，而是编译评分单位。

| 类别 | 示例 | 关键参数 |
|---|---|---|
| 电微结构 | 晶体管指、PN 结、过孔、金属互连、SRAM 单元 | 宽度、长度、扇出、寄生电容、发热 |
| 光微结构 | 直波导、弯曲波导、Y 分束器、MZI、环形谐振腔、光栅耦合器 | 曲率半径、相位长度、损耗、串扰 |
| 卡玛恩非线性结构 | 非线性腔、双稳态晶胞、阈值门、饱和吸收腔 | χ²、阈值漂移、响应 tick、相干消耗 |
| 量子微结构 | 单光子源、纠缠耦合器、测量门、SNSPD、误差校验片 | 保真度、暗计数、退相干、测量破坏 |
| 存储结构 | 电 SRAM、光循环腔、波函数缓存接口、全息膜页口 | 容量、保持时间、读取损耗、刷新成本 |
| 工程结构 | 冷却微流道、热通孔、屏蔽环、隔离沟槽、应力释放槽、防尘封盖、ESD 防护环、绝缘/防火层 | 冷却能力、占面积、隔离评分、制造难度、可靠性 |

### 3.4 设计规则检查（DRC）

DRC 是 EDA 玩法的主要反馈，不靠玩家猜。

检查项：

- 最小线宽、最小间距、最小波导弯曲半径。
- 光路交叉、相位长度不匹配、MZI 臂长差超限。
- 电互连过载、扇出过高、热密度过高。这里的“过载/扇出”是抽象 DRC，不要求玩家手动计算电平和阻抗。
- 量子区靠近热源、测量门离缓存太近、屏蔽断开。
- 冷却管线不闭合、低温区域和常温区域无隔离沟槽。
- 端口没有映射到封装焊盘、光口或低温口。
- 不同 `die_domain` 的主逻辑无桥接直接相连。
- 缺少基础工艺防护：静电防护环、颗粒防护封盖、防火/绝缘隔离、封装应力释放槽。缺失时通常给 warning 或降低良率，不阻断早期流片。

DRC 输出三类结果：

```text
error: 不能流片，例如不同环境域短接、端口悬空、低温区无隔离
warning: 可流片但降分，例如热密度偏高、波导弯曲损耗大
hint: 优化建议，例如移动激光源、增加热通孔、缩短相干线
```

### 3.5 抽象仿真

仿真不做真实 SPICE/FDTD/量子态演化，而是基于版图图结构结算。

输出：

- 逻辑连通性：端口是否连接、方向是否正确、是否有环路。
- 时序/相干估算：路径长度、频率域、刷新周期、相位漂移。
- 热估算：热点、冷却管线距离、热界面质量。
- 良率估算：面积、层数、微结构复杂度、制程精度、洁净度。
- 工艺隐患估算：静电、颗粒、封装应力、绝缘、防火、接触质量。
- 算力画像：`control_ops`、`matrix_ops`、`route_ops`、`sampling_ops` 等。

玩家看到的是“版图热图 + 错误标记 + 指标拆项”，不是黑盒成功/失败。

### 3.6 时序参数设计

时序设计是 EDA 的核心可玩层。它不是旧频率协议的附属项，而是“频率信息的延伸”：频率决定可用信道和载波等级，时序决定信息在信道中如何排列、采样、对齐、刷新、复用和闭环。

```text
频率 = 信息载体的等级
时序 = 信息在载体上的组织方式
```

时序不进入真实电路时序收敛。玩家不做晶体管级建立/保持时间、不做寄生补偿、不做电源完整性分析。玩家设计的是系统级信息节拍。

### 3.6.1 时序等级

建议引入独立的 T0-T5 时序等级。F1-F5 仍是频率/协议等级；T0-T5 是时间组织能力等级。二者相关但不等价。

| 时序等级 | 名称 | 解锁能力 | 典型用途 |
|---|---|---|---|
| T0 | 手动/事件时序 | 单次触发、无稳定节拍 | 手动机器、一次性流片、调试 |
| T1 | tick 时序 | 固定 tick 周期、简单边沿触发 | 红石边界、低速探针、早期控制 |
| T2 | 缓存时序 | 采样窗口、去抖、FIFO、延迟预算 | 传感器汇聚、信息中心、存储页 |
| T3 | 流水时序 | 流水级、批处理节拍、同步路径长度 | 矩阵/激活、批量工艺调度、多模块协作 |
| T4 | 相干时序 | 相位窗口、锁相 epoch、光RAM 刷新窗口 | 光控制核、光GPU、光RAM、F4 光互连 |
| T5 | 观测/维度时序 | 相干窗口、后选择测量窗口、跨维度时间锁 | 量子光学协处理器、视界、维度创世 |

频率和时序组合示例：

```text
F2 + T2 = 数据频段上的缓存/采样网络
F3 + T3 = 矩阵/激活频段上的流水和批处理
F4 + T4 = 光频协议上的相干相位窗口和刷新周期
F5 + T5 = 维度同步频段上的观测窗口和世界规则锁相
```

低频可以有高级时序，例如 F2 + T3 的低速但严格流水控制；高频也可能时序粗糙，例如 F4 + T1 只能传高速脉冲但无法稳定光逻辑闭环。

可设计对象：

| 对象 | 参数 | 影响 |
|---|---|---|
| 时钟域 | `clock_domain`,`frequency_tier`,`sync_source` | 决定模块是否能直接通信 |
| 流水级 | `pipeline_stage`,`stage_latency`,`buffer_between_stages` | 决定吞吐、延迟和状态缓存需求 |
| 采样窗口 | `sample_window`,`trigger_edge`,`debounce_ticks` | 决定传感器/端口读入稳定性 |
| 刷新周期 | `refresh_period`,`state_life_ticks` | 决定寄存器、光RAM、波函数缓存能否稳定保持 |
| 光路相位窗口 | `phase_window`,`path_length_class`,`calibration_epoch` | 决定 MZI、光逻辑门和光GPU 的相干稳定 |
| 跨域同步 | `sync_boundary`,`fifo_depth`,`bridge_latency` | 决定电-光、光-量子、主板-背板通信损耗 |
| 时序等级 | `timing_tier`,`timing_mode`,`timing_precision` | 决定可用的采样、流水、刷新、相位和观测机制 |

### 3.6.2 频率域与时序域

EDA 版图中的每个端口、宏单元和同步线都同时声明频率域和时序域：

```text
frequency_tier: F1 / F2 / F3 / F4 / F5
timing_tier: T0 / T1 / T2 / T3 / T4 / T5
sync_domain_id
clock_source
clock_tree_quality
timing_source
timing_precision
```

连接规则：

```text
同频 + 同时序域：满速、低延迟连接
同频 + 不同时序域：需要同步边界、FIFO 或采样器
相邻频段 + 兼容时序：需要频率桥，带宽下降
相邻频段 + 不兼容时序：需要频率桥 + 时序桥
差距过大：必须通过缓存、协议转换或任务队列解耦
```

对玩家的表现是“这条路径能否按指定节拍稳定输出结果”，不是电气波形是否满足纳秒级约束。

### 3.6.3 时序结构件

时序玩法需要实体化元件，而不是只在 GUI 填数字。

| 元件 | 作用 | 对应等级 |
|---|---|---|
| `timing_marker` | 给路径打节拍标记，定义 T1/T2 边界 | T1-T2 |
| `sample_window_gate` | 只在窗口内采样输入，降低抖动 | T2 |
| `sync_fifo_cell` | 跨时序域缓存，吸收延迟差 | T2-T3 |
| `pipeline_latch_cell` | 明确流水级边界 | T3 |
| `phase_epoch_marker` | 标记一组光路共享相位 epoch | T4 |
| `refresh_scheduler_cell` | 为光RAM/状态缓存安排刷新周期 | T2-T4 |
| `observation_window_gate` | 控制量子/费曼/视界观测窗口 | T5 |

这些元件都只结算抽象参数；玩家不需要调真实电平。

### 3.6.4 同步路径与长度差

同步节点之间的线路长度需要接近，长度差过大会降低多模块并行效率。EDA 中保留这个玩法，并扩展到芯片版图：

```text
sync_distance_delta = max(sync_path_lengths) - min(sync_path_lengths)
sync_penalty = sync_distance_delta / max(1, sync_tolerance)
```

时序检查只计算抽象路径长度、频率域、同步组和带宽等级。它不模拟电磁场。

不同 trace 类型权重不同：

| trace | 更敏感的项 |
|---|---|
| `control_trace` | 同步距离差、跨域桥接 |
| `data_trace` | 带宽拥塞、路径长度 |
| `memory_trace` | 延迟、刷新窗口 |
| `matrix_trace` | 带宽、批量对齐 |
| `sync_trace` | 长度差、锁相质量 |
| `optical_trace` | 相位窗口、路径长度差、相干能、T4 epoch |
| `cooling_trace` | 覆盖率、热点距离 |

### 3.6.5 延迟预算

EDA 时序报告把芯片、主板和网络路径纳入同一延迟预算口径：

```text
expected_ticks =
  compute_ticks
  + queue_delay
  + route_latency
  + bridge_latency
  + schema_or_format_transform_latency
  + refresh_wait_ticks
```

端口声明：

```text
PortTiming {
  port_id
  timing_tier
  timing_mode
  latency_budget
  max_jitter
  required_frequency_tier
  required_sync_domain
  packet_or_signal_type
}
```

当 `expected_ticks > latency_budget` 时，诊断台显示“延迟超预算”，并标出是算力不足、路径太长、桥接太多、刷新等待、队列拥塞还是频率域不兼容。

### 3.6.6 光时序与刷新窗口

光工艺族进入 T4 相干时序：

- F4 是光控制核 FSM、光GPU 光路传播、板级光总线和短距集群的时钟/锁相基准。
- 光RAM 默认使用随时间线性衰减 + 随读取次数乘法衰减。
- 粗制/稳定/调谐光RAM 的建议刷新周期分别约为 8-10 tick、16-20 tick、32-40 tick。

EDA 中应把这些做成可视化时序窗口：

```text
ram_refresh_window = ram_coherence_life × safety_factor
read_strength = stored_strength × age_factor × read_factor
phase_window = f(clock_tree_quality, phase_stability, path_length_delta, wavelength_load)
```

玩家调的是刷新周期、光路长度分组、相位调谐器位置和 F4 锁相质量；不是真实光场仿真。

### 3.6.7 量子/观测时序

量子微逻辑进入 T5 观测时序。它不模拟真实量子态，但要求玩家处理观测窗口：

```text
coherence_time
observation_window
post_selection_rounds
measurement_cooldown
collapse_risk
```

诊断重点：

- 任务窗口是否短于 `coherence_time`。
- 测量门是否在正确 `observation_window` 打开。
- 后选择轮数是否超出协处理器预算。
- 低温和屏蔽是否足以维持 T5 时序。

时序 DRC 检查：

- 同步域不同但没有桥接 FIFO、锁相器或采样边界。
- 时序等级不足：例如 T1 路径试图承载 T3 流水任务，或 T2 缓存网络试图承载 T4 相干光路。
- 流水级之间没有足够的缓存或刷新周期。
- `sync_distance_delta` 超过 `sync_tolerance`。
- 路径的 `expected_ticks` 超过端口 `latency_budget`。
- 光路路径长度差超过当前 `phase_window`。
- 光RAM 的 `refresh_period` 大于 `state_life_ticks`。
- 量子微逻辑的任务窗口超过 `coherence_time`。
- 传感器采样窗口短于输入信号稳定时间。

玩家可通过以下方式修复：

- 降低频率等级。
- 增加流水级或缓存页。
- 增加锁相器、频率桥、同步 FIFO。
- 缩短光路、增加相位调谐器或重新校准。
- 增加光RAM 刷新预算。
- 提升低温/屏蔽质量以延长量子相干窗口。

推荐把时序诊断显示成路径列表：

```text
path_id
source_port -> sink_port
domain
latency_ticks
required_window
actual_window
status: ok / marginal / failed
bottleneck
```

---

## 4. 隔离规则

不同物理环境的逻辑门必须隔离到不同芯片或不同受控区域。隔离规则是算力系统的硬约束，也是玩法来源。

### 4.1 裸片级隔离

同一裸片只能声明一个主工艺族：

```text
die_domain:
  electronic
  photonic
  quantum_photonic
  cryogenic_control
  storage
  bridge
```

允许少量辅助元件进入裸片，但不能承担主信息逻辑。例如光芯片里可以有热光调谐结构作为工艺/校准辅助，但不能把电信号作为主控制流；量子光学芯片可以有低温控制读数接口，但量子态处理区域必须与常温电逻辑隔离。

### 4.2 封装级桥接

跨工艺通信必须通过桥接封装：

| 桥接器 | 连接 | 代价 |
|---|---|---|
| ADC/DAC 边界片 | 电信号 ↔ 抽象数值页 | 延迟、量化噪声、发热 |
| 光电探测结 | 光信号 → 电/数值读出 | 暗电流、读出噪声、湮灭损耗 |
| 调制注入器 | 电/数值描述 → 光场编码 | 校准成本、相干能消耗 |
| 单光子测量阵列 | 量子态 → 经典结果 | 坍缩风险、采样次数成本 |
| 相干控制线 | 光/量子相位控制 | 低温或屏蔽要求、相位漂移 |

桥接器不只是“能接上”，还会改变预算：带宽、延迟、噪声、冷却、相干能和错误率都要显示在诊断台中。

### 4.3 主板级集成

主板不是单一电路板，而是“承载不同芯片的工程平面”：

- 电主板：适合早期接口、存储、传感器、普通自动化。
- 光背板：适合全光五件套、F4 同步、多芯片光互连。
- 低温载板：适合量子光学协处理器、SNSPD、误差校验阵列。
- 混合集成板：可以同时安装不同芯片，但必须有桥接器和热/相干隔离槽。

混合集成板的核心限制不是“能不能放”，而是“不同区域是否满足环境要求”。例如量子微逻辑区需要低温与屏蔽，光逻辑区需要相干能和光路校准，电逻辑区需要散热和供电稳定。

---

## 5. 芯片蓝图数据

`chip_logic_blueprint` 扩展为多工艺 EDA 蓝图：

```text
chip_role: control / matrix / pulse / io / storage / bridge / sampler / mixed_node
die_domain: electronic / photonic / quantum_photonic / cryogenic_control / storage / bridge
process_node: crude / fine / precision / coherent / single_photon / horizon
logic_family: transistor / photonic_gate / mzi_mesh / bistable_cavity / single_photon_gate
schematic_graph
layout_grid
layer_stack
microstructures
layout_nets
gate_counts
memory_blocks
interconnect_layers
timing_profile
timing_tier
timing_mode
clock_domains
timing_domains
pipeline_stages
sync_boundaries
cooling_interfaces
coherence_interfaces
io_ports
bridge_ports
frequency_tier
environment_requirements
drc_report
timing_report
simulation_report
score_cache
```

推荐数据结构：

```text
Microstructure {
  id
  type
  layer
  pos
  size
  rotation
  ports[]
  params
  quality
}

LayoutNet {
  id
  medium: electric / optical / coherent_control / coolant / cryogenic / quantum
  layer
  path[]
  endpoints[]
  length
  loss_estimate
}

LayoutZone {
  id
  domain
  bounds
  environment_requirements
  isolation_rating
}
```

`hardware_blueprint` 扩展为板级/机柜级集成蓝图：

```text
blueprint_type: motherboard / optical_backplane / cryogenic_carrier / mixed_compute_node / rack
grid_size
zones
slots
ports
bus_layers
cooling_pipes
coherent_energy_lines
frequency_domains
environment_domains
bridge_map
score_cache
```

---

## 6. 编辑器工具与交互

为了做出“设计软件”的感觉，芯片蓝图台应提供明确工具，而不是只用 JEI 配方。

基础工具：

- 选择、移动、旋转、镜像。
- 放置微结构。
- 画线：电互连、光波导、相干控制线、冷却管线。
- 放置端口：引脚、焊盘、光栅耦合器、低温接口。
- 区域工具：声明电区、光区、量子区、冷却区、keepout 区。
- 层面板：切换 active、metal、optical、cooling、shield、ports 等层。
- 规则检查按钮：运行 DRC。
- 抽象仿真按钮：生成性能画像。
- 生成掩膜按钮：把版图导出为 `lithography_mask_set` 或 `chip_logic_blueprint`。

高级工具：

- 总线自动布线：只对电互连和规则化光波导开放。
- MZI 阵列生成器：输入 N×N、拓扑（Clements/Reck）、目标相位精度。
- SRAM/光RAM 阵列生成器：输入容量、刷新周期、端口数。
- 冷却管线填充：按热图自动建议微流道。
- 版图模板：保存/复用宏单元，例如 4-bit ALU、8×8 MZI tile、双稳态寄存器组。

### 6.1 GUI 分区

建议芯片蓝图台 GUI 至少有：

```text
左侧：元件库 / 层列表 / 工艺规则
中间：版图画布
右侧：属性面板 / DRC 错误 / 性能预览
底部：坐标、缩放、当前层、当前工具、材料消耗
```

MVP 可以先用有限格点、固定层数和少量宏单元做出编辑闭环；后续再扩展自由曲线波导、模板库和自动布线。

---

## 7. 元件库分层

### 7.1 电逻辑元件

电逻辑门用于早期接口、传感器、存储页、低速自动化和兼容性边界：

- `electronic_logic_gate`
- `electronic_register_cell`
- `electronic_sram_block`
- `electronic_io_controller`
- `electronic_bridge_controller`

这些元件可以存在，但不再作为第 6 阶段主计算路线的 CPU/GPU/NPU。它们负责边界、低速控制和制造前置。

### 7.2 光逻辑元件

光逻辑是中游主计算路线：

- `photonic_logic_gate`
- `kamaen_bistable_cell`
- `mzi_modulator`
- `silicon_photonic_waveguide`
- `photonic_ram_unit`
- `single_freq_laser_source`

光逻辑门必须位于 `die_domain=photonic` 的芯片中。光GPU、光控制核、光脉冲处理器、光RAM 的细节以全光计算文档为准。

### 7.3 量子微逻辑元件

量子微逻辑是后期协处理路线：

- `single_photon_source`
- `snspd_detector`
- `quantum_phase_gate`
- `entanglement_coupler_plate`
- `quantum_error_correction_plate`
- `wavefunction_cache_page`

这些元件不输出稳定的通用 `control_ops`，而是输出 `sampling_ops`、`blueprint_search_ops`、`coherence_analysis_ops` 和 `synthesis_curve_ops`。它们适合处理费曼蓝图、底噪解释、中观合成曲线和视界前置运算。

### 7.4 存储与冷却元件

存储和冷却应作为 EDA 的可放置资源，而不是隐藏属性：

- 电存储：`memory_page`、`electronic_sram_block`
- 光存储：`photonic_ram_unit`、循环腔缓存
- 量子缓存：`wavefunction_cache_page`
- 视界存储：`holographic_membrane`
- 冷却：`thermal_interface_plate`、`coolant_pipe_port`、`cryo_control_plate`、`horizon_cooling_tower`

存储元件决定 State/Parameter/Activation 能停留多久；冷却元件决定高密度芯片是否稳定运行。

---

## 8. 制程、掩膜与流片

制程不只影响“等级”，还决定可用元件库。

| 制程 | 解锁 | 环境要求 |
|---|---|---|
| 粗制掺杂 | PN 结、基础电逻辑、低速存储 | 常温、FE、普通散热 |
| 精密光刻 | 细互连、探测结、相位片 | 洁净度、对准、相干能辅助 |
| 相干光路 | 光逻辑门、MZI、光RAM | F4、单频源、光路校准 |
| 单光子制程 | 单光子源、SNSPD、测量阵列 | 低温、屏蔽、相干控制 |
| 视界/全息制程 | 全息膜、熵流接口 | III 型框架、视界约束、熵流控制 |

不同制程可以通过板级集成协作，但不能在裸片中无代价混合。升级的重点从“堆更高等级 CPU”转为“选择合适工艺族，并处理接口与环境成本”。

### 8.1 掩膜链

版图不会直接变成芯片。它先生成掩膜与制程任务：

```text
chip_layout
-> DRC 合格
-> lithography_mask_set
-> wafer_process_job
-> bare_die
-> packaged_logic_chip
```

掩膜集合可以包含多个层：

- active mask：定义 PN 结、沟道、非线性腔。
- metal mask：定义电互连。
- optical mask：定义波导、MZI、耦合器。
- via mask：定义层间连接。
- cooling mask：定义微流道或热通孔。
- shield mask：定义屏蔽层和隔离沟槽。

掩膜质量影响对准误差和良率。玩家可以复用一套掩膜批量制造同一芯片；掩膜磨损或污染会逐渐降低良率。

### 8.2 流片结果

一次流片输出若干裸片，质量不是完全随机，而由工艺评分决定：

```text
die_quality =
  layout_rule_score
  × process_precision
  × material_purity
  × alignment_quality
  × cooling_design_margin
  × environment_isolation
  / complexity_penalty
```

失败不应该只给“废品”。可分为：

- 完全失败：回收晶片碎片。
- 降频可用：频率上限下降。
- 漏光/串扰：光路损耗和错误率上升。
- 热缺陷：需要更强冷却。
- 端口缺陷：部分 I/O 不可用。

这让玩家可以把低良率芯片用于低级设备，高良率芯片用于核心算力节点。

---

## 9. 评分画像

芯片和算力节点输出一组画像：

```text
control_ops
matrix_ops
pulse_ops
route_ops
io_bandwidth
memory_bandwidth
state_life_ticks
sampling_ops
bridge_latency
logic_error_rate
coherence_draw
thermal_output
cooling_required
yield_score
environment_fit
```

诊断台必须能解释这些数值来自哪里：

- 门数量不足。
- 存储元件寿命不够。
- 光路相干能不足。
- 量子区冷却不足。
- 桥接器成为瓶颈。
- 制程良率低。
- 不同环境域隔离失败。

### 9.1 版图评分拆项

```text
layout_area
device_density
wire_length
waveguide_loss
phase_mismatch
thermal_hotspot_score
cooling_coverage
coherence_path_length
port_escape_score
bridge_count
isolation_rating
manufacturing_complexity
```

这些拆项用于解释性能，不必全部展示在普通 tooltip 中；诊断台高级页可以展开。

---

## 10. 与现有全光路线的关系

本文不推翻全光五件套，而是把它放进更大的 EDA 系统中：

- 第 4 阶段：解锁掺杂、光刻、探测结、相位片、电/光基础元件。
- 第 5 阶段：解锁 EDA 蓝图、封装、板级集成、存储和宏观信息中心。
- 第 6 阶段：以光逻辑为主计算路线，完成光控制核、光GPU、光脉冲处理器、光协处理器、光RAM。
- 第 7-8 阶段：引入单光子源、SNSPD、量子微逻辑和低温载板，作为量子光学协处理器的 EDA 元件库。
- 第 9-10 阶段：视界存储、黑洞运算和全息膜成为特殊高阶存储/运算域。

因此，旧的“电气 CPU/GPU/NPU 当前路线”不恢复；电逻辑只是 EDA 元件库的一支，承担早期、接口、桥接和兼容任务。中游主计算仍由光工艺族承担，后期协处理由量子光学工艺族承担。

---

## 11. MVP 实现顺序

1. 实现 `chip_logic_blueprint` 的 `die_domain`、`logic_family`、`environment_requirements`、`microstructures`、`layout_nets` 字段。
2. 做一个有限格点版图编辑器：放置宏单元、画线、放端口、运行 DRC。
3. 把字典中的旧 CPU/GPU/NPU 条目改为 EDA 元件、芯片封装和桥接模块。
4. 先开放电逻辑 + 基础光路的微结构：电逻辑门、寄存器、SRAM、波导、MZI、光电探测结、冷却管线。
5. 第 6 阶段实现光工艺族的最小集合：光逻辑门、双稳态晶胞、MZI、光RAM、单频源。
6. 诊断台优先显示 `environment_fit`、`bridge_latency`、`logic_error_rate`、`coherence_draw`、`cooling_required`、`drc_report`。
7. 量子微逻辑先作为第 8 阶段协处理器内部评分元件，后续再开放完整低温版图。

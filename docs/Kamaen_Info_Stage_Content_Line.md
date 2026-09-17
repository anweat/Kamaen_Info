# Kamaen Info 阶段内容科技线

版本：v0.4 Content Line Draft  
状态：在既有科技树路线确定后，对每个阶段的物品、方块、合成/获取、参数、传感器、多方块玩法和实现边界进行落地补全；第 6 阶段已统一为全光五件套。  

本稿不替代 `Kamaen_Info_TechTree_Plan.md`。总案负责主线和世界观，本稿负责阶段玩法说明；逐物品/方块的固定字段开发表单见 `Kamaen_Info_Item_Block_Dictionary.md`。

## 1. 统一设计规则

### 1.1 命名与 id

- 注册 id 使用小写 snake_case。
- 可大量变体化的物品优先用一个 id + Data Component 区分，避免物品爆炸。
- 阶段性核心物品必须有清晰中文名、英文 id、获取方式和用途。
- 机器方块 id 以功能命名，不使用时代前缀，避免后续升级路线变窄。

### 1.2 必须进入 Data Component 的参数

这些参数需要随物品移动、进入配方、被 tooltip/JEI/EMI/框架读取，应统一做成 Data Component。

```text
kamaen_crystal_state:
  spectrum_signature
  axis_tensor
  stress
  noise_index
  coherence
  doping_concentration
  doping_type
  gate_axis
  cutoff_axis
  feedback_axis
  background_noise_response

infosignal:
  type
  value
  frequency_vector
  confidence
  timestamp
  source_id

noise_sample:
  noise_layer_id
  amplitude
  frequency
  entropy_density
  coherence
  dimension_key
  interpretation_tags

feynman_blueprint:
  external_lines
  vertices
  propagators
  conservation_constraints
  loop_order
  target_material

synthesis_parameter_curve:
  parameter_channels
  time_points
  confidence
  source_blueprint

kamaen_storage_page:
  page_type
  capacity
  used
  namespace
  payload_ref

dimension_parameter_matrix:
  terrain_base
  biome_weight
  physics_rule
  resource_spectrum
  entity_spawn
  noise_structure
  entropy_rate
```

### 1.3 只适合 BlockEntity 状态的参数

这些参数是机器运行态，不应写入物品。

```text
current_progress
energy_buffer
fluid_tank
running_recipe
cooldown_ticks
structure_dirty
cached_framework_profile
runtime_sensor_cache
route_table_cache
active_task_queue
last_tick_sample
```

### 1.4 多方块实现边界

所有多方块复用 `MultiblockFormer` 思路：

```text
structure scan only when dirty
-> module whitelist
-> position scoring
-> cached FrameworkProfile/MachineProfile
-> recipe/process runtime reads cache
```

运行时禁止每 tick 全结构扫描。爆炸室、合成框架、信息中心、视界框架和巨型节点框架都必须走缓存画像。

### 1.5 传感器复杂度分级

| 等级 | 用途 | 实现策略 | 是否需要模型调参 |
| --- | --- | --- | --- |
| S0 | 手持/单方块读数 | 右键或 GUI 查询 | 否 |
| S1 | 低频机器传感器 | 20-200 tick 周期 | 否 |
| S2 | 多源工艺传感器 | 进入框架画像，参与配方评分 | 可选 |
| S3 | 后期复杂传感器 | 批量预算、缓存、延迟输出 | 可选但有收益 |
| S4 | 维度/视界传感器 | 抽样、预算、任务队列 | 建议支持模型调参 |

## 2. 阶段一：圆石频谱初炼

### 2.1 阶段目标

玩家从圆石和水启动，获得基础粉末、频谱滤渣、均值化圆石和白噪晶种。这个阶段必须确定性可推进，随机只影响副产物数量和品质。

### 2.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 粗频谱碎屑 | `crude_spectrum_scrap` | 物品 | 手摇频谱筛处理圆石 | 早期中间产物，`spectrum_bias`、`purity` | 圆石 | P0 |
| 粗频谱泥浆 | `crude_spectrum_slurry` | 物品/流体候选 | 圆石 + 水，经分馏塔 | 分馏输入，`frequency_integral`、`contamination` | 水、圆石 | P0 |
| 频谱滤渣 | `spectrum_slag` | 物品 | 泥浆分馏副产 | 白噪晶种前置，`residue_spectrum`、`heat_response` | 无 | P0 |
| 均值化圆石 | `whitened_cobblestone` | 方块/物品 | 频谱滤渣 + 热噪坩埚 | 白噪化基底，`noise_mean`、`mean_deviation` | 圆石 | P0 |
| 白噪晶种 | `white_noise_seed` | 物品 | 均值化圆石 + 频谱滤渣 | 卡玛恩晶体起点，`white_noise_potential` | 无 | P0 |
| 基础粉末 | `spectrum_powder` | 物品 | 分馏副产 | 用 `powder_type` 区分 iron/coal/copper/mineral，减少 id 数 | 铁、煤、铜、沙子 | P1 |
| 滤膜 | `spectrum_membrane` | 物品 | 纸/线/铁/玻璃板等合成 | `membrane_type` 区分 carbon/metal/silica，影响副产物权重 | 纸、线、铁、玻璃 | P1 |
| 手摇频谱筛 | `hand_spectrum_sieve` | 方块/工具 | 木棍 + 铁锭 + 滤膜 | 右键积累工作量，保障空岛起步 | 工作台式交互 | P0 |
| 搅拌分馏塔 | `fractionating_tower` | 方块/多方块 | 铜/铁/玻璃 + 桶 + 搅拌轴 | 分馏主机器，记录污染和积分 | 水、圆石 | P0 |
| 热噪坩埚 | `thermal_noise_crucible` | 方块 | 熔炉 + 铁 + 频谱滤渣 | 加热滤渣，松动尖锐谱线 | 熔炉 | P0 |
| 初级分光镜 | `basic_spectroscope` | 工具/方块 | 玻璃 + 铁 + 滤渣 | 显示物品频谱、峰值偏差、白噪潜势 | 望远镜视觉类比 | P0 |

### 2.3 玩法与合成链

```text
圆石 + 手摇频谱筛 -> 粗频谱碎屑
圆石 + 水 + 分馏塔 -> 粗频谱泥浆
粗频谱泥浆 + 滤膜 -> 基础粉末 + 频谱滤渣
频谱滤渣 + 热噪坩埚 -> 均值化圆石
均值化圆石 + 频谱滤渣 -> 白噪晶种
```

连续处理同一类输入会提高 `contamination`。更换滤膜、混入不同石材或升级搅拌轴可降低污染。初版可以只做一个污染数值，后续再分成碳谱线、金属谱线、硅谱线。

### 2.4 传感器与实现

- 初级分光镜是 S0 传感器，只读取物品 Data Component 或根据注册名生成稳定 hash。
- 分馏塔是首个多方块，但 v0.1 建议先固定为 1 控制器 + 1 输入 + 1 输出 + 1 水槽的简化结构。
- 不需要独立线程。每 20 tick 结算一次分馏积分即可。

## 3. 阶段二：白噪结晶与力学合成

### 3.1 阶段目标

用模拟爆破和力学应力把白噪晶种塑造成第一代卡玛恩晶体，并让玩家理解向量、应力、轴向和晶体品质。

### 3.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 爆震粉 | `blast_powder` | 物品 | 煤粉/火药 + 频谱滤渣 | 爆破输入，`blast_strength`、`waveform_purity` | 火药 | P0 |
| 理想刚体板 | `ideal_rigid_plate` | 方块 | 铁块 + 均值化石材 | 反射冲击波，`reflectivity`、`rigidity` | 铁块、黑曜石 | P0 |
| 缓冲砂层 | `buffer_sand_layer` | 方块 | 沙子 + 均值化圆石 | 降低强度，提高容错 | 沙子 | P0 |
| 靶座 | `target_pedestal` | 方块 | 铁 + 石材 | 固定晶种，记录受击方向 | 展示框/盔甲架类比 | P0 |
| 粗卡玛恩晶体 | `raw_kamaen_crystal` | 物品 | 白噪晶种 + 爆破评分达标 | `axis_tensor`、`stress`、`noise_index` | 无 | P0 |
| 卡玛恩晶体碎片 | `kamaen_crystal_debris` | 物品 | 爆破失败 | 用 `debris_type` 区分裂纹/粉尘/残片 | 无 | P1 |
| 导波型卡玛恩晶体 | `waveguide_kamaen_crystal` | 物品 | X 轴爆破 | `axis_x` 强化，适合总线/导线 | 无 | P0 |
| 抗压型卡玛恩晶体 | `compression_kamaen_crystal` | 物品 | Y 轴爆破 | `axis_y` 强化，适合结构/压力 | 无 | P0 |
| 稳谱型卡玛恩晶体 | `stable_spectrum_kamaen_crystal` | 物品 | Z 轴爆破 | `axis_z` 强化，适合能量和相干 | 无 | P0 |
| 偏振卡玛恩晶体 | `polarized_kamaen_crystal` | 物品 | I 型框架压合 | `polarization_direction`、`tensor_alignment` | 无 | P1 |
| 应力记录片 | `stress_recording_plate` | 物品 | 铁板 + 晶体碎片 | 保存一次应力椭球快照 | 纸/地图类比 | P1 |
| 爆炸室控制器 | `explosion_chamber_controller` | 方块/多方块 | 铁、刚体板、红石 | 扫描爆炸室，计算 `VectorImpulse` | TNT 但不真实爆炸 | P0 |
| 应力传感器 | `stress_sensor` | 方块 | 偏振晶体 + 红石 | 读取 `stress_ellipsoid` | 红石比较器 | P1 |
| 轴向压头 | `axial_press_head` | 方块 | 活塞 + 铁块 + 晶体 | 提供 `pressure_vector` | 活塞 | P0 |
| I 型力学合成框架 | `tier1_mechanical_framework` | 方块/多方块 | 爆炸室升级 | 读取压力、应力、向量、晶格对齐 | 多方块 | P0 |

### 3.3 玩法与合成链

```text
白噪晶种 + 小型爆炸室 + 爆震粉 -> 粗卡玛恩晶体
粗卡玛恩晶体 + X 轴爆破 -> 导波型卡玛恩晶体
粗卡玛恩晶体 + Y 轴爆破 -> 抗压型卡玛恩晶体
粗卡玛恩晶体 + Z 轴爆破 -> 稳谱型卡玛恩晶体
粗卡玛恩晶体 + I 型框架 + 轴向压头 -> 偏振卡玛恩晶体
失败加工 -> 卡玛恩晶体碎片
```

爆炸室不调用 `Level.explode()`。控制器只根据结构画像计算：

```text
VectorImpulse:
  direction
  strength
  waveform_purity
  impulse_width

Score:
  direction_match
  energy_match
  waveform_purity
  stress_stability
```

### 3.4 传感器与实现

- 应力传感器是 S1/S2。单独使用时给大概数值，放入框架后提高评分精度。
- 爆炸室是早期最高风险多方块。初版建议固定 3x3x3，允许玩家只改变刚体板和缓冲砂位置。
- I 型框架先只支持 `pressure`、`impact_vector`、`stress_reading` 三个动态参数。
- 不需要独立线程。一次爆破是离散任务，计算量很小。

## 4. 阶段三：共振调谐与信息读取

### 4.1 阶段目标

把卡玛恩晶体从材料推进为信息介质。玩家学会读取原版方块状态、红石、简单机器状态，并将其封装为 `InfoSignal`。

### 4.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 调谐晶片 | `tuning_wafer` | 物品 | 卡玛恩晶体切片 | `frequency_response`、`lock_range` | 无 | P0 |
| 固有频谱样本 | `intrinsic_spectrum_sample` | 物品 | 频谱锁相器读取目标 | `sampled_signature`、`source_type` | 任意物品/方块 | P0 |
| 信息单元 | `information_unit` | 物品 | 探针台封装 | `InfoSignal` 的基础载体 | 红石、方块状态 | P0 |
| 共振催化晶体 | `resonance_catalyst_crystal` | 物品 | 晶体 + 频谱样本 | `resonance_type`、`efficiency` | 熔炉/作物/机器 | P0 |
| 频率总线 | `frequency_bus` | 方块/线缆 | 调谐晶片 + 红石 + 铁 | 传递 `InfoSignal` | 红石线类比 | P0 |
| 频率转红石模块 | `frequency_to_redstone_module` | 方块 | 信息单元 + 调谐晶片 | 输出 0-15 红石 | 比较器 | P1 |
| 晶体干涉仪 | `crystal_interferometer` | 方块 | 玻璃 + 偏振晶体 | 显示晶体张量、应力、频谱 | 讲台/制图台类比 | P0 |
| 频谱锁相器 | `spectrum_phaselocker` | 方块 | 调谐晶片 + 金 + 红石 | 生成固有频谱样本，写入晶体 | 无 | P0 |
| 卡玛恩探针台 | `kamaen_probe_station` | 方块 | 铁 + 比较器 + 调谐晶片 | 将可读对象转为 `InfoSignal` | 比较器、容器 | P0 |
| 调谐阵列 | `tuning_array` | 多方块 | 中心晶体 + 样本 + 透镜 | 提高共振效率 | 信标式摆放 | P1 |

### 4.3 可读边界

探针不反射读取任意内部字段，只读取：

```text
BlockState
redstone signal
public BlockEntity summary
item handler
fluid handler
FE storage
IKamaenReadable
```

初版 P0 只支持 `BlockState` 和红石强度。FE、流体、物品槽作为 P1/P2。

### 4.4 玩法引导

```text
晶体干涉仪读取晶体属性
-> 频谱锁相器读取熔炉/作物/红石信号
-> 生成固有频谱样本
-> 卡玛恩晶体锁相
-> 共振催化晶体加速对应机器
-> 探针台读取机器状态
-> 频率总线 + 红石模块形成闭环控制
```

### 4.5 传感器与实现

- 探针台是 S1 传感器，建议 20 tick 冷却。
- 频率总线初版可做成单方块相邻网络，不需要复杂线缆寻路。
- 固有频谱初版可用注册名 hash + 少量 BlockState 属性生成，后续再做属性加权。

## 5. 阶段四：掺杂晶片与光路工艺

### 5.1 阶段目标

引入掺杂、退火、光刻和刻蚀，把晶体科技转成光路工艺基础。电力只用于机器供能、泵浦和执行器，不作为信息传递媒介。

### 5.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 二代卡玛恩晶体 | `kamaen_crystal_t2` | 物品 | 稳谱晶体 + 电气级精炼 | 允许掺杂与门控参数 | 无 | P0 |
| 掺杂剂 | `kamaen_dopant` | 物品 | 粉末 + 滤渣 + 化学处理 | `dopant_type` 区分 donor/acceptor | 红石、石英、金属粉 | P0 |
| 卡玛恩晶片 | `kamaen_wafer` | 物品 | 稳谱晶体切片 | `wafer_type` 区分 blank/n_type/p_type/defect | 无 | P0 |
| 卡玛恩 PN 结 | `kamaen_pn_junction` | 物品 | N/P 晶片 + 退火 | `junction_barrier`、`threshold_voltage` | 无 | P0 |
| 掺杂导波晶片 | `doped_waveguide_wafer` | 物品 | N/P 晶片 + 退火 | `waveguide_axis`、`loss`、`threshold` | 无 | P0 |
| 阈值滤波片 | `kamaen_threshold_filter` | 物品 | 掺杂晶片 + 光刻 + 刻蚀 | `threshold_axis`、`filter_band` | 比较器类比 | P0 |
| 卡玛恩探测结 | `kamaen_detector_junction` | 物品 | N/P 晶片 + 稳谱镀层 | `responsivity`、`noise` | 无 | P0 |
| 相位调谐片 | `phase_tuning_chip` | 物品 | 掺杂晶片 + 光刻 + 刻蚀 | `phase_axis`、`tuning_precision` | 无 | P0 |
| 光刻掩膜 | `lithography_mask` | 物品 | 玻璃板 + 铁板 + 刻写 | `exposure_pattern`、`circuit_layout` | 旗帜图案类比 | P1 |
| 晶体导波线 | `crystal_waveguide_line` | 物品 | 金 + 导波晶片碎片 | `line_density`、`optical_loss` | 红石/金线视觉类比 | P1 |
| 卡玛恩晶振 | `kamaen_oscillator` | 物品 | 石英/稳谱晶体 + 红石 | `frequency_tier` 区分 F1/F2/F3 | 石英、红石 | P0/P1/P2 |
| 相干能缓存 | `coherent_energy_buffer` | 方块/物品 | FE + 稳谱晶体 + 稳压器 | `coherent_energy`、`noise_floor` | FE | P0 |
| 相干能稳压器 | `coherent_energy_regulator` | 方块 | FE 缓存 + 调谐晶片 | 将 FE 整理为低噪工艺能源 | FE | P0 |
| 离子注入器 | `ion_implanter` | 方块 | 铁块 + 稳谱晶体 + 红石 | `doping_axis`、`concentration` | 无 | P0 |
| 晶格退火炉 | `lattice_annealing_furnace` | 方块 | 熔炉升级 + 稳谱晶体 | `temperature_curve`、`defect_repair` | 熔炉/高炉 | P0 |
| 光刻投影器 | `lithography_projector` | 方块 | 玻璃 + F2 晶振 | `exposure_pattern`、`alignment_precision` | 无 | P0 |
| 刻蚀槽 | `etching_tank` | 方块 | 桶 + 化学流体 + 晶体 | `etch_depth`、`pattern_fidelity` | 炼药锅类比 | P0 |
| II 型光路工艺框架 | `tier2_optical_process_framework` | 多方块 | 注入/退火/光刻/刻蚀模块组合 | 统一光路工艺画像 | 多方块 | P1 |
| 信息诊断台 | `info_diagnostic_station` | 方块 | 探针 + F2 晶振 + 调谐晶片 | 输出信号与结构诊断画像 | 无 | P1 |

### 5.3 玩法链

```text
稳谱晶体 -> 卡玛恩晶片(blank)
卡玛恩晶片 + 施主掺杂剂 + 离子注入 -> N 型晶片
卡玛恩晶片 + 受主掺杂剂 + 离子注入 -> P 型晶片
N/P 晶片 + 退火 -> 掺杂导波晶片 / 阈值滤波片
掺杂晶片 + 光刻掩膜 + 刻蚀 -> 波导毛坯 / 探测结 / 相位调谐片
调谐晶片 + 信号缓存片 + F2 晶振 -> 共振信号缓存器
```

### 5.4 传感器与实现

- 初版只开放 X 轴掺杂，Y/Z 轴后移，降低教学压力。
- 掺杂浓度、晶片类型、晶振频率都进入 Data Component。
- II 型框架不要一开始就联动所有机器。先让独立机器跑通，框架作为集中控制和评分升级。
- 不需要独立线程。光刻/退火/刻蚀都是多 tick 配方。

## 6. 阶段五：共振信息自动化与宏观信息中心

### 6.1 阶段目标

让玩家从读取单个机器状态推进到组织传感器、频率总线、信号缓存和底噪数据库，开始读取世界背景信息场。本阶段不提供电气 CPU/GPU/NPU；信息通过晶体共振、InfoSignal、频率总线、光路前置组件和红石边界触发传递。

### 6.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 共振信号缓存器 | `resonant_signal_cache` | 物品/方块 | 调谐晶片 + 信号缓存片 + F2 晶振 | `cache_life`、`signal_quality` | 无 | P0 |
| 信号缓存片 | `signal_cache_plate` | 物品 | 稳谱晶体 + 导波线 | `page_type` 区分 sensor/state/index | 无 | P1 |
| 频率路由片 | `frequency_route_plate` | 物品 | 信号缓存片 + 调谐晶片 | 记录频道、过滤规则和路由标签 | 无 | P1 |
| 世界底噪样本 | `world_noise_sample` | 物品 | 底噪谱仪采样 | `noise_sample` Data Component | 维度/群系 | P0 |
| 热噪声谱片 | `thermal_noise_plate` | 物品 | 底噪样本过滤 | 热噪层专用样本 | 无 | P0 |
| 背景辐射谱片 | `radiation_noise_plate` | 物品 | 底噪样本过滤 | 辐射层样本 | 无 | P1 |
| 量子涨落片 | `quantum_fluctuation_plate` | 物品 | 底噪样本过滤 | 量子层样本 | 无 | P1 |
| 区块熵流记录 | `chunk_entropy_record` | 物品 | 熵流计读取区块 | `entropy_flow_rate`、`chunk_pos` | 区块更新 | P1 |
| 底噪数据库 | `noise_database` | 方块 | 样本 x16 + 信息核心 | 存储样本和解释标签 | 书架/讲台类比 | P0 |
| 宏观信息索引核心 | `macro_info_index_core` | 方块/物品 | 信息中心控制器 + 探针 + F2 | 路由表、传感器绑定 | 无 | P0 |
| 底噪谱仪 | `noise_spectrometer` | 方块 | 稳谱晶体 + F2 晶振 | 采样底噪层 | 天气/时间/维度 | P0 |
| 热力学背景天线 | `thermodynamic_antenna` | 多方块附属 | 导波晶体 + 金属结构 | 扩大采样范围 | 避雷针视觉类比 | P1 |
| 熵流计 | `entropy_flow_meter` | 方块 | 探针 + 稳谱晶体 | 读取区块熵流 | 区块更新 | P1 |
| 信息中心控制器 | `info_center_controller` | 多方块 | 探针 + 数据库 + 频率总线 + 信号缓存 | 路由、采样、数据库查询 | 多方块 | P0 |

### 6.3 底噪层落地

第一版只需要三层稳定可用：

```text
ThermalNoiseLayer
RadiationNoiseLayer
QuantumNoiseLayer
```

其余层先注册占位：

```text
BlockUpdateNoiseLayer
EntityBehaviorLayer
RedstoneNoiseLayer
BiomeNoiseLayer
VoidNoiseLayer
StringResidueLayer
```

### 6.4 传感器与实现

- 底噪谱仪是 S2/S3。每 200 tick 采样一次。
- 同一维度同一层采样结果缓存 200 tick，多个谱仪读缓存，避免重复计算。
- 不建议独立线程。放在 `ServerLevel` tick 末尾批量结算。
- 信息中心控制器初版只做静态路由，不做模型训练。

## 7. 阶段六：全光计算

### 7.1 阶段目标

将中游计算推进到全光形态。第 5 阶段的频率总线和信号缓存只负责组织信息；第 6 阶段开始由五件套全光系统（光控制核、光GPU、光脉冲处理器、光协处理器、光RAM）执行模型计算。FE 仍用于生产机器供能，不进入计算域。完整规范见 `docs/Kamaen_Info_Optical_Computing_Design.md`。

### 7.2 核心物品与方块

**新增基元组件**：

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| 卡玛恩非线性介质 | `kamaen_nonlinear_medium` | 物品 | 导波晶体 + 稳谱晶体 + 应力调谐腔 | `chi2_coefficient`（χ⁽²⁾ 系数）、`nonlinear_bandwidth`；由晶体应力张量决定 χ⁽²⁾ | P0 |
| 光逻辑门 | `photonic_logic_gate` | 物品 | 非线性介质 + 波导 + 分束器 | `gate_type`（AND/OR/NOT/NAND/XOR）、`threshold_stability`；品级影响随机翻转率 | P0 |
| 卡玛恩双稳态晶胞 | `kamaen_bistable_cell` | 物品 | 两个耦合卡玛恩共振腔 | `bistable_margin`、`hold_power`；光学 SR 触发器 | P0 |

**全光五件套（计算单元）**：

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| 光控制核 | `photonic_control_core` | 物品/方块 | 双稳态晶胞 x16 + 光逻辑门 x32 + 波导 x8 + 相位调谐器 x4 + 激光源 x2 + F4 晶振 | `fsm_state_depth`、`logic_error_rate`、`control_ops`；全光 FSM，承担控制、路由、脚本、调度和 I/O | P0 |
| 光脉冲处理器 | `photonic_pulse_processor` | 物品/方块 | 非线性介质 x8 + 波导 x8 + 相位调谐器 x4 + 激光源 x2 + F3 晶振 | `pulse_threshold_drift`、`sparse_ops`、`nonlinear_ops`；饱和吸收体做稀疏激活 | P0 |
| 光RAM | `photonic_ram_unit` | 物品/方块 | 双稳态晶胞 x4 + 波导 x4 + 非线性介质 x2 + 激光源 + F2 晶振 | `ram_coherence_life`（tick）、`loop_count`；受激辐射循环腔，有寿命上限 | P0 |
| 光GPU 单元 | `photonic_gpu_unit` | 物品/方块 | 波导 x8 + MZI x16 + 相位调谐器 x16 + 非线性介质 x8 + 激光源 x2 + F4 晶振 | `photonic_throughput`、`mzi_grid_size`、`weight_switch_cost`；不变 | P0 |
| 光协处理器 | `photonic_coprocessor` | 物品/方块 | 单频激光源 + 光路由交换机 + F4 晶振 | `data_move_ops`、`prep_ops`、`optical_bandwidth`；不变 | P0 |

**沿用组件（工艺不变，部分升级）**：

| 中文名 | id | 类型 | 升级说明 | 优先级 |
| --- | --- | --- | --- | --- |
| 硅光波导 | `silicon_photonic_waveguide` | 物品 | 不变 | P0 |
| 马赫-曾德尔调制器 | `mzi_modulator` | 物品 | 不变 | P0 |
| 相位调谐器 | `phase_tuner` | 物品 | 升级为声光效应版（光信号控制，无电信号） | P0 |
| 单频激光源 | `single_freq_laser_source` | 物品/方块 | 不变；现在泵浦整个全光系统 | P0 |
| F4 光频晶振 | `kamaen_oscillator (F4)` | 物品 | 不变；现在也是光控制核 FSM 时钟基准 | P0 |
| 光路校准令牌 | `calibration_token` | 物品 | 不变 | P1 |

**资源**：

| 中文名 | id | 获取 | 备注 | 优先级 |
| --- | --- | --- | --- | --- |
| 相干能 | `coherent_energy` | 稳谱晶体 + 单频激光源 持续产生 | 独立资源条；不是 FE 子类；消耗扩展为逻辑层 + 矩阵层两部分 | P0 |

**机器与框架**：

| 中文名 | id | 类型 | 作用 | 优先级 |
| --- | --- | --- | --- | --- |
| 卡玛恩非线性介质制备台 | `kamaen_nonlinear_medium_station` | 方块 | 导波晶体 + 稳谱晶体 → 共掺杂非线性腔 | P0 |
| 光逻辑门封装台 | `photonic_gate_assembly_station` | 方块 | 非线性介质 + 波导 + 分束器 → 光逻辑门 | P0 |
| 双稳态晶胞组装台 | `bistable_cell_assembly_station` | 方块 | 卡玛恩共振腔 x2 → 双稳态晶胞 | P0 |
| 光控制核封装台 | `photonic_control_core_assembly` | 方块/多方块 | 晶胞 + 逻辑门 + 时钟 → 光控制核 | P0 |
| 光脉冲处理器封装台 | `photonic_pulse_processor_assembly` | 方块 | 饱和吸收体腔 + 时分波导 → 脉冲处理器 | P0 |
| 光RAM 封装台 | `photonic_ram_assembly` | 方块 | 循环腔 + 部分反射镜 → 光RAM | P0 |
| 波导刻蚀台 | `photonic_waveguide_etching_station` | 方块 | 毛坯 → 波导芯片（沿用）| P0 |
| MZI 编织台 | `mzi_weaving_station` | 方块 | 波导 + 调制器 → MZI 网格（沿用）| P0 |
| 激光泵浦塔 | `laser_pump_tower` | 多方块 | 全系统相干能来源（沿用）| P0 |
| 光路校准台 | `photonic_calibration_station` | 方块 | 重写 MZI 权重；60 秒/次（沿用）| P1 |
| 诊断台升级模块 | — | 升级 | 新增 `logic_error_rate`、`bistable_cell_health`、`pulse_threshold_drift`、`ram_coherence_life`、`feynman_mode` | P1 |

### 7.3 相干能模型（扩展版）

```text
coherent_cost =
  logic_cost × gate_count × crystal_quality_factor        ← 新增：光逻辑层
  + matrix_cost × mzi_count × temperature_factor × wavelength_count × duty   ← 保留：光矩阵层
```

| 失稳区间 | 光逻辑层后果 | 光矩阵层后果 |
|---------|------------|------------|
| 70–100% | 正常 | 正常 |
| 50–70% | 光控制核偶发位翻转，调度偶发异常 | 轻微数值噪声 |
| 30–50% | 逻辑错误率显著上升 | 推理精度下降，结果标记 invalid |
| < 30% | 全光系统进入光路崩溃，所有组件暂停 | 同左 |

### 7.4 可视化方案

- 光纤亮度对应数据率；颜色按频段（F2 绿、F3 蓝、F4 紫）
- 光GPU：表面渲染 MZI 干涉条纹（不变）
- **光控制核**：顶面双稳态晶胞亮点阵列（实时 FSM 状态）；逻辑门激活时侧面微弱蓝光脉冲
- **光脉冲处理器**：强脉冲→橙色粒子通过；弱脉冲被湮灭→暗橙粒子侧面逸散
- **光RAM**：循环腔内光子以螺旋线显示，每次读取螺旋线变细
- **费曼描述模式**（诊断台开关）：各组件浮现简化费曼图标注，为第 7 阶段预习
- 失稳：光纤闪烁（70%–60%）→ 暗红 + 警告粒子（< 30%）
- 服务端只算抽象数值；客户端只渲染，不做光物理模拟

### 7.5 传感器与实现

- 光控制核、光脉冲处理器、光RAM 内部逻辑为纯抽象数值（逻辑错误率、腔体寿命、阈值漂移），无实际光物理模拟
- 双稳态晶胞品级通过 `crystal_quality_factor` 影响逻辑层相干能消耗和错误率；这个值来自对应卡玛恩晶体的应力张量品质
- 光RAM 的腔体寿命（tick）在 BlockEntity 中独立计时；超时后自动清除（状态丢失警告）
- 诊断台费曼描述模式：纯客户端渲染，不影响服务端逻辑

### 7.6 毕业门槛

1. 至少 1 台光控制核持续运行 ≥ 10 分钟，逻辑错误率 < 1%
2. 至少 1 台光GPU 与光控制核协作完成一次矩阵推理
3. 至少 1 台光脉冲处理器处理光GPU 输出并正确输出激活值
4. 至少 1 台光RAM 维持 State 存储 ≥ 20 tick 不丢失
5. 相干能产生与消耗达到稳态平衡，持续 5 分钟无失稳
6. 诊断台打开费曼描述模式，确认至少一个组件显示费曼图标注

## 8. 阶段七：凝聚态材料与费曼过程合成

### 8.1 阶段目标

把底噪样本、卡玛恩晶体和低温相干场结合，制造准粒子材料、传播子片、费曼蓝图和第一批凝聚态材料。本阶段同时产出**单光子源**（量子点 / 参量下转换）和**超导纳米线单光子探测器（SNSPD）**——作为第 9 章量子光学协处理器的前置材料；也可反向升级第 7 章光GPU 的探测器（提升信噪比，降低相干能消耗）。

### 8.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 准粒子晶格 | `quasiparticle_lattice` | 物品 | 底噪样本 + 晶体 + 低温凝聚腔 | `quasiparticle_type`、`energy_gap` | 无 | P0 |
| 传播子片 | `propagator_plate` | 物品 | 准粒子捕获器 | `propagator_type` 区分 phonon/electron/exciton/spinwave | 无 | P0/P1 |
| 库珀对种子 | `cooper_pair_seed` | 物品 | 电子传播子 x2 + 低温场 | `pairing_gap`、`critical_temperature` | 无 | P1 |
| 费曼顶点片 | `feynman_vertex_plate` | 物品 | 传播子 + 相互作用条件 | `vertex_type`、`coupling_constant` | 无 | P0 |
| 费曼过程蓝图 | `feynman_process_blueprint` | 物品 | 编译台组合外线/顶点/约束 | `feynman_blueprint` Data Component | 锻造模板类比 | P0 |
| 超导卡玛恩环 | `superconducting_kamaen_ring` | 物品/方块 | 库珀对 + 低温场 + III 型框架 | `critical_current`、`coherence_length` | 无 | P0 |
| 拓扑绝缘晶体 | `topological_insulator_crystal` | 物品 | 自旋波过程 + 拓扑相变炉 | `topology_id`、`edge_state_count` | 无 | P1 |
| 相变记忆晶体 | `phase_change_memory_crystal` | 物品 | 拓扑晶体 + 激子过程 | `phase_state`、`endurance` | 红石锁存类比 | P1 |
| 准粒子滤波器 | `quasiparticle_filter` | 方块/物品 | 传播子 + 拓扑晶体 | `pass_band`、`filter_q_factor` | 无 | P2 |
| 隧穿链路器 | `tunnel_linker` | 方块 | 电子/自旋传播子 + III 型框架 | 合并隧穿串联器和 4 维电路桥 | 远程红石类比 | P1 |
| 低温凝聚腔 | `cryo_condensation_chamber` | 多方块 | 密封结构 + 相干能 | 提供低温和相干保持 | 冰、蓝冰 | P0 |
| 准粒子捕获器 | `quasiparticle_detector` | 方块/传感器 | 低温腔升级 | 捕获电子/声子等传播子 | 无 | P0 |
| 费曼过程编译台 | `feynman_compiler` | 方块 | 调谐台升级 | 编译蓝图 | 锻造台 GUI 类比 | P0 |
| 拓扑相变炉 | `topology_furnace` | 方块/多方块 | 退火炉升级 | 场强扫描和相变 | 高炉类比 | P1 |
| III 型视界框架雏形 | `horizon_framework_mk1` | 多方块 | 凝聚态模块组合 | 提供观测、低温、相干场 | 多方块 | P0 |
| 单光子源 | `single_photon_source` | 物品/方块 | 量子点 / 参量下转换 | 第 9 阶段量子光学前置；可升级第 7 阶段光GPU 探测器 | 无 | P0 |
| SNSPD 探测器 | `snspd_detector` | 物品/方块 | 超导纳米线 + 低温腔 | 单光子级高信噪比探测；同上 | 无 | P1 |

### 8.3 玩法链

```text
底噪样本 + 卡玛恩晶体 -> 准粒子响应测试
准粒子响应 + 捕获器 -> 传播子片
传播子片 + 顶点片 + 守恒约束 -> 费曼过程蓝图
费曼过程蓝图 + 低温凝聚腔/III 型框架 -> 凝聚态材料
```

### 8.4 传感器与实现

- 低温传感器、准粒子捕获器、隧穿链路器属于 S3。
- 费曼蓝图校验不需要真实物理模拟，只校验枚举约束：电荷、频率、拓扑数、晶格对称性。
- 隧穿链路跨 chunk 是风险点。用维度级注册表保存成对链接，chunk unload 时清理。
- 模型调参是可选收益：自动调节温度、场强、冷却速率。主线保留固定窗口。
- 模型调参的密集矩阵推理可调用第 7 阶段光GPU 加速。

## 9. 阶段八：量子光学协处理器与中观合成

### 9.1 阶段目标

量子光学协处理器不做万能计算，只把费曼蓝图和材料状态转换为可执行的合成参数曲线。**物理路线**：单光子 + 线性光路 + SNSPD 后选择测量（玻色采样路线）；与第 7 阶段经典光计算形成「经典光 → 量子光」的连续阶梯。

### 9.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 量子光学协处理核心 | `quantum_optical_coprocessor_core`（原 `quantum_coprocessor_core`） | 物品 | 超导环 + 拓扑晶体 + 单光子源 + F4 晶振 | `qubit_count`、`coherence_time` | 无 | P0 |
| 低温控制片 | `cryo_control_plate` | 物品 | 低温腔 + 稳谱晶体 | `target_temperature`、`stability` | 无 | P0 |
| 相干控制线 | `coherent_control_line` | 物品/方块 | 超导环 + 互连线 | `phase_drift`、`attenuation` | 红石线类比 | P1 |
| 纠缠耦合片 | `entanglement_coupler_plate` | 物品 | 拓扑晶体 + 传播子 | `entanglement_fidelity` | 无 | P1 |
| 波函数缓存页 | `wavefunction_cache_page` | 物品 | 内存页 + 量子涨落片 | `collapse_risk`、`cache_valid_ticks` | 书与笔类比 | P1 |
| 量子误差校验片 | `quantum_error_correction_plate` | 物品 | 量子涨落片 + 超导环 | `code_distance`、`logical_error_rate` | 无 | P1 |
| 准粒子路径样本 | `quasiparticle_path_sample` | 物品 | 捕获器连续监控 | `transition_probability` | 无 | P2 |
| 合成参数曲线 | `synthesis_parameter_curve` | 物品 | 协处理器任务输出 | `synthesis_parameter_curve` Data Component | 唱片数据类比 | P0 |
| 中观合成协议 | `meso_synthesis_protocol` | 物品 | 曲线 + III 型框架 + 信息中心 | 参数曲线封装 | 无 | P2 |
| 量子光学协处理器 | `quantum_optical_coprocessor`（原 `quantum_coprocessor`） | 多方块 | 核心 + 低温控制 + 误差校验 + SNSPD x4 | 蓝图 -> 稳定窗口 -> 曲线 | 多方块 | P0 |
| 低温控制柜 | `cryo_control_cabinet` | 方块 | 低温控制片 + 相干能 | 维持温度 | 无 | P0 |
| 波函数采样仪 | `wavefunction_sampler` | 方块/传感器 | 协处理器附属 | 读取 `collapse_risk` | 无 | P1 |
| 误差校验阵列 | `error_correction_array` | 多方块模块 | 校验片重复摆放 | 方块数量和位置决定 `code_distance` | 多方块 | P1 |
| 中观合成调度器 | `meso_synthesis_scheduler` | 方块 | 信息中心升级 | 曲线分发给框架控制端口 | 无 | P0 |

### 9.3 实现边界

量子光学协处理器提交任务后分步结算：

```text
submit task
-> every 10-20 tick compute one abstract step (single-photon boson sampling)
-> after 100-400 tick output synthesis_parameter_curve
-> scheduler feeds III framework dynamic_control_ports
```

禁止真实量子模拟，禁止独立线程常驻计算。可以用任务队列和冷却表现复杂度。物理路线设定为单光子 + 线性光路 + SNSPD 后选择测量；不是通用量子计算机。

### 9.4 模型调参

这是模型系统第一次显著有用的阶段，但不是主线强制：

- 主线：固定参数曲线即可完成材料。
- 进阶：模型读取低温、坍缩风险、准粒子路径，自动微调曲线。
- 实现：预留 `model_output` -> `framework_control_port`，不在 v0.9 强制实现训练。

## 10. 阶段九：戈古尔斯弦与人造视界框架

### 10.1 阶段目标

将底噪数据库、凝聚态约束材料、量子曲线和戈古尔斯弦残迹合并，制造有限多方块内的可控人造视界。

### 10.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 戈古尔斯弦残迹 | `gorguth_string_residue` | 物品 | 虚空残响 + 底噪数据库 + 稳谱晶体 | `anchor_potential`、`decay_rate` | 虚空/末地 | P0 |
| 戈古尔斯弦 | `gorguth_string` | 物品 | 残迹 + 弦锚定器 + 相干能 | `stability`、`boundary_coupling` | 无 | P0 |
| 视界约束片 | `horizon_constraint_plate` | 物品 | 超导环 + 拓扑晶体 + 隧穿链路 | `closure_rating`、`field_leak_rate` | 黑曜石结构 | P0 |
| 熵流泵 | `entropy_pump` | 方块 | 约束片 + 相干能 + III 型框架 | `extraction_rate`、`backflow_ratio` | 无 | P0 |
| 全息信息膜 | `holographic_membrane` | 方块/物品 | 膜刻写器 + 约束片 | `capacity_pages`、`readout_fidelity` | 末影箱存储类比 | P0 |
| 霍金采样器 | `hawking_sampler` | 方块/传感器 | 底噪谱仪升级 + 辐射谱片 | 合并采样和回收 | 无 | P1 |
| 彭罗斯吸积线圈 | `penrose_accretion_coil` | 方块 | 超导环 + N 型晶片 + 抗压晶体 | 合并彭罗斯线圈和吸积盘环 | 高密度方块进料 | P1 |
| 人造视界核心 | `artificial_horizon_core` | 方块/核心物品 | III 型框架 + 弦 + 约束环 | `horizon_radius`、`stability_threshold` | 信标/龙蛋视觉类比 | P0 |
| 紧急熄灭器 | `emergency_quencher` | 方块 | 熵流泵 + 红石 + 相干能缓存 | 安全停机，防止全损 | 红石控制 | P0 |
| 弦锚定器 | `string_anchor` | 方块 | 拓扑晶体 + 末地材料 | 稳定戈古尔斯弦 | 末地烛视觉类比 | P0 |
| 全息膜刻写器 | `holographic_membrane_writer` | 方块 | 信息中心 + 全息膜 | 写入/读取信息膜 | 书写类比 | P1 |
| III 型人造视界框架 | `horizon_framework` | 多方块 | 约束环 + 传感器 + 控制层 | 完整视界成型 | 多方块 | P0 |

### 10.3 成型条件

```text
framework_tier >= 3
horizon_constraint >= threshold
coherence_budget >= threshold
entropy_extraction >= threshold
string_anchor_stability >= threshold
background_noise_profile known
emergency_shutdown present
```

允许低阈值试运行，但效率下降、坍缩风险上升。坍缩不应全毁，应该产出黑洞解析残渣，保留玩家恢复路径。

### 10.4 传感器与实现

- 传感器包括相干度、弦稳定度、熵流、霍金辐射、约束泄漏，属于 S4。
- 每 tick 只结算约 7 个抽象参数：稳定度、熵流、相干度、冷却、锚定稳定、信息膜进度、泄漏率。
- 多方块建议上限 7x7x7，并只在结构变化时重扫。
- 模型调参收益高，但主线可以用预设曲线和稳定钥完成。

## 11. 阶段十：黑洞发电、存储与运算

### 11.1 阶段目标

让可控人造视界成为能量、存储和运算三类设备的公共核心，而不是只做大发电机。

### 11.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 黑洞解析残渣 | `black_hole_residue` | 物品 | 视界退役/失败/运行副产 | `residue_purity` | 无 | P0 |
| 长期光存储单元 | `long_term_photonic_memory` | 物品/方块 | 稀土掺杂晶体 + 量子点 + 视界材料 | 受激辐射 / 室温暗态光存储；第 6 阶段 `photonic_ram_unit` 的持久化升级 | 无 | P1 |
| WDM 复用器 | `wdm_multiplexer` | 物品/方块 | 单频激光源 x4 + 滤波器阵列 + F4 晶振 | 单光纤多波长 | 无 | P1 |
| 全光交换核 | `all_optical_switch_core` | 物品/方块 | 视界材料的非线性光开关 + 光协处理器接口 | 控制平面光化（电气退场） | 无 | P2 |
| 视界能量缓存 | `horizon_energy_buffer` | 方块/物品 | 残渣 + 稳谱晶体 | `capacity`、`discharge_stability` | FE | P0 |
| 全息数据片 | `holographic_data_slice` | 物品 | 视界 + 全息膜 + 信息中心 | `page_count`、`error_rate` | 末影箱类比 | P0 |
| 熵梯度结果 | `entropy_gradient_result` | 物品 | 黑洞运算任务输出 | `convergence_score`、`confidence` | 无 | P1 |
| 微观态枚举表 | `microstate_table` | 物品 | 费曼蓝图 + 运算核心 | `state_count`、`branch_factor` | 无 | P2 |
| 维度规则候选 | `dimension_rule_candidate` | 物品 | 视界协处理 + 底噪数据库 | `rule_type`、`conflict_tags` | 无 | P0 |
| 黑洞运算核心 | `black_hole_compute_core` | 方块/物品 | 视界核心 + 协处理器 + 全息膜 | `compute_budget` | 无 | P1 |
| 熵差整流器 | `entropy_rectifier` | 方块 | 熵流泵升级 | 将熵流差转为 FE/相干能 | FE | P1 |
| 视界冷却塔 | `horizon_cooling_tower` | 多方块附属 | 低温系统 + 熵流泵 | 控制热预算 | 水/冰 | P1 |
| 视界地址索引器 | `horizon_address_indexer` | 方块 | 信息中心升级 | 给全息膜分页寻址 | 无 | P1 |

### 11.3 三模式互斥

同一可控人造视界一次只运行一种模式：

```text
generation:
  fed_mass_score
  spin_rate
  cooling
  capped_FE_output

storage:
  stored_pages
  hamming_distance
  hawking_parity
  readout_fidelity

computation:
  compute_budget
  gradient_convergence
  solution_quality
```

三模式互斥能显著降低服务端结算量，也让玩家有明确的设备用途选择。

### 11.4 原版关联

- 铁块、金块、钻石块、下界合金块作为质量进料，提供不同 `mass_score`。
- 末影箱和潜影盒作为“空间化存储”的玩家认知锚点。
- 龙蛋可以作为极后期黑洞运算核心或维度规则候选的稀有催化物，但不应让主线硬卡唯一物品。

## 12. 阶段十一：世界之心提取与维度创世

### 12.1 阶段目标

提取当前维度的信息特征，结合戈古尔斯弦、底噪数据库、黑洞运算结果和参数矩阵，编译一个可进入、可维护的新维度。

### 12.2 核心物品与方块

| 中文名 | id | 类型 | 获取/合成 | 主要作用与参数 | 原版关联 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 世界之心频率 | `world_heart_frequency` | 物品/数据 | 巨型节点框架超载萃取 | `dimension_id`、`base_frequency` | 下界之星/末地 | P0 |
| 维度参数矩阵 | `dimension_parameter_matrix` | 物品 | 创世编译台 + 7 组参数 | `dimension_parameter_matrix` Data Component | 地图/书类比 | P0 |
| 创世蓝图 | `genesis_blueprint` | 物品 | 世界之心 + 戈古尔斯弦 + 规则候选 | `validation_errors`、`compile_progress` | 锻造模板/地图 | P0 |
| 空间锚 | `spatial_anchor` | 方块 | 末地框架 + 视界能量缓存 | `anchor_stability`、`drift_rate` | 末地传送门 | P0 |
| 规则干涉器 | `rule_interferometer` | 方块 | 协处理器 + 规则候选 + 全息膜 | `rule_lock_strength` | 无 | P1 |
| 已编译维度核心 | `compiled_dimension_core` | 物品/方块 | 蓝图 + 参数矩阵 + 视界能量缓存 | 完整维度定义引用 | 无 | P0 |
| 巨型节点框架 | `giant_node_framework` | 多方块 | 晶体管 + 凝聚态链路 + 稳定环 | 世界之心萃取和维护模式 | 信标/传送门 | P0 |
| 创世编译台 | `genesis_compiler` | 方块 | 信息中心 + 黑洞运算核心 | 编译维度核心 | 制图台类比 | P0 |
| 维度点火环 | `dimension_ignition_ring` | 多方块 | 空间锚 + 维度核心 | 打开入口 | 末地传送门 | P0 |
| 维度维护塔 | `dimension_maintenance_tower` | 多方块模式 | 巨型节点框架维护模式 | 压制规则漂移和熵增 | 信标类比 | P1 |

### 12.3 参数矩阵

```text
terrain_base
biome_weight
physics_rule
resource_spectrum
entity_spawn
noise_structure
entropy_rate
```

主线应提供 3-5 个预置模板，例如稳定平原、浮岛矿脉、低重力荒原、底噪富集层。玩家自定义是上限玩法。

### 12.4 实现边界

- 第一版使用预注册维度模板或数据包模板，不做运行时无限动态注册。
- 维度维护不遍历全部区块，只对抽样区块估算熵增。
- 编译是长任务，持续数百 tick，显示进度。不要阻塞 server tick。
- 维度可进入冻结状态：停止维护消耗，但禁止进入或禁止机器运行。

## 13. 可合并项总表

| 合并对象 | 建议 |
| --- | --- |
| 铁粉、煤粉、铜粉 | 合并为 `spectrum_powder`，用 `powder_type` 区分 |
| 植物/铁网/玻璃纤维滤膜 | 合并为 `spectrum_membrane`，用 `membrane_type` 区分 |
| 裂纹晶体、频谱粉尘 | 合并为 `kamaen_crystal_debris`，用 `debris_type` 区分 |
| 晶片坯、N 型、P 型、缺陷片 | 合并为 `kamaen_wafer`，用 `wafer_type`、`doping_type` 区分 |
| 施主/受主掺杂剂 | 合并为 `kamaen_dopant`，用 `dopant_type` 区分 |
| F1/F2/F3 晶振 | 合并为 `kamaen_oscillator`，用 `frequency_tier` 区分 |
| 内存页、参数页、状态页 | 合并存储后端为 `kamaen_storage_page` 或 `memory_page` |
| 隧穿串联器、4 维电路桥 | 合并为 `tunnel_linker` |
| 彭罗斯线圈、吸积盘环 | 合并为 `penrose_accretion_coil` |
| 霍金采样器、霍金回收器 | 合并为 `hawking_sampler` |
| 巨型节点框架、维度维护塔 | 维护塔作为巨型节点框架的维护模式 |

## 14. 主线卡点与降低风险

| 卡点 | 阶段 | 风险 | 降低方式 |
| --- | --- | --- | --- |
| 分馏塔多方块 | 一 | 太早引入复杂结构 | v0.1 固定结构，后续接入 `MultiblockFormer` |
| 爆炸室向量评分 | 二 | 玩家难理解，公式复杂 | 先预设方向和线性评分，GUI 显示四项分数 |
| 探针读取边界 | 三 | 兼容性范围过大 | P0 只读方块状态和红石，能力适配后移 |
| 掺杂轴定向 | 四 | 三轴参数教学压力大 | 初版只开放 X 轴，Y/Z 作为升级 |
| II 型框架联动 | 四 | 多机器联动爆炸 | 先独立机器，框架只做集中控制 |
| 底噪层数量 | 五 | 9 层一次做完过重 | 先 3 层可用，其余占位 |
| 光计算硬件 | 六（新增） | 相干能模型、光路可视化、校准机制复杂 | 第一版只做五件套最小闭环：光控制核 + 光协处理器 + 光GPU + 光脉冲处理器 + 光RAM；相干能用简单线性公式；可视化做最低限度光纤亮度 |
| III 型框架 | 七/九 | 全科技树最大架构风险 | 复用基类，限制方块数量，分级成型 |
| 隧穿跨 chunk | 七 | 引用失效和卸载问题 | 维度级注册表 + chunk unload 清理 |
| 量子光学协处理器 | 八 | 容易误做真实模拟 | 任务队列 + 分步抽象结算（玻色采样路线） |
| 视界坍缩 | 九 | 失败惩罚过重 | 紧急熄灭器 + 残渣回收 + 稳定次数 |
| 黑洞三模式 | 十 | 参数过多 | 发电/存储/运算互斥运行 |
| 维度创世 | 十一 | 运行时注册和维护成本 | 预置模板 + 冻结维度 + 抽样维护 |

## 15. 版本落地优先级

| 版本 | 必须完成 | 暂做占位 | 延后 |
| --- | --- | --- | --- |
| v0.1 | 分馏塔、频谱滤渣、白噪晶种、初级分光镜 | 粉末变体 | 污染细分 |
| v0.2 | 爆炸室、粗晶体、三轴晶体、晶体 Data Component | 应力传感器 | 可变爆破结构 |
| v0.3 | 干涉仪、探针台、InfoSignal、频率总线 | FE/流体/物品槽适配 | 复杂总线路由 |
| v0.4 | I 型框架、偏振晶体、共振催化晶体 | 调谐阵列高级评分 | 自动调参 |
| v0.5 | 晶片、掺杂剂、注入器、退火炉、晶体管 | 多轴掺杂 | II 型完整联动 |
| v0.6 | 光刻、刻蚀、相干能、导波材料、相位调谐片 | 信号缓存高级用途 | 多维信息诊断 |
| v0.7 | 信息诊断台、F1-F3、共振信号缓存、自动化闭环 | 频率路由片高级用途 | 模型结构预览 |
| v0.75 | 硅光波导、MZI、相位调谐器、探测器、激光源、光控制核、光协处理器、光GPU、光脉冲处理器、光RAM、相干能、F4 晶振 | 光路可视化（仅亮度）；WDM | 高级光路校准 UI |
| v0.8 | 底噪谱仪、3 层底噪、数据库、信息中心 | 其余 6 层底噪 | 长期模型采样 |
| v0.9 | 低温腔、传播子、费曼蓝图、III 型雏形、量子光学协处理器曲线、单光子源/SNSPD | 高级传播子 | 隐藏过程发现 |
| v1.0 | 人造视界、黑洞发电/存储、长期光存储/WDM/全光网络、维度编译和入口 | 黑洞运算深度玩法、全光控制平面 | 完全自定义维度规则 |

## 16. 推荐实现切入点

最小可玩链路应优先锁定：

```text
圆石
-> 频谱滤渣
-> 白噪晶种
-> 粗卡玛恩晶体
-> 稳谱晶体
-> 探针读取红石/方块状态
-> InfoSignal
-> 频率转红石
```

这条链路能验证材料、Data Component、机器配方、GUI、传感器和自动化闭环。后续所有阶段都可以沿着同一套参数和框架体系自然扩展。

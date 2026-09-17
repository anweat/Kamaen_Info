# Kamaen Info 复杂硬件组件制造工艺参考设计

状态：参考设计稿。  
用途：为后续细化晶振、裸片、PCB、封装、光纤、无线、电源、冷却、传感器等制造链提供统一框架。本文不替代硬件科技树文档，而是补充“硬件组件如何被制造、如何受环境影响、如何被自动化控制”的设计基线。

## 1. 设计目标

复杂硬件制造不是一次性配方合成，而是一个可观测、可调参、可自动化的工艺过程。

核心目标：

```text
手动工艺可以制造基础可用件。
传感器和阈值控制可以稳定标准件。
PID、回归模型和更高级模型可以提高良率、分档和一致性。
```

玩家最终使用组件时，不需要关心完整工艺细节，只看组件画像是否达到蓝图要求：

```text
频率等级达标
损耗达标
热阻达标
缺陷达标
端口/引脚密度达标
相位稳定达标
```

制造过程中则保留更细的过程变量和环境变量，为传感器网络、数据集和模型调参提供输入。

## 2. 需要复杂工艺的硬件部件

根据硬件科技树文档，以下部件最适合进入复杂制造系统。

### 2.1 晶振与锁相组件

对应硬件字段：

```text
frequency_tier
clock_domain
sync_quality
clock_tree_quality
phase_stability
```

典型产物：

```text
粗制石英晶振
F1 基准晶振
F2 数据晶振
F3 矩阵同步晶振
F4 锁相光频晶振
频率桥
锁相接口
多卡锁相器
```

适合高精度工艺建模。它对温度、振动、相位噪声、应力稳定和晶体质量高度敏感。

### 2.2 芯片硅底、晶圆与裸片

对应硬件字段：

```text
yield_score
frequency_limit
thermal_output
process_quality
die_area_penalty
```

典型产物：

```text
粗硅质片
抛光硅片
掺杂晶圆
裸片
低频裸片
标准裸片
高频裸片
高并行裸片
低功耗裸片
锁相特化裸片
```

适合长流程、多步骤、误差累积型工艺建模。

### 2.3 芯片封装与引脚

对应硬件字段：

```text
pin_count
port_layout
port_width
package_loss
thermal_transfer
frequency_limit
motherboard_socket_type
wireless_attenuation
optical_coupling_quality
```

典型产物：

```text
DIP 封装件
QFP 封装件
BGA 封装件
光电混合封装件
无线封装件
金触点
铜引脚
插槽座
散热封盖
```

封装连接芯片与主板，是端口、热、损耗和兼容性的重要来源。

### 2.4 主板 PCB、通信平面与总线层

对应硬件字段：

```text
bus_bandwidth
trace_penalty
layer_alignment
port_exposure
power_delivery
clock_tree_quality
thermal_clearance
```

典型产物：

```text
绝缘基板
铜覆层基板
F1 控制 PCB
F2 数据 PCB
高频 PCB
锁相背板
多层数据基板
频率总线层
光频总线层
```

主板蓝图决定布局，PCB 和总线材料决定蓝图能达到的质量边界。

### 2.5 内存页、储存芯片与参数页载体

对应硬件字段：

```text
memory_pages
storage_pages
read_bandwidth
write_bandwidth
index_speed
data_loss_risk
thermal_stability
power_stability
```

典型产物：

```text
参数页
激活页
状态页
索引页
交换页
一级储存芯片
参数库接口
缓存页
```

这些不需要真实存储结构模拟，但可以通过材料质量、封装、热稳定和供电稳定影响最终性能。

### 2.6 光纤与光电组件

对应硬件字段：

```text
optical_coupling_quality
per_port_bandwidth
switch_bandwidth
clock_passthrough
multicast_efficiency
```

典型产物：

```text
石英纤芯
多模光纤
单模光纤
相干光纤
光纤芯片
光频互连卡
相干光背板
光纤交换机端口件
```

光纤链路适合与晶振、锁相、光学纯度和拉丝工艺绑定。

### 2.7 无线组件

对应硬件字段：

```text
wireless_slots
wireless_attenuation
remote_session_count
frequency_band
latency
coverage
```

典型产物：

```text
无线芯片
无线天线
公网接收器
无线基站组件
频段调制片
天线隔离件
```

无线组件适合受封装隔离、空间暴露、频段拥挤和电磁噪声影响。

### 2.8 电源与相位供能组件

对应硬件字段：

```text
power_budget
power_delivery
power_stability
power_loss_risk
phase_noise
power_ripple
```

典型产物：

```text
稳压线圈
相位整流片
供能背板
电源接口
低纹波电源模块
三相稳相模块
```

电源组件应连接早期“供电相位稳定性”玩法和中后期硬件稳定运行。

### 2.9 冷却与热界面组件

对应硬件字段：

```text
thermal_clearance
cooling_headroom
thermal_transfer
thermal_throttle_risk
liquid_cooling_rate
cryogenic_boost
```

典型产物：

```text
散热片
热界面层
冷却管接口
液冷模块
低温冷却模块
机柜冷却管道
```

冷却组件可以做成较直观的工程链，但高端版本仍可受材料纯度、接触质量和环境温度影响。

### 2.10 传感器组件

传感器分为两层：

```text
通用电子基座：
  PCB、小型芯片、晶振、封装、数据端口。

场景探头：
  由温度、压力、应力、相位、生物、光学、下界热场、末影相位等特殊材料决定。
```

传感器本身也可以由复杂工艺制造，但更重要的是服务其他工艺的观测和闭环控制。

### 2.11 光学元件与光计算组件（第 6 阶段，新增）

第 6 阶段「光计算」阶段需要的光学元件工艺。完整设计参见 `docs/Kamaen_Info_Optical_Computing_Design.md` 第 3 章。

对应硬件字段：

```text
photonic_throughput
coherence_avg
coherence_min
wavelength_load
optical_bandwidth
mzi_grid_size
weight_switch_cost
detector_noise_floor
logic_error_rate
bistable_cell_health
pulse_threshold_drift
ram_coherence_life
coherent_energy_draw
calibration_age
```

典型产物：

```text
硅光波导毛坯（silicon_photonic_waveguide_blank）
硅光波导（silicon_photonic_waveguide）
马赫-曾德尔调制器（mzi_modulator）
相位调谐器（phase_tuner，热光/电光两种）
硅光探测器（silicon_photodetector，PIN/APD/锗硅）
单频激光源（single_freq_laser_source）
卡玛恩非线性介质（kamaen_nonlinear_medium）
光逻辑门（photonic_logic_gate）
卡玛恩双稳态晶胞（kamaen_bistable_cell）
光控制核（photonic_control_core）
光协处理器（photonic_coprocessor）
光GPU 单元（photonic_gpu_unit）
光脉冲处理器（photonic_pulse_processor）
光RAM 单元（photonic_ram_unit）
光路校准令牌（calibration_token）
```

工艺要点：

```text
波导刻蚀：
  导波晶体掺杂硅 → 光刻（短波长曝光 + 相位掩模） → 反应离子刻蚀 → 退火。
  受洁净度、光刻精度、退火温度均匀性影响。

MZI 编织：
  两段波导 + 中间相位调谐器 + 输入/输出 50:50 分束 → MZI 单元；
  N×N MZI 网格采用 Reck 三角或 Clements 矩形拓扑。
  受波导对齐精度、分束器一致性、相位调谐器线性度影响。

光探测器制造：
  PN 结掺杂 + 增益区设计 + 暗电流抑制；
  锗硅探测器需要锗外延层；
  受退火温度、掺杂均匀性、电场均匀性影响。

单频激光源：
  稳谱晶体 + F4 晶振泵浦 → 锁相单频光；
  受稳谱晶体品级、F4 晶振相位噪声、泵浦能源相干能耦合影响。

相位调谐器：
  热光：在波导上方加微加热条；受热分布均匀性影响。
  电光：在波导内掺杂载流子注入；受掺杂浓度和电场均匀性影响。

光协处理器封装：
  简化光调度逻辑 + 光数据通路 + 全光路由交换机；
  关键是多通道波导损耗、路由延迟和 F4 时钟同步。

卡玛恩非线性介质制备：
  导波晶体 + 稳谱晶体共掺杂 → 应力调谐非线性腔；
  关键字段是 chi2_coefficient、nonlinear_bandwidth 和 threshold_stability。

光逻辑门 / 双稳态晶胞：
  非线性介质 + 波导 + 分束器 → AND/OR/NOT 等光逻辑门；
  两个耦合卡玛恩共振腔 → 双稳态晶胞。
  受晶体应力张量、腔体 Q 值、泵浦稳定度影响。

光控制核封装：
  双稳态晶胞阵列 + 光逻辑门阵列 + F4 光时钟 → 全光 FSM；
  关键诊断字段是 logic_error_rate、fsm_state_depth、bistable_cell_health。

光脉冲处理器封装：
  饱和吸收体腔 + S 型非线性传输腔 + 时分复用波导；
  关键诊断字段是 sparse_ops、nonlinear_ops、pulse_threshold_drift。

光RAM 封装：
  双稳态晶胞 + 循环波导 + 增益介质 + 部分反射镜；
  关键诊断字段是 ram_coherence_life、read_decay_rate、refresh_cost。

光路校准：
  使用相位调谐器扫描 + 干涉测量 → 重新写入 MZI 权重；
  消耗校准令牌 + 60 秒；受温度稳定性影响。
```

前置工艺要求：

- 第 3 阶段提供光栅原型、波导原型、初级调制器（不可重写）。
- 第 4 阶段提供精密化光刻、光探测器、相位调谐器、激光源前体；电气合成时代的光刻台升级后同时服务电气晶体管制造与光波导制造。
- 第 7 阶段（凝聚态）提供单光子源、SNSPD，可反向升级第 6 阶段的探测器（提升信噪比，降低相干能消耗）。

## 3. 统一工艺步骤

不同部件可以共用一组工艺动作。每个部件只选择其中需要的步骤。

```text
裂解 / 粉化
分离 / 沉降
纯化 / 清洗
成型 / 压制
晶体生长 / 拉丝
应力写入
抛光 / 平整
掺杂 / 渗透
图案化 / 曝光
蚀刻 / 去除
沉积 / 互连
退火 / 稳定化
封装 / 接口映射
测试 / 分档
```

原则：

```text
机器按工艺动作统合。
材料路线按步骤组合区分。
高级产物需要更多步骤和更窄的工艺窗口。
```

## 4. 工艺步骤的数据结构

每个工艺步骤都可以用同一套逻辑描述。

```text
ProcessStep
- targetState
- controlInputs
- processDisturbances
- environmentInputs
- sensorObservations
- outputMetrics
- failureModes
```

含义：

```text
targetState:
  希望过程状态接近的目标。

controlInputs:
  玩家、机器、PID 或模型可以调整的参数。

processDisturbances:
  生产过程中随机或半随机变化的过程扰动。

environmentInputs:
  机器外部或结构环境提供的动态条件。

sensorObservations:
  可由传感器读取的状态。

outputMetrics:
  影响成品画像的结果指标。

failureModes:
  可诊断的失败原因或降级原因。
```

## 5. 环境参数系统

环境不是背景装饰，而是可测量、可控制、可建模的输入变量。

每个工艺步骤应声明：

```text
required_environment
sensitive_environment
compensatable_environment
fatal_environment
```

### 5.1 热环境

变量：

```text
ambient_temperature
thermal_gradient
thermal_inertia
heat_dissipation
cooling_stability
```

影响：

```text
晶振主频漂移
晶圆应力不均
退火曲线偏差
封装翘曲
冷却效率
热循环寿命
```

控制设施：

```text
温控模块
隔热墙体
冷却管道
热缓冲块
液冷 / 低温冷却模块
```

### 5.2 振动环境

变量：

```text
vibration_amplitude
vibration_frequency
mechanical_shock
foundation_stability
machine_balance
neighbor_shock_events
```

影响：

```text
晶振切向偏差
光刻对准误差
光纤拉丝粗细波动
封装引脚偏移
硅片微裂纹
```

控制设施：

```text
减震基座
惯性稳定框架
机器配平模块
隔振墙体
爆炸室隔离距离
```

### 5.3 洁净环境

变量：

```text
particle_density
chemical_contamination
organic_contamination
static_dust_level
filter_quality
room_pressure
```

影响：

```text
晶圆缺陷密度
蚀刻断线率
封装接触不良
光纤散射损耗
传感器噪声
```

控制设施：

```text
洁净室墙体
正压过滤器
静电中和器
材料预清洗槽
密封接口
```

### 5.4 电气与相位环境

变量：

```text
power_ripple
phase_noise
ground_reference_quality
electromagnetic_noise
frequency_domain_crowding
```

影响：

```text
晶振相位噪声
锁相捕获范围
掺杂方向稳定
传感器读数噪声
无线组件底噪
```

控制设施：

```text
稳相电源
低纹波供电模块
接地框架
屏蔽墙
频率隔离器
低噪声总线
```

### 5.5 流体与化学环境

变量：

```text
fluid_purity
fluid_temperature
flow_rate
concentration
viscosity
pressure
reaction_byproduct_level
```

影响：

```text
蚀刻深度
掺杂扩散
清洗残留
冷却效率
包层厚度
污染回流
```

控制设施：

```text
流量阀
浓度调节器
循环过滤器
温控槽
压力稳定器
废液分离器
```

### 5.6 结构与空间环境

变量：

```text
room_isolation
machine_spacing
foundation_material
neighbor_machine_interference
port_accessibility
maintenance_access
```

影响：

```text
机器震动串扰
无线衰减
散热路径
端口暴露
机柜维护评分
自动化布线复杂度
```

控制设施：

```text
专用机房
隔离地基
机柜通道
端口背板
线缆桥架
维护通道
```

### 5.7 维度、生物与特殊场环境

变量：

```text
dimension_type
light_level
humidity
biological_activity
nether_heat_field
ender_phase_noise
sky_exposure
```

影响：

```text
生物材料培养
末影相位组件
下界热场材料
光学处理
无线传播
特殊传感器探头
```

这些环境参数可用于高阶或特殊材料，不必在前期全面启用。

## 6. 过程扰动系统

过程扰动发生在机器运行内部或材料反应过程中。

常见扰动：

```text
浓度波动
温度漂移
压力波动
振动噪声
供电纹波
相位漂移
输入材料批次差异
机器磨损
流体流量波动
副产物污染
```

设计边界：

```text
扰动必须可观测或可估计。
扰动必须有补偿手段。
影响应连续，而不是纯随机失败。
基础件应能手动制造。
失败件或低分档件应能回收或降级使用。
```

## 7. 手动、自动与模型控制层级

复杂工艺支持多个控制层级。

```text
1. 固定参数
玩家设定温度、时间、频率、压力等固定值。

2. 阈值控制
传感器超过阈值后停机、报警或切换红石信号。

3. PID 控制
根据目标与当前值的误差连续调整温度、流量、压力、频率等。

4. 回归模型
根据材料画像、环境状态和历史批次预测下一步参数。

5. 序列模型 / 高级控制模型
根据传感器时间序列动态调整完整工艺路线。
```

自动化的价值：

```text
提高良率
提高分档
减少材料浪费
稳定批量生产
适应不同材料批次
抵消环境扰动
在多步骤流程中修正误差累积
```

## 8. 组件画像与分档

组件使用端应该简化，只暴露少量画像指标。

通用画像：

```text
quality_tier
frequency_grade
loss
thermal_rating
phase_stability
defect_level
purity
interface_density
stress_stability
```

不同组件可以有专属指标：

```text
晶振：
  main_frequency
  peak_width
  phase_noise
  temperature_drift
  lock_range

裸片：
  die_yield
  defect_density
  doping_uniformity
  frequency_response
  thermal_output

PCB：
  layer_alignment
  trace_density
  trace_loss
  insulation_stability
  clock_tree_quality

封装：
  pin_count
  package_loss
  thermal_transfer
  port_width
  socket_type

光纤：
  optical_loss
  coupling_quality
  clock_passthrough
  bandwidth_grade

无线：
  frequency_band
  attenuation
  noise_floor
  coverage_grade
```

分档不应只有成功或失败。

示例：

```text
废品：
  回收或作为低级材料。

低频件：
  可用于 F1 控制、低端传感器、低速接口。

标准件：
  可用于 F2 数据、通用主板、基础自动化。

高频件：
  可用于 F3 矩阵、GPU/NPU、数据背板。

锁相特化件：
  可用于 F4 光频、同步、多卡互连。

低功耗 / 高可靠 / 高并行特化件：
  用于特定蓝图方向。
```

## 9. 晶振制造链参考

晶振链是短流程、高精度工艺，适合优先落地。

流程：

```text
晶体基材制备
→ 晶轴定向
→ 应力调谐
→ 电极 / 触点沉积
→ 频率扫描
→ 退火稳定
→ 锁相封装
→ 分档
```

关键控制参数：

```text
切向角度
压力 / 应力张量
退火温度曲线
激励频率
相位稳定
触点沉积厚度
扫描时间
```

关键环境参数：

```text
ambient_temperature
thermal_gradient
vibration_amplitude
phase_noise
power_ripple
electromagnetic_noise
foundation_stability
```

关键过程扰动：

```text
相位漂移
触点厚度波动
晶体应力回弹
温度漂移
微振动
```

关键检测状态：

```text
主频
峰宽
相位噪声
温漂系数
轴向响应
应力椭球稳定度
锁相捕获范围
```

分档方向：

```text
粗制晶振
F1 基准晶振
F2 数据晶振
F3 矩阵同步晶振
F4 锁相光频晶振
锁相接口
多卡锁相器
```

手动可行性：

```text
手动切向和固定退火可获得 F1/F2 粗件。
稳定 F3 以上需要低振动、低相位噪声环境和传感器反馈。
F4 锁相件应强依赖自动控制和环境设施。
```

## 10. 裸片制造链参考

裸片链是长流程、多步骤工艺，适合体现数据集和模型调参。

流程：

```text
硅质前体提纯
→ 晶圆生长 / 压制
→ 切片
→ 抛光
→ 掺杂
→ 图案化 / 光刻
→ 蚀刻
→ 退火
→ 金属互连
→ 裸片测试
→ 分档
```

关键控制参数：

```text
纯化频率
晶圆生长温度
压力
掺杂浓度
掺杂方向
曝光图案
曝光强度
蚀刻深度
退火时间
冷却曲线
洁净度目标
```

关键环境参数：

```text
particle_density
chemical_contamination
ambient_temperature
thermal_gradient
vibration_amplitude
fluid_concentration
fluid_temperature
phase_noise
power_ripple
```

关键过程扰动：

```text
浓度波动
温度漂移
微粒污染事件
振动事件
蚀刻速率变化
掺杂扩散偏差
退火应力回弹
机器磨损
```

关键检测状态：

```text
晶圆纯度
缺陷密度
掺杂均匀度
图案对准度
蚀刻完整度
互连密度
退火应力
频率响应
```

分档方向：

```text
残次裸片
低频裸片
标准裸片
高频裸片
高并行裸片
低功耗裸片
锁相特化裸片
```

手动可行性：

```text
手动固定参数可获得低频或标准裸片。
高频、高并行、低功耗和锁相特化裸片需要传感器反馈与过程控制。
复杂蓝图的裸片良率应强烈依赖自动化工艺。
```

## 11. 数据采样与模型学习

每个制造批次可以生成工艺样本。

```text
ProcessBatchSample
- batch_id
- material_initial_profile
- machine_configuration
- environment_time_series
- control_input_series
- sensor_observation_series
- disturbance_events
- output_component_profile
- binning_result
- failure_reason
```

模型学习目标：

```text
预测成品分档
预测失败原因
推荐下一步工艺参数
在扰动出现时动态补偿
判断是否暂停、重做、降级或继续
为不同目标画像选择工艺路线
```

玩家可以设定目标：

```text
最大频率等级
最低损耗
最高良率
最低热阻
最低缺陷
最高相位稳定
成本与质量平衡
```

## 12. 与前期机器的衔接

复杂制造不应凭空开始，应从早期机器自然发展。

```text
便携爆炸室：
  粗粉、应力写入、早期特殊处理。

TNT 爆炸室：
  批量冲击处理、粗晶体激活、强应力样本。

谐振装配台：
  基础零件、小批量成型、手动调频、早期晶振/硅片处理。

共振分离阵列：
  资源分离、纯化、晶体分析、频率筛选、材料前体生产。

共振分离阵列扩展：
  应力处理、退火、相位控制、分析、数据接口、传感器接入。
```

中期新增或扩展的工艺设备：

```text
压制成型机
纯化清洗槽
掺杂渗透机
图案化曝光机
蚀刻槽
退火稳定炉
封装测试台
光纤拉丝塔
热循环测试台
洁净室环境模块
减震基座
稳相电源
环境监控背板
```

## 13. 后续细化方向

后续可以按以下顺序把本参考设计细化成具体配方和机器：

```text
1. 晶振 / 锁相器制造链 MVP
2. 硅底 / 裸片制造链 MVP
3. PCB / 主板基材制造链
4. 封装 / 引脚 / 接口制造链
5. 传感器电子基座与场景探头
6. 电源与相位供能组件
7. 冷却与热界面组件
8. 光纤与光电组件
9. 无线组件
10. 内存页、储存芯片与参数页载体
```

每条链都应补充：

```text
输入材料
工艺步骤
所需机器
控制参数
环境参数
传感器观测
扰动事件
成品画像
分档规则
失败与回收规则
自动化收益
```

## 14. 暂不解决的问题

本文暂不确定具体数值公式。

后续仍需讨论：

```text
环境参数如何从方块空间采样。
环境设施的多方块判定方式。
传感器采样频率与服务器性能限制。
过程控制是否按 tick、阶段或批次结算。
PID / 回归模型在游戏内的表达方式。
工艺数据集如何存储与压缩。
低分档产物的具体用途。
与现有硬件科技树文档的字段合并方式。
```

# Kamaen Info 计算基础设施完整路径

状态：确定版整理。

## 1. 总定位

本系统不是完整电路仿真、真实无线网络、真实操作系统或真实深度学习后端，而是一套游戏内可设计、可制造、可封装、可组网、可诊断的计算基础设施玩法。

核心循环：

```text
需求定义
-> 芯片/主板/网络蓝图设计
-> 零部件制造与良率控制
-> 芯片封装与主板封装
-> 机柜组装、供电、冷却和连线
-> 机柜族/集群组网
-> 接入传感器、存储中心和模型任务
-> 诊断瓶颈
-> 优化蓝图、工艺、网络、调度和模型结构
```

硬边界：

```text
不模拟晶体管级电路。
不模拟真实电磁场。
不模拟完整真实操作系统。
不实现真实 IPv4/IPv6 协议栈。
不在服务端 tick 内运行真实大模型训练。
复杂任务可以表达，但运行必须受预算、权限和调度限制。
```

允许的自由度：

```text
芯片模块组合、位宽、端口、bus 和封装。
主板格点蓝图、多层布线、端口方向、芯片组和散热。
机柜供电、冷却、理线、交换机、光纤、电源和管道。
集群任务分片、调度、DNS、服务发现、无线策略和数据流。
传感器采样、同步、数据表、模型输入和反馈闭环。
```

## 2. 六层架构

```text
芯片层
模块、位宽、频率、端口、bus、热。

封装层
引脚/接口、端口分布、散热、频率上限、socket 兼容。

主板层
总线、内存、一级储存、端口、供电、散热、无线宽度。

机柜层
算力密度、供电、冷却、光纤/电线、理线、掉电和过热风险。

集群层
调度、交换、带宽、存储、DNS/服务发现、任务分片。

模型层
参数加载、推理、训练、传感器输入、运行可视化。
```

关系：

```text
芯片输出算力和 I/O 单元
-> 封装决定接口和热边界
-> 主板决定本机资源组织
-> 机柜决定密度和稳定运行
-> 集群决定任务拆分和网络效率
-> 模型层消耗算力、内存、带宽、存储和调度预算
```

设计原则：

```text
聚合不抹除个体。
集群可以聚合资源，但任务仍然分配到具体机柜、主板、端口和芯片。

每层都有 AggregateProfile 与 TracePath。
快速结算用聚合画像，诊断和玩法用可反推路径。

适配器按层分化。
硬件、数据、传感器、网络各自有适配/转换对象，不强行统一命名。
```

TracePath 示例：

```text
cluster.available_cpu_ops
<- rack_03.available_cpu_ops
<- board_cpu_01.effective_control_ops
<- chip_slot_2.control_ops
<- packaged_logic_chip_17
```

### 2.1 层间数据继承与聚合

每一层不重新发明性能字段，而是继承下层画像并加入本层损耗、瓶颈或聚合规则。

聚合规则分四类：

```text
sum
同类资源相加，例如多个芯片的 control_ops、route_ops、memory_pages。

min
瓶颈资源取最小值，例如芯片频率上限、封装频率上限、主板 bus 带宽。

multiply
质量或损耗系数相乘，例如封装效率、主板走线效率、散热降频系数。

map
结构映射，例如芯片端口映射到封装引脚，封装引脚映射到主板 socket，主板端口映射到机柜面板。
```

示例：控制芯片 -> DIP 封装 -> 5x5 主板。

```text
chip_profile
control_ops = 100
script_ops = 60
io_bandwidth = 16
thermal_output = 20
frequency_limit = F2
ports = input:2, output:1

package_profile
package_type = DIP
pin_count = 16
io_efficiency = 0.75
thermal_transfer = 0.40
frequency_limit = F1
port_layout = input:2, output:1

motherboard_profile
bus_efficiency = 0.80
socket_compatibility = mechanical
board_thermal_budget = 18
board_power_budget = 40
```

计算：

```text
effective_frequency = min(chip.frequency_limit, package.frequency_limit, board.clock_limit)
effective_control_ops = chip.control_ops * package.io_efficiency * board.bus_efficiency * frequency_factor
effective_io_bandwidth = min(chip.io_bandwidth * package.io_efficiency, board.io_lane_bandwidth)
effective_heat = chip.thermal_output * (1 - package.thermal_transfer)
thermal_overflow = max(0, effective_heat - board_thermal_budget)
```

`frequency_factor` 来源：

```text
effective_frequency = min(chip.frequency_limit, package.frequency_limit, board.clock_limit, rack.clock_policy if installed_in_rack)
frequency_factor = frequency_multiplier(effective_frequency) / frequency_multiplier(chip.native_frequency_tier)

frequency_multiplier 草案：
F1 = 1x
F2 = 2x
F3 = 4x
F4 = 8x
F5 = 16x
```

如果芯片画像中的 `control_ops` 已经按当前运行频率结算，则 `frequency_factor = 1`。如果诊断台回溯到芯片原生设计频率，则使用上面的倍率做归一化。超频、降频和散热限制最终都要落到 `effective_frequency`。

主板 runtime_profile 不是手填，而是由安装的芯片、封装、socket、bus、供电和散热共同生成。

机柜和集群继续沿用同一规则：

```text
rack.available_control_ops = sum(board.effective_control_ops) * rack.power_factor * rack.cooling_factor
rack.external_bandwidth = min(sum(board.external_ports.bandwidth), rack.front_panel_bandwidth, rack.switch_uplink_bandwidth)
cluster.available_cpu_budget = sum(rack.available_control_ops) - reserved_runtime_overhead
cluster.network_fabric_bandwidth = min(sum(rack.external_bandwidth), switch_capacity)
```

`reserved_runtime_overhead` 是集群自身维持成本，来自 DNS、调度器、遥测、服务注册表、缓存刷新和安全余量。实现上可以先用固定比例：

```text
reserved_runtime_overhead = max(fixed_runtime_cost, raw_cluster_cpu_ops * runtime_reserve_ratio)
```

后续文档统一使用 `reserved_runtime_overhead`，不再另设集群保留成本字段。

任务落点仍然保留个体路径：

```text
TaskSpec
-> assigned rack
-> assigned board
-> assigned runtime role
-> assigned chip/socket/port budget
```

运行时可以用聚合参数加速结算，但诊断必须能反推到具体机柜、主板、端口或芯片。

## 3. 芯片设计与合成

芯片采用简化逻辑模块组合。玩家不画晶体管，而是在芯片蓝图里放置逻辑模块、选择位宽、端口、bus、频率和目标封装。

基础模块：

```text
ALU Tile
Register Tile
Cache Tile
I/O Tile
Route Tile
Memory Ctrl Tile
MAC Tile
Clock/PLL Tile
Power Gate Tile
Thermal Pad Tile
```

芯片角色：

```text
control_cpu
route_cpu
io_controller
memory_controller
matrix_accelerator
fiber_controller
wireless_controller
clock_controller
mixed
```

芯片配置：

```text
bit_width: 4 / 8 / 16 / 32 / 64
frequency_tier: F1 / F2 / F3 / F4 / F5
input_ports
output_ports
bidirectional_ports
internal_bus_width
package_target
```

芯片内部 bus 不做逐线仿真，采用 bus 归属：

```text
control_bus
data_bus
memory_bus
io_bus
sync_bus
```

设计检查：

```text
总线是否过载。
模块是否有时钟。
I/O 位宽是否够。
热区是否过度集中。
封装引脚是否够。
```

芯片画像：

```text
control_ops
script_ops
route_ops
io_bandwidth
memory_bandwidth
matrix_ops
frequency_limit
power_draw
thermal_output
yield_score
package_requirement
```

良率：

```text
yield_score =
wafer_quality
* lithography_alignment
* doping_uniformity
* annealing_quality
* cleanliness
/ blueprint_complexity
/ die_area_penalty
```

光刻环境参数可动态变化：

```text
cleanroom_dust
humidity
temperature_stability
vibration
power_noise
mask_wear
photoresist_age
etchant_purity
annealing_curve_drift
operator_alignment
```

这些参数不是玩家直接输入的数字，而是来自 II 型电气合成框架的结构画像和运行状态。

光刻环境应被视为一个多源建模问题，而不是单一机器参数。它由结构画像、世界环境、坐标/维度、声学/振动、动态工艺状态和传感器反馈共同决定。

来源分层：

```text
结构参数
洁净室密封、过滤器、减震结构、机架材料、隔热层。

世界参数
群系、天气、湿度、温度、高度、维度、时间。

坐标/场参数
区块熵流、环境热噪、重力偏差、潮汐力、背景噪声层。

声学/振动
附近机器、活塞、爆破、实体移动、声音事件、流体流动。

工艺参数
掩膜磨损、光刻胶年龄、蚀刻液纯度、退火曲线、电源噪声。

控制参数
玩家设置、传感器采样、模型预测、反馈调参。
```

设计目的：

```text
手动调参可以处理少数显性参数。
真实良率受大量动态参数影响。
玩家搭建传感器网络和学习模型，才能稳定找到工艺窗口。
```

来源：

```text
cleanroom_dust
由洁净室结构、密封材料、过滤器和门禁状态结算。

humidity
由群系、天气、水体邻近、除湿模块和框架密封度结算。

temperature_stability
由热源、冷却模块、相干能稳压和环境温度波动结算。

vibration
由附近机器、爆破/冲击流程、支撑结构和减震模块结算。

power_noise
由电源质量、稳压器、负载波动和电缆质量结算。

mask_wear
由光刻掩膜使用次数、清洗质量和材料等级结算。

photoresist_age
由光刻胶批次、保存条件和时间结算。

etchant_purity
由刻蚀流体、过滤器和污染积累结算。

annealing_curve_drift
由退火炉控制精度、传感器反馈和热惯性结算。

operator_alignment
由光刻投影器对准度、自动控制模型和玩家手动校准结算。
```

模板模式下这些参数仍然后台结算，但 UI 只显示总览：

```text
良率风险：低 / 中 / 高
主要风险项：洁净度 / 对准 / 电源噪声 / 退火漂移
```

蓝图模式和 Runtime 模式可查看完整参数、历史曲线和模型调参建议。

非完美芯片可继续利用：

```text
低频芯片 -> 边缘节点、传感器、低速控制。
高热芯片 -> 低频主板或强散热主板。
I/O 缺陷芯片 -> 内部计算。
矩阵缺陷芯片 -> CPU 辅助或数据处理。
锁相差芯片 -> 单机可用，多卡同步差。
废片 -> 回收材料或作为工艺训练数据。
```

芯片必须记录缺陷标签：

```text
defect_tags:
low_freq
high_heat
io_defect
matrix_defect
sync_drift
dead
```

缺陷来源：

```text
low_freq
frequency_response 或 annealing_curve_drift 未达标。

high_heat
thermal_output 超过同级封装推荐值，或 power_noise 长期偏高。

io_defect
lithography_alignment、pin_mapping_test 或 metal_interconnect_quality 未达标。

matrix_defect
MAC Tile 区域缺陷、etchant_purity 或 mask_wear 导致阵列不完整。

sync_drift
Clock/PLL Tile、operator_alignment 或 temperature_stability 未达标。

dead
核心供电、主 bus、封装连通性或裸片测试失败。
```

缺陷标签由结算因子低于阈值触发，不做纯随机抽选。随机性只用于同等风险下的轻微波动。

## 4. 芯片封装与 socket

封装决定芯片能否上主板、端口如何暴露、散热如何结算。

封装类型：

```text
DIP：低端，少引脚，低频，便宜。
QFP：中端，较多引脚，适合 CPU/I/O。
BGA：高端，高引脚密度，适合 CPU/GPU/内存控制。
Optical BGA：带光口/同步接口，适合集群。
RF Package：带无线接口，适合无线芯片。
```

封装字段：

```text
pin_count
socket_type
thermal_transfer
frequency_limit
port_layout
port_width_limit
special_ports: optical / rf / sync
```

socket 限制不做硬阻断，采用兼容层：

```text
完全匹配：满速。
机械适配：能插，但端口少、频率低或散热差。
转接适配：需要 adapter，占格点，占带宽，有损耗。
```

例子：

```text
QFP-32 可插 QFP-64 插槽，但浪费部分引脚。
BGA 可用转接板接服务器主板，但频率上限下降。
无线封装可转接普通 socket，但天线暴露差。
```

## 5. 主板设计

主板是简化 EDA 玩法。玩家用格点蓝图设计主板，放置芯片 socket、内存、一级储存、晶振、电源、散热和外部端口。

主板尺寸：

```text
5x5：早期控制板。
7x7：通用主板。
9x9：服务器、交换、存储或无线基站主板。
```

主板用途：

```text
general_board
cpu_board
gpu_board
storage_board
switch_board
wireless_base_board
edge_board
```

格点组件：

```text
chip_socket
memory_slot
storage_slot
oscillator_socket
power_input
thermal_zone
fiber_port
wireless_slot
wireless_lane
antenna_mount
frequency_bus_port
redstone_port
internal_bus_trace
sync_trace
```

主板 bus：

```text
control_trace
data_trace
memory_trace
matrix_trace
sync_trace
power_trace
thermal_path
```

bus 设计模式：

```text
手动布线模式
玩家自己在主板格点上画 trace。

系统总线模式
玩家放置芯片和端口后，系统生成推荐 bus trunk 和抽象连接，玩家可接受、微调或局部重画。
```

多层主板：

```text
Layer 0: power / ground
Layer 1: control / low-speed data
Layer 2: memory / high-speed data
Layer 3: matrix / sync / optical prep
```

系统辅助布线只做抽象连接，不追求真实自动布线：

```text
芯片 socket -> 最近 bus trunk
bus trunk -> 目标端口/内存/晶振
```

系统总线模式不是完整自动布线算法，而是生成可编辑的抽象总线骨架。玩家微调的是 trunk 位置、层级、端口归属和关键高带宽路径。

结算：

```text
路径长度
交叉惩罚
层数消耗
带宽拥塞
同步距离差
```

bus_efficiency 草案：

```text
path_penalty = avg_path_length / max(1, board_diagonal_length) * path_weight
crossing_penalty = crossing_count * crossing_weight
layer_penalty = used_layer_count / max_layer_count * layer_weight
congestion_penalty = max(0, requested_bandwidth - trace_bandwidth) / max(1, trace_bandwidth)
sync_penalty = sync_distance_delta / max(1, sync_tolerance)

bus_efficiency = clamp(1 - path_penalty - crossing_penalty - layer_penalty - congestion_penalty - sync_penalty, 0.1, 1)
```

不同 bus 类型可以使用不同权重。例如 control_trace 更怕同步距离差，data_trace 更怕带宽拥塞，power_trace 更怕路径长度和层数消耗。系统总线模式生成的是这些指标的初始解，玩家微调后重新结算。

主板散热组件：

```text
thermal_pad
heat_pipe
cooling_mount
thermal_spreader
cryo_interface
```

散热指标：

```text
hotspot_score
thermal_budget
frequency_sustain
throttle_risk
cooling_interface_count
```

散热结算：

```text
chip_heat = sum(chip.thermal_output)
package_transfer = f(package_type, thermal_transfer, contact_quality)
board_spread = f(thermal_path, heat_pipe, thermal_spreader, hotspot_score)
mount_transfer = f(cooling_mount_count, mount_contact_quality)
rack_cooling = f(fans, liquid_cooling, cryo_interface, pipe_network)
ambient_penalty = f(environment_temperature, biome, dimension)

effective_heat = chip_heat * package_transfer * board_spread * ambient_penalty
effective_cooling = min(board.thermal_budget * mount_transfer, rack_cooling if installed_in_rack else board.thermal_budget)
thermal_headroom = effective_cooling - effective_heat
throttle_risk = max(0, effective_heat - effective_cooling) / max(1, effective_cooling)
frequency_sustain = clamp(1 - throttle_risk, 0, 1)
```

管道网络可参与机柜散热：

```text
coolant_flow
coolant_temperature
pipe_length
pump_pressure
blockage
leak_risk
heat_exchanger_quality
```

诊断台必须能拆分显示：

```text
芯片发热过高。
封装导热不足。
主板热点过于集中。
主板散热接口不足。
机柜冷却预算不足。
冷却管道流量不足或堵塞。
```

上式是默认结算模型，不是固定物理公式。后续高级冷却模块可以替换 `f(...)` 的具体结算，但必须继续输出 `thermal_headroom`、`throttle_risk` 和 TracePath。

无线主板参数：

```text
wireless_lane_width
wireless_session_count
rf_isolation
antenna_exposure
attenuation_penalty
```

主板外部接口支持四向或六向自定义：

```text
north
south
east
west
up
down
```

接口类型：

```text
power_input
cooling_input
cooling_output
fiber_port
copper_data
frequency_bus
redstone_control
wireless_antenna_mount
```

封装输出：

```text
board_profile
port_map
runtime_profile
thermal_profile
power_profile
diagnostic_report
```

## 6. 机柜、机柜族和集群

机柜把多块主板封装为稳定节点，负责供电、冷却、连线、端口暴露和维护风险。

机柜字段：

```text
rack_size
installed_boards
assigned_tasks
current_load
power_budget
power_draw
cooling_budget
cooling_flow
temperature
hotspot_score
liquid_cooling_rate
cryogenic_boost
cable_quality
pipe_layout
front_panel_ports
wireless_exposure
maintenance_access
stability
uptime
fault_flags
network_uplink_usage
storage_io_usage
power_loss_risk
thermal_throttle_risk
```

机柜必须保留个体状态。集群可以生成资源池摘要，但不能把机柜压平成一个总数。

```text
RackState
每个机柜自己的负载、热量、供电、冷却、任务和故障。

ClusterAggregate
调度时使用的聚合摘要，用于快速筛选可用资源。
```

机柜族：

```text
CPU 调度柜族
GPU 推理柜族
训练柜族
存储柜族
交换柜族
无线基站柜族
传感器接入柜族
```

集群封装：

```text
cluster_id
service_roles
resource_pool
scheduler_policy
network_fabric
storage_backend
dns_zone
failure_policy
```

集群需要统一管理结构：

```text
cluster_orchestrator
集群编排核心
```

集群编排核心可以是一个方块、多方块控制器或机柜服务角色。代码层面建议视为 BlockEntity 持有的 `ClusterProfile` 与 `ServiceRegistry`，GUI 负责显示和编辑。

关键字段：

```text
cluster_id
registered_racks
registered_nodes
resource_pool
service_registry
dns_zone
route_policy
scheduler_policy
permission_policy
storage_backends
network_fabric
telemetry_buffer
failure_policy
```

resource_pool：

```text
available_cpu_ops
available_script_ops
available_route_ops
available_io_bandwidth
available_gpu_matrix_ops
available_memory_pages
available_storage_pages
available_network_bandwidth
thermal_headroom
power_headroom
reserved_runtime_overhead
```

与机柜的计算关系：

```text
registered_racks = scan_or_register(server_rack)
registered_nodes = flatten(rack.installed_boards + rack.network_roles)
resource_pool.cpu = sum(rack.available_control_ops where rack.stability ok) - reserved_runtime_overhead
resource_pool.gpu = sum(rack.available_matrix_ops where rack.thermal_throttle_risk below limit)
resource_pool.network = min(sum(rack.external_bandwidth - rack.network_uplink_usage), network_fabric.switch_capacity)
resource_pool.storage = sum(storage_backend.capacity_pages)
thermal_headroom = min(rack.cooling_headroom)
power_headroom = min(rack.power_budget - rack.power_draw)
```

机柜稳定性结算：

```text
power_stability = clamp((power_budget - power_draw) / max(1, power_budget), 0, 1)
cooling_stability = clamp((cooling_budget - current_heat) / max(1, cooling_budget), 0, 1)
cable_stability = cable_quality * (1 - overload_fault_rate)
pipe_stability = f(coolant_flow, blockage, leak_risk)
fault_stability = 0 if fatal_fault else fault_penalty_multiplier

stability = clamp(weighted_mean(power_stability, cooling_stability, cable_stability, pipe_stability, fault_stability), 0, 1)
stability ok = stability >= scheduler_policy.min_rack_stability
```

`reserved_runtime_overhead` 来自集群调度、DNS、遥测、注册表、缓存和安全余量。实现时应保留两类显示：总资源池扣除后的可用值，以及每个机柜自己的未扣除状态。

任务分配仍然落到具体机柜和元件：

```text
task
-> rack_03
-> board_gpu_02
-> runtime role / socket / port
```

诊断应能从集群瓶颈反推：

```text
集群训练慢
-> rack_03 过热降频
-> board_gpu_02 内存链路不足
-> chip_slot_4 封装散热差
```

它整合：

```text
所有机柜资源
主板 runtime_profile
网络拓扑
DNS/service registry
存储中心
任务队列
模型部署
传感器数据源
权限规则
```

## 7. Kamaen Runtime

集群接收统一参数化任务：

```text
TaskSpec
```

字段：

```text
task_id
task_type
entrypoint
inputs
outputs
parameters
resources
runtime
schedule
permissions
failure_policy
metrics
```

entrypoint：

```text
builtin_task
graph_task
script_task
model_task
service_task
external_api_task
```

已知任务类型：

```text
sensor_ingest
data_transform
model_compile
model_inference
model_training
parameter_sync
storage_index
network_service
control_loop
script_job
```

节点性能：

```text
NodeProfile
node_id
node_type
cpu_ops
script_ops
route_ops
io_bandwidth
memory_pages
storage_pages
gpu_matrix_ops
gpu_vram_pages
sync_bandwidth
network_ports
thermal_headroom
power_headroom
reliability
```

运行时吞吐字段由 NodeProfile 派生，不需要玩家单独填写：

```text
node.available_cpu_ops = cpu_ops * frequency_sustain * reliability
node.available_script_ops = script_ops * frequency_sustain * reliability
node.available_io_bandwidth = io_bandwidth * port_availability * congestion_factor
node.available_network_bandwidth = sum(network_ports.available_bandwidth)

node.cpu_ops_per_tick = node.available_cpu_ops * scheduler_policy.cpu_slice
node.script_ops_per_tick = node.available_script_ops * scheduler_policy.script_slice
node.io_bandwidth_per_tick = node.available_io_bandwidth * scheduler_policy.io_slice
node.gpu_matrix_ops_per_tick = gpu_matrix_ops * frequency_sustain * scheduler_policy.gpu_slice
node.service_ops_per_tick = max(node.cpu_ops_per_tick, node.script_ops_per_tick, node.gpu_matrix_ops_per_tick)
path.bandwidth_per_tick = min(each_link.available_bandwidth on TracePath) * route_policy.slice
```

`*_slice` 是调度器给该任务分配的时间片比例。单任务独占时可以近似为 1，多任务并发时由队列和优先级拆分。

任务成本：

```text
TaskCostEstimate
cpu_ops_required
script_ops_required
route_ops_required
io_bandwidth_required
memory_pages_required
storage_pages_required
gpu_matrix_ops_required
network_bandwidth_required
expected_ticks
thermal_load
```

调度输出：

```text
assigned_nodes
expected_latency
expected_throughput
bottleneck
risk
```

简化调度规则：

```text
1. 解析 TaskSpec 输入输出，检查 DataSchema、PortSchema 和权限。
2. 根据 task_type 生成或读取 TaskCostEstimate。
3. 过滤不可用节点：权限不符、端口不符、schema 不符、资源不足、过热或故障。
4. 按任务类型打分候选节点。
5. 优先选择 expected_ticks 较低、thermal_headroom 较高、TracePath 风险较低的节点。
6. 将任务分配到具体 rack、board、runtime role 和端口。
7. 写入 assigned_nodes、expected_latency、bottleneck 和 risk。
```

候选过滤：

```text
cpu_ops_required <= node.available_cpu_ops
script_ops_required <= node.available_script_ops
io_bandwidth_required <= node.available_io_bandwidth
memory_pages_required <= node.available_memory_pages
network_bandwidth_required <= node.available_network_bandwidth
thermal_load <= node.thermal_headroom
PortSchema.required 必须全部可满足
PortSchema.rate 必须小于端口可用吞吐
PortSchema.latency_budget 必须大于 expected_ticks + route_latency
```

expected_ticks 草案：

```text
cpu_ticks = cpu_ops_required / max(1, node.cpu_ops_per_tick)
script_ticks = script_ops_required / max(1, node.script_ops_per_tick)
io_ticks = io_bandwidth_required / max(1, node.io_bandwidth_per_tick)
gpu_ticks = gpu_matrix_ops_required / max(1, node.gpu_matrix_ops_per_tick)
network_ticks = network_bandwidth_required / max(1, path.bandwidth_per_tick)

expected_ticks = ceil(max(cpu_ticks, script_ticks, io_ticks, gpu_ticks, network_ticks))
               + queue_delay
               + route_latency
               + schema_transform_latency
```

延迟项来源：

```text
queue_delay = ceil(queued_required_ops_before_task / max(1, node.service_ops_per_tick))
route_latency = sum(link.latency on TracePath) + dns_lookup_latency + wireless_extra_latency
schema_transform_latency = sum(converter.cost_ticks for required schema conversion)
```

如果任务直接命中本地节点、本地 schema 完全匹配且队列为空，这三项可以为 0。

任务类型可提供基础成本模板：

```text
sensor_ingest
低 cpu_ops、低 memory_pages，成本主要来自采样频率、端口 rate 和写入带宽。

data_transform
吃 script_ops、memory_pages 和 schema_transform_latency。

model_inference
吃 gpu_matrix_ops、parameter bandwidth、activation memory 和 deadline。

network_service
吃 route_ops、packet_buffer、PortSchema.rate 和 DNS/cache 命中率。
```

运行时模块：

```text
Scheduler
Resource Manager
Page Store
Service Registry
Message Bus
Permission Manager
Runtime Sandbox
Telemetry
```

脚本可以图灵完备，但必须受预算限制：

```text
instruction_budget
memory_budget
io_budget
network_budget
tick_budget
permission_scope
```

脚本分层：

```text
配置图
非图灵完备，安全、可视化，适合大多数玩家。

受限脚本
接近 eBPF/Lua/Forth 风格，有循环和状态，但预算受限。

完整运行时
后期高级玩法，部署在专门 CPU/集群上，强制沙箱、权限和资源配额。
```

脚本三层与复杂度入口的关系：

```text
模板模式
使用配置图，不要求玩家写脚本。

蓝图模式
使用配置图，允许少量受限脚本作为 route_node 或 data_transform 的扩展。

Runtime 模式
允许受限脚本和后期完整运行时，必须部署在主板节点、专用 runtime node 或 cluster_orchestrator 管理的集群资源上。
```

切换路径：

```text
配置图可以导出为受限脚本草案。
受限脚本可以被封装为 ModuleArtifact。
完整运行时不能自动由普通配置图升级，必须显式部署并通过权限审查。
```

## 8. Schema 与任务 I/O

所有任务、脚本、模型、传感器、存储和网络服务都声明输入输出格式。

核心结构：

```text
DataSchema
PortSchema
TaskIOMap
Transform
```

转换与适配对象按层分化，不使用统一物品名：

```text
硬件层
socket_adapter / port_adapter，解决封装、socket、端口方向和物理接口不兼容。

数据层
schema_converter / data_transform，解决 DataSchema、shape、dtype、单位、精度和窗口不兼容。

传感器层
reader_adapter / mod_adapter，解决原版、Kamaen 标准接口、Capability 和白名单模组读取。

网络层
protocol_bridge / gateway_rule，解决协议、地址域、权限域和网关转发差异。
```

这些对象共享诊断字段，但不强行统一实现：

```text
input
output
compatibility
loss_or_cost
resource_cost
error_report
```

DataSchema：

```text
schema_id
base_type
shape
dtype
unit
tags
timestamp_policy
confidence_policy
nullable
version
```

PortSchema：

```text
port_id
direction
accepted_schemas
produced_schema
required
rate
batching
latency_budget
```

TaskIOMap：

```text
from_task
from_port
to_task
to_port
transform
```

匹配结果：

```text
Exact：完全匹配，直接连接。
Convertible：可转换，需要转换器，消耗资源。
Invalid：不可连接，必须改 schema 或插入处理任务。
```

常见转换：

```text
cast_dtype
normalize
reshape
window
select_fields
encode_tags
scale
offset
clamp
```

错误信息必须给出可执行建议：

```text
缺字段
shape 错误
dtype 错误
版本不匹配
延迟超预算
权限不足
需要插入 data_transform 节点
```

## 9. 传感器系统

卡玛恩探针是统一读数核心，其他传感器是探针的专用化、阵列化、同步化和网络化。

流程：

```text
目标对象
-> Reader / Adapter
-> InfoSignal / SensorFrame
-> DataSchema
-> 数据处理 / 存储 / 模型输入
```

可读对象：

```text
物品：id、tag、数量、耐久、NBT 摘要、模组 Data Component。
方块：BlockState、红石强度、朝向、含水、光照、硬度、容器状态。
方块实体：能量、流体、库存、进度、温度、压力、配方状态。
环境：温度、湿度、光照、天气、群系、维度、热噪、重力、潮汐力。
实体：生命值、速度、位置、朝向、标签、AI 状态、目标、背包摘要。
模组内机器：工艺阶段、良率参数、热量、供电、散热、污染、对准度。
网络/硬件：端口流量、队列、延迟、功耗、热量、算力利用率。
```

读取等级：

```text
S0 原版公开读数
S1 Kamaen 标准接口
S2 Capability / API Adapter
S3 白名单高级 Adapter
S4 环境/维度场采样
```

传感器不能默认读取所有模组内部字段。跨模组高级读取必须通过白名单 Adapter。

物理范围和数据字段：

```text
name
base_type: scalar/vector/grid/event/tagset/text
dtype
unit
min_value
max_value
default_value
confidence
timestamp
source_id
precision
noise_level
stale_ticks
missing_reason
source_range
```

采样策略：

```text
fixed_interval
on_change
threshold
redstone_trigger
task_trigger
manual_probe
```

触发参数：

```text
lower_bound
upper_bound
deadband
hysteresis
cooldown
```

近段历史：

```text
last_value
min_recent
max_recent
mean_recent
delta
slope
sample_count
last_n_values
```

基础处理：

```text
round / quantize
scale
offset
add / subtract / multiply / divide
clamp
normalize
moving_average
delta
threshold_to_bool
discretize
one_hot / tag encode
```

传感器空间范围：

```text
point
line
box
sphere
cone
chunk
multiblock_profile
```

事件型传感器：

```text
block_changed
entity_entered
redstone_edge
machine_stage_changed
threshold_crossed
item_inserted
packet_received
```

同步结构：

```text
sensor_base
传感器底座，容纳多个探针/传感器模块，聚合为一个采样点。

sensor_syncer
传感器同步器，按时间窗口收集多个传感器值，生成同一行数据。

sensor_table
数据表，保存 schema、列定义、行数据、时间戳和缺失值。
```

同步行示例：

```text
timestamp
source_group
temperature
humidity
redstone_power
machine_progress
thermal_noise
entity_count
confidence_flags
```

缺失标记：

```text
missing
stale
interpolated
defaulted
```

传感器到模型输入的数据链路：

```text
SensorFrame
-> sensor_syncer 聚合时间窗口
-> SensorTable row
-> DataSchema 检查
-> data_transform 任务，可选
-> ModelInput schema
-> kamaen_io_gateway
-> RuntimeGraph input node
```

如果 SensorTable row 与模型输入 schema 完全匹配，`kamaen_io_gateway` 可以直接读取。若字段单位、精度、离散/连续类型或窗口长度不匹配，则必须插入 `data_transform` 任务；该任务消耗 `script_ops`、`memory_pages` 和 `schema_transform_latency`。若缺少 required 字段，则编译器或运行时直接报错。

## 10. 模型基础组件

模型系统不提供大量专用神经网络方块。所有模型、脚本、反馈和数据处理都由少数通用组件组成。CNN、MoE、VAE、Diffusion、Embedding、损失函数和控制器都是可拆解模板。

基础方块：

```text
kamaen_io_gateway
kamaen_data_node
kamaen_route_node
kamaen_trigger_node
kamaen_register_node
kamaen_graph_compiler
```

IO 网关：

```text
传感器输入
数据表输入
存储页输入/输出
模型输入/输出
红石/执行器输出
网络/集群任务输入输出
```

数据节点：

```text
input
activation
parameter_ref
metric
feedback
output
```

路由节点：

```text
direct
broadcast
merge
conditional
top_k
weighted_merge
lookup
window
normalize
reshape
cast
scale
clamp
simple_math
```

触发器节点：

```text
on_input_ready
on_timer
on_change
on_threshold
on_route_complete
on_feedback
manual
loop
```

寄存器节点：

```text
hidden
latent
history
counter
accumulator
optimizer_state
last_value
```

图封装/编译器：

```text
扫描 graph
检查 ID
检查 schema
检查循环预算
检查端口连接
估算硬件成本
生成 RuntimeGraph
封装为 ModuleArtifact / ModelArtifact
```

模型图到 TaskCostEstimate 的桥接：

```text
RuntimeGraph
-> GraphCompiler 扫描模板、shape、batch、量化、循环预算
-> OperatorCostTable 匹配硬件元函数
-> TaskCostEstimate
-> Scheduler
```

OperatorCostTable 草案：

```text
LinearBlock / WeightedSumBlock
主要消耗 gpu_matrix_ops，附带 memory_pages 和 parameter bandwidth。

EmbeddingBlock / lookup
主要消耗 memory_pages、io_bandwidth 和 cache hit rate。

NormalizeBlock / PoolBlock / simple_math
主要消耗 script_ops 或 reduction_ops，可落到 CPU 或 GPU。

AttentionBlock
消耗 gpu_matrix_ops、activation memory、sync_bandwidth 和 route_ops。

MoEBlock
额外消耗 route_ops、top_k 路由和条件触发预算。

DiffusionStepBlock / VAEBlock
按重复步数、latent shape 和参数页读取次数放大成本。
```

因此玩家看到的“模型跑不动”诊断应能拆成：矩阵吞吐不足、参数页带宽不足、激活内存不足、路由/同步成本过高、schema 转换成本过高等。

ID 作用域：

```text
local:
export:
remote:
param:
state:
sensor:
table:
```

常用封装模板：

```text
LinearBlock
WeightedSumBlock
EmbeddingBlock
PoolBlock
NormalizeBlock
AttentionBlock
MoEBlock
ResidualBlock
VAEEncoderBlock
VAEDecoderBlock
DiffusionStepBlock
SensorFusionBlock
ControlLoopBlock
LossMetricBlock
OptimizerRequestBlock
```

模板不是独立不可修改方块，而是预配置的 IO、数据、路由、触发器、寄存器网络。

模板创建流程：

```text
1. 玩家用基础方块搭建 graph。
2. kamaen_graph_compiler 扫描 graph，检查 ID、schema、端口和循环预算。
3. 玩家选择暴露哪些 local id 为 export 端口。
4. 编译器生成 ModuleArtifact 或 ModelArtifact。
5. 模板可复制、版本化、部署，也可以拆开回到基础 graph 继续编辑。
```

系统内置模板也是预制 ModuleArtifact，不是额外的不可修改方块。`kamaen_graph_compiler` 同时承担图编译、模板保存、模板检查和模板展开功能。

## 11. 网络通信

网络系统是游戏内仿真。无线实际仍在游戏内，但仿真带宽、延迟、范围、会话、干扰、信号衰减和协议代际。

网络节点不是魔法线缆，而是普通计算节点安装网络职能模块后形成的专用节点。

核心方块：

```text
network_role_module
网络职能模块
```

节点模式：

```text
switch_mode
router_mode
wireless_ap_mode
dns_mode
auth_mode
gateway_mode
monitor_mode
```

第一版节点：

```text
switch_mode
wireless_ap_mode
dns_mode
gateway_mode
```

网络服务：

```text
packet_forwarder
resolver
auth_checker
queue_manager
telemetry
```

无线信号站：

```text
wireless_signal_station
```

无线代际：

```text
G1：控制命令，低带宽，高范围。
G2：少量传感器数据。
G3：状态同步和小数据块。
G4：普通传感器流和轻量模型请求。
G5：低延迟推理请求和边缘计算。
G6：高密度传感器网和跨基地高速无线。
```

无线代际只影响：

```text
bandwidth
latency
session_limit
range
interference_resistance
power_draw
```

相对倍率草案，以 G1 为基准：

```text
generation | bandwidth | latency | session_limit | range | interference_resistance | power_draw
G1         | 1x        | 5x      | 1x            | 4x    | 1x                      | 1x
G2         | 4x        | 4x      | 2x            | 3.5x  | 1.2x                    | 1.4x
G3         | 12x       | 3x      | 4x            | 3x    | 1.5x                    | 2x
G4         | 32x       | 2x      | 8x            | 2.5x  | 2x                      | 3x
G5         | 96x       | 1x      | 16x           | 2x    | 2.5x                    | 4.5x
G6         | 256x      | 0.7x    | 32x           | 1.5x  | 3x                      | 7x
```

无线策略修正：

```text
range_priority
range * 1.5, bandwidth * 0.7, latency * 1.2

bandwidth_priority
bandwidth * 1.4, range * 0.75, power_draw * 1.2

low_latency
latency * 0.7, power_draw * 1.3, session_limit * 0.8

sensor_dense
session_limit * 1.5, small_packet_efficiency * 1.4, bandwidth * 0.9

model_request
latency * 0.85, bandwidth * 1.15, session_limit * 0.9
```

主板与机柜会继续修正无线参数：

```text
effective_bandwidth = generation_bandwidth * wireless_lane_width * rf_isolation * antenna_exposure
effective_range = generation_range * antenna_exposure / max(1, attenuation_penalty)
interference = density_penalty / interference_resistance
```

无线密度与小包效率：

```text
local_wireless_density = nearby_active_wireless_nodes / max(1, rf_isolation_radius)
session_pressure = active_sessions / max(1, session_limit)
shield_penalty = 1 - rf_isolation

density_penalty = local_wireless_density * density_weight + session_pressure * session_weight + shield_penalty

small_packet_efficiency = clamp(1 + cache_hit_rate * 0.3 + batching_quality * 0.3 - header_overhead_ratio, 0.5, 1.5)
```

高密度无线主板不是完全禁止，而是会提高 `density_penalty`。使用更好的隔离、外置天线、基站机柜或传感器密集策略可以把惩罚转成可控的工程问题。

无线策略：

```text
range_priority
bandwidth_priority
low_latency
sensor_dense
model_request
```

配置分层：

```text
模板配置
小型交换机、无线传感器站、模型推理网关、存储中心上联、DNS 服务节点。

表格配置
端口表、服务表、地址表、路由表、权限表、QoS 表。

高级脚本
包过滤、路由策略、认证策略、负载均衡脚本。
```

配置页：

```text
PortMapPage
AddressPage
RoutePage
ServicePage
AuthPage
WirelessProfilePage
```

## 12. 地址系统与多 DNS

地址分五类。

节点地址：

```text
knode://<scope>/<zone>/<node_id>
```

例子：

```text
knode://base/main/rack_01
knode://base/farm/sensor_hub_03
knode://cluster/train/gpu_rack_02
knode://remote/nether/gateway_01
```

端口地址：

```text
kport://<scope>/<zone>/<node_id>/<port_id>
```

例子：

```text
kport://base/main/rack_01/fiber_0
kport://base/farm/sensor_hub_03/out
kport://cluster/train/gpu_rack_02/model_in
```

服务地址：

```text
ksvc://<domain>/<service>/<version>
```

例子：

```text
ksvc://farm/sensor.temperature/v1
ksvc://model/irrigation.infer/v3
ksvc://storage/terrain.height/v1
ksvc://dns/root/v1
ksvc://auth/base/v1
```

数据地址：

```text
kdata://<domain>/<dataset_or_page>/<version>#<path>
```

例子：

```text
kdata://farm/temperature_dataset/v1#chunk_0004
kdata://model/irrigation_params/v3#page_12
kdata://storage/terrain_height/v1#region_0_0
```

本地地址：

```text
local:<name>
param:<name>
state:<name>
table:<name>
sensor:<name>
```

多 DNS 是网络子系统第一版必做内容。计算基础设施 MVP 可以只保留本地服务解析和兼容地址格式，但进入网络子系统第一版时必须补齐 root/zone/cache/local resolver。

DNS 节点类型：

```text
root_dns
zone_dns
cache_dns
local_resolver
```

解析顺序：

```text
local cache
-> local zone_dns
-> parent zone_dns
-> root_dns
-> remote gateway dns
```

记录类型：

```text
NODE
PORT
DATA
MODEL
SENSOR
AUTH
GATEWAY
ALIAS
```

DNS 表字段：

```text
name
record_type
target
ttl
priority
permission
status
owner_node
version_policy
last_heartbeat
```

DNS 记录生命周期：

```text
手动注册
玩家在 DNS 表中创建记录，适合固定服务、别名和外部网关。

服务启动自动注册
network_service、model_service、sensor_hub 或 storage_backend 启动时向 zone_dns 注册。

心跳续约
服务周期发送 heartbeat，刷新 ttl 和 last_heartbeat。

TTL 过期
记录进入 stale 状态。若 stale_allowed=true，可继续短期使用缓存并显示风险。

服务停止注销
服务正常停止时删除或禁用记录。

异常失联
heartbeat 超时后标记 STALE_CACHE，下一次查询尝试重新解析或走 fallback。
```

错误触发：

```text
NXDOMAIN
当前 DNS 链找不到 name。

TIMEOUT
DNS 节点不可达或查询超出 latency_budget。

PERMISSION_DENIED
请求方无权解析该记录。

STALE_CACHE
ttl 过期且无法刷新，但本地仍有旧记录。

LOOP_DETECTED
DNS 转发链出现重复节点或重复 zone。

VERSION_MISMATCH
请求 exact 版本不存在，或 latest compatible 找不到兼容 schema/protocol。
```

DNS 错误：

```text
NXDOMAIN
TIMEOUT
PERMISSION_DENIED
STALE_CACHE
LOOP_DETECTED
VERSION_MISMATCH
```

地址别名：

```text
@farm_temp -> ksvc://farm/sensor.temperature/v1
```

版本策略：

```text
exact v3
latest compatible
fallback v2
```

离线缓存：

```text
cache_valid_ticks
stale_allowed
```

## 13. Packet Header 与通信流程

底层请求头完整，UI 默认只显示来源、目标、类型、优先级、权限和状态。

PacketHeader：

```text
packet_id
protocol_version
src_node
src_port
dst_service
dst_resolved
packet_type
schema_id
payload_ref
timestamp
ttl
priority
qos
auth_token
permission_scope
trace_id
reply_to
compression
encryption
```

压缩与加密：

```text
compression = none / fast / dense
encryption = none / signed / encrypted
```

初版可以默认 `none`。启用压缩时，payload 带宽消耗下降，但会增加 `cpu_ops_required` 或 `script_ops_required`；启用签名/加密时，会增加认证延迟、CPU 成本和密钥/权限检查成本。是否允许启用由服务端口、权限策略和网络节点能力共同决定。

payload_ref：

```text
inline_payload
memory_page
storage_page
parameter_page
dataset_shard
external_ref
```

发起流程：

```text
Task / Script / Model / Trigger
-> create Packet
-> resolve dst_service through DNS
-> permission/auth check
-> route planning
-> enqueue to network node
-> switch/router/wireless forwarding
-> receiver port
-> schema check
-> task callback or message queue
```

接收流程：

```text
port receives Packet
-> validate header
-> auth check
-> schema check
-> dispatch by packet_type/service
-> write to queue/register/data node
-> trigger runtime task
-> optional reply
```

协议族：

```text
KNP-Control
KNP-Sensor
KNP-Data
KNP-Model
KNP-Param
KNP-Metric
```

协议族与包类型关系：

```text
KNP-Control -> ControlPacket, ConfigUpdate, Heartbeat, FaultReport
KNP-Sensor -> SensorFrame, SensorBatch, TriggerEvent
KNP-Data -> DataChunk, TableRow, StoragePageRef
KNP-Model -> ModelInput, ModelOutput, ActivationChunk
KNP-Param -> ParameterPage, ParameterVersion, OptimizerState
KNP-Metric -> MetricReport, TraceReport, DiagnosticReport
```

KNP-* 是协议族，用于权限、路由和端口策略；`packet_type` 是具体包类型，用于接收端分发。

玩家可自定义协议，但必须声明：

```text
packet_type
schema
allowed_ports
max_payload
resource_cost
```

## 14. 可视化与诊断

抽象系统必须可见。

至少显示：

```text
端口连接表
Schema 匹配状态
数据包流向
CPU/GPU/网络/存储利用率
热量和供电
任务队列
错误日志
DNS 解析路径
无线信号质量
传感器最近 N 次曲线
```

诊断优先级：

```text
数据格式错
-> 缺转换器
-> 端口带宽不足
-> CPU 脚本预算不足
-> 存储/网络延迟超预算
-> 供电或散热导致降频
```

网络错误：

```text
DNS 未解析
权限拒绝
schema 不匹配
端口堵塞
无线信号弱
路由无下一跳
目标队列满
```

## 15. 复杂度分层

给玩家三种入口：

```text
模板模式
直接用预设芯片、主板、网络、传感器、模型模板。

蓝图模式
改芯片、主板、端口、bus、封装、机柜和网络表。

Runtime 模式
写脚本、定义 schema、配置任务、调集群、改路由策略。
```

预设模板必须覆盖：

```text
基础控制芯片
传感器采集主板
小型推理节点
存储节点
光纤交换机
无线基站
DNS 服务节点
模型数据处理链
```

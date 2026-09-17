# Kamaen Info 计算基础设施 MVP 路线

状态：历史草案 / 暂缓实现。当前第一阶段改为卡玛恩晶体原型、晶体画像、向量爆破写入、InfoSignal 和频率总线闭环；本文件不作为当前 MVP 排期依据。

## 1. MVP 目标

第一阶段只验证一条完整、可玩、可诊断的最小链路：

```text
ALU/控制芯片设计
-> 简单 CPU 芯片封装
-> 通用主板蓝图
-> 单机运行传感器数据处理任务
-> 诊断 CPU、内存、端口、散热和供电瓶颈
```

MVP 不追求训练大模型、真实无线网络、机柜族、跨维度网络或复杂集群。

## 2. MVP 必做系统

### 2.1 芯片蓝图

只做控制芯片和少量模块。

模块：

```text
ALU Tile
Register Tile
I/O Tile
Clock/PLL Tile
Thermal Pad Tile
```

MVP 中的 Clock/PLL Tile 只启用低阶时钟能力，暂不开放复杂锁相、同步漂移和多卡同步玩法。

配置：

```text
bit_width: 4 / 8
frequency_tier: F1 / F2
input_ports
output_ports
internal_bus_width
```

输出：

```text
control_ops
script_ops
io_bandwidth
power_draw
thermal_output
yield_score
```

### 2.2 芯片封装

只做：

```text
DIP
QFP
```

封装检查：

```text
pin_count 是否足够。
frequency_limit 是否覆盖芯片频率。
thermal_transfer 是否足够。
socket_type 是否能进入目标主板。
```

### 2.3 主板蓝图

只做 5x5 通用主板。

组件：

```text
chip_socket
memory_slot
storage_slot
oscillator_socket
power_input
thermal_zone
sensor_input_port
storage_output_port
control_trace
data_trace
power_trace
```

bus 模式：

```text
手动布线
系统总线模式（辅助直连）
```

MVP 不做多层复杂布线，只实现完整路径中 Layer 0/1 的子集：

```text
Layer 0: power
Layer 1: control/data
```

输出：

```text
board_profile
port_map
runtime_profile
thermal_profile
power_profile
diagnostic_report
```

### 2.4 传感器 MVP

核心方块：

```text
kamaen_probe_station
sensor_base
sensor_syncer
sensor_table
```

首批读数：

```text
block_state
redstone_power
item_tagset
machine_progress
energy_level
local_temperature
thermal_noise
entity_count
```

采样方式：

```text
fixed_interval
threshold
redstone_trigger
manual_probe
```

基础处理：

```text
round
scale
offset
clamp
normalize
moving_average
delta
threshold_to_bool
```

输出：

```text
SensorFrame
SensorTable row
```

### 2.5 Runtime MVP

只做单机主板节点，不做真正集群。

任务类型：

```text
sensor_ingest
data_transform
storage_index
script_job
```

TaskSpec 字段：

```text
task_id
task_type
inputs
outputs
parameters
resources
schedule
permissions
metrics
```

资源预算：

```text
cpu_ops
script_ops
io_bandwidth
memory_pages
storage_pages
tick_budget
```

脚本 MVP 只做配置图或受限表达，不做完整图灵完备运行时。

### 2.6 Schema MVP

必须做：

```text
DataSchema
PortSchema
TaskIOMap
```

匹配结果：

```text
Exact
Convertible
Invalid
```

首批转换：

```text
cast_dtype
normalize
scale
offset
clamp
select_fields
```

错误显示必须清楚：

```text
缺字段
shape 错误
dtype 错误
版本不匹配
权限不足
需要插入 data_transform
```

### 2.7 网络 MVP

第一阶段网络只做本地节点通信，不做完整无线代际和多 DNS。

必做：

```text
kamaen_io_gateway
network_role_module
network_config_terminal
```

可选早期节点：

```text
switch_mode
dns_mode
```

地址只需支持：

```text
local:<name>
kport://base/main/<node_id>/<port_id>
ksvc://local/<service>/v1
```

PacketHeader MVP：

```text
src_port
dst_service
dst_resolved
packet_type
schema_id
payload_ref
timestamp
ttl
priority
trace_id
```

多 DNS、无线代际、认证节点、网关节点留到第二阶段。这里的第二阶段指基础设施 MVP 之后的网络子系统第一版；地址格式在 MVP 期就要保持兼容。

## 3. MVP 方块/物品清单

硬件：

```text
logic_module_plate
chip_blueprint_writer
chip_packaging_station
packaged_logic_chip
motherboard_blueprint
configurable_motherboard
hardware_diagnostic_station
```

传感器：

```text
kamaen_probe_station
sensor_base
sensor_syncer
sensor_table
```

Runtime / 数据：

```text
kamaen_io_gateway
kamaen_data_node
kamaen_route_node
kamaen_trigger_node
kamaen_register_node
kamaen_graph_compiler
memory_page
storage_center_controller 或简化 storage_page_block
```

网络：

```text
network_role_module
network_config_terminal
```

## 4. MVP 暂不做

```text
GPU/NPU 大规模矩阵加速。
MoE、VAE、Diffusion 的完整模板。
机柜族和跨基地集群。
完整 1G-6G 无线。
多级 root/zone/cache DNS 的完整玩法。
跨维度通信。
真实外部 API 后端。
完整图灵完备脚本运行时。
复杂多层自动布线算法。
跨模组高级 Adapter 大规模支持。
```

这些内容要保持接口兼容，但不阻塞第一阶段。

## 5. MVP 验收目标

玩家可以完成：

```text
1. 用芯片蓝图台设计一个 4-bit 或 8-bit 控制芯片。
2. 用封装台把芯片封装为 DIP 或 QFP 芯片。
3. 用主板蓝图编辑 5x5 通用主板，放入芯片、晶振、内存、储存和端口。
4. 接入卡玛恩探针或传感器底座。
5. 设定采样频率、上下限和基础处理。
6. 生成 SensorFrame。
7. 通过 Runtime 任务把传感器数据写入 SensorTable 或存储页。
8. 打开诊断台看到 CPU、I/O、内存、散热、供电和 schema 匹配报告。
```

验收时必须能看到：

```text
芯片性能画像。
主板端口连接表。
芯片 -> 封装 -> 主板的 TracePath。
传感器最近 N 次曲线。
DataSchema / PortSchema 匹配状态。
任务队列和资源消耗。
错误日志和修复建议。
硬件瓶颈报告。
```

MVP 的诊断也要遵守“聚合不抹除个体”原则。即使只做单机主板，也应能从 `runtime_profile` 反推到具体芯片、封装、bus、端口或散热组件。

## 6. 第二阶段入口

MVP 跑通后，按以下顺序扩展：

```text
1. 机柜封装：供电、冷却、理线、主板安装。
2. 光纤交换机：多端口转发和服务访问。
3. 多 DNS：root_dns、zone_dns、cache_dns、local_resolver。
4. 无线信号站：G1-G6、策略、覆盖、并发、衰减。
5. 模型模板：Embedding、Pool、Linear、MoE、VAE、DiffusionStep。
6. GPU/NPU：MAC Tile、矩阵 bus、显存页、模型推理任务。
7. 集群编排核心：ClusterProfile、服务注册、任务分片。
```

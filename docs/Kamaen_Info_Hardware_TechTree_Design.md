# Kamaen Info 硬件科技树与计算网络设计

版本：v0.4 Historical Draft  
状态：历史草案 / 暂缓实现。本文保留早期“电气硬件与计算基础设施”设想，当前主线已改为“电只供能，信息走晶体共振、频率总线、光路和全光计算”。开发排期以 `Kamaen_Info_Core_Gameplay_Development_Plan.md`、`Kamaen_Info_GDD.md`、`Kamaen_Info_TechTree_Plan.md` 和 `Kamaen_Info_Optical_Computing_Design.md` 为准；本文不得作为当前 CPU/GPU/NPU 或主板/机柜路线的实现依据。

## 1. 设计定位

硬件系统不追求真实计算机、电路、电磁场、芯片版图或操作系统模拟，而是做一套可设计、可制造、可封装、可组网、可诊断的计算基础设施玩法。玩家的目标不是合成一台“最终电脑”，而是从芯片蓝图到集群调度逐层搭建模型训练、推理、传感器数据处理、存储和传输所需的基础设施。

硬件系统服务三个目标：

- 限制模型训练、推理、加载、通信和自动化控制的性能上限。
- 提供复杂且可分阶段推进的合成与制造玩法。
- 为后续模型自动化工艺调参提供需求，让玩家用低级计算系统制造更高级计算系统。

硬件玩法的核心不是“合成一个最终电脑”，而是搭建一个由 CPU、GPU/NPU、主板、内存页、参数库、光纤集群、无线公网和地址索引共同组成的信息计算基础设施。

推荐核心循环：

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

## 2. 核心原则

- CPU 与 GPU/NPU 的设计目标不同。CPU 优化调度、脚本、路由、I/O 和模型图组织；GPU/NPU 根据模型算子和元函数提供硬件加速。
- 晶振不作为随机错误来源，而作为频率协议、同步域和带宽等级的约束。
- 内存和储存不做复杂架构玩法，主要作为模型地址空间、参数页、状态页和长期快照的实体化表示。
- 通信分为模型内通信、硬件内通信、短距离集群通信和长距离无线通信。
- 第一版优先采用确定性限制，不设计漂移、随机损坏或不可控错误。
- 玩家应能通过诊断设备明确看到瓶颈，而不是猜测复杂系统内部发生了什么。

硬边界：

```text
不模拟晶体管级电路。
不模拟真实电磁场。
不模拟完整操作系统或真实网络协议栈。
不在服务端 tick 内运行真实深度学习。
不要求玩家配置真实 DNS、真实 TCP/IP 或真实驱动。
```

允许的自由度：

```text
芯片模块组合、位宽、端口和封装。
主板格点蓝图、端口方向、芯片组和总线。
机柜供电、冷却、理线、交换机和管道。
集群任务分片、调度、服务发现和数据流。
传感器采样、数据处理、存储、传输和模型映射。
```

系统所有复杂度都应通过少量可读指标表达，避免把玩家推入真实工程细节。

### 2.1 六层计算基础设施

硬件玩法按六层拆分，每层只保留有限核心指标。

```text
芯片层
模块、位宽、频率、端口、热。

封装层
引脚/接口、端口分布、散热、频率上限、主板兼容性。

主板层
总线、内存、一级储存、端口、供电、散热。

机柜层
算力密度、供电、冷却、连线、掉电/过热风险。

集群层
调度、交换、带宽、存储、DNS/服务发现、任务分片。

模型层
参数加载、推理、训练、传感器输入、运行可视化。
```

这六层的关系：

```text
芯片输出算力和 I/O 单元
-> 封装决定接口和热边界
-> 主板决定本机资源组织
-> 机柜决定密度和稳定运行
-> 集群决定任务拆分和网络效率
-> 模型层消耗算力、内存、带宽、存储和调度预算
```

## 3. 频率协议与晶振

晶振是硬件时钟标准、通信协议等级和同步域钥匙。它不制造随机故障，只决定兼容性、带宽、同步效率和可接入设备等级。

建议频率等级：

```text
F1 控制频段
红石转换、触发器、低速 InfoSignal、小型控制器。

F2 数据频段
模型内网、内存页、参数页、小模型部署、主板基础通信。

F3 矩阵/激活频段
GPU/NPU 激活流、batch 数据、参数加载、多卡基础同步。

F4 光频协议
训练集群、多卡互连、高速模型服务、参数同步。

F5 维度锁相协议
跨维度通信、世界之心、创世编译、维度级模型部署。
```

连接规则：

```text
同频设备：满速连接。
相邻频段：需要频率桥或兼容接口，带宽下降。
差距过大：不能直接连接。
```

代表组件：

```text
粗制石英晶振
F1 基准晶振
F2 数据晶振
F3 矩阵同步晶振
F4 锁相光频晶振
F5 维度同步晶振
频率桥
锁相接口
多卡锁相器
```

## 4. 芯片蓝图与封装

芯片层采用“简化逻辑模块组合”，参考 MCU 配置工具和 EDA 的体验，但只抽象到可结算的指标。玩家不画晶体管，而是在芯片蓝图中放置逻辑模块、选择位宽、端口、频率和封装方向。

### 4.1 逻辑模块

基础芯片模块：

```text
ALU
整数控制运算，提升 control_ops、script_ops 和小规模数据处理。

寄存器组
提升状态机、低延迟控制和小任务切换。

缓存块
提升热路径、参数索引、协议处理和重复请求。

乘加阵列
提升 matrix_ops、vector_ops 和小型模型推理。

路由控制单元
提升 route_ops、packet_filter 和端口转发效率。

I/O 控制器
提升外部端口、传感器接入和储存访问。

内存控制器
提升 memory_bandwidth、page_load 和参数页访问。

无线控制器
提供无线会话、基站协议和远程访问能力。

光纤控制器
提供 F4 光纤口、参数同步和集群互连能力。

晶振/锁相单元
决定频率等级、同步域和多芯片协调效率。
```

芯片蓝图字段：

```text
chip_role: cpu/gpu_npu/io/network/storage/wireless/mixed
bit_width: 4/8/16/32/64
module_counts
input_ports
output_ports
bidirectional_ports
internal_bus_width
frequency_tier
clock_domain
thermal_class
```

第一版不需要让每个逻辑门单独模拟。ALU、寄存器、缓存、乘加阵列、I/O 单元等只作为蓝图模块参与公式。

### 4.2 芯片评分公式

芯片输出一组性能画像，而不是单一等级。

```text
control_ops = ALU * bit_width * frequency * yield_factor
script_ops = ALU * cache_factor * frequency * yield_factor
matrix_ops = multiply_accumulate_array * bit_width * frequency * operator_factor
route_ops = route_units * port_count * frequency * protocol_factor
io_bandwidth = io_controllers * port_width * frequency * package_efficiency
memory_bandwidth = memory_controllers * bus_width * frequency * package_efficiency
thermal_output = module_complexity * frequency^2 * package_loss
power_draw = active_modules * bit_width * frequency * voltage_factor
yield_score = process_quality / blueprint_complexity / die_area_penalty
```

这些公式只需保持相对关系清晰，不需要追求现实数值。诊断台显示公式拆项，让玩家知道瓶颈来自模块不足、位宽不足、频率过高、封装差、良率低还是散热不足。

### 4.3 芯片封装

芯片制造后必须封装才能进入主板。封装决定引脚、接口、散热、频率上限和主板兼容性。

```text
DIP 封装
低端，接口少，散热差，便宜，适合早期控制芯片。

QFP 封装
中端，接口较多，适合 CPU、I/O 和网络控制芯片。

BGA 封装
高端，接口密度高，适合 CPU、GPU/NPU 和内存控制器。

光电混合封装
支持光纤口、F4 同步和高带宽互连，成本高。

无线封装
支持天线和无线协议，但高密度摆放会产生信号衰减。
```

封装字段：

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

封装阶段把芯片蓝图的内部端口映射成主板可连接接口。玩家可以选择端口分布，但接口数、位宽和散热都受封装类型限制。

## 5. CPU 设计

CPU 不负责大规模矩阵计算，主要负责控制、调度、路由、脚本和数据组织。

CPU 蓝图由功能模块配比决定，而不是直接模拟 ARM、x86 或 RISC-V 等现实架构。现实架构只作为灵感，不作为必须复刻的规则。

**阶段边界**：第 5 阶段的 CPU 是电气控制芯片，承担自动化、路由、脚本和 I/O。进入第 6 阶段后，计算路径由 `photonic_control_core`（光控制核）接管：光逻辑门与双稳态晶胞在游戏设定中成立，承担原电气 CPU 的控制职能。第 5 阶段电气 CPU 仍可作为外层接口、维护终端或兼容控制器保留，但不再是第 6 阶段计算域的核心。

### 5.1 CPU 基础模块

```text
ALU 阵列
提升 control_ops、script_ops 和小规模 vector_ops。

南桥 I/O 阵列
提升 route_ops、io_ops、传感器协调、存储访问和网络包处理。

缓存阵列
提升参数索引、重复模型调用、脚本热路径、触发器队列和模型图编译效率。

高速同步接口
提升与 GPU/NPU、内存页、参数库、光纤芯片和主板总线的协同效率。

优化核心
负责图编译、算子融合、shape 固定、批处理规划和 GPU/NPU 利用率提升。

冷却单元
提高可用频率上限，允许更多高频模块满速工作。
```

### 5.2 CPU 性能画像

CPU 输出多维指标，而不是单一等级：

```text
control_score
script_score
route_score
io_score
cache_score
sync_score
compile_score
thermal_headroom
frequency_tier
```

### 5.3 CPU 特化方向

```text
自动化控制 CPU
ALU 多，少量缓存，低级 I/O。适合触发器、执行器和简单闭环控制。

路由服务器 CPU
南桥 I/O 多，高速同步接口，中等缓存。适合模型外网、服务发现、消息队列和传感器集群。

脚本处理 CPU
ALU 多，缓存多。适合数据预处理、脚本器、多模态融合。

模型编译 CPU
优化核心多，缓存多，高速同步接口。适合图编译、算子融合、shape 推导和批处理规划。

训练协调 CPU
南桥 I/O、高速同步接口和优化核心均衡。适合喂 GPU、参数同步和训练任务队列。

低延迟推理 CPU
ALU、高速同步接口和缓存均衡。适合远程推理请求调度和模型热调用。
```

## 6. GPU / NPU / 光计算硬件设计

GPU/NPU 的设计依据不是任务类型，而是模型算子背后的元函数种类。模型编译器扫描模型图后，给出元函数需求；GPU/NPU 蓝图根据这些需求配置硬件加速单元。

**中游硬件分两段**：
- **第 5 阶段（电气段）**：电气 CPU 实装，电气 GPU 作为"密集矩阵临时方案"，电NPU 占位件只承担稀疏/激活算子的临时预算。本章 6.1–6.3 节描述电气段的元函数与算子需求。
- **第 6 阶段（全光计算段）**：光控制核 + 光协处理器 + 光GPU + 光脉冲处理器 + 光RAM 五件套上线；电气 CPU 退为外层兼容接口，电气 GPU/NPU 被全光组件取代。本章 6.4–6.7 节只摘录与硬件性能画像、诊断指标、主板接口相关的内容，完整规范以 `docs/Kamaen_Info_Optical_Computing_Design.md` 为准。

完整的光计算阶段规范参见 `docs/Kamaen_Info_Optical_Computing_Design.md`，本章只摘录与硬件性能画像、诊断指标、主板接口相关的内容。

核心关系：

```text
算子 = 由元函数组成
GPU/NPU = 对部分元函数提供硬件加速
模型性能 = 算子图与硬件元函数单元的匹配程度
```

### 6.1 元函数与加速单元

```text
乘加阵列
服务 MatMul、Linear、部分 Conv 和张量运算。

归约阵列
服务 sum、mean、variance、softmax、normalize。

局部采样阵列
服务 Conv、Pool、空间 grid、局部窗口读取。

查表/Embedding 阵列
服务物品标签、方块 ID、实体关系、稀疏参数读取。

逐元素函数阵列
服务 ReLU、GELU、Sigmoid、Clamp、Scale、Bias。

Softmax/Normalize 阵列
服务 Attention、LayerNorm、BatchNorm 和归一化算子。

稀疏路由阵列
服务 MoE、Gate、Route、稀疏激活和条件专家调用。

量化张量阵列
服务 int8/int4 推理、反量化、低精度矩阵运算。

KV/激活缓存
服务 Transformer 历史序列、层间激活和推理缓存。

显存控制器
决定参数、激活、batch 和缓存是否能及时喂给算子单元。
```

### 6.2 算子需求示例

```text
Linear / MatMul
核心元函数：乘加、矩阵块乘、累加。
硬件方向：乘加阵列、量化张量阵列、高带宽显存。

Conv
核心元函数：局部窗口采样、乘加、滑动聚合。
硬件方向：局部采样阵列、乘加阵列、激活缓存。

Attention
核心元函数：QK 矩阵乘、softmax、加权求和、KV 缓存。
硬件方向：乘加阵列、Softmax/Normalize 阵列、KV 缓存、高带宽显存。

Embedding
核心元函数：索引查表、稀疏读取、向量聚合。
硬件方向：查表/Embedding 阵列、稀疏路由阵列、大容量显存。

Normalize
核心元函数：均值、方差、缩放、偏移。
硬件方向：归约阵列、逐元素函数阵列、融合单元。

Quantization
核心元函数：缩放、截断、反量化、整数乘加。
硬件方向：量化张量阵列、量化参数缓存。
```

### 6.3 GPU/NPU 诊断指标

```text
operator_match
matrix_ops
reduction_ops
lookup_ops
elementwise_ops
sparse_ops
quant_ops
vram_pages
activation_cache
memory_bandwidth
sync_bandwidth
gpu_utilization
```

诊断示例：

```text
算子匹配度：68%
瓶颈：Attention 单元不足，Normalize 阵列不足。
显存占用：82%
带宽利用：96%
核心利用率：41%
建议：增加归约阵列、KV 缓存或显存控制器。
```

### 6.4 光GPU 设计（第 6 阶段，photonic_gpu_unit）

光GPU 把矩阵乘法（GEMM）、卷积、FFT 转化为光的酉变换在 MZI（马赫-曾德尔）干涉网络中传播完成。**密集线性代数甜点**：单次推理峰值算力极高，但权重写入即烧入相位掩模（切换权重需"光路再校准"）。

**架构组件**：

```text
单频激光源（输入泵浦）
调制器阵列（输入向量 x 编码为光场幅度/相位）
MZI 干涉网络（N×N 网格，Reck 三角或 Clements 矩形拓扑；任意酉矩阵可分解为此结构）
相位调谐器（每个 MZI 内一个；权重 = 相位偏置）
光探测器阵列（输出端，光→电）
F4 光频晶振（光路相干基准）
```

**性能画像**：

```text
photonic_throughput          每秒推理次数
mzi_grid_size                MZI 网格规模（4×4 / 8×8 / 16×16 ...）
weight_switch_cost           权重切换代价（重新校准时长 × 校准令牌消耗）
input_modulation_bandwidth   输入调制器带宽
detector_noise_floor         探测器噪声基底（信噪比下限）
coherence_dependency         相干度对推理精度的敏感度
```

**适用 / 不适用**：

| 维度 | 光GPU |
|------|-------|
| 适合 | 密集 GEMM / FFT / Conv（前向）/ 大批量推理 / 固定权重 |
| 不适合 | 分支密集、稀疏权重、快速权重切换、动态算子、小批量 |

### 6.5 光脉冲处理器设计（第 6 阶段，photonic_pulse_processor）

光脉冲处理器是第 5 阶段电NPU 占位的全光替代。它承担光GPU 不擅长的部分：稀疏激活、非线性激活函数近似、低精度时分复用信号处理和脉冲整形。

**核心组件**：

```text
卡玛恩饱和吸收体腔
S 型非线性传输腔
时分复用波导
相位调谐器
单频激光源
F3 时分多路晶振
```

**性能画像**（继承自第 6.3 节，针对光脉冲处理器强调）：

```text
sparse_ops              稀疏算子算力
nonlinear_ops           激活函数近似算力
pulse_ops               脉冲整形与时分多路能力
quant_ops               低精度时分信号处理能力
pulse_threshold_drift   饱和吸收阈值漂移
operator_match          与稀疏/非线性算子的匹配度
```

**与光GPU 的分工**：

| 维度 | 光GPU | 光脉冲处理器 |
|------|-------|-------|
| 数据形态 | 密集张量 | 稀疏 / 脉冲序列 |
| 算子类型 | GEMM / FFT / 卷积 | 稀疏激活 / 非线性函数 / 低精度时分处理 |
| 权重切换 | 慢（重新校准） | 快（调整泵浦功率和腔体调谐） |
| 适合场景 | 模型主干 | 模型尾部 / 后处理 |
| 实际部署 | 共存：光GPU 啃大矩阵，光脉冲处理器处理稀疏和非线性尾部 | 同左 |

### 6.6 光协处理器设计（第 6 阶段新增模块，photonic_coprocessor）

光控制核调度下的可插拔互连模块。不取代控制权，而是承担**光适用的工作**：高带宽数据搬运、批量数据预处理、缓存间互连、零拷贝光总线。

**架构组件**：

```text
简化光调度逻辑（接收光控制核派发的任务描述符）
光数据通路（N 通道并行波导）
全光路由交换机（决定数据从哪个端口进/出，是否经过光GPU 或光脉冲处理器）
F4 光频晶振
```

**性能画像**：

```text
data_move_ops           批量数据搬运吞吐
prep_ops                量化 / 归一化 / 转置等预处理算力
optical_bandwidth       光数据通路总带宽（通道数 × F4 波长峰值）
route_latency           光路由固定延迟（不适合极小批量）
coherent_energy_draw    相干能消耗速率（低，短距/少波长）
```

**信息系统职能映射**（与 `docs/Kamaen_Info_Information_System_Design.md` 第 10 章对齐）：

| 操作类型 | 承担方 |
|---------|--------|
| `control_ops` / `dispatch_ops`（任务派发） | 光控制核 |
| `data_move_ops`（批量数据搬运） | 光协处理器 |
| `prep_ops`（量化/归一化/转置） | 光协处理器 + 光脉冲处理器 |
| `matmul_ops` / `conv_ops` / `fft_ops` | 光GPU |
| `sparse_ops` / `quant_ops` / `nonlinear_ops` / `pulse_ops` | 光脉冲处理器 |

### 6.7 相干能与诊断扩展

第 6 阶段后诊断台输出新增维度（用于光计算硬件的运行健康）：

```text
coherence_avg            当前光路平均相干度（0–1）
coherence_min            最差光路相干度
wavelength_load          同时锁相波长数 / 最大支持数
photonic_throughput      光GPU 每秒推理次数
coherent_energy_draw     相干能消耗速率
calibration_age          距上次校准的 tick 数（用于自动校准预警）
```

相干能消耗模型与失稳后果详见 `docs/Kamaen_Info_Optical_Computing_Design.md` 第 7 章。

## 7. 主板与硬件通信平面

所有外部通信都应经过 I/O 芯片、主板、网络芯片和交换设备逐级扩展。CPU/GPU 核心不直接连接远程设备。

基础层级：

```text
CPU/GPU 核心
-> 片上互连
-> 南桥/I/O 芯片
-> 主板通信平面
-> 内存/储存/网络芯片
-> 交换机/光纤/无线设备
-> 集群/公网/远程节点
```

主板可插组件：

```text
内存页槽
储存芯片槽
参数库接口
光纤芯片
无线芯片
交换芯片
频率晶振
高速同步接口
多卡锁相器
```

### 7.1 主板蓝图玩法

主板不应只是“放进 CPU 和内存的盒子”，而应是玩家设计计算网络自由度的核心载体。主板由蓝图决定插槽、接口方向、总线宽度、供能、散热、频率域和扩展能力。

主板蓝图建议包含：

```text
board_size
插槽布局：CPU/GPU/NPU/内存/储存/参数库/协处理器
总线层数：control_bus/data_bus/matrix_bus/optical_bus
外部接口：fiber_ports/wireless_slots/copper_io/frequency_bus_ports
端口方向：north/south/east/west/up/down
芯片组：southbridge/io_controller/network_controller/clock_controller
同步域：sync_domain_id/frequency_tier/clock_tree_quality
供能与散热：power_budget/thermal_budget
制造质量：trace_density/layer_alignment/package_loss
```

玩家编辑蓝图时，主要选择这些方向：

```text
I/O 主板：外部端口多，route_ops 和 sensor_ops 高，矩阵吞吐低。
训练主板：GPU/NPU 槽、多卡锁相器和光纤口多，吃同步与散热。
存储主板：内存页、储存芯片和参数库接口多，适合模型仓库和数据库。
边缘主板：无线槽、低功耗 CPU、少量缓存，适合远程传感器和执行器。
控制主板：F1/F2 端口多，红石/频率总线适配好，适合工厂闭环。
混合服务器主板：各项均衡，但制造成本、体积和供能要求高。
```

蓝图编辑不需要做像素级电路。第一版可以使用格点槽位：玩家在 5x5、7x7 或 9x9 蓝图板上放置插槽、总线段、接口和芯片组，保存后得到主板蓝图物品。制造时根据蓝图消耗互连线、晶片、晶振、光纤芯片和封装材料，结算出主板性能画像。

### 7.2 主板评分与约束

主板评分不应只奖励“堆满所有槽”，而应让布局选择产生清晰取舍。

```text
slot_capacity：可安装模块数量。
io_lane_count：外部端口与南桥通道数量。
bus_bandwidth：主板内部数据总线带宽。
sync_quality：多卡和高速模块同步效率。
clock_tree_quality：频率域稳定和跨频桥效率。
power_delivery：满载供能能力。
thermal_clearance：高频模块持续运行能力。
port_exposure：接口方向是否可接线。
trace_penalty：线路过长、交叉过多或跨频域导致的损耗。
```

确定性后果：

```text
端口数量不足：设备可安装但无法接入外部网络。
端口方向不对：需要转接背板、扩展坞或重新摆放机器。
总线窄：CPU/GPU 单体性能高但喂不满。
同步差：多 GPU/NPU 效率下降。
供能差：高频晶振不能满速工作。
散热差：持续任务自动降频。
频域混乱：需要频率桥，占用槽位并降低带宽。
```

### 7.3 芯片选择与接口数量

芯片组负责把硬件模块接入不同网络。玩家应能选择“芯片方向”，而不是只升级等级。

```text
基础南桥芯片：增加 copper_io、frequency_bus_ports、低速储存访问。
数据南桥芯片：增加 F2/F3 data_lanes、内存页和参数库吞吐。
光纤控制芯片：增加 fiber_ports、optical_lane_count、F4 兼容。
无线控制芯片：增加 wireless_slots、remote_session_count、公网吞吐。
传感器汇聚芯片：增加 sensor_channel_count、timestamp_alignment、采样缓存。
交换芯片：增加 packet_switch_capacity、vlan_or_namespace_count、组播效率。
安全/权限芯片：增加 access_rule_count、认证开销降低、远程控制安全性。
```

接口数量应是主板最直观的构筑自由度之一：

```text
1-2 光纤口：单机外接或小型存储。
4-8 光纤口：推理节点、训练节点、交换机上联。
12+ 光纤口：专用交换设备或大型集群核心。
1 无线槽：边缘节点或远程控制。
2-4 无线槽：基站、网关或跨基地路由器。
多频率总线口：工厂自动化、传感器网和红石转换密集场景。
```

硬件平面可加入简化的高速信号布局规则：

```text
同步节点之间的烧录线路长度需要接近。
长度差在容许范围内：满速同步。
长度差过大：需要高速信号同步接口。
缺少同步接口：多卡或多模块并行效率下降。
```

不需要模拟电磁场，只计算线路长度、频率域、同步组和带宽等级。

### 7.4 扩展背板与机箱结构

主板蓝图解决单机自由度，背板和机箱解决多板自由度。

```text
扩展背板
连接多块主板，提供共享供能、散热、同步时钟和统一外部端口。

光纤背板
把多张计算卡接入同一 F4 光频平面，适合训练集群。

传感器背板
提供大量低速输入端口、时间戳对齐和采样缓存。

边缘机箱
支持无线、低功耗和少量本地推理，适合远程基地。

服务器机柜
以多方块形式容纳多个主板节点、交换机、储存阵列和冷却模块。
```

背板不直接增加算力，而是减少跨机器连接成本，提高端口密度和维护可读性。

### 7.5 主板类型

主板类型应随机柜、用途和网络位置分化。类型不是硬锁死，而是由蓝图槽位、端口和封装约束自然形成。

```text
通用主板
能跑基础任务，适合工作台式单机和早期自动化，但不能进入高密度服务器机柜。

CPU 主板
ALU、缓存、I/O 和路由单元多，适合脚本、调度、DNS、传感器协调和通信维持。

GPU/NPU 主板
乘加阵列、显存控制器和高速同步接口多，适合推理、训练和模型层执行。

存储主板
内存页、一级储存、索引页和存储端口多，适合数据集、模型快照和参数页。

交换机主板
物理端口多，交换芯片、路由 CPU 和包缓存多，适合集群与机柜族互连。

无线基站主板
无线芯片和天线接口多，支持远程访问、边缘节点和公网服务，但需要处理衰减。

边缘主板
低功耗、少量无线、少量本地推理，适合远程传感器、执行器和小基地。
```

主板诊断必须把算力分成两类：

```text
维持算力
CPU 消耗，用于调度、通信、路由、脚本、传感器和服务发现。

任务算力
CPU/GPU/NPU 共同消耗，用于数据处理、模型编译、推理和训练。
```

这能避免玩家误以为 GPU 很强就能解决所有网络与传感器问题。

### 7.6 机柜、机柜族与集群封装

机柜把多块主板封装为稳定节点。它不只是外壳，而是供电、冷却、连线、端口暴露和维护风险的结算单位。

机柜字段：

```text
rack_size
installed_boards
power_budget
cooling_budget
liquid_cooling_rate
cryogenic_boost
cable_quality
pipe_layout
front_panel_ports
wireless_exposure
maintenance_access
power_loss_risk
thermal_throttle_risk
```

机柜输出：

```text
available_control_ops
available_route_ops
available_matrix_ops
available_storage_pages
available_memory_pages
external_bandwidth
cooling_headroom
uptime_score
```

机柜族是同用途机柜的集合，例如：

```text
CPU 调度柜族
GPU 推理柜族
训练柜族
存储柜族
交换柜族
无线基站柜族
传感器接入柜族
```

集群封装把多个机柜族注册为统一服务，输出可调度的资源池：

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

第一版可以只做“单机柜节点”，中期再扩展机柜族，后期再做跨基地集群。

## 8. 内存与储存

内存不作为复杂架构玩法，而作为模型装载资源和地址空间实体化。

定义：

```text
内存 = 地址空间 + 参数页 + 激活页 + 状态页 + 索引页
```

内存页类型：

```text
参数页
存放模型权重、偏置、量化参数。

激活页
存放推理或训练中间结果。

状态页
存放历史、RNN hidden、PID 状态、任务队列状态。

索引页
存放参数地址、shape、dtype、版本和命名空间信息。

交换页
当显存或高速缓存不足时，用于低速溢出。
```

储存负责长期保存：

```text
模型文件
参数快照
训练数据集
日志
蓝图
版本记录
```

### 8.1 存储中心

存储中心是数据和模型的长期基础设施，主要服务两类内容：

```text
传感器数据集
模型参数、模型快照和编译缓存
```

存储中心核心指标：

```text
capacity_pages
read_bandwidth
write_bandwidth
index_speed
backup_level
power_stability
thermal_stability
data_loss_risk
compression_ratio
```

本地存储脚本只做轻量处理：

```text
过滤
压缩
抽样
重命名
索引
按标签分片
生成训练集清单
```

重型数据处理需要提交到算力中心：

```text
大规模清洗
特征提取
训练集重平衡
模型编译
参数量化
批量评估
```

掉电和热平衡只做确定性风险：

```text
供电不足：写入速度下降，长任务暂停。
短时掉电：未提交缓存页丢失。
长期过热：写入降速，数据损坏风险升高。
备份不足：故障后只能恢复旧快照。
```

部署流程：

```text
储存中的模型快照
-> 加载到内存参数页
-> CPU/GPU/NPU 运行
-> 状态页更新
-> 需要时写回储存
```

内存不足的确定性后果：

```text
参数页不足：模型无法完整加载，或只能加载裁剪版。
激活页不足：batch 下降，激活重算增加。
状态页不足：历史窗口变短，长期任务效果下降。
索引页不足：模型版本和地址查询能力下降。
```

## 9. 通信系统分层

通信分为四层。

### 9.1 模型内通信

模型内数据流转采用统一数据线，不区分多种实体线缆。语义由接口、端口声明和数据包类型决定。

```text
ModelDataLine
IModelDataPort
IModelPacket
```

统一模型数据线可承载：

```text
Input
ParameterRef
Activation
State
Feedback
Metric
```

模型内通信依赖：

```text
local:id
触发器
模型数据线
模型内交换节点
子图入口/出口
```

优化目标：

```text
减少路由跳数
固定 local:id，避免动态查找
合并小数据包
将高频子图放入同一频率域
为重复路径增加缓存
```

### 9.2 硬件内通信

硬件内通信由主板平面、南桥 I/O、显存控制器、参数库接口和高速同步接口承担。

主要传输：

```text
Task
TensorChunk
ParameterPage
ActivationPage
StatePage
ModelLoadRequest
```

主要瓶颈：

```text
南桥 I/O 不足
主板通信平面带宽不足
显存控制器不足
参数加载链路不足
同步线路长度差过大
频率域不兼容
```

### 9.3 短距离光纤集群

光纤定位为高带宽近中距离连接，不替代无线。

用途：

```text
多 GPU/NPU 并行
训练集群
参数同步
模型服务集群
短距离存储中心
推理中心
```

设备：

```text
光纤芯片
光频互连卡
光纤交换机
相干光背板
参数同步链路
训练同步器
推理调度交换机
```

光纤接口玩法：

```text
单模光纤：距离远、端口成本高、适合基地间干线。
多模光纤：短距离高吞吐、适合机柜和训练集群。
相干光纤：需要 F4 锁相，支持参数同步和多卡训练。
光纤分线器：一分多，降低每路带宽，适合低频传感器汇聚。
光纤交换机：按地址转发，吃交换芯片和路由 CPU。
光交叉连接器：手动指定端口映射，低 CPU 成本但不灵活。
```

光纤交换机的可玩点：

```text
port_count：物理端口数量。
switch_bandwidth：总交换背板带宽。
per_port_bandwidth：单口上限。
route_table_size：可维护的节点数量。
packet_buffer：突发流量缓存。
multicast_efficiency：参数同步、广播采样和模型下发效率。
clock_passthrough：是否能传递同步域。
```

交换机可以通过插入交换芯片、光频晶振、缓存页和路由 CPU 进行定向升级。大型网络不要求玩家每根线手动配置，但诊断台必须能显示“哪台交换机、哪个端口、哪段链路”成为瓶颈。

### 9.4 长距离无线网络

无线用于远程节点、边缘计算、公网数据包接收和跨基地通信。

无线设备需要公网地址或注册服务：

```text
public_id
remote:id
模型服务名
权限规则
频段等级
```

设备：

```text
无线芯片
无线天线
公网接收器
无线基站
公网网关
边缘计算机
数据包路由器
```

传输对象：

```text
InfoPacket
DatasetShard
ModelSnapshot
ParameterDelta
MetricReport
InferenceRequest
InferenceResult
ControlCommand
```

无线不与光纤竞争同一定位：

```text
无线优势：跨区块、跨基地、快速部署、远程传感器、移动执行器。
无线限制：带宽较低、延迟较高、需要公网地址、需要权限规则。
光纤优势：高吞吐、低延迟、同步好、适合训练和存储。
光纤限制：需要实体布线、端口规划和交换设备。
```

无线技术等级可用 1G-6G 做游戏内升级语言，但不模拟现实移动通信协议。

```text
1G
低速远程控制命令，适合开关量、报警和低频状态。

2G
少量传感器数据和低速文本/标签包。

3G
远程状态同步、基础边缘节点和小型数据块。

4G
普通传感器数据、轻量模型请求和远程机器管理。

5G
低延迟推理请求、边缘计算和高并发传感器。

6G
高密度传感器网、跨基地高速无线和高级公网服务。
```

无线密度规则：

```text
普通主板可插无线芯片，但高密度无线会产生 attenuation_penalty。
无线基站主板拥有更好的天线暴露和隔离，衰减更低。
机柜内无线芯片太密集时，覆盖范围下降、延迟上升、功耗增加。
交换机或基站机柜更适合承载大量无线会话。
```

### 9.5 数据接口与端口声明

所有设备应把可连接能力声明为端口，而不是让玩家猜某个面能不能连。

端口基础字段：

```text
port_id
side
direction: input/output/bidirectional
protocol: frequency_bus/model_data/fiber/wireless/storage/control/redstone
frequency_tier
bandwidth
packet_types
permission_scope
```

典型端口：

```text
控制端口：ControlCommand、Trigger、RedstoneMapping。
传感端口：InfoSignal、SensorFrame、MetricReport。
模型数据端口：Input、Activation、State、ParameterRef。
存储端口：ModelSnapshot、DatasetShard、StoragePage。
光纤端口：高速 Packet、ParameterDelta、TensorChunk。
无线端口：RemoteRequest、InferenceResult、ControlCommand。
```

玩家放置设备时，端口方向决定布线和机柜排布。高级主板、背板和交换机可以提供端口重映射，但会消耗芯片槽或路由预算。

### 9.6 简化运行环境与协议

主板不模拟完整操作系统，但每块主板或机柜节点可以拥有一个简化运行环境配置。

```text
runtime_profile
task_roles
input_ports
output_ports
packet_formats
protocol_rules
script_hooks
scheduler_priority
resource_limits
```

数据包格式保持有限枚举，玩家可以给字段命名或添加标签，但底层仍归入固定类型。

```text
ControlPacket
控制命令、开关量、执行器动作。

SensorFrame
传感器帧，包含时间戳、来源、置信度和数据 payload。

DataChunk
普通数据块、文件片、日志片和数据集分片。

ModelInput
模型输入，通常来自传感器融合或脚本处理。

ModelOutput
模型输出，发往执行器、日志、反馈或下游模型。

ParameterPage
参数页、权重页、索引页和量化参数。

ActivationChunk
模型运行中间激活，主要在模型内网或 GPU/NPU 节点之间流动。

MetricReport
loss、reward、吞吐、延迟、能耗、错误率和诊断指标。
```

协议设置只影响抽象成本：

```text
serialization_cost
route_ops
bandwidth_efficiency
latency_ticks
permission_cost
packet_loss_risk
compatibility
```

脚本语言只用于轻量数据处理、端口映射、过滤和任务提交。长时间运行或高频脚本必须编译为数据处理图并受 CPU 预算限制。

### 9.7 传感器独立网络

传感器可以直接挂在模型外网，也可以组成独立传感器网络。建议两者都支持，但定位不同。

```text
直接接入
适合少量低频传感器，结构简单，延迟低。

独立传感器网络
适合大量传感器、远程采样、时间戳对齐、采样缓存、批量上传和数据质量控制。
```

传感器网络由这些节点组成：

```text
sensor_node：单个传感器或传感器组。
sensor_hub：汇聚本地传感器，提供时间戳与缓存。
sensor_backplane：大量低速端口，常用于机器框架或信息中心。
edge_sampler：远程采样与本地预处理。
fusion_processor：多源数据融合，输出 vector/grid/sequence/event。
dataset_uploader：把采样批次上传到数据库或训练节点。
```

传感器网络的收益不是“必须多一层”，而是当传感器数量上来后提供：

```text
采样周期统一
时间戳对齐
缺失值标记
批量压缩
局部过滤
异常事件触发
训练数据自动归档
```

### 9.8 模型组件方块网络

模型组件方块用于把参数、算子、状态、触发器和网关实体化。它们不应每 tick 扫描全世界，而是在保存、编译或结构变化时生成可执行图。

基础组件：

```text
input_gateway：接收传感器、外网或玩家输入。
operator_block：声明算子或脚本片段。
parameter_block：引用参数页或参数库地址。
state_register：保存跨 tick 状态。
activation_bus：传递临时激活。
trigger_block：提交内部或外部任务。
output_gateway：输出到执行器、网络或数据物品。
feedback_node：把评价、loss、reward 或 metric 回流。
model_compiler：扫描组件网络并生成 ExecutableGraph。
```

模型组件方块网络的自由度：

```text
拓扑自由：串联、并联、残差、反馈、分支、门控。
命名自由：local/export/remote 地址由网关和命名空间决定。
部署自由：小模型可在单主板运行，大模型可拆到多个节点。
优化自由：玩家通过合批、缓存、量化和静态 shape 提升硬件利用率。
接口自由：同一模型可同时接传感器网、工厂控制网和无线外网。
```

第一版实现边界：

```text
结构变化时扫描组件网络。
编译为静态图和端口表。
运行时只按任务预算推进。
不执行任意高频文本脚本。
不保存无限激活历史。
```

## 10. 地址索引与网络中心

后期玩家可以搭建网络中心，把多个计算节点、训练节点、推理节点、存储节点和边缘节点组织成完整信息网络。

核心设备：

```text
地址索引器
维护 local/export/remote 地址映射。

嵌套 DNS
维护层级化服务名，例如：
base.train.gpu0
base.infer.mob_detector
edge.farm.sensor_grid
dim.nether.remote_probe

模型服务注册表
记录哪些模型在哪些节点可调用。

参数版本目录
记录模型版本、参数页位置、快照状态。

任务调度器
决定推理请求、训练 batch、数据同步发往哪里。

缓存索引器
记录哪些节点已经拥有某个模型、参数页或数据集分片。
```

网络中心优化目标：

```text
地址解析速度
路由跳数
服务发现延迟
模型热加载命中率
参数版本一致性
任务拆分效率
公网请求吞吐
```

## 11. 模型任务类型

硬件性能最终应作用到具体任务。建议第一版定义这些任务类型：

```text
realtime_inference
低延迟推理，吃 CPU 调度、缓存、高速同步和模型热加载。

batch_inference
合批推理，吃 GPU/NPU 算子匹配、显存、batch 缓冲和调度器。

offline_training
离线训练，吃 GPU/NPU、显存、参数同步、样本流和检查点写入。

model_loading
模型加载，吃参数页、储存、主板 I/O 和参数加载链路。

dataset_transfer
数据集转移，吃储存、光纤/无线、路由和压缩格式。

parameter_sync
参数同步，吃光纤互连、多卡锁相器、同步接口和版本目录。

sensor_fusion
传感器融合，吃 CPU 脚本、缓存、内网地址和数据线。

graph_compile
模型图编译，吃 CPU 优化核心、缓存、shape 推导和算子融合。
```

## 12. 硬件制造闭环

硬件合成与制造可以设计得复杂，形成后续模型自动化工艺调参的需求。

建议制造流程按四段理解：

```text
芯片蓝图
-> 晶圆/光刻/刻蚀/退火
-> 芯片封装
-> 主板封装
-> 机柜/集群封装
```

芯片制造流程：

```text
晶圆生长
-> 切片
-> 抛光
-> 掺杂
-> 光刻
-> 蚀刻
-> 退火
-> 金属互连
-> 裸片测试
```

封装流程：

```text
选择封装类型
-> 端口/引脚映射
-> 散热界面处理
-> 频率上限测试
-> I/O 测试
-> 分级
```

主板封装流程：

```text
主板蓝图
-> 安装芯片封装
-> 安装晶振/电源/内存/一级储存
-> 连接端口和总线
-> 烧录运行环境配置
-> 诊断台生成硬件画像
```

机柜封装流程：

```text
安装主板
-> 接入供电
-> 接入光纤/无线/控制线
-> 接入冷却管道或液氮模块
-> 理线评分
-> 节点注册到网络中心
```

工艺参数：

```text
温度
压力
相干能输入
频率
掺杂方向
曝光图案
蚀刻深度
退火时间
洁净度
```

检测状态：

```text
晶圆纯度
掺杂均匀度
光刻对准度
蚀刻完整度
退火应力
互连密度
封装损耗
频率响应
```

芯片良率与模型调参：

```text
芯片蓝图复杂度越高，基础良率越低。
晶圆质量、掺杂均匀度、光刻对准、蚀刻深度和退火应力共同影响分档。
传感器采样工艺状态，模型输出下一步工艺参数。
系统仍用固定公式结算，不运行真实工艺仿真。
```

模型参与方式：

```text
芯片制造状态
-> 传感器采样
-> 模型推理
-> 输出下一步工艺参数
-> 固定公式结算质量与分档
```

硬件分档建议：

```text
残次芯片
低频芯片
标准芯片
高频芯片
高并行芯片
低功耗芯片
锁相特化芯片
```

这形成自举闭环：

```text
复杂硬件制造
-> 人工难以稳定量产
-> 建立传感器、数据集和控制模型
-> 模型优化工艺参数
-> 产出更好硬件
-> 支撑更大的模型
```

## 13. 诊断与平衡

诊断台是硬件系统的核心设备。玩家设计硬件、部署模型或组建集群后，系统应给出可读瓶颈。

统一性能画像：

```text
control_ops
script_ops
route_ops
io_bandwidth
sync_bandwidth
matrix_ops
operator_match
memory_pages
storage_pages
frequency_tier
model_load_time
gpu_utilization
batch_throughput
sync_overhead
parameter_bandwidth
activation_bandwidth
```

诊断示例：

```text
GPU 利用率低：南桥 I/O 不足。
多卡效率低：同步接口不足或线路长度差过大。
模型加载慢：参数页带宽不足。
推理延迟高：路由层级过深或模型热加载缺失。
训练吞吐低：样本流、参数同步或检查点写入瓶颈。
公网调用慢：无线网关、地址索引或服务发现瓶颈。
算子匹配度低：GPU/NPU 元函数单元与模型图不匹配。
```

## 14. 科技阶段建议

本节阶段对应模组主线第 4–8 阶段（共 5 个主线阶段，覆盖电气硬件与光计算两段中游）。完整 11 阶段主线见 `docs/Kamaen_Info_TechTree_Plan.md`。

```text
硬件阶段一：逻辑模块与控制芯片（主线第 4 阶段）
ALU、寄存器、基础 I/O、F1 晶振、低位宽芯片蓝图、简单封装。

硬件阶段二：基础主板与单机任务（主线第 4–5 阶段）
F2 晶振、通用主板蓝图、内存页、一级储存、传感器数据处理任务。

硬件阶段三：机柜与稳定运行（主线第 5 阶段）
服务器主板、供电、冷却、机柜理线、掉电风险、硬件诊断。

硬件阶段四：电气矩阵加速与模型部署（主线第 5 阶段）
F3 晶振、电气 GPU/NPU 元函数单元（密集矩阵临时方案 + 占位 NPU）、显存页、参数加载链路、模型编译器。

硬件阶段五：光计算硬件（主线第 6 阶段，新增）
F4 光频晶振、单频激光源、硅光波导、MZI 调制器、相位调谐器、硅光探测器、光控制核、光协处理器、光GPU（MZI 网络）、光脉冲处理器、光RAM、相干能、光路校准。详见 `docs/Kamaen_Info_Optical_Computing_Design.md`。

硬件阶段六：光纤集群与存储中心（主线第 6–7 阶段后期）
光纤交换机、训练同步器、存储中心、数据集传输；多光GPU 集群互连。

硬件阶段七：无线公网与服务发现（主线第 7 阶段）
无线芯片、1G-6G 基站、公网网关、root/zone DNS、模型服务注册表。

硬件阶段八：单光子源 / SNSPD / 量子光学协处理（主线第 7–8 阶段）
凝聚态产物升级光GPU 探测器；量子光学协处理器（玻色采样路线）作为光计算的量子延伸。

硬件阶段九：光RAM / WDM / 全光网络（主线第 10 阶段）
F4 协议升级密集波分复用；稀土掺杂晶体或量子点光RAM；控制平面也走光，电气退场。

硬件阶段十：维度级网络（主线第 11 阶段）
F5 维度同步晶振、跨维度通信、世界之心数据、创世编译网络。
```

## 15. 后续落地拆分

实现时可按以下顺序推进：

1. 定义硬件性能画像数据结构。
2. 定义频率等级与兼容规则。
3. 实现芯片蓝图：ALU、寄存器、I/O、位宽、端口和基础评分。
4. 实现芯片封装：封装类型、端口映射、散热、频率上限。
5. 实现主板蓝图：格点布局、芯片槽、晶振、内存、一级储存和端口方向。
6. 实现主板运行环境：固定数据包类型、轻量脚本、任务角色和资源上限。
7. 实现硬件诊断台：CPU/内存/端口/散热/供电瓶颈报告。
8. 实现传感器数据处理 MVP：传感器帧 -> 脚本处理 -> 存储页或模型输入。
9. 实现机柜封装：供电、冷却、理线、主板安装和掉电风险。
10. 实现 GPU/NPU 元函数单元与模型算子需求报告。
11. 实现光纤交换机、存储中心和短距离集群。
12. 实现无线芯片、1G-6G 基站、公网地址和 remote 服务。
13. 实现地址索引器、root/zone DNS 和模型服务注册表。
14. 实现硬件制造工艺状态和模型调参闭环。

MVP 第一条链：

```text
ALU/控制芯片设计
-> 简单 CPU 芯片封装
-> 通用主板蓝图
-> 单机运行传感器数据处理任务
-> 诊断 CPU、内存、端口、散热和供电瓶颈
```

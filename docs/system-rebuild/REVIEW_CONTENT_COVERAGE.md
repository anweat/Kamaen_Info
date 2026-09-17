# R1旧内容覆盖与去向

逐项读取旧字典§3–13的164个实体条目，另核对阶段表独有的20个ID。不是注册代码清单；名称/旧用途保留用于追溯，配方以R1重构规则修订。不同档次设备归到同一能力不代表同一配方或同一时点。

当前计算研究阶段的具体取得、物料与装配以[R4逐项去向](R4_SOURCE_RECONCILIATION.md)为准，本表保留全局能力位置。

| 旧ID | 原名 | R1能力/位置 | 原用途 | 处置/修订 | 原字典行 |
| --- | --- | --- | --- | --- | --- |
| `crude_spectrum_scrap` | 粗频谱碎屑 | P01 / `manual` | 手动起步中间产物 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 50 |
| `crude_spectrum_slurry` | 粗频谱泥浆 | P01 / `manual` | 分馏输入，承接污染 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 51 |
| `spectrum_slag` | 频谱滤渣 | P01 / `manual` | 白噪链核心副产物 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 52 |
| `whitened_cobblestone` | 均值化圆石 | P02 / `mean` | 白噪晶种基底 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 53 |
| `white_noise_seed` | 白噪晶种 | P02 / `seed` | 卡玛恩晶体起点 | 平均背景初始结晶；结构质量与中性分开 | 54 |
| `spectrum_powder` | 频谱粉末 | P01 / `manual` | 合并铁粉/煤粉/铜粉/矿粉 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 55 |
| `spectrum_membrane` | 频谱滤膜 | P01 / `manual` | 控制分馏偏向 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 56 |
| `hand_spectrum_sieve` | 手摇频谱筛 | P01 / `manual` | 空岛/早期手动产物 | 重做首版：木筛不需铁；金属筛再升级 | 57 |
| `fractionating_tower` | 搅拌分馏塔 | P01 / `manual` | 第一台自动机器 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 58 |
| `thermal_noise_crucible` | 热噪坩埚 | P02 / `mean` | 热处理滤渣和均值化圆石 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 59 |
| `basic_spectroscope` | 初级分光镜 | P02 / `mean` | 早期分析工具 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 60 |
| `blast_powder` | 爆震粉 | P03 / `raw` | 模拟爆破能源 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 66 |
| `ideal_rigid_plate` | 理想刚体板 | P03 / `raw` | 爆炸室反射模块 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 67 |
| `buffer_sand_layer` | 缓冲砂层 | P03 / `raw` | 降低爆破强度，提高容错 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 68 |
| `target_pedestal` | 靶座 | P03 / `raw` | 固定晶种/晶体 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 69 |
| `raw_kamaen_crystal` | 粗卡玛恩晶体 | P03 / `raw` | 第一代晶体母体 | 旧设计别名，注册对齐kamaen_crystal_raw；必须加生长基材 | 70 |
| `kamaen_crystal_debris` | 卡玛恩晶体碎片 | P03 / `raw` | 失败回收和低级配方 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 71 |
| `waveguide_kamaen_crystal` | 导波型卡玛恩晶体 | P03 / `stress` | 总线、导线、信号结构材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 72 |
| `compression_kamaen_crystal` | 抗压型卡玛恩晶体 | P03 / `stress` | 高压、结构、视界材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 73 |
| `stable_spectrum_kamaen_crystal` | 稳谱型卡玛恩晶体 | P03 / `stress` | 能量、相干、底噪相关基底 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 74 |
| `polarized_kamaen_crystal` | 偏振卡玛恩晶体 | P03 / `stress` | 高级传感器/偏振模块 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 75 |
| `stress_recording_plate` | 应力记录片 | P03 / `stress` | 保存一次应力快照 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 76 |
| `explosion_chamber_controller` | 爆炸室控制器 | P03 / `raw` | 扫描结构并计算爆破评分 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 77 |
| `stress_sensor` | 应力传感器 | P03 / `stress` | 读取晶体应力 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 78 |
| `axial_press_head` | 轴向压头 | P03 / `stress` | 提供可控压力 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 79 |
| `tier1_mechanical_framework` | I 型力学合成框架 | P03 / `stress` | 力学合成研究站 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 80 |
| `tuning_wafer` | 调谐晶片 | P04 / `resonance` | 频谱锁相和总线基础材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 86 |
| `intrinsic_spectrum_sample` | 固有频谱样本 | P04 / `resonance` | 目标频谱模板 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 87 |
| `information_unit` | 信息单元 | P05 / `feedback` | `InfoSignal` 基础载体 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 88 |
| `resonance_catalyst_crystal` | 共振催化晶体 | P04 / `resonance` | 加速/优化对应机器或材料流程 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 89 |
| `frequency_bus` | 频率总线 | P05 / `feedback` | 传递 InfoSignal | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 90 |
| `frequency_to_redstone_module` | 频率转红石模块 | P05 / `feedback` | 将 InfoSignal 映射到 0-15 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 91 |
| `crystal_interferometer` | 晶体干涉仪 | P08 / `optical` | 晶体属性分析台 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 92 |
| `spectrum_phaselocker` | 频谱锁相器 | P04 / `resonance` | 读取样本并写入晶体 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 93 |
| `kamaen_probe_station` | 卡玛恩探针台 | P05 / `feedback` | 把可读世界状态转 InfoSignal | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 94 |
| `tuning_array` | 调谐阵列 | P04 / `resonance` | 提高锁相和共振效率 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 95 |
| `kamaen_crystal_t2` | 二代卡玛恩晶体 | P06 / `doping` | 允许掺杂、导波、阈值和相位控制的晶体 | 用途检验/工艺资格，不是全属性统一升级 | 101 |
| `kamaen_dopant` | 卡玛恩掺杂剂 | P06 / `doping` | 合并施主/受主掺杂剂 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 102 |
| `kamaen_wafer` | 卡玛恩晶片 | P06 / `doping` | 合并 blank/N/P/defect 晶片 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 103 |
| `kamaen_pn_junction` | 卡玛恩 PN 结 | P08 / `electric` | 二极管/晶体管前置 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 104 |
| `electronic_logic_gate` | 电逻辑门片 | P08 / `electric` | EDA 电逻辑基础元件，用于早期接口、桥接、低速控制和电存储 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 105 |
| `lithography_mask` | 光刻掩膜 | P07 / `precision` | 定义曝光图案 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 106 |
| `lithography_mask_set` | 分层光刻掩膜组 | P09 / `eda` | 保存 active/metal/optical/via/cooling/shield 等多层掩膜 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 107 |
| `process_protection_kit` | 工艺防护套件 | P07 / `precision` | 抽象表示 ESD、防尘、防火/绝缘、封装应力释放等工艺防护 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 108 |
| `timing_structure_cell` | 时序结构单元 | P09 / `eda` | 在 EDA 版图中提供 T0-T5 时序能力 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 109 |
| `crystal_interconnect` | 晶体互连线 | P08 / `bridge` | 封装芯片、板级互连和桥接同步材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 110 |
| `kamaen_oscillator` | 卡玛恩晶振 | P01 / `power` | 统一 F1/F2/F3/F4/F5，同步 EDA 芯片和板级域 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 111 |
| `coherent_energy_buffer` | 相干能缓存 | P01 / `power` | 低噪工艺能源存储 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 112 |
| `coherent_energy_regulator` | 相干能稳压器 | P01 / `power` | FE -> 相干能 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 113 |
| `ion_implanter` | 离子注入器 | P06 / `doping` | 给晶片写掺杂参数 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 114 |
| `lattice_annealing_furnace` | 晶格退火炉 | P07 / `precision` | 降低缺陷、形成 PN 结 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 115 |
| `lithography_projector` | 光刻投影器 | P07 / `precision` | 曝光图案到 PN 结/晶片 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 116 |
| `etching_tank` | 刻蚀槽 | P07 / `precision` | 按图案移除材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 117 |
| `tier2_optical_process_framework` | II 型光路工艺框架 | P07 / `precision` | 掺杂、光刻、导波、阈值、相位和探测结工艺集中控制 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 118 |
| `hardware_diagnostic_station` | 硬件诊断台 | P09 / `board` | 输出 EDA 芯片、封装、主板/背板和环境域性能画像 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 119 |
| `electronic_control_chip` | 电控接口芯片 | P09 / `board` | 早期接口、传感器汇聚、桥接控制和低速路由预算 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 125 |
| `electronic_matrix_tile` | 电矩阵瓦片 | P12 / `e_matrix` | 可选早期/兼容密集矩阵元件，不作为中游主线 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 126 |
| `electronic_activation_tile` | 电激活瓦片 | P12 / `e_matrix` | 可选早期/兼容稀疏、量化、激活算子元件 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 127 |
| `memory_page` | 内存页 | P10 / `store` | 统一参数/状态/索引页，属于电/经典存储域 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 128 |
| `eda_module_plate` | EDA 模块片 | P09 / `eda` | ALU、寄存器、MZI、双稳态腔、I/O、桥接等芯片模块的制造单元 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 129 |
| `chip_blueprint_writer` | 芯片蓝图台 | P09 / `eda` | 编辑 EDA 原理图、微结构版图、分级时序、端口、冷却、相干和桥接要求 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 130 |
| `chip_packaging_station` | 芯片封装台 | P09 / `package` | 将芯片蓝图和 EDA 模块封装成可上主板/光背板/低温载板芯片 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 131 |
| `packaged_logic_chip` | 封装逻辑芯片 | P09 / `package` | 电/光/量子/存储/桥接芯片实体 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 132 |
| `motherboard_blueprint` | 集成板蓝图 | P09 / `board` | 保存电主板、光背板、低温载板或混合集成节点布局 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 133 |
| `configurable_motherboard` | 可配置集成板 | P09 / `board` | 承载电控、光逻辑、存储、桥接或低温芯片并输出硬件画像 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 134 |
| `network_interface_chip` | 网络接口芯片 | P11 / `network` | 给主板提供光纤、无线、传感器或交换端口 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 135 |
| `fiber_switch` | 光纤交换机 | P11 / `network` | 多端口高速光纤转发、参数同步和集群组网 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 136 |
| `sensor_hub` | 传感器汇聚器 | P11 / `sensors` | 汇聚多传感器、时间戳对齐、缓存并批量上传 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 137 |
| `model_component_gateway` | 模型组件网关 | P10 / `runtime` | 模型组件方块网络的输入/输出端口 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 138 |
| `model_compiler` | 模型编译器 | P10 / `runtime` | 扫描模型组件方块网络并生成 ExecutableGraph | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 139 |
| `server_rack` | 服务器机柜 | P12 / `cluster` | 将多块主板封装为稳定算力/存储/交换节点 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 140 |
| `storage_center_controller` | 存储中心控制器 | P10 / `store` | 存储传感器数据集、模型快照和参数页 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 141 |
| `world_noise_sample` | 世界底噪样本 | P11 / `sensors` | 底噪采样载体 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 142 |
| `thermal_noise_plate` | 热噪声谱片 | P15 / `noise` | 热噪层专用材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 143 |
| `radiation_noise_plate` | 背景辐射谱片 | P15 / `noise` | 辐射层材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 144 |
| `quantum_fluctuation_plate` | 量子涨落片 | P15 / `noise` | 量子噪声材料 | 量子解释未成立时只标候选残差，不能直接测得任意真值 | 145 |
| `chunk_entropy_record` | 区块熵流记录 | P15 / `noise` | 记录区块熵流 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 146 |
| `noise_database` | 底噪数据库 | P11 / `network` | 存储样本、标签、版本 | 空白载体先造，数据库为应用；记录x16不作为研究点门槛 | 147 |
| `macro_info_index_core` | 宏观信息索引核心 | P11 / `network` | 信息中心核心组件 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 148 |
| `noise_spectrometer` | 底噪谱仪 | P11 / `sensors` | 采样维度底噪 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 149 |
| `thermodynamic_antenna` | 热力学背景天线 | P11 / `sensors` | 扩大谱仪范围 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 150 |
| `entropy_flow_meter` | 熵流计 | P15 / `noise` | 读取区块熵流 | 区块活动代理指标与热力学熵区分 | 151 |
| `info_center_controller` | 信息中心控制器 | P11 / `network` | 宏观采样、路由、归档 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 152 |
| `silicon_photonic_waveguide_blank` | 硅光波导毛坯 | P08 / `optical` | 第 6 阶段所有光路元件的基础 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 160 |
| `silicon_photonic_waveguide` | 硅光波导 | P08 / `optical` | MZI / 光协处理器底层导光介质 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 161 |
| `mzi_modulator` | 马赫-曾德尔调制器 | P08 / `optical` | 光GPU 权重单元 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 162 |
| `phase_tuner` | 相位调谐器 | P08 / `optical` | 校准 MZI / 写入光GPU 权重 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 163 |
| `silicon_photodetector` | 硅光探测器 | P08 / `bridge` | 光GPU 输出端 / 光协处理器光电边界 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 164 |
| `single_freq_laser_source` | 单频激光源 | P08 / `optical` | 光路相干基准 + 相干能消耗中心 | 精密版保留；粗源/手动校准先于F4规模系统 | 165 |
| `calibration_token` | 光路校准令牌 | P08 / `optical` | 光路校准消耗品 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 166 |
| `kamaen_nonlinear_medium` | 卡玛恩非线性介质 | P12 / `photonic_logic` | 光逻辑门、光脉冲处理器和光RAM 的 χ² 基材 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 167 |
| `photonic_logic_gate` | 光逻辑门 | P12 / `photonic_logic` | 全光 AND/OR/NOT/NAND/XOR 基元 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 168 |
| `kamaen_bistable_cell` | 卡玛恩双稳态晶胞 | P12 / `photonic_logic` | 光控制核状态寄存器和光RAM 反射基元 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 169 |
| `photonic_control_core` | 光控制核 | P12 / `photonic_control` | 全光 FSM，承担第 6 阶段控制/路由/脚本/调度/IO | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 170 |
| `photonic_coprocessor` | 光协处理器 | P12 / `photonic_move` | 光控制核调度下的数据搬运/缓存互连加速 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 171 |
| `photonic_gpu_unit` | 光GPU 单元 | P12 / `o_matrix` | 密集 GEMM / FFT / 卷积加速 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 172 |
| `photonic_pulse_processor` | 光脉冲处理器 | P12 / `photonic_pulse` | 稀疏激活、非线性算子、低精度时分信号处理 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 173 |
| `photonic_ram_unit` | 光RAM 单元 | P12 / `photonic_ram` | 短时状态存储、激活缓存和状态寄存器 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 174 |
| `coherent_energy` | 相干能（资源） | P01 / `power` | 维持光路相干的能量预算（独立资源条，非 FE 子类） | 保留资源表现；能量、参考稳定度、相干条件分开 | 175 |
| `photonic_waveguide_etching_station` | 波导刻蚀台 | P08 / `optical` | 制造硅光波导 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 176 |
| `mzi_weaving_station` | MZI 编织台 | P12 / `o_matrix` | 把波导和调制器组装为 N×N 网格 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 177 |
| `laser_pump_tower` | 激光泵浦塔 | P01 / `power` | 集中产生相干能 + 单频激光源 | 集中规模升级；初版光源不依赖这座塔 | 178 |
| `photonic_calibration_station` | 光路校准台 | P12 / `o_matrix` | 重新写入光GPU 权重 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 179 |
| `quasiparticle_lattice` | 准粒子晶格 | P16 / `phase` | 凝聚态基础材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 185 |
| `propagator_plate` | 传播子片 | P19 / `effective` | 合并声子/电子/激子/自旋波 | 响应/模型数据，不是可装袋物理传播子 | 186 |
| `cooper_pair_seed` | 库珀对种子 | P16 / `phase` | 超导环前置 | 实体态预制件，需基材和环境；不能用两张记录变物质 | 187 |
| `feynman_vertex_plate` | 费曼顶点片 | P19 / `effective` | 描述相互作用顶点 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 188 |
| `feynman_process_blueprint` | 费曼过程蓝图 | P19 / `effective` | 凝聚态配方核心 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 189 |
| `superconducting_kamaen_ring` | 超导卡玛恩环 | P16 / `phase` | 量子/视界/线圈核心材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 190 |
| `topological_insulator_crystal` | 拓扑绝缘晶体 | P16 / `phase` | 拓扑材料和边界态 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 191 |
| `phase_change_memory_crystal` | 相变记忆晶体 | P16 / `phase` | 高级存储/状态材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 192 |
| `quasiparticle_filter` | 准粒子滤波器 | P16 / `phase` | 过滤传播子/底噪 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 193 |
| `tunnel_linker` | 隧穿链路器 | P23 / `string` | 合并隧穿串联器/4D 电路桥 | 局部耦合用途可早于视界；远程/跨维度作用移入边界公设与成对锚 | 194 |
| `cryo_condensation_chamber` | 低温凝聚腔 | P16 / `cryo` | 低温和相干保持 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 195 |
| `quasiparticle_detector` | 准粒子捕获器 | P19 / `effective` | 捕获传播子片 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 196 |
| `feynman_compiler` | 费曼过程编译台 | P19 / `effective` | 外线/顶点/约束 -> 蓝图 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 197 |
| `topology_furnace` | 拓扑相变炉 | P16 / `phase` | 制造拓扑材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 198 |
| `horizon_framework_mk1` | III 型视界框架雏形 | P16 / `cryo` | 凝聚态用 III 型框架，不产生视界 | 低温材料框架雏形，不产生视界 | 199 |
| `quantum_optical_coprocessor_core` | 量子光学协处理核心（原 `quantum_coprocessor_core`） | P20 / `q_prepare` | 协处理器核心；物理路线为单光子玻色采样 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 205 |
| `cryo_control_plate` | 低温控制片 | P16 / `cryo` | 低温控制模块 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 206 |
| `coherent_control_line` | 相干控制线 | P20 / `q_prepare` | 相位控制和低损耗连接 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 207 |
| `entanglement_coupler_plate` | 纠缠耦合片 | P20 / `q_prepare` | 协处理器高级模块 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 208 |
| `wavefunction_cache_page` | 波函数缓存页 | P20 / `q_hybrid` | 缓存抽象波函数状态 | 制备/任务/测量摘要；不是未知量子态复制页 | 209 |
| `quantum_error_correction_plate` | 量子误差校验片 | P20 / `qec` | 降低协处理任务错误 | 先诊断校验；逻辑纠错要求编码、综合征和译码 | 210 |
| `quasiparticle_path_sample` | 准粒子路径样本 | P19 / `effective` | 高级模型训练/隐藏过程发现 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 211 |
| `synthesis_parameter_curve` | 合成参数曲线 | P20 / `q_hybrid` | III 型框架参数曲线 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 212 |
| `meso_synthesis_protocol` | 中观合成协议 | P20 / `q_hybrid` | 参数曲线和传感回读端口打包 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 213 |
| `quantum_optical_coprocessor` | 量子光学协处理器（原 `quantum_coprocessor`） | P20 / `q_hybrid` | 蓝图和材料状态 -> 曲线；物理路线：单光子 + 线性光路 + 后选择测量（玻色采样） | 按任务能力区分玻色采样与变分制备/测量，不互相冒充 | 214 |
| `cryo_control_cabinet` | 低温控制柜 | P16 / `cryo` | 给协处理器供低温 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 215 |
| `wavefunction_sampler` | 波函数采样仪 | P20 / `q_hybrid` | 读取坍缩风险 | 可测统计与校准风险，不能暴露任意波函数 | 216 |
| `error_correction_array` | 误差校验阵列 | P20 / `qec` | 提高逻辑稳定性 | 方块数量不足以单独证明码距与逻辑纠错能力 | 217 |
| `meso_synthesis_scheduler` | 中观合成调度器 | P20 / `q_hybrid` | 曲线分发到框架控制端口 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 218 |
| `gorguth_string_residue` | 戈古尔斯弦残迹 | P23 / `string` | 人造视界前置奇异材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 224 |
| `gorguth_string` | 戈古尔斯弦 | P23 / `string` | 视界边界锚点 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 225 |
| `horizon_constraint_plate` | 视界约束片 | P24 / `horizon_parts` | 视界约束环材料 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 226 |
| `entropy_pump` | 熵流泵 | P24 / `horizon_parts` | 定向抽取/排放熵流 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 227 |
| `holographic_membrane` | 全息信息膜 | P24 / `horizon_parts` | 视界存储介质 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 228 |
| `hawking_sampler` | 霍金采样器 | P25 / `mode_power` | 合并霍金采样/回收 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 229 |
| `penrose_accretion_coil` | 彭罗斯吸积线圈 | P25 / `mode_power` | 合并彭罗斯线圈/吸积盘环 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 230 |
| `artificial_horizon_core` | 人造视界核心 | P24 / `horizon` | 可控视界核心 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 231 |
| `emergency_quencher` | 紧急熄灭器 | P24 / `horizon_parts` | 安全停机，防止全损 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 232 |
| `string_anchor` | 戈古尔斯弦锚定器 | P23 / `string` | 残迹稳定为弦 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 233 |
| `holographic_membrane_writer` | 全息膜刻写器 | P24 / `horizon_parts` | 写入/读取全息膜 | 普通头/空白膜自举，视界高容量版后升级 | 234 |
| `horizon_framework` | III 型人造视界框架 | P24 / `horizon_parts` | 完整人造视界成型 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 235 |
| `black_hole_residue` | 黑洞解析残渣 | P25 / `mode_power` | 失败回收和高阶材料 | 只回收未转换预算，不重复返还已输出能量对应质量 | 241 |
| `horizon_energy_buffer` | 视界能量缓存 | P25 / `mode_power` | 高容量 FE/相干能存储 | 后期储备升级，不作为首次视界启动前置 | 242 |
| `holographic_data_slice` | 全息数据片 | P25 / `mode_store` | 黑洞存储产物 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 243 |
| `entropy_gradient_result` | 熵梯度结果 | P25 / `mode_compute` | 运算结果和维度优化 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 244 |
| `microstate_table` | 微观态枚举表 | P25 / `mode_compute` | 黑洞运算中间数据 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 245 |
| `dimension_rule_candidate` | 维度规则候选 | P27 / `rules` | 创世规则输入 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 246 |
| `black_hole_compute_core` | 黑洞运算核心 | P25 / `mode_compute` | 视界加速运算 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 247 |
| `entropy_rectifier` | 熵差整流器 | P25 / `mode_power` | 熵流差发电/整流 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 248 |
| `horizon_cooling_tower` | 视界冷却塔 | P25 / `mode_power` | 控制黑洞热预算 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 249 |
| `horizon_address_indexer` | 视界地址索引器 | P25 / `mode_store` | 全息数据分页寻址 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 250 |
| `world_heart_frequency` | 世界之心频率 | P26 / `heart` | 当前维度核心频率 | 受控可复测的世界特征记录，不毁掉母世界 | 256 |
| `dimension_parameter_matrix` | 维度参数矩阵 | P27 / `rules` | 创世参数集合 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 257 |
| `genesis_blueprint` | 创世蓝图 | P27 / `genesis` | 待编译维度设计 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 258 |
| `spatial_anchor` | 空间锚 | P27 / `return_anchor` | 固定维度入口和坐标 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 259 |
| `rule_interferometer` | 规则干涉器 | P27 / `rules` | 校验/压制规则冲突 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 260 |
| `compiled_dimension_core` | 已编译维度核心 | P27 / `genesis` | 维度入口和维护核心 | 晨曦世界种候选显示名，复制引用不复制世界实例 | 261 |
| `giant_node_framework` | 巨型节点框架 | P26 / `heart` | 世界之心萃取/维度维护模式 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 262 |
| `genesis_compiler` | 创世编译台 | P27 / `genesis` | 蓝图/矩阵/核心编译 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 263 |
| `dimension_ignition_ring` | 维度点火环 | P27 / `world` | 打开新维度入口 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 264 |
| `dimension_maintenance_tower` | 维度维护塔 | P28 / `maintain` | 压制规则漂移和熵增 | 保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。 | 265 |

## 阶段表独有条目

以下精确ID差异不自动要求新注册。导波线/诊断台应评估别名合并；多个装配台可作为同平台工装，但功能全部保留。

| ID | 原名 | R1能力 | 处置 | 原阶段表行 |
| --- | --- | --- | --- | --- |
| `doped_waveguide_wafer` | 掺杂导波晶片 | `precision` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 294 |
| `kamaen_threshold_filter` | 阈值滤波片 | `precision` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 295 |
| `kamaen_detector_junction` | 卡玛恩探测结 | `bridge` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 296 |
| `phase_tuning_chip` | 相位调谐片 | `precision` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 297 |
| `crystal_waveguide_line` | 晶体导波线 | `bridge` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 299 |
| `info_diagnostic_station` | 信息诊断台 | `scan` | 保留操作，候选合并为通用装配平台的工装/模式 | 308 |
| `resonant_signal_cache` | 共振信号缓存器 | `store` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 338 |
| `signal_cache_plate` | 信号缓存片 | `store` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 339 |
| `frequency_route_plate` | 频率路由片 | `network` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 340 |
| `kamaen_nonlinear_medium_station` | 卡玛恩非线性介质制备台 | `photonic_logic` | 保留操作，候选合并为通用装配平台的工装/模式 | 428 |
| `photonic_gate_assembly_station` | 光逻辑门封装台 | `photonic_logic` | 保留操作，候选合并为通用装配平台的工装/模式 | 429 |
| `bistable_cell_assembly_station` | 双稳态晶胞组装台 | `photonic_logic` | 保留操作，候选合并为通用装配平台的工装/模式 | 430 |
| `photonic_control_core_assembly` | 光控制核封装台 | `photonic_control` | 保留操作，候选合并为通用装配平台的工装/模式 | 431 |
| `photonic_pulse_processor_assembly` | 光脉冲处理器封装台 | `photonic_pulse` | 保留操作，候选合并为通用装配平台的工装/模式 | 432 |
| `photonic_ram_assembly` | 光RAM 封装台 | `photonic_ram` | 保留操作，候选合并为通用装配平台的工装/模式 | 433 |
| `single_photon_source` | 单光子源 | `q_lab` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 507 |
| `snspd_detector` | SNSPD 探测器 | `snspd` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 508 |
| `long_term_photonic_memory` | 长期光存储单元 | `advanced_optics` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 628 |
| `wdm_multiplexer` | WDM 复用器 | `advanced_optics` | 保留为对应工艺/设备模块；首次版与规模升级分别定义 | 629 |
| `all_optical_switch_core` | 全光交换核 | `advanced_optics` | 保留全光专化，不要求电气退场 | 630 |

## 字典之外的玩法家族

| 家族 | 首次能力 | 去向/细节 |
| --- | --- | --- |
| 木筛、木盆、开局材料 | manual | 发展线一§2，粗版自举 |
| 有机基底、纤维/树脂/培养 | bio | 发展线三§6，输入有机质量约束 |
| 基本发电与泵/物流接口 | power / feedback | 发展线普通能源与原版漏斗先可用 |
| 硅/化学前体与封装材料 | doping / precision | 发展线二§2–3，需要物料表继续细化 |
| EDA宏单元、冷却/时序/屏蔽与封装族 | eda / package | 发展线三§1，模板入门，微结构深化 |
| 参数空间、算子、图与高级Runtime | runtime | 发展线三§2，受限可返回编辑场 |
| 数据集、校准、轨迹、策略和主动实验 | train / rl / active | 发展线三§5–7，实验来源与独立验收 |
| 多DNS、无线G1–G6、机柜族 | network / advanced_network | 发展线三§3–4，地址/服务/权限及预算 |
| 全部模型族与实体/交易/对抗 | model_families / entity_policy | 发展线三§5–6，各有支持任务与离线版本 |
| 外部API与本地后端 | api | 发展线三§7，关闭外部服务不阻塞 |
| 流水线、无人机与计算辅助装备 | production_cell / drone / adaptive_gear | 发展线三的[应用续稿](MIDGAME_APPLICATIONS.md)，登记可选能力；材料数量及适配尚待细化 |
| SPAD/预告源/计数器/态制备 | q_lab / q_prepare | 发展线四§4–5，先校准后量子任务 |
| 星录、谱尺、背景与几何 | sky / spectrum / cosmic_geometry | 发展线四§3、6，独立宇观线 |
| 接界棱镜、间隙腔、互证谱册 | micro_boundary / cross | 发展线四§6，实体与档案分开 |
| 空白膜/普通头/启动储备 | horizon_parts | 发展线五§2，解除视界自举环 |
| 新维度槽、返回锚、休眠救援 | return_anchor / maintain | 发展线五§5–6，不覆盖实例、不困住玩家 |

覆盖意味着已安排位置、用途和修订方向，不等于所有玩法子参数均已详细规范或实现。旧传感器表§14复用已有实体；全局组件表是共享状态契约，不重复计入164个实体。

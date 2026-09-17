# R4旧稿去向与本轮修订

R4不删除旧稿。这里明确当前阶段采用的定位；R2/R3用于追溯，冲突处以[R4总案](R4_STAGE_DESIGN.md)及对应专题为准。

## 旧字典67项

| 旧ID/名称 | R4定位 | 完整设计 |
| --- | --- | --- |
| `kamaen_crystal_t2` / 二代卡玛恩晶体 | 按母批/处理状态与器件模板组织；二代是用途检验名，N/P是目标响应族 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `kamaen_dopant` / 卡玛恩掺杂剂 | 按母批/处理状态与器件模板组织；二代是用途检验名，N/P是目标响应族 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `kamaen_wafer` / 卡玛恩晶片 | 按母批/处理状态与器件模板组织；二代是用途检验名，N/P是目标响应族 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `kamaen_pn_junction` / 卡玛恩 PN 结 | 按母批/处理状态与器件模板组织；二代是用途检验名，N/P是目标响应族 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `electronic_logic_gate` / 电逻辑门片 | 门控阵列片、明确状态模块、按尺度分开的互连与实际晶振 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `lithography_mask` / 光刻掩膜 | 粗接触模板先行，精密层组后续；防护按实际覆盖与用途 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `lithography_mask_set` / 分层光刻掩膜组 | 粗接触模板先行，精密层组后续；防护按实际覆盖与用途 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `process_protection_kit` / 工艺防护套件 | 粗接触模板先行，精密层组后续；防护按实际覆盖与用途 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `timing_structure_cell` / 时序结构单元 | 门控阵列片、明确状态模块、按尺度分开的互连与实际晶振 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `crystal_interconnect` / 晶体互连线 | 门控阵列片、明确状态模块、按尺度分开的互连与实际晶振 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `kamaen_oscillator` / 卡玛恩晶振 | 门控阵列片、明确状态模块、按尺度分开的互连与实际晶振 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `coherent_energy_buffer` / 相干能缓存 | 激励能量、缓存、调节与集中供给分别记账，参考/相干状态另算 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `coherent_energy_regulator` / 相干能稳压器 | 激励能量、缓存、调节与集中供给分别记账，参考/相干状态另算 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `ion_implanter` / 离子注入器 | 保留对应实物工位及顺序历史，统一面板向已连接工位派任务 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `lattice_annealing_furnace` / 晶格退火炉 | 保留对应实物工位及顺序历史，统一面板向已连接工位派任务 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `lithography_projector` / 光刻投影器 | 保留对应实物工位及顺序历史，统一面板向已连接工位派任务 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `etching_tank` / 刻蚀槽 | 保留对应实物工位及顺序历史，统一面板向已连接工位派任务 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `tier2_optical_process_framework` / II 型光路工艺框架 | 保留对应实物工位及顺序历史，统一面板向已连接工位派任务 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `hardware_diagnostic_station` / 硬件诊断台 | 工程台统一入口，诊断/封装仍由实体设备执行；初版无需计算板自举 | [对应专题](R4_UNIFIED_WORKBENCH.md) |
| `electronic_control_chip` / 电控接口芯片 | 实际模块与制造模板分开；角色名不重复产出硬件，双路线分账 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `electronic_matrix_tile` / 电矩阵瓦片 | 实际模块与制造模板分开；角色名不重复产出硬件，双路线分账 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `electronic_activation_tile` / 电激活瓦片 | 实际模块与制造模板分开；角色名不重复产出硬件，双路线分账 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `memory_page` / 内存页 | 工作2 KiB与持久16 KiB使用不同已测模板；逻辑页仅分配地址 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `eda_module_plate` / EDA 模块片 | 实际模块与制造模板分开；角色名不重复产出硬件，双路线分账 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `chip_blueprint_writer` / 芯片蓝图台 | 工程台统一入口，诊断/封装仍由实体设备执行；初版无需计算板自举 | [对应专题](R4_UNIFIED_WORKBENCH.md) |
| `chip_packaging_station` / 芯片封装台 | 工程台统一入口，诊断/封装仍由实体设备执行；初版无需计算板自举 | [对应专题](R4_UNIFIED_WORKBENCH.md) |
| `packaged_logic_chip` / 封装逻辑芯片 | 实际模块与制造模板分开；角色名不重复产出硬件，双路线分账 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `motherboard_blueprint` / 集成板蓝图 | B01/B02与R04两托盘柜；实际背板、包接口和世界线缆 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `configurable_motherboard` / 可配置集成板 | B01/B02与R04两托盘柜；实际背板、包接口和世界线缆 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `network_interface_chip` / 网络接口芯片 | B01/B02与R04两托盘柜；实际背板、包接口和世界线缆 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `fiber_switch` / 光纤交换机 | B01/B02与R04两托盘柜；实际背板、包接口和世界线缆 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `sensor_hub` / 传感器汇聚器 | 通用采样服务配对应物理量探头，天线仅服务其波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `model_component_gateway` / 模型组件网关 | 统一工作台中的语义图/部署页，世界底座和参数空间仍为同一图的表现 | [对应专题](R4_UNIFIED_WORKBENCH.md) |
| `model_compiler` / 模型编译器 | 统一工作台中的语义图/部署页，世界底座和参数空间仍为同一图的表现 | [对应专题](R4_UNIFIED_WORKBENCH.md) |
| `server_rack` / 服务器机柜 | B01/B02与R04两托盘柜；实际背板、包接口和世界线缆 | [对应专题](R4_HARDWARE_AND_CLUSTER.md) |
| `storage_center_controller` / 存储中心控制器 | 记录节点先行，再部署索引/参数库/底噪应用；应用不提供额外存储 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `world_noise_sample` / 世界底噪样本 | 有来源原始记录和解释视图；辐射谱仅限当前探头实测波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `thermal_noise_plate` / 热噪声谱片 | 有来源原始记录和解释视图；辐射谱仅限当前探头实测波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `radiation_noise_plate` / 背景辐射谱片 | 有来源原始记录和解释视图；辐射谱仅限当前探头实测波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `quantum_fluctuation_plate` / 量子涨落片 | 交界保留至P18对应仪器；当前只留未解释残差，禁止提前标成量子实证 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `chunk_entropy_record` / 区块熵流记录 | 当前登记输入/输出及估计模型的账本，不宣称测出任意区块热力学总熵 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `noise_database` / 底噪数据库 | 记录节点先行，再部署索引/参数库/底噪应用；应用不提供额外存储 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `macro_info_index_core` / 宏观信息索引核心 | 记录节点先行，再部署索引/参数库/底噪应用；应用不提供额外存储 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `noise_spectrometer` / 底噪谱仪 | 通用采样服务配对应物理量探头，天线仅服务其波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `thermodynamic_antenna` / 热力学背景天线 | 通用采样服务配对应物理量探头，天线仅服务其波段 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `entropy_flow_meter` / 熵流计 | 当前登记输入/输出及估计模型的账本，不宣称测出任意区块热力学总熵 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `info_center_controller` / 信息中心控制器 | 记录节点先行，再部署索引/参数库/底噪应用；应用不提供额外存储 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `silicon_photonic_waveguide_blank` / 硅光波导毛坯 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `silicon_photonic_waveguide` / 硅光波导 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `mzi_modulator` / 马赫-曾德尔调制器 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `phase_tuner` / 相位调谐器 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `silicon_photodetector` / 硅光探测器 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `single_freq_laser_source` / 单频激光源 | 粗光件与精密变体共用器件/制程模型，光电并行 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `calibration_token` / 光路校准令牌 | 改为对象、映射、条件与报告的绑定记录，无魔法正确性消耗品 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `kamaen_nonlinear_medium` / 卡玛恩非线性介质 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_logic_gate` / 光逻辑门 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `kamaen_bistable_cell` / 卡玛恩双稳态晶胞 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_control_core` / 光控制核 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_coprocessor` / 光协处理器 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_gpu_unit` / 光GPU 单元 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_pulse_processor` / 光脉冲处理器 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `photonic_ram_unit` / 光RAM 单元 | 先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套 | [对应专题](R4_RUNTIME_AND_RESEARCH.md) |
| `coherent_energy` / 相干能（资源） | 激励能量、缓存、调节与集中供给分别记账，参考/相干状态另算 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `photonic_waveguide_etching_station` / 波导刻蚀台 | 对应刻蚀、模块拼装、校准工装；专用外壳可保留，不重复基础流水线 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `mzi_weaving_station` / MZI 编织台 | 对应刻蚀、模块拼装、校准工装；专用外壳可保留，不重复基础流水线 | [对应专题](R4_MATERIALS_MACHINES.md) |
| `laser_pump_tower` / 激光泵浦塔 | 激励能量、缓存、调节与集中供给分别记账，参考/相干状态另算 | [对应专题](R4_MODELS_AND_FACTORS.md) |
| `photonic_calibration_station` / 光路校准台 | 对应刻蚀、模块拼装、校准工装；专用外壳可保留，不重复基础流水线 | [对应专题](R4_MATERIALS_MACHINES.md) |

## 34个补充内容族

| 族 | 合并入口 | 保留范围 |
| --- | --- | --- |
| C01 器件夹具与测试座 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C02 粗硅质片/抛光支撑片 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C03 绝缘/覆铜/多层空板 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C04 触点、引脚与插槽座 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C05 封装壳与热界面 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C06 实际裸片 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C07 芯片设计记录 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C08 工艺任务单 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C09 测试/分档报告 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C10 采样门/FIFO/流水锁存/相位标记/刷新器 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C11 分束/耦合/光口件 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C12 石英纤芯与世界光纤 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C13 电数据线/控制线与端口面板 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C14 普通电源与供能背板 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C15 风冷/液冷模块与管路 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C16 机柜框架/机板托盘/检修面板 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C17 数据/供能/同步背板 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C18 网络前端/无线天线与隔离件 | [专题](R4_MATERIALS_MACHINES.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C19 集群编排核心 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C20 服务/部署配置卡 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C21 通用I/O网关底座 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C22 数据/运算节点底座 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C23 路由节点底座 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C24 触发节点底座 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C25 状态寄存节点底座 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C26 参数晶胞/矩阵板/晶体簇 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C27 参数库 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C28 模型工件/模块模板 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C29 数据集/实验日志/轨迹 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C30 训练配置/候选参数/验收报告 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C31 检查点 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C32 执行网关与回执缓存 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C33 压力测试与算子能力报告 | [专题](R4_RUNTIME_AND_RESEARCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |
| C34 空间编辑入口/投影模块 | [专题](R4_UNIFIED_WORKBENCH.md) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |

## 阶段表额外15个ID

| 原ID | 当前处理 |
| --- | --- |
| `doped_waveguide_wafer` | kamaen_wafer的导波用途成品变体；操作入口、材料与实体位置遵循R4 |
| `kamaen_threshold_filter` | 阈值滤波器件；按模板映射到electronic_logic_gate或光学器件，不能无条件互换；操作入口、材料与实体位置遵循R4 |
| `kamaen_detector_junction` | 探测结器件族；与silicon_photodetector按材料/量程分型；操作入口、材料与实体位置遵循R4 |
| `phase_tuning_chip` | phase_tuner的前置相位晶片，需加驱动封装；操作入口、材料与实体位置遵循R4 |
| `crystal_waveguide_line` | 模块导波材料/世界光纤按尺度分开；不直接等同crystal_interconnect全部类型；操作入口、材料与实体位置遵循R4 |
| `info_diagnostic_station` | hardware_diagnostic_station的信息/信号测试模式；操作入口、材料与实体位置遵循R4 |
| `resonant_signal_cache` | 实体缓存模块；接入真实页容量与寿命；操作入口、材料与实体位置遵循R4 |
| `signal_cache_plate` | memory_page/保持器件的缓存用途变体，易失性明示；操作入口、材料与实体位置遵循R4 |
| `frequency_route_plate` | 路由配置内容载片+实际接口模块，不能只放数据卡就增加物理口；操作入口、材料与实体位置遵循R4 |
| `kamaen_nonlinear_medium_station` | II型工艺线的共掺杂/阈值试验工装；操作入口、材料与实体位置遵循R4 |
| `photonic_gate_assembly_station` | 精密装配台的光门模式；操作入口、材料与实体位置遵循R4 |
| `bistable_cell_assembly_station` | 精密装配台的双稳态模式；操作入口、材料与实体位置遵循R4 |
| `photonic_control_core_assembly` | 芯片封装台的光控制模块路线；操作入口、材料与实体位置遵循R4 |
| `photonic_pulse_processor_assembly` | 芯片封装台的光脉冲模块路线；操作入口、材料与实体位置遵循R4 |
| `photonic_ram_assembly` | 芯片封装台的光保持/刷新模块路线；操作入口、材料与实体位置遵循R4 |

## 本轮反复检查后形成的修订

1. 从所有影响因素归纳八类，参数属于实际物理层，默认只展示当前相关部分。
2. 工程册、工程台和各机器打开同一项目；设计图、物理结构与模型语义保持各自真值与明确绑定。
3. 第一颗芯片走粗模块实验封装，精密控制器再反过来改进流片设备；首台仪器不依赖待测成品。
4. 容量/算力来自有展开规模的制造模板；B01工作4 KiB扣512 B系统预留，示例推理32/训练16批分别核算。
5. R2.1四托盘柜改为R04两前维护托盘，后部用于背板和风路；保留2×2×3教学外形，但不把四盘与新风路同时塞进原空间。
6. B02增加实际侧挂载板、支撑、插座和光源；不在满板上免费增加器件。
7. 初始光模块仅保证2×2非负强度映射，通用有符号MatMul保留电后端；光五件套仍作为本阶段拓展，有对应结构与验证。
8. 线缆、支撑、管路引用同一实体几何；虚拟模型排版不制造线长。自动连接草稿与实际施工分开。
9. 小模型在单板训练，集群解决规模/位置问题；RL和主动采样使用真实有界动作，不成为唯一通关门槛。
10. 量子涨落记录保留交界，只有后期对应仪器才赋该含义；普通残差不提前解释成量子信号。

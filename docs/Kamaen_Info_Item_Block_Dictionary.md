# Kamaen Info 物品与方块开发字典

版本：v0.4 Dictionary Draft  
用途：给开发、数据包、贴图、配方、BlockEntity、Data Component、GUI、JEI/EMI 分类和测试拆分提供统一条目表单。  
状态提示：本文的 Stage 4-6 条目按“多工艺 EDA + 芯片/封装隔离”方向维护。电逻辑、光逻辑、量子微逻辑都可以作为 EDA 元件库，但不同物理环境的主逻辑必须隔离到不同芯片或不同受控区域。完整规则见 `docs/Kamaen_Info_Computing_EDA_Design.md`。  

## 1. 字典字段

每个条目尽量按同一套字段理解。

| 字段 | 含义 |
| --- | --- |
| `id` | 注册 id，默认命名空间为 `kamaeninfo` |
| `中文名` | 游戏内显示名建议 |
| `类型` | `item`、`block`、`machine`、`multiblock_controller`、`sensor`、`data_item`、`component_item` |
| `阶段` | 科技树阶段 |
| `获取/合成` | 玩家如何获得，含机器、结构、主要输入 |
| `开发作用` | 此条目在系统中的职责 |
| `Data Component` | 需要随物品移动并参与配方/tooltip/查询的数据 |
| `BlockEntity 状态` | 只属于方块运行态的数据 |
| `MC 原版关联` | 原版材料、交互或玩家认知锚点 |
| `Kamaen 参数关联` | 与模组内部哪些参数、配方类型、能力接口关联 |
| `配套/同类` | 同套物品、升级件、互相配合项 |
| `多方块` | `否`、`附属`、`控制器`、`结构模块` |
| `传感器` | 传感类型；非传感器写 `无` |
| `异步/预算` | 是否需要冷却、缓存、任务队列、批量结算或独立线程；默认不独立开线程 |
| `自定义程度` | `低`、`中`、`高`；高表示玩家可配置参数较多 |
| `实现备注` | 开发拆分、降级方案、MVP 边界 |

## 2. 全局 Data Component 字典

| id | 中文名 | 类型 | 阶段 | 获取/合成 | 开发作用 | Data Component | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kamaen_crystal_state` | 卡玛恩晶体状态 | component | 全阶段 | 所有晶体类物品自带 | 统一描述晶体材料 | `spectrum_signature`,`axis_tensor`,`stress`,`noise_index`,`coherence`,`doping_type`,`doping_concentration`,`gate_axis`,`cutoff_axis`,`feedback_axis`,`background_noise_response` | 无 | `vector_blasting`,`doping`,`framework_process`,`condensed_matter_synthesis` | 所有晶体、晶片、环、约束片 | 高 | 必须优先实现，后续配方都依赖 |
| `infosignal` | 信息信号 | component | 三以后 | 探针、信息单元、总线写入 | 统一信息读取输出 | `type`,`value`,`frequency_vector`,`confidence`,`timestamp`,`source_id` | 红石、比较器、容器状态 | `IKamaenReadable`,`frequency_bus`,`hardware_control_node` | 信息单元、封装片、频率总线 | 中 | value 初版可用 string/int NBT 表示，后续类型化 |
| `noise_sample` | 底噪样本 | component | 五以后 | 底噪谱仪写入 | 统一维度底噪读数 | `noise_layer_id`,`amplitude`,`frequency`,`entropy_density`,`coherence`,`dimension_key`,`interpretation_tags` | 天气、群系、维度 | `NoiseLayerSampler`,`background_noise_sampling` | 世界底噪样本、谱片、数据库 | 中 | 同维度同层缓存 200 tick |
| `feynman_blueprint` | 费曼过程蓝图 | component | 七以后 | 费曼编译台写入 | 描述凝聚态合成语法 | `external_lines`,`vertices`,`propagators`,`conservation_constraints`,`loop_order`,`target_material` | 锻造模板认知 | `feynman_process`,`condensed_matter_synthesis` | 传播子片、顶点片、III 型框架 | 高 | 只做抽象约束校验，不做真实物理模拟 |
| `synthesis_parameter_curve` | 合成参数曲线 | component | 八以后 | 量子光学协处理器输出 | 框架动态参数序列 | `parameter_channels`,`time_points`,`confidence`,`source_blueprint` | 唱片/地图式数据载体 | `quantum_optical_coprocessing`,`framework_control_port` | 中观调度器、III 型框架 | 高 | 曲线用有限采样点，不存连续函数 |
| `kamaen_storage_page` | 卡玛恩存储页 | component | 五以后 | 内存页、数据库、全息片复用 | 通用 typed payload 存储 | `page_type`,`capacity`,`used`,`namespace`,`payload_ref` | 书、地图、末影箱 | `hardware_assembly`,`noise_database`,`holographic_storage` | 内存页、参数页、全息数据片 | 中 | 可先用 NBT payload，后续改索引后端 |
| `chip_logic_blueprint` | 芯片逻辑蓝图 | component | 五以后 | 芯片蓝图台写入 | 描述 EDA 芯片的逻辑输出、工艺域、原理图、微结构版图、端口、时序和环境要求 | `chip_role`,`die_domain`,`process_node`,`logic_family`,`schematic_graph`,`layout_grid`,`layer_stack`,`microstructures`,`layout_nets`,`gate_counts`,`memory_blocks`,`interconnect_layers`,`timing_profile`,`timing_tier`,`timing_mode`,`clock_domains`,`timing_domains`,`pipeline_stages`,`sync_boundaries`,`cooling_interfaces`,`coherence_interfaces`,`io_ports`,`bridge_ports`,`frequency_tier`,`environment_requirements`,`drc_report`,`timing_report`,`simulation_report`,`score_cache` | 红石逻辑、锻造模板 | `chip_design`,`control_ops`,`io_bandwidth`,`matrix_ops`,`sampling_ops`,`coherence_draw`,`timing_budget` | 逻辑模块、光逻辑门、量子微逻辑片、芯片封装、主板蓝图 | 高 | 类微电子 EDA：原理图 + 版图 + DRC + 抽象仿真；F1-F5 是频率等级，T0-T5 是时序等级；玩家设计系统级时序，不做电平/阻抗/晶体管级时序 |
| `chip_package_profile` | 芯片封装画像 | component | 五以后 | 封装台写入 | 描述芯片封装、引脚/光口/低温口、散热、相干与频率上限 | `package_type`,`pin_count`,`port_layout`,`port_width`,`thermal_transfer`,`cooling_ports`,`coherence_coupling`,`frequency_limit`,`socket_type`,`environment_domain` | 无 | `chip_packaging`,`motherboard_socket`,`thermal_budget`,`coherence_budget` | 封装芯片、光背板、低温载板、诊断台 | 高 | 决定芯片能否装进对应主板/光背板/低温载板槽 |
| `hardware_blueprint` | 硬件蓝图 | component | 五以后 | 蓝图台或主板编辑器写入 | 描述主板、光背板、低温载板、混合集成节点或模型组件网络 | `blueprint_type`,`grid_size`,`zones`,`slots`,`ports`,`chipsets`,`bus_layers`,`cooling_pipes`,`coherent_energy_lines`,`frequency_domains`,`environment_domains`,`bridge_map`,`score_cache` | 纸、锻造模板、地图 | `hardware_assembly`,`motherboard_layout`,`network_ports`,`eda_environment_domains` | 主板蓝图、光背板蓝图、低温载板蓝图、模型蓝图 | 高 | 初版用有限格点和枚举槽位；环境域隔离失败直接降低 `environment_fit` |
| `network_port_profile` | 网络端口画像 | component | 五以后 | 主板、交换机、网关、模型组件生成 | 统一描述可连接接口 | `port_id`,`side`,`direction`,`protocol`,`frequency_tier`,`bandwidth`,`packet_types`,`permission_scope` | 红石面向、漏斗方向 | `model_data_port`,`fiber_port`,`wireless_port`,`sensor_port` | 主板、交换机、传感器汇聚器、模型网关 | 高 | 方块 tooltip 和诊断台都可读取 |
| `dimension_parameter_matrix` | 维度参数矩阵 | component | 十 | 创世编译台写入 | 维度创世参数集合 | `terrain_base`,`biome_weight`,`physics_rule`,`resource_spectrum`,`entity_spawn`,`noise_structure`,`entropy_rate` | 地图、数据包维度 | `dimension_compiling` | 创世蓝图、维度核心 | 高 | v1.0 使用预置模板，不做无限动态规则 |

## 3. 阶段一：圆石频谱初炼

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `crude_spectrum_scrap` | 粗频谱碎屑 | item | 手摇频谱筛处理圆石 | 手动起步中间产物 | 可选 `spectrum_bias`,`purity` | 无 | 圆石 | `fractionating` 前置 | 粗频谱泥浆、频谱滤渣 | 否 | 无 | 无 | 低 | MVP 可无组件，作为普通物品 |
| `crude_spectrum_slurry` | 粗频谱泥浆 | item/fluid_candidate | 圆石 + 水，经分馏塔 | 分馏输入，承接污染 | `frequency_integral`,`contamination` | 若做流体则在 tank 中记录量 | 圆石、水 | `fractionating` | 滤膜、分馏塔 | 否 | 无 | 20 tick 分馏 | 中 | 初版建议物品化，流体后移 |
| `spectrum_slag` | 频谱滤渣 | item | 泥浆分馏副产 | 白噪链核心副产物 | `residue_spectrum`,`heat_response` 可选 | 无 | 无 | `fractionating`,`spectrum_tuning` | 均值化圆石、白噪晶种 | 否 | 无 | 无 | 低 | P0，许多配方会用 |
| `whitened_cobblestone` | 均值化圆石 | block/item | 频谱滤渣 + 热噪坩埚 | 白噪晶种基底 | `noise_mean`,`mean_deviation` 可选 | 无 | 圆石 | `white_noise_potential` | 频谱滤渣、白噪晶种 | 否 | 分光镜可读 | 无 | 低 | 可直接作为方块，也可只做物品 |
| `white_noise_seed` | 白噪晶种 | item | 均值化圆石 + 频谱滤渣 | 卡玛恩晶体起点 | `white_noise_potential`,`mean_deviation` | 无 | 无 | `vector_blasting` 输入 | 粗卡玛恩晶体 | 否 | 分光镜可读 | 无 | 低 | 主线门槛物品 |
| `spectrum_powder` | 频谱粉末 | item | 泥浆分馏副产 | 合并铁粉/煤粉/铜粉/矿粉 | `powder_type`,`purity` | 无 | 铁、煤、铜、沙子 | 掺杂剂、爆震粉、基础材料 | 滤膜、分馏塔 | 否 | 无 | 无 | 中 | 用 `powder_type=iron/coal/copper/mineral/silica` |
| `spectrum_membrane` | 频谱滤膜 | item | 纸/线/铁/玻璃板合成 | 控制分馏偏向 | `membrane_type`,`durability`,`bias_vector` | 无 | 纸、线、铁、玻璃 | `fractionating` 副产权重 | 分馏塔 | 否 | 无 | 无 | 中 | 替代多个滤膜 id |
| `hand_spectrum_sieve` | 手摇频谱筛 | block/tool | 木棍 + 铁锭 + 滤膜 | 空岛/早期手动产物 | 无 | `work_accumulator`,`input_slot`,`output_slot` | 工作台、筛子认知 | `fractionating` 手动模式 | 粗频谱碎屑 | 否 | 无 | 右键积累 | 低 | 分馏塔后自然淘汰 |
| `fractionating_tower` | 搅拌分馏塔 | multiblock_controller | 铁/铜/玻璃/桶/搅拌轴 | 第一台自动机器 | 无 | `contamination`,`filter_slot`,`progress`,`water_tank`,`cached_profile` | 水、圆石、漏斗 | `fractionating`,`MachineProfile` | 滤膜、热噪坩埚 | 控制器 | 无 | 20 tick 一次积分 | 中 | v0.1 固定结构，后续可变 |
| `thermal_noise_crucible` | 热噪坩埚 | machine | 熔炉 + 铁 + 频谱滤渣 | 热处理滤渣和均值化圆石 | 无 | `heat_level`,`fuel_time`,`progress` | 熔炉 | `heat_response`,`spectrum_loosen` | 频谱滤渣、均值化圆石 | 否 | 温度读数可选 | 熔炉式 tick | 低 | 可复用熔炉进度逻辑 |
| `basic_spectroscope` | 初级分光镜 | item/block | 玻璃 + 铁 + 频谱滤渣 | 早期分析工具 | 无 | 若为方块则 `target_slot` | 望远镜、比较器认知 | 读取 `spectrum_signature`,`peak_deviation`,`white_noise_potential` | 所有早期材料 | 否 | S0 频谱读数 | 无 | 低 | 右键物品显示 tooltip 最省事 |

## 4. 阶段二：白噪结晶与力学合成

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `blast_powder` | 爆震粉 | item | 频谱粉末 + 火药/煤粉 + 滤渣 | 模拟爆破能源 | `blast_strength`,`waveform_purity` 可选 | 无 | 火药、TNT | `vector_blasting` | 爆炸室 | 否 | 无 | 无 | 低 | 不造成真实爆炸 |
| `ideal_rigid_plate` | 理想刚体板 | block | 铁块 + 均值化石材 | 爆炸室反射模块 | 无 | 无 | 铁块、黑曜石 | `reflectivity`,`rigidity`,`waveform_preserve` | 缓冲砂、爆炸室 | 结构模块 | 无 | 扫描时计分 | 低 | 方块状态可带朝向 |
| `buffer_sand_layer` | 缓冲砂层 | block | 沙子 + 均值化圆石 | 降低爆破强度，提高容错 | 无 | 无 | 沙子 | `absorption`,`strength_dampen`,`tolerance` | 刚体板、靶座 | 结构模块 | 无 | 扫描时计分 | 低 | 失败保护方块 |
| `target_pedestal` | 靶座 | block | 铁 + 石材 | 固定晶种/晶体 | 无 | `held_item`,`impact_direction` | 展示框/盔甲架 | `vector_blasting` 输入位 | 爆炸室控制器 | 结构模块 | 无 | 离散爆破 | 低 | 需要物品展示/槽位 |
| `raw_kamaen_crystal` | 粗卡玛恩晶体 | item | 白噪晶种 + 爆破评分达标 | 第一代晶体母体 | `kamaen_crystal_state` | 无 | 无 | `axis_tensor`,`stress`,`noise_index` | 三轴晶体、碎片 | 否 | 干涉仪可读 | 无 | 中 | 已有贴图可对应 |
| `kamaen_crystal_debris` | 卡玛恩晶体碎片 | item | 爆破或工艺失败 | 失败回收和低级配方 | `debris_type`,`residual_spectrum` | 无 | 无 | 失败产物、掺杂回收 | 裂纹晶体/粉尘合并 | 否 | 分光镜可读 | 无 | 中 | 合并裂纹晶体和频谱粉尘 |
| `waveguide_kamaen_crystal` | 导波型卡玛恩晶体 | item | 粗晶体 + X 轴爆破 | 总线、导线、信号结构材料 | `kamaen_crystal_state.axis_x=waveguide` | 无 | 无 | `frequency_bus`,`signal_loss` | 抗压、稳谱晶体 | 否 | 干涉仪可读 | 无 | 中 | 可用同一晶体 item + component，也可独立 id |
| `compression_kamaen_crystal` | 抗压型卡玛恩晶体 | item | 粗晶体 + Y 轴爆破 | 高压、结构、视界材料 | `axis_y=compression_resistance` | 无 | 无 | `structure_integrity`,`pressure` | 导波、稳谱晶体 | 否 | 干涉仪可读 | 无 | 中 | 后期吸积/约束材料常用 |
| `stable_spectrum_kamaen_crystal` | 稳谱型卡玛恩晶体 | item | 粗晶体 + Z 轴爆破 | 能量、相干、底噪相关基底 | `axis_z=spectrum_retention`,`coherence` | 无 | 无 | `coherent_energy`,`background_noise_sampling` | 导波、抗压晶体 | 否 | 干涉仪可读 | 无 | 中 | 阶段四以后高频使用 |
| `polarized_kamaen_crystal` | 偏振卡玛恩晶体 | item | I 型框架压合 | 高级传感器/偏振模块 | `polarization_direction`,`tensor_alignment` | 无 | 无 | `stress_ellipsoid`,`framework_process` | 应力传感器、干涉仪 | 否 | 干涉仪可读 | 无 | 中 | P1，可后移 |
| `stress_recording_plate` | 应力记录片 | data_item | 铁板 + 晶体碎片，或框架记录 | 保存一次应力快照 | `stress_history`,`ellipsoid_snapshot`,`source_crystal` | 无 | 地图/纸张 | `framework_process` 诊断 | 应力传感器、I 型框架 | 否 | S1 数据输出 | 无 | 中 | 可作为 JEI 教学数据物品 |
| `explosion_chamber_controller` | 爆炸室控制器 | multiblock_controller | 铁、红石、刚体板 | 扫描结构并计算爆破评分 | 无 | `cached_profile`,`last_vector_impulse`,`progress`,`input_slots` | TNT 认知但不爆炸 | `vector_blasting`,`MultiblockFormer` | 刚体板、缓冲砂、靶座 | 控制器 | 可接应力传感器 | 离散任务，无线程 | 中 | 首版固定 3x3x3 |
| `stress_sensor` | 应力传感器 | sensor/block | 偏振晶体 + 红石 + 铁 | 读取晶体应力 | 无 | `precision`,`last_stress_reading` | 比较器 | `stress`,`stress_ellipsoid`,`sensor_modules` | I 型框架 | 附属 | S1/S2 应力 | 20 tick 或工艺结束读 | 中 | 放入框架提高评分精度 |
| `axial_press_head` | 轴向压头 | block | 活塞 + 铁块 + 晶体 | 提供可控压力 | 无 | `pressure_vector`,`force`,`extension` | 活塞 | `pressure`,`axis_layout`,`actuator_modules` | I 型框架 | 结构模块 | 无 | 运行时读缓存 | 中 | 方块朝向决定压力方向 |
| `tier1_mechanical_framework` | I 型力学合成框架 | multiblock_controller | 爆炸室升级 + 压头/传感器 | 力学合成研究站 | 无 | `FrameworkProfile(tier=1)`,`dynamic_parameters`,`running_process` | 多方块机器 | `framework_process`,`precision_budget`,`stress_reading` | 爆炸室、偏振晶体 | 控制器 | S2 框架传感 | 缓存画像，无线程 | 高 | 只支持压力/向量/应力三参数起步 |

## 5. 阶段三：共振调谐与信息读取

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tuning_wafer` | 调谐晶片 | item | 卡玛恩晶体切片/抛光 | 频谱锁相和总线基础材料 | `frequency_response`,`lock_range` | 无 | 无 | `spectrum_tuning`,`frequency_domain` | 锁相器、总线、探针台 | 否 | 无 | 无 | 中 | 阶段三核心消耗品 |
| `intrinsic_spectrum_sample` | 固有频谱样本 | data_item | 锁相器读取目标物品/方块 | 目标频谱模板 | `sampled_signature`,`source_type`,`source_id`,`confidence` | 无 | 任意方块/物品 | `spectrum_signature`,`resonance_type` | 共振晶体、锁相器 | 否 | S0/S1 采样数据 | 锁相有冷却 | 中 | 初版用注册名 hash |
| `information_unit` | 信息单元 | data_item | 探针台读取后封装 | `InfoSignal` 基础载体 | `infosignal` | 无 | 红石、方块状态 | `frequency_bus`,`IKamaenReadable` | 封装片、红石模块 | 否 | 数据输出 | 读取冷却 | 中 | 可堆叠性取决于 signal 是否相同 |
| `resonance_catalyst_crystal` | 共振催化晶体 | item | 晶体 + 固有频谱样本 + 锁相器 | 加速/优化对应机器或材料流程 | `kamaen_crystal_state`,`target_category`,`resonance_efficiency` | 无 | 熔炉/作物/机器 | `total_resonance`,`speed_multiplier` | 调谐阵列 | 否 | 干涉仪可读 | 无 | 高 | 同一 id 可支持多目标 |
| `frequency_bus` | 频率总线 | block | 调谐晶片 + 红石 + 导波晶体 | 传递 InfoSignal | 无 | `channel`,`connected_nodes`,`packet_buffer` | 红石线 | `frequency_bus`,`InfoSignal` 路由 | 探针台、红石模块、信息中心 | 结构模块 | 可承载传感器数据 | 限频/带宽 | 中 | 初版只做相邻网络 |
| `frequency_to_redstone_module` | 频率转红石模块 | block | 信息单元 + 调谐晶片 + 比较器 | 将 InfoSignal 映射到 0-15 | `mapping_mode` 可选 | `last_signal`,`redstone_output` | 比较器、红石 | `InfoSignal.value -> redstone` | 频率总线 | 否 | S1 输出器 | 20 tick 更新 | 中 | 支持 scalar/int/bool 三类即可 |
| `crystal_interferometer` | 晶体干涉仪 | machine | 玻璃 + 偏振晶体 + 铁 | 晶体属性分析台 | 无 | `target_slot`,`last_report` | 制图台/讲台 | 读取 `kamaen_crystal_state` | 所有晶体、晶片 | 否 | S0 晶体分析 | 无 | 低 | GUI/tooltip 重点设备 |
| `spectrum_phaselocker` | 频谱锁相器 | machine | 调谐晶片 + 金 + 红石 | 读取样本并写入晶体 | 无 | `target_slot`,`sample_slot`,`energy`,`progress` | 无 | `spectrum_tuning`,`target_spectrum` | 频谱样本、共振晶体 | 否 | S1 频谱采样 | 多 tick 配方 | 中 | 可作为调谐阵列子模块 |
| `kamaen_probe_station` | 卡玛恩探针台 | machine/sensor | 铁 + 比较器 + 调谐晶片 | 把可读世界状态转 InfoSignal | 无 | `target_pos`,`adapter_type`,`cooldown`,`last_signal` | 比较器、容器 | `IKamaenReadable`,`InfoSignal` | 信息单元、频率总线 | 否 | S1 方块/红石/能力读取 | 20 tick 冷却 | 中 | P0 只读 BlockState 和红石 |
| `tuning_array` | 调谐阵列 | multiblock_controller | 中心晶体 + 样本/透镜/能源节点 | 提高锁相和共振效率 | 无 | `total_resonance`,`symmetry_score`,`energy_buffer` | 信标式摆放 | `frequency_lock`,`resonance_efficiency` | 锁相器、共振晶体 | 控制器 | 可读阵列状态 | 缓存画像 | 高 | P1，避免阶段三过载 |

## 6. 阶段四：掺杂晶片与 EDA 基础工艺

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kamaen_crystal_t2` | 二代卡玛恩晶体 | item | 稳谱晶体 + 精密精炼 | 允许掺杂、导波、阈值和相位控制的晶体 | `kamaen_crystal_state` 扩展掺杂字段 | 无 | 无 | `doping`,`lithography`,`optical_assembly` | 晶片、PN 结、导波片、相位片 | 否 | 干涉仪可读 | 无 | 中 | 可由稳谱晶体设置 component 升级 |
| `kamaen_dopant` | 卡玛恩掺杂剂 | item | 频谱粉末 + 滤渣 + 化学处理 | 合并施主/受主掺杂剂 | `dopant_type`,`carrier_density`,`purity` | 无 | 红石、石英、金属粉 | `doping_type=donor/acceptor` | 晶片、离子注入器 | 否 | 无 | 无 | 中 | 替代 donor/acceptor 两 id |
| `kamaen_wafer` | 卡玛恩晶片 | item | 稳谱晶体切片；注入后变体 | 合并 blank/N/P/defect 晶片 | `wafer_type`,`doping_type`,`doping_concentration`,`thickness`,`defect_density` | 无 | 无 | `doping`,`lithography`,`hardware_assembly` | PN 结、晶体管 | 否 | 干涉仪/诊断可读 | 无 | 高 | 阶段四最重要数据物品 |
| `kamaen_pn_junction` | 卡玛恩 PN 结 | component_item | N 型晶片 + P 型晶片 + 退火 | 二极管/晶体管前置 | `junction_barrier`,`threshold_voltage`,`junction_quality` | 无 | 红石二极管认知 | `doping`,`threshold_gate` | 晶体管、二极管模式 | 否 | 诊断可读 | 无 | 中 | 二极管可作为晶体管 `device_type=diode` |
| `electronic_logic_gate` | 电逻辑门片 | component_item | PN 结 + 光刻 + 刻蚀 | EDA 电逻辑基础元件，用于早期接口、桥接、低速控制和电存储 | `gate_type`,`bit_width`,`switching_loss`,`gain`,`noise_index`,`thermal_factor` | 无 | 红石逻辑、比较器 | `eda_electronic`,`control_ops`,`io_ops` | 电寄存器、电 SRAM、桥接控制器、封装芯片 | 否 | 诊断可读 | 无 | 中 | 不作为第 6 阶段主计算路线；只在 `die_domain=electronic` 裸片中承担主逻辑 |
| `lithography_mask` | 光刻掩膜 | item | 玻璃板 + 铁板 + 刻写 | 定义曝光图案 | `exposure_pattern`,`circuit_layout`,`mask_durability` | 无 | 旗帜图案/模板 | `lithography`,`etch_depth` | 光刻投影器 | 否 | 无 | 无 | 高 | 图案初版使用枚举，不做像素编辑 |
| `lithography_mask_set` | 分层光刻掩膜组 | data_item | 芯片蓝图台导出合格版图 | 保存 active/metal/optical/via/cooling/shield 等多层掩膜 | `layer_masks`,`alignment_marks`,`mask_quality`,`durability`,`source_blueprint_id` | 无 | 锻造模板/旗帜图案 | `lithography`,`chip_layout`,`wafer_process` | 光刻投影器、流片任务 | 否 | 无 | 无 | 高 | 允许同一设计批量流片；掩膜磨损会降低良率 |
| `process_protection_kit` | 工艺防护套件 | component_item | 绝缘材料 + 稳谱晶体粉 + 金属薄片 | 抽象表示 ESD、防尘、防火/绝缘、封装应力释放等工艺防护 | `protection_types`,`cleanliness_bonus`,`reliability_bonus`,`thermal_penalty` | 无 | 玻璃、铜、避雷针、防火材料 | `yield_score`,`process_reliability`,`packaging` | 微结构单元、封装台、流片任务 | 否 | 诊断可读 | 无 | 中 | 不让玩家手动做复杂电学；作为隐含参数提高良率和可靠性 |
| `timing_structure_cell` | 时序结构单元 | component_item/data_item | 晶振 + 缓存片 + 互连/波导元件 | 在 EDA 版图中提供 T0-T5 时序能力 | `timing_type`,`timing_tier`,`timing_precision`,`latency_budget`,`jitter_margin`,`sync_domain_id` | 无 | 红石中继器/比较器认知 | `timing_budget`,`sync_domain`,`pipeline`,`refresh_window` | 芯片蓝图台、光RAM、频率桥、锁相器 | 否 | 诊断可读 | 无 | 高 | 示例：采样窗口门、同步 FIFO、流水锁存、相位 epoch 标记、刷新调度器、观测窗口门 |
| `crystal_interconnect` | 晶体互连线 | item | 金 + 掺杂晶片碎片 | 封装芯片、板级互连和桥接同步材料 | `line_density`,`sync_delay`,`frequency_tier_limit`,`environment_domain` | 无 | 红石、金 | `sync_bandwidth`,`route_ops`,`bridge_latency` | 逻辑芯片、存储页、晶振、桥接器 | 否 | 无 | 无 | 中 | 方块线缆后移，先物品；跨介质通信必须走桥接端口 |
| `kamaen_oscillator` | 卡玛恩晶振 | item | 石英/稳谱晶体 + 红石，逐级升级 | 统一 F1/F2/F3/F4/F5，同步 EDA 芯片和板级域 | `frequency_tier`,`sync_domain`,`bandwidth` | 无 | 石英、红石 | `frequency_tier`,`hardware_assembly`,`eda_sync_domain` | 封装芯片、主板、光背板、频率桥 | 否 | 诊断可读 | 无 | 中 | `frequency_tier=1..5` |
| `coherent_energy_buffer` | 相干能缓存 | block/item | FE + 稳谱晶体 + 稳压器 | 低噪工艺能源存储 | 若物品化：`coherent_energy`,`noise_floor` | 方块态：`energy`,`noise_floor`,`lock_phase` | FE 能源 | `coherent_energy`,`thermal_budget` | 稳压器、II/III 框架 | 否 | 能量读数 | tick 能源接口 | 中 | 合并低噪 FE 缓存 |
| `coherent_energy_regulator` | 相干能稳压器 | machine | FE 缓存 + 调谐晶片 + 稳谱晶体 | FE -> 相干能 | 无 | `fe_input`,`coherent_output`,`regulation_quality` | FE | `coherent_energy_rate`,`noise_floor` | 相干能缓存 | 否 | 能量/噪声读数 | 20 tick 转换 | 中 | 阶段四后高频使用 |
| `ion_implanter` | 离子注入器 | machine | 铁块 + 稳谱晶体 + 红石 | 给晶片写掺杂参数 | 无 | `doping_axis`,`concentration`,`energy`,`progress` | 无 | `doping` 配方 | 掺杂剂、晶片 | 否 | S1 掺杂读数可选 | 多 tick 配方 | 高 | 初版只开放 X 轴 |
| `lattice_annealing_furnace` | 晶格退火炉 | machine | 熔炉升级 + 稳谱晶体 | 降低缺陷、形成 PN 结 | 无 | `temperature_curve`,`defect_repair`,`progress` | 熔炉/高炉 | `annealing`,`defect_density` | 晶片、PN 结 | 否 | 温度读数 | 熔炉式 tick | 中 | 可复用 furnace 菜单 |
| `lithography_projector` | 光刻投影器 | machine | 玻璃 + F2 晶振 + 调谐晶片 | 曝光图案到 PN 结/晶片 | 无 | `alignment_precision`,`mask_slot`,`exposure_progress` | 无 | `lithography`,`exposure_pattern` | 光刻掩膜、刻蚀槽 | 否 | 对准读数 | 多 tick 配方 | 高 | 高复杂但阶段四核心 |
| `etching_tank` | 刻蚀槽 | machine | 桶/炼药锅 + 化学流体 + 晶体 | 按图案移除材料 | 无 | `etch_depth`,`fluid_tank`,`pattern_fidelity`,`progress` | 炼药锅、流体 | `lithography`,`interconnect` | 光刻投影器、晶体管 | 否 | 液位/刻蚀读数 | 多 tick 配方 | 中 | 化学流体可后移，用物品酸剂起步 |
| `tier2_optical_process_framework` | II 型光路工艺框架 | multiblock_controller | 注入器/退火/光刻/刻蚀/耦合模块组合 | 掺杂、光刻、导波、阈值、相位和探测结工艺集中控制 | 无 | `FrameworkProfile(tier=2)`,`doping_profile`,`waveguide_loss`,`phase_precision`,`running_process` | 多方块 | `framework_process`,`doping_axis`,`etch_depth`,`optical_assembly` | 阶段四机器套件、光路元件 | 控制器 | S2 掺杂/对准/导波损耗 | 缓存画像 | 高 | P1，先让独立机器跑通；旧“电气合成框架”命名弃用 |
| `hardware_diagnostic_station` | 硬件诊断台 | machine/sensor | 电逻辑门片 + F2 晶振 + 显示件 | 输出 EDA 芯片、封装、主板/背板和环境域性能画像 | 无 | `last_profile`,`target_slot`,`bottleneck_report`,`environment_report` | 无 | `control_ops`,`route_ops`,`matrix_ops`,`sampling_ops`,`frequency_tier`,`environment_fit` | EDA 元件、封装芯片、主板/光背板/低温载板 | 否 | S1 硬件诊断 | 低频计算 | 中 | v0.7 前先固定报告模板；必须显示桥接、冷却、相干和隔离瓶颈 |

## 7. 阶段五：EDA 芯片封装、板级集成与宏观信息中心

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `electronic_control_chip` | 电控接口芯片 | component_item/block | 电逻辑门片 + F1/F2 晶振 + 互连线 | 早期接口、传感器汇聚、桥接控制和低速路由预算 | `control_score`,`route_score`,`io_score`,`frequency_tier`,`die_domain=electronic` | 若方块：`task_queue`,`thermal_state` | 无 | `eda_electronic`,`control_ops`,`io_ops` | 主板、诊断台、信息中心、桥接器 | 否 | 诊断可读 | 任务预算 | 中 | 替代旧 `basic_cpu_module` 当前职责；第 6 阶段计算域由 `photonic_control_core` 接管 |
| `electronic_matrix_tile` | 电矩阵瓦片 | component_item/block | 电逻辑门片阵列 + F3 晶振 + 内存页 | 可选早期/兼容密集矩阵元件，不作为中游主线 | `matrix_ops`,`elementwise_ops`,`vram_pages`,`operator_match`,`die_domain=electronic` | 若方块：`active_task`,`utilization`,`thermal_state` | 无 | `matrix_ops`,`operator_match`,`eda_electronic` | 模型系统、封装芯片、桥接器 | 否 | 诊断可读 | 任务预算 + 散热 | 中 | 旧 `electric_gpu_unit` 改名定位；第 6 阶段主线被 `photonic_gpu_unit` 取代 |
| `electronic_activation_tile` | 电激活瓦片 | component_item/block | 电逻辑门片阵列 + F3 晶振 + 内存页 | 可选早期/兼容稀疏、量化、激活算子元件 | `sparse_ops`,`quant_ops`,`special_act_ops`,`die_domain=electronic` | 若方块：`active_task`,`utilization`,`thermal_state` | 无 | `sparse_ops`,`quant_ops`,`eda_electronic` | 模型系统、光脉冲处理器桥接 | 否 | 诊断可读 | 任务预算 + 散热 | 中 | 旧 `electric_npu_unit_placeholder` 改名定位；第 6 阶段主线由 `photonic_pulse_processor` 承担 |
| `memory_page` | 内存页 | data_item | 电逻辑门片 + 互连线 | 统一参数/状态/索引页，属于电/经典存储域 | `kamaen_storage_page`,`page_type`,`storage_domain=electronic` | 无 | 书/地图 | `memory_pages`,`parameter_buffer` | 参数库、数据库、桥接器 | 否 | 诊断可读 | 无 | 中 | 合并参数页/状态页；光RAM 和波函数缓存页另属光/量子存储域 |
| `eda_module_plate` | EDA 模块片 | component_item | 对应逻辑门/光学元件/低温元件 + 光刻掩膜 + 互连线 | ALU、寄存器、MZI、双稳态腔、I/O、桥接等芯片模块的制造单元 | `module_type`,`die_domain`,`logic_family`,`bit_width`,`quality`,`thermal_factor`,`coherence_factor` | 无 | 红石逻辑 | `chip_design`,`control_ops`,`route_ops`,`matrix_ops`,`sampling_ops` | 芯片蓝图、封装芯片 | 否 | 诊断可读 | 无 | 高 | `module_type=alu/register/cache/mac/io/route/memory/fiber/clock/mzi/bistable/bridge/q_measure` |
| `chip_blueprint_writer` | 芯片蓝图台 | machine/block | 光刻投影器 + 诊断台 + F2 晶振 | 编辑 EDA 原理图、微结构版图、分级时序、端口、冷却、相干和桥接要求 | 无 | `editing_blueprint`,`active_layer`,`selected_tool`,`validation_errors`,`drc_report`,`timing_report`,`simulation_report`,`score_preview`,`environment_preview` | 制图台/锻造台 | `chip_logic_blueprint`,`chip_design`,`eda_domain_rules`,`chip_layout`,`timing_budget` | EDA 模块片、微结构单元、时序结构单元、分层掩膜组、封装台 | 否 | 蓝图诊断 | 手动编辑 | 高 | 类微电子设计软件：元件库、层面板、画线、T0-T5 时序路径、DRC、热图；F 级决定频率，T 级决定信息节拍 |
| `chip_packaging_station` | 芯片封装台 | machine/block | 退火炉 + 互连线 + 封装材料 | 将芯片蓝图和 EDA 模块封装成可上主板/光背板/低温载板芯片 | 无 | `package_type`,`port_mapping`,`thermal_test`,`coherence_test`,`yield_report` | 锻造台 | `chip_package_profile`,`hardware_assembly`,`eda_environment_domains` | 主板蓝图、封装芯片、桥接器 | 否 | 封装诊断 | 多 tick 任务 | 高 | 端口分布、封装类型、冷却口和相干接口影响兼容 |
| `packaged_logic_chip` | 封装逻辑芯片 | component_item | 芯片封装台产出 | 电/光/量子/存储/桥接芯片实体 | `chip_logic_blueprint`,`chip_package_profile` | 无 | 无 | `control_ops`,`io_bandwidth`,`route_ops`,`matrix_ops`,`sampling_ops`,`thermal_budget`,`coherence_budget` | 主板、光背板、低温载板、交换机、基站 | 否 | 诊断可读 | 无 | 高 | 芯片质量影响性能、发热、相干消耗和环境匹配 |
| `motherboard_blueprint` | 集成板蓝图 | data_item | 蓝图台 + 晶振样本 + 互连线 | 保存电主板、光背板、低温载板或混合集成节点布局 | `hardware_blueprint(blueprint_type=motherboard/optical_backplane/cryogenic_carrier/mixed_compute_node)` | 无 | 地图/锻造模板 | `motherboard_layout`,`hardware_assembly`,`eda_environment_domains` | 可配置主板、光背板、低温载板、诊断台 | 否 | 诊断可读 | 无 | 高 | 5x5/7x7/9x9 格点，P0 可从预设模板起步 |
| `configurable_motherboard` | 可配置集成板 | machine/block | 集成板蓝图 + 互连/波导/冷却材料 + 晶振 | 承载电控、光逻辑、存储、桥接或低温芯片并输出硬件画像 | `hardware_blueprint`,`network_port_profile` | `installed_modules`,`port_map`,`bus_profile`,`thermal_state`,`coherence_state`,`environment_domains`,`power_state` | 工作台/讲台式装配认知 | `control_ops`,`io_bandwidth`,`sync_bandwidth`,`hardware_profile`,`environment_fit` | 封装芯片、接口芯片、光背板、低温载板 | 否/机柜附属 | 硬件诊断 | 结构变化或手动刷新 | 高 | 板级自由度核心；不同环境域必须由桥接器连接 |
| `network_interface_chip` | 网络接口芯片 | component_item | 晶体管 + 光纤/无线材料 + F2/F4 晶振 | 给主板提供光纤、无线、传感器或交换端口 | `chip_mode`,`port_count`,`protocol`,`frequency_tier`,`bandwidth` | 无 | 网卡认知 | `fiber_port`,`wireless_port`,`sensor_port`,`route_ops` | 主板、交换机、传感器汇聚器 | 否 | 诊断可读 | 无 | 高 | `chip_mode=fiber/wireless/sensor/switch/security` |
| `fiber_switch` | 光纤交换机 | machine/block | 接口芯片 + 光纤 + 电控接口芯片 + F4 晶振 | 多端口高速光纤转发、参数同步和集群组网 | `network_port_profile` | `route_table`,`packet_buffer`,`port_status`,`switch_bandwidth` | 无 | `fiber_cluster`,`parameter_sync`,`route_ops` | 主板/光背板、光纤、网络中心 | 否/机柜附属 | 网络诊断 | 包预算/低频统计 | 高 | 端口数和交换背板带宽分开评分 |
| `sensor_hub` | 传感器汇聚器 | machine/block | 探针 + 缓存页 + F2 晶振 | 汇聚多传感器、时间戳对齐、缓存并批量上传 | `network_port_profile` | `sensor_registry`,`sample_buffer`,`alignment_window`,`last_batch` | 漏斗/侦测器认知 | `sensor_network`,`timestamp_alignment`,`dataset` | 传感器背板、信息中心、模型输入网关 | 否/附属 | S2/S3 传感网络 | 采样批处理 | 高 | 解决“传感器是否有独立网络”的核心方块 |
| `model_component_gateway` | 模型组件网关 | machine/block | 信息单元 + 频率总线 + 内存页 | 模型组件方块网络的输入/输出端口 | `network_port_profile`,`local_export_ids` | `bound_ports`,`packet_buffer`,`namespace` | 红石中继/漏斗认知 | `model_data_port`,`local_export_remote_id` | 算子方块、参数方块、模型编译器 | 结构模块 | 可读端口状态 | 路由预算 | 高 | 可配置为 input/output/feedback/control |
| `model_compiler` | 模型编译器 | machine/block | 电控接口芯片 + 内存页 + 诊断台 + F3 晶振 | 扫描模型组件方块网络并生成 ExecutableGraph | `hardware_blueprint(blueprint_type=model_graph)` 可选 | `last_graph`,`compile_errors`,`cost_report`,`operator_requirements` | 制图台/讲台 | `ExecutableGraph`,`operator_match`,`model_inner_network` | 模型网关、参数库、光GPU/光脉冲处理器 | 否/控制器 | 编译诊断 | 手动/结构变化编译 | 高 | 不每 tick 扫描；保存后可导出模型物品 |
| `server_rack` | 服务器机柜 | multiblock_controller/block | 可配置主板 + 电源 + 冷却 + 线缆 | 将多块主板封装为稳定算力/存储/交换节点 | `hardware_blueprint(blueprint_type=rack)` 可选 | `installed_boards`,`power_budget`,`cooling_budget`,`cable_quality`,`risk_report` | 无 | `rack_node`,`power_budget`,`thermal_budget`,`cluster_resource` | 主板、交换机、存储中心 | 控制器 | 机柜诊断 | 低频统计 | 高 | 第一版可先单方块机柜，后续多方块 |
| `storage_center_controller` | 存储中心控制器 | multiblock_controller/block | 存储主板 + 内存页 + 储存芯片 + 电源 | 存储传感器数据集、模型快照和参数页 | 无 | `capacity_pages`,`read_bandwidth`,`write_bandwidth`,`index_speed`,`backup_level`,`data_loss_risk` | 书架/箱子 | `dataset_storage`,`model_snapshot`,`parameter_page` | 传感器汇聚器、模型编译器、集群 | 控制器 | 存储诊断 | 写入/备份预算 | 高 | 掉电和过热只做确定性风险 |
| `world_noise_sample` | 世界底噪样本 | data_item | 底噪谱仪 + 稳谱晶体 + F2 | 底噪采样载体 | `noise_sample` | 无 | 维度、天气、群系 | `background_noise_sampling` | 谱片、数据库 | 否 | S2 数据输出 | 采样冷却 | 中 | P0 |
| `thermal_noise_plate` | 热噪声谱片 | data_item | 世界底噪样本过滤 | 热噪层专用材料 | `noise_sample.noise_layer_id=thermal` | 无 | 熔炉、温度认知 | `ThermalNoiseLayer`,`entropy_density` | 底噪数据库、低温腔 | 否 | 无 | 无 | 低 | P0 |
| `radiation_noise_plate` | 背景辐射谱片 | data_item | 世界底噪样本过滤 | 辐射层材料 | `noise_sample.noise_layer_id=radiation` | 无 | 天空/日夜 | `RadiationNoiseLayer` | 霍金采样器 | 否 | 无 | 无 | 低 | P1 |
| `quantum_fluctuation_plate` | 量子涨落片 | data_item | 世界底噪样本过滤 | 量子噪声材料 | `noise_sample.noise_layer_id=quantum`,`coherence_deviation` | 无 | 无 | `QuantumNoiseLayer`,`collapse_risk` | 协处理器、误差校验 | 否 | 无 | 无 | 中 | P1 |
| `chunk_entropy_record` | 区块熵流记录 | data_item | 熵流计读取区块 | 记录区块熵流 | `chunk_pos`,`entropy_flow_rate`,`block_update_count` | 无 | 区块、随机刻 | `entropy_flow`,`BlockUpdateNoiseLayer` | 熵流泵、数据库 | 否 | 数据输出 | 100-200 tick | 中 | 坐标可能需隐藏/压缩 |
| `noise_database` | 底噪数据库 | machine/block | 样本 x16 + 信息核心 | 存储样本、标签、版本 | 可存 `kamaen_storage_page` | `stored_layers`,`capacity`,`index`,`query_cooldown` | 书架/讲台 | `noise_sample`,`interpretation_tags` | 信息中心、谱仪 | 附属/核心 | 可查询传感数据 | 查询预算 | 中 | 不必一开始做远程查询 |
| `macro_info_index_core` | 宏观信息索引核心 | component_item/block | 信息中心控制器 + 探针 + F2 | 信息中心核心组件 | `routes`,`bound_sensors`,`query_latency` 可选 | 若方块：`route_table` | 无 | `frequency_bus`,`hardware_control_node` | 信息中心 | 控制器核心 | S2 路由诊断 | 路由预算 | 高 | 可并入控制器方块 |
| `noise_spectrometer` | 底噪谱仪 | sensor/machine | 稳谱晶体 + F2 晶振 | 采样维度底噪 | 无 | `sample_interval`,`energy`,`last_sample`,`layer_filter` | 天气、群系、维度 | `NoiseLayerSampler` | 天线、数据库 | 否/附属 | S3 底噪层采样 | 同维度缓存 200 tick | 中 | 不开独立线程 |
| `thermodynamic_antenna` | 热力学背景天线 | block/multiblock_module | 导波晶体 + 金属结构 | 扩大谱仪范围 | 无 | 结构方块无 BE；控制器缓存高度 | 避雷针 | `sampling_range`,`dimension_bias` | 底噪谱仪 | 附属 | 增强底噪采样 | 结构变化扫描 | 中 | 1-3 级天线杆 |
| `entropy_flow_meter` | 熵流计 | sensor/machine | 探针 + 稳谱晶体 | 读取区块熵流 | 无 | `target_chunk`,`last_entropy_flow`,`cooldown` | 区块更新 | `entropy_density`,`block_update_noise` | 区块熵流记录 | 否 | S3 熵流采样 | 100-200 tick | 中 | 抽样估算，不遍历全部方块 |
| `info_center_controller` | 信息中心控制器 | multiblock_controller | 电控接口芯片 + 数据库 + 总线 + 探针 | 宏观采样、路由、归档 | 无 | `FrameworkProfile/MachineProfile`,`route_table`,`sensor_registry`,`query_budget` | 多方块控制中枢 | `InfoSignal`,`frequency_bus`,`hardware_profile` | 谱仪、数据库、总线 | 控制器 | S2/S3 传感网络 | 批量路由预算 | 高 | 阶段五只做静态路由；第 6 阶段可接入光控制核扩展 |

## 8. 阶段六：全光计算硬件

本阶段新增。承接第 5 阶段 EDA 蓝图和板级集成，把中游主计算推进到光工艺族。完整设计见 `docs/Kamaen_Info_Optical_Computing_Design.md`；跨工艺隔离与桥接规则见 `docs/Kamaen_Info_Computing_EDA_Design.md`。

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `silicon_photonic_waveguide_blank` | 硅光波导毛坯 | item | 导波晶体 + 掺杂硅 + 光刻精密化 | 第 6 阶段所有光路元件的基础 | `purity`,`waveguide_loss` | 无 | 无 | `optical_assembly` | 光刻投影器（精密化）、刻蚀槽 | 否 | 无 | 无 | 中 | 与电气晶圆并轨工艺，复用第 4 阶段光刻台 |
| `silicon_photonic_waveguide` | 硅光波导 | item | 毛坯 + 反应离子刻蚀 + 退火 | MZI / 光协处理器底层导光介质 | `waveguide_loss`,`mode_confinement`,`length` | 无 | 无 | `optical_assembly` | MZI 调制器、光协处理器 | 否 | 无 | 无 | 中 | P0；长度参数影响光路相干预算 |
| `mzi_modulator` | 马赫-曾德尔调制器 | component_item | 波导 x2 + 50:50 分束 + 相位调谐器 | 光GPU 权重单元 | `phase_bias`,`extinction_ratio`,`switching_speed` | 无 | 无 | `optical_assembly`,`mzi_grid_size` | 光GPU 单元 | 否 | 无 | 无 | 高 | 阶段六核心；相位偏置即"权重" |
| `phase_tuner` | 相位调谐器 | component_item | 热光（微加热条）或电光（载流子注入） | 校准 MZI / 写入光GPU 权重 | `tuning_method=thermal/electro`,`linearity`,`response_time` | 无 | 无 | `coherent_energy_calibration` | MZI 调制器、校准台 | 否 | 无 | 无 | 高 | 两种实现方式可分别走两条工艺路 |
| `silicon_photodetector` | 硅光探测器 | component_item | PN 结 + 增益区 + 锗外延层（APD 高端） | 光GPU 输出端 / 光协处理器光电边界 | `responsivity`,`dark_current`,`bandwidth`,`detector_noise_floor` | 无 | 无 | `optical_assembly` | 光GPU、光协处理器 | 否 | 诊断可读 | 无 | 中 | 第 7 阶段 SNSPD 升级时性能跃迁 |
| `single_freq_laser_source` | 单频激光源 | component_item | 稳谱晶体 + F4 晶振 + 相干能稳压器 | 光路相干基准 + 相干能消耗中心 | `wavelength`,`linewidth`,`output_power`,`coherence_time` | 若方块：`pump_status`,`coherence_energy_drain` | 无 | `coherent_energy`,`F4`,`wavelength_load` | 光GPU、光协处理器、激光泵浦塔 | 否/附属 | 诊断可读 | 持续相干能消耗 | 高 | 第 6 阶段持续消耗相干能的主要节点 |
| `calibration_token` | 光路校准令牌 | item | 频谱锁相器 + 相位调谐器测试合格 | 光路校准消耗品 | `target_grid_size`,`expected_calibration_time` | 无 | 无 | `coherent_energy_calibration` | 光路校准台 | 否 | 无 | 无 | 中 | 每次重新校准消耗一枚；推动玩家避免频繁切换权重 |
| `kamaen_nonlinear_medium` | 卡玛恩非线性介质 | component_item | 导波晶体 + 稳谱晶体 + 应力调谐腔 | 光逻辑门、光脉冲处理器和光RAM 的 χ² 基材 | `chi2_coefficient`,`nonlinear_bandwidth`,`stress_tensor_ref`,`threshold_stability` | 无 | 无 | `optical_assembly`,`kamaen_crystal_state.stress` | 光逻辑门、双稳态晶胞、光脉冲处理器 | 否 | 干涉/阈值诊断可读 | 无 | 高 | 第 2-3 阶段晶体质量在第 6 阶段兑现的关键条目 |
| `photonic_logic_gate` | 光逻辑门 | component_item | 非线性介质 + 波导 + 分束器 | 全光 AND/OR/NOT/NAND/XOR 基元 | `gate_type`,`threshold_stability`,`logic_error_rate`,`response_ticks` | 无 | 红石逻辑认知 | `control_ops`,`logic_error_rate` | 光控制核、双稳态晶胞 | 否 | 诊断可读 | 无 | 高 | 低品级晶体导致概率性位翻转 |
| `kamaen_bistable_cell` | 卡玛恩双稳态晶胞 | component_item | 两个耦合卡玛恩共振腔 + 非线性介质 | 光控制核状态寄存器和光RAM 反射基元 | `bistable_margin`,`hold_power`,`state_life_ticks` | 无 | 红石锁存器认知 | `state_hold_ops`,`bistable_cell_health` | 光控制核、光RAM | 否 | 诊断可读 | 持续相干能消耗 | 高 | 光学 SR 触发器；状态需要泵浦维持 |
| `photonic_control_core` | 光控制核 | component_item/block | 双稳态晶胞 x16 + 光逻辑门 x32 + 波导 x8 + 相位调谐器 x4 + 激光源 x2 + F4 晶振 | 全光 FSM，承担第 6 阶段控制/路由/脚本/调度/IO | `fsm_state_depth`,`logic_error_rate`,`control_ops`,`route_ops`,`script_ops` | 若方块：`active_state`,`task_queue`,`coherent_energy_draw`,`error_retry_count` | 红石控制器认知 | `control_ops`,`route_ops`,`sensor_ops`,`io_ops` | 光协处理器、光GPU、光脉冲处理器、光RAM | 否/机柜附属 | 诊断可读 + FSM 状态可视化 | 任务预算 + 持续相干能 | 高 | 取代第 5 阶段电气 CPU 的计算域职责；电气 CPU 仅作外层接口 |
| `photonic_coprocessor` | 光协处理器 | component_item/block | 光路由交换机 + 单频激光源 + 并行波导 + F4 晶振 | 光控制核调度下的数据搬运/缓存互连加速 | `data_move_ops`,`prep_ops`,`optical_bandwidth`,`route_latency`,`coherent_energy_draw` | 若方块：`active_task`,`route_state` | 无 | `data_move_ops`,`prep_ops`,`coherent_energy` | 光控制核、光GPU、光脉冲处理器、光RAM | 否 | 诊断可读 | 任务预算 + 相干能消耗 | 高 | 第 6 阶段五件套之一；纯光数据通路 |
| `photonic_gpu_unit` | 光GPU 单元 | component_item/block | 硅光波导 x8 + MZI x16 + 相位调谐器 x16 + 探测器 x8 + 单频激光源 x2 + F4 晶振 + 光协处理器接口板 | 密集 GEMM / FFT / 卷积加速 | `photonic_throughput`,`mzi_grid_size`,`weight_switch_cost`,`coherence_dependency`,`coherent_energy_draw` | 若方块：`active_task`,`utilization`,`current_calibration` | 无 | `matmul_ops`,`conv_ops`,`fft_ops`,`coherent_energy` | 模型系统、光控制核、光协处理器、光脉冲处理器 | 否 | 诊断可读 + S2 干涉条纹快照 | 任务预算 + 相干能消耗 | 高 | 取代 `electric_gpu_unit`；权重 = 相位偏置；切换需校准 |
| `photonic_pulse_processor` | 光脉冲处理器 | component_item/block | 非线性介质 x8 + 波导 x8 + 相位调谐器 x4 + 激光源 x2 + F3 晶振 | 稀疏激活、非线性算子、低精度时分信号处理 | `sparse_ops`,`nonlinear_ops`,`pulse_ops`,`quant_ops`,`pulse_threshold_drift` | 若方块：`active_task`,`threshold_state`,`utilization` | 无 | `sparse_ops`,`nonlinear_ops`,`quant_ops` | 模型系统、光GPU、光协处理器 | 否 | 诊断可读 + 湮灭可视化 | 任务预算 + 相干能消耗 | 高 | 取代 `electric_npu_unit_placeholder`；与光GPU 互补 |
| `photonic_ram_unit` | 光RAM 单元 | component_item/block | 双稳态晶胞 x4 + 波导 x4 + 非线性介质 x2 + 激光源 + F2 晶振 | 短时状态存储、激活缓存和状态寄存器 | `ram_coherence_life`,`loop_count`,`read_decay_rate`,`refresh_cost` | 若方块：`stored_state`,`remaining_life`,`refresh_timer`,`read_count` | 红石锁存/缓存认知 | `state_hold_ops`,`ram_coherence_life` | 光控制核、光GPU、光脉冲处理器 | 否 | 诊断可读 + 衰减可视化 | 20-80 tick 寿命 + 刷新预算 | 高 | 第 6 阶段短时光存储；第 10 阶段长期光存储另作升级 |
| `coherent_energy` | 相干能（资源） | resource | 单频激光源持续产生 | 维持光路相干的能量预算（独立资源条，非 FE 子类） | 资源量 + 衰减率 | 在 BlockEntity capability 中 | 无 | `coherent_energy`,`logic_cost × gate_count + matrix_cost × mzi_count` | 单频激光源、光控制核、光GPU、光脉冲处理器、光RAM、光路校准台 | 否 | 资源条 + 警告 | 持续 tick | 中 | 失稳阈值：< 70% 逻辑错误上升，< 30% 光路崩溃 |
| `photonic_waveguide_etching_station` | 波导刻蚀台 | machine | 光刻投影器（精密化）+ 反应离子刻蚀模块 + 退火 | 制造硅光波导 | 无 | `lithography_alignment`,`etch_progress`,`anneal_temp` | 无 | `optical_assembly` | 波导毛坯、波导 | 否 | 工艺读数 | 多 tick 配方 | 高 | 第 4 阶段光刻台升级配方 |
| `mzi_weaving_station` | MZI 编织台 | machine | 波导组装 + 调谐器对齐 + 分束器精装 | 把波导和调制器组装为 N×N 网格 | 无 | `current_grid_size`,`alignment_quality`,`progress` | 无 | `optical_assembly`,`mzi_grid_size` | 光GPU | 否 | 工艺读数 | 多 tick 配方 | 高 | 拓扑选择：Reck 三角 / Clements 矩形 |
| `laser_pump_tower` | 激光泵浦塔 | multiblock | 稳谱晶体 + F4 晶振 + 相干能稳压器 + 泵浦腔 | 集中产生相干能 + 单频激光源 | 无 | `pump_status`,`coherent_energy_output`,`thermal_state` | 无 | `coherent_energy`,`F4`,`wavelength_load` | 单频激光源、光GPU、光协处理器 | 控制器 | 诊断可读 | 持续 tick | 高 | 第 6 阶段地标多方块；高负载需主动冷却 |
| `photonic_calibration_station` | 光路校准台 | machine | 相位调谐器扫描 + 干涉测量装置 + F4 晶振 | 重新写入光GPU 权重 | 无 | `calibrating_target`,`progress`,`tokens_consumed` | 无 | `coherent_energy_calibration` | 光GPU、校准令牌 | 否 | 校准诊断 | 60 秒/次 | 高 | 消耗校准令牌；失稳后强制使用 |

## 9. 阶段七：凝聚态材料与费曼过程

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `quasiparticle_lattice` | 准粒子晶格 | item | 底噪样本 + 晶体 + 低温凝聚腔 | 凝聚态基础材料 | `quasiparticle_type`,`lattice_spacing`,`energy_gap` | 无 | 无 | `condensed_matter_synthesis` | 传播子片 | 否 | 可被捕获器读取 | 无 | 中 | 响应测试输出 |
| `propagator_plate` | 传播子片 | data_item | 准粒子捕获器捕获 | 合并声子/电子/激子/自旋波 | `propagator_type`,`momentum_vector`,`lifetime`,`charge`,`spin` | 无 | 无 | `feynman_process.external_lines` | 顶点片、蓝图 | 否 | 数据输出 | 捕获冷却 | 高 | `propagator_type` 枚举 |
| `cooper_pair_seed` | 库珀对种子 | item | 电子传播子 x2 + 低温场 | 超导环前置 | `pairing_gap`,`critical_temperature` | 无 | 无 | `superconductivity`,`coherence` | 超导卡玛恩环 | 否 | 无 | 无 | 中 | 完整超导流程可后移 |
| `feynman_vertex_plate` | 费曼顶点片 | data_item | 传播子 + 相互作用条件 | 描述相互作用顶点 | `vertex_type`,`in_lines`,`out_lines`,`coupling_constant` | 无 | 无 | `feynman_process.vertices` | 传播子片、编译台 | 否 | 无 | 无 | 高 | 顶点类型先少量枚举 |
| `feynman_process_blueprint` | 费曼过程蓝图 | data_item | 编译台组合外线/顶点/约束 | 凝聚态配方核心 | `feynman_blueprint` | 无 | 锻造模板 | `feynman_process`,`quantum_optical_coprocessing` | III 型框架、协处理器 | 否 | 蓝图校验 | 编译冷却 | 高 | 不模拟真实量子场 |
| `superconducting_kamaen_ring` | 超导卡玛恩环 | item/block | 库珀对 + 低温场 + III 型框架 | 量子/视界/线圈核心材料 | `critical_current`,`flux_quantum`,`coherence_length` | 若方块：`current_flux` | 无 | `coherence_budget`,`horizon_constraint` | 拓扑晶体、协处理器 | 结构模块 | 可被相干传感器读 | 无 | 中 | 阶段七标志性产物 |
| `topological_insulator_crystal` | 拓扑绝缘晶体 | item | 自旋波过程 + 拓扑相变炉 | 拓扑材料和边界态 | `topology_id`,`edge_state_count`,`bulk_gap` | 无 | 无 | `topology_id`,`tunnel_link` | 超导环、隧穿链路 | 否 | 可读拓扑 id | 无 | 高 | P1 |
| `phase_change_memory_crystal` | 相变记忆晶体 | item | 拓扑晶体 + 激子过程 | 高级存储/状态材料 | `phase_state`,`readout_voltage`,`endurance` | 无 | 红石锁存器认知 | `state_page`,`memory_pages` | 内存页、全息数据片 | 否 | 状态读数 | 无 | 中 | 可作为后续存储升级 |
| `quasiparticle_filter` | 准粒子滤波器 | block/item | 传播子 + 拓扑晶体 | 过滤传播子/底噪 | `pass_band`,`stop_band`,`filter_q_factor` | 若方块：`current_band` | 无 | `noise_shielding`,`observation_strength` | III 型框架、全息膜 | 结构模块 | S2/S3 过滤读数 | 低频更新 | 高 | P2 |
| `tunnel_linker` | 隧穿链路器 | block/machine | 传播子 + 拓扑晶体 + III 型框架 | 合并隧穿串联器/4D 电路桥 | `tunneling_frequency`,`topology_id`,`linked_nodes` 可选 item 配对 | `pair_id`,`linked_pos`,`coherent_distance` | 远程红石认知 | `tunnel_frequency`,`logical_adjacency` | 4D 电路、视界约束 | 结构模块 | S3 链路稳定 | 20 tick 同步 | 高 | 维度级注册表处理跨 chunk |
| `cryo_condensation_chamber` | 低温凝聚腔 | multiblock_controller | 密封腔 + 冷却 + 相干能 | 低温和相干保持 | 无 | `temperature`,`coolant`,`coherence_field`,`cached_profile` | 冰、蓝冰、雪 | `temperature`,`coherent_energy_rate` | 捕获器、超导环 | 控制器 | S3 温度/相干 | 20 tick 热预算 | 高 | 不做真实热传导 |
| `quasiparticle_detector` | 准粒子捕获器 | sensor/machine | 低温腔升级 | 捕获传播子片 | 无 | `excitation_mode`,`resolution`,`last_trace` | 无 | `propagator_type`,`noise_layer` | 传播子片、低温腔 | 附属 | S3 准粒子 | 捕获任务冷却 | 高 | 先做电子/声子两模式 |
| `feynman_compiler` | 费曼过程编译台 | machine | 调谐台升级 | 外线/顶点/约束 -> 蓝图 | 无 | `slots`,`validation_errors`,`progress` | 锻造台 | `feynman_process` | 传播子片、顶点片 | 否 | 蓝图校验 | 编译冷却 | 高 | GUI 类似扩展锻造台 |
| `topology_furnace` | 拓扑相变炉 | machine/multiblock | 退火炉升级 + 场线圈 | 制造拓扑材料 | 无 | `field_strength`,`quench_rate`,`phase_progress` | 高炉 | `topological_phase`,`cooling_rate` | 拓扑晶体 | 附属/控制器 | S2 相变读数 | 多 tick 配方 | 高 | 可先做单方块 |
| `horizon_framework_mk1` | III 型视界框架雏形 | multiblock_controller | 低温、捕获、拓扑、相干模块 | 凝聚态用 III 型框架，不产生视界 | 无 | `FrameworkProfile(tier=3_mk1)`,`noise_shielding`,`coherence_budget` | 多方块 | `framework_process`,`condensed_matter_synthesis` | 阶段七/八/九共用 | 控制器 | S3 框架传感 | 缓存画像 | 高 | 先做雏形，阶段九再完整视界 |

## 10. 阶段八：量子光学协处理器与中观合成

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `quantum_optical_coprocessor_core` | 量子光学协处理核心（原 `quantum_coprocessor_core`） | component_item | 超导环 + 拓扑晶体 + 单光子源 + F4 晶振 | 协处理器核心；物理路线为单光子玻色采样 | `qubit_count`,`coherence_time`,`gate_fidelity` | 无 | 无 | `quantum_optical_coprocessing` | 低温控制片、误差校验、SNSPD | 否 | 诊断可读 | 无 | 高 | 不等于通用计算机 |
| `cryo_control_plate` | 低温控制片 | component_item | 低温腔 + 稳谱晶体 + 刻蚀 | 低温控制模块 | `target_temperature`,`stability`,`power_draw` | 无 | 无 | `temperature`,`thermal_budget` | 低温控制柜 | 否 | 无 | 无 | 中 | 协处理器必需 |
| `coherent_control_line` | 相干控制线 | block/item | 超导环 + 互连线 | 相位控制和低损耗连接 | `signal_attenuation`,`phase_drift` | 若方块：`current_phase` | 红石线 | `coherence_budget`,`sync_bandwidth` | 协处理器、调度器 | 结构模块 | 相位读数可选 | 低频 | 高 | 可先物品化为合成材料 |
| `entanglement_coupler_plate` | 纠缠耦合片 | component_item | 拓扑晶体 + 传播子 + III 框架 | 协处理器高级模块 | `entanglement_fidelity`,`bell_pair_count` | 无 | 无 | `qubit_count`,`error_rate` | 误差校验阵列 | 否 | 诊断可读 | 无 | 高 | P1 |
| `wavefunction_cache_page` | 波函数缓存页 | data_item | 内存页 + 量子涨落片 + 低温控制 | 缓存抽象波函数状态 | `kamaen_storage_page`,`collapse_risk`,`cache_valid_ticks` | 无 | 书与笔 | `quantum_coprocessing`,`state_page` | 采样仪、协处理器 | 否 | 数据输出 | 任务结束写入 | 高 | 只保存摘要，不保存真实波函数 |
| `quantum_error_correction_plate` | 量子误差校验片 | component_item | 量子涨落片 + 稳谱晶体 + 超导环 | 降低协处理任务错误 | `code_distance`,`syndrome_rate`,`logical_error_rate` | 无 | 无 | `error_correction`,`coherence_time` | 误差校验阵列 | 结构模块 | 诊断可读 | 无 | 高 | 阵列数量影响评分 |
| `quasiparticle_path_sample` | 准粒子路径样本 | data_item | 捕获器连续监控蓝图过程 | 高级模型训练/隐藏过程发现 | `path_trajectory`,`transition_probability`,`dominant_channel` | 无 | 无 | `dataset`,`feynman_process` | 模型系统、协处理器 | 否 | S3 数据输出 | 低频采样 | 高 | 主线不强制 |
| `synthesis_parameter_curve` | 合成参数曲线 | data_item | 量子光学协处理器任务输出 | III 型框架参数曲线 | `synthesis_parameter_curve` | 无 | 唱片/地图数据 | `framework_control_port`,`quantum_optical_coprocessing` | 调度器、III 型框架 | 否 | 数据输出 | 100-400 tick 任务 | 高 | 阶段八核心产物 |
| `meso_synthesis_protocol` | 中观合成协议 | data_item | 曲线 + III 框架 + 信息中心封装 | 参数曲线和传感回读端口打包 | `curve_ref`,`actuator_commands`,`sensor_readback_ports` | 无 | 无 | `dynamic_control_ports` | 调度器、信息中心 | 否 | 无 | 无 | 高 | P2，可由曲线直接替代 |
| `quantum_optical_coprocessor` | 量子光学协处理器（原 `quantum_coprocessor`） | multiblock_controller | 核心 + 低温 + 误差校验 + SNSPD x4 + 单光子源 | 蓝图和材料状态 -> 曲线；物理路线：单光子 + 线性光路 + 后选择测量（玻色采样） | 无 | `submitted_task`,`physical_qubits`,`noise_profile`,`cooldown`,`progress_step` | 无 | `quantum_optical_coprocessing`,`synthesis_parameter_curve` | 控制柜、采样仪、阵列、单光子源、SNSPD | 控制器 | S3/S4 协处理诊断 | 分步任务，不开线程 | 高 | 每 10-20 tick 抽象一步 |
| `cryo_control_cabinet` | 低温控制柜 | machine | 低温控制片 + 相干能 | 给协处理器供低温 | 无 | `target_temperature`,`actual_temperature`,`power_draw` | 冰/蓝冰 | `thermal_budget`,`error_rate` | 协处理器 | 附属 | S3 温度反馈 | 20 tick 更新 | 中 | 温度波动影响错误率 |
| `wavefunction_sampler` | 波函数采样仪 | sensor/machine | 协处理器附属 | 读取坍缩风险 | 无 | `collapse_risk`,`sampling_strength`,`last_snapshot` | 无 | `observation_strength`,`collapse_risk` | 缓存页、调度器 | 附属 | S4 波函数摘要 | 20 tick | 高 | 不做真实量子态 |
| `error_correction_array` | 误差校验阵列 | multiblock_module | 误差校验片重复摆放 | 提高逻辑稳定性 | 无 | 控制器缓存 `code_distance`,`overhead` | 多方块重复结构 | `logical_error_rate`,`physical_qubits` | 协处理器 | 结构模块 | 诊断可读 | 结构变化扫描 | 高 | 方块数量/距离映射编码距离 |
| `meso_synthesis_scheduler` | 中观合成调度器 | machine | 信息中心升级 + CPU + 曲线接口 | 曲线分发到框架控制端口 | 无 | `active_curve`,`channel_map`,`dispatch_progress` | 无 | `dynamic_control_ports`,`model_output` | III 型框架、信息中心 | 附属/中枢 | S3 控制回读 | 逐段分发 | 高 | 可作为信息中心扩展模块 |

## 11. 阶段九：戈古尔斯弦与人造视界

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gorguth_string_residue` | 戈古尔斯弦残迹 | item | 虚空残响 + 底噪数据库 + 稳谱晶体 | 人造视界前置奇异材料 | `frequency_signature`,`decay_rate`,`anchor_potential` | 无 | 末地/虚空 | `StringResidueLayer`,`boundary_condition` | 戈古尔斯弦 | 否 | 底噪可读 | 无 | 高 | 阶段五可先占位 |
| `gorguth_string` | 戈古尔斯弦 | item | 残迹 + 弦锚定器 + 相干能 | 视界边界锚点 | `stability`,`tension`,`boundary_coupling`,`decay_suppressed` | 无 | 无 | `string_anchor_stability`,`horizon_framework` | 弦锚定器、视界核心 | 否 | 弦稳定度读数 | 衰减/稳定预算 | 高 | 需要稳定化，不是普通材料 |
| `horizon_constraint_plate` | 视界约束片 | component_item/block | 超导环 + 拓扑晶体 + 隧穿链路 | 视界约束环材料 | `closure_rating`,`thermal_tolerance`,`field_leak_rate` | 若方块：`leak_rate` | 黑曜石、哭泣黑曜石 | `horizon_constraint`,`field_closure` | 约束环、视界核心 | 结构模块 | S4 泄漏读数 | 每 tick 少量参数 | 高 | 方块状态可带环方向 |
| `entropy_pump` | 熵流泵 | machine/block | 约束片 + 相干能 + III 框架 | 定向抽取/排放熵流 | 无 | `extraction_rate`,`direction_vector`,`backflow_ratio`,`energy` | 无 | `entropy_extraction`,`entropy_flow` | 视界、黑洞、维度维护 | 附属 | S4 熵流 | 每 tick 参数 | 高 | 跨阶段复用 |
| `holographic_membrane` | 全息信息膜 | component_item/block | 膜刻写器 + 约束片 + 滤波器 | 视界存储介质 | `write_resolution`,`capacity_pages`,`readout_fidelity` | 若方块：`stored_pages`,`write_progress` | 末影箱认知 | `holographic_storage`,`horizon_information` | 膜刻写器、数据片 | 结构模块 | 完整性读数 | 写入任务 | 高 | 用 typed pages 表示存储 |
| `hawking_sampler` | 霍金采样器 | sensor/machine | 底噪谱仪升级 + 辐射谱片 + 超导环 | 合并霍金采样/回收 | 无 | `sensitivity`,`frequency_range`,`signal_noise_ratio`,`collection_rate` | 无 | `hawking_leak_rate`,`radiation_noise` | 黑洞发电/存储校验 | 附属 | S4 辐射 | 20 tick 或每 tick 抽象 | 高 | 采样面/回收面可用朝向区分 |
| `penrose_accretion_coil` | 彭罗斯吸积线圈 | machine/block | 超导环 + N 型晶片 + 抗压晶体 | 合并彭罗斯线圈/吸积盘环 | `mode` 可选 | `mass_capacity`,`spin_tolerance`,`extraction_efficiency`,`fed_mass` | 铁/金/钻石/下界合金块进料 | `fed_mass_score`,`spin_rate`,`capped_FE_output` | 视界核心、能量缓存 | 附属 | 质量/旋转读数 | 模式运行预算 | 高 | 发电核心外挂模块 |
| `artificial_horizon_core` | 人造视界核心 | multiblock_controller/block | III 框架 + 弦 + 约束环 + 全息膜 | 可控视界核心 | `horizon_radius`,`schwarzschild_mass`,`stabilizer_charges` 可选 | `horizon_stability`,`coherence`,`cooling`,`mode`,`active_process` | 信标/龙蛋视觉认知 | `horizon_framework`,`black_hole_operation` | 熵流泵、线圈、采样器 | 控制器 | S4 综合视界 | 每 tick <= 15 参数 | 高 | 稳定钥建议做 charges 而非独立物品 |
| `emergency_quencher` | 紧急熄灭器 | machine/block | 熵流泵 + 红石 + 相干能缓存 | 安全停机，防止全损 | 无 | `quench_speed`,`safe_discharge_ratio`,`armed` | 红石开关 | `emergency_shutdown`,`horizon_stability` | 视界核心 | 附属 | 安全状态 | 事件触发 | 中 | 成型条件必须有 |
| `string_anchor` | 戈古尔斯弦锚定器 | machine/block | 拓扑晶体 + 末地材料 + 相干能 | 残迹稳定为弦 | 无 | `anchor_stability`,`tension`,`decay_suppression` | 末地烛、末影材料 | `string_anchor_stability` | 戈古尔斯弦 | 否/附属 | S4 弦稳定 | 稳定化任务 | 高 | 阶段九入口机器 |
| `holographic_membrane_writer` | 全息膜刻写器 | machine | 信息中心 + 全息膜 + 视界材料 | 写入/读取全息膜 | 无 | `page_buffer`,`write_progress`,`error_rate` | 书写/制图台 | `holographic_storage`,`InfoSignal` | 全息膜、数据片 | 附属 | 完整性读数 | 写入任务 | 高 | 存储玩法核心 |
| `horizon_framework` | III 型人造视界框架 | multiblock_controller | 约束环 + 控制层 + 传感器 + 熄灭器 | 完整人造视界成型 | 无 | `FrameworkProfile(tier=3)`,`field_closure`,`entropy_extraction`,`noise_profile` | 多方块 | `horizon_framework`,`framework_process` | 视界核心全套 | 控制器 | S4 多传感器 | 缓存画像 + 每 tick 少量参数 | 高 | 结构上限建议 7x7x7 |

## 12. 阶段十：黑洞发电、存储与运算

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `black_hole_residue` | 黑洞解析残渣 | item | 视界退役/坍缩/运转副产 | 失败回收和高阶材料 | `residue_purity`,`elemental_composition` | 无 | 无 | `black_hole_operation` 副产 | 视界能量缓存 | 否 | 无 | 无 | 中 | 坍缩给残渣，降低惩罚 |
| `horizon_energy_buffer` | 视界能量缓存 | block/item | 残渣 + 稳谱晶体 + 相干稳压 | 高容量 FE/相干能存储 | `capacity`,`charge_rate`,`discharge_stability` 可选 | 方块态 `energy`,`stability` | FE、能量单元 | `capped_FE_output`,`coherent_energy` | 黑洞发电、创世 | 否 | 能量读数 | tick 能源接口 | 中 | v1.0 关键收益 |
| `holographic_data_slice` | 全息数据片 | data_item | 视界 + 全息膜 + 信息中心 | 黑洞存储产物 | `kamaen_storage_page`,`page_count`,`encoding_density`,`error_rate` | 无 | 末影箱、地图 | `holographic_storage`,`dimension_compiling` | 规则候选、维度矩阵 | 否 | 数据读数 | 写入任务结束 | 高 | 和存储页后端统一 |
| `entropy_gradient_result` | 熵梯度结果 | data_item | 黑洞运算任务输出 | 运算结果和维度优化 | `convergence_score`,`solution_path`,`confidence` | 无 | 无 | `entropy_gradient_search`,`black_hole_compute` | 规则候选 | 否 | 数据输出 | 长任务 | 高 | P1，可选上限 |
| `microstate_table` | 微观态枚举表 | data_item | 费曼蓝图 + 运算核心 | 黑洞运算中间数据 | `state_count`,`branch_factor`,`pruning_threshold` | 无 | 无 | `microstate_enumeration` | 熵梯度结果 | 否 | 无 | 长任务 | 高 | P2，不阻塞主线 |
| `dimension_rule_candidate` | 维度规则候选 | data_item | 视界协处理 + 底噪数据库 + 弦 | 创世规则输入 | `rule_type`,`compatibility_score`,`conflict_tags` | 无 | 数据包维度认知 | `dimension_compiling`,`rule_validation` | 创世蓝图 | 否 | 数据读数 | 运算任务 | 高 | 阶段十一 P0 前置 |
| `black_hole_compute_core` | 黑洞运算核心 | machine/component | 视界核心 + 量子光学协处理器 + 全息膜 | 视界加速运算 | `compute_budget`,`gradient_depth`,`solution_quality` 可选 | `active_task`,`budget`,`progress` | 无 | `black_hole_operation`,`quantum_optical_coprocessing` | 熵梯度/微观态 | 附属 | S4 运算诊断 | 长任务分步 | 高 | 可作为量子光学协处理器升级 |
| `entropy_rectifier` | 熵差整流器 | machine/block | 熵流泵升级 + 视界材料 | 熵流差发电/整流 | 无 | `entropy_delta`,`fe_output`,`efficiency` | FE | `entropy_flow`,`capped_FE_output` | 熵流泵、能量缓存 | 附属 | 熵差读数 | 每 tick 少量参数 | 高 | P1 |
| `horizon_cooling_tower` | 视界冷却塔 | multiblock_module | 低温系统 + 熵流泵 + 水/冰 | 控制黑洞热预算 | 无 | 控制器缓存 `cooling_capacity` | 水、冰、蓝冰 | `cooling`,`thermal_budget` | 视界核心 | 附属 | 温度读数 | 20 tick | 中 | 可先做单方块升级 |
| `horizon_address_indexer` | 视界地址索引器 | machine/block | 信息中心升级 + 全息膜 | 全息数据分页寻址 | 无 | `address_table`,`lookup_latency`,`page_cache` | 讲台/地图 | `holographic_storage`,`route_ops` | 全息数据片 | 附属 | 存储诊断 | 查询预算 | 高 | 存储玩法 P1 |

## 13. 阶段十一：世界之心与维度创世

| id | 中文名 | 类型 | 获取/合成 | 开发作用 | Data Component | BlockEntity 状态 | MC 原版关联 | Kamaen 参数关联 | 配套/同类 | 多方块 | 传感器 | 异步/预算 | 自定义程度 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `world_heart_frequency` | 世界之心频率 | data_item | 巨型节点框架超载萃取 | 当前维度核心频率 | `dimension_id`,`base_frequency`,`harmonic_overtones` | 无 | 下界之星、末地 | `dimension_compiling`,`world_background_noise` | 创世蓝图 | 否 | S4 世界频率 | 萃取长任务 | 高 | 失败不应永久毁档，可人工替代 |
| `dimension_parameter_matrix` | 维度参数矩阵 | data_item | 创世编译台 + 7 组模板参数 | 创世参数集合 | `dimension_parameter_matrix` | 无 | 地图/书 | `dimension_compiling` | 创世蓝图、维度核心 | 否 | 数据读数 | 编译前校验 | 高 | 主线提供预置模板 |
| `genesis_blueprint` | 创世蓝图 | data_item | 世界之心 + 弦 + 规则候选 | 待编译维度设计 | `dimension_parameter_matrix`,`compile_progress`,`validation_errors` | 无 | 地图、锻造模板 | `dimension_compiling`,`rule_validation` | 创世编译台 | 否 | 数据读数 | 长任务 | 高 | 不直接生成维度 |
| `spatial_anchor` | 空间锚 | block/component | 末地框架 + 视界能量缓存 | 固定维度入口和坐标 | `anchor_stability`,`linked_dimension`,`drift_rate` 可选 | `charge`,`linked_portal`,`stability` | 末地传送门框架、末影之眼 | `dimension_anchor`,`rule_drift` | 点火环、维度核心 | 结构模块 | 空间稳定读数 | 低频维护 | 高 | 可掉线后恢复入口 |
| `rule_interferometer` | 规则干涉器 | machine/sensor | 协处理器 + 规则候选 + 全息膜 | 校验/压制规则冲突 | 无 | `interference_power`,`rule_lock_strength`,`conflict_report` | 无 | `dimension_rule_candidate`,`rule_lock` | 维护塔、编译台 | 附属 | S4 规则漂移 | 20-200 tick | 高 | 高级自定义必需 |
| `compiled_dimension_core` | 已编译维度核心 | data_item/block | 蓝图 + 参数矩阵 + 视界能量缓存 | 维度入口和维护核心 | `dimension_definition_ref`,`entropy_budget`,`maintenance_cost_tick` | 若方块：`active_dimension`,`maintenance_state` | 无 | `dimension_compiling`,`maintenance_cost` | 点火环、空间锚 | 核心模块 | 数据读数 | 编译完成后生成 | 高 | 引用预注册模板，不无限注册 |
| `giant_node_framework` | 巨型节点框架 | multiblock_controller | 晶体管 + 凝聚态链路 + 稳定环 | 世界之心萃取/维度维护模式 | 无 | `FrameworkProfile`,`overload_progress`,`maintenance_mode`,`entropy_suppression` | 信标、多方块传送门 | `world_heart_extraction`,`dimension_maintenance` | 维护塔模式、点火环 | 控制器 | S4 世界/规则传感 | 长任务 + 低频维护 | 高 | 上限建议 9x9x9 |
| `genesis_compiler` | 创世编译台 | machine | 信息中心 + 黑洞运算核心 | 蓝图/矩阵/核心编译 | 无 | `input_blueprint`,`validation_errors`,`compile_progress` | 制图台 | `dimension_compiling` | 维度矩阵、维度核心 | 否 | 编译诊断 | 数百 tick 长任务 | 高 | 显示错误标签，避免黑盒失败 |
| `dimension_ignition_ring` | 维度点火环 | multiblock_controller | 空间锚 + 维度核心 + 视界能量 | 打开新维度入口 | 无 | `linked_core`,`ignition_progress`,`portal_state` | 末地传送门 | `dimension_anchor`,`compiled_dimension_core` | 空间锚 | 控制器 | 空间稳定读数 | 点火长任务 | 高 | 5x5 结构足够 |
| `dimension_maintenance_tower` | 维度维护塔 | multiblock_mode | 巨型节点框架维护模式 | 压制规则漂移和熵增 | 无 | `suppression_strength`,`energy_draw`,`material_consumption_rate`,`freeze_state` | 信标 | `entropy_rate`,`rule_drift`,`maintenance_cost` | 巨型节点框架 | 模式/附属 | S4 维度维护 | 低频抽样 | 高 | 建议不是独立结构，而是巨型框架模式 |

## 14. 传感器开发字典

| id | 中文名 | 传感类型 | 阶段 | 输入 | 输出 | 需要独立线程 | 预算/缓存 | 是否适合模型学习 | 实现备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `basic_spectroscope` | 初级分光镜 | 物品频谱 | 一 | 物品/方块 | 频谱、偏差、白噪潜势 | 否 | 无 | 否 | tooltip 或简单 GUI |
| `stress_sensor` | 应力传感器 | 应力椭球 | 二 | 晶体/框架过程 | stress、ellipsoid | 否 | 20 tick 或工艺结束 | 可选 | 放入 I 型框架提高精度 |
| `kamaen_probe_station` | 卡玛恩探针台 | 方块/红石/能力读取 | 三 | 目标方块/BE | InfoSignal | 否 | 20 tick 冷却 | 可选 | P0 只读 BlockState/红石 |
| `hardware_diagnostic_station` | 硬件诊断台 | 硬件性能画像 | 四/五 | CPU/GPU/内存/网络 | bottleneck_report | 否 | 手动/低频 | 是 | 指导自动化扩展 |
| `noise_spectrometer` | 底噪谱仪 | 维度底噪 | 五 | 维度、位置、层 | noise_sample | 否 | 同层缓存 200 tick | 是 | 批量结算，不开线程 |
| `entropy_flow_meter` | 熵流计 | 区块熵流 | 五 | chunk | entropy_flow_rate | 否 | 100-200 tick | 是 | 抽样估算 |
| `quasiparticle_detector` | 准粒子捕获器 | 准粒子响应 | 六 | 底噪、晶格、低温场 | propagator_plate/path | 否 | 捕获任务冷却 | 是 | 先电子/声子模式 |
| `wavefunction_sampler` | 波函数采样仪 | 坍缩风险摘要 | 七 | 协处理任务 | collapse_risk | 否 | 20 tick | 是 | 不保存真实波函数 |
| `hawking_sampler` | 霍金采样器 | 视界辐射/泄漏 | 八/九 | 人造视界 | leak_rate、parity、energy | 否 | 20 tick/每 tick抽象 | 是 | 复用辐射谱片 |
| `rule_interferometer` | 规则干涉器 | 维度规则冲突 | 十 | 规则候选、维度核心 | conflict_report | 否 | 20-200 tick | 是 | 高自定义维度才需要 |

## 15. 开发落地顺序

| 批次 | 必做条目 | 目的 |
| --- | --- | --- |
| A | `kamaen_crystal_state`,`spectrum_slag`,`white_noise_seed`,`fractionating_tower`,`basic_spectroscope` | 建立材料和 Data Component 基础 |
| B | `explosion_chamber_controller`,`raw_kamaen_crystal`,`waveguide_kamaen_crystal`,`compression_kamaen_crystal`,`stable_spectrum_kamaen_crystal` | 跑通晶体生成 |
| C | `infosignal`,`crystal_interferometer`,`kamaen_probe_station`,`frequency_bus`,`frequency_to_redstone_module` | 跑通信息读取闭环 |
| D | `kamaen_wafer`,`kamaen_dopant`,`ion_implanter`,`lattice_annealing_furnace`,`kamaen_transistor` | 跑通电气元件 |
| E1 | `logic_module_plate`,`chip_blueprint_writer`,`chip_packaging_station`,`packaged_logic_chip`,`hardware_diagnostic_station` | 跑通 ALU/控制芯片设计、封装和诊断 |
| E2 | `motherboard_blueprint`,`configurable_motherboard`,`memory_page`,`sensor_hub`,`storage_center_controller` | 跑通基础主板、传感器数据处理和存储页 |
| E3 | `network_interface_chip`,`fiber_switch`,`server_rack`,`model_component_gateway`,`model_compiler` | 扩展交换机、机柜、模型组件和编译部署 |
| E4 | `silicon_photonic_waveguide`,`mzi_modulator`,`phase_tuner`,`silicon_photodetector`,`single_freq_laser_source`,`coherent_energy`,`photonic_waveguide_etching_station`,`mzi_weaving_station`,`laser_pump_tower` | 跑通光计算工艺链与相干能资源（第 6 阶段铺垫） |
| E5 | `kamaen_nonlinear_medium`,`photonic_logic_gate`,`kamaen_bistable_cell`,`photonic_control_core`,`photonic_coprocessor`,`photonic_gpu_unit`,`photonic_pulse_processor`,`photonic_ram_unit`,`calibration_token`,`photonic_calibration_station` | 跑通全光五件套与光路校准（第 6 阶段核心） |
| F | `feynman_process_blueprint`,`propagator_plate`,`cryo_condensation_chamber`,`feynman_compiler`,`superconducting_kamaen_ring`,`single_photon_source`,`snspd_detector` | 凝聚态线（新增单光子源/SNSPD 作为量子光学前置） |
| G | `quantum_optical_coprocessor`,`synthesis_parameter_curve`,`meso_synthesis_scheduler` | 量子光学中观参数曲线（玻色采样路线） |
| H | `artificial_horizon_core`,`horizon_framework`,`entropy_pump`,`holographic_membrane`,`emergency_quencher` | 人造视界 |
| I | `horizon_energy_buffer`,`holographic_data_slice`,`dimension_rule_candidate` | 黑洞用途 |
| J | `world_heart_frequency`,`dimension_parameter_matrix`,`genesis_blueprint`,`compiled_dimension_core`,`dimension_ignition_ring` | 维度创世 |

# L3整合科技图与首次能力

当前设计图由[build_late_l3.py](build_late_l3.py)从R1基线与L3覆盖生成；前中期已有能力保留，后期首次依赖按连续玩法修订。机器数据：[late-l3-tech-tree.json](late-l3-tech-tree.json)。

共86项能力，其中29项可选深化；仍沿用P01—P28索引。编号用于归档，不是严格完成顺序。core表示主线能力候选，不表示每项必须逐一打卡。

**边界：** 检查首次能力依赖，不能证明每一配方、装置操作和玩家任务已可运行。实物额外条件见[内容表](LATE_L3_CONTENT.md)和专题。R1图保留历史，当前后期以本图为准。

| 能力 | 索引 | 名称 | 全部前置 | 路线 | 取得后能做什么 |
| --- | --- | --- | --- | --- | --- |
| `start` | P01 | 开局条件 | 开局 | core | 木材、圆石、水、普通燃料与基本种植可达 |
| `manual` | P01 | 无铁手筛与木盆 | start | core | 手工分离产出粉末与滤渣 |
| `metal` | P01 | 基础金属与玻璃 | manual | core | 累计产出与普通熔炼，不靠稀有抽奖 |
| `power` | P01 | 普通供能 | metal | core | 普通燃料/机械与电能尽早进入；首套产线留供给余量，外部FE可替代 |
| `mean` | P02 | 均值化基底 | manual, metal | core | 同批处理后偏差减弱 |
| `seed` | P02 | 白噪晶种 | mean | core | 结晶与放置复测，保留参考 |
| `raw` | P03 | 带物料来源的粗晶 | seed, metal | core | 晶种、生长基材与工艺冲击 |
| `stress` | P03 | 力学框架与特化 | raw, metal | core | 基本压头先可用，导波抗压稳谱按用途测 |
| `resonance` | P04 | 选择性共振 | stress, metal | core | 真实样本与晶体调谐改善合法产物份额 |
| `bio` | P04 | 有机分离 | resonance, manual | core | 真实有机基底供纤维树脂与培养前体 |
| `feedback` | P05 | 信息反馈闭环 | resonance, power | core | 探针、类型化信号、滞回、时效与停料恢复 |
| `scan` | P05 | 局部扫测与记录 | stress, power | core | 固定步进与单域读出先行，记录母批/顺序/量程；完整光电扫测随后整合 |
| `doping` | P06 | 组成特化 | stress, bio, feedback | core | 母批交叉掺杂与应力试片 |
| `precision` | P07 | 模板与工艺控制 | doping, metal | core | 粗接触模板先行、退火历史和分档；控制芯片之后反向改进精密工位 |
| `electric` | P08 | 电气门控 | precision, power | core | 结区、控制端、阈值与低速保持实验 |
| `optical` | P08 | 光学相位模块 | precision, resonance, power | core | 粗源与手动校准，两路组合实验 |
| `bridge` | P08 | 光电桥接 | electric, optical | core | 调制与探测，转换预算与读出校准 |
| `eda` | P09 | 实验结构与工程设计 | scan, precision, electric | core | 已测器件拼接与调谐、有限规则检查；同项目联到制造/实物/模型视图 |
| `package` | P09 | 模块封装与制造复制 | eda, precision | core | 先封装实际模块，再精密裸片复制；两条材料账与封装后复测 |
| `board` | P09 | 集成板 | package, power | core | 安装实体芯片与热/供能接口 |
| `store` | P10 | 持久记录与内存 | electric, precision | core | 空白记录柜先造，四类数据生命周期 |
| `runtime` | P10 | 单机运行时 | board, store | core | 单节点可承担本地信息中心；有限算子图、记录、预算与回滚 |
| `sensors` | P11 | 多点采集与对齐 | scan, store | core | 多探头、校准、位置与时间来源；不是首次局部记录的前置 |
| `network` | P11 | 联网采集与服务网络 | runtime, sensors | core | 实际节点直连与预设服务域，扩展本地信息中心；先单板后按需装柜 |
| `sky` | P11 | 初始星录 | optical, sensors | core | 基础天区强度与粗谱，不需量子设备 |
| `production_cell` | P11 | 可重组生产单元 | runtime, feedback, precision | extension | 复用工位/输送/检测，按实际订单排程与分流；模型优化和多线联网按需增加 |
| `e_matrix` | P12 | 电矩阵 | electric, precision, store | core | 有限算术阵列与电域基准 |
| `o_matrix` | P12 | 光矩阵 | optical, precision, store | core | 小阵列、编码读出与手动标定 |
| `hybrid` | P12 | 混合计算节点 | e_matrix, o_matrix, board, bridge | core | 同任务端到端成本与误差对照 |
| `cluster` | P12 | 实际节点集群 | e_matrix, network, board | core | 电节点可先直连；本地工作集、实际路径、分块与失败恢复 |
| `photonic_logic` | P12 | 光逻辑与非线性专化 | optical, precision | extension | 非线性介质、逻辑门、双稳态及有限工作域 |
| `photonic_control` | P12 | 光控制核 | photonic_logic, runtime | extension | 全光FSM与有限控制任务 |
| `photonic_ram` | P12 | 短时光RAM | photonic_logic, store | extension | 刷新、寿命与读取扰动 |
| `photonic_pulse` | P12 | 光脉冲处理器 | photonic_logic, o_matrix | extension | 登记非线性与稀疏任务 |
| `photonic_move` | P12 | 光协处理器 | o_matrix, network | extension | 光域搬运与路由预算 |
| `drone` | P12 | 无人机与移动作业 | package, runtime, feedback, scan | extension | 实际机体、驱动、测头与本地控制，先单机固定航路再学习/协作；不强加载区块 |
| `adaptive_gear` | P12 | 计算辅助装备 | model, package, feedback, precision | extension | 工艺/结构优化成果可离线使用；随身主动组件另付硬件、供给与热预算 |
| `model` | P13 | 小模型与参数 | runtime, scan | core | 公式查表与有限预测，首次不等集群 |
| `train` | P13 | 监督验证 | model, scan | core | 本地有效记录即可开展小批训练/验证；新母批留出、损失、版本和回退 |
| `model_families` | P13 | 模型与架构探索 | model | extension | 先用可运行小图研究结构/状态/算子；训练与规模按任务需要增加，不先要求集群 |
| `rl` | P14 | 控制基线与策略实验 | train, feedback | core | 规则/PID可满足基础闭环；有限Q-learning为深化，保留真实动作与未见扰动验收 |
| `bio_policy` | P14 | 培养与物流策略 | bio, rl, network | extension | 营养/库存/历史与实际任务收益 |
| `entity_policy` | P14 | 实体交易与对抗 | rl, runtime | extension | 支持代理、离线意图与可重置回放 |
| `active` | P15 | 主动实验 | train, rl, scan | core | 单工位先按模型分歧/成本选可执行工况并实际测量，多点扩展另接网络 |
| `noise` | P15 | 底噪分层与归因 | network, scan, model | core | 分层记录与实际对照；公式/规则基线可用，主动学习是扩展 |
| `advanced_network` | P15 | 多DNS与无线分代 | cluster | extension | G1–G6服务能力与多域解析挑战 |
| `api` | P15 | 外部后端 | active, runtime | extension | 同Schema、成本、时限、验收与离线替代 |
| `responsive_tool` | P15 | 可部署响应组合 | package, feedback, scan, runtime | core | 以现有器件做作业头/控制模块，按用途选择直接、保持或分步作用 |
| `cryo` | P16 | 独立低温工程 | precision, feedback, power | core | 普通制冷与散热，不依赖超导或视界 |
| `phase` | P16 | 凝聚态工作窗 | cryo, model | core | 温场相图、各材料用途的独立证据；可用公式/查表基线，不强制监督训练 |
| `pattern` | P16 | 区域谱纹与制造 | responsive_tool, precision, model | core | 粗分片先行，双区域结构与实际耦合，再精细复制 |
| `field_anchor` | P16 | 作用头与功能锚 | pattern, power | core | 实体位置、方向、路径与源，先支持局部可标定作用 |
| `spectrum` | P17 | 实验室谱尺 | optical, scan, model | core | 独立参考、多谱线与仪器偏置分离；有限模型校准先行 |
| `cosmic` | P17 | 宇观谱图与背景 | sky, spectrum, noise | extension | 红移谱册、对应波段接收头、余辉星图 |
| `field_workshop` | P17 | 织相工场 | field_anchor, runtime, scan | core | 串行、交叉和并列布局，实际剂量与工件历程 |
| `q_lab` | P18 | 基础量子光学实验 | optical, electric, store, precision | extension | 制备源、初级计数头、时间标签与符合扫描 |
| `q_cal` | P18 | 量子读出校准 | q_lab, model | extension | 暗计数、效率、窗口、HOM曲线与统计范围 |
| `snspd` | P18 | 低温探测升级 | phase, q_cal | extension | 超导探测器用于需要的读出任务 |
| `bell` | P18 | 贝尔教学挑战 | q_cal | extension | 明确态制备、多设置与采样假设 |
| `world_slice` | P18 | 世界切片 | field_workshop, sensors, model | core | 将已能控制的条件组织成可运行区域，支持生产和原版应用 |
| `effective` | P19 | 有效模型与费曼图 | pattern, model, scan | core | 有限过程蓝图先服务材料与作用；费曼/振幅按任务展开 |
| `world_reference` | P19 | 可复测远端参照 | sky, spectrum, network | core | 初始星录/谱尺即可开展，对区域记录提供独立参照 |
| `q_prepare` | P20 | 任务态制备与测量能力 | q_cal, effective | extension | 明确所需态与可测算符，拒绝不支持任务 |
| `q_hybrid` | P20 | 混合量子交叉验证 | q_prepare, runtime | extension | 有限期望估计、经典优化、实际试制与曲线 |
| `boson` | P20 | 玻色采样挑战 | q_cal, optical | extension | 固定采样任务，不替代VQE后端 |
| `qec` | P20 | 逻辑纠错深化 | q_prepare, phase | extension | 显式编码、综合征与译码资源 |
| `micro_boundary` | P21 | 微观边界对照 | phase, field_workshop, precision | core | 真实材料/区域作用的边界对照，量子方法按任务采用 |
| `regional_boundary` | P21 | 区域模式与边界关系 | world_slice, noise | core | 回响探索、位置与条件对照，得到可用于区域工程的关系 |
| `cosmic_geometry` | P22 | 宇观几何 | cosmic, model | extension | 多源透镜模板、测地卷与候选区间 |
| `bounded_link` | P22 | 有限特殊链路 | phase, pattern, regional_boundary, network | extension | 实际端点、支持的载荷、容量/时延和在线状态，首版小范围 |
| `cross` | P23 | 独立证据联合标定 | micro_boundary, regional_boundary, world_reference, model | core | 材料、区域与远端参照共同限制边界，产出实体接界组件与知识记录 |
| `string` | P23 | 戈古尔斯弦 | cross, phase, power | core | 实体载体、受限边界耦合与锚定 |
| `horizon_parts` | P24 | 首套约束膜与熄灭器 | phase, precision, feedback | core | 普通基膜及写入头，独立停机与启动储备 |
| `horizon` | P24 | 受控视界 | string, horizon_parts, power | core | 普通能源启动、降载停机、回收与重启 |
| `mode_power` | P25 | 视界发电模式 | horizon | extension | 登记质量与净能量账，不重复记账 |
| `mode_store` | P25 | 视界存储模式 | horizon, store | extension | 全息页、校验、持久保留与读回 |
| `mode_compute` | P25 | 视界求解模式 | horizon, effective, runtime | extension | 有限候选搜索、可验证输出 |
| `advanced_optics` | P25 | 长期光存储与WDM | optical, network, store, phase | extension | 独立持久光介质、WDM与交换；全息膜和短时光RAM按所选实现追加条件，不共绑视界 |
| `closure` | P26 | 双尺度闭合图谱 | horizon, world_slice, cross, world_reference, cluster, hybrid | core | 集群与光电节点整合材料、区域、远端参照及边界运行；三种视界模式按用途扩展 |
| `heart` | P26 | 世界之心辨识 | closure, sensors | core | 可复测世界特征与不确定度，不破坏源世界 |
| `rules` | P27 | 维度规则候选 | heart, effective, runtime | core | 经典有限基线先生成七组参数候选；视界求解可扩大搜索 |
| `genesis` | P27 | 蓝图与实体核心 | rules, string, store, horizon_parts | core | 资料参与编译，实体基材/控制/锚与储备成核心；普通存储可用 |
| `return_anchor` | P27 | 母世界返回与救援锚 | horizon_parts, power, cross | core | 在创建新世界之前建成独立返回和救援能力 |
| `world` | P27 | 点火与新维度 | genesis, return_anchor | core | 使用空闲槽，不覆盖旧世界 |
| `maintain` | P28 | 维护休眠与返回 | world, closure | core | 实际作业、离开、休眠、恢复、返回与复测 |
| `dim_gateway` | P28 | 跨维度网关 | bounded_link, network, string | extension | 先支持已有原版维度的成对服务；新增世界在取得实例后加入 |

## 相比R1/L1改变的首次依赖

| 能力 | 此前前置/路线 | 当前前置/路线 |
| --- | --- | --- |
| noise | active, network / core | network, scan, model / core |
| cosmic | sky, spectrum, noise / core | sky, spectrum, noise / extension |
| q_lab | optical, electric, store, precision / core | optical, electric, store, precision / extension |
| q_cal | q_lab, train / core | q_lab, model / extension |
| effective | phase, noise, model / core | pattern, model, scan / core |
| q_prepare | q_cal, effective / core | q_cal, effective / extension |
| q_hybrid | q_prepare, runtime / core | q_prepare, runtime / extension |
| micro_boundary | phase, q_hybrid, precision / core | phase, field_workshop, precision / core |
| cosmic_geometry | cosmic, train / core | cosmic, model / extension |
| cross | micro_boundary, cosmic_geometry, noise / core | micro_boundary, regional_boundary, world_reference, model / core |
| mode_power | horizon / core | horizon / extension |
| mode_store | horizon, store / core | horizon, store / extension |
| mode_compute | horizon, effective, runtime / core | horizon, effective, runtime / extension |
| advanced_optics | mode_store, photonic_ram, photonic_move / extension | optical, network, store, phase / extension |
| closure | mode_power, mode_store, mode_compute, cosmic_geometry, cross, cluster, hybrid / core | horizon, world_slice, cross, world_reference, cluster, hybrid / core |
| rules | heart, mode_compute / core | heart, effective, runtime / core |
| genesis | rules, string, mode_store / core | rules, string, store, horizon_parts / core |
| return_anchor | horizon_parts, power, heart / core | horizon_parts, power, cross / core |
| dim_gateway | world, network, string / extension | bounded_link, network, string / extension |

量子、透镜、视界三用途及训练方法均保留，但不统一充当创世前置；材料边界与实际远端参照继续共同参与收束。特殊链路可先服务已有原版维度，新世界实例建立后再接入。完整玩法：[L3总稿](LATE_L3_COMPLETE_GAMEPLAY.md)。

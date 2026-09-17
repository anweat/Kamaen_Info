# R1统一科技依赖与能力表

以[审核总案](REVIEW_SYSTEM.md)为语义依据。箭头/前置表示首次取得能力的AND关系；量产反馈不计作首次依赖。core包含主线教学体验，extension是保留的深化玩法。编号不是强制串行日期。

**范围：能力依赖可达，不是完整物品配方验证。** 当前P06–15的粗版/精密版、模块封装、初始电节点集群与控制基线已同步[R4阶段设计](R4_STAGE_DESIGN.md)；[R4材料目录](R4_MATERIALS_MACHINES.md)提供本阶段逐数量基线，后续低温和膜工艺仍需分段深化。

2026-09-08按[前中期总览与后期入口](EARLY_MID_REVIEW_AND_LATE_ENTRY.md)同步：早期供能/局部扫测、电单板独立入口、单机学习与架构探索，以及[三类中期应用候选](MIDGAME_APPLICATIONS.md)。新增应用为深化能力，不是后期门槛或已注册物品。

| 节点 | 里程碑 | 能力 | 全部前置 | 路线 | 可见成果 |
| --- | --- | --- | --- | --- | --- |
| `start` | P01 | 开局条件 | 开局 | core | 木材、圆石、水、普通燃料与基本种植可达 |
| `manual` | P01 | 无铁手筛与木盆 | start | core | 手工分离产出粉末与滤渣 |
| `metal` | P01 | 基础金属与玻璃 | manual | core | 累计产出与普通熔炼，不靠稀有抽奖 |
| `mean` | P02 | 均值化基底 | manual、metal | core | 同批处理后偏差减弱 |
| `seed` | P02 | 白噪晶种 | mean | core | 结晶与放置复测，保留参考 |
| `raw` | P03 | 带物料来源的粗晶 | seed、metal | core | 晶种、生长基材与工艺冲击 |
| `stress` | P03 | 力学框架与特化 | raw、metal | core | 基本压头先可用，导波抗压稳谱按用途测 |
| `power` | P01 | 普通供能 | metal | core | 普通燃料/机械与电能尽早进入；首套产线留供给余量，外部FE可替代 |
| `resonance` | P04 | 选择性共振 | stress、metal | core | 真实样本与晶体调谐改善合法产物份额 |
| `bio` | P04 | 有机分离 | resonance、manual | core | 真实有机基底供纤维树脂与培养前体 |
| `feedback` | P05 | 信息反馈闭环 | resonance、power | core | 探针、类型化信号、滞回、时效与停料恢复 |
| `doping` | P06 | 组成特化 | stress、bio、feedback | core | 母批交叉掺杂与应力试片 |
| `precision` | P07 | 模板与工艺控制 | doping、metal | core | 粗接触模板先行、退火历史和分档；控制芯片之后反向改进精密工位 |
| `electric` | P08 | 电气门控 | precision、power | core | 结区、控制端、阈值与低速保持实验 |
| `optical` | P08 | 光学相位模块 | precision、resonance、power | core | 粗源与手动校准，两路组合实验 |
| `bridge` | P08 | 光电桥接 | electric、optical | core | 调制与探测，转换预算与读出校准 |
| `scan` | P05 | 局部扫测与记录 | stress、power | core | 固定步进与单域读出先行，记录母批/顺序/量程；完整光电扫测随后整合 |
| `eda` | P09 | 实验结构与工程设计 | scan、precision、electric | core | 已测器件拼接与调谐、有限规则检查；同项目联到制造/实物/模型视图 |
| `package` | P09 | 模块封装与制造复制 | eda、precision | core | 先封装实际模块，再精密裸片复制；两条材料账与封装后复测 |
| `board` | P09 | 集成板 | package、power | core | 安装实体芯片与热/供能接口 |
| `store` | P10 | 持久记录与内存 | electric、precision | core | 空白记录柜先造，四类数据生命周期 |
| `runtime` | P10 | 单机运行时 | board、store | core | 单节点可承担本地信息中心；有限算子图、记录、预算与回滚 |
| `sensors` | P11 | 多点采集与对齐 | scan、store | core | 多探头、校准、位置与时间来源；不是首次局部记录的前置 |
| `network` | P11 | 联网采集与服务网络 | runtime、sensors | core | 实际节点直连与预设服务域，扩展本地信息中心；先单板后按需装柜 |
| `sky` | P11 | 初始星录 | optical、sensors | core | 基础天区强度与粗谱，不需量子设备 |
| `e_matrix` | P12 | 电矩阵 | electric、precision、store | core | 有限算术阵列与电域基准 |
| `o_matrix` | P12 | 光矩阵 | optical、precision、store | core | 小阵列、编码读出与手动标定 |
| `hybrid` | P12 | 混合计算节点 | e_matrix、o_matrix、board、bridge | core | 同任务端到端成本与误差对照 |
| `cluster` | P12 | 实际节点集群 | e_matrix、network、board | core | 电节点可先直连；本地工作集、实际路径、分块与失败恢复 |
| `model` | P13 | 小模型与参数 | runtime、scan | core | 公式查表与有限预测，首次不等集群 |
| `train` | P13 | 监督验证 | model、scan | core | 本地有效记录即可开展小批训练/验证；新母批留出、损失、版本和回退 |
| `rl` | P14 | 控制基线与策略实验 | train、feedback | core | 规则/PID可满足基础闭环；有限Q-learning为深化，保留真实动作与未见扰动验收 |
| `active` | P15 | 主动实验 | train、rl、scan | core | 单工位先按模型分歧/成本选可执行工况并实际测量，多点扩展另接网络 |
| `noise` | P15 | 底噪分层与归因 | active、network | core | 近远开关对照、相关波动与残差档案 |
| `cryo` | P16 | 独立低温工程 | precision、feedback、power | core | 普通制冷与散热，不依赖超导或视界 |
| `phase` | P16 | 凝聚态工作窗 | cryo、model | core | 温场相图、各材料用途的独立证据；可用公式/查表基线，不强制监督训练 |
| `spectrum` | P17 | 实验室谱尺 | optical、scan、model | core | 独立参考、多谱线与仪器偏置分离；有限模型校准先行 |
| `cosmic` | P17 | 宇观谱图与背景 | sky、spectrum、noise | core | 红移谱册、对应波段接收头、余辉星图 |
| `q_lab` | P18 | 基础量子光学实验 | optical、electric、store、precision | core | 制备源、初级计数头、时间标签与符合扫描 |
| `q_cal` | P18 | 量子读出校准 | q_lab、train | core | 暗计数、效率、窗口、HOM曲线与统计范围 |
| `effective` | P19 | 有效模型与费曼图 | phase、noise、model | core | 登记自由度、允许顶点、经典小任务基准 |
| `q_prepare` | P20 | 任务态制备与测量能力 | q_cal、effective | core | 明确所需态与可测算符，拒绝不支持任务 |
| `q_hybrid` | P20 | 混合量子交叉验证 | q_prepare、runtime | core | 有限期望估计、经典优化、实际试制与曲线 |
| `micro_boundary` | P21 | 微观边界对照 | phase、q_hybrid、precision | core | 有限间隙与表面对照，材料及仪器偏置分离 |
| `cosmic_geometry` | P22 | 宇观几何 | cosmic、train | core | 多源透镜模板、测地卷与候选区间 |
| `cross` | P23 | 独立证据联合标定 | micro_boundary、cosmic_geometry、noise | core | 互证谱册与实体接界棱镜 |
| `string` | P23 | 戈古尔斯弦 | cross、phase、power | core | 实体载体、受限边界耦合与锚定 |
| `horizon_parts` | P24 | 首套约束膜与熄灭器 | phase、precision、feedback | core | 普通基膜及写入头，独立停机与启动储备 |
| `horizon` | P24 | 受控视界 | string、horizon_parts、power | core | 普通能源启动、降载停机、回收与重启 |
| `mode_power` | P25 | 视界发电模式 | horizon | core | 登记质量与净能量账，不重复记账 |
| `mode_store` | P25 | 视界存储模式 | horizon、store | core | 全息页、校验、持久保留与读回 |
| `mode_compute` | P25 | 视界求解模式 | horizon、effective、runtime | core | 有限候选搜索、可验证输出 |
| `closure` | P26 | 双尺度闭合图谱 | mode_power、mode_store、mode_compute、cosmic_geometry、cross、cluster、hybrid | core | 集群与光电互证能力共同组织视界、宇观和底噪记录 |
| `heart` | P26 | 世界之心辨识 | closure、sensors | core | 可复测世界特征与不确定度，不破坏源世界 |
| `rules` | P27 | 维度规则候选 | heart、mode_compute | core | 固定种类、七组参数、硬约束与预算 |
| `genesis` | P27 | 蓝图与实体核心 | rules、string、mode_store | core | 有限模板编译、实体资源与唯一实例绑定 |
| `return_anchor` | P27 | 母世界返回与救援锚 | horizon_parts、power、heart | core | 不依赖待创建维度的供能和出口 |
| `world` | P27 | 点火与新维度 | genesis、return_anchor | core | 使用空闲槽，不覆盖旧世界 |
| `maintain` | P28 | 维护休眠与返回 | world、closure | core | 实际作业、离开、休眠、恢复、返回与复测 |
| `photonic_logic` | P12 | 光逻辑与非线性专化 | optical、precision | extension | 非线性介质、逻辑门、双稳态及有限工作域 |
| `photonic_control` | P12 | 光控制核 | photonic_logic、runtime | extension | 全光FSM与有限控制任务 |
| `photonic_ram` | P12 | 短时光RAM | photonic_logic、store | extension | 刷新、寿命与读取扰动 |
| `photonic_pulse` | P12 | 光脉冲处理器 | photonic_logic、o_matrix | extension | 登记非线性与稀疏任务 |
| `photonic_move` | P12 | 光协处理器 | o_matrix、network | extension | 光域搬运与路由预算 |
| `advanced_network` | P15 | 多DNS与无线分代 | cluster | extension | G1–G6服务能力与多域解析挑战 |
| `bio_policy` | P14 | 培养与物流策略 | bio、rl、network | extension | 营养/库存/历史与实际任务收益 |
| `entity_policy` | P14 | 实体交易与对抗 | rl、runtime | extension | 支持代理、离线意图与可重置回放 |
| `model_families` | P13 | 模型与架构探索 | model | extension | 先用可运行小图研究结构/状态/算子；训练与规模按任务需要增加，不先要求集群 |
| `production_cell` | P11 | 可重组生产单元 | runtime、feedback、precision | extension | 复用工位/输送/检测，按实际订单排程与分流；模型优化和多线联网按需增加 |
| `drone` | P12 | 无人机与移动作业 | package、runtime、feedback、scan | extension | 实际机体、驱动、测头与本地控制，先单机固定航路再学习/协作；不强加载区块 |
| `adaptive_gear` | P12 | 计算辅助装备 | model、package、feedback、precision | extension | 工艺/结构优化成果可离线使用；随身主动组件另付硬件、供给与热预算 |
| `api` | P15 | 外部后端 | active、runtime | extension | 同Schema、成本、时限、验收与离线替代 |
| `snspd` | P18 | 低温探测升级 | phase、q_cal | extension | 超导探测器用于需要的读出任务 |
| `bell` | P18 | 贝尔教学挑战 | q_cal | extension | 明确态制备、多设置与采样假设 |
| `boson` | P20 | 玻色采样挑战 | q_cal、optical | extension | 固定采样任务，不替代VQE后端 |
| `qec` | P20 | 逻辑纠错深化 | q_prepare、phase | extension | 显式编码、综合征与译码资源 |
| `advanced_optics` | P25 | 长期光存储与WDM | mode_store、photonic_ram、photonic_move | extension | 容量、寿命、串扰与全光交换 |
| `dim_gateway` | P28 | 跨维度网关 | world、network、string | extension | 成对锚、服务授权和离线处理 |

## 持续反馈（不作为首次解锁依赖）

- 掺杂/相图/学习改进既有晶体和分离线；工艺历史仍需复测。
- 微观材料改进天空探测，宇观参照检验本地模型。
- 全光专化改善部分任务，电域继续承担控制、存储与接口。
- 流水线、无人机与装备消化前中期能力，产生新的工况记录；规模学习与集群按实际任务扩展。
- 视界产能改善后续工业，首次视界仍用普通能源。
- 新维度测量复核既有模型，不复制/覆盖已有世界。

自动检查与反例见[验证记录](REVIEW_VALIDATION.md)。

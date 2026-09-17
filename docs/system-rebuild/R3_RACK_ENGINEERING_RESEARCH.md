# R3.3调研：真实机柜与集成电路怎样转成工程玩法

日期：2026-09-07。用途是为[机柜环境与工程玩法](COMPUTING_R3_RACK_ENVIRONMENT_AND_ENGINEERING.md)提供事实依据与取舍，不是现实机房施工指南。厂商产品只是具体案例，不把其尺寸、电压、温度、带宽或维护规定直接写成游戏规则。

检索使用agent-reach的Exa网页检索，结合网页检索与原文阅读。只采用厂商、开放硬件/PDK维护方与原始研究。读取范围分别标明；本轮没有安装仿真工具，也没有验证Minecraft运行。

## 1. 三种有用的真实案例

| 案例 | 原文支持的事实 | 对本项目的设计推导 |
| --- | --- | --- |
| DGX H100 SuperPOD风冷机房 | 柜列朝向组织冷热通道；挡板与穿线处封堵用于控制回流；降低密度会增加占地和布线距离。见[S01](#s01)。 | 普通板先能运行；持续负载推动风道、理线和柜列布置。扩大间距不是免费改善，要多用空间和线缆。 |
| DGX GB机架系统 | 托盘、铜缆背板、供电母排、液冷分配管构成实际系统；CPU/GPU使用冷板，其他部件仍有风冷。见[S05](#s05)。 | 高密度柜由玩家的小组件组成；液冷升级保留电源、接口等剩余热源，不能给整个柜子一个“液冷后免热”属性。 |
| 光学平台与光子芯片 | 隔振与结构阻尼解决不同问题；热光阵列需要考虑热串扰。见[S08](#s08)、[S12](#s12)。 | 精密计算柜与普通电控制柜的敏感频段和工作窗不同；晶体调谐、安装和环境研究继续有价值。 |

这些案例共同支持的设计方向是：**器件能力、实际安装、供给与可维护性共同决定持续服务能力。**这句话是本项目的综合判断，不是某个规范的原文结论。

## 2. 来源与读取边界

### S01

[NVIDIA：Cooling and Airflow Optimization](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/cooling.html)，页面更新2025-11-19；已读正文。

冷热通道控制进风与排风；热气回流会抬高服务器入口温度。空位挡板与穿线口封堵是通道组织的一部分。冷却不足时降低密度或拉开机柜距离，会影响空间和线长。

采纳：分区温度、实际风路和串柜影响。游戏不搬用该产品的通道宽度、热负载与部署图例数字。

### S02

[NVIDIA：White Space Infrastructure](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/infrastructure.html)，H100数据中心设计指南；已读检索返回的相关正文段落。

该部署同时考虑柜宽、理线、配电位置、导轨、检修距离和扩展空间；网络设备的气流方向与安装位置有关。

采纳：接口面、气流方向、抽出方向分别声明；选风扇/外壳模板才改变风路，旋转外观不凭空反转内部风扇。具体柜型和安装尺寸不通用。

### S03

[NVIDIA：Cable Management Guidance](https://docs.nvidia.com/dgx-superpod/design-guide-cabling-data-centers/latest/cable-management-guidance.html)，页面更新2025-11-19；已读正文。

导线需要遵守自身弯曲限制、承重与应力支撑，并兼顾电源/铜数据/光数据分路、风流和标记。

采纳：线缆类别有自己的外径、弯曲半径、接头与支撑需求。不同类别不是仅换皮肤；不为所有线缆规定同一个现实半径。

### S04

[NVIDIA：Deploying the Bundles](https://docs.nvidia.com/dgx-superpod/design-guide-cabling-data-centers/latest/deploying-bundles.html)，Cabling Data Centers Design Guide；已读相关正文。

该指南指出穿越机柜中央的线束可能阻挡气流及设备插拔，线缆余量的放置也会影响拥挤程度。

采纳：运行可通与检修可达分开检查。游戏允许保留能运行但难维护的布局，预览解释代价，不对“线不好看”扣分。

### S05

[NVIDIA：DGX GB Rack Scale Systems — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)，页面更新2026-03-03；已读正文。

系统有计算托盘、交换托盘、被动铜缆背板、电源架、母排、冷却分配管和管理接口。冷板服务CPU/GPU，其他组件仍通过空气散热。后部接口也承担维护访问。

采纳：计算数据、管理、供电、冷却分别有实际路径；可用同一外壳承载，但不能合成一条万能总线。本稿不复制NVLink域、GPU数量或电源冗余配方。

### S06

[OCP：Open Rack V3 Blind Mate Manifold Specification，Rev 1.0，2024-04-05](https://www.opencompute.org/documents/open-rack-v3-blind-mate-manifold-specification-rev-1-0-review-april05-2024-pdf)；[OCP规范目录](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns)已读取。PDF全文抓取超时，仅取得检索收录的§14及第25页相关段落。

可支持的有限事实：盲插液冷接口的工作范围与机架、设备、分配管的变形预算相关，还需考虑热膨胀。

采纳：高级盲插模板需要机械容差及供回口匹配。未核验完整阀门、压力或测试条款，不据此制定现实参数或声称符合OCP。

### S07

[TI：Semiconductor and IC Package Thermal Metrics，SPRA953D](https://www.ti.com/lit/pdf/spra953)，2024-03修订；已读取PDF相关章节。

结到环境热阻依赖测试板与系统环境，不能把数据表的一个值视作封装在任何装配下的固有常数。

采纳：保留局部发热、封装/载板接触和外部散热边界；测得的整件温升报告须绑定工况。不得同时套用整件热阻与已含其中的内部路径。

### S08

[Newport：Optical Table System Design](https://www.newport.com/n/vibration-control-systems/)，页面未标明发布日期；浏览器正文提取为空，改由Exa读取完整相关段落。

光学装配关注部件相对位移。结构刚度、隔振支撑和阻尼作用不同；隔振器在固有频率附近可能放大振动，高于一定频段才有效隔离。新增载荷也会改变结构响应。

采纳：扫描振源频率、支撑与载荷的匹配。共架刚体位移与内部变形分开；数值采用自定义低阶模型，不套用厂商产品曲线。

### S09

[Microchip：AN6172 — Clock Jitter Basics，DS00006172A](https://ww1.microchip.com/downloads/aemDocuments/documents/VOP/ApplicationNotes/ApplicationNotes/AN6172-Clock-Jitter-Basics-DS00006172.pdf)，2025；已读PDF，重点第1、3、10–12页。

抖动有不同测量定义与积分频带；振动、串扰和供电噪声可影响振荡器。石英的加速度敏感性是现实类比依据。

采纳：卡玛恩晶振测量自己的敏感轴与频带；它是虚构材料，不能直接继承石英系数。本文只引用这些概念，不搬用原文示例参数或所有近似公式。

### S10

[Analog Devices：What Are the Basic Guidelines for Layout Design of Mixed-Signal PCBs?](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html)，已读相关正文；本轮不依赖发表日期。

混合信号设计需考虑布局、去耦和电流返回路径；不同系统的接地组织需要根据实际器件与电流路径判断。

采纳：提供已知有效的供电/返回路径模板，允许对照实验。不设置“模拟数字必须割裂地平面”或“一块屏蔽板通吃所有干扰”的规则。

### S11

[TI：SSZT090 — 降低开关电源EMI的布局与集成电容讨论](https://www.ti.com/document-viewer/lit/html/SSZT090/GUID-D62264EC-5FF1-497C-9311-E3E043EE6B4F)，已读正文；以文献编号限定来源。

高变化率电流回路面积、开关节点面积及电容位置影响EMI；封装内集成电容可改变这些路径。

采纳：制程/封装/板级都有改善局部供给与耦合的机会。工程效果落到真实连接与局部结构，不给整柜无条件加成。

### S12

[Gurses等：Large-Scale Crosstalk-Corrected Thermo-Optic Phase Shifter Arrays in Silicon Photonics](https://arxiv.org/abs/2206.04525)，2022-06-05提交；已读作者与摘要，仅据摘要引用成果方向，未复现全文实验。

该原始研究报告热光相移阵列、热激励模型及热串扰修正方法，并比较控制方案。

采纳：调谐器自身热量进入邻接模型；测得交叉响应后可做有工作窗的补偿。游戏耦合矩阵、参数和验收阈值均需独立设计，不声称复现该芯片。

### S13

[SkyWater SKY130 PDK：Physical & Design Verification](https://skywater-pdk.readthedocs.io/en/main/verification.html)，在线main文档，2026-09-07读取；已读正文，页面有未完成条目。

文档区分设计规则检查、版图与原理对应检查及寄生提取，并明确部分规则不能由检查工具覆盖。

采纳：EDA自动回答“可制造吗、连接一致吗、实际响应如何变化”；三个结论不能互相代替。仅借鉴职责，不要求玩家使用真实PDK或认为所有检查已经可执行。

### S14

[SkyWater SKY130 PDK：Parasitic Layout Extraction](https://skywater-pdk.readthedocs.io/en/main/rules/rcx.html)，在线main文档，2026-09-07读取；已读相关正文与规则说明。

提取规则区分器件模型已经包含的寄生项和外部应提取部分，也披露工具/模型范围差异。

采纳：器件、封装与主板的因子声明覆盖边界，防止同一接触/线路被重复结算。此处不导入SKY130的电阻、电容或几何值。

## 3. 回接旧稿的修订

| 旧稿思想/冲突 | 本轮处理 |
| --- | --- |
| [Runtime §4–6](../Kamaen_Runtime_Infrastructure/Complete_Path.md)：封装、板、机柜逐层热预算和追踪 | 保留对象与TracePath，改为热源/储热/导热/搬热模型；差导热改变温升，不凭空改变产生的能量。 |
| [Runtime 光刻环境](../Kamaen_Runtime_Infrastructure/Complete_Path.md)：世界位置、声学/振动和工况 | 扩展到上架后的运行环境；加工留存的材料状态与运行时扰动分开。 |
| [EDA §3、5](../Kamaen_Info_Computing_EDA_Design.md)：方向、工程层、规则与自动布线 | R3保留物理后果和辅助检查；不用双视图微结构作为必修入口。 |
| [硬件 §7–9](../Kamaen_Info_Hardware_TechTree_Design.md)：板/背板、机柜个体、端口、诊断 | 扩展真实线路几何、服务方向、局部场与上游故障范围；不再用统一cable_quality替代所有原因。 |
| “不模拟真实电磁场”与新增电磁影响 | 保留不解全场的范围；引入有限频段、已知耦合路径与器件响应近似，满足用户对工程影响的要求。 |
| 光与电整片硬隔离、光计算统一高阶锁相 | 继续按R3.2分开工艺兼容、信号表示和工作条件。包网络、模拟光路和量子状态各有边界。 |

## 4. 建议的复杂度边界

主线逐步引入持续负载、风路、可达接口、局部噪声诊断；密集相干阵列才推动精细隔振、串扰补偿和专用参考。默认模板能完成早期任务，自建结构仍有空间/能效/精度/维护上的实际收益。

真实工程的启发转成“提出假设→换一个部件或路径→复测→沉淀模板”。本轮不加入全场CFD/电磁/有限元求解、逐引脚手算、固定日期维护和没有征兆的随机损坏。后期更复杂的研究必须带来可观测的新能力，不能只增加清单长度。

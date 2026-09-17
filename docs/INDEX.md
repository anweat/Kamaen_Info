# Kamaen Info 文档索引

版本：v0.6 Index  
状态：文档组导航根节点。所有设计文档以本索引为出发点，迭代时以本文记录变更摘要。

---

## 1. 文档地图

### 1.1 核心设计文档（必读）

| 文档 | 定位 | 最近重大更新 |
|------|------|------------|
| [GDD.md](Kamaen_Info_GDD.md) | 模组核心愿景、设计原则、阶段玩法摘要 | v0.6：非电信息路线，电只作为供能 |
| [TechTree_Plan.md](Kamaen_Info_TechTree_Plan.md) | 完整科技树计划，阶段目标、配方、门槛 | v0.6：Stage 4-5 改为光路工艺与共振信息自动化 |
| [Stage_Content_Line.md](Kamaen_Info_Stage_Content_Line.md) | 逐阶段物品/方块开发表，优先级，实现边界 | v0.6：Stage 4-5 非电路线更新 |
| [Core_Gameplay_Development_Plan.md](Kamaen_Info_Core_Gameplay_Development_Plan.md) | 核心玩法开发任务拆分，按玩法密度优先规划实现顺序 | v0.2：玩法优先，卡玛恩晶体原型前置 |

### 1.2 系统深度设计文档

| 文档 | 定位 | 依赖的核心文档 |
|------|------|------------|
| [Computing_EDA_Design.md](Kamaen_Info_Computing_EDA_Design.md) | 算力系统与多工艺 EDA：电/光/量子微逻辑门、存储、冷却、封装与隔离规则 | GDD §5.5, TechTree §7–10 |
| [Optical_Computing_Design.md](Kamaen_Info_Optical_Computing_Design.md) | 全光计算系统完整规范（五件套架构、激发-湮灭周期、费曼桥接） | Computing_EDA §8, TechTree §9 |
| [Information_System_Design.md](Kamaen_Info_Information_System_Design.md) | 信息系统：数据分类、模型运行、传感器、路由、反馈、训练 | GDD §5.3–5.5 |
| [Hardware_TechTree_Design.md](Kamaen_Info_Hardware_TechTree_Design.md) | 硬件基础设施：芯片层到集群层六层架构 | GDD §5.5, TechTree §7–8 |
| [Resonance_Crystal_And_Early_Game_Design.md](Kamaen_Info_Resonance_Crystal_And_Early_Game_Design.md) | 卡玛恩晶体定义、共振规则、早期机械合成 | GDD §3, TechTree §4–5 |

### 1.3 参考文档

| 文档 | 定位 |
|------|------|
| [Complex_Manufacturing_Process_Reference.md](Kamaen_Info_Complex_Manufacturing_Process_Reference.md) | 复杂工艺流程参考 |
| [Item_Block_Dictionary.md](Kamaen_Info_Item_Block_Dictionary.md) | 逐物品/方块固定字段开发表单 |

### 1.4 设计历史文档

| 文档 | 定位 |
|------|------|
| [DESIGN_HISTORY.md](DESIGN_HISTORY.md) | 主要设计决策记录：变更原因、收录的旧想法、演进过程 |

---

## 2. 阅读路径

### 首次接触模组（设计师视角）
```
GDD.md → Resonance_Crystal → TechTree_Plan §1-3 → INDEX §3（核心设计原则）
```

### 开发具体阶段（开发者视角）
```
TechTree_Plan §[目标阶段] → Stage_Content_Line §[对应章节] → 对应系统文档
```

### 理解全光计算设计
```
Optical_Computing_Design.md §1（设计定位）→ §4（光控制核）→ §13（费曼桥接）
→ Information_System_Design §10.2
```

### 理解算力系统与 EDA
```
Computing_EDA_Design.md §1（设计目标）→ §2（工艺族）→ §3（隔离规则）
→ §4（蓝图数据）→ Optical_Computing_Design.md §2-4
```

### 理解早期-中期晶体路径的连续性
```
Resonance_Crystal §2-4（晶体定义）→ TechTree_Plan §4-7（力学/光路工艺阶段）
→ Optical_Computing §3（工艺链）→ §1.3（激发-湮灭）
```

---

## 3. 核心设计原则（快速参考）

### 3.1 能量职责分离

```
FE（锻造能量）= 热力学功
  → 早期机器运转（爆炸室、共振分离阵列、分馏塔）
  → 物质生产、传感器供能、数据采集基础设施
  → 「让机器转起来」

相干能（Coherent Energy）= 信息传播
  → 第 3 阶段起：精密工艺（光刻、掺杂、退火）的低噪能源
  → 第 6 阶段起：维持全光计算路径相干（MZI 网络、双稳态腔、循环腔）
  → 「让计算发生」

晶体 = 两者的桥梁
  → FE 通过机械应力「写入」晶体（向量爆破）
  → 相干能通过光「读出」晶体（激发-湮灭）
```

### 3.2 晶体作为计算介质的连续性

```
第 2 阶段（力学合成）：
  向量爆破参数 → 写入应力张量 = 「编程」晶体
  晶体应力状态 = 「程序输出」（也是第 6 阶段光逻辑门的 χ⁽²⁾ 系数来源）

第 3 阶段（共振调谐）：
  晶体频谱与目标频谱干涉 = 模拟滤波运算
  InfoSignal = 把模拟结果「量化读出」

第 4-5 阶段（光路工艺 / 共振信息自动化）：
  晶格结构 → 掺杂 → 导波/阈值/相位调谐 = 「晶格光路化」
  探针 + 频率总线 + 信号缓存 = 非电信息自动化

第 6 阶段（全光）：
  应力张量决定 χ⁽²⁾ → χ⁽²⁾ 决定光逻辑门阈值 = 「晶格光化运算」
  早期晶体质量直接影响中期计算可靠性

第 7-8 阶段（费曼/量子光学）：
  第 6 阶段的激发-湮灭周期 IS 单光子级费曼顶点的宏观系综
  术语直接延续，尺度改变
```

### 3.3 物理结构即模型

```
玩家摆放的方块拓扑
  = 模型架构（网络连接方式）

晶体的参数状态（应力张量、频谱、χ⁽²⁾）
  = 模型权重（通过第 2-3 阶段工艺「训练」进晶体）

光在这个结构中的传播
  = 一次前向推理

光多次迭代通过（类光 diffusion 计算过程）
  = 迭代计算 / 参数细化
```

类比：如同真实世界的光学模拟计算芯片（如 LightOn、Lightmatter），物理介质的结构和光学特性本身就是运算；Minecraft 里玩家摆方块就是在「搭建这个介质」。

### 3.4 信息系统的三条线

```
材料与合成主线（物质线）：
  圆石频谱 → 晶体 → 掺杂 → 凝聚态 → 视界约束材料 → 维度核心

信息与自动化支线（计算线）：
  探针/InfoSignal → 频率总线 → 信号缓存 → 全光计算 → 信息中心
  → 底噪数据库 → 视界控制网络

微观物理后期线（量子线）：
  底噪 → 费曼过程 → 量子光学协处理器 → 视界 → 黑洞 → 维度创世
```

---

## 4. 术语基准（跨文档统一）

### 4.1 能量类型

| 术语 | ID | 含义 | 获取 |
|------|-----|------|------|
| FE（锻造能量） | — | 热力学功；驱动机器 | 原版发电机、燃料 |
| 相干能 | `coherent_energy` | 维持光路相干；承载精密工艺 | 稳谱晶体 + 单频激光源 |

### 4.2 第 6 阶段全光五件套

| 组件 | ID | 功能 |
|------|-----|------|
| 光控制核 | `photonic_control_core` | 全光 FSM；分支/控制/路由/脚本/IO |
| 光协处理器 | `photonic_coprocessor` | 光数据通路；批量搬运/预处理/互连 |
| 光GPU | `photonic_gpu_unit` | MZI 网络；密集矩阵运算 |
| 光脉冲处理器 | `photonic_pulse_processor` | 饱和吸收体；稀疏激活/非线性算子 |
| 光RAM | `photonic_ram_unit` | 受激辐射循环腔；短时状态存储 |

### 4.3 EDA 工艺族

| 工艺族 | 主用途 | 隔离规则 |
|------|------|------|
| 电逻辑 | 早期接口、存储、桥接、低速自动化 | 只能在 `die_domain=electronic` 裸片内承担主逻辑 |
| 光逻辑 | 第 6 阶段主计算，光控制核/光GPU/光RAM | 只能在 `die_domain=photonic` 裸片内承担主逻辑 |
| 量子微逻辑 | 第 8 阶段协处理、采样、蓝图搜索 | 只能在低温/屏蔽的 `die_domain=quantum_photonic` 区域内工作 |
| 桥接芯片 | 电-光、光-量子、量子-经典读出 | 必须显式消耗延迟、噪声、相干能或冷却预算 |

### 4.3 基本操作周期

| 步骤 | 物理过程 | 费曼对应 |
|------|---------|---------|
| 激发（Excitation） | 光子进入晶体共振腔 → 声子模式激活 | 吸收顶点 |
| 传播（Propagation） | 声子模式修改探针光子路径 → 逻辑运算 | 传播子 |
| 湮灭（Annihilation） | 声子弛豫 → 定向释放光子 → 信息输出 | 发射顶点 |

---

## 5. 文档变更日志

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| v0.7 | 2026-06-17 | 新增算力系统与多工艺 EDA 设计基线：电、光、量子微逻辑门作为可选元件库，但以芯片/封装/环境域强制隔离 |
| v0.6 | 2026-06-04 | 主线收束为非电信息路线；删除电气 CPU/GPU/NPU 当前路线；开发计划改为玩法优先，卡玛恩晶体原型前置 |
| v0.5 | 2026-06-04 | 补充第 6 阶段「物理结构即模型」具体玩法；新增核心玩法开发任务计划；补充光RAM 读取衰减默认曲线 |
| v0.4 | 2026-06-03 | 全光架构：电气 CPU → 光控制核，电NPU → 光脉冲处理器，新增光RAM；激发-湮灭基本操作周期；FE/CE 职责分离；物理结构=模型设计原则；费曼桥接章节 |
| v0.3 | 前期 | 光协处理器 + 光GPU + 电NPU 三件套；相干能独立资源；F4 光频协议落地 |
| v0.2 | 前期 | 信息系统核心闭环；数据四分类；模型内外网 |
| v0.1 | 前期 | 圆石频谱 → 卡玛恩晶体 → 掺杂晶体管 → 凝聚态 → 维度创世主线 |

---

## 6. 待规范事项（下一次迭代）

- [x] `Hardware_TechTree_Design.md` §5–6 章核心术语已与新五件套架构对齐
- [x] `Item_Block_Dictionary.md` 的 Stage 6 条目已添加 `photonic_control_core`, `photonic_pulse_processor`, `photonic_ram_unit` 等新 ID
- [x] `Complex_Manufacturing_Process_Reference.md` 中光计算工艺链已更新（卡玛恩非线性介质、光逻辑门、光控制核、光脉冲处理器、光RAM）
- [x] 第 6 阶段「物理结构即模型」的具体玩法机制已在 `Information_System_Design.md` §10.3 补充
- [x] 光RAM 的「读取衰减曲线」已在 `Optical_Computing_Design.md` §8.4 给出默认实现基准
- [x] 新增 `Computing_EDA_Design.md`，把电/光/量子微逻辑门统一为 EDA 工艺族，并规定不同物理环境必须芯片/封装隔离
- [ ] 光RAM 的默认曲线仍需游戏测试后校准具体数值
- [ ] `Item_Block_Dictionary.md` 的 Stage 4-5 条目仍需继续细化 EDA 元件库、桥接器和主板/背板/低温载板条目

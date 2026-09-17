# Kamaen Info

Kamaen Info 是一个面向 Minecraft NeoForge 的科技向模组构想：从圆石的“宽频谱”中提取资源，结晶出卡玛恩晶体，再通过向量爆破、共振调谐、信息读取、掺杂晶片与光路工艺、共振信息自动化、全光计算、世界底噪采样、凝聚态费曼过程、量子光学协处理、人造视界与黑洞信息设备，最终走向参数化维度创世。

当前仓库仍处于早期 MDK/设计阶段，核心玩法和技术路线已整理到文档中，代码实现还未展开。

## 核心循环

```text
圆石分馏
-> 白噪晶种
-> 卡玛恩晶体
-> 向量爆破与力学合成
-> 共振调谐与信息读取
-> 掺杂晶片与光路工艺
-> 共振信息自动化
-> 全光计算
-> 世界底噪采样
-> 凝聚态费曼过程
-> 量子光学协处理器
-> 人造视界
-> 黑洞发电 / 存储 / 运算
-> 维度创世
```

## 文档

- `docs/INDEX.md`：文档导航根节点，记录当前术语基准、阅读路径、设计原则和待规范事项。
- `docs/Kamaen_Info_GDD.md`：整合后的核心 GDD，概述世界观、阶段玩法、信息系统、硬件系统、实现边界和版本路线。
- `docs/Kamaen_Info_TechTree_Plan.md`：完整科技树、资源链、合成框架、配方类型、实现方案和 v0.1-v1.0 路线。
- `docs/Kamaen_Info_Stage_Content_Line.md`：逐阶段物品/方块、参数、传感器、多方块玩法和落地优先级。
- `docs/Kamaen_Info_Item_Block_Dictionary.md`：开发用物品/方块字典，统一 id、组件、BlockEntity 状态和实现备注。
- `docs/Kamaen_Info_Core_Gameplay_Development_Plan.md`：核心玩法开发任务计划，按玩法密度优先规划卡玛恩晶体原型、信息读取、频率总线和最小光学模型。
- `docs/Kamaen_Info_Optical_Computing_Design.md`：第 6 阶段全光五件套规范，包含光控制核、光协处理器、光GPU、光脉冲处理器、光RAM、相干能和费曼桥接。
- `docs/Kamaen_Info_Information_System_Design.md`：信息学模型运行系统概念定稿，重点包括参数/算子、模型内外网、触发任务、路由、传感器、反馈与硬件性能关联。
- `docs/Kamaen_Info_Hardware_TechTree_Design.md`：历史硬件草案，当前主线已转向非电信息网络与全光计算，引用时以 GDD、TechTree 和 Optical_Computing 为准。
- `docs/assets/kamaen_texture_atlas_6x128.png`：已生成的 6 个 128x128 纹理合成预览。

## 已生成纹理

本轮设计产出了 6 个项目内纹理草案：

- `src/main/resources/assets/kamaeninfo/textures/item/item_kamaen_crystal_raw.png`
- `src/main/resources/assets/kamaeninfo/textures/item/item_kamaen_crystal_tuned.png`
- `src/main/resources/assets/kamaeninfo/textures/item/item_info_probe.png`
- `src/main/resources/assets/kamaeninfo/textures/block/block_fractionating_tower_front.png`
- `src/main/resources/assets/kamaeninfo/textures/block/block_explosion_chamber_controller_front.png`
- `src/main/resources/assets/kamaeninfo/textures/block/block_black_hole_parser_core.png`

## 实现方向

建议优先实现玩法最重的“卡玛恩晶体原型闭环”：

1. 用 Data Component 存储晶体的频谱签名、三轴张量、应力、噪声、相干度和专化倾向。
2. 让 `info_probe` 能读取晶体画像，并用 tooltip 或简易 UI 展示差异。
3. 做模拟爆炸室 controller，只计算向量评分，不调用真实大范围爆炸，让玩家能写入/改变晶体属性。
4. 定义 `InfoSignal` 与 `IKamaenReadable` capability，避免默认反射读取任意字段。
5. 实现晶体干涉仪、频率总线、信号缓存片和红石转换模块，形成第一条非电信息自动化链。
6. 后续再扩展分馏塔、I 型合成框架、共振调谐、光路工艺、最小光学模型、底噪采样和凝聚态流程。

## 开发环境

- Minecraft / NeoForge：由 `build.gradle` 与 `gradle.properties` 配置决定。
- Java：Minecraft 1.21.1 目标 Java 21。
- 构建：`gradlew build`
- 刷新依赖：`gradlew --refresh-dependencies`

## 设计约束

- 前期资源产出采用确定性进度加小随机扰动，避免空岛玩家卡死。
- 多方块结构只在变化时重扫，避免每 tick 大范围扫描。
- 爆炸室只做向量矩阵和结构评分，不调用真实大范围爆炸。
- 信息读取统一经过 capability、adapter 和 `IKamaenReadable` 白名单接口。
- 电力只作为机器供能、泵浦、加热和执行器来源，不作为信息传递媒介。
- 模型与算力系统只结算抽象性能画像，不在服务端 tick 内运行真实神经网络。
- 外部 API 是可选扩展，需要延迟、成本、失败、权限、限流、超时和离线 fallback。
- 黑洞装置服务端只计算稳定度、库存、熵流、信息页和封顶能量输出，视觉效果放到客户端粒子。
- 维度创世优先采用预注册模板、数据包配置和参数矩阵，避免早期承诺任意动态维度生成。

## License

See `LICENSE.txt`.

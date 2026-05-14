# Kamaen Info

Kamaen Info 是一个面向 Minecraft NeoForge 的科技向模组构想：从圆石的“宽频谱”中提取资源，结晶出卡玛恩晶体，再通过向量爆破、共振调谐、信息读取、掺杂晶体管、硬件自动化、世界底噪采样、凝聚态费曼过程、人造视界与黑洞信息设备，最终走向参数化维度创世。

当前仓库仍处于早期 MDK/设计阶段，核心玩法和技术路线已整理到文档中，代码实现还未展开。

## 核心循环

```text
圆石分馏
-> 白噪晶种
-> 卡玛恩晶体
-> 向量爆破与力学合成
-> 共振调谐与信息读取
-> 掺杂晶体管与电气合成
-> 硬件自动化
-> 世界底噪采样
-> 凝聚态费曼过程
-> 人造视界
-> 黑洞发电 / 存储 / 运算
-> 维度创世
```

## 文档

- `docs/Kamaen_Info_GDD.md`：整合后的核心 GDD，概述世界观、阶段玩法、信息系统、硬件系统、实现边界和版本路线。
- `docs/Kamaen_Info_TechTree_Plan.md`：完整科技树、资源链、合成框架、配方类型、实现方案和 v0.1-v1.0 路线。
- `docs/Kamaen_Info_Information_System_Design.md`：信息学模型运行系统概念定稿，重点包括参数/算子、模型内外网、触发任务、路由、传感器、反馈与硬件性能关联。
- `docs/Kamaen_Info_Hardware_TechTree_Design.md`：硬件科技树与计算网络设计，重点包括 CPU/GPU/NPU 蓝图、晶振频率协议、主板 I/O、内存页、光纤集群、无线公网和诊断平衡。
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

建议优先实现 v0.1-v0.3 的可玩闭环：

1. 新增 `fractionating` 分馏配方类型与搅拌分馏塔 BlockEntity。
2. 用 Data Component 存储晶体的频谱签名、三轴张量、应力、掺杂、噪声和相干度。
3. 做模拟爆炸室 controller，只计算向量评分，不调用真实大范围爆炸。
4. 定义 `InfoSignal` 与 `IKamaenReadable` capability，避免默认反射读取任意字段。
5. 实现晶体干涉仪、初级探针台、频率总线和红石转换模块。
6. 后续再扩展 I 型合成框架、共振调谐、掺杂晶体管、硬件诊断台、底噪采样和凝聚态流程。

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
- 硬件与模型系统只结算抽象性能画像，不在服务端 tick 内运行真实神经网络。
- 外部 API 是可选扩展，需要延迟、成本、失败、权限、限流、超时和离线 fallback。
- 黑洞装置服务端只计算稳定度、库存、熵流、信息页和封顶能量输出，视觉效果放到客户端粒子。
- 维度创世优先采用预注册模板、数据包配置和参数矩阵，避免早期承诺任意动态维度生成。

## License

See `LICENSE.txt`.

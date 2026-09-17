# 开发工具链

## 当前基底

按 2026-09-10 的决定，**沿用仓库根目录现有工程**：Minecraft 1.21.1、NeoForge 21.1.222、Java 21、Gradle 9.2.1。当前 Java 注册与实现保留，不把 Wiki 的示例实体自动当成游戏功能。

官方 [NeoForge 1.21.1 ModDevGradle MDK](https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle) 克隆于 `.tools/mdk-1.21.1`，固定参考提交 `30cafee9cd8d7f46427ec88fa8579d49c146df9a`。该快照使用 NeoForge 21.1.250、ModDevGradle 2.0.146；当前工程不自动升级或覆盖。Java 要求参见 [1.21.1 官方入门文档](https://docs.neoforged.net/docs/1.21.1/gettingstarted/)。

换机器时可在目标目录尚不存在的情况下恢复工具参考：

```powershell
git clone https://github.com/NeoForgeMDKs/MDK-1.21.1-ModDevGradle .tools/mdk-1.21.1
git -C .tools/mdk-1.21.1 checkout --detach 30cafee9cd8d7f46427ec88fa8579d49c146df9a
gh release download v1.15.3 --repo tryashtar/nbt-studio --pattern NbtStudio.exe --dir .tools/nbt-studio/1.15.3
```

## 配置与入口

`workbench.json` 定义可分享的入口；`local.json` 存储本机路径，已被 Git 忽略。换机器时复制 `local.example.json`，填入实际 Java、Blockbench 和 IDEA 路径。

从 Wiki 的 **开发工作台**（`#/development`）打开 IDEA、Blockbench、NBT Studio、模型源目录、模型/贴图导出目录。入口在本地 Vite 开发服务可用；静态站点不执行桌面程序。桌面桥只允许配置中的入口，不接受网页传入的任意命令或文件路径。

在工程根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\tooling\dev.ps1 doctor
powershell -ExecutionPolicy Bypass -File .\tooling\dev.ps1 build
powershell -ExecutionPolicy Bypass -File .\tooling\dev.ps1 client
powershell -ExecutionPolicy Bypass -File .\tooling\dev.ps1 data
```

可用动作还包括 `server`、`idea`、`blockbench`、`nbt`。Java 21 仅影响此次命令进程，不更改系统默认 Java。客户端/服务端使用工程已有 Gradle 运行配置；首次启动会下载资源。`data` 是否产生内容取决于实际注册的数据生成器。

## 模型与贴图

1. 先定义一个小闭环的用途、注册 ID、获取方式、交互和验收条件。
2. 使用 Blockbench **Java Block/Item** 格式，源工程保存到 `art/models/<name>.bbmodel`。
3. 导出模型 JSON 到 `src/main/resources/assets/kamaeninfo/models/block` 或 `models/item`；PNG 到 `textures/block` 或 `textures/item`。
4. 使用 `kamaeninfo:block/<name>` / `kamaeninfo:item/<name>` 纹理引用，按实际形态补充 blockstates、物品模型、语言和数据文件。
5. Java 注册、交互与制作数据分别实现；运行开发客户端检验显示、碰撞、掉落、交互和保存重载。
6. Wiki 实体以实际注册 ID 关联说明和素材，并记录“设计 / 实现 / 已验证”的证据。当前不自动复制或生成游戏注册代码。

不要直接将 Bedrock geometry 或 PBR 材质导出为 Java 原版模型。先从一个物品或普通方块开始，复杂多方块与动画按需要增加支持。

Blockbench 5.1.4 桌面程序已经配置。检查时本机 `plugins/mcp.js` 为 0 字节，`/bb-mcp` 返回 404；因此 **MCP 建模尚未连通**。普通建模、绘图、保存和导出可直接在桌面进行。之后补充 MCP 时需验证真实工具列表与当前项目，不能把其他服务的 `/health` 当成 Blockbench 连接证明。

## NBT 与数据组件

[NBT Studio 1.15.3](https://github.com/tryashtar/nbt-studio/releases/tag/v1.15.3) 的官方独立程序存放于 `.tools/nbt-studio/1.15.3/NbtStudio.exe`。本次下载 SHA-256：`f3204aad72655af4108cd161f329229b63617b4faf81b17860b499e5b9047eb9`（本地记录，用于复验；上游 Release 未提供 digest）。第三方程序不纳入仓库。

`art/nbt/development-sample.nbt` 是 gzip 压缩、大端序的独立测试样本，旁边的 SNBT 表示其内容。它不属于世界存档，也不定义正式模组数据。

该版本原本依赖 .NET 6，本机未安装。`local.json` 中的 `nbtRollForward: "LatestMajor"` 仅为 NBT Studio 子进程启用运行时兼容启动；已在本机 .NET 10.0.8 下验证启动并显示此 NBT 样本。未修改系统环境，也未对全部编辑功能做兼容性认证。策略依据 [.NET 官方运行时选择说明](https://github.com/dotnet/runtime/blob/main/docs/design/features/framework-version-resolution.md)。

```powershell
node tooling/create-nbt-sample.mjs --check
powershell -ExecutionPolicy Bypass -File tooling/dev.ps1 nbt
```

Minecraft 1.21.1 的物品持久状态需要按实际数据组件 API 设计；NBT 编辑器用于观察序列化结果，不替代 Java 数据组件的注册。正式存档修改使用副本，游戏关闭后操作并在开发世界验证重载。

## 后续第一轮

先从 E1 的第一项可操作内容选一个闭环，依次做需求、注册、贴图/模型、获取与交互、游戏实测、Wiki 回填。此轮仅接通入口和开发工具，不提前冻结第一批美术素材或玩法数值。

## 2026-09-10 验证

- 官方 MDK 提交和干净工作树已核对；当前工程的版本配置保持不变。
- 首次 Gradle 构建遇到 TLS/下载不完整，补齐四个官方依赖并核对上游 SHA-1 与 ZIP CRC 后成功。没有禁用 TLS 校验或更改全局代理。随后通过 `tooling/dev.ps1 build` 再次成功。
- 新产物：`build/libs/kamaeninfo-0.1.0.jar`，183389 字节，SHA-256 `fa847cd6d86ef4174f416a879a101300ea884b0d0ea0da13bfa8d9dca53d5632`。这是当前工作树的开发构建，包含原本未提交的 Java/mixin 改动；本轮没有新增游戏功能。
- Wiki 生产构建通过，13 项自动测试通过，包括桌面桥的固定目标启动、未知入口、任意参数、缺失程序、跨来源及 Host 校验。
- Chrome 验证 8 个入口可检测，320/768/1440 宽度无页面溢出。实际从网页启动 Blockbench 与 NBT Studio；后者窗口已显示测试样本。修正了 GUI 子进程被隐藏的问题。
- 未启动 Minecraft 客户端进行游戏验收；Gradle `test` 当前为 `NO-SOURCE`，不能据构建成功推断玩法已经验证。Blockbench MCP 尚待补装/修复。

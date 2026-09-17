# 模型源文件

在 Blockbench 中选择 **Java Block/Item** 格式。将可编辑项目保存为此目录下的 `<registry_name>.bbmodel`。

导出的游戏模型放入 `src/main/resources/assets/kamaeninfo/models/block/` 或 `models/item/`；PNG 放入同一 namespace 的 `textures/block/` 或 `textures/item/`。纹理引用使用 `kamaeninfo:block/<name>` 或 `kamaeninfo:item/<name>`，不使用绝对路径。

此目录不被 Gradle 打包。不要将 Bedrock geometry、PBR 材质或 Blockbench 工程文件当作 Java 版游戏模型导出。

第一件正式素材留待流程讨论后创建；现有 Wiki 图标仍是展示示例。

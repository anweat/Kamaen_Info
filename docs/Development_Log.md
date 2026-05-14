# Kamaen Info 开发经验记录

本文件用于记录每次较大编辑、环境整理、发布或排障后的提交经验。目标是让后续开发能复用已经踩过的坑和有效流程。

## 2026-05-14：整理 NeoForge 1.21.1 开发环境并发布仓库

### 本次提交

- `a44f55f Initialize Kamaen Info NeoForge project`
- `5ff3b1f Update build workflow actions`

### 做了什么

- 将项目整理为单模块 Minecraft 1.21.1 / NeoForge 21.1.222 工程。
- 补齐 `gradle.properties` 中的 Minecraft、NeoForge、Parchment 和 mod metadata。
- 删除 Gradle init 误生成的 `app` 示例模块、`settings.gradle.kts` 和无用 version catalog。
- 将 MDK 示例注册项替换为 Kamaen Info 的基础占位物品和方块。
- 为已有 PNG 纹理补齐 item model、block model 和 blockstate。
- 整合并更新 README、GDD、License。
- 初始化 git，创建 GitHub 仓库并推送到 `main`。
- 配置 GitHub Actions，使用 JDK 21 构建，并升级到 Node 24 兼容的 action 版本。

### 关键经验

- NeoForge ModDevGradle 的 `createMinecraftArtifacts` 依赖解析不只需要项目级 `repositories`。如果只在 `build.gradle` 加 `mavenCentral()`，NeoFormRuntime 仍可能只搜索 NeoForge Maven，导致 `j2objc-annotations` 等依赖找不到。
- 对 1.21.1 / NeoForge 21.1.222，仓库解析需要覆盖三类来源：
  - Maven Central
  - `https://maven.neoforged.net/releases`
  - `https://libraries.minecraft.net`
- 更稳的写法是在 `settings.gradle` 使用 `dependencyResolutionManagement`，并设置 `RepositoriesMode.PREFER_SETTINGS`。这样 Gradle 不会因为项目级仓库配置把 settings 中的仓库忽略掉。
- 如果在 `settings.gradle` 应用了 `net.neoforged.moddev.repositories`，根 `build.gradle` 里的 `id 'net.neoforged.moddev' version '...'` 可能触发 “already on the classpath with an unknown version” 冲突。解决方式是根工程保留 `id 'net.neoforged.moddev'`，去掉版本号。
- Gradle configuration cache 可能把旧的失败解析结果缓存住。排障时可用 `--no-configuration-cache` 或 `--refresh-dependencies` 区分缓存问题和真实配置问题。
- GitHub Actions 在 2026 年已经开始提示 Node 20 action 弃用。新仓库 workflow 优先使用：
  - `actions/checkout@v6`
  - `actions/setup-java@v5`
  - `gradle/actions/setup-gradle@v6`

### 验证

- 本地执行 `.\gradlew.bat build` 通过。
- GitHub Actions `Build` 工作流通过。

### 后续约定

- 每次进行较大范围文档、工程配置、架构、发布或排障编辑后，都在本文件追加一条记录。
- 记录应至少包含：提交、变更范围、关键经验、验证方式和遗留风险。

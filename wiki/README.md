# Kamaen · 模组发展地图

用于持续讨论模组想法的本地交互 Wiki。总览是一片自由格点画布：独立物品贴图、斜视方块、文字、箭头、线条、虚线框、虚线画笔、3D 空间、2D 模型与自定义渲染可以自由组合。点击实体时，背景变暗，在原位置附近打开图文详情；画布布局保持不动。

当前是可扩展的示例工作稿，材质、机制和结构均待讨论。网页实体注册不等于游戏运行时注册。

## 启动

在 PowerShell 中运行：

```powershell
Set-Location D:\codeproject\mod_project\Kamaen_Info\wiki
npm ci
npm run dev
```

打开 <http://127.0.0.1:4173/#/canvas>。`Ctrl+C` 停止。使用 Node.js 22.12+；端口固定为 4173，冲突时不会静默换端口。

`npm run dev` / `npm run build` 同步 rebuild 阅读资料，并校验注册文件。原始 Mod 代码与 rebuild 文档不会被写回。讨论期间原文更新后执行 `npm run sync` 重新导入；独立注册内容则由开发服务自动监听。

## 自由画布

- 选择“模组发展地图”查看组合示例，或选择“空白自由画布”从零开始；“专注画布”展开至整个视口。
- 点击实体打开原位详情。关联入口在同一窗口继续阅读；点击背景、关闭按钮或按 Escape 返回，焦点回到对象。
- 拖动对象改变位置；选中后的右下角调整大小；齿轮编辑属性。支持小数坐标，不吸附格点、不自动推开其他对象。
- 虚线框与笔迹仅用于标注关系，没有容器或约束语义。箭头和线条可以自由绘制，也可以从对象拖到对象以绑定端点。
- 文字、3D、2D 和自定义渲染从左侧工具栏加入。交互空间内部的旋转、参数控制和滚动不会拖动画布。
- 空白拖动平移，滚轮以指针位置为中心缩放；也可使用平移工具、空格拖动、中键、缩放按钮和整图适配。
- V/H/T/A/L/R/P 对应选择、平移、文字、箭头、线条、虚线框、画笔。Tab 访问对象，方向键移动，Shift 放大步长；尺寸手柄支持方向键。Delete 删除，Ctrl/Cmd+Z 撤销，保留最近 50 次操作。

详见 [交互设计](DESIGN.md)。

## 从文件注册内容

**新增内容的入口是 [content/README.md](content/README.md)。** 复制模板并新建 JSON、Markdown 和资源文件后，组件库、实体总览和实验页面自动出现相应内容，无需修改前端。

| 内容                              | 文件位置                                   |
| --------------------------------- | ------------------------------------------ |
| 物品、方块、多方块、NBT、模型实体 | `content/entities/**/*.json`               |
| 图文说明与材质                    | `content/descriptions/`、`content/assets/` |
| 3D 体素场景                       | `content/scenes/**/*.json`                 |
| 参数、公式与曲线                  | `content/models/**/*.json`                 |
| 独立自定义渲染                    | `content/renderers/**/*.json` + HTML       |
| 自由地图                          | `content/maps/**/*.json`                   |
| 模板与编辑器 Schema               | `content/templates/`、`schemas/`           |

实体使用稳定 ID；地图只记录其引用、位置和尺寸。完整档案、原位详情与其他页面共享实体说明。文件注册支持子目录，并在启动/构建时检查重复 ID、资源路径、关联对象、场景和模型引用。

当前界面同时保留文档阅读、配方与路线、3D 查看、模型实验台、NBT、研究笔记，以及 rebuild 导入物品目录。后者作为既有文档的阅读适配器；新文件实体有自己的命名空间。

## 保存

本地“保存”写回当前地图 JSON；笔记写回 `content/notes.json`。地图用文件内容哈希阻止并发覆盖，外部编辑不增加 revision 也会触发冲突。未保存画布放在浏览器草稿；与文件版本不同时，先提供旧草稿导出，避免直接覆盖文件。

静态构建支持阅读、浏览器草稿和 JSON 导出，没有服务器文件写入。自定义 HTML 使用无同源权限的 sandbox iframe；当前尚无父子共享状态接口。

## 开发工作台

`#/development` 连接现有 Minecraft 1.21.1 / NeoForge 工程、IDEA、Blockbench、NBT Studio 以及模型与贴图目录。使用本地 `npm run dev` 开启桌面入口。工程级设置、PowerShell 命令和制作流程见 [tooling/README.md](../tooling/README.md)；本机程序路径保存在不入库的 `tooling/local.json`。

## 验证

视觉主题与“频率 / 信息积累”的交互约定见 [DESIGN.md](DESIGN.md#视觉与观测节律)。主题在 `src/visual/`，素材、实体和地图继续通过 `content/` 文件扩展。

```powershell
npm run validate:content
npm run build
npm test
```

自动测试与浏览器实测见 [VERIFICATION.md](VERIFICATION.md)。

## 旧版与参考

2026-09-07 的章节团簇方案保留在 `#/legacy-canvas`，布局仍为 `content/canvas.json`；它不再是默认入口。旧交互说明见 [LEGACY_CANVAS.md](LEGACY_CANVAS.md)，旧版开发记录和以撒 Wiki、Patchouli、Ponder 参考链接见 [LEGACY_WIKI.md](LEGACY_WIKI.md)。当前自由地图依据 2026-09-09 的讨论重新构建。

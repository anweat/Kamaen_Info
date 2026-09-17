# 通过文件编写模组档案

此目录是当前自由地图和实体档案的内容源。编辑文件即可注册内容，不必修改 React。开发服务监听新增、修改和删除；生产构建读取同一套文件。`templates/` 仅提供模板，不参与注册。

## 文件如何连接

```text
content/
  entities/*.json       物品 / 方块 / 多方块 / NBT / 模型实体
  descriptions/*.md    实体的图文说明
  assets/*              PNG / SVG / WebP / JPEG 材质与插图
  scenes/*.json         3D 体素、部件和分步讲述
  models/*.json         参数、范围和公式运算树
  renderers/*.json      自定义渲染入口
  renderers/*.html      自包含的交互展示
  maps/*.json           地图、位置、尺寸、文字、笔迹和引用
  templates/            可复制的实体、地图模板
```

注册目录支持子目录。实体文件的 `id` 是引用依据；文件名用于组织，二者不必相同。所有资源、说明、渲染入口路径**相对 content 根目录**，仅 `$schema` 相对当前 JSON 文件。图片在构建时打包，不依赖第三方图片服务。

## 添加一个物品或方块

1. 复制 `templates/entity.json` 到 `entities/your-item.json`，修改唯一 `id`、名称、类型和说明路径。
2. 创建对应的 Markdown 文件。可先使用已有示例图片，之后更换 `visual.asset`。
3. 文件保存后，页面自动重载，新条目进入“物品与方块”和地图组件库。画布已有未保存修改会保留在浏览器草稿中。
4. 从组件库放入地图，或直接在地图 `nodes` 中添加引用：

```json
{
  "id": "sample-on-map",
  "type": "entity",
  "ref": "kamaen:your_item",
  "x": 245.35,
  "y": 180.8,
  "width": 128,
  "height": 150
}
```

`kind` 支持 `item`、`block`、`multiblock`、`nbt`、`model`。方块使用 `visual.type: "block"`，`asset` 为正面，可选 `top`、`side` 指定另外两面；缺省复用正面。`color` 指定占位色。实体存在多个地图实例时，名称和说明仍来自同一个文件。

完整参考：`entities/waveguide-chip.json` 是本轮仅通过文件新增、自动出现在界面的示例；`entities/sample-data.json` 演示 NBT 字段。

## 在说明中组合文字和图片

Markdown 图片用 `![说明](asset:assets/example.png)`，实体链接用 `[晶体](#/entities/kamaen%3Araw_crystal)`。`gallery` 可以再列贴图和图注。`relations` 使用 `{ "target": "kamaen:raw_crystal", "label": "加工来源" }`，在详情里渲染为带贴图的关联入口。

实体可引用 `scene`、`model`、`renderer`。这些内容会同时出现在完整档案和原位弹窗中；地图也能直接放置空间或渲染组件。

## 地图的九种组件

| type    | 主要字段                         | 行为                                  |
| ------- | -------------------------------- | ------------------------------------- |
| entity  | ref                              | 独立物品 / 斜视方块，点击打开图文弹窗 |
| text    | title、body、fontSize、color     | 透明底文字与 Markdown                 |
| arrow   | points、from?、to?、title、color | 箭头；可自由放置，也可跟随端点对象    |
| line    | 同 arrow                         | 无箭头关系线                          |
| rect    | title、color                     | 自由虚线矩形，不限制框内实体          |
| pen     | points、title?、color            | 虚线自由笔迹                          |
| space3d | ref                              | 引用 scenes 中的 3D 场景              |
| space2d | ref                              | 引用 models 中的参数曲线              |
| custom  | ref                              | 引用 renderers 中的独立展示           |

每个组件都有唯一 `id`、`x`、`y`、`width`、`height`。数值使用世界坐标并保留小数，不吸附格点。`points` 相对组件左上角；使用 `from`、`to` 绑定地图组件 ID 时，线端点随目标外框变化。删除被引用组件时，线条保留在删除前的位置并解除相应端点。

复制 `templates/map.json` 到 `maps/` 并修改 ID，就会新增可选择的独立地图。网页“保存”只更新当前地图文件，不写实体说明或原始 rebuild 文档。“导入”载入为当前地图草稿，保存时写回当前地图；新增地图应创建文件。

## 3D 场景和模型

`scenes/impact.json` 展示部件位置、尺寸、颜色和步骤。体素使用 `position: [x,y,z]`，`size` 可选，`step` 从 0 开始并对应 `steps`。支持旋转、剖层、拆解、部件说明和步骤播放。当前实现为体素示意，不包含任意 glTF 导入、NBT 二进制解析或 Minecraft 结构匹配。

`models/response-window.json` 描述坐标范围、参数滑块和公式。`formula` 是展示文字，`expression` 是实际计算的运算树；二者由作者保持一致。支持 `add/sub/mul/div/pow` 双参数与 `sin/exp` 单参数；字符串只能引用已声明参数。无效数值形成曲线缺口，不执行 JavaScript 表达式。

复杂关系展示可复制 `renderers/signal-window.json` 与 `.html`。HTML 在 `sandbox="allow-scripts"` 的 iframe 内运行；没有同源权限，不能访问父页面或共享其状态。代码、样式和依赖应自包含，或使用绝对资源 URL。此接口适用于独立交互展示，尚未提供父子消息协议。

## 校验和版本

编辑器补全 schema 位于 `../schemas/`。`npm run validate:content` 执行真实文件与引用校验；`npm run dev` 和 `npm run build` 也会校验。重复 ID、不存在的资源、关联对象、模型参数或地图引用会显示带文件位置的错误。

本地保存使用内容哈希比较文件版本，即使外部编辑未增加 revision 也会阻止旧网页覆盖。冲突时先导出草稿，刷新读取文件，再合并；浏览器旧草稿不会直接覆盖新文件。静态托管支持浏览器草稿和 JSON 导出，没有服务器文件写入。

这里的“注册”是**网页研究档案注册**。它不注册游戏对象、不修改游戏存档，也不自动产生 Java 注册代码。正式游戏注册可以在后续确定运行时格式后增加单独适配器。

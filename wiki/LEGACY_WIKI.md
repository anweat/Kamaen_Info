# Kamaen · 世界画布

一个用于持续讨论 Mod 想法的本地交互 Wiki。主入口是可平移、缩放的章节画布：物品贴图组成团簇，文字、配方和 3D 结构作为可组合组件。当前都是预填充工作稿，未冻结物品、配方、纹理和多方块形状。

## 启动

要求 Node.js 22.12+（本次使用 24.14.0）。在 PowerShell 中运行：

```powershell
Set-Location D:\codeproject\mod_project\Kamaen_Info\wiki
npm ci
npm run dev
```

打开 <http://127.0.0.1:4173/#/canvas>。终端按 `Ctrl+C` 停止。端口固定且启用 strictPort，不会静默换端口。

`npm run dev` / `npm run build` 会先同步 rebuild 文档和可用示例贴图；不会运行任何旧文档生成脚本，不回写 Mod 源码或 rebuild 文件。讨论期间原文有更新时，执行 `npm run sync` 即可重新导入。

## 画布交互

- 拖动空白处平移；空白处滚轮缩放，工具条也可缩放/适配。组件内部滚轮用于阅读，`Ctrl+滚轮`缩放画布。3D 场景自行处理旋转和缩放。
- 顶部章节按钮定位章节；“整条主线”展示所有贴图团簇；右下缩略图点击定位。
- 拖动组件顶栏移动，右下角调整尺寸；顶栏可展开/收起。移动/缩放手柄支持键盘方向键，组件设置可直接输入宽高。
- 点击贴图，在所属分组下方展开详情；同一团簇一次显示一个物品，不同团簇可各自保留一个。再次点击或点击关闭收起。
- 详情需要空间时，当前组件向下增长，同列下方组件等距推开；收起时恢复。当前组件顶部不移动，连线端点随布局更新。
- 手动缩小组件后，保留设定高度，内部滚动；贴图按宽度自动换行。再次选择物品恢复自动测量。
- 关联指引定位并展开已有团簇中的对象；对象尚未放在画布时，新建一个补充团簇。E1 指引标为“关系示例”；R4 指引来自材料输入/产出关系。
- “组件”新增贴图团簇、文字、配方或 3D 场景；铅笔按钮编辑说明、分组、物品与来源。
- 连线区分发展线和研究反馈。叙事连线不是逐配方依赖证明。
- “撤销”保留最近 30 次操作。“保存”写入项目；“导出”生成 JSON 备份。

## 保存位置

| 内容 | 位置 | 作用 |
| --- | --- | --- |
| 正式画布布局与组件内容 | `content/canvas.json` | 位置、大小、分组、连线及展开物品 |
| 正式研究笔记 | `content/notes.json` | Markdown、阶段、状态、物品/配方/场景引用 |
| 未保存画布草稿 | 当前浏览器 localStorage | 同一服务版本可恢复，项目版本冲突不覆盖 |
| 未保存笔记草稿 | 当前标签页 sessionStorage | 离开笔记页后可恢复；不代替正式保存 |
| rebuild 同步结果 | `src/generated/content.json` | 自动生成，Git 忽略，不手动编辑 |

本地保存端点只允许 `127.0.0.1` 同源请求，使用 revision 防止两个页面覆盖彼此，先写临时文件再原子替换。保存失败保留编辑内容。页面顶部/底部明确显示保存模式与状态。

`npm run build` 生成静态站点。静态托管没有文件写入接口：可以看构建时的画布和笔记，修改保存在浏览器并手动导出。要让多人共同编辑，后续再设计共享服务、权限和合并机制。

## 怎样扩展

1. **新增团簇 / 讲述**：直接在画布添加组件，用设置面板添加分组、选择物品和编辑 Markdown，然后保存。不必修改 React。
2. **写组合笔记**：进入研究记录，添加正文和物品/配方/结构/文档引用。正文中的标准链接如 `[晶种](#/items/e1%3Awhite_noise_seed)` 会渲染为带贴图的行内引用。
3. **新增设计物品**：E1 来源为 `docs/system-rebuild/EARLY_E1_CONTENT.md` 前四个目录表；R4 来源为 `r4-stage-content.json`；后期概念来自 R1 内容映射。修改来源后同步。导入器检查 E1 自述行数、ID 唯一与引用一致性。新结构化来源可在 `scripts/sync-content.mjs` 加适配器。
4. **正式贴图**：在 `src/data.ts` 的 `textureFor` 映射精确条目与材质。无贴图时用 `PixelSprite.tsx` 的原创临时像素轮廓，程序生成的形状和颜色不表达真实物性或等级。
5. **新结构**：在 `src/scenes.ts` 增加场景（部件位置、尺寸、颜色、说明、关联条目和步骤）；即可在结构页与画布组件中选择。不是 Minecraft NBT / 模型 / 碰撞求解器。
6. **新页面类型**：在 `CanvasNode.type`、服务端校验、组件渲染器与设置面板中一起添加；详见 `DESIGN.md`。

当前优先级依据 rebuild 入口：E1/E1.1 组织前期，R4承接中期，R1组织全局。网页中历史资料单独标识。当前机读 R4 配方仍是旧的前期基线，不代表 E1/E1.1 新成本已统一。

## 验证

```powershell
npm run build
npm test
```

测试覆盖源引用、候选配方引用、画布结构与贴图引用、展开/换选/收起的布局回流，以及本地记录校验、原子保存、并发冲突和同源限制。浏览器实测记录见 `VERIFICATION.md`。

## 参考

- [以撒 Wiki 物品目录](https://bindingofisaacrebirth.wiki.gg/wiki/Items)：图像、名称和效果的紧凑组合。
- [以撒 Wiki 的 Brimstone 条目](https://bindingofisaacrebirth.wiki.gg/wiki/Brimstone)：基础机制、组合和交互分层。
- [IsaacGuru Item Laboratory](https://isaacguru.com/item/)：密集图标、聚焦快速说明。仅参考信息交互，不复制其图像或样式。
- [Patchouli 多方块定义](https://vazkiimods.github.io/Patchouli/docs/patchouli-basics/multiblocks/)：数据与展示分离。
- [Create Ponder 场景说明](https://github.com/Creators-of-Create/Create/wiki/Internal---Ponder-UI)：结构加分步讲述；旧版文档只用作概念参考。
- [Three.js Raycaster](https://threejs.org/docs/pages/Raycaster.html)：部件拾取。

最终产品形态按本次讨论采用“章节贴图团簇＋可伸缩画布”，上述网站并未提供这一整套布局实现。

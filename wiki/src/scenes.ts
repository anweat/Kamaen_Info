export type Voxel = {
  position: [number, number, number];
  size?: [number, number, number];
  color: string;
  label: string;
  detail: string;
  step: number;
  ref?: string;
  texture?: string;
};
export type SceneSpec = {
  id: string;
  title: string;
  subtitle: string;
  source: string;
  steps: { title: string; text: string }[];
  voxels: Voxel[];
};
const v = (
  position: Voxel["position"],
  color: string,
  label: string,
  detail: string,
  step: number,
  ref?: string,
  size?: Voxel["size"],
): Voxel => ({ position, color, label, detail, step, ref, size });
const impact: Voxel[] = [];
for (let x = -1; x <= 1; x++)
  for (let z = -1; z <= 1; z++)
    impact.push(
      v(
        [x, 0, z],
        "#718b80",
        "支撑基座",
        "承接靶座与缓冲件。3×3轮廓仅作示意，E1未冻结尺寸。",
        0,
      ),
    );
impact.push(
  v(
    [0, 1, 0],
    "#8ccdc2",
    "待处理晶坯",
    "具有实际生长基材、质量、朝向和母批；不能只靠能量生成晶体。",
    1,
    "e1:raw_kamaen_crystal",
    [0.65, 1.3, 0.65],
  ),
);
impact.push(
  v(
    [-1.1, 1, 0],
    "#d2b884",
    "脉冲源",
    "先充入实际能量，再释放一次有限脉冲。示意不求解冲击波。",
    2,
    undefined,
    [0.8, 0.8, 0.8],
  ),
);
impact.push(
  v(
    [1.1, 1, 0],
    "#91a69c",
    "反射 / 缓冲件",
    "改变源、反射或缓冲位置，比较成型、残余应力与损伤。",
    2,
    undefined,
    [0.35, 1.4, 1.4],
  ),
);
impact.push(
  v(
    [0, 1, -1.2],
    "#d8c5a6",
    "测量工装",
    "用同母批、同温窗复测；记录成功与失败，再决定如何回到生产。",
    3,
    undefined,
    [0.6, 0.8, 0.5],
  ),
);
const rack: Voxel[] = [];
for (const x of [-0.75, 0.75])
  for (const z of [-0.75, 0.75])
    rack.push(
      v(
        [x, 1, z],
        "#6e8278",
        "R04结构立柱",
        "R4候选外形2×2×3；本图以拆解几何表达，非碰撞/合法性检测。",
        0,
        "r4:rack_shell",
        [0.15, 3, 0.15],
      ),
    );
for (const y of [-0.4, 2.4])
  rack.push(
    v(
      [0, y, 0],
      "#86998d",
      "机柜框架",
      "保留前维护通道和实际支撑。",
      0,
      "r4:rack_shell",
      [1.65, 0.18, 1.65],
    ),
  );
rack.push(
  v(
    [0, 1, -0.72],
    "#c2ab7f",
    "供能背板",
    "两个受控输出共享上游额定能力；连接仍需真实线路。",
    1,
    "r4:power_backplane",
    [1.4, 2.4, 0.12],
  ),
);
for (const y of [0.3, 1.4])
  rack.push(
    v(
      [0, y, 0],
      "#acb8a4",
      y === 0.3 ? "A托盘" : "B托盘（空置）",
      "前维护托盘。R04单板节点只在A托盘装一块B01。",
      2,
      "r4:tray",
      [1.4, 0.13, 1.4],
    ),
  );
rack.push(
  v(
    [0, 0.47, 0],
    "#487f6c",
    "B01计算板",
    "八个实体槽位，4096 B工作内存中预留512 B系统空间。",
    2,
    "r4:populated_board",
    [1.15, 0.15, 1.1],
  ),
);
for (let x = 0; x < 4; x++)
  rack.push(
    v(
      [-0.42 + x * 0.28, 0.61, -0.22],
      "#d8c7a5",
      "已封装模块",
      "图中模块仅示意排布；查看B01文档中的具体八槽定义。",
      2,
      "r4:control_chip",
      [0.17, 0.13, 0.25],
    ),
  );
rack.push(
  v(
    [0.72, 1, 0.2],
    "#a7c5bb",
    "风冷模块",
    "实际风路、回流与余热独立存在；此演示不计算热平衡。",
    3,
    "r4:fan",
    [0.13, 0.8, 0.8],
  ),
);
export const scenes: SceneSpec[] = [
  {
    id: "impact",
    title: "从晶坯到第一份响应",
    subtitle: "E1 · 冲击与测量工作站",
    source: "EARLY_E1_GAMEPLAY.md",
    steps: [
      {
        title: "建立支撑",
        text: "先固定工作区。这里采用3×3示意基座，具体多方块尺寸仍待空间原型验证。",
      },
      {
        title: "放置同批晶坯",
        text: "保留一份参考；另一份记录朝向、质量和加工前状态。",
      },
      {
        title: "改变一次冲击",
        text: "只改变源档位、朝向或一处缓冲条件，比较残余结构与损伤。",
      },
      {
        title: "复测并回到生产",
        text: "测量工作窗，选择适合已有设备的晶体；失败残片进入有损回收。",
      },
    ],
    voxels: impact,
  },
  {
    id: "rack",
    title: "一座可维护的计算节点",
    subtitle: "R4 · R04单板机柜",
    source: "R4_HARDWARE_AND_CLUSTER.md",
    steps: [
      {
        title: "搭建框架",
        text: "R04使用2×2×3候选外形，两个前维护托盘。框架本身不提供算力。",
      },
      {
        title: "连接供给",
        text: "背板分配已有供给，两路输出共享预算，不能各自复制一份上游功率。",
      },
      {
        title: "装入B01",
        text: "A托盘安装计算板，B托盘留空。跨柜内存不能直接相加。",
      },
      {
        title: "检查风路与维护",
        text: "运行前验通，持续负载后观察余热，再改善风路。网页只演示部件与步骤。",
      },
    ],
    voxels: rack,
  },
];

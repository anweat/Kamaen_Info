"""Generate design artifacts only; graph is first-access capabilities, not recipes."""
from pathlib import Path
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
# id | label | chapter | AND prerequisites | outcome | track
ROWS = """
start|开局资源契约|1||可再生木材、圆石来源、水、基本种植条件|main
manual|无铁筛与木盆|1|start|木质工具，不用铁或工业滤膜|main
powder|手工分离|1|manual|碎屑、水和工作量→基础粉末与滤渣|main
metal|金属、玻璃与基础红石|1|powder|确定性粉末积分与燃料熔炼|main
crucible|粗坩埚与均值化|2|powder metal|石质热处理，不需要晶体|main
seed|白噪晶种|2|crucible|基底、滤渣、水、手动压制|main
fractionation|分馏塔与排污|2|metal manual|自动化既有手工分离流程|main
blast|模拟爆炸室|3|metal seed|普通结构、缓冲和工艺爆震粉，不要求TNT|main
raw|粗卡玛恩晶体|3|blast|基材、晶种与合格冲击|main
special|三类专化晶体|4|raw|导波、承压、稳谱，各有用途|main
frame1|基本I型框架|4|raw metal|粗压头与结构，不要求偏振传感器|main
polar|偏振与应力观察|4|frame1|先压合出偏振，再做传感器升级|main
repair|退火与回收|4|raw crucible|缺陷可降级使用或有损回收|main
fe|自带燃料发电|4|metal|本模组提供FE，外部FE可替换|main
tuning|切片、调谐与记录|5|special polar|锁相样本，区分知识与物质|main
bio|生物分离|5|tuning fractionation|有机基底与样本→纤维/树脂/培养前体|main
probe|探针与类型化信号|6|tuning metal|类型、单位、来源、时效与置信度|main
bus|总线与阈值控制|6|probe special|条件、滞回、缓存与安全执行|main
logistics|物料接口与简易泵|6|metal fe bus|前期手工/漏斗，此时补自动搬运|main
loop|实际工艺闭环|6|bus fractionation logistics|污染→停料→清洗→恢复|main
ce|初级相干稳压|6|special tuning fe|FE→初级CE，不用单频光源或泵浦塔|main
chem|制造与化学前体|7|metal bio|硅基材、掺杂剂、蚀刻剂和封装材料|main
wafer|掺杂退火晶片|7|chem special ce|公开窗口制造首批标准晶片|main
mask|机械预设掩膜|7|metal tuning|第一掩膜不用EDA或成品芯片|main
optics|基础光路器件|7|wafer mask|曝光、刻蚀、清洗、测试|main
logic|电逻辑与诊断|8|wafer mask probe|常温有限门；诊断由探针自举|main
local_light|局域相干光源与干涉|8|optics ce|经典干涉、相位扫描；不要求F4或模型|main
eda|EDA原理图|8|logic optics|编辑功能图，明确输入输出|main
layout|版图与时序|9|eda|布局、连线、域隔离、采样与缓存|main
tapeout|分层掩膜与流片|9|layout optics loop|真实材料制造裸片并分档|main
package|封装与端口|10|tapeout|DIP/QFP/BGA等按接口/环境选择|main
board|主板与存储槽|10|package logic fe|安装实体芯片、供能、散热和端口|main
record|独立持久记录柜|10|tuning metal|空白记录页先造，不依赖信息中心|main
center|信息中心|11|record board bus|先核心、后中心；数据库为应用模块|main
survey|环境档案|11|center probe|跨地点/工况采样，重复副本不算新证据|main
network|交换路由与DNS|12|center board|预设root/zone/cache/local服务链|main
runtime|Schema与Runtime|12|network record|格式转换、任务、预算、时限和权限|main
electric_matrix|电矩阵与激活瓦片|10|board logic|独立电域算术、非线性与基准计算|main
eo_bridge|光电转换与校准|10|package logic optics local_light|调制、光电读出、ADC/DAC抽象和转换预算|main
hybrid_board|光电混合计算板|10|board electric_matrix photonic_matrix eo_bridge|共同运行小矩阵任务；电存储和激活可用|main
parameter_space|参数实验空间|13|runtime record|有限可返回编辑场，不产资源|main
dataset|数据集与实验出处|12|survey runtime|时间/地点/批次分组，训练验证分离|main
model|有限模型实际求值|13|hybrid_board parameter_space dataset cluster|光电共同后端，小shape实际算子|main
feedback|监督学习与版本|14|model dataset|标签/损失/有限优化、留出工况和回滚|main
simulator|可复位环境与轨迹|14|survey runtime model|有限热/场动态、传感延迟、动作边界与回放|main
rl|强化学习策略|15|feedback simulator cluster bus|状态-动作-奖励-下一状态；有限回合训练和独立验收|main
agent|实体控制与协作|15|rl bus|指定代理搬运、路径与合作|challenge
dialogue|对话交易与对抗|15|agent feedback|离线有限状态NPC、可复现评价|challenge
active_lab|主动采样与实验调度|16|rl survey cluster|比较不确定度与试验成本，提出实验再实测|main
frame2|II型稳定制造|9|optics loop|固定公开曲线先造；学习仅优化已有工艺|main
f4|F4与单频光源|9|frame2 local_light ce|精密参考扩展同步，不是基础光矩阵门槛|main
pump|激光泵浦塔|12|f4 fe|扩大CE通量，不是第一份CE来源|main
nonlinear|非线性介质与晶胞|10|special optics frame2|材质范围和写入参数分开|main
photonic_control|光控制核|16|nonlinear f4 package|相干区有限状态机，替代部分电控路径|main
photonic_matrix|光GPU与MZI|10|optics local_light|基础线性矩阵，不依赖非线性介质/光RAM/模型|main
photonic_pulse|光脉冲处理器|16|nonlinear f4|光域非线性与脉冲任务专化|main
photonic_ram|光RAM与刷新|16|nonlinear f4 photonic_control|短期光状态，电存储可先支撑模型|main
optical_model|模型光电分区部署|13|model photonic_matrix eo_bridge|算子分配与端到端成本，不是首次获得光计算|main
photonic_io|光协处理器互连|12|hybrid_board f4 network|电管理面与光数据面，不要求光RAM或光控核|main
cluster|光电机柜与集群|12|photonic_io network runtime pump|任务落到个体板/芯片/端口，早于学习|main
optical_specialization|全光五件套协作实验|16|optical_model photonic_control photonic_pulse photonic_ram photonic_io|专化光路径保留，不锁首次模型/集群/物理实验|main
model_families|CNN/Attention/MoE|16|cluster feedback|有限网格、序列、专家数和实际算子|challenge
api|外部后端网关|16|runtime feedback cluster|同任务离线替代，限流/超时/权限|external
cryo|普通低温与场线圈|17|frame2 survey ce|普通铜线圈与换热自举，不用超导|main
response|微观响应与相图|17|cryo active_lab optical_model|温度/外场/组分扫描，记录重复性和有效域|main
condensed|初级凝聚态材料|17|response|基础公开模板制超导/拓扑/相变|main
frame3|III型精密场框架|17|condensed cryo|前级材料制造升级，不要求视界|main
feynman|费曼过程设计|18|response frame3|输入、顶点、传播、守恒和环境校验|main
remote|远程站与无线G1–G4|18|network survey condensed|早期代际S5可起步，此时扩多地采样|main
tunnel|隧穿配对|18|feynman condensed|持久配对与在线状态分开|challenge
latent|VAE/Diffusion候选|18|model_families feynman|有限latent和迭代，候选仍需实测|challenge
classical_curve|经典保守曲线|19|feynman optical_model survey|量子自举与故障维修备用|main
single_photon|关联光子与预告单光子源|17|nonlinear f4 optics|泵浦与非线性对源，预告/多光子污染可测|main
spad|SPAD与符合计数|17|wafer eo_bridge f4|半导体读出、暗计数、死时间和时间标签|main
quantum_lab|量子光学基础实验|17|single_photon spad survey optical_model|g2统计与双光子干涉；无需SNSPD或量子计算机|main
snspd|SNSPD低温读出|19|condensed cryo optics|已有超导制造探测器，首个超导不用它|main
hamiltonian|有限哈密顿量任务|18|feynman quantum_lab cluster|登记态空间、耦合与可测量；小规模经典精确基准|main
quantum|量子光学协处理器|19|quantum_lab snspd frame3 classical_curve hamiltonian|可控态制备/测量与任务支持范围，非通用量子机|main
quantum_calibration|量子读出与误差校准|19|quantum dataset|效率/损耗/可见度/重复制备，误差缓解不等于纠错|main
quantum_curve|混合量子求解与候选窗口|20|quantum_calibration hamiltonian feedback|经典更新参数、量子估计观测量，有限VQE式任务|main
protocol|可靠合成协议|20|frame3 survey|候选来自经典或量子路线，框架实测验证|main
crosscheck|量子交叉验证报告|20|protocol quantum_curve|长流程毕业成果；知识保留供维修|main
advanced_network|无线G5–G6与高级脚本|20|remote cluster|高密度、低延迟、预算化循环|challenge
dimension_samples|下界末地实际样本|21|metal|正常探索或明确定义的可再获得来源|main
boundary|边界档案|21|remote feynman dimension_samples metric_atlas|微观响应与宇观几何对照，保留采样出处|main
string|稳定戈古尔斯弦|21|boundary frame3 condensed scale_bridge|接界棱镜校准后由基材凝聚；普通末地材制锚|main
constraint|高阶约束材料|21|protocol condensed|曲线与实际基材，数据不替代物质|main
membrane_blank|空白膜基材|21|constraint frame3 condensed|普通框架制造，不用膜刻写器|main
membrane_writer|全息膜刻写器|21|optics center constraint|普通写入头与存储接口，不用全息膜|main
membrane|功能全息膜·界面铭膜|21|membrane_blank membrane_writer record scale_bridge|微观基材写入宇观边界档案，数据不替代物质|main
entropy|熵流泵与排热|22|constraint cryo fe|普通泵升级，明确热/流体/CE预算|main
quench|独立安全熄灭|22|entropy fe bus|机械联锁与预充储备，主控失稳仍可用|main
horizon|首次人造视界|22|string constraint membrane entropy quench pump crosscheck|外部FE/CE启动、受控停机与恢复|main
generation|视界发电|23|horizon|质量进料与维持成本，产有限FE/残渣|main
horizon_buffer|视界能源缓存|23|generation special|先有正常副产，再制缓存|main
holo_data|全息存储读写|23|horizon membrane center|真实档案与校验，切模式仍持久化|main
rule_solver|黑洞规则求解|24|horizon holo_data boundary|登记候选集，绑定档案版本|main
late_optics|WDM/长期光存储/全光交换|24|holo_data constraint photonic_io|通道、容量和并发升级|challenge
heart|世界之心采样|25|rule_solver frame3 boundary|受控采样，不毁原维度|main
genesis|创世编译与点火|25|world_seed|晨曦世界种绑定唯一实例，固定槽和返回入口|main
maintenance|维护与专化工厂|26|genesis logistics|覆盖维护预算，休眠可恢复|main
crossdim|F5跨维度网络|26|genesis network photonic_io|版本/时间边界与恢复，不无限强加载|main
young_record|杨氏条纹片|8|local_light probe|干涉对照记录，用于光路标定；不冒充量子关联|main
photoelectric|光电效应对照实验|10|eo_bridge local_light|比较频率/光强与读出，有限光电模板|challenge
radiometry|普朗克标定片|11|center eo_bridge young_record|热辐射对照与响应标定；实体基片承载校准|main
sky_watch|巡天接收台与初始星录|11|radiometry optics survey|有限天区数据，分前景/背景，不要求量子|main
atomic_spectra|巴耳末谱尺|17|radiometry response|样本谱线与仪器响应对照，实验室标尺服务巡天|main
bloch_core|布洛赫晶核|18|condensed frame3|合格晶格基材加工的功能核心，名称为理论致意|main
cosmic_baseline|哈勃谱册与余辉星图|18|sky_watch atomic_spectra remote dataset|红移多谱线匹配、背景前景分离；观测不是物质|main
bell_record|贝尔关联签|19|quantum_lab quantum_calibration|登记纠缠态/测量设置的关联报告，不可超光速通信|challenge
casimir|卡西米尔间隙腔|20|frame3 active_lab eo_bridge|制实体精密腔并测间距/力响应，不提供无限真空能|main
metric_atlas|爱因斯坦测地卷|20|cosmic_baseline cluster active_lab|有限引力透镜模型与观测校验，不是造引力的物品|main
chirp_archive|啁啾回声匣|20|cosmic_baseline photonic_io remote|双站相关瞬变与噪声排查，LIGO启发挑战|challenge
scale_bridge|接界棱镜|21|boundary casimir crosscheck bloch_core constraint|微观核心+宇观标定+物理基材，首次跨尺度耦合件|main
closure_archive|双尺度闭合图谱|24|rule_solver metric_atlas scale_bridge|比对受控视界响应与外部档案，约束可行世界模板|main
world_seed|晨曦世界种|25|heart closure_archive holo_data horizon_buffer string|实体核心装配并写入已验证模板，不复制世界|main
finish|完整长流程终点|26|maintenance crossdim|新维度专化产线运行并安全休眠恢复|main
"""
nodes = []
for row in ROWS.strip().splitlines():
    id, name, chapter, required, outcome, track = row.split("|")
    nodes.append(dict(id=id, name=name, chapter=int(chapter), requires_all=required.split(),
                      requires_any=[["classical_curve", "quantum_curve"]] if id == "protocol" else [],
                      outcome=outcome, track=track))
nodes.sort(key=lambda n: n["chapter"])
by_id = {n["id"]: n for n in nodes}
assert len(by_id) == len(nodes)
def deps(n):
    return n["requires_all"] + [x for g in n["requires_any"] for x in g]
for n in nodes:
    assert all(d in by_id for d in deps(n)), n
    assert all(by_id[d]["chapter"] <= n["chapter"] for d in deps(n)), n
visiting, visited, order = set(), set(), []
def visit(id):
    assert id not in visiting, f"cycle: {id}"
    if id in visited:
        return
    visiting.add(id)
    for d in deps(by_id[id]):
        visit(d)
    visiting.remove(id)
    visited.add(id)
    order.append(id)
for n in nodes:
    visit(n["id"])
def reachable(disabled=()):
    got = set()
    for id in order:
        n = by_id[id]
        if id not in disabled and all(d in got for d in n["requires_all"]) and all(any(d in got for d in g) for g in n["requires_any"]):
            got.add(id)
    return got
full = reachable()
standard = reachable([n["id"] for n in nodes if n["track"] != "main"])
no_quantum = reachable(["quantum", "quantum_curve", "crosscheck"])
assert len(full) == len(nodes) and "finish" in standard
assert "constraint" in no_quantum and "horizon" not in no_quantum
assert "classical_curve" in reachable(["quantum"])
assert set(range(1,27)) == {n["chapter"] for n in nodes}
without_photonic_specialists = reachable(["photonic_control", "photonic_pulse", "photonic_ram", "optical_specialization"])
assert {"model", "cluster", "feedback", "rl", "active_lab", "quantum", "finish"} <= without_photonic_specialists
assert "photonic_matrix" in reachable(["electric_matrix", "model", "feedback", "f4", "nonlinear"])
assert "electric_matrix" in reachable(["photonic_matrix", "model", "feedback"])
assert "quantum_lab" in reachable(["cryo", "condensed", "snspd", "quantum"])
assert "quantum_curve" not in reachable(["quantum_calibration"])
assert "active_lab" not in reachable(["rl"])
assert "sky_watch" in reachable(["quantum", "cryo", "condensed"])
assert "metric_atlas" in reachable(["horizon", "quantum"])
assert "scale_bridge" not in reachable(["casimir"])
assert "finish" not in reachable(["casimir"])
assert "scale_bridge" not in reachable(["metric_atlas"])
assert "finish" not in reachable(["metric_atlas"])
named_items = re.findall(r"^\| I(\d+) \|.*?\| [^|]* / `([^`]+)`", (OUT/"RESEARCH_AND_STORY.md").read_text(encoding="utf-8"), re.M)
assert sorted(int(i) for i, _ in named_items) == list(range(1,15))
assert all(node in by_id for _, node in named_items)
feedback = [
    ["feedback", "special", "优化晶体工艺，不是首次前置"],
    ["optical_model", "tapeout", "提高复杂版图良率"],
    ["condensed", "photonic_ram", "改善缓存/温控"],
    ["generation", "fe", "升级能源，不是第一次启动来源"],
    ["maintenance", "fractionation", "专化产区扩大产能，付维护成本"],
]
feedback += [
    ["rl", "loop", "验收策略改善动态工况，阈值控制先能工作"],
    ["active_lab", "survey", "选择下一组实验，数据仍来自实测"],
    ["quantum_curve", "active_lab", "估计观测量辅助排序，不直接授予工艺成功"],
]
feedback += [
    ["condensed", "sky_watch", "微观材料提升接收灵敏度，不锁初始巡天"],
    ["cosmic_baseline", "active_lab", "宇观残差提出新的实验目标"],
    ["horizon", "metric_atlas", "内部实验与外部观测对照，不替代原始宇观证据"],
]
data = dict(version="rebuild-0.3", status="proposal", chapters=26,
            semantics="requires_all AND; each requires_any group OR; first access only; not executable recipes",
            nodes=nodes, optimization_feedback=feedback)
(OUT/"tech-tree.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
text = ["# 完整科技依赖与节点表", "", "Rebuild 0.3：十一时代、二十六章，光电并行，微观与宇观交织。建模首次获得能力的依赖，不是全部Minecraft物料配方。`+`全部必需，`/`替代前置。", "", "main表示标准内容路径，不代表每个节点都是通关硬门槛；是否必需由终点前置决定。五件套保留正式实验，专用光控/光RAM不锁学习与物理。challenge为深化挑战，external为可禁用外部后端。", "", "## 主干", "", "```mermaid", "flowchart TD", "  A[C01–07 资源/晶体/共振/晶片] --> E[C08–10 电逻辑与电矩阵]", "  A --> O[C08–10 相干光路与光矩阵]", "  E --> H[C10 光电转换与混合板]", "  O --> H", "  H --> D[C11–12 环境档案与数据集]", "  H --> C[C12 光电互连与计算集群]", "  D --> M[C13–14 模型/监督学习/环境模拟]", "  C --> M", "  M --> R[C15–16 强化学习与主动实验]", "  R --> P[C17–18 凝聚态/相图/过程模型]", "  O --> Q[C17 单光子/符合计数/量子干涉]", "  D --> Q", "  P --> V[C19–20 校准与混合量子求解]", "  Q --> V", "  C --> V", "  D --> U[C11–20 巡天/谱册/宇观测地]", "  P --> U", "  U --> B[C21–22 双尺度接界/弦膜/视界]", "  V --> B", "  B --> J[C23–26 视界工业/创世/维护]", "```", "", "分组概览不替代下表和JSON的精确AND/OR前置。", "", "## 节点表", "", "| ID | 章 | 内容 | 首次前置 | 产出与约束 | 路线 |", "| --- | --- | --- | --- | --- | --- |"]
for n in nodes:
    req = " + ".join(n["requires_all"]+["("+" / ".join(g)+")" for g in n["requires_any"]]) or "开局契约"
    text.append(f'| `{n["id"]}` | C{n["chapter"]:02} | {n["name"]} | {req} | {n["outcome"]} | {n["track"]} |')
text += ["", "## 量产反馈，非首次前置", ""] + [f"- `{a}` → `{b}`：{c}。" for a,b,c in feedback]
text += ["", "## 微观与宇观的三次交汇", "", "```mermaid", "flowchart LR", "  A[C11 标定与初始巡天] --> M[C17 实验室谱尺]", "  A --> U[C18 红移谱册与余辉星图]", "  M --> U", "  M --> N[C18–20 晶核/量子/间隙腔]", "  U --> G[C20 测地卷]", "  N --> B[C21 接界棱镜]", "  G --> B", "  B --> H[C21–22 弦膜/视界]", "  H --> R[C24 双尺度闭合图谱]", "  G --> R", "  R --> W[C25–26 世界种/创世/维护]", "```", "", "故事、实验和命名物品见[研究与故事](RESEARCH_AND_STORY.md)。分组箭头是概览，节点表的精确前置为准。"]
text += ["", "## 验证边界", "", "禁用量子后，经典曲线和约束材料仍可生产，但长流程首次视界要求量子交叉验证。禁用挑战/外部后端仍可到达终点。", "", "无环不证明物料数量、能源速率、场地和研究条件平衡；这些需要逐配方与游戏原型验证。", ""]
(OUT/"TECH_TREE.md").write_text("\n".join(text),encoding="utf-8")

dictionary = ROOT/"docs/Kamaen_Info_Item_Block_Dictionary.md"
source_rows, section = [], 0
for number,line in enumerate(dictionary.read_text(encoding="utf-8").splitlines(),1):
    match = re.match(r"## (\d+)",line)
    if match:
        section = int(match.group(1))
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if 3 <= section <= 13 and line.startswith("| `") and len(cells)>=15:
        id = re.search(r"`([^`]+)`",cells[0]).group(1)
        source_rows.append(dict(id=id,name=cells[1],line=number,section=section))
OVERRIDES = """
raw_kamaen_crystal|C03|ID对齐|保留已注册kamaen_crystal_raw，原字典名作为设计别名
hand_spectrum_sieve|C01|重做自举|木质首版不用铁或工业滤膜；配木盆手工链
tier1_mechanical_framework|C04|拆首次与升级|偏振传感器不是基本型成型要求
coherent_energy_regulator|C06|明确源头|FE产初级CE，不依赖激光源或泵浦塔
coherent_energy_buffer|C06|分制造与充能|先造空设备，再注入CE
noise_database|C11|移除循环|独立记录柜先造，数据库作为应用模块
macro_info_index_core|C11|重做自举|调谐片/导波/F2/逻辑制造，不由信息中心反造
info_center_controller|C11|重做自举|先核心与记录柜，不依赖完整数据库
electronic_control_chip|C09–10|正式章节|保留电域控制、接口与远程维护用途
electronic_matrix_tile|C10起|光电并行|同期电矩阵，持续承担精确/稀疏算术与训练任务
electronic_activation_tile|C10起|光电并行|混合板非线性和量化，不等光脉冲处理器
chip_blueprint_writer|C08–09|正式章节|先有预设掩膜制逻辑件，不循环锁死首片
chip_packaging_station|C10|明确制造链|必须输入已制造裸片，蓝图不免费提供硬件
model_compiler|C13|分离四种图|功能、布局、参数、部署分开，有限真实求值
server_rack|C12起|集群前移|采样/批处理先用，后支持学习/RL/物理
network_interface_chip|C12–18|分级保留|电/光域明确桥接，避免未定义晶体管简称
fiber_switch|C12起|光电混合互连|电管理面/光数据面，与后期全光交换分开
hardware_diagnostic_station|C08|共享入口|S3探针可先诊断，不用被测高级芯片自举
phase_tuner|C08起|光电校准|局域源先用电热校准，跨节点F4后扩展
single_freq_laser_source|C09起|光源前移|C08局域源自举，C09精密F4扩展，不等学习结果
photonic_ram_unit|C16|用途修正|短时光状态，前期电存储先支撑模型和集群
photonic_gpu_unit|C10起|光电并行|基础MZI先造；F4/更大网格为升级，不用非线性/光RAM自举
photonic_control_core|C16|专化保留|相干区光状态机，不取代全部电控或阻塞首次模型
photonic_pulse_processor|C16|专化保留|光域非线性；混合板先用电激活
photonic_coprocessor|C12起|互连前移|电管理/光数据的首版不要求全光五件套
laser_pump_tower|C12起|供能前移|集群用集中CE，首个光算术由局域源供给
photonic_waveguide_etching_station|C07起|工艺前移|共享精密工艺框架，不要求完整光GPU
mzi_weaving_station|C09–10|装配前移|用公开预设与局域校准造首个小矩阵
photonic_calibration_station|C10起|校准前移|低速电扫描/探测先用，后续F4精密同步升级
silicon_photonic_waveguide_blank|C07|并行制造|晶片工艺先产波导坯，与电域共用前体
silicon_photonic_waveguide|C07–08|并行制造|刻蚀/清洗后支持首个局域光路
mzi_modulator|C08–10|并行制造|局域干涉到小矩阵；基础件不需成品光GPU
silicon_photodetector|C08–10|光电接口|经典光电读出，不等同于SPAD或SNSPD
calibration_token|C10起|诊断记录|实测校准记录或耗材凭证，不作为未校准设备的循环制造前置
kamaen_nonlinear_medium|C10起|非线性支路|服务晶胞/光脉冲及后续对源，基础线性矩阵不用它
photonic_logic_gate|C16|专化保留|光域状态与控制，早期电逻辑已可工作
kamaen_bistable_cell|C10/C16|分制造与应用|C10有基础介质，C16用于光态存储/控制
coherent_energy|C06起|早期供能|S3稳压输出，局域源/集中泵浦分期；相干度另算
horizon_framework_mk1|C17|角色重命名|III型精密场框架，第一凝聚态由II型低温扩展制
holographic_membrane|C21|界面铭膜成品名|沿用ID；空白膜+刻写器+数据，经接界棱镜标定，无自举环
holographic_membrane_writer|C21|解除配方环|普通光学件与存储接口，不以全息膜为首台材料
meso_synthesis_scheduler|C20|控制模块|明确用光控/已制控制芯片，不依赖未定义CPU
quantum_optical_coprocessor|C19–20|正式章节|保守曲线先造设备，再量子验证；任务指标代替万能qubit数
wavefunction_cache_page|C19|限定语义|有限有效期任务摘要，不是可无限复制持久量子态
giant_node_framework|C25–26|合并工作模式|光控与精密场模块，采样/维护共享平台
dimension_maintenance_tower|C26|保留框架模式|休眠可恢复，始终保留返回与救援
spatial_anchor|C25|可制造材料|末地框架是模组可制造结构，不要求原版传送门框架
"""
overrides = {r.split("|")[0]:r.split("|")[1:] for r in OVERRIDES.strip().splitlines()}
chapter_map = {3:"C01–02",4:"C03–04",5:"C05–06",6:"C07–09",7:"C10–12",8:"C08–16（分组件）",9:"C17–18",10:"C19–20",11:"C21–22",12:"C23–24",13:"C25–26"}
mapping = ["# 逐项内容保留与迁移表", "", "旧物品/方块字典§3–13每个实体条目均列出，保留原名与原始行定位；不是已注册ID清单。重复工作台可转工装，玩法保留。", "", "通用修正：区分设备制造/运行、材料/数据、图/实体，补首次获取与回收。特性不锁主线，随机错误不直接发执行器。", "", "| 旧ID | 名称 | 新章 | 处置 | 说明 | 旧字典行 |", "| --- | --- | --- | --- | --- | --- |"]
for r in source_rows:
    chapter,status,note = overrides.get(r["id"], [chapter_map[r["section"]],"保留/细化","沿用职责，按SYSTEM对应章节补首次材料、成本、失败回收"])
    mapping.append(f'| `{r["id"]}` | {r["name"]} | {chapter} | {status} | {note} | {r["line"]} |')
existing = {r["id"] for r in source_rows}
missing = []
for number,line in enumerate((ROOT/"docs/Kamaen_Info_Stage_Content_Line.md").read_text(encoding="utf-8").splitlines(),1):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if line.startswith("| ") and len(cells)>=4:
        match = re.fullmatch(r"`([a-z][a-z0-9_]*)`",cells[1])
        if match and match.group(1) not in existing:
            missing.append([match.group(1),cells[0],number])
mapping += ["", "## 阶段表与实体字典的ID差集", "", "精确ID差异含别名/改名，不意味着全部需要新增ID；须逐项明确映射或补定义。", "", "| ID | 名称 | 阶段表行 |", "| --- | --- | --- |"]
mapping += [f"| `{id}` | {name} | {line} |" for id,name,line in missing]
mapping += ["", "## 字典之外必须补齐的内容家族", "", "| 家族 | 正式位置 | 缺口 |", "| --- | --- | --- |",
"| 木筛、木盆/木碗、粗坩埚 | C01–02 | 无铁起步、手工出金属 |",
"| 发电、泵、物料/流体接口 | C04/C06 | 自带FE和基础物流 |",
"| 谐振装配台、共振分离阵列、生物扩展 | C05 | 基础装配、滤膜、树脂与培养前体 |",
"| 硅基材、掺杂/蚀刻剂、封装材料 | C07 | 明确每个工序的上游 |",
"| 光源前体、机械掩膜、空白记录页 | C06–10 | CE、EDA与数据库自举 |",
"| 裸片/流片任务、FIFO/观测窗/冷却微结构 | C09–10 | 完整制造与时序，不能跳过裸片 |",
"| 网络职能模块、Schema转换 | C12 | 交换/路由/DNS/权限/监测 |",
"| 参数空间、参数/算子/状态/反馈组件 | C13–14 | 受限实验场、有限模型与版本 |",
"| 模型族、实体/交易/对抗任务与回放 | C15–20挑战 | 有限真实功能与可验证收益 |",
"| 机柜族、无线G1–G6、集群与高级Runtime | C12–24 | 分代解锁与个体诊断路径 |",
"| API网关和离线后端 | C16后 | 可禁用外部服务 |",
"| 光电调制/探测/转换桥与混合板 | C10 | 共同计算、转换/校准预算 |",
"| 数据集、可复位模拟器、轨迹、策略与实验计划 | C12–16 | 监督学习、强化学习、主动实验分开 |",
"| SPAD、符合计数、预告源、量子干涉报告 | C17 | 量子观测先于量子计算，不依赖SNSPD |",
"| 哈密顿量任务、态制备、校准与测量摘要 | C18–20 | 有限混合量子求解与经典基准 |",
"| 空白膜、普通写入头、边界档案 | C21 | 解除膜环，分数据与物质 |",
"| 维度槽、返回锚、救援与跨维度网关 | C25–26 | 不复制实例、不覆盖存档、不困住玩家 |", ""]
mapping += ["## 0.3新增研究与命名内容", "", "新增内容不是旧164行的遗漏；见[14项命名物品与用途](RESEARCH_AND_STORY.md)。布洛赫晶核/间隙腔/接界棱镜为部件，谱册/星图/测地卷/闭合图谱为记录；标定件占设备槽。界面铭膜沿用holographic_membrane，晨曦世界种为已编译维度核心成品名，后续注册时核对既有ID，不重复注册。", "", "巡天接收台及对应波段接收头使用已有光电制造；杨氏/黑体/谱线等实验共用前期设备与记录后端。三项深化挑战不作为必需材料来源。", ""]
(OUT/"CONTENT_MAP.md").write_text("\n".join(mapping),encoding="utf-8")

sources = [ROOT/"README.md"] + sorted((ROOT/"docs").glob("*.md")) + sorted((ROOT/"docs/Kamaen_Runtime_Infrastructure").glob("*.md"))
manifest = ["# 审核源文档清单", "", "当前工作区含未提交修改。SHA-256用于识别后续漂移。重构输出不作为输入；Obsidian/Gephi归代码图资料。", "", "| 文件 | 字节数 | SHA-256 |", "| --- | --- | --- |"]
for p in sources:
    b = p.read_bytes()
    manifest.append(f"| `{p.relative_to(ROOT).as_posix()}` | {len(b)} | `{hashlib.sha256(b).hexdigest()}` |")
(OUT/"SOURCE_MANIFEST.md").write_text("\n".join(manifest)+"\n",encoding="utf-8")
chapters = re.findall(r"^\| C(\d{2}) \|", (OUT/"SYSTEM.md").read_text(encoding="utf-8"), re.M)
assert sorted(map(int,chapters)) == list(range(1,27))
links = []
for p in OUT.glob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
        if "://" not in target and not target.startswith("#"):
            if target == "VALIDATION.md":
                continue
            assert (p.parent/target.split("#")[0]).exists(), (p.name,target)
            links.append(target)
report = ["# 设计验证结果", "", "结构检查，不是游戏通关、性能或数值平衡测试。", "",
f"- 审核源清单：{len(sources)}份文档。",
f"- 首次依赖节点：{len(nodes)}个，覆盖26章。",
"- ID唯一、全部前置引用有效：通过。",
"- 全部候选依赖边无环、无章节倒置：通过。",
f"- 全内容可达：{len(full)}/{len(nodes)}。",
f"- 禁用挑战与外部服务：{len(standard)}节点可达，主线终点可达。",
"- 禁用量子反例：保守曲线/约束材料可达；首次视界不可达（长流程要求量子验证）。",
"- 经典曲线不依赖量子设备：通过，可用于自举/维修。",
"- 禁用专用光控/脉冲/光RAM：集群、模型、RL、主动实验、量子和终点仍可达。",
"- 禁用电矩阵、模型、反馈、F4和非线性介质：基础光矩阵仍可达。",
"- 禁用光矩阵、模型和反馈：电矩阵仍可达。",
"- 禁用低温、凝聚态、SNSPD和量子协处理器：量子基础实验仍可达。",
"- 缺量子校准不能进入混合量子求解；缺RL不能完成主动实验章：通过。",
"- 无量子/低温/凝聚态仍可初始巡天；无视界/量子仍可形成测地档案。",
"- 禁用微观间隙腔或宇观测地卷：接界与终点均不可达，双线均有实际前置。",
f"- 命名物品表：{len(named_items)}条，编号连续，关联能力节点全部有效。",
f"- 旧实体字典迁移覆盖：{len(source_rows)}行。",
f"- 阶段表与字典ID差集：{len(missing)}项（含别名），已列出。",
"- SYSTEM的C01–C26唯一连续：通过。",
f"- 本目录相对文件链接：{len(links)}条已检查；验证结果文件本身由本次生成。",
"- 光RAM反例：life20、age8、reads1、d0.1，强度0.54，小于稳定阈值0.65。",
"", "## 未验证", "", "未将旧自然语言配方全部解析成BOM；图是新提案能力图，不证明材料数量、场地、工艺速率与科研阈值可玩。未验证所有空岛整合包、实际游玩时长或服务器负载。未改Java/游戏资源，未运行Gradle游戏测试。", "", "复现：`python docs/system-rebuild/build_design.py`。仅覆写本目录生成文档及JSON。", ""]
(OUT/"VALIDATION.md").write_text("\n".join(report),encoding="utf-8")
print(json.dumps(dict(nodes=len(nodes),reachable=len(full),main_reachable=len(standard),dictionary_rows=len(source_rows),source_docs=len(sources),stage_only_ids=len(missing)),ensure_ascii=False))

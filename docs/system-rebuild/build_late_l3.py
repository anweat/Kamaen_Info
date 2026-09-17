"""Generate the L3 integrated design graph/catalog and finite design checks.

Writes only into docs/system-rebuild. R1 is an input snapshot, not overwritten.
These checks are not Minecraft, full-recipe balance, or GUI validation.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
baseline = json.loads((BASE / 'review-tech-tree.json').read_text(encoding='utf-8'))
nodes = copy.deepcopy(baseline['nodes'])
by_id = {n['id']: n for n in nodes}

NEW = '''
responsive_tool|可部署响应组合|15|package feedback scan runtime|core|以现有器件做作业头/控制模块，按用途选择直接、保持或分步作用
pattern|区域谱纹与制造|16|responsive_tool precision model|core|粗分片先行，双区域结构与实际耦合，再精细复制
field_anchor|作用头与功能锚|16|pattern power|core|实体位置、方向、路径与源，先支持局部可标定作用
field_workshop|织相工场|17|field_anchor runtime scan|core|串行、交叉和并列布局，实际剂量与工件历程
world_slice|世界切片|18|field_workshop sensors model|core|将已能控制的条件组织成可运行区域，支持生产和原版应用
world_reference|可复测远端参照|19|sky spectrum network|core|初始星录/谱尺即可开展，对区域记录提供独立参照
regional_boundary|区域模式与边界关系|21|world_slice noise|core|回响探索、位置与条件对照，得到可用于区域工程的关系
bounded_link|有限特殊链路|22|phase pattern regional_boundary network|extension|实际端点、支持的载荷、容量/时延和在线状态，首版小范围
'''
for line in NEW.strip().splitlines():
    key, title, stage, deps, track, outcome = line.split('|')
    n = dict(id=key, title=title, milestone=f'P{int(stage):02}',
             requires_all=deps.split(), track=track, outcome=outcome)
    nodes.append(n)
    by_id[key] = n

changes = []


def revise(key, deps=None, track=None, outcome=None):
    old = copy.deepcopy(by_id[key])
    if deps is not None:
        by_id[key]['requires_all'] = deps.split()
    if track is not None:
        by_id[key]['track'] = track
    if outcome is not None:
        by_id[key]['outcome'] = outcome
    changes.append(dict(id=key, old=old, new=copy.deepcopy(by_id[key])))


revise('noise', 'network scan model', outcome='分层记录与实际对照；公式/规则基线可用，主动学习是扩展')
revise('cosmic', track='extension')
revise('q_lab', track='extension')
revise('q_cal', 'q_lab model', 'extension')
revise('effective', 'pattern model scan', outcome='有限过程蓝图先服务材料与作用；费曼/振幅按任务展开')
revise('q_prepare', 'q_cal effective', 'extension')
revise('q_hybrid', track='extension')
revise('micro_boundary', 'phase field_workshop precision', outcome='真实材料/区域作用的边界对照，量子方法按任务采用')
revise('cosmic_geometry', 'cosmic model', 'extension')
revise('cross', 'micro_boundary regional_boundary world_reference model',
       outcome='材料、区域与远端参照共同限制边界，产出实体接界组件与知识记录')
for key in ['mode_power', 'mode_store', 'mode_compute']:
    revise(key, track='extension')
revise('advanced_optics', 'optical network store phase',
       outcome='独立持久光介质、WDM与交换；全息膜和短时光RAM按所选实现追加条件，不共绑视界')
revise('closure', 'horizon world_slice cross world_reference cluster hybrid',
       outcome='集群与光电节点整合材料、区域、远端参照及边界运行；三种视界模式按用途扩展')
revise('rules', 'heart effective runtime', outcome='经典有限基线先生成七组参数候选；视界求解可扩大搜索')
revise('genesis', 'rules string store horizon_parts', outcome='资料参与编译，实体基材/控制/锚与储备成核心；普通存储可用')
revise('return_anchor', 'horizon_parts power cross', outcome='在创建新世界之前建成独立返回和救援能力')
revise('dim_gateway', 'bounded_link network string', outcome='先支持已有原版维度的成对服务；新增世界在取得实例后加入')

# B prefixes denote concrete R4/E1 assembly units, not new registered item IDs.
IMPORTS = {
    'B片': '区域处理晶片1片；E1母批/局部特化及R4区域工艺',
    'B构': '金属/绝缘结构件1份；已有熔炼、成型、装配工艺',
    'B光': '相容光路组件1套；已有源/导波/调制中按用途实际选配',
    'B控': '本地控制组件1件；已验证门控/保持或B01能力，按任务实际容量选配',
    'B读': '激励/参考/读出组件1套；已校准的实际测头与接口',
    'B接': '相容接触/导线件1份；电、光、力端口分别选配',
    'B热': '换热/排热组件1件；已有金属热路与实际散热能力',
    'B封': '壳体/密封/绝缘件1份；已有有机与玻璃/金属工艺',
    'B驱': '普通驱动/循环/加载组件1件；E1工艺与电气控制',
    'B介': '净水与普通有机馏分1批；已有净化/分离产物',
    'B存': '持久记录组件1件；R4页载片/普通记录设备，实际容量核算',
    'B储': '普通供能储备接口1套；已有供给/储能，不依赖视界',
    'B末': '可再取得末地类基材1份；已有维度探索与基底加工，非唯一龙蛋',
}

# ID | display name | kind | capability | consumed/contained components | process/requirements | use
# Data and services use persistent storage/computation as conditions, never as consumed information.
CATALOG = '''
response_head|回响作业头|device|responsive_tool|B片:2,B控:1,B读:1,B驱:1,B接:2,B封:1|原工位拼装、用途测试、封装；参照L2.1|生产、工具和移动载具的响应式执行
pattern_wafer|双区域谱纹件|material|pattern|B片:2,B接:1|分片定向/锁定后连接；粗版先行，单片版按区域模板另选工艺|独立区域与耦合作用，后续部件共同基材
memory_pattern|忆形晶片|material|pattern|pattern_wafer:1,B控:1,B接:1|安装写读/保持接口并复测；首版易失，不宣称非易失|状态与材料作用结合
pattern_writer_head|谱纹织构头|device|pattern|B片:1,B驱:1,B读:1,B构:2,B接:2|已有局部作用件和定位夹具组装；不用高级谱纹自举|局部处理与模板复制
pattern_master|谱纹母版|material|pattern|B片:1,B构:1|将已验证区域模板制造成实际可复用工装|批量复制，方案数据另存
field_anchor_part|功能锚|device|field_anchor|pattern_wafer:1,B光:1,B构:2,B接:2|组装指定作用/引导或读出端，测方向与作用核|织相工场及环境作用布置
field_workshop_instance|织相工场实例|assembly|field_workshop|field_anchor_part:2,response_head:1,B控:1,B热:1,B储:1|已取得实体按实际平面/路径安装，清点输入为包含关系|局部或并行工艺，不自动产生任意场
world_slice_instance|世界切片实例|assembly|world_slice|field_workshop_instance:1,B读:1,B驱:1|安装所需环境作用件，装入实际对象；仅重建已能控制条件|条件复现、材料/培育/行为用途
echo_atlas|回响图|data|regional_boundary||实际测站/工具记录按来源汇聚，持久存储另占空间|找位置、追踪现象和指导部署
world_reference_record|远端参照记录|data|world_reference||初始星录和谱尺实测，保留时间/方向/误差|独立参照与跨区域关系
cold_medium|封装冷媒|material|cryo|B介:1,B封:1|普通分离/反应工位与可复用晶体触媒；游戏工质|首套普通低温循环
interface_prism|接界棱镜|material|cross|topological_insulator_crystal:1,pattern_wafer:1,B光:1|按已识别边界工作窗处理并验证，知识不消耗|受限模式耦合
cross_record|互证谱册|data|cross||材料、区域、远端参照的独立记录共同约束|边界解释与适用范围
quasiparticle_lattice|准粒子晶格|material|phase|pattern_wafer:1|C1低温腔与已登记激励/场工艺，源/控制可复用|支持某类可用模式
propagator_plate|传播子片|data|effective||材料模式响应实测/解释记录，须列适用范围|响应核与寿命等模型内容
cooper_pair_seed|库珀对种子|material|phase|B片:2,B接:1|普通C1工位制实体配对态预制件；保持态需工作环境|稳定环前体，不消耗电子数据
feynman_vertex_plate|费曼顶点片|data|effective||过程候选和有效输入输出约束，保存证据版本|有效相互作用卡
feynman_process_blueprint|费曼过程蓝图|data|effective||以记录与受支持过程组合，编译服务检查|过程预测与实际工艺条件
superconducting_kamaen_ring|超导卡玛恩环|material|phase|cooper_pair_seed:1,B构:1,B接:2|普通C1腔内成环/接触与受限低阻态验证；不需视界框架|低温控制与约束材料
topological_insulator_crystal|拓扑绝缘晶体|material|phase|pattern_wafer:1,B封:1|相变工位的场/退火与边缘响应验证|指定模式的隔离/传输
phase_change_memory_crystal|相变记忆晶体|material|phase|pattern_wafer:1,B接:1|相容局部写热/结构工艺，断供读回与循环验证|非易失结构态，与短期保持独立
quasiparticle_filter|准粒子滤波器|device|phase|quasiparticle_lattice:1,topological_insulator_crystal:1,B接:2|带宽/方向与插损标定|选模激励、读出和工艺
tunnel_linker|隧穿链路器|device|bounded_link|topological_insulator_crystal:1,pattern_wafer:1,B控:1,B接:2|两只实际端点分别制造，先用受支持小范围连接；弦锚提供后续升级|保留隧穿串联器/4维电路桥功能变体
cryo_condensation_chamber|低温凝聚腔|device|cryo|B构:4,B封:2,B驱:1,B热:2,B控:1,cold_medium:1|普通循环/密封与排热装配，C1设计目标120K|独立低温工艺，不先需超导或视界
quasiparticle_detector|准粒子捕获器|device|effective|B片:1,B读:1,B光:1,B接:1|指定源/模式/读出配置，使用其实际所需环境|测响应，不捕获抽象传播子实体
feynman_compiler|费曼过程编译台|service|effective||已有节点上的有预算检查/求值服务；专用壳体为可选|统一终端的过程视图
topology_furnace|拓扑相变炉|device|phase|B驱:1,B控:1,B构:2,B热:1,B读:1|既有退火工位加实际场/读出模块，按材料需要接低温腔|相变/边缘通道材料工艺
horizon_framework_mk1|III型框架雏形|assembly|cryo|cryo_condensation_chamber:1,B控:1,B读:1|已独立工作模块的组合配置，不增加免费制冷或相干能力|材料与模式研究工装，不是人造视界
single_photon_source|单光子源|device|q_lab|B片:1,B光:2,B控:1,B接:1|已支持发光/参量源制造与实际状态/计数资格检查|有限量子光任务
initial_counter|初级计数头|device|q_lab|B片:1,B读:1,B控:1,B接:1|精密结区/读出与暗事件、效率、时间标定|首次计数，不依赖SNSPD
snspd_detector|SNSPD探测器|device|snspd|superconducting_kamaen_ring:1,B片:1,B读:1,B接:1|超导材料薄膜/结构加工，工作时接对应低温环境|特定低温计数升级
quantum_optical_coprocessor_core|量子光学协处理核心|device|q_prepare|single_photon_source:1,pattern_wafer:1,B光:4,B控:1|按模板组装实际支持的制备/控制通道；高级低温模块可后装|固定采样与有限态过程分能力声明
cryo_control_plate|低温控制片|device|cryo|B片:1,B控:1,B读:1|测温/控制接口组装及相应环境验证|低温闭环，不从冷却数据直接合成
coherent_control_line|相干控制线|device|q_prepare|superconducting_kamaen_ring:1,B接:2|实际相位/时序传输路径，需材料保持环境|特定低噪控制升级
entanglement_coupler_plate|纠缠耦合片|device|q_prepare|topological_insulator_crystal:1,B光:2,B接:1|支持的态制备工艺和联合测量验证|有限态模板的实体作用组件
wavefunction_cache_page|波函数缓存页|data|q_hybrid||真实存储中的制备指令、任务引用和测量摘要|不携带可复制未知量子态
quantum_error_correction_plate|量子误差校验片|device|qec|superconducting_kamaen_ring:1,B控:1,B读:1|先声明编码/综合征/译码接口，不以数量直接给码距|有明确范围的校验组件
quasiparticle_path_sample|准粒子路径样本|data|effective||实际模式观测与推断的分开记录|有限过程比较，非观察虚粒子轨迹
synthesis_parameter_curve|合成参数曲线|data|effective||经典或相容协处理求值得到候选，经实际试制验收|实际工艺程序的参数内容
meso_synthesis_protocol|中观合成协议|data|effective||把已验收曲线与目标设备接口、范围一起保存|可复用执行协议
quantum_optical_coprocessor|量子光学协处理器|assembly|q_hybrid|quantum_optical_coprocessor_core:1,initial_counter:2,B控:1,B热:1|按能力模板组织路径/计数与经典服务；SNSPD等为升级|受支持统计估计与混合任务
cryo_control_cabinet|低温控制柜|assembly|cryo|cryo_control_plate:1,B控:1,B热:1,B构:2|实际机柜/托盘/连接与热路，接已有低温装置|低温控制与记录
wavefunction_sampler|波函数采样仪|device|q_hybrid|initial_counter:2,B光:1,B控:1|支持测量设置的实体读出；只输出可测统计|过程判别和估计
error_correction_array|误差校验阵列|assembly|qec|quantum_error_correction_plate:2,B控:1,B接:2|有限编码模板实际连线与译码预算；示例份数不承诺码距|编码研究与特定差错处置
meso_synthesis_scheduler|中观合成调度器|service|effective||已有计算节点、持久作业记录和真实工场接口|分发曲线与接收单次执行结果
gorguth_string_residue|戈古尔斯弦残迹|material|string|B片:1,B末:1|用接界工装在已识别区域受限耦合；消耗载体，知识可复用|实体残迹及后续锚定
gorguth_string|戈古尔斯弦|material|string|gorguth_string_residue:1|已有弦锚定器与普通供给稳定载体；维持条件保留|边界作用媒介
horizon_constraint_plate|视界约束片|material|horizon_parts|superconducting_kamaen_ring:1,topological_insulator_crystal:1,B构:1,B接:2|初级版普通连续连接成形，不要求隧穿或完整视界|边界约束与后续部件
entropy_pump|熵流泵|device|horizon_parts|horizon_constraint_plate:1,B驱:1,B热:1,B控:1|前序工位装配并接声明的抽取/回流通道|边界模式的能量/物料路径，非万能熵数值
holographic_membrane|全息信息膜|material|horizon_parts|B片:1,B封:1,B接:1|普通基膜经前序刻写头加工，初始容量保守|实体页载体；高密度由约束工艺升级
hawking_sampler|霍金采样器|device|mode_power|B读:1,quasiparticle_filter:1,B光:1|组装视界公设通道的读出，采样/回收账分开|观测与特定回收接口
penrose_accretion_coil|彭罗斯吸积线圈|device|mode_power|superconducting_kamaen_ring:2,B构:2,B控:1|有实体进料/回流与负载的公设抽取组件|能量转换通道
artificial_horizon_core|人造视界核心|device|horizon|gorguth_string:1,horizon_constraint_plate:2,B构:2|在已组装框架内用普通外部供给成形|同一平台的边界运行实体
emergency_quencher|紧急熄灭器|device|horizon_parts|B驱:1,B控:1,B储:1,B热:1|前序工位装配独立隔离/卸载/储备接口，不先依赖熵流泵|受控降载与停止
string_anchor|弦锚定器|device|string|topological_insulator_crystal:1,B末:1,B控:1,B储:1|前序工位制成并匹配已认识区域；不先消耗戈古尔斯弦|稳定实体残迹
holographic_membrane_writer|全息膜刻写器|device|horizon_parts|B光:2,B控:1,B存:1,B接:1|普通精密刻写头起步，不用成品膜制造首台|膜的写入/读取，高密度为升级
horizon_framework|III型人造视界框架|assembly|horizon|horizon_constraint_plate:4,field_anchor_part:2,string_anchor:1,emergency_quencher:1,B控:1,B热:2,B储:1|安装关系与源/载体成形位置；核心在其中形成，非先拿核心造框架|实际边界装配平台
black_hole_residue|黑洞解析残渣|byproduct|horizon||已运行视界的未转化份额或有损退役载体；按来源账本收料|回收基材，不能返还已转成输出的质量
long_term_photonic_memory|长期光存储单元|device|advanced_optics|phase_change_memory_crystal:1,holographic_membrane:1,B光:2,B控:1|实体光写读存储，保持/刷新/容量分别验证|长期档案层的可选实现
wdm_multiplexer|WDM复用器|device|advanced_optics|B光:4,pattern_wafer:1,B控:1|分波段端口与相容滤波组装，校对串扰/总带宽|多波段传输
all_optical_switch_core|全光交换核|device|advanced_optics|pattern_wafer:2,B光:4,B控:1,horizon_constraint_plate:1|实测非线性开关/相容控制与路由，不替换所有电气节点|可选全光交换服务
horizon_energy_buffer|视界能量缓存|device|horizon|black_hole_residue:1,pattern_wafer:1,B储:1,B封:1|仅在真实残渣取得后制造，充电按实际输入结算|后续储备升级，首台使用普通储备
holographic_data_slice|全息数据片|data|mode_store||实际膜中已写入页的索引/导出，引用实例与版本|页访问或数据副本，占真实容量
entropy_gradient_result|熵梯度结果|data|mode_compute||有限求解器输出候选与约束残差、停止原因|有范围的优化建议
microstate_table|微观态枚举表|data|effective||受支持生成器与真实求值预算，可经典求值|候选空间记录
dimension_rule_candidate|维度规则候选|data|rules||有限规则与用途约束搜索；经典或视界服务均可|可执行范围内的世界参数组合
black_hole_compute_core|黑洞运算核心|device|mode_compute|horizon_constraint_plate:1,B控:1,B存:1,B光:1|普通工位装配视界任务接口，运行时接实际视界|有限求值，不消耗整台视界核心另复制一台
entropy_rectifier|熵差整流器|device|mode_power|entropy_pump:1,B控:1,B热:1|已有抽取通道的升级，和其他输出共用同一输入账|特定能量回收
horizon_cooling_tower|视界冷却塔|assembly|horizon_parts|cryo_condensation_chamber:1,B热:4,B驱:1|已有制冷/换热并联扩展，按实际容量结算|热管理升级，不是首次制冷来源
horizon_address_indexer|视界地址索引器|service|mode_store||实际计算/持久存储上的页映射与提交服务|索引不产生免费容量
world_heart_frequency|世界之心频率|data|heart||材料、区域、远端参照、边界运行与整合采集的特征记录|可再取得的世界描述，不包含整个存档
dimension_parameter_matrix|维度参数矩阵|data|rules||七组受支持参数、来源、约束与不确定范围|创世配置
genesis_blueprint|创世蓝图|data|genesis||世界之心/弦关系/规则候选参与编译，知识不消耗|版本化世界方案
spatial_anchor|空间锚|device|return_anchor|B末:1,horizon_constraint_plate:1,B控:1,B储:1|首版普通储备、母世界独立返回接口，视界电池是升级|真实端点与救援能力
rule_interferometer|规则干涉器|device|rules|interface_prism:1,B读:1,B控:1,holographic_membrane:1|实际已支持条件的读出/约束接口|规则组合的可观测验证
compiled_dimension_core|已编译维度核心|device|genesis|B片:2,horizon_constraint_plate:2,B存:1,B控:1,B储:1|使用已验收蓝图写入实体并预留新实例；数据不当原料|一个绑定实例的世界核心
giant_node_framework|巨型节点框架|assembly|closure|field_anchor_part:4,horizon_constraint_plate:2,B控:2,B存:2,B读:2|前序模块组合并连接实际集群/参照；先有装置再采集世界之心|整合采集与后续维护
genesis_compiler|创世编译台|service|genesis||已有节点执行有预算的检查、预演与实体核心写入作业|视界协处理可选，普通有限基线可用
dimension_ignition_ring|维度点火环|assembly|world|spatial_anchor:2,B构:4,B控:1,B储:2|核心为插入的绑定对象；先检查母世界返回与空闲槽|创建提交和入口，不复制核心
dimension_maintenance_tower|维度维护塔|assembly|maintain|giant_node_framework:1,spatial_anchor:1,B热:1|框架切换维护配置或另造实例，连接已创建世界|分级降载、休眠、恢复与返回
'''
catalog = []
for line in CATALOG.strip().splitlines():
    key, name, kind, cap, raw_inputs, process, use = line.split('|')
    inputs = {}
    if raw_inputs:
        inputs = {a.split(':')[0]: int(a.split(':')[1]) for a in raw_inputs.split(',')}
    catalog.append(dict(id=key, name=name, kind=kind, capability=cap,
                        inputs=inputs, process=process, use=use))
items = {item['id']: item for item in catalog}
ALIASES = {'quantum_coprocessor_core': 'quantum_optical_coprocessor_core',
           'quantum_coprocessor': 'quantum_optical_coprocessor'}

checks = []


def check(name, passed, evidence):
    checks.append((name, bool(passed), evidence))


def reach(excluded=()):
    available = set()
    while True:
        new = {n['id'] for n in nodes if n['id'] not in excluded
               and set(n['requires_all']) <= available}
        if new <= available:
            return available
        available |= new


check('旧能力全部保留且新增ID唯一', len(by_id) == len(nodes)
      and {n['id'] for n in baseline['nodes']} <= set(by_id),
      f"保留{len(baseline['nodes'])}项，当前{len(nodes)}项；包含新增谱纹/场域等能力")
check('首次依赖全部存在', all(dep in by_id for n in nodes for dep in n['requires_all']),
      'requires_all为AND；这里只描述能力，不把整段任务顺序当解锁条件')
check('整合能力图可达且无环', len(reach()) == len(nodes),
      f'{len(reach())}/{len(nodes)}项可从起点取得')
optional = {n['id'] for n in nodes if n['track'] == 'extension'}
check('移除全部可选深化仍能建设并返回新世界', 'maintain' in reach(optional),
      f'排除{len(optional)}项深化，主线仍可达；保留其用途而不要求全收集')
science = {'q_lab','q_cal','q_prepare','q_hybrid','cosmic_geometry',
           'mode_power','mode_store','mode_compute','train','rl','active'}
check('特定量子/透镜/三模式及训练课题不再统一挡住终局',
      'maintain' in reach(science), '材料、区域与远端参照仍需取得，研究手段可选择')
check('移除精密材料或世界参照都会限制边界收束',
      'cross' not in reach({'phase'}) and 'cross' not in reach({'world_reference'}),
      '两侧共同参与，不由单线提供全部终局能力')
check('首套低温和约束件独立于视界及其残渣',
      {'cryo','phase','horizon_parts'} <= reach({'horizon','string','mode_power'}),
      '普通制冷、材料、膜和独立停机可先取得')
check('长期光存储和WDM不统一依赖视界存储',
      'advanced_optics' in reach({'horizon','mode_store','photonic_ram'}),
      '普通持久介质与实际光网络先行；全息版本和RAM版本另列组件条件')
check('所有物件ID唯一且有有效能力去向', len(items) == len(catalog)
      and all(c['capability'] in by_id for c in catalog), f'{len(catalog)}条内容/实例/服务')
check('实物投入都是已定义实体或前期工程份',
      all(key in items or key in IMPORTS for c in catalog for key in c['inputs']),
      f'{len(IMPORTS)}种进口工程份，每种来源在内容表展开')
check('不消耗知识记录合成实体',
      all(key in IMPORTS or items[key]['kind'] not in {'data','service'}
          for c in catalog for key in c['inputs']),
      '资料和工位作为可复用条件，装配部件为实物包含关系')

# Material-only edges must be acyclic. Operating equipment and qualifications
# are explicit process conditions: this does not prove the complete BOM.
made = set(IMPORTS)
while True:
    new = {c['id'] for c in catalog if set(c['inputs']) <= made}
    if new <= made:
        break
    made |= new
check('声明的实物投入图无自我材料循环', set(items) <= made,
      '此项不检查所有工装运行条件；关键首台的工装循环另在正文解释')

source = (ROOT / 'docs/Kamaen_Info_Stage_Content_Line.md').read_text(encoding='utf-8')
late_source = source[source.index('## 8. 阶段七'):source.index('## 13.')]
source_ids = []
for line in late_source.splitlines():
    if line.startswith('|'):
        cells = line.split('|')
        if len(cells) > 3:
            source_ids.extend(re.findall(r'`([a-z][a-z0-9_]+)`', cells[2]))
check('旧阶段七至十一逐ID覆盖含旧别名',
      set(source_ids) <= set(items) | set(ALIASES),
      f'{len(set(source_ids))}个ID含{len(ALIASES)}个旧别名；无删除玩法处理')
late_caps = {n['id'] for n in baseline['nodes'] if int(n['milestone'][1:]) >= 16}
old_entities = baseline['dictionary_entities'] + baseline['stage_only_entities']
old_late = {x['id'] for x in old_entities if x['capability'] in late_caps}
check('R1已登记后期物件也全部有当前去向', old_late <= set(items) | set(ALIASES),
      f'旧字典/额外表映射中的{len(old_late)}项，逐项保留或明确服务化')

# Finite numerical counterexamples for new seams.
def process(events):
    alignment, locked = 0.0, 0.0
    for kind, dose in events:
        if kind == 'A' and locked < 1:
            alignment = min(1, alignment + dose / 4)
        elif kind == 'B' and alignment >= 0.8:
            locked = min(1, locked + dose / 3)
    return alignment, locked


forward, reverse = process([('A',4),('B',3)]), process([('B',3),('A',4)])
check('同总剂量的顺序决定是否锁定', forward == (1,1) and reverse == (1,0),
      f'A4→B3={forward}，B3→A4={reverse}；固定温窗教学投影')
check('同工序划分成多步不额外赠送剂量',
      process([('A',1)]*4 + [('B',1)]*3) == forward,
      '只验证此指定无中途锁定反转的例子，非完整热/力学积分')


def split_energy(emitted, efficiency, weights, loss_weight):
    denom = sum(weights) + loss_weight
    output = [emitted * efficiency * w / denom if denom else 0 for w in weights]
    return output, emitted - sum(output)


delivered, lost = split_energy(20, 0.8, [1,1], 0)
check('并列出口分享同一输入预算', delivered == [8,8] and lost == 4,
      '输入20，两个实际出口各8，损耗4；两个对象不能各拿16')
check('无人占用的出口仍保留传输份额', delivered[0] == 8,
      '另一个出口空置时，其8进入声明终端；不重新按当前工件枚举归一')
check('零路径时能量去向仍完整', split_energy(20, 0.8, [0,0], 0) == ([0,0],20),
      '无有效分配路径，输入全部进入声明源/终端损耗')
pa = 20*0.8*(1+0.9*math.cos(0.7))/2
pb = 20*0.8*(1-0.9*math.cos(0.7))/2
check('相干分配共同计算两个出口', abs(pa+pb-16) < 1e-10 and min(pa,pb)>=0,
      f'PA={pa:.6f}, PB={pb:.6f}, 传输合计16，损耗4')
cop = .2*120/(300-120)
check('C1冷端与热端预算一起成立', abs(6/cop-45)<1e-9 and 6+6/cop==51,
      '冷量6至少输入45，热端排51；能力上限须另外满足')
u,v=3,2
y1,y2=u+v,u+2*v
check('不同响应测头可区分本例两个来源', (2*y1-y2,y2-y1)==(u,v),
      '观测5、7得到u=3、v=2；两个相同测头则不能单独辨识两源')
xx=[math.sin(2*math.pi/4)*math.cos(p) for p in [0,math.pi]]
check('同Z分布可有不同X联合统计', all(abs(a-b)<1e-9 for a,b in zip(xx,[1,-1])),
      '有限态模板θ=π/4、φ=0/π；实际设备支持是额外条件')
check('视界净输出与剩余材料不重复结算', 480+120+4*100==10*100,
      '转化6份→500输出/100热，再支付维护20→净480/热120；4份残留')
check('物理页与逻辑页分别计量', 64//2 == 32,
      '双副本64物理页仅32逻辑页，索引另占空间')
candidates=[dict(name='高产但无通路',score=99,cost=6,access=False),
            dict(name='可建设',score=60,cost=7,access=True),
            dict(name='超预算',score=100,cost=11,access=True)]
valid=[c for c in candidates if c['access'] and c['cost']<=10]
check('世界候选先满足约束再比较目标', max(valid,key=lambda c:c['score'])['name']=='可建设',
      '高分不能绕过通路与预算，未证明全部七组世界规则')


def boundary_eta(detuning, phase, direction=1):
    return .8 * direction**2 / (1 + detuning**2) * (1 + math.cos(phase))/2


boundary_outputs = [10*boundary_eta(0,0), 10*boundary_eta(1,0),
                    10*boundary_eta(0,math.pi/2), 10*boundary_eta(0,0,0)]
check('接界的频差相位和实体方向改变实际传输',
      all(abs(a-b)<1e-9 for a,b in zip(boundary_outputs,[8,4,4,0]))
      and all(0 <= boundary_eta(f,p,d) <= .8
              for f in [-2,0,1] for p in [0,math.pi/2,math.pi]
              for d in [-1,0,.5,1]),
      '指定四设置输出8/4/4/0，输入10；未传出的部分进入声明损耗，不另重扣同一因素')
check('一次相同读数不能唯一反推边界参数',
      abs(boundary_outputs[1]-boundary_outputs[2])<1e-9
      and abs(10*boundary_eta(1,math.pi/2)-10*boundary_eta(0,math.pi))>1,
      '频差与相位两候选最初均读4；追加相位对照后分别读2和0')
loads=[6,7,12,5]
check('平均负荷合格不能掩盖局部约束点超限',
      sum(loads)/len(loads) < 10 and not all(x<=10 for x in loads),
      '平均7.5而第三点12超过上限10，样机拒绝按平均值继续接料')
check('排热不足在同负载下累积而非重置热状态',
      40+16-18 == 38 and 40+16-8 == 48,
      '同初态与发热，排18降到38，排8升到48；仅核单周期预算，非完整停机仿真')
check('新世界附加条件与工场共用实际维护供给',
      2+2+5 <= 10 and 2+2+3+5 > 10,
      '保守静默工场需求9；增局部低载荷需求12，不能由10供给维持；完整适配另验')

manifest = (BASE / 'SOURCE_MANIFEST.md').read_text(encoding='utf-8')
manifest_rows = re.findall(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|', manifest)
intact = len(manifest_rows) == 18
for path, size, digest in manifest_rows:
    data = (ROOT / path).read_bytes()
    intact &= len(data) == int(size) and hashlib.sha256(data).hexdigest() == digest
check('18份原始文档字节不变', intact, '与SOURCE_MANIFEST中的长度和SHA-256比较')

integrated = copy.deepcopy(baseline)
integrated.update(version='L3-integrated-design', late_revision='L3',
                  late_direction='LATE_L3_COMPLETE_GAMEPLAY.md',
                  late_experiments='LATE_L3_WORLD_AND_ENDGAME.md', nodes=nodes,
                  baseline='review-tech-tree.json', changes=changes)
for entity in integrated['dictionary_entities'] + integrated['stage_only_entities']:
    canonical = ALIASES.get(entity['id'], entity['id'])
    if canonical in items:
        entity['capability'] = items[canonical]['capability']
        entity['milestone'] = by_id[entity['capability']]['milestone']
        entity['disposition'] = items[canonical]['process'] + '；用途：' + items[canonical]['use']
catalog_json = dict(version='L3-design-catalog', imports=IMPORTS, items=catalog,
                    aliases=ALIASES, old_source_ids=sorted(set(source_ids)),
                    quantity_semantics='样机工程份；不等于全程原版原料平衡；装配为实物包含，资料/工装条件可复用')
(BASE/'late-l3-tech-tree.json').write_text(json.dumps(integrated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(BASE/'late-l3-content.json').write_text(json.dumps(catalog_json,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# L3整合科技图与首次能力', '',
       '当前设计图由[build_late_l3.py](build_late_l3.py)从R1基线与L3覆盖生成；'
       '前中期已有能力保留，后期首次依赖按连续玩法修订。'
       '机器数据：[late-l3-tech-tree.json](late-l3-tech-tree.json)。', '',
       f'共{len(nodes)}项能力，其中{len(optional)}项可选深化；仍沿用P01—P28索引。'
       '编号用于归档，不是严格完成顺序。core表示主线能力候选，不表示每项必须逐一打卡。', '',
       '**边界：** 检查首次能力依赖，不能证明每一配方、装置操作和玩家任务已可运行。'
       '实物额外条件见[内容表](LATE_L3_CONTENT.md)和专题。R1图保留历史，当前后期以本图为准。', '',
       '| 能力 | 索引 | 名称 | 全部前置 | 路线 | 取得后能做什么 |', '| --- | --- | --- | --- | --- | --- |']
for n in sorted(nodes,key=lambda x:(x['milestone'],nodes.index(x))):
    lines.append(f"| `{n['id']}` | {n['milestone']} | {n['title']} | {', '.join(n['requires_all']) or '开局'} | {n['track']} | {n['outcome']} |")
lines += ['', '## 相比R1/L1改变的首次依赖', '', '| 能力 | 此前前置/路线 | 当前前置/路线 |', '| --- | --- | --- |']
for c in changes:
    lines.append(f"| {c['id']} | {', '.join(c['old']['requires_all'])} / {c['old']['track']} | {', '.join(c['new']['requires_all'])} / {c['new']['track']} |")
lines += ['', '量子、透镜、视界三用途及训练方法均保留，但不统一充当创世前置；'
          '材料边界与实际远端参照继续共同参与收束。特殊链路可先服务已有原版维度，'
          '新世界实例建立后再接入。完整玩法：[L3总稿](LATE_L3_COMPLETE_GAMEPLAY.md)。', '']
(BASE/'LATE_L3_TECH_TREE.md').write_text('\n'.join(lines),encoding='utf-8')

lines=['# L3内容、首次制造与旧稿去向', '',
       '生成源：[build_late_l3.py](build_late_l3.py)；机器目录：[late-l3-content.json](late-l3-content.json)。', '',
       f'共{len(catalog)}条内容，包含材料、组件、装配实例、数据与节点服务，'
       f'覆盖旧阶段七至十一{len(set(source_ids))}个ID（含旧别名）。每一行不等于新增一个注册方块。', '',
       '投入为样机工程份；装配件进入实例的包含关系，不能同时在两台机器使用。'
       '工装、节点服务和知识记录在条件栏复用；后续性能分档/批量配方需实际平衡。', '',
       '## 从E1/R4取得的工程份', '', '| 代号 | 实际来源与计量 |', '| --- | --- |']
lines += [f'| {k} | {v} |' for k,v in IMPORTS.items()]
lines += ['', '## 逐项内容', '', '| ID / 名称 | 类型 / 能力 | 首次投入 | 工序与可复用条件 | 用途 |', '| --- | --- | --- | --- | --- |']
kind_names = dict(material='材料', device='装置', assembly='装配实例',
                  data='资料', service='节点服务', byproduct='副产物')
for c in catalog:
    empty_inputs = '来源由前序实例账本结算；见条件' if c['kind']=='byproduct' else '无消耗性物料；见条件'
    supplies='；'.join(f"{items[k]['name'] if k in items else k}×{v}" for k,v in c['inputs'].items()) or empty_inputs
    lines.append(f"| `{c['id']}` / {c['name']} | {kind_names[c['kind']]} / {c['capability']} | {supplies} | {c['process']} | {c['use']} |")
lines += ['', '## 旧名与共享实体', '']
lines += [f'- `{old}` → `{new}`：保留旧引用为别名，不复制第二套量子设备。' for old,new in ALIASES.items()]
lines += ['- 传播子片、顶点片、波函数页、规则矩阵等按数据管理，不成为消耗性奇异质量。',
          '- 过程编译、曲线调度、索引和初级创世编译优先复用实际节点；已有独立机器外形可保留为封装选择。',
          '- III型雏形、织相工场、控制柜与维护塔是装配/运行配置，重复使用同一实体需先卸载或切换，不免费复制。',
          '- 表中物理输入图无环仅是一项局部检查；低温、首膜/写入、弦锚、熄灭和返回的工装自举详见专题。',
          '- 原18份文档保持原样，原逐ID来源由R1字典映射和阶段内容线保留；本表给当前设计去向。', '']
(BASE/'LATE_L3_CONTENT.md').write_text('\n'.join(lines),encoding='utf-8')

passed=sum(p for _,p,_ in checks)
lines=['# L3设计范围与有限验证', '',
       '运行：`python -X utf8 docs/system-rebuild/build_late_l3.py`。'
       '生成器仅更新本目录中的L3输出，不覆盖R1历史或旧源文档。', '',
       f'结果：**{passed}/{len(checks)}项通过**。', '',
       '| 检查 | 结果 | 证据与范围 |', '| --- | --- | --- |']
lines += [f"| {name} | {'通过' if good else '失败'} | {evidence} |" for name,good,evidence in checks]
lines += ['', '## 完成的设计层', '',
          '- 后期首段、谱纹、空间工艺、世界切片、微观/量子与宇观、边界、视界三用途、世界之心、创世及持续使用均有玩法与用途。',
          '- 每项旧后期ID有去向，实物给首次投入/工序，资料与服务给生成/运行条件；修正明显的材料与首台循环。',
          '- 整合能力图保留前中期与全部旧能力，更新后期首次依赖，注明研究深入项。', '',
          '## 仍未验证的实现层', '',
          '- Minecraft GUI、方块/实体注册、原版行为适配、三维渲染与自动布线。',
          '- 完整热/机械/光场、材料状态到所有响应的函数、全部运行工装条件与首个实际生产存档。',
          '- 样机工程份拆回原版原料的全程数量、耗时、产能、回收与经济平衡。',
          '- 实际量子装置/随机计数、全部维度规则组合、创建事务、多人/区块卸载与返回恢复。',
          '- 玩家试玩与难度节奏；有限例子和图可达不等于游戏已经可通关。', '']
(BASE/'LATE_L3_VALIDATION.md').write_text('\n'.join(lines),encoding='utf-8')
print(f'L3: {len(nodes)} capabilities, {len(catalog)} content entries, {len(set(source_ids))} legacy IDs; checks {passed}/{len(checks)}')
for name,good,evidence in checks:
    if not good:
        print('FAIL:',name,evidence)
if passed != len(checks):
    raise SystemExit(1)

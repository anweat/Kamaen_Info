"""Build R1 review navigation/coverage and validate capability dependencies.

Only writes R1 outputs alongside this script. Does not modify old design sources.
The graph describes capabilities, not complete item-quantity recipes.
"""
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
# id | title | milestone | AND prerequisites | track | observable outcome
ROWS = '''
start|开局条件|1||core|木材、圆石、水、普通燃料与基本种植可达
manual|无铁手筛与木盆|1|start|core|手工分离产出粉末与滤渣
metal|基础金属与玻璃|1|manual|core|累计产出与普通熔炼，不靠稀有抽奖
mean|均值化基底|2|manual metal|core|同批处理后偏差减弱
seed|白噪晶种|2|mean|core|结晶与放置复测，保留参考
raw|带物料来源的粗晶|3|seed metal|core|晶种、生长基材与工艺冲击
stress|力学框架与特化|3|raw metal|core|基本压头先可用，导波抗压稳谱按用途测
power|普通供能|1|metal|core|普通燃料/机械与电能尽早进入；首套产线留供给余量，外部FE可替代
resonance|选择性共振|4|stress metal|core|真实样本与晶体调谐改善合法产物份额
bio|有机分离|4|resonance manual|core|真实有机基底供纤维树脂与培养前体
feedback|信息反馈闭环|5|resonance power|core|探针、类型化信号、滞回、时效与停料恢复
doping|组成特化|6|stress bio feedback|core|母批交叉掺杂与应力试片
precision|模板与工艺控制|7|doping metal|core|粗接触模板先行、退火历史和分档；控制芯片之后反向改进精密工位
electric|电气门控|8|precision power|core|结区、控制端、阈值与低速保持实验
optical|光学相位模块|8|precision resonance power|core|粗源与手动校准，两路组合实验
bridge|光电桥接|8|electric optical|core|调制与探测，转换预算与读出校准
scan|局部扫测与记录|5|stress power|core|固定步进与单域读出先行，记录母批/顺序/量程；完整光电扫测随后整合
eda|实验结构与工程设计|9|scan precision electric|core|已测器件拼接与调谐、有限规则检查；同项目联到制造/实物/模型视图
package|模块封装与制造复制|9|eda precision|core|先封装实际模块，再精密裸片复制；两条材料账与封装后复测
board|集成板|9|package power|core|安装实体芯片与热/供能接口
store|持久记录与内存|10|electric precision|core|空白记录柜先造，四类数据生命周期
runtime|单机运行时|10|board store|core|单节点可承担本地信息中心；有限算子图、记录、预算与回滚
sensors|多点采集与对齐|11|scan store|core|多探头、校准、位置与时间来源；不是首次局部记录的前置
network|联网采集与服务网络|11|runtime sensors|core|实际节点直连与预设服务域，扩展本地信息中心；先单板后按需装柜
sky|初始星录|11|optical sensors|core|基础天区强度与粗谱，不需量子设备
e_matrix|电矩阵|12|electric precision store|core|有限算术阵列与电域基准
o_matrix|光矩阵|12|optical precision store|core|小阵列、编码读出与手动标定
hybrid|混合计算节点|12|e_matrix o_matrix board bridge|core|同任务端到端成本与误差对照
cluster|实际节点集群|12|e_matrix network board|core|电节点可先直连；本地工作集、实际路径、分块与失败恢复
model|小模型与参数|13|runtime scan|core|公式查表与有限预测，首次不等集群
train|监督验证|13|model scan|core|本地有效记录即可开展小批训练/验证；新母批留出、损失、版本和回退
rl|控制基线与策略实验|14|train feedback|core|规则/PID可满足基础闭环；有限Q-learning为深化，保留真实动作与未见扰动验收
active|主动实验|15|train rl scan|core|单工位先按模型分歧/成本选可执行工况并实际测量，多点扩展另接网络
noise|底噪分层与归因|15|active network|core|近远开关对照、相关波动与残差档案
cryo|独立低温工程|16|precision feedback power|core|普通制冷与散热，不依赖超导或视界
phase|凝聚态工作窗|16|cryo model|core|温场相图、各材料用途的独立证据；可用公式/查表基线，不强制监督训练
spectrum|实验室谱尺|17|optical scan model|core|独立参考、多谱线与仪器偏置分离；有限模型校准先行
cosmic|宇观谱图与背景|17|sky spectrum noise|core|红移谱册、对应波段接收头、余辉星图
q_lab|基础量子光学实验|18|optical electric store precision|core|制备源、初级计数头、时间标签与符合扫描
q_cal|量子读出校准|18|q_lab train|core|暗计数、效率、窗口、HOM曲线与统计范围
effective|有效模型与费曼图|19|phase noise model|core|登记自由度、允许顶点、经典小任务基准
q_prepare|任务态制备与测量能力|20|q_cal effective|core|明确所需态与可测算符，拒绝不支持任务
q_hybrid|混合量子交叉验证|20|q_prepare runtime|core|有限期望估计、经典优化、实际试制与曲线
micro_boundary|微观边界对照|21|phase q_hybrid precision|core|有限间隙与表面对照，材料及仪器偏置分离
cosmic_geometry|宇观几何|22|cosmic train|core|多源透镜模板、测地卷与候选区间
cross|独立证据联合标定|23|micro_boundary cosmic_geometry noise|core|互证谱册与实体接界棱镜
string|戈古尔斯弦|23|cross phase power|core|实体载体、受限边界耦合与锚定
horizon_parts|首套约束膜与熄灭器|24|phase precision feedback|core|普通基膜及写入头，独立停机与启动储备
horizon|受控视界|24|string horizon_parts power|core|普通能源启动、降载停机、回收与重启
mode_power|视界发电模式|25|horizon|core|登记质量与净能量账，不重复记账
mode_store|视界存储模式|25|horizon store|core|全息页、校验、持久保留与读回
mode_compute|视界求解模式|25|horizon effective runtime|core|有限候选搜索、可验证输出
closure|双尺度闭合图谱|26|mode_power mode_store mode_compute cosmic_geometry cross cluster hybrid|core|集群与光电互证能力共同组织视界、宇观和底噪记录
heart|世界之心辨识|26|closure sensors|core|可复测世界特征与不确定度，不破坏源世界
rules|维度规则候选|27|heart mode_compute|core|固定种类、七组参数、硬约束与预算
genesis|蓝图与实体核心|27|rules string mode_store|core|有限模板编译、实体资源与唯一实例绑定
return_anchor|母世界返回与救援锚|27|horizon_parts power heart|core|不依赖待创建维度的供能和出口
world|点火与新维度|27|genesis return_anchor|core|使用空闲槽，不覆盖旧世界
maintain|维护休眠与返回|28|world closure|core|实际作业、离开、休眠、恢复、返回与复测
photonic_logic|光逻辑与非线性专化|12|optical precision|extension|非线性介质、逻辑门、双稳态及有限工作域
photonic_control|光控制核|12|photonic_logic runtime|extension|全光FSM与有限控制任务
photonic_ram|短时光RAM|12|photonic_logic store|extension|刷新、寿命与读取扰动
photonic_pulse|光脉冲处理器|12|photonic_logic o_matrix|extension|登记非线性与稀疏任务
photonic_move|光协处理器|12|o_matrix network|extension|光域搬运与路由预算
advanced_network|多DNS与无线分代|15|cluster|extension|G1–G6服务能力与多域解析挑战
bio_policy|培养与物流策略|14|bio rl network|extension|营养/库存/历史与实际任务收益
entity_policy|实体交易与对抗|14|rl runtime|extension|支持代理、离线意图与可重置回放
model_families|模型与架构探索|13|model|extension|先用可运行小图研究结构/状态/算子；训练与规模按任务需要增加，不先要求集群
production_cell|可重组生产单元|11|runtime feedback precision|extension|复用工位/输送/检测，按实际订单排程与分流；模型优化和多线联网按需增加
drone|无人机与移动作业|12|package runtime feedback scan|extension|实际机体、驱动、测头与本地控制，先单机固定航路再学习/协作；不强加载区块
adaptive_gear|计算辅助装备|12|model package feedback precision|extension|工艺/结构优化成果可离线使用；随身主动组件另付硬件、供给与热预算
api|外部后端|15|active runtime|extension|同Schema、成本、时限、验收与离线替代
snspd|低温探测升级|18|phase q_cal|extension|超导探测器用于需要的读出任务
bell|贝尔教学挑战|18|q_cal|extension|明确态制备、多设置与采样假设
boson|玻色采样挑战|20|q_cal optical|extension|固定采样任务，不替代VQE后端
qec|逻辑纠错深化|20|q_prepare phase|extension|显式编码、综合征与译码资源
advanced_optics|长期光存储与WDM|25|mode_store photonic_ram photonic_move|extension|容量、寿命、串扰与全光交换
dim_gateway|跨维度网关|28|world network string|extension|成对锚、服务授权和离线处理
'''

nodes = []
for line in ROWS.strip().splitlines():
    key, title, stage, deps, track, result = line.split('|')
    nodes.append(dict(id=key, title=title, milestone=f'P{int(stage):02}',
                      requires_all=deps.split(), track=track, outcome=result))
by_id = {n['id']: n for n in nodes}
assert len(by_id) == len(nodes), 'duplicate node ids'
assert all(d in by_id for n in nodes for d in n['requires_all']), 'unknown dependency'

def reachable(disabled=()):
    disabled = set(disabled)
    done = set()
    while True:
        new = {n['id'] for n in nodes if n['id'] not in disabled and
               set(n['requires_all']) <= done}
        if new <= done:
            return done
        done |= new

def ancestors(key):
    result = set()
    todo = list(by_id[key]['requires_all'])
    while todo:
        item = todo.pop()
        if item not in result:
            result.add(item)
            todo += by_id[item]['requires_all']
    return result

checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name

check('all_nodes_reachable_and_no_dependency_cycle', len(reachable()) == len(nodes))
check('all_28_milestones_have_core_content', {n['milestone'] for n in nodes if n['track']=='core'} == {f'P{i:02}' for i in range(1,29)})
extensions = {n['id'] for n in nodes if n['track'] == 'extension'}
check('ending_reachable_without_extensions_or_external_api', 'maintain' in reachable(extensions))
check('small_model_without_cluster', 'model' in reachable({'cluster','hybrid','e_matrix','o_matrix'}))
check('ordinary_power_before_crystal', by_id['power']['milestone']=='P01' and 'power' in reachable({'seed','raw','stress'}))
check('local_scan_without_optics_or_cpu', 'scan' in reachable({'optical','bridge','electric','runtime'}))
check('electric_runtime_without_optical_branch', 'runtime' in reachable({'optical','bridge','o_matrix','hybrid'}))
check('local_training_without_multisite_or_network', 'train' in reachable({'sensors','network','cluster'}))
check('local_active_experiment_without_multisite', 'active' in reachable({'sensors','network','cluster'}))
check('architecture_exploration_without_cluster_or_training', 'model_families' in reachable({'cluster','train'}))
application_nodes = {'production_cell','drone','adaptive_gear'}
check('applications_have_local_non_ml_entry', application_nodes <= reachable({'train','cluster','hybrid'}))
check('late_branches_do_not_require_applications', {'phase','cosmic','q_cal'} <= reachable(application_nodes))
check('electric_matrix_without_optical_matrix', 'e_matrix' in reachable({'o_matrix'}))
check('optical_matrix_without_electric_matrix', 'o_matrix' in reachable({'e_matrix'}))
check('hybrid_requires_both_matrices', 'hybrid' not in reachable({'e_matrix'}) and 'hybrid' not in reachable({'o_matrix'}))
check('first_cluster_without_optical_matrix_or_hybrid', 'cluster' in reachable({'o_matrix','hybrid'}))
check('initial_sky_without_quantum_or_cryo', 'sky' in reachable({'q_lab','cryo'}))
check('material_windows_without_training_or_astronomy', 'phase' in reachable({'train','sky','spectrum','cosmic','q_lab'}))
check('lab_spectral_reference_without_training_or_cryo', 'spectrum' in reachable({'train','cryo','phase','q_lab'}))
check('quantum_lab_without_cryo_or_snspd', 'q_cal' in reachable({'cryo','snspd'}))
check('quantum_hybrid_requires_calibration_and_task_preparation', 'q_hybrid' not in reachable({'q_cal'}) and 'q_hybrid' not in reachable({'q_prepare'}))
check('cross_requires_micro_and_cosmic_independently', 'cross' not in reachable({'micro_boundary'}) and 'cross' not in reachable({'cosmic_geometry'}))
check('initial_horizon_without_its_own_outputs', 'horizon' in reachable({'mode_power','mode_store','mode_compute'}))
check('ending_requires_independent_return_anchor', 'maintain' not in reachable({'return_anchor'}))
check('all_three_modes_in_core_closure', {'mode_power','mode_store','mode_compute'} <= ancestors('closure'))
check('ending_visits_all_core_capabilities', {n['id'] for n in nodes if n['track']=='core'} == ancestors('maintain') | {'maintain'})

def chapter_for(section):
    return {3:'P01–02',4:'P03',5:'P04–05',6:'P06–09',7:'P09–15',
            8:'P08/P12',9:'P16/P19/P21',10:'P18–20',11:'P23–24',
            12:'P25',13:'P26–28'}[section]

# Each entity is tied to a real capability, not merely a blanket "retained" flag.
groups = {
 'manual':'crude_spectrum_scrap crude_spectrum_slurry spectrum_slag spectrum_powder spectrum_membrane hand_spectrum_sieve fractionating_tower',
 'mean':'whitened_cobblestone thermal_noise_crucible basic_spectroscope',
 'seed':'white_noise_seed',
 'raw':'blast_powder ideal_rigid_plate buffer_sand_layer target_pedestal raw_kamaen_crystal kamaen_crystal_debris explosion_chamber_controller',
 'stress':'waveguide_kamaen_crystal compression_kamaen_crystal stable_spectrum_kamaen_crystal polarized_kamaen_crystal stress_recording_plate stress_sensor axial_press_head tier1_mechanical_framework',
 'resonance':'tuning_wafer intrinsic_spectrum_sample resonance_catalyst_crystal spectrum_phaselocker tuning_array',
 'feedback':'information_unit frequency_bus frequency_to_redstone_module kamaen_probe_station',
 'optical':'crystal_interferometer silicon_photonic_waveguide_blank silicon_photonic_waveguide mzi_modulator phase_tuner single_freq_laser_source calibration_token photonic_waveguide_etching_station',
 'doping':'kamaen_crystal_t2 kamaen_dopant kamaen_wafer ion_implanter',
 'electric':'kamaen_pn_junction electronic_logic_gate',
 'precision':'lithography_mask process_protection_kit lattice_annealing_furnace lithography_projector etching_tank tier2_optical_process_framework',
 'eda':'lithography_mask_set timing_structure_cell eda_module_plate chip_blueprint_writer',
 'bridge':'crystal_interconnect silicon_photodetector',
 'package':'chip_packaging_station packaged_logic_chip',
 'board':'motherboard_blueprint configurable_motherboard electronic_control_chip hardware_diagnostic_station',
 'power':'kamaen_oscillator coherent_energy_buffer coherent_energy_regulator coherent_energy laser_pump_tower',
 'e_matrix':'electronic_matrix_tile electronic_activation_tile',
 'store':'memory_page storage_center_controller',
 'network':'network_interface_chip fiber_switch macro_info_index_core noise_database info_center_controller',
 'sensors':'sensor_hub world_noise_sample noise_spectrometer thermodynamic_antenna',
 'runtime':'model_component_gateway model_compiler',
 'cluster':'server_rack',
 'noise':'thermal_noise_plate radiation_noise_plate quantum_fluctuation_plate chunk_entropy_record entropy_flow_meter',
 'photonic_logic':'kamaen_nonlinear_medium photonic_logic_gate kamaen_bistable_cell',
 'photonic_control':'photonic_control_core',
 'photonic_move':'photonic_coprocessor',
 'o_matrix':'photonic_gpu_unit mzi_weaving_station photonic_calibration_station',
 'photonic_pulse':'photonic_pulse_processor',
 'photonic_ram':'photonic_ram_unit',
 'phase':'quasiparticle_lattice cooper_pair_seed superconducting_kamaen_ring topological_insulator_crystal phase_change_memory_crystal quasiparticle_filter topology_furnace',
 'effective':'propagator_plate feynman_vertex_plate feynman_process_blueprint quasiparticle_detector feynman_compiler quasiparticle_path_sample',
 'cryo':'cryo_condensation_chamber horizon_framework_mk1 cryo_control_plate cryo_control_cabinet',
 'q_prepare':'quantum_optical_coprocessor_core entanglement_coupler_plate coherent_control_line',
 'q_hybrid':'wavefunction_cache_page synthesis_parameter_curve meso_synthesis_protocol quantum_optical_coprocessor wavefunction_sampler meso_synthesis_scheduler',
 'qec':'quantum_error_correction_plate error_correction_array',
 'string':'gorguth_string_residue gorguth_string string_anchor tunnel_linker',
 'horizon_parts':'horizon_constraint_plate entropy_pump holographic_membrane emergency_quencher holographic_membrane_writer horizon_framework',
 'horizon':'artificial_horizon_core',
 'mode_power':'penrose_accretion_coil hawking_sampler black_hole_residue horizon_energy_buffer entropy_rectifier horizon_cooling_tower',
 'mode_store':'holographic_data_slice horizon_address_indexer',
 'mode_compute':'entropy_gradient_result microstate_table black_hole_compute_core',
 'rules':'dimension_rule_candidate dimension_parameter_matrix rule_interferometer',
 'heart':'world_heart_frequency giant_node_framework',
 'genesis':'genesis_blueprint compiled_dimension_core genesis_compiler',
 'return_anchor':'spatial_anchor',
 'world':'dimension_ignition_ring',
 'maintain':'dimension_maintenance_tower',
}
entity_nodes = {}
for cap, ids in groups.items():
    assert cap in by_id
    for key in ids.split():
        assert key not in entity_nodes, key
        entity_nodes[key] = cap

notes = {
 'hand_spectrum_sieve':'重做首版：木筛不需铁；金属筛再升级',
 'raw_kamaen_crystal':'旧设计别名，注册对齐kamaen_crystal_raw；必须加生长基材',
 'white_noise_seed':'平均背景初始结晶；结构质量与中性分开',
 'kamaen_crystal_t2':'用途检验/工艺资格，不是全属性统一升级',
 'coherent_energy':'保留资源表现；能量、参考稳定度、相干条件分开',
 'laser_pump_tower':'集中规模升级；初版光源不依赖这座塔',
 'single_freq_laser_source':'精密版保留；粗源/手动校准先于F4规模系统',
 'noise_database':'空白载体先造，数据库为应用；记录x16不作为研究点门槛',
 'quantum_fluctuation_plate':'量子解释未成立时只标候选残差，不能直接测得任意真值',
 'entropy_flow_meter':'区块活动代理指标与热力学熵区分',
 'cooper_pair_seed':'实体态预制件，需基材和环境；不能用两张记录变物质',
 'propagator_plate':'响应/模型数据，不是可装袋物理传播子',
 'horizon_framework_mk1':'低温材料框架雏形，不产生视界',
 'tunnel_linker':'局部耦合用途可早于视界；远程/跨维度作用移入边界公设与成对锚',
 'wavefunction_cache_page':'制备/任务/测量摘要；不是未知量子态复制页',
 'wavefunction_sampler':'可测统计与校准风险，不能暴露任意波函数',
 'quantum_optical_coprocessor':'按任务能力区分玻色采样与变分制备/测量，不互相冒充',
 'quantum_error_correction_plate':'先诊断校验；逻辑纠错要求编码、综合征和译码',
 'error_correction_array':'方块数量不足以单独证明码距与逻辑纠错能力',
 'holographic_membrane_writer':'普通头/空白膜自举，视界高容量版后升级',
 'black_hole_residue':'只回收未转换预算，不重复返还已输出能量对应质量',
 'horizon_energy_buffer':'后期储备升级，不作为首次视界启动前置',
 'world_heart_frequency':'受控可复测的世界特征记录，不毁掉母世界',
 'compiled_dimension_core':'晨曦世界种候选显示名，复制引用不复制世界实例',
}
dictionary = ROOT/'docs/Kamaen_Info_Item_Block_Dictionary.md'
entities=[]
section=0
for i, line in enumerate(dictionary.read_text(encoding='utf-8').splitlines(), 1):
    match=re.match(r'## (\d+)\.',line)
    if match: section=int(match.group(1))
    if not 3 <= section <= 13 or not line.startswith('| `'): continue
    cells=[x.strip() for x in line.split('|')[1:-1]]
    key=cells[0].strip('`')
    assert key in entity_nodes, f'unmapped dictionary entity: {key}'
    cap=entity_nodes[key]
    entities.append(dict(id=key,name=cells[1],source_line=i,capability=cap,
                         milestone=by_id[cap]['milestone'],old_section=section,
                         role=cells[4],disposition=notes.get(key,'保留原有用途；首次能力与量产升级分开，按对应发展线修订配方。')))
check('dictionary_all_164_rows_mapped',len(entities)==164)
check('dictionary_unique_ids',len({x['id'] for x in entities})==len(entities))
check('no_mapping_for_nonexistent_dictionary_item',set(entity_nodes)=={x['id'] for x in entities})

extras_groups={
 'precision':'doped_waveguide_wafer kamaen_threshold_filter phase_tuning_chip',
 'bridge':'kamaen_detector_junction crystal_waveguide_line',
 'scan':'info_diagnostic_station',
 'store':'resonant_signal_cache signal_cache_plate',
 'network':'frequency_route_plate',
 'photonic_logic':'kamaen_nonlinear_medium_station photonic_gate_assembly_station bistable_cell_assembly_station',
 'photonic_control':'photonic_control_core_assembly',
 'photonic_pulse':'photonic_pulse_processor_assembly',
 'photonic_ram':'photonic_ram_assembly',
 'q_lab':'single_photon_source',
 'snspd':'snspd_detector',
 'advanced_optics':'long_term_photonic_memory wdm_multiplexer all_optical_switch_core',
}
extra_map={key:cap for cap,ids in extras_groups.items() for key in ids.split()}
extras=[]
for i,line in enumerate((ROOT/'docs/Kamaen_Info_Stage_Content_Line.md').read_text(encoding='utf-8').splitlines(),1):
    if not line.startswith('|'): continue
    cells=[x.strip() for x in line.split('|')[1:-1]]
    if len(cells)<4 or not cells[1].startswith('`'):continue
    match=re.match(r'`([^`]+)`',cells[1])
    if not match:continue
    key=match.group(1)
    # Stage table also labels an existing item's variant as `kamaen_oscillator (F4)`.
    if key == 'kamaen_oscillator (F4)': key = 'kamaen_oscillator'
    if key in entity_nodes:continue
    if key in extra_map:extras.append(dict(id=key,name=cells[0],source_line=i,capability=extra_map[key]))
    else:raise AssertionError(f'unmapped stage-only entity {key}')
check('stage_only_20_rows_mapped',len(extras)==20 and len({x['id'] for x in extras})==20)
check('exact_stage_extra_mapping',set(extra_map)=={x['id'] for x in extras})

source_rows=re.findall(r'^\| `([^`]+)` \| (\d+) \| `([a-f0-9]+)` \|$',(BASE/'SOURCE_MANIFEST.md').read_text(encoding='utf-8'),re.M)
drift=[]
for name,size,digest in source_rows:
    raw=(ROOT/name).read_bytes()
    if len(raw)!=int(size) or hashlib.sha256(raw).hexdigest()!=digest:drift.append(name)
check('18_original_sources_unchanged',len(source_rows)==18 and not drift)

data=dict(version='R1-review',stage_revision='R4',stage_design='R4_STAGE_DESIGN.md',progression_review='EARLY_MID_REVIEW_AND_LATE_ENTRY.md',application_design='MIDGAME_APPLICATIONS.md',late_revision='L1',late_direction='LATE_L1_DIRECTION_AND_RESEARCH.md',late_experiments='LATE_L1_EXPERIMENTS_AND_INSTRUMENTS.md',edge_semantics='requires_all is AND; feedback is documented separately and is not a first-unlock edge',
          nodes=nodes,dictionary_entities=entities,stage_only_entities=extras)
(BASE/'review-tech-tree.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# R1统一科技依赖与能力表','',
       '以[审核总案](REVIEW_SYSTEM.md)为语义依据。箭头/前置表示首次取得能力的AND关系；量产反馈不计作首次依赖。core包含主线教学体验，extension是保留的深化玩法。编号不是强制串行日期。','',
       '**范围：能力依赖可达，不是完整物品配方验证。** 当前P06–15的粗版/精密版、模块封装、初始电节点集群与控制基线已同步[R4阶段设计](R4_STAGE_DESIGN.md)；[R4材料目录](R4_MATERIALS_MACHINES.md)提供本阶段逐数量基线，后续低温和膜工艺仍需分段深化。','',
       '2026-09-08按[前中期总览与后期入口](EARLY_MID_REVIEW_AND_LATE_ENTRY.md)同步：早期供能/局部扫测、电单板独立入口、单机学习与架构探索，以及[三类中期应用候选](MIDGAME_APPLICATIONS.md)。新增应用为深化能力，不是后期门槛或已注册物品。','',
       '| 节点 | 里程碑 | 能力 | 全部前置 | 路线 | 可见成果 |','| --- | --- | --- | --- | --- | --- |']
for n in nodes:lines.append(f"| `{n['id']}` | {n['milestone']} | {n['title']} | {'、'.join(n['requires_all']) or '开局'} | {n['track']} | {n['outcome']} |")
lines += ['', '## 持续反馈（不作为首次解锁依赖）','',
 '- 掺杂/相图/学习改进既有晶体和分离线；工艺历史仍需复测。',
 '- 微观材料改进天空探测，宇观参照检验本地模型。',
 '- 全光专化改善部分任务，电域继续承担控制、存储与接口。',
 '- 流水线、无人机与装备消化前中期能力，产生新的工况记录；规模学习与集群按实际任务扩展。',
 '- 视界产能改善后续工业，首次视界仍用普通能源。',
 '- 新维度测量复核既有模型，不复制/覆盖已有世界。','',
 '自动检查与反例见[验证记录](REVIEW_VALIDATION.md)。']
(BASE/'REVIEW_TECH_TREE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

lines=['# R1旧内容覆盖与去向','',
       '逐项读取旧字典§3–13的164个实体条目，另核对阶段表独有的20个ID。不是注册代码清单；名称/旧用途保留用于追溯，配方以R1重构规则修订。不同档次设备归到同一能力不代表同一配方或同一时点。','',
       '当前计算研究阶段的具体取得、物料与装配以[R4逐项去向](R4_SOURCE_RECONCILIATION.md)为准，本表保留全局能力位置。','',
       '| 旧ID | 原名 | R1能力/位置 | 原用途 | 处置/修订 | 原字典行 |','| --- | --- | --- | --- | --- | --- |']
for e in entities:
    lines.append(f"| `{e['id']}` | {e['name']} | {e['milestone']} / `{e['capability']}` | {e['role']} | {e['disposition']} | {e['source_line']} |")
lines += ['','## 阶段表独有条目','',
          '以下精确ID差异不自动要求新注册。导波线/诊断台应评估别名合并；多个装配台可作为同平台工装，但功能全部保留。','',
          '| ID | 原名 | R1能力 | 处置 | 原阶段表行 |','| --- | --- | --- | --- | --- |']
for e in extras:
    disposition='保留为对应工艺/设备模块；首次版与规模升级分别定义'
    if 'assembly' in e['id'] or 'station' in e['id']:disposition='保留操作，候选合并为通用装配平台的工装/模式'
    if e['id']=='all_optical_switch_core':disposition='保留全光专化，不要求电气退场'
    lines.append(f"| `{e['id']}` | {e['name']} | `{e['capability']}` | {disposition} | {e['source_line']} |")
lines += ['','## 字典之外的玩法家族','',
          '| 家族 | 首次能力 | 去向/细节 |','| --- | --- | --- |']
families=[('木筛、木盆、开局材料','manual','一§2，粗版自举'),('有机基底、纤维/树脂/培养','bio','三§6，输入有机质量约束'),
 ('基本发电与泵/物流接口','power / feedback','普通能源与原版漏斗先可用'),('硅/化学前体与封装材料','doping / precision','二§2–3，需要物料表继续细化'),
 ('EDA宏单元、冷却/时序/屏蔽与封装族','eda / package','三§1，模板入门，微结构深化'),('参数空间、算子、图与高级Runtime','runtime','三§2，受限可返回编辑场'),
 ('数据集、校准、轨迹、策略和主动实验','train / rl / active','三§5–7，实验来源与独立验收'),('多DNS、无线G1–G6、机柜族','network / advanced_network','三§3–4，地址/服务/权限及预算'),
 ('全部模型族与实体/交易/对抗','model_families / entity_policy','三§5–6，各有支持任务与离线版本'),('外部API与本地后端','api','三§7，关闭外部服务不阻塞'),
 ('流水线、无人机与计算辅助装备','production_cell / drone / adaptive_gear','三的[应用续稿](MIDGAME_APPLICATIONS.md)，登记可选能力；材料数量及适配尚待细化'),
 ('SPAD/预告源/计数器/态制备','q_lab / q_prepare','四§4–5，先校准后量子任务'),('星录、谱尺、背景与几何','sky / spectrum / cosmic_geometry','四§3、6，独立宇观线'),
 ('接界棱镜、间隙腔、互证谱册','micro_boundary / cross','四§6，实体与档案分开'),('空白膜/普通头/启动储备','horizon_parts','五§2，解除视界自举环'),
 ('新维度槽、返回锚、休眠救援','return_anchor / maintain','五§5–6，不覆盖实例、不困住玩家')]
for fam,cap,note in families:lines.append(f'| {fam} | {cap} | 发展线{note} |')
lines += ['','覆盖意味着已安排位置、用途和修订方向，不等于所有玩法子参数均已详细规范或实现。旧传感器表§14复用已有实体；全局组件表是共享状态契约，不重复计入164个实体。']
(BASE/'REVIEW_CONTENT_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

lines=['# R1设计验证记录','',
       '运行方式：`python docs/system-rebuild/build_review.py`。仅生成R1图/覆盖/验证文件，不运行旧build_design.py，不回写原稿。','',
       f"能力节点：{len(nodes)}；主线：{len(nodes)-len(extensions)}；深化：{len(extensions)}；里程碑：28；旧实体：{len(entities)}；阶段表独有：{len(extras)}。",'',
       '| 检查 | 结果 |','| --- | --- |']
for name,ok in checks.items():lines.append(f'| `{name}` | {"PASS" if ok else "FAIL"} |')
lines += ['', '## 验证的实际边界','',
          '- 可达/无环基于能力图，节点内精密/粗版部件与数量配方尚未完整验证。',
          '- 可选分支删除实验验证依赖不阻塞，不能证明禁用相应内容后的所有经济平衡。',
          '- 164+20是从源表逐行匹配，功能说明和修订做了人工核对；并非已注册或已实现内容。',
          '- 本轮三项应用能力不计入旧实体覆盖数；其新增机体、移动储能、执行模块尚未并入R4数量目录，图可达不能替代物料/空间验算。',
          '- L1仅修订凝聚态工作窗与实验室谱尺的模型前置，首批实验/仪器见LATE_L1_EXPERIMENTS_AND_INSTRUMENTS.md；新增组件的完整制程和数量没有由能力图验证。',
          '- 18份原文SHA-256与源清单一致，未覆盖既有未提交修改。',
          '- R1模型公式只完成适用域/数据来源设计；D1两个离线原型不能代表全模型已验证。',
          '- 尚无Java更改、Gradle测试、实际试玩、时长平衡、多人/区块生命周期验证。','',
          '审核后的首批验证应优先做材料质量账、光电端到端成本、随机实验可辨识性和终局停机/返回状态机。']
(BASE/'REVIEW_VALIDATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(dict(nodes=len(nodes),core=len(nodes)-len(extensions),extensions=len(extensions),dictionary=len(entities),stage_only=len(extras),checks=len(checks),all_pass=all(checks.values())),ensure_ascii=False))

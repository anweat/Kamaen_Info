"""Generate the R4 availability, bill-of-materials and traceability review."""
from collections import Counter
from pathlib import Path
from math import ceil, isclose
import hashlib
import json
import re

from r4_stage_catalog import ITEMS, RECIPES, STAGES, STATIONS, START, EVIDENCE, ASSEMBLY, PACKS, ARRAY_TEMPLATES

BASE = Path(__file__).resolve().parent
REPO = BASE.parent.parent
checks = {}


def check(key, value):
    checks[key] = bool(value)
    if not value:
        raise AssertionError(key)


def names(amounts):
    return '；'.join(f"{ITEMS[k]['name']}×{v}" for k,v in amounts.items()) or '—'


by_output = {}
for r in RECIPES:
    for k in r['outputs']:
        by_output.setdefault(k, []).append(r)


def primary(key):
    # Prefer a named intended output, not incidental waste production.
    rows = by_output[key]
    return next((r for r in rows if r['id'] == key), rows[0])


def available_closure(disable=None):
    available, knowledge = set(START), set()
    changed = True
    while changed:
        changed = False
        for key,e in EVIDENCE.items():
            if set(e['needs']) <= knowledge and set(e['objects']) <= available and key not in knowledge:
                knowledge.add(key); changed = True
        for r in RECIPES:
            if r['id'] == disable:
                continue
            needed = set(r['inputs']) | set(r['tools'])
            station = STATIONS[r['station']]['item']
            if station:
                needed.add(station)
            if r['energy']:
                needed.add('generator')
            if needed <= available and set(r['evidence']) <= knowledge:
                new = set(r['outputs']) - available
                if new:
                    available.update(new); changed = True
    return available, knowledge


class Bill:
    """Nominal successful route; reusable tools remain, installed children do not."""
    def __init__(self):
        self.stock = Counter()
        self.roots = Counter()
        self.runs = Counter()
        self.known = set()
        self.stack = []
        self.energy_left = 0
        self.energy = 0
        self.seconds = 0
        self.log = []
        self.auto = False

    def evidence(self, key):
        if key in self.known:
            return
        e = EVIDENCE[key]
        for earlier in e['needs']:
            self.evidence(earlier)
        for part in e['objects']:
            self.need(part, e.get('minimum_instances',{}).get(part,1))
        self.known.add(key)
        self.log.append('验证条件 '+key)

    def need(self, key, count):
        if self.stock[key] >= count:
            return
        if key in START:
            delta = count - self.stock[key]
            self.roots[key] += delta
            self.stock[key] += delta
            return
        if key in self.stack:
            raise ValueError('循环依赖: '+' -> '.join(self.stack+[key]))
        self.stack.append(key)
        try:
            r = primary(key)
            if self.auto and r['id'] == 'separate':
                r = next(x for x in RECIPES if x['id']=='separate_auto')
            runs = ceil((count-self.stock[key])/r['outputs'][key])
            for gate in r['evidence']:
                self.evidence(gate)
            station = STATIONS[r['station']]['item']
            if station:
                self.need(station,1)
            for part in r['tools']:
                self.need(part,1)
            if r['energy']:
                self.need('generator',1)
            # Inputs can create co-products used by later inputs. Order is stable.
            for part,n in r['inputs'].items():
                self.need(part,n*runs)
                # Reserve now; a later ingredient's own recipe must not consume it.
                self.stock[part] -= n*runs
                assert self.stock[part] >= 0, (key,part)
            total_energy = r['energy']*runs
            if total_energy > self.energy_left:
                fuel = ceil((total_energy-self.energy_left)/3200)
                self.need('carbon',self.stock['carbon']+fuel)
                self.stock['carbon'] -= fuel
                self.energy_left += fuel*3200
            self.energy_left -= total_energy
            for part,n in r['outputs'].items():
                self.stock[part] += n*runs
            self.runs[r['id']] += runs
            self.seconds += runs*r['seconds']
            self.energy += total_energy
            self.log.append(r['id']+' ×'+str(runs))
        finally:
            self.stack.pop()

    def produce(self, targets):
        # Build the early mechanisation once using manual resources, then select
        # the same-output automatic separation route for subsequent batches.
        self.need('fractionator',1)
        self.need('generator',1)
        self.auto = True
        for part,n in targets.items():
            self.need(part,n)
        # Some early target may be installed in another target; recheck the bill.
        for part,n in targets.items():
            self.need(part,n)
        assert all(self.stock[k]>=n for k,n in targets.items())
        return dict(roots=dict(self.roots), total_energy=self.energy,
                    serial_recipe_seconds=self.seconds, runs=dict(self.runs),
                    remaining=dict(sorted((k,v) for k,v in self.stock.items() if v)),
                    evidence=sorted(self.known), log=self.log)


LEGACY = {}
def map_ids(ids, meaning, destination):
    for key in ids.split():
        assert key not in LEGACY
        LEGACY[key] = dict(meaning=meaning, destination=destination)


map_ids('kamaen_crystal_t2 kamaen_wafer kamaen_dopant kamaen_pn_junction', '按母批/处理状态与器件模板组织；二代是用途检验名，N/P是目标响应族', 'R4_MATERIALS_MACHINES.md')
map_ids('electronic_logic_gate timing_structure_cell crystal_interconnect kamaen_oscillator', '门控阵列片、明确状态模块、按尺度分开的互连与实际晶振', 'R4_MODELS_AND_FACTORS.md')
map_ids('lithography_mask lithography_mask_set process_protection_kit', '粗接触模板先行，精密层组后续；防护按实际覆盖与用途', 'R4_MATERIALS_MACHINES.md')
map_ids('ion_implanter lattice_annealing_furnace lithography_projector etching_tank tier2_optical_process_framework', '保留对应实物工位及顺序历史，统一面板向已连接工位派任务', 'R4_MATERIALS_MACHINES.md')
map_ids('hardware_diagnostic_station chip_blueprint_writer chip_packaging_station', '工程台统一入口，诊断/封装仍由实体设备执行；初版无需计算板自举', 'R4_UNIFIED_WORKBENCH.md')
map_ids('electronic_control_chip electronic_matrix_tile electronic_activation_tile eda_module_plate packaged_logic_chip', '实际模块与制造模板分开；角色名不重复产出硬件，双路线分账', 'R4_HARDWARE_AND_CLUSTER.md')
map_ids('memory_page', '工作2 KiB与持久16 KiB使用不同已测模板；逻辑页仅分配地址', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('motherboard_blueprint configurable_motherboard network_interface_chip server_rack fiber_switch', 'B01/B02与R04两托盘柜；实际背板、包接口和世界线缆', 'R4_HARDWARE_AND_CLUSTER.md')
map_ids('sensor_hub noise_spectrometer thermodynamic_antenna', '通用采样服务配对应物理量探头，天线仅服务其波段', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('model_component_gateway model_compiler', '统一工作台中的语义图/部署页，世界底座和参数空间仍为同一图的表现', 'R4_UNIFIED_WORKBENCH.md')
map_ids('storage_center_controller macro_info_index_core info_center_controller noise_database', '记录节点先行，再部署索引/参数库/底噪应用；应用不提供额外存储', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('world_noise_sample thermal_noise_plate radiation_noise_plate', '有来源原始记录和解释视图；辐射谱仅限当前探头实测波段', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('quantum_fluctuation_plate', '交界保留至P18对应仪器；当前只留未解释残差，禁止提前标成量子实证', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('chunk_entropy_record entropy_flow_meter', '当前登记输入/输出及估计模型的账本，不宣称测出任意区块热力学总熵', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('silicon_photonic_waveguide_blank silicon_photonic_waveguide mzi_modulator phase_tuner silicon_photodetector single_freq_laser_source', '粗光件与精密变体共用器件/制程模型，光电并行', 'R4_MODELS_AND_FACTORS.md')
map_ids('calibration_token', '改为对象、映射、条件与报告的绑定记录，无魔法正确性消耗品', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('coherent_energy coherent_energy_buffer coherent_energy_regulator laser_pump_tower', '激励能量、缓存、调节与集中供给分别记账，参考/相干状态另算', 'R4_MODELS_AND_FACTORS.md')
map_ids('kamaen_nonlinear_medium photonic_logic_gate kamaen_bistable_cell photonic_control_core photonic_coprocessor photonic_gpu_unit photonic_pulse_processor photonic_ram_unit', '先有限2×2强度映射，再按经过验证的阵列/编码/非线性/保持模板扩展光五件套', 'R4_RUNTIME_AND_RESEARCH.md')
map_ids('photonic_waveguide_etching_station mzi_weaving_station photonic_calibration_station', '对应刻蚀、模块拼装、校准工装；专用外壳可保留，不重复基础流水线', 'R4_MATERIALS_MACHINES.md')

FAMILY_DESTINATIONS = {
    'R4_MATERIALS_MACHINES.md': 'C01 C02 C03 C04 C05 C06 C08 C11 C12 C14 C15 C16 C17 C18',
    'R4_UNIFIED_WORKBENCH.md': 'C07 C09 C13 C20 C21 C22 C23 C24 C25 C34',
    'R4_RUNTIME_AND_RESEARCH.md': 'C10 C19 C26 C27 C28 C29 C30 C31 C32 C33',
}


def build():
    check('recipe_ids_unique',len({r['id'] for r in RECIPES})==len(RECIPES))
    check('all_references_declared',all(set(r['inputs'])|set(r['outputs'])|set(r['tools']) <= set(ITEMS) and r['station'] in STATIONS and set(r['evidence'])<=set(EVIDENCE) for r in RECIPES))
    check('positive_counts_and_bounded_energy',all(all(isinstance(v,int) and v>0 for v in list(r['inputs'].values())+list(r['outputs'].values())) and r['seconds']>0 and 0<=r['energy']<=64*r['seconds'] for r in RECIPES))
    check('all_evidence_references_valid',all(set(e['objects'])<=set(ITEMS) and set(e['needs'])<=set(EVIDENCE) for e in EVIDENCE.values()))
    available,knowledge = available_closure()
    check('all_authored_products_reachable',set(ITEMS)<=available)
    check('all_evidence_reachable',set(EVIDENCE)<=knowledge)
    check('manual_bootstrap_remains_without_tower',set(['seed','wafer','control_chip','populated_board'])<=available_closure('separate_auto')[0])
    sep=next(r for r in RECIPES if r['id']=='separate')
    check('separation_dry_budget_8',sum(sep['outputs'][k] for k in ['iron_powder','copper_powder','silica','clay','slag'])==8)
    check('auto_separation_same_material_budget',sep['outputs']==next(r for r in RECIPES if r['id']=='separate_auto')['outputs'])
    check('array_templates_declared',set(ARRAY_TEMPLATES)<=set(ITEMS) and all(any(r.get('array_template')==k for r in RECIPES) for k in ARRAY_TEMPLATES))
    check('ram_array_capacity',ARRAY_TEMPLATES['ram']['array_wafers']*ARRAY_TEMPLATES['ram']['bits_per_wafer']==8*ARRAY_TEMPLATES['ram']['bytes'])
    check('storage_array_capacity',ARRAY_TEMPLATES['storage']['array_wafers']*ARRAY_TEMPLATES['storage']['bits_per_wafer']==8*ARRAY_TEMPLATES['storage']['bytes'])
    check('control_state_capacity',4*ARRAY_TEMPLATES['hold']['bits']==ARRAY_TEMPLATES['control_chip']['internal_state_bits'])
    check('RAM_requires_manufactured_array',primary('ram')['inputs'].get('working_array_wafer')==2 and 'region_wafer' not in primary('ram')['inputs'])
    check('storage_requires_manufactured_array',primary('storage')['inputs'].get('record_array_wafer')==2 and 'wafer' not in primary('storage')['inputs'])
    check('controller_requires_real_program_region',primary('control_chip')['inputs'].get('logic_program_wafer')==1)
    check('RAM_child_template_matches_capacity',primary('ram')['inputs']['working_array_wafer']*ARRAY_TEMPLATES['working_array_wafer']['bits']==8*ARRAY_TEMPLATES['ram']['bytes'])
    check('storage_child_template_matches_capacity',primary('storage')['inputs']['record_array_wafer']*ARRAY_TEMPLATES['record_array_wafer']['bits']==8*ARRAY_TEMPLATES['storage']['bytes'])
    old=json.loads((BASE/'computing-content.json').read_text(encoding='utf-8'))
    check('all_67_legacy_items_mapped',set(LEGACY)=={x['id'] for x in old['existing_dictionary_items']})
    families={k:v for v,keys in FAMILY_DESTINATIONS.items() for k in keys.split()}
    check('all_34_families_mapped',set(families)=={x['design_key'] for x in old['additional_families']})
    check('all_15_stage_ids_retained',len(old['stage_id_treatment'])==15)
    source_count=0
    for rel,size,digest in re.findall(r'\| `([^`]+)` \| (\d+) \| `([a-f0-9]{64})` \|',(BASE/'SOURCE_MANIFEST.md').read_text(encoding='utf-8')):
        raw=(REPO/rel).read_bytes()
        check('source_'+rel,len(raw)==int(size) and hashlib.sha256(raw).hexdigest()==digest)
        source_count+=1
    check('source_count_18',source_count==18)
    bills={key:Bill().produce(p['target']) for key,p in PACKS.items()}
    for key,b in bills.items():
        check('bill_'+key,all(b['remaining'].get(k,0)>=v for k,v in PACKS[key]['target'].items()))
    check('B01_inference_32_fits',744+56*32 <= 4096-512 < 744+56*64)
    check('B01_training_16_fits',1208+136*16 <=4096-512 <1208+136*32)
    payload=dict(version='R4-complete-stage-candidate', stages=STAGES, items=list(ITEMS.values()),recipes=RECIPES,
                 stations=STATIONS,evidence=EVIDENCE,array_templates=ARRAY_TEMPLATES,assembly_recipes=ASSEMBLY,bills=bills,
                 legacy=LEGACY,families=families,stage_aliases=old['stage_id_treatment'],checks=checks,
                 limits='候选配方的名义成功路径与依赖/数量检查，非物理求解、真实化学、Java或试玩验证')
    (BASE/'r4-stage-content.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# R4材料、机器与制造目录','',
           '由[r4_stage_catalog.py](r4_stage_catalog.py)定义、[build_r4_stage.py](build_r4_stage.py)生成；2026-09-07。完整阶段入口：[R4总案](R4_STAGE_DESIGN.md)。', '',
           '## 计量与自举约定','',
           '- 木材、圆石和水为开局可再生条件。粗纤维用木浆，碳材用木炭，基础配方不依赖金、钻石、红石、石油、天然火药或稀有掉落。普通资源路线可从外部合格原料替代，但须匹配登记材料/品级。',
           '- 所有数量是候选料件数；不同物品一件的质量不同。只有8份干料分离例使用统一干料单位并检查总额；本表不是全物品化学质量或元素守恒证明。A/B处理剂是虚构晶体的登记处理配方，不是现实半导体化学教程。',
           '- 时间为模型秒的名义工序预算，能量E为游戏计量，尚不等同真实J。表中电工序须接供能机；1碳材供3200 E、额定64 E/s，耗散与设备余热另由模型计算。燃料工序已在投入中列碳材，不能重复收电热成本。',
           '- 产物身份/内部件保留；装配配方中的输入转为成品子件，不再留在库存。工装不消耗，但一次被占用的工装不能同时给其他任务使用。表中秒数不含首次研究、调谐、搬料、排队和换线。',
           '- 工序条件用公开保守模板保证首批可达；偏离工况的分档、返工和材料历史见总案。所有成品均有条件测试，证据要求不等于提前拿成品自举。',
           '- 门控/保持为有展开单元数的阵列片；页载片、CPU等必须按[R4模型规格](R4_MODELS_AND_FACTORS.md)核对实际阵列模板，不把原料计数当逻辑容量。',
           '- 流片行是投影、注入、刻蚀、退火的固定流程模板摘要，必须逐步记录工序；并非投影器一台吞料直接产芯片。多层掩膜组来自同版图各层的实体掩膜，按实际层数复用。', '',
           '## 首次可获得材料与部件','', '| 键/显示名 | 最早段 | 形态 | 约束 |','| --- | --- | --- | --- |']
    lines.extend(f"| `{k}` / {v['name']} | {STAGES[v['stage']]} | {v['kind']} | {v['note'] or '按下表登记路线生产；允许经检验的同类材料替代'} |" for k,v in ITEMS.items())
    lines += ['', '## 设备与工装服务','', '| 工位 | 首台实物 | 同时处理范围 | 操作与边界 |','| --- | --- | --- | --- |']
    lines.extend(f"| {v['name']} | {ITEMS[v['item']]['name'] if v['item'] else '起始手工能力'} | {v['capacity']}个工件/单个工程（非料盒总堆叠数） | {v['modes']} |" for v in STATIONS.values())
    lines += ['', '精密注入、诊断、终端、II型框架与专用光学外壳虽不各开一套独立配方语法，仍是实际设备/工装服务；需要的组件与首次制造配方在下表。专用台与通用框架共用服务，不重复制造功能。', '',
              '## 名义制造与装配配方','', '| 配方 | 工位 | 投入 | 产出 | 秒 / E | 复用工装 / 研究证据 |','| --- | --- | --- | --- | --- | --- |']
    for r in RECIPES:
        extra=', '.join(r['tools']) or '—'
        gates=', '.join(r['evidence']) or '—'
        lines.append(f"| `{r['id']}` | {STATIONS[r['station']]['name']} | {names(r['inputs'])} | {names(r['outputs'])} | {r['seconds']} / {r['energy']} | 工装：{extra}；证据：{gates} |")
    lines += ['', '门控/保持、页载片与控制器的配方含指定阵列模板的重复加工、接触/互连及测试预算；原料区域片不能直接赋容量。ram与storage的未封装阵列证据在下表，完整结构规模见[R4模型规格](R4_MODELS_AND_FACTORS.md)。', '',
              '残料/废水存入可用容器，满则阻止下一次会产生该副产物的工序；有登记回收路线才回收，不一键变回全部原料。已封装模块拆解按内部件、连接损耗与可维修性处理，不默认正配方完全逆转。', '',
              '## 首次研究条件','', '| 证据键 | 已有前置 | 可用工具/试片 | 完成什么对照 |','| --- | --- | --- | --- |']
    lines.extend(f"| `{k}` | {', '.join(e['needs']) or '—'} | {', '.join(ITEMS[i]['name'] for i in e['objects'])} | {e['experiment']} |" for k,e in EVIDENCE.items())
    lines += ['', 'cluster条件实际需要两个不同在线节点；检查配方可达性不替代这一运行验收。实验消耗能源、样品处理与记录容量，粗验证与生产合格测试可共用仪器，但不把一次空载测试当全部工况合格。', '',
              '## 三套装配的从零物料展开','',
              '每套独立从起始资源计算；先手工建立分馏塔与供能机，再使用等产出自动分离。复用设备保留，多产物留在库存供后续使用。采用固定成功工艺，只准备证据所需基础对象，不模拟实验处理的转化/损耗；没有算入随机返工、实验耗材/能源或玩家走动。它是生产物料基线，remaining不是实际完成所有实验后的库存。串行秒数是生产预算，不能直接当游玩时长。', '',
              '| 装配目标 | 木材 | 圆石 | 水份 | 电工序E | 串行工序秒 |','| --- | --- | --- | --- | --- | --- |']
    for key,b in bills.items():
        lines.append(f"| {PACKS[key]['name']} | {b['roots'].get('wood',0)} | {b['roots'].get('stone',0)} | {b['roots'].get('water',0)} | {b['total_energy']} | {b['serial_recipe_seconds']} |")
    lines += ['', '完整配方批次数与剩余工具/副产物见[r4-stage-content.json](r4-stage-content.json)的bills。两柜示例使用节点本地的固定编排服务，不强制额外造独立cluster_core；独立编排节点是管理规模升级。', '']
    (BASE/'R4_MATERIALS_MACHINES.md').write_text('\n'.join(lines),encoding='utf-8')
    coverage=['# R4旧稿去向与本轮修订','', 'R4不删除旧稿。这里明确当前阶段采用的定位；R2/R3用于追溯，冲突处以[R4总案](R4_STAGE_DESIGN.md)及对应专题为准。', '',
              '## 旧字典67项','', '| 旧ID/名称 | R4定位 | 完整设计 |','| --- | --- | --- |']
    for olditem in old['existing_dictionary_items']:
        k=olditem['id'];v=LEGACY[k]
        coverage.append(f"| `{k}` / {olditem['source']['name']} | {v['meaning']} | [对应专题]({v['destination']}) |")
    coverage += ['', '## 34个补充内容族','', '| 族 | 合并入口 | 保留范围 |','| --- | --- | --- |']
    for f in old['additional_families']:
        k=f['design_key']
        coverage.append(f"| {k} {f['name']} | [专题]({families[k]}) | 保留实体/工装/数据各自定位；不把内容族数量当新注册方块数 |")
    coverage += ['', '## 阶段表额外15个ID','', '| 原ID | 当前处理 |','| --- | --- |']
    coverage.extend(f"| `{k}` | {v}；操作入口、材料与实体位置遵循R4 |" for k,v in old['stage_id_treatment'].items())
    coverage += ['', '## 本轮反复检查后形成的修订','',
                 '1. 从所有影响因素归纳八类，参数属于实际物理层，默认只展示当前相关部分。',
                 '2. 工程册、工程台和各机器打开同一项目；设计图、物理结构与模型语义保持各自真值与明确绑定。',
                 '3. 第一颗芯片走粗模块实验封装，精密控制器再反过来改进流片设备；首台仪器不依赖待测成品。',
                 '4. 容量/算力来自有展开规模的制造模板；B01工作4 KiB扣512 B系统预留，示例推理32/训练16批分别核算。',
                 '5. R2.1四托盘柜改为R04两前维护托盘，后部用于背板和风路；保留2×2×3教学外形，但不把四盘与新风路同时塞进原空间。',
                 '6. B02增加实际侧挂载板、支撑、插座和光源；不在满板上免费增加器件。',
                 '7. 初始光模块仅保证2×2非负强度映射，通用有符号MatMul保留电后端；光五件套仍作为本阶段拓展，有对应结构与验证。',
                 '8. 线缆、支撑、管路引用同一实体几何；虚拟模型排版不制造线长。自动连接草稿与实际施工分开。',
                 '9. 小模型在单板训练，集群解决规模/位置问题；RL和主动采样使用真实有界动作，不成为唯一通关门槛。',
                 '10. 量子涨落记录保留交界，只有后期对应仪器才赋该含义；普通残差不提前解释成量子信号。', '']
    (BASE/'R4_SOURCE_RECONCILIATION.md').write_text('\n'.join(coverage),encoding='utf-8')
    report=['# R4目录验证','', f'{len(checks)}项目录/依赖/配方示例检查通过。', '',
            '| 检查 | 结果 |','| --- | --- |']+[f'| {k} | 通过 |' for k in checks]
    report += ['', '验证能力：引用完整、名义材料/工位/证据自举可达、三套配方库存不为负及目标产出、指定内存预算、旧内容去向与18份旧源文件哈希。', '',
               '范围限制：证据表的对象可达不证明实验已经通过；配方按名义成功路线且不模拟并行占用。目录去向不证明每个高阶模板已编码。未验证完整物理、真实配方质量、游戏渲染或实际游玩；模型/自动搭线行为另见专题中的验收表。', '']
    (BASE/'R4_VALIDATION.md').write_text('\n'.join(report),encoding='utf-8')
    print(json.dumps(dict(items=len(ITEMS),recipes=len(RECIPES),evidence=len(EVIDENCE),checks=len(checks),bills={k:{'roots':v['roots'],'seconds':v['serial_recipe_seconds']} for k,v in bills.items()}),ensure_ascii=False))


if __name__=='__main__': build()

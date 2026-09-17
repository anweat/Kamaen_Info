"""R4 authored recipe/availability source. Design units, not game registrations."""
STAGES = ['A0 起步资源', 'A1 晶体与粗工具', 'A2 器件实验', 'A3 封装与单板', 'A4 机柜与集群', 'A5 学习与主动实验']
ITEMS = {}
RECIPES = []


def item(key, name, stage, kind='料件', note=''):
    assert key not in ITEMS, key
    ITEMS[key] = dict(id=key, name=name, stage=stage, kind=kind, note=note)


def recipe(key, station, inputs, outputs, seconds, energy=0, tools=(), evidence=()):
    RECIPES.append(dict(id=key, station=station, inputs=inputs, outputs=outputs,
                        seconds=seconds, energy=energy, tools=list(tools), evidence=list(evidence)))


for key, name, note in [
    ('wood','木材','开局可再生树木；不以稀有树种为前置'), ('stone','圆石','开局可再生来源'),
    ('water','水份','就地装入容器；一份为配方计量，不吞掉无限水源'),
]: item(key,name,0,'起始资源',note)

for key,name in [('fiber','粗纤维'),('carbon','碳材'),('scrap','粗频谱碎屑'),('iron_powder','铁粉'),
                 ('copper_powder','铜粉'),('silica','硅质粉'),('clay','陶土料'),('slag','频谱滤渣'),
                 ('iron','铁料'),('copper','铜料'),('glass','玻璃料'),('ceramic','陶瓷料'),
                 ('binder','树脂粘结料'),('wire','绝缘导线段'),('frame','机架结构件'),
                 ('contact','接触件'),('board_blank','绝缘覆铜板坯'),('heat_pad','热界面片'),
                 ('coolant','冷却液份'),('wastewater','待处理废水'),('residue','回收残料')]:
    item(key,name,0)

for key,name,note in [
    ('sieve','木质手筛','无金属前置'),('basin','沉降滤盆','采用粗纤维滤网，后续滤膜升级'),
    ('furnace','石炉','普通燃料加热'),('fractionator','搅拌分馏塔','自动化已有分离，不解锁新的元素集合'),
    ('crucible','热噪坩埚','先手动按保守温程操作'),('spectroscope','初级分光镜','只给粗谱与可测性质'),
    ('mechanical_bench','机械制备台','手动切磨、夹持、粗模板；不是精密注入机'),
    ('generator','燃料供能机','碳材供能，额定64 E/s；1碳材提供3200 E，余热归此机'),
]: item(key,name,0,'设备',note)

for key,name,note in [
    ('neutral','均值化基底','合格窗内的平均背景材料'),('seed','白噪晶种','初始结晶；不是随机特化词条'),
    ('raw_crystal','粗卡玛恩晶体','可追溯母批、组成与应力；显示名别名统一'),
    ('wafer','空白晶片','来自定向切片，保留母批/取向'),('debris','晶体碎料','不能无损恢复原结构'),
    ('stable_piece','稳谱片','相应用途检验，不等于全属性提高'),
    ('guide_piece','导波片','取向与传输窗经测量'),('blank_mask','接触掩膜坯','可刻粗图案'),
    ('record_sheet','研究记录载体','静态记录，不提供工作内存'),('mount','器件夹具','限制姿态并形成接触'),
    ('book','工程册','统一入口的初版；只查询、记图、投影和做有限规则检查'),
    ('probe','粗读出探头','机械/光学刻度与固定读出，不能运行任意模型'),
    ('scanner','固定步进测试器','机械步进/固定测试序列，无可编程CPU自举要求'),
    ('power_module','供给模块','固定供给与保护，额定64 E/s，输出能量不能超过输入'),
    ('fan','风冷模块','由驱动、散热与风口组成，自身有耗散与振源'),
]: item(key,name,1,'模块' if key in ('probe','scanner','power_module','fan') else '料件',note)

for key,name,note in [
    ('crystal_frame','I型力学框架','普通机械夹具首版，不以偏振晶体/应力传感器为前置'),
    ('device_bench','晶体实验台','拼接、扫描、调谐；源和读出工具可外接'),
    ('annealer','晶格退火炉','首版固定温程，后接终点芯片与模型控制'),
]: item(key,name,1,'设备',note)

for key,name in [('treat_a','A型组成处理剂'),('treat_b','B型组成处理剂'),('etchant','刻蚀处理液'),
                 ('resist','感光/保护涂料'),('pattern_mask','已刻接触掩膜'),('region_wafer','区域处理晶片'),
                 ('filter','选频器件'),('gate','电门控器件'),('hold','电保持器件'),
                 ('window','连续窗口模块'),('oscillator','粗晶振模块'),('guide','加工导波器件'),
                 ('coupler','分束/耦合件'),('phase','相位调谐器'),('light_source','粗稳谱光源'),
                 ('encoder','强度编码模块'),('reader','强度读出模块'),('mzi','双路干涉模块'),
                 ('case','可拆封装壳'),('socket','安装插座'),('data_cable','铜数据线段'),
                 ('optical_cable','世界光纤段'),('panel','端口面板'),('tray','主板托盘'),
                 ('duct','导风/封口件'),('cable_tray','理线槽段'),('damper','可调支撑/阻尼件'),
                 ('local_filter','局部供给滤波件'),('shield','屏蔽/返回路径套件'),
                 ('sensor_head','可换环境探头'),('fluid_pipe','冷却管段'),('cold_plate','冷板'),
                 ('pump','循环泵'),('exchanger','换热器')]: item(key,name,2)

for key,name,note in [
    ('packager','封装与装板工位','模块/裸片两条路线，板级工装复用'),
    ('etch_station','刻蚀/清洗工位','粗版接触图案先行，液体与样品分账'),
]: item(key,name,2,'设备',note)

for key,name,note in [
    ('working_array_wafer','8192位工作阵列片','区域片经保持阵列模板加工与逐地址测试；不是空白原料'),
    ('logic_program_wafer','固定微程序片','256×16位结构编码程序区，属于控制模板的实际内件'),
    ('record_array_wafer','65536位记录阵列片','非易失记录材料与刻写阵列模板，需断供复读'),
]: item(key,name,2,'料件',note)

for key,name,note in [
    ('endpoint_chip','退火终点芯片','封装实际选频/读出/判据/窗口结构'),
    ('control_chip','可编程电控制芯片','粗模块堆叠首版；可执行有限标量/固定服务'),
    ('ram','工作页载片','已测2 KiB易失容量；复制数据不增加容量'),
    ('storage','持久记录载片','已测16 KiB非易失容量；未通电仍保留已提交记录'),
    ('bus_controller','存储与总线控制模块','同一本地地址空间的页寻址/通路'),
    ('nic','数据接口模块','铜包接口；不免费转为光强或相位口'),
    ('matrix','电矩阵模块','登记小矩阵内核，实际数据计算'),
    ('activation','电激活模块','可选；没有它时由兼容控制芯片处理'),
    ('populated_board','B01已装控制计算板','见装配表；含512 B系统工作内存预留'),
    ('bare_die','精密裸片','受控模板整片制造产物；材料账不再收完整离散器件'),
    ('integrated_chip','集成控制芯片','与粗控制芯片功能族兼容，密度/工况另测'),
    ('optic_array','2×2强度算子模块','MZI/编码/读出已包含；限定映射，不承诺任意有符号MatMul'),
    ('world_base','通用模型组件底座','世界表达图需实物，编辑器图元不消耗底座'),
]: item(key,name,3,'模块',note)

for key,name,note in [
    ('terminal','工程工作台','工程册的同一项目界面；承担登记的编译/预测服务'),
    ('diagnostic','硬件诊断台','复用粗测试服务再提高通道/精度；不是初次检测前置'),
    ('injector','精密组成注入机','粗控制板首版制造后再升级精度'),
    ('projector','光刻投影器','接触模板/粗光源先行；改进有效工艺窗口'),
    ('process_frame','II型工艺框架','组织实际工位，不替代缺失模块'),
]: item(key,name,3,'设备',note)

for key,name,note in [
    ('rack_monitor','机柜监测/控制模块','固定结构发现和遥测；不赠送通用计算节点'),
    ('power_backplane','供能背板','两个独立受控输出，共享上游额定能力'),
    ('data_backplane','数据背板','含真实交换与缓存内件；共享出口64 B/调度步'),
    ('service_panel','检修/支撑内件','维护包络与实际支撑'),('rack_shell','R04小柜结构','2×2×3，两个前维护托盘；不含计算板'),
    ('rack_node','R04单板机柜节点','一块B01装到A托盘，B托盘空置'),
    ('switch','柜间交换节点','多口与总转发能力分别受限'),
    ('sensor_hub','传感汇聚节点','输入通道和缓存，断网有界记录'),
    ('storage_node','记录/参数库节点','板、介质、地址与实际链路共同提供服务'),
    ('cluster_core','集群编排节点','固定管理服务，自己消耗板/内存/网络资源'),
    ('hybrid_board','B02光电混合板','实际B01加已测2×2光模块，不重复收编码/读出内件'),
    ('quiet_reference','稳谱参考模块','改进源/供给/安装，需当前工况校准'),
    ('sync_backplane','同步/参考背板','可选分配模块；参考域、实际分支与抖动预算保留'),
    ('wireless_frontend','有限无线前端','控制/记录首版；真实编解码、缓存、供给与载频'),
    ('wireless_antenna','无线收发天线','与前端分开；方向、遮挡和频带匹配'),
]: item(key,name,4,'模块',note)

for key,name,note in [
    ('nonlinear','非线性晶体器件','开放阈值/脉冲/保持的光学专化'),
    ('opt_gate','光门模块','真值、供给与工作窗均需验收'),
    ('opt_hold','光保持模块','有写读复位/刷新成本，不替代持久介质'),
    ('opt_control','光控制模块','有限控制模板；替换角色须逐接口检查'),
    ('opt_pulse','光脉冲模块','支持已测有限非线性函数'),
    ('opt_ram','光RAM模块','短期激活/状态，容量由实际胞与刷新能力产生'),
    ('opt_coprocessor','光协处理模块','转移/编码；计算需登记内核'),
    ('pump_tower','集中激励/参考架','共享服务，自身供电散热和故障范围保留'),
    ('sky_head','可见光巡天头','有限天空目录与粗谱；不具备微波/量子测量'),
]: item(key,name,5,'模块',note)

START = {'wood': 1, 'stone': 1, 'water': 1}  # Renewable availability, not an inventory grant of all future supplies.
STATIONS = {
    'hand': dict(name='手工制作', item=None, capacity=1, modes='起步构件/装配'),
    'sieve': dict(name='木质手筛', item='sieve', capacity=8, modes='累计有效筛分；可暂停'),
    'basin': dict(name='沉降滤盆', item='basin', capacity=8, modes='沉降、粗滤、废水分离'),
    'fractionator': dict(name='搅拌分馏塔', item='fractionator', capacity=8, modes='集成粗碎/筛分与搅拌，直接处理圆石和水；同干料预算，3秒/批连续作业'),
    'furnace': dict(name='石炉', item='furnace', capacity=8, modes='燃料熔炼/烧制；失热保存实际热历史'),
    'mechanical_bench': dict(name='机械制备台', item='mechanical_bench', capacity=4, modes='切磨、压合、刻粗模板'),
    'crucible': dict(name='热噪坩埚', item='crucible', capacity=4, modes='均值化、成核；不混用未处理滤渣'),
    'crystal_frame': dict(name='I型力学框架', item='crystal_frame', capacity=1, modes='生长冲击、定向/应力写入'),
    'device_bench': dict(name='晶体实验台', item='device_bench', capacity=16, modes='器件拼接/调谐/扫描；模块可超过单格'),
    'annealer': dict(name='晶格退火炉', item='annealer', capacity=4, modes='升温/保持/冷却，独立固定控制'),
    'etch_station': dict(name='刻蚀/清洗工位', item='etch_station', capacity=4, modes='接触图案、粗刻蚀、清洗、废液管理'),
    'packager': dict(name='封装与装板工位', item='packager', capacity=1, modes='按结构占用装配；1个在制工程，料盒容量另计'),
    'projector': dict(name='精密图案工位', item='projector', capacity=4, modes='投影/多步流片；需注入、刻蚀、退火协作'),
}

# Craft recipes express item counts. Only the mineral separation example uses a
# common dry-input unit; no claim of universal chemical mass conservation.
recipe('wood_fiber','hand',{'wood':1,'water':1},{'fiber':2,'wastewater':1},4)
recipe('first_sieve','hand',{'wood':3,'fiber':2},{'sieve':1},8)
recipe('first_basin','hand',{'wood':4,'fiber':2},{'basin':1},8)
recipe('first_furnace','hand',{'stone':8},{'furnace':1},8)
recipe('sifting','sieve',{'stone':8},{'scrap':8},16)
recipe('separate','basin',{'scrap':8,'water':2},{'iron_powder':1,'copper_powder':1,'silica':2,'clay':1,'slag':3,'wastewater':2},24)
recipe('separate_auto','fractionator',{'stone':8,'water':2},{'iron_powder':1,'copper_powder':1,'silica':2,'clay':1,'slag':3,'wastewater':2},3,96)
recipe('wash_water','basin',{'wastewater':4},{'water':3,'residue':1},12)
recipe('charcoal','furnace',{'wood':2},{'carbon':1,'residue':1},8)
for raw,out in [('iron_powder','iron'),('copper_powder','copper'),('silica','glass'),('clay','ceramic')]:
    recipe('fire_'+out,'furnace',{raw:2,'carbon':1},{out:2,'residue':1},12)
recipe('binder','furnace',{'wood':2,'carbon':1},{'binder':2,'residue':1},12)
recipe('wire','hand',{'copper':1,'fiber':1,'binder':1},{'wire':4},6)
recipe('frame','hand',{'iron':2},{'frame':2},6)
recipe('contact','hand',{'copper':1},{'contact':4},4)
recipe('board_blank','hand',{'ceramic':2,'copper':1,'binder':1},{'board_blank':1},10)
recipe('heat_pad','hand',{'copper':1,'carbon':1,'binder':1},{'heat_pad':4},6)
recipe('coolant','basin',{'water':4,'carbon':1},{'coolant':4,'residue':1},8)
recipe('mechanical_bench','hand',{'frame':2,'iron':2,'ceramic':1},{'mechanical_bench':1},20)
recipe('fractionator','hand',{'frame':3,'copper':2,'glass':2,'basin':1},{'fractionator':1},24)
recipe('crucible','hand',{'furnace':1,'iron':2,'ceramic':2,'slag':1},{'crucible':1},16)
recipe('spectroscope','hand',{'glass':2,'iron':1,'carbon':1},{'spectroscope':1},12)
recipe('generator','hand',{'frame':3,'copper':3,'wire':4,'carbon':1},{'generator':1},24)
recipe('neutral','crucible',{'slag':3,'carbon':1},{'neutral':2,'residue':2},30)
recipe('seed','crucible',{'neutral':1,'carbon':1},{'seed':1,'residue':1},30)
recipe('crystal_frame','hand',{'mechanical_bench':1,'frame':4,'iron':2},{'crystal_frame':1},24)
recipe('raw_crystal','crystal_frame',{'seed':1,'neutral':3},{'raw_crystal':1,'debris':1},24)
recipe('reclaim_debris','crucible',{'debris':4,'carbon':1},{'neutral':2,'residue':3},24)
recipe('wafer','mechanical_bench',{'raw_crystal':1,'silica':1},{'wafer':4,'debris':1},20)
recipe('stable_piece','crystal_frame',{'wafer':1},{'stable_piece':1},12,64,tools=['spectroscope'])
recipe('guide_piece','crystal_frame',{'wafer':1},{'guide_piece':1},12,64,tools=['spectroscope'])
recipe('blank_mask','mechanical_bench',{'glass':1,'carbon':1},{'blank_mask':2},8)
recipe('record_sheet','hand',{'fiber':1,'carbon':1},{'record_sheet':8},4)
recipe('mount','hand',{'iron':1,'ceramic':1,'contact':2},{'mount':2},8)
recipe('book','hand',{'record_sheet':2,'wood':1},{'book':1},4)
recipe('probe','hand',{'spectroscope':1,'mount':1,'contact':2},{'probe':1},12)
recipe('scanner','mechanical_bench',{'iron':2,'contact':2,'mount':1},{'scanner':1},16)
recipe('power_module','hand',{'copper':2,'wire':2,'ceramic':1},{'power_module':1},12)
recipe('fan','mechanical_bench',{'iron':2,'copper':1,'wire':2,'heat_pad':1},{'fan':1},16)
recipe('device_bench','hand',{'frame':3,'mount':4,'wire':4,'power_module':1},{'device_bench':1},24)
recipe('annealer','hand',{'crucible':1,'frame':2,'probe':1,'power_module':1},{'annealer':1},24)
recipe('treat_a','basin',{'copper_powder':1,'carbon':1,'water':2},{'treat_a':2,'wastewater':1},12)
recipe('treat_b','basin',{'iron_powder':1,'silica':1,'water':2},{'treat_b':2,'wastewater':1},12)
recipe('etchant','basin',{'slag':1,'water':2,'carbon':1},{'etchant':2,'residue':1},12)
recipe('resist','basin',{'binder':1,'carbon':1,'water':1},{'resist':2},8)
recipe('pattern_mask','mechanical_bench',{'blank_mask':1},{'pattern_mask':1},16,tools=['scanner'])
recipe('etch_station','hand',{'ceramic':4,'glass':2,'frame':2},{'etch_station':1},20)
recipe('region_wafer','etch_station',{'wafer':2,'treat_a':1,'treat_b':1,'etchant':1,'water':1},{'region_wafer':2,'wastewater':2},24,128,tools=['pattern_mask'],evidence=['composition'])
recipe('filter','device_bench',{'guide_piece':1,'mount':1,'contact':2},{'filter':1},12,64,evidence=['response'])
recipe('gate','device_bench',{'region_wafer':1,'contact':3,'mount':1},{'gate':1},16,96,evidence=['composition'])
recipe('hold','device_bench',{'gate':2,'wire':2},{'hold':1},16,96,evidence=['gate_response'])
recipe('window','device_bench',{'gate':2,'hold':2,'scanner':1},{'window':1},20,128,evidence=['state_response'])
recipe('oscillator','device_bench',{'stable_piece':1,'contact':2,'mount':1},{'oscillator':1},16,96,evidence=['response'])
recipe('guide','etch_station',{'guide_piece':1,'etchant':1,'water':1},{'guide':1,'wastewater':1},16,96,tools=['pattern_mask'])
recipe('coupler','device_bench',{'guide':1,'glass':1,'mount':1},{'coupler':1},12,64)
recipe('phase','device_bench',{'wafer':1,'guide':1,'contact':2,'heat_pad':1},{'phase':1},16,96)
recipe('light_source','device_bench',{'stable_piece':1,'glass':2,'power_module':1},{'light_source':1},20,128,evidence=['response'])
recipe('encoder','device_bench',{'gate':2,'phase':1,'power_module':1},{'encoder':1},20,128,evidence=['gate_response'])
recipe('reader','device_bench',{'region_wafer':1,'probe':1,'power_module':1},{'reader':1},16,96)
recipe('mzi','device_bench',{'guide':2,'coupler':2,'phase':1,'mount':1},{'mzi':1},24,192,evidence=['interference'])
recipe('case','mechanical_bench',{'iron':1,'ceramic':1},{'case':1},8)
recipe('socket','mechanical_bench',{'ceramic':1,'contact':4},{'socket':1},8)
recipe('data_cable','hand',{'wire':2,'contact':2},{'data_cable':2},6)
recipe('optical_cable','mechanical_bench',{'glass':2,'binder':1,'fiber':1},{'optical_cable':4},12,64)
recipe('panel','mechanical_bench',{'frame':1,'socket':2,'contact':4},{'panel':1},12)
recipe('tray','mechanical_bench',{'frame':2,'heat_pad':2,'socket':1},{'tray':1},12)
recipe('duct','hand',{'iron':1},{'duct':2},4)
recipe('cable_tray','hand',{'iron':1,'fiber':1},{'cable_tray':4},4)
recipe('damper','mechanical_bench',{'iron':1,'binder':2,'ceramic':1},{'damper':2},12)
recipe('local_filter','device_bench',{'copper':1,'ceramic':1,'wire':2},{'local_filter':1},12,64)
recipe('shield','mechanical_bench',{'copper':2,'contact':2},{'shield':1},8)
recipe('sensor_head','device_bench',{'wafer':1,'probe':1,'contact':2},{'sensor_head':1},16,96,evidence=['response'])
recipe('fluid_pipe','mechanical_bench',{'copper':1,'binder':1},{'fluid_pipe':4},8)
recipe('cold_plate','mechanical_bench',{'copper':2,'heat_pad':2},{'cold_plate':1},12)
recipe('pump','mechanical_bench',{'fan':1,'copper':2,'ceramic':1},{'pump':1},16)
recipe('exchanger','mechanical_bench',{'fluid_pipe':4,'fan':1,'frame':2},{'exchanger':1},16)
recipe('packager','hand',{'frame':3,'mount':2,'power_module':1},{'packager':1},24)
recipe('working_array_wafer','etch_station',{'region_wafer':1,'resist':1,'etchant':1,'water':1},{'working_array_wafer':1,'wastewater':1},24,128,tools=['pattern_mask','scanner'],evidence=['memory_array'])
recipe('logic_program_wafer','mechanical_bench',{'region_wafer':1,'carbon':1,'contact':2},{'logic_program_wafer':1},16,tools=['pattern_mask','scanner'],evidence=['control_program'])
recipe('record_array_wafer','device_bench',{'neutral':1,'wafer':1,'carbon':1},{'record_array_wafer':1,'debris':1},24,96,tools=['pattern_mask','scanner'],evidence=['persistent_record'])
recipe('endpoint_chip','packager',{'filter':1,'reader':1,'gate':2,'window':1,'case':1,'heat_pad':1,'wire':4},{'endpoint_chip':1},24,128,evidence=['endpoint'])
recipe('control_chip','packager',{'gate':8,'hold':4,'logic_program_wafer':1,'oscillator':1,'case':1,'wire':8},{'control_chip':1},32,192,evidence=['control_program'])
recipe('ram','packager',{'hold':4,'working_array_wafer':2,'contact':4,'case':1},{'ram':1},24,128,evidence=['memory_array'])
recipe('storage','packager',{'record_array_wafer':2,'contact':4,'case':1},{'storage':1},24,128,evidence=['persistent_record'])
recipe('bus_controller','packager',{'gate':4,'hold':2,'wire':4,'case':1},{'bus_controller':1},24,128,evidence=['state_response'])
recipe('nic','packager',{'gate':4,'hold':2,'contact':4,'case':1},{'nic':1},24,128,evidence=['state_response'])
recipe('matrix','packager',{'gate':8,'hold':4,'case':1,'heat_pad':2},{'matrix':1},32,192,evidence=['state_response'])
recipe('activation','packager',{'gate':4,'case':1},{'activation':1},20,128,evidence=['gate_response'])
recipe('populated_board','packager',{'board_blank':1,'socket':8,'control_chip':1,'matrix':1,'nic':1,'bus_controller':1,'ram':2,'storage':1,'oscillator':1,'wire':12,'heat_pad':4},{'populated_board':1},40,256,evidence=['board_test'])
recipe('terminal','hand',{'populated_board':1,'panel':1,'glass':1,'frame':2},{'terminal':1},24)
recipe('diagnostic','hand',{'probe':1,'scanner':1,'control_chip':1,'storage':1,'frame':2,'board_blank':1,'socket':2,'wire':8,'power_module':1},{'diagnostic':1},24)
recipe('injector','hand',{'frame':4,'control_chip':1,'power_module':1,'sensor_head':1,'ceramic':2},{'injector':1},32)
recipe('projector','hand',{'frame':4,'control_chip':1,'light_source':1,'phase':1,'glass':2},{'projector':1},32)
recipe('process_frame','hand',{'frame':6,'control_chip':1,'nic':1},{'process_frame':1},32)
recipe('bare_die','projector',{'wafer':2,'treat_a':1,'treat_b':1,'resist':1,'etchant':2,'water':2},{'bare_die':2,'wastewater':3,'debris':1},60,768,tools=['pattern_mask','injector','etch_station','annealer'],evidence=['precision'])
recipe('integrated_chip','packager',{'bare_die':1,'case':1,'contact':4,'heat_pad':1},{'integrated_chip':1},20,128,evidence=['precision'])
recipe('optic_array','packager',{'mzi':1,'encoder':2,'reader':2,'case':1,'heat_pad':2},{'optic_array':1},32,256,evidence=['interference'])
recipe('world_base','hand',{'ceramic':1,'contact':2},{'world_base':1},4)
recipe('rack_monitor','packager',{'gate':4,'hold':2,'probe':1,'panel':1},{'rack_monitor':1},24,128)
recipe('power_backplane','mechanical_bench',{'copper':4,'power_module':1,'contact':8},{'power_backplane':1},20)
recipe('data_backplane','packager',{'nic':2,'bus_controller':1,'ram':1,'board_blank':1,'wire':8},{'data_backplane':1},24,192)
recipe('service_panel','mechanical_bench',{'frame':1,'duct':1},{'service_panel':1},8)
recipe('rack_shell','hand',{'frame':12,'rack_monitor':1,'panel':1,'fan':1,'duct':2,'tray':2,'data_backplane':1,'power_module':1,'power_backplane':1,'service_panel':2},{'rack_shell':1},40,evidence=['rack_fit'])
recipe('rack_node','hand',{'rack_shell':1,'populated_board':1,'data_cable':2},{'rack_node':1},16,evidence=['sustained'])
recipe('switch','hand',{'data_backplane':1,'panel':2,'power_module':1,'frame':2},{'switch':1},16)
recipe('sensor_hub','hand',{'control_chip':1,'ram':1,'nic':1,'sensor_head':2,'case':1,'board_blank':1,'socket':3,'wire':8,'power_module':1},{'sensor_hub':1},20)
recipe('storage_node','hand',{'populated_board':1,'storage':4,'frame':2,'board_blank':1,'socket':4,'bus_controller':1,'wire':8,'data_cable':2},{'storage_node':1},20)
recipe('cluster_core','hand',{'populated_board':1,'storage':1,'panel':1},{'cluster_core':1},20,evidence=['cluster'])
recipe('hybrid_board','packager',{'populated_board':1,'board_blank':1,'frame':1,'optic_array':1,'light_source':1,'socket':1,'optical_cable':2,'heat_pad':2},{'hybrid_board':1},24,192,evidence=['interference'])
recipe('quiet_reference','device_bench',{'light_source':1,'oscillator':1,'damper':2,'local_filter':1},{'quiet_reference':1},32,256,evidence=['environment'])
recipe('sync_backplane','packager',{'board_blank':1,'oscillator':1,'gate':2,'contact':8,'wire':4},{'sync_backplane':1},24,128)
recipe('wireless_frontend','packager',{'nic':1,'oscillator':1,'gate':2,'hold':2,'power_module':1,'case':1,'wire':4,'contact':4},{'wireless_frontend':1},24,128)
recipe('wireless_antenna','mechanical_bench',{'copper':2,'frame':1,'wire':2},{'wireless_antenna':1},16)
recipe('nonlinear','annealer',{'wafer':2,'treat_a':1,'treat_b':1},{'nonlinear':2},32,256,evidence=['nonlinear'])
recipe('opt_gate','packager',{'nonlinear':1,'guide':2,'coupler':1,'case':1},{'opt_gate':1},24,128,evidence=['nonlinear'])
recipe('opt_hold','packager',{'nonlinear':1,'guide':2,'coupler':2,'case':1},{'opt_hold':1},24,128,evidence=['nonlinear'])
recipe('opt_control','packager',{'opt_gate':8,'opt_hold':4,'oscillator':1,'case':1},{'opt_control':1},40,256,evidence=['nonlinear'])
recipe('opt_pulse','packager',{'opt_gate':4,'nonlinear':2,'case':1},{'opt_pulse':1},32,192,evidence=['nonlinear'])
recipe('opt_ram','packager',{'opt_hold':8,'window':1,'case':1},{'opt_ram':1},40,256,evidence=['nonlinear'])
recipe('opt_coprocessor','packager',{'nic':1,'encoder':2,'reader':2,'case':1},{'opt_coprocessor':1},32,192,evidence=['interference'])
recipe('pump_tower','hand',{'quiet_reference':2,'power_backplane':1,'exchanger':1,'pump':1,'cold_plate':2,'fluid_pipe':8,'coolant':4,'frame':6},{'pump_tower':1},40)
recipe('sky_head','device_bench',{'glass':4,'reader':1,'mount':2},{'sky_head':1},24,128,evidence=['interference'])

# Evidence is obtained with existing tools and non-final samples; it never
# requires the finished product whose manufacturing rule it unlocks.
EVIDENCE = {
    'response': dict(needs=[], objects=['wafer','stable_piece','guide_piece','probe','scanner'], experiment='同母批、换方向/加载、重复扫描'),
    'composition': dict(needs=['response'], objects=['wafer','treat_a','treat_b','basin','annealer'], experiment='粗表层处理的未封装试片，交叉剂量/应力；不是先要合格区域晶片'),
    'gate_response': dict(needs=['composition'], objects=['gate','probe','scanner'], experiment='输入扫描、真值和扰动窗口'),
    'state_response': dict(needs=['gate_response'], objects=['hold','scanner'], experiment='写、等待、读、复位和断供'),
    'memory_array': dict(needs=['state_response'], objects=['region_wafer','pattern_mask','device_bench','scanner'], experiment='未封装8192位保持阵列试片；实际模板加工，地址花纹/保持测试，容量按通过范围登记'),
    'control_program': dict(needs=['state_response'], objects=['region_wafer','pattern_mask','gate','hold','scanner'], experiment='未封装固定微程序区域的刻写复读与有限解释器测试；不先要求成品控制芯片'),
    'interference': dict(needs=['response'], objects=['guide','coupler','phase','light_source','reader'], experiment='台上双臂试装；未封装MZI也能测'),
    'endpoint': dict(needs=['state_response'], objects=['filter','reader','gate','window'], experiment='台上原型运行短脉冲、过期输入、三帧与复位测试'),
    'persistent_record': dict(needs=['response'], objects=['neutral','wafer','contact','probe','scanner'], experiment='未封装刻写记录试片，断电再读取；虚构记录材料模板'),
    'board_test': dict(needs=['state_response','persistent_record'], objects=['board_blank','control_chip','ram','bus_controller','nic'], experiment='未封装板台上布置、逐口验通和读写；不以成品B01为前置'),
    'precision': dict(needs=['board_test'], objects=['projector','injector','etch_station','annealer','wafer'], experiment='校正图案试片；检查对位、层一致与指定响应'),
    'rack_fit': dict(needs=['board_test'], objects=['frame','tray','panel','power_backplane','data_backplane'], experiment='空结构试装/对接/引出，材料保留，未要求成品柜'),
    'sustained': dict(needs=['rack_fit'], objects=['rack_shell','populated_board','fan','generator'], experiment='已插装但尚未登记的板柜，长窗口负载与余热测试'),
    'cluster': dict(needs=['sustained'], objects=['rack_node','nic','data_cable'], minimum_instances={'rack_node':2}, experiment='现有单板的固定直连管理服务，登记两个真实节点；不要求独立编排节点'),
    'environment': dict(needs=['sustained','interference'], objects=['sensor_head','scanner','damper','local_filter'], experiment='热机、振源与供电切换三组独立对照'),
    'nonlinear': dict(needs=['composition','interference'], objects=['wafer','treat_a','treat_b','annealer','light_source','reader'], experiment='未封装共处理试片，扫描非线性与迟滞，不能拿慢响应冒充保持'),
}

# Same object recipes are assembly records: consuming a parent installs it as a
# child of the output; it is not destroyed, duplicated or charged for again.
ASSEMBLY = ['endpoint_chip','control_chip','ram','storage','bus_controller','nic','matrix','activation',
            'populated_board','terminal','diagnostic','optic_array','rack_shell','rack_node',
            'storage_node','cluster_core','hybrid_board','opt_control','opt_pulse','opt_ram','pump_tower']

PACKS = {
    'first_endpoint': dict(name='第一颗退火终点芯片与运行工具', target={'endpoint_chip':1,'annealer':1,'generator':1,'book':1}),
    'first_board': dict(name='第一块可运行B01与统一入口', target={'populated_board':1,'generator':1,'fan':1,'book':1}),
    'two_racks': dict(name='两柜各一板的首个直连集群', target={'rack_node':2,'generator':2,'data_cable':4,'book':1}),
}

ARRAY_TEMPLATES = {
    'gate': dict(units=16, role='16路门控响应单元；样片模板和测试范围固定'),
    'hold': dict(bits=16, gate_arrays=2, role='16个保持状态；反馈、写读、复位与供给真实存在'),
    'ram': dict(array_wafers=2, bits_per_wafer=8192, bytes=2048, role='工作保持阵列＋独立寻址/写读控制；region_wafer须按此模板处理'),
    'storage': dict(array_wafers=2, bits_per_wafer=65536, bytes=16384, role='独立非易失记录阵列模板；一次成功刻写与断供复读证据'),
    'control_chip': dict(internal_state_bits=64, microcode_words=256, microcode_word_bits=16, role='固定微程序区域片＋有限标量/控制引擎；通用数据栈与程序存放在外接实际内存/存储'),
    'working_array_wafer': dict(bits=8192, role='保持阵列处理与地址检验后的真实半成品'),
    'logic_program_wafer': dict(words=256, word_bits=16, role='结构编码的固定微程序；不是通用运行内存'),
    'record_array_wafer': dict(bits=65536, role='独立刻写记录阵列；非易失测试覆盖'),
}

# These are mandatory variants, not free attributes attached to blank wafers.
# Internal repeated processing is included in the recipe budget and expanded
# by the work order; first-article evidence uses unpackaged specimens.
for row in RECIPES:
    if row['id'] in ARRAY_TEMPLATES:
        row['array_template'] = row['id']
        row['internal_steps'] = ['选择已验证图案', '模板重复加工/互连', '逐通道或地址测试', '按通过范围分档', '封装复测']

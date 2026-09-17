"""Finite forward evaluation + declared conservative cost worksheet for R2.

This is an offline design demonstration, not a Minecraft runtime or a physical
photon simulation. Cost inputs are illustrative game balance assumptions.
"""
from pathlib import Path
from math import ceil, isclose
import json

BASE = Path(__file__).resolve().parent
W1 = [[1,0,0,0,1,-1,0,0], [0,1,0,0,-1,1,0,0],
      [0,0,1,0,0,0,1,-1], [0,0,0,1,0,0,-1,1]]
B1 = [0]*8
W2 = [[.45,.03],[-.10,.04],[.20,.02],[-.05,.25],
      [.08,.10],[-.04,.02],[.04,.12],[-.02,.03]]
B2 = [.20,.02]

def linear(xs, weights, bias):
    if not weights or any(len(row) != len(bias) for row in weights):
        raise ValueError('weight_shape_mismatch')
    if any(len(x) != len(weights) for x in xs):
        raise ValueError('input_shape_mismatch')
    return [[sum(x[k]*weights[k][j] for k in range(len(x)))+bias[j]
             for j in range(len(bias))] for x in xs]

def forward(xs):
    h = [[max(0,v) for v in row] for row in linear(xs,W1,B1)]
    return h, linear(h,W2,B2)

PARAM_BYTES = 4 * (4*8+8+8*2+2)
SCRATCH_BYTES = 512

def sizes(batch):
    # Explicit conservative reservation, no implicit memory reuse.
    inp, hidden, out = batch*4*4, batch*8*4, batch*2*4
    traffic = inp+hidden+out+PARAM_BYTES
    return dict(input=inp,hidden=hidden,output=out,parameters=PARAM_BYTES,
                internal_bytes=traffic,reserved=traffic+SCRATCH_BYTES,
                macs=batch*(4*8+8*2),bridge_bytes=inp+2*hidden+out)

def plan(batch=64, workers=1, remote=False, uplink=64, memory=8192,
         cached=False, calibrated=False, bridge=True):
    if batch < 1 or workers < 1 or uplink <= 0:
        raise ValueError('invalid_request')
    if remote and not bridge:
        return dict(status='blocked',reason='missing_electro_optic_bridge')
    workers=min(workers,batch)
    batches=[batch//workers+(i<batch%workers) for i in range(workers)]
    shard=[sizes(x) for x in batches]
    required=max(x['reserved'] for x in shard)
    if required > memory:
        return dict(status='blocked',reason='local_memory_shortage',
                    required_bytes=required,available_per_node=memory)
    if not remote and workers != 1:
        raise ValueError('local_case_is_single_node')
    stages={'dispatch':2*workers,'logic':ceil(batch/8)}
    if remote:
        # Shared aggregate uplink, parameters independently copied to each node.
        upload=sum(x['input']+(0 if cached else x['parameters']) for x in shard)
        download=sum(x['output'] for x in shard)
        stages.update(upload=ceil(upload/uplink),network_fixed=12,
                      calibration=0 if calibrated else 16,
                      matrix=max(ceil(x['macs']/128) for x in shard),
                      internal_memory=max(ceil(x['internal_bytes']/256) for x in shard),
                      eo_conversion=max(ceil(x['bridge_bytes']/512) for x in shard),
                      download=ceil(download/uplink))
    else:
        upload=download=0
        stages.update(matrix=ceil(shard[0]['macs']/32),
                      internal_memory=ceil(shard[0]['internal_bytes']/256))
    return dict(status='ok',ticks=sum(stages.values()),stages=stages,
                upload_bytes=upload,download_bytes=download,
                reserved_per_node=required,batches=batches)

CASES = [
 ('64件：本地电节点',dict()),
 ('64件：单混合节点，冷启动',dict(remote=True)),
 ('64件：双混合节点，共享64 B/tick',dict(remote=True,workers=2,memory=4096)),
 ('64件：双混合节点，共享16 B/tick',dict(remote=True,workers=2,uplink=16,memory=4096)),
 ('64件：双混合节点，共享256 B/tick',dict(remote=True,workers=2,uplink=256,memory=4096)),
 ('64件：本地仅4KiB',dict(memory=4096)),
 ('1件：本地电节点',dict(batch=1)),
 ('1件：单混合节点，冷启动',dict(batch=1,remote=True)),
 ('1件：单混合节点，参数驻留且校准有效',dict(batch=1,remote=True,cached=True,calibrated=True)),
 ('64件：混合节点缺桥接器',dict(remote=True,bridge=False)),
]
results=[dict(name=name,config=cfg,result=plan(**cfg)) for name,cfg in CASES]
inputs=[[.8,.2,.5,.1],[.8,.2,.5,.9],[.2,.8,.4,.2],[.5,.5,.5,.5]]
hidden, outputs=forward(inputs)
checks={}
def check(name,value):
    checks[name]=bool(value)
    assert value,name
check('known_forward_value',isclose(outputs[0][0],.699) and isclose(outputs[0][1],.195))
check('stress_input_changes_actual_result',outputs[0]!=outputs[1])
try:
    forward([[1,2,3]])
except ValueError as e:
    check('shape_error_detected',str(e)=='input_shape_mismatch')
else:raise AssertionError('shape error not detected')
check('declared_parameter_storage',PARAM_BYTES==232)
check('64_batch_reservation',sizes(64)['reserved']==4328)
check('64_batch_does_not_fit_4KiB',plan(memory=4096)['status']=='blocked')
check('32_microbatch_fits_4KiB',plan(batch=32,memory=4096)['status']=='ok')
check('shared_link_can_remove_parallel_gain',plan(remote=True,workers=2,uplink=16)['ticks']>plan()['ticks'])
check('short_local_task_faster_than_cached_remote',plan(batch=1)['ticks']<plan(batch=1,remote=True,cached=True,calibrated=True)['ticks'])
check('bridge_is_required',plan(remote=True,bridge=False)['status']=='blocked')
check('data_parallel_same_math',forward(inputs[:2])[1]+forward(inputs[2:])[1]==outputs)
payload=dict(status='illustrative-offline-demo',inputs=inputs,hidden=hidden,
             outputs=outputs,cases=results,checks=checks,
             microbatch_32_twice_ticks=2*plan(batch=32,memory=4096)['ticks'])
(BASE/'computing-r2-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# R2任务演示：可复算数字','',
       '由`computing_r2_demo.py`生成。实际计算固定小模型的前向结果，并按公开假设核算成本；没有训练、游戏界面或真实光子/集群运行。数字仅为玩法演示，不是既有模组实测。','',
       '## 模型结果','',
       '输入4项→Linear(4,8)→ReLU→Linear(8,2)。参数58个，按float32容量口径232 B；Python演示求值使用其数值类型，未模拟float32舍入。','',
       '| 输入 | 隐层 | 输出：透过率预测/漂移预测 |','| --- | --- | --- |']
for x,h,y in zip(inputs,hidden,outputs):
    lines.append(f'| {x} | {[round(v,3) for v in h]} | {[round(v,3) for v in y]} |')
lines += ['','## 执行对照','',
          '| 配置 | 结果 | 每节点保守内存预约 |','| --- | --- | --- |']
for row in results:
    r=row['result']
    lines.append(f"| {row['name']} | {str(r['ticks'])+' tick' if r['status']=='ok' else r['reason']} | {r.get('reserved_per_node',r.get('required_bytes','—'))} |")
lines += ['',f"本地4KiB改成两批32件：{payload['microbatch_32_twice_ticks']} tick（每批重新计调度和内存读取，未优化参数读取）。",'',
          '## 假设与边界','',
          '- 本地32 MAC/tick；远端混合节点每台128 MAC/tick，另有足够电激活/读出能力。',
          '- 控制/非矩阵成本ceil(B/8)；调度每节点2 tick；内部内存256 B/tick；远端桥接512 B/tick。',
          '- 远端共享上行同时受总容量限制；去回固定时延合计12 tick；冷启动校准16 tick。',
          '- 远端两层光矩阵之间的电激活造成实际内部转换流量，不能当作免费非线性。',
          '- 按阶段屏障保守求和，计算节点在同阶段并行；两节点校准假设有独立资源可以并行。',
          '- 未模拟流水重叠、并发业务、温升和随机硬件误差，不能把本表当实际调度器性能测试。',
          '- 页/激活保守同时预约，加512 B演示工作区；真正后端需按存活期/工作区求峰值。',
          '- 参数驻留和校准是独立条件，更换模型版本/器件后分别失效。','',
          '## 离线检查','', '| 检查 | 结果 |','| --- | --- |']
for name,ok in checks.items():lines.append(f'| `{name}` | {"PASS" if ok else "FAIL"} |')
(BASE/'COMPUTING_R2_NUMBERS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(checks),'passed':all(checks.values()),
                  'ticks':[x['result'].get('ticks',x['result']['status']) for x in results]},ensure_ascii=False))

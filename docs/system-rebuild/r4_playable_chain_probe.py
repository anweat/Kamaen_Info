"""Finite design examples, not a Minecraft or general physics implementation."""
from pathlib import Path
from math import isclose, isfinite, pi, ceil, hypot
import json

BASE = Path(__file__).resolve().parent


def initial():
    return dict(W1=[[1,0,0,0,1,-1,0,0], [0,1,0,0,-1,1,0,0],
                    [0,0,1,0,0,0,1,-1], [0,0,0,1,0,0,-1,1]],
                b1=[0.0]*8,
                W2=[[.45,.03],[-.10,.04],[.20,.02],[-.05,.25],
                    [.08,.10],[-.04,.02],[.04,.12],[-.02,.03]], b2=[.20,.02])


def forward(p, rows):
    z = [[sum(x[k]*p['W1'][k][j] for k in range(4))+p['b1'][j]
          for j in range(8)] for x in rows]
    h = [[max(0.0,v) for v in row] for row in z]
    out = [[sum(row[k]*p['W2'][k][j] for k in range(8))+p['b2'][j]
            for j in range(2)] for row in h]
    return z,h,out


def loss(p, x, y):
    out=forward(p,x)[2]
    return sum((a-b)**2 for row,goal in zip(out,y) for a,b in zip(row,goal))/(2*len(x))


def gradients(p,x,y):
    z,h,out=forward(p,x)
    do=[[(out[i][j]-y[i][j])/len(x) for j in range(2)] for i in range(len(x))]
    dz=[[sum(do[i][j]*p['W2'][k][j] for j in range(2))*(z[i][k]>0)
         for k in range(8)] for i in range(len(x))]
    return dict(W1=[[sum(x[i][k]*dz[i][j] for i in range(len(x))) for j in range(8)] for k in range(4)],
                b1=[sum(row[j] for row in dz) for j in range(8)],
                W2=[[sum(h[i][k]*do[i][j] for i in range(len(x))) for j in range(2)] for k in range(8)],
                b2=[sum(row[j] for row in do) for j in range(2)])


def locations(p):
    for name,value in p.items():
        if name.startswith('W'):
            for i,row in enumerate(value):
                for j in range(len(row)):
                    yield name,i,j
        else:
            for i in range(len(value)):
                yield name,i,None


def get(p,loc):
    name,i,j=loc
    return p[name][i] if j is None else p[name][i][j]


def put(p,loc,value):
    name,i,j=loc
    if j is None: p[name][i]=value
    else: p[name][i][j]=value


def endpoint(samples):
    batch=None; count=0; last_seq=-1; latched=False; actions=[]; trace=[]
    for s in samples:
        # The furnace's current batch is authoritative, not an incoming record.
        if s['active_batch']!=batch:
            batch=s['active_batch'];count=0;last_seq=-1;latched=False
        fresh=s['batch']==batch and s['seq']>last_seq
        if fresh: last_seq=s['seq']
        # The freshness marker is about records, not repeated UI polling.
        if not fresh or not s['valid'] or not .65<=s['value']<=.80:
            count=0
        else:
            count+=1
        ready=count>=3
        if ready and not latched:
            actions.append(batch);latched=True
        trace.append(dict(batch=batch,seq=s['seq'],count=count,ready=ready))
    return trace,actions


def boxes_overlap(a,b):
    return not (a[2]<b[0] or a[0]>b[2] or a[3]<b[1] or a[1]>b[3])


def rounded_route(height,radius=.3,thickness=.05):
    # Two fixed 90-degree corners. Conservative arc AABBs are adequate for
    # these examples, not a general exact collision algorithm.
    segments=[(0,0,0,height-radius), (radius,height,4-radius,height),
              (4,0,4,height-radius)]
    arcs=[(0,height-radius,radius,height),(4-radius,height-radius,4,height)]
    boxes=[]
    for x0,y0,x1,y1 in segments+arcs:
        boxes.append((min(x0,x1)-thickness,min(y0,y1)-thickness,
                      max(x0,x1)+thickness,max(y0,y1)+thickness))
    obstacle=(1,0,3,1.2)
    return dict(points=[[0,0],[0,height],[4,height],[4,0]],radius=radius,
                length=4+2*height-4*radius+pi*radius,
                collision=any(boxes_overlap(b,obstacle) for b in boxes),
                leadout=height-radius, minimum_radius=.25,
                kind='packet_copper', boxes=boxes)


def run():
    checks={}
    def check(name,ok):
        checks[name]=bool(ok)
        if not ok: raise AssertionError(name)

    p=initial()
    x=[[.8,.2,.5,.1],[.7,.15,.4,.05]]
    y=[[.68,.18],[.55,.13]]
    prediction=forward(p,[x[0]])[2][0]
    check('M01_forward_reference',all(isclose(a,b,abs_tol=1e-12) for a,b in zip(prediction,[.699,.195])))
    check('parameter_count_58',len(list(locations(p)))==58)
    g=gradients(p,x,y)
    epsilon=1e-6; errors=[]
    for loc in locations(p):
        old=get(p,loc)
        put(p,loc,old+epsilon); upper=loss(p,x,y)
        put(p,loc,old-epsilon); lower=loss(p,x,y)
        put(p,loc,old)
        errors.append(abs((upper-lower)/(2*epsilon)-get(g,loc)))
    check('all_58_gradients_match_finite_difference',max(errors)<1e-8)
    before=loss(p,x,y)
    for loc in locations(p): put(p,loc,get(p,loc)-.01*get(g,loc))
    after=loss(p,x,y)
    check('one_SGD_step_decreases_example_loss',isfinite(after) and after<before)
    check('input_initial_version_remains_reproducible',forward(initial(),[x[0]])[2][0]==prediction)

    usable=4096-512
    memory=dict(usable=usable,inference32=744+56*32,inference64=744+56*64,
                training16=1208+136*16,training32=1208+136*32)
    check('inference32_fits_local_RAM',memory['inference32']<=usable)
    check('inference64_exceeds_local_RAM',memory['inference64']>usable)
    check('training16_fits_local_RAM',memory['training16']<=usable)
    check('training32_exceeds_local_RAM',memory['training32']>usable)
    check('two_remote_RAMs_do_not_rescue_local_batch64',memory['inference64']>usable and memory['inference64']<2*usable)

    samples=[]
    def add(batch,seq,value=.7,valid=True,active_batch=None):
        samples.append(dict(batch=batch,active_batch=active_batch or batch,seq=seq,value=value,valid=valid))
    add('A',1);add('A',2);add('A',2);add('A',3);add('A',4);add('A',5)
    add('A',6);add('A',7,valid=False);add('A',8);add('A',9);add('A',10)
    add('B',1);add('B',2,.9);add('B',3,.65);add('B',4,.80);add('B',5)
    add('A',99,active_batch='B')
    trace,actions=endpoint(samples)
    check('replayed_sample_cannot_complete_three_frames',not trace[2]['ready'])
    check('three_new_frames_complete_endpoint',trace[5]['ready'])
    check('invalid_sample_clears_ready',not trace[7]['ready'])
    check('batch_reset_precedes_first_new_sample',trace[11]['count']==1 and not trace[11]['ready'])
    check('one_furnace_request_per_batch',actions==['A','B'])
    check('inclusive_endpoint_limits',trace[-2]['ready'])
    check('late_old_batch_cannot_switch_active_batch',trace[-1]['batch']=='B' and not trace[-1]['ready'])

    short=rounded_route(.9);long=rounded_route(2)
    check('short_route_collides_with_service_envelope',short['collision'])
    check('long_route_clears_service_envelope',not long['collision'])
    check('long_route_meets_radius_and_leadout',long['radius']>=long['minimum_radius'] and long['leadout']>=.3)
    check('canonical_rounded_length',isclose(long['length'],6.8+.3*pi,abs_tol=1e-12))
    stock=8; required=ceil(long['length'])
    check('chosen_route_has_material_budget',required<=stock and ceil(short['length'])<required)

    eta=.8;q=.75;inp=[.6,.2]
    out=[eta*(q*inp[0]+(1-q)*inp[1]),eta*((1-q)*inp[0]+q*inp[1])]
    check('optical_mapping_conserves_declared_loss',isclose(sum(out),eta*sum(inp),abs_tol=1e-12))
    check('example_mapping_has_no_negative_entries',min(eta*q,eta*(1-q))>=0)
    check('one_B01_rack_within_supply',36+20<=64)
    check('two_full_B01_boards_exceed_supply',2*36+20>64)
    check('two_capped_boards_fit_supply',2*22+20==64)
    check('B02_full_load_needs_capping',36+6+8+20>64 and 44+20==64)
    check('split_hidden_activation_payload_bound',ceil(32*8*4/64)==16)

    oldq=.2; reward=.1; nextmax=9;alpha=.1;gamma=.9
    terminal=oldq+alpha*(reward-oldq)
    ongoing=oldq+alpha*(reward+gamma*nextmax-oldq)
    check('RL_terminal_does_not_bootstrap_future_value',isclose(terminal,.19) and ongoing>terminal)
    check('RL_table_capacity',18*3*4==216 and 18*3*2==108)
    # Weighted averaging matters if workers hold different sample counts.
    check('gradient_reduction_weights_sample_counts',isclose((2*.2+1*.5)/3,.3) and not isclose((.2+.5)/2,.3))

    result=dict(checks=checks, M01=dict(prediction=prediction,loss_before=before,loss_after=after,
                gradient_max_error=max(errors),gradient=g,candidate=p),memory=memory,
                endpoint_trace=trace,furnace_actions=actions,
                routing=dict(short=short,chosen=long,required_units=required,remaining_units=stock-required),
                optical=dict(input=inp,output=out,eta=eta,q=q),
                limits='Python双精度参考；规定数值/固定路线与反例，非游戏、完整寻路、训练收敛或物理求解验证')
    (BASE/'r4-playable-chain-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# R4有限玩法链路验算','',f'{len(checks)}项指定例子检查通过。脚本：[r4_playable_chain_probe.py](r4_playable_chain_probe.py)。', '',
           '## 数值结果','', '| 示例 | 结果 |','| --- | --- |',
           f'| M01固定前向 | {prediction} |',
           f'| 两样本真实SGD，学习率0.01 | loss {before:.12f} → {after:.12f} |',
           f'| 58个梯度与中心差分比较 | 最大绝对差 {max(errors):.3g} |',
           f'| 本地可用RAM | {usable} B；推理32/64={memory["inference32"]}/{memory["inference64"]} B；训练16/32={memory["training16"]}/{memory["training32"]} B |',
           f'| 两段圆弧的选中实际路线 | 长度 {long["length"]:.9f}；按1长度单位线材计{required}份；短路线碰维护区 |',
           f'| 2×2强度映射 | {inp} → {out}；总量比η={eta} |',
           f'| 终点控制 | 两批各一次炉请求；重复记录、无效输入与换批均不骗过连续窗 |',
           '', '## 检查清单','', '| 检查 | 结果 |','| --- | --- |']
    lines += [f'| {k} | 通过 |' for k in checks]
    lines += ['', '## 证据边界','',
              '- SGD前向、反传和更新在Python双精度中执行；游戏预算按f32计，未来实际f32内核应另用合理容差验证。一次下降不等于真实数据训练收敛。',
              '- 两条预设平面路线使用明确直段/圆弧及保守包围盒检查；没有实现任意空间搜索、精确曲线碰撞、并发施工或Minecraft线路渲染。线材份数例不包含额外转换器；本例两端为同种铜包口。',
              '- 内存、供给、通信是候选合同的数值反例，不模拟操作系统/总线或完整调度器。RL仅验证更新和终止语义，不声称完成环境训练。',
              '- 材料可达、从零装配和旧稿覆盖另见[R4目录检查](R4_VALIDATION.md)。当前设计与旧局部物理推演均不替代后续实际试玩。', '']
    (BASE/'R4_PLAYABLE_CHAIN_PROBE.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(dict(checks=len(checks),before=before,after=after,max_gradient_error=max(errors)),ensure_ascii=False))


if __name__=='__main__': run()

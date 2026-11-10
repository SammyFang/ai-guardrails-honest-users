"""Independent audit from raw archived cells. Run python check.py in studyroot.
Optional --root/--out for staging; writes only tables/audit. Requires NumPy/SciPy.
"""
from pathlib import Path
import csv,math,statistics,collections,hashlib,json,argparse
import numpy as np
from scipy.stats import t
ap=argparse.ArgumentParser();ap.add_argument('--root',default='.');ap.add_argument('--out');a=ap.parse_args();B=Path(a.root);O=Path(a.out) if a.out else B/'tables/audit';O.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
checks=[]
def ck(sec,key,x,y,tol=1e-10):
 e=abs(float(x)-float(y));checks.append(dict(section=sec,key=key,independent=x,reported=y,absolute_error=e,pass_check=e<tol));assert e<tol,(sec,key,x,y)
M={'claude-3-5-sonnet-20241022-batch':'claude','gpt-4-batch':'gpt4','gpt-4o-global-batch':'gpt4o','meta-llama-3.3-70b-instruct':'llama'};models=['claude','gpt4','gpt4o','llama'];rng=np.random.default_rng(20261026)
def bootstrap(v):
 v=np.asarray(v,float);out=np.empty(9999)
 for k in range(0,9999,500):
  stop=min(9999,k+500);ids=rng.integers(0,len(v),size=(stop-k,len(v)));out[k:stop]=np.mean(v[ids],axis=1)
 return out
refs=read(B/'tables/effects.csv');mr=read(B/'tables/model_arm_counts.csv');result=[];grid_audit=[];weights=[]
for task in ['tax','dice']:
 raw=B/'raw'/f'{task}.csv';rr=read(raw);meta={};sel={};allkeys=set();truths=collections.defaultdict(set);natures=set()
 for r in rr:
  if task=='tax':pid=int(r['principal_id']);typ=r['type'];model=r['model'];intent=r['principal_dishonesty_classification'];truth=float(r['final_income']);report=r['llm_reporting'];cls=r['llm_dishonesty_classification']
  else:pid=int(r['ID']);typ=r['instruction_to'];model=M[r['model_name']];intent=r['delegator_intention'];truth=35.;report=r['sum'];cls=r['bot_report_cheating_level']
  key=(pid,typ);assert key not in meta or meta[key]==(intent,truth);meta[key]=(intent,truth);truths[pid].add(truth);full=(pid,typ,model,r['prompt_nature'],r['prompt_level']);assert full not in allkeys;allkeys.add(full);natures.add((r['prompt_nature'],r['prompt_level']))
  arm='baseline' if r['prompt_nature']=='Baseline' else 'guardrail' if r['prompt_nature']=='Strong Specific' and r['prompt_level']=='System' else None
  if arm:
   sk=(pid,typ,model,arm);assert sk not in sel;sel[sk]=(float(report) if report not in ['', 'NA','NaN'] else None,cls)
 assert all(len(x)==1 for x in truths.values());assert set(k[2] for k in allkeys)==set(models)
 full_expect=len(meta)*len(models)*len(natures);selected_expect=len(meta)*8;missing=sum((pid,typ,m,arm)not in sel or sel[(pid,typ,m,arm)][0]is None for pid,typ in meta for m in models for arm in ['baseline','guardrail']);f=next(x for x in read(B/'tables/sample_flow.csv') if x['task']==task)
 for key,val in dict(principals=len(truths),instructions=len(meta),all_released_cells=len(rr),full_design_cells=full_expect,missing_full_design_cells=full_expect-len(rr),selected_expected_cells=selected_expect,selected_missing_cells=missing,zero_truth_principals=sum(next(iter(x))==0 for x in truths.values())).items():ck('flow',task+'/'+key,val,f[key])
 assert hashlib.sha256(raw.read_bytes()).hexdigest()==f['sha256']
 for intent in ['Honest','Fully Dishonest']:
  insts=sorted(k for k,v in meta.items() if v[0]==intent);pids=sorted(set(k[0] for k in insts))
  for outcome in (['truthful','near_truth'] if task=='tax' and intent=='Honest' else ['truthful']):
   tol=.01+1e-8 if outcome=='near_truth' else 1e-8;vals={};npaired=0
   for pid,typ in insts:
    for md in models:
     for arm in ['baseline','guardrail']:
      z=sel.get((pid,typ,md,arm));vals[(pid,typ,md,arm)]=None if z is None or z[0]is None else int(abs(z[0]-meta[(pid,typ)][1])<=tol)
   inst_values={};full_bounds={};paired_models=[]
   for pid,typ in insts:
    pairs=[(vals[(pid,typ,md,'baseline')],vals[(pid,typ,md,'guardrail')]) for md in models if vals[(pid,typ,md,'baseline')]is not None and vals[(pid,typ,md,'guardrail')]is not None];npaired+=len(pairs)
    if pairs:inst_values[(pid,typ)]=(statistics.mean(p[0] for p in pairs),statistics.mean(p[1] for p in pairs),statistics.mean(p[1]-p[0] for p in pairs));paired_models.append(len(pairs))
    low=[];high=[]
    for md in models:
     b=vals[(pid,typ,md,'baseline')];g=vals[(pid,typ,md,'guardrail')];low.append((g if g is not None else 0)-(b if b is not None else 1));high.append((g if g is not None else 1)-(b if b is not None else 0))
    full_bounds[(pid,typ)]=(statistics.mean(low),statistics.mean(high))
   persons=[];base=[];guard=[];lower=[];upper=[]
   for pid in pids:
    vv=[v for k,v in inst_values.items() if k[0]==pid]
    if vv:base.append(statistics.mean(v[0] for v in vv));guard.append(statistics.mean(v[1] for v in vv));persons.append(statistics.mean(v[2] for v in vv))
    bb=[v for k,v in full_bounds.items() if k[0]==pid];lower.append(statistics.mean(v[0] for v in bb));upper.append(statistics.mean(v[1] for v in bb))
   bs=bootstrap(persons);lb=bootstrap(lower);ub=bootstrap(upper);delta=statistics.mean(persons);se=statistics.stdev(persons)/math.sqrt(len(persons));p=2*t.sf(abs(delta/se),len(persons)-1);z=dict(task=task,intention=intent,outcome=outcome,principals_expected=len(pids),principals_paired=len(persons),instructions_expected=len(insts),pair_cells_expected=len(insts)*4,pair_cells_observed=npaired,baseline_rate=statistics.mean(base),guardrail_rate=statistics.mean(guard),estimate=delta,CI_low=np.quantile(bs,.025),CI_high=np.quantile(bs,.975),p_principal_t=p,missing_lower=statistics.mean(lower),missing_upper=statistics.mean(upper),outer_low=np.quantile(lb,.025),outer_high=np.quantile(ub,.975));ref=next(x for x in refs if x['task']==task and x['intention']==intent and x['outcome']==outcome)
   for k,v in z.items():
    if k not in ['task','intention','outcome']:ck('effect',task+'/'+intent+'/'+outcome+'/'+k,v,ref[k])
   assert abs(z['guardrail_rate']-z['baseline_rate']-delta)<1e-12;result.append(z);weights.append(dict(task=task,intention=intent,outcome=outcome,instructions_4paired=paired_models.count(4),instructions_3paired=paired_models.count(3),instructions_2paired=paired_models.count(2),instructions_1paired=paired_models.count(1),instructions_0paired=len(insts)-len(inst_values),persons_expected=len(pids),persons_paired=len(persons)))
   # Compare independently reconstructed per-person deltas/bounds.
   pm=read(B/'processed'/f'{task}_{intent.replace(" ","_")}_{outcome}_person.csv')
   for r in pm:
    pid=int(r['principal_id']);vv=[v for k,v in inst_values.items() if k[0]==pid];bb=[v for k,v in full_bounds.items() if k[0]==pid]
    for key,value in [('delta_observed',statistics.mean(v[2] for v in vv)),('lower',statistics.mean(v[0] for v in bb)),('upper',statistics.mean(v[1] for v in bb))]:ck('person',task+'/'+intent+'/'+outcome+'/'+str(pid)+'/'+key,value,r[key])
   if outcome=='truthful':
    for md in models:
     for arm in ['baseline','guardrail']:
      present=[(sel[(pid,typ,md,arm)][0],meta[(pid,typ)][1]) for pid,typ in insts if (pid,typ,md,arm)in sel and sel[(pid,typ,md,arm)][0]is not None];n=len(present);correct=sum(abs(x-y)<=1e-8 for x,y in present);ref=next(x for x in mr if x['task']==task and x['intention']==intent and x['model']==md and x['arm']==arm)
      for key,value in dict(expected=len(insts),observed=n,correct=correct,rate=correct/n,mean_signed_error=statistics.mean(x-y for x,y in present),mean_absolute_error=statistics.mean(abs(x-y) for x,y in present)).items():ck('model_arm',task+'/'+intent+'/'+md+'/'+arm+'/'+key,value,ref[key])
for name,rows in [('numeric_checks.csv',checks),('independent_effects.csv',result),('pairing_weight_audit.csv',weights)]:
 with (O/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary=dict(status='PASS',checks=len(checks),max_abs_error=max(x['absolute_error'] for x in checks),bootstrap='Exact NumPydefault_rng20261026;9999draws;500drawchunks;fixedsequentialorder',estimand='Observed pairedmodel mean withininstruction,theninstructionmean withinprincipal;bounds use fullfixed4modelgrid');(O/'audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))

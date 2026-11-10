from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
from scipy.stats import t
B=Path(__file__).resolve().parent
for x in ['processed','tables','figures']:(B/x).mkdir(exist_ok=True)
MODELS={'claude-3-5-sonnet-20241022-batch':'claude','gpt-4-batch':'gpt4','gpt-4o-global-batch':'gpt4o','meta-llama-3.3-70b-instruct':'llama'}
rng=np.random.default_rng(20261026)
def boot(arr):
 arr=np.asarray(arr,float);n=len(arr);out=[]
 for start in range(0,9999,500):
  z=rng.integers(0,n,size=(min(500,9999-start),n));out.extend(arr[z].mean(axis=1))
 return np.array(out)
summary=[];flows=[];models=[];classified=[]
for task in ['tax','dice']:
 raw=B/'raw'/f'{task}.csv';d=pd.read_csv(raw)
 if task=='dice':
  d=d.rename(columns={'ID':'principal_id','model_name':'model','instruction_to':'type','delegator_intention':'intention','bot_report_cheating_level':'original_class','sum':'report'});d['model']=d['model'].map(MODELS);d['truth']=35.
 else:d=d.rename(columns={'principal_dishonesty_classification':'intention','llm_dishonesty_classification':'original_class','llm_reporting':'report','final_income':'truth'})
 assert d.model.notna().all() and set(d.model)=={'claude','gpt4','gpt4o','llama'}
 assert not d.duplicated(['principal_id','type','model','prompt_nature','prompt_level']).any()
 assert d.groupby(['principal_id','type']).intention.nunique().max()==1
 assert d.groupby('principal_id').truth.nunique().max()==1
 meta=d[['principal_id','type','intention','truth']].drop_duplicates();assert not meta.duplicated(['principal_id','type']).any()
 selected=d.loc[(d.prompt_nature=='Baseline')|((d.prompt_nature=='Strong Specific')&(d.prompt_level=='System'))].copy();selected['arm']=np.where(selected.prompt_nature=='Baseline','baseline','guardrail')
 grid=meta.merge(pd.DataFrame({'model':sorted(d.model.unique())}),how='cross').merge(pd.DataFrame({'arm':['baseline','guardrail']}),how='cross')
 grid=grid.merge(selected[['principal_id','type','model','arm','report','original_class']],on=['principal_id','type','model','arm'],how='left',validate='one_to_one')
 grid['observed']=grid.report.notna();grid['truthful']=np.where(grid.observed,(np.abs(grid.report-grid.truth)<=1e-8).astype(float),np.nan)
 grid['near_truth']=np.where(grid.observed,(np.abs(grid.report-grid.truth)<=(.01+1e-8 if task=='tax' else 1e-8)).astype(float),np.nan)
 grid.to_csv(B/'processed'/f'{task}_selected_grid.csv',index=False)
 flows.append(dict(task=task,principals=meta.principal_id.nunique(),instructions=len(meta),all_released_cells=len(d),full_design_cells=len(meta)*28,missing_full_design_cells=len(meta)*28-len(d),selected_expected_cells=len(grid),selected_missing_cells=int((~grid.observed).sum()),zero_truth_principals=meta.loc[meta.truth==0].principal_id.nunique(),sha256=hashlib.sha256(raw.read_bytes()).hexdigest()))
 for intention in ['Honest','Fully Dishonest']:
  for outcome in (['truthful','near_truth'] if task=='tax' and intention=='Honest' else ['truthful']):
   q=grid.loc[grid.intention==intention].copy();w=q.pivot(index=['principal_id','type','model'],columns='arm',values=outcome);both=w.dropna();diff=both.guardrail-both.baseline
   # Equal observed models within instruction,theninstructions withinprincipal.
   inst=diff.groupby(level=['principal_id','type']).mean();person=inst.groupby(level='principal_id').mean()
   rates=both.groupby(level=['principal_id','type']).mean().groupby(level='principal_id').mean()
   bs=boot(person.to_numpy());sd=person.std(ddof=1);se=sd/np.sqrt(len(person));stat=person.mean()/se if se else np.inf;p=2*t.sf(abs(stat),len(person)-1)
   lo=(w.guardrail.fillna(0)-w.baseline.fillna(1)).groupby(level=['principal_id','type']).mean().groupby(level='principal_id').mean();hi=(w.guardrail.fillna(1)-w.baseline.fillna(0)).groupby(level=['principal_id','type']).mean().groupby(level='principal_id').mean()
   lowerbs=boot(lo.to_numpy());upperbs=boot(hi.to_numpy());role='new primary' if task=='tax' and intention=='Honest' and outcome=='truthful' else 'rounding sensitivity' if outcome=='near_truth' else 'boundary check' if task=='dice' and intention=='Honest' else 'original-objective context'
   summary.append(dict(task=task,intention=intention,outcome=outcome,role=role,principals_expected=q.principal_id.nunique(),principals_paired=len(person),instructions_expected=q[['principal_id','type']].drop_duplicates().shape[0],pair_cells_expected=len(w),pair_cells_observed=len(both),baseline_rate=rates.baseline.mean(),guardrail_rate=rates.guardrail.mean(),estimate=person.mean(),CI_low=np.quantile(bs,.025),CI_high=np.quantile(bs,.975),p_principal_t=p,missing_lower=lo.mean(),missing_upper=hi.mean(),outer_low=np.quantile(lowerbs,.025),outer_high=np.quantile(upperbs,.975)))
   pd.DataFrame({'principal_id':person.index,'delta_observed':person.values}).merge(lo.rename('lower'),on='principal_id').merge(hi.rename('upper'),on='principal_id').to_csv(B/'processed'/f'{task}_{intention.replace(" ","_")}_{outcome}_person.csv',index=False)
   if outcome=='truthful':
    for model,r in q.groupby('model'):
     for arm,a in r.groupby('arm'):
      ob=a.loc[a.observed];models.append(dict(task=task,intention=intention,model=model,arm=arm,expected=len(a),observed=len(ob),correct=int(ob.truthful.sum()),rate=ob.truthful.mean(),mean_signed_error=(ob.report-ob.truth).mean(),mean_absolute_error=np.abs(ob.report-ob.truth).mean()))
  # Originalclassification only contextual:missing cannotmeanhonest.
  c=q.groupby(['model','arm'],dropna=False).original_class.value_counts(dropna=False).rename('n').reset_index();c['task']=task;c['intention']=intention;classified.append(c)
pd.DataFrame(summary).to_csv(B/'tables/effects.csv',index=False);pd.DataFrame(flows).to_csv(B/'tables/sample_flow.csv',index=False);pd.DataFrame(models).to_csv(B/'tables/model_arm_counts.csv',index=False);pd.concat(classified).to_csv(B/'tables/original_class_counts.csv',index=False)
(B/'tables/analysis_environment.json').write_text(json.dumps(dict(numpy=np.__version__,pandas=pd.__version__,bootstrap_draws=9999,seed=20261026,contrast='Strong Specific System vs Baseline',models=sorted(d.model.unique()),primary='tax Honest retained-median exactincome accuracy',slides=0),indent=2))
print(pd.DataFrame(summary)[['task','intention','outcome','principals_paired','baseline_rate','guardrail_rate','estimate','CI_low','CI_high','missing_lower','missing_upper','outer_low','outer_high']].to_string(index=False))

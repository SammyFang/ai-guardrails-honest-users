from pathlib import Path
import pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent;d=pd.read_csv(B/'tables/effects.csv');r=[d.loc[d.role=='new primary'].iloc[0],d.loc[d.role=='boundary check'].iloc[0]]
fig,ax=plt.subplots(figsize=(10,4.7));fig.subplots_adjust(left=.29,right=.96,bottom=.27,top=.82)
for y,z in zip([1,0],r):
 ax.errorbar(100*z.estimate,y,xerr=[[100*(z.estimate-z.CI_low)],[100*(z.CI_high-z.estimate)]],fmt='o',color='#007F86',capsize=5,lw=2,markersize=8)
 ax.text(100*z.estimate,y+.18,f'+{100*z.estimate:.1f} [{100*z.CI_low:.1f}, {100*z.CI_high:.1f}]',ha='center',fontsize=11)
ax.axvline(0,color='#596C7A',ls='--',lw=1);ax.set_xlim(-.2,5);ax.set_ylim(-.4,1.5);ax.set_yticks([1,0],['Income reporting\nPrimary · 561 principals','Dice total\nBoundary · 317 principals']);ax.set_xlabel('Accuracy difference, percentage points (guardrail minus baseline)',labelpad=12);ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15)
fig.suptitle('A fixed anti-cheating rule improved intended-honest reporting',fontsize=14,fontweight='bold',y=.96)
fig.text(.5,.08,'Retained numeric medians; paired principal-weighted estimates.\n95% principal bootstrap CIs. Dice: total accuracy only. Not per-call reliability.',ha='center',fontsize=10,color='#4A5F70')
fig.savefig(B/'figures/accuracy_effect.png',dpi=180);plt.close(fig)

# A full 0–100% scale keeps the modest absolute change visually honest.
z=r[0]
fig,(a,b)=plt.subplots(1,2,figsize=(11,4.8),gridspec_kw={'width_ratios':[1.7,1]})
fig.subplots_adjust(left=.14,right=.97,bottom=.27,top=.80,wspace=.35)
rates=[100*z.baseline_rate,100*z.guardrail_rate]
for y,rate in zip([1,0],rates):
 a.barh(y,100,color='#DDE3E7',height=.42)
 a.barh(y,rate,color='#007F86',height=.42)
 a.text(rate-2,y,f'{rate:.1f}%',va='center',ha='right',color='white',fontsize=14,fontweight='bold')
a.set_yticks([1,0],['Baseline','Guardrail']);a.set_xlim(0,100);a.set_ylim(-.6,1.6)
a.set_xlabel('Correct retained numeric median (%)');a.spines[['top','right','left']].set_visible(False)
b.errorbar(100*z.estimate,0,xerr=[[100*(z.estimate-z.CI_low)],[100*(z.CI_high-z.estimate)]],fmt='o',color='#007F86',lw=3,capsize=6,markersize=9)
b.axvline(0,color='#596C7A',ls='--',lw=1);b.set_xlim(-.2,5);b.set_ylim(-.65,.65);b.set_yticks([])
b.set_xlabel('Paired gain (percentage points)');b.spines[['top','right','left']].set_visible(False)
b.text(100*z.estimate,.26,f'+{100*z.estimate:.2f} pp\n95% CI [{100*z.CI_low:.2f}, {100*z.CI_high:.2f}]',ha='center',fontsize=12)
fig.suptitle('Honest-intention income reporting: a modest accuracy benefit',fontsize=15,fontweight='bold')
fig.text(.5,.08,'561 people · 1,083 instructions · 4,249 observed paired model cells\nPerson-weighted estimates; 9,999 person-bootstrap resamples. Historical models, retained medians only.',ha='center',fontsize=10,color='#4A5F70')
fig.savefig(B/'figures/accuracy_rates.png',dpi=180);plt.close(fig)

"""Publication figures from the implemented architecture and frozen calibration bins.

No respondent-level data is read and no model is refitted.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 16})
fig, ax = plt.subplots(figsize=(7, 5.12))
ax.set(xlim=(0, 7), ylim=(0, 5.12))
ax.axis('off')
def box(x, y, w, h, text):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04',
                 facecolor='#f3f3f3',edgecolor='black',linewidth=1.2))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=15)
def arrow(x1,y1,x2,y2):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),
                arrowprops={'arrowstyle':'->','lw':1.3,'color':'black'})
box(.16,4.1,3.05,.78,'Offline research\nThree linked LCS tables')
box(3.8,4.1,3.03,.78,'Local Streamlit\nValidated historical CSV')
box(.6,2.78,5.8,.81,'Shared versioned observable screen\nSeparate reported-receipt outcome')
arrow(1.69,4.05,2.0,3.65)
arrow(5.31,4.05,5.0,3.65)
box(.16,1.35,3.05,.87,'Offline analysis\nDescription + grouped fits')
box(3.8,1.35,3.03,.87,'Frozen full-data fit\nUpload inference')
arrow(1.85,2.72,1.69,2.28)
arrow(5.1,2.72,5.31,2.28)
box(.16,.13,3.05,.77,'Person-weighted prevalence\nUnweighted OOF evaluation')
box(3.8,.13,3.03,.77,'Statuses, reasons, scores\nAudited report exports')
arrow(1.69,1.29,1.69,.96)
arrow(5.31,1.29,5.31,.96)
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
for ext in ('png','svg'): fig.savefig(OUT/f'architecture.{ext}',dpi=300)
plt.close(fig)
with (ROOT.parent/'output/runs/primary/calibration_bins.csv').open(newline='') as f:
    rows=list(csv.DictReader(f))
assert sum(int(r['people']) for r in rows)==1013
assert sum(int(r['events']) for r in rows)==67
fig, ax = plt.subplots(figsize=(7,5))
x=[float(r['mean_predicted']) for r in rows]
y=[float(r['mean_observed']) for r in rows]
ax.plot([0,.22],[0,.22],color='gray',ls='--',lw=1.4,label='Exact calibration')
ax.plot(x,y,'o-',color='black',lw=1.2,ms=7)
for r,dx,dy in zip(rows,[-1,28,34,20,-40],[24,-19,16,-20,18]):
    ax.annotate(f"{r['events']}/{r['people']}",
                (float(r['mean_predicted']),float(r['mean_observed'])),
                xytext=(dx,dy),textcoords='offset points',fontsize=15,
                arrowprops={'arrowstyle':'-','color':'gray','lw':.8})
ax.set(xlim=(0,.22),ylim=(0,.22),xlabel='Mean predicted probability',ylabel='Observed non-receipt')
ax.set_xticks([0,.05,.10,.15,.20])
ax.set_yticks([0,.05,.10,.15,.20])
ax.grid(alpha=.18)
fig.tight_layout(pad=.7)
for ext in ('png','svg'): fig.savefig(OUT/f'calibration.{ext}',dpi=300)
plt.close(fig)
print('Wrote four figures; calibration aggregates: 1,013 people / 67 events.')
# Matplotlib emits trailing blanks inside multiline SVG paths; retain the
# whitespace-separated coordinates while keeping generated text Git-clean.
for svg in OUT.glob('*.svg'):
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')

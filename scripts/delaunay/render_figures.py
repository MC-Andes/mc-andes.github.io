from pathlib import Path
import json,hashlib,csv,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Patch
root=Path(__file__).resolve().parents[2]
a=root/'docs/assets/delaunay'; case=a/'ejemplo'
nodes=np.loadtxt(case/'Input_nodos.txt',delimiter=',')[:,2:4]
rows=list(csv.reader((case/'input_elements.txt').open()))[1:]
polys=[nodes[np.array(row[3:],int)-1] for row in rows]
areas=np.array([abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1)))/2 for p in polys])
diam=np.sqrt(4*areas/np.pi)
plt.rcParams.update({'font.size':12,'axes.labelcolor':'#1a1a1a','text.color':'#1a1a1a','axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(5,7),layout='constrained'); ax.set_facecolor('#f0ede8')
for p in polys: ax.add_patch(Polygon(p,facecolor='#2d5a4e',edgecolor='#1a1a1a',linewidth=.6))
ax.set(xlim=(0,100),ylim=(0,200),xlabel='x (mm)',ylabel='y (mm)',aspect='equal')
ax.legend(handles=[Patch(facecolor='#2d5a4e',edgecolor='#1a1a1a',label='Agregado'),Patch(facecolor='#f0ede8',edgecolor='#1a1a1a',label='Matriz')],loc='upper center',bbox_to_anchor=(.5,1.12),ncol=2,frameon=False)
fig.savefig(a/'geometria-2d.svg'); plt.close(fig)
bins=[(50,63),(25,50),(12.5,25),(4.75,12.5)]; target=np.array([.05,.4,.35,.2])*100
actual=np.array([areas[(diam>=lo)&(diam<=hi)].sum()/areas.sum()*100 for lo,hi in bins])
fig,ax=plt.subplots(figsize=(7,4.3),layout='constrained'); x=np.arange(4)
ax.bar(x-.2,target,.4,label='Objetivo G1',color='#f0ede8',edgecolor='#1a1a1a',hatch='///')
ax.bar(x+.2,actual,.4,label='Geometría generada',color='#2d5a4e',edgecolor='#1a1a1a')
ax.set(xticks=x,xticklabels=['50–63','25–50','12,5–25','4,75–12,5'],xlabel='Diámetro equivalente (mm)',ylabel='Fracción del área de agregado (%)',ylim=(0,50)); ax.legend(frameon=False); fig.savefig(a/'granulometria.svg'); plt.close(fig)
files=['Input_nodos.txt','input_elements.txt','audit/sampled_inclusions.csv','audit/validation_report.json','audit/roundtrip_report.json','audit/resolved_config.json']
record={'project_commit':'04d3d362677397aeb290d77cb2a9d02959fd44c8','case':'CA1_A2_G1_R01','source':'public main example, not PI192-v3','seed':7259952857075019525,'particle_count':len(polys),'aggregate_area_mm2':float(areas.sum()),'aggregate_fraction':float(areas.sum()/20000),'target_fraction':.30,'gradation_target_percent':target.tolist(),'gradation_measured_percent':actual.tolist(),'hashes':{f:hashlib.sha256((case/f).read_bytes()).hexdigest() for f in files},'figure_source':'Original figures rendered from the exported polygons; no external artwork.'}
(a/'procedencia.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))

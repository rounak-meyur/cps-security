"""
========================================
Create 2D bar graphs
========================================

"""

import os, sys
import cPickle as pkl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import itertools


workPath = os.getcwd()

pathTemp = workPath + "\\Temp Files\\"
pathBin = workPath + "\\Binary Output\\"
pathLib = workPath + "\\Libraries\\"
pathFig = workPath + "\\Figures\\"
sys.path.append(pathLib)


Impact = pkl.load(open(pathBin+"Impact_pkl_file.p",'r'))
Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))


sub = 2
dataset = Impact[sub]

IED_list = Sub2IED[sub].keys()
IED_attacklist = []
for r in range(1,len(IED_list)+1):
    IED_attacklist.extend(list(itertools.combinations(IED_list, r)))

figfile = "Substation"+str(sub)+".png"
f = plt.figure(figsize=(15,9))
ax = f.add_subplot(1,1,1)
color_code = {1:'royalblue',2:'darkorchid',3:'seagreen',4:'orange',5:'lightcoral',
              6:'crimson'}
for i,alist in enumerate(IED_attacklist):
    key = ''.join([str(x) for x in alist])
    ax.bar(i+1,Impact[sub][key],align='center',color=color_code[len(alist)])

ax.set_ylabel('Impact of IED attack',fontsize=20)
ax.set_xlabel('IED set attacked',fontsize=20)
ax.set_title('Impact of attacking IEDs of substation'+str(sub),fontsize=20)
ax.tick_params(bottom=False,labelbottom=False,left=False,labelleft=False)
leglines = [Line2D([0], [0], color='royalblue', markerfacecolor='black', marker='o',markersize=0),
            Line2D([0], [0], color='darkorchid', markerfacecolor='crimson', marker='o',markersize=0),
            Line2D([0], [0], color='seagreen', markerfacecolor='dodgerblue', marker='o',markersize=0),
            Line2D([0], [0], color='orange', markerfacecolor='green', marker='o',markersize=0),
            Line2D([0], [0], color='lightcoral', markerfacecolor='red', marker='o',markersize=0),
            Line2D([0], [0], color='crimson', markerfacecolor='dodgerblue', marker='o',markersize=0)]
ax.legend(leglines,['1 IED','2 IEDs','3 IEDs','4 IEDs','5 IEDs','6 IEDs'],
                  loc='best',ncol=2,prop={'size': 20})
f.savefig(pathFig+figfile, bbox_inches='tight')
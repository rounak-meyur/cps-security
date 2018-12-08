"""
========================================
Create 2D bar graphs
========================================

"""

import os, sys
import cPickle as pkl
import matplotlib.pyplot as plt
import numpy as np
import itertools


workPath = os.getcwd()

pathTemp = workPath + "\\Temp Files\\"
pathBin = workPath + "\\Binary Output\\"
pathLib = workPath + "\\Libraries\\"
pathFig = workPath + "\\Figures\\"
sys.path.append(pathLib)


Impact = pkl.load(open(pathBin+"Impact_pkl_file.p",'rb'))
Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))


for sub in range(1,28):
    dataset = Impact[sub]
    
    IED_list = Sub2IED[sub].keys()
    IED_attacklist = []
    for r in range(1,len(IED_list)+1):
        IED_attacklist.extend(list(itertools.combinations(IED_list, r)))
    
    impactlist = [Impact[sub][''.join([str(x) for x in alist])] for alist in IED_attacklist]
    
    figfile = "Substation"+str(sub)+".png"
    f = plt.figure(figsize=(10,6))
    y_pos = np.arange(1,len(impactlist)+1)
    plt.bar(y_pos, impactlist, align='center', color='b')
    plt.ylabel('Impact of IED attack',fontsize=15)
    plt.title('Impact of attacking IEDs of substation'+str(sub),fontsize=15)
    f.savefig(pathFig+figfile, bbox_inches='tight')       
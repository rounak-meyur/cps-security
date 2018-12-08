# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:51:08 2018

Author: Rounak Meyur

Description: This program evaluates the impact of all possible individual attacks
on the substations.
"""

import os, sys
import cPickle as pkl
import itertools
import re
workPath = os.getcwd()

pathTemp = workPath + "\\Temp Files\\"
pathBin = workPath + "\\Binary Output\\"
pathLib = workPath + "\\Libraries\\"
sys.path.append(pathLib)

Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))
numbus = 39

SubIEDdict = {sub:{} for sub in range(1,28)}

for sub in range(1,28):
    IED_list = Sub2IED[sub].keys()
    IED_attacklist = []
    for r in range(1,len(IED_list)+1):
        IED_attacklist.extend(list(itertools.combinations(IED_list, r)))
    
    
    for alist in IED_attacklist:
        targets = ''.join([str(x) for x in alist])
        tempfilename = "ieee39-devn-sub"+str(sub)+"-attackIED"+targets+'.txt'
        
        tempfile = open(pathTemp+tempfilename,'r')
        lines = tempfile.readlines()
        freqdata = lines[8:8+numbus]
        freqmod = [re.split('\s{1,}',f.strip('\n')) for f in freqdata]
        freqdev = [abs(float(freqmod[f][7])) for f in range(numbus)]
        voltdata = lines[15+numbus:15+numbus+numbus]
        voltmod = [re.split('\s{1,}',v.strip('\n')) for v in voltdata]
        voltdev = [abs(float(voltmod[v][7])) for v in range(numbus)]
        SubIEDdict[sub][targets] = [freqdev,voltdev]
        

pkl.dump(SubIEDdict,open(pathBin+"freqvoltdev_pkl_file.p",'wb'))

#%%
Impact = {sub:{t:((0.1*sum(SubIEDdict[sub][t][0]))/(numbus*0.01))+ \
               ((0.1*sum(SubIEDdict[sub][t][1]))/(numbus*0.05)) \
    for t in SubIEDdict[sub]} for sub in range(1,28)}

pkl.dump(Impact,open(pathBin+"impact_pkl_file.p",'wb'))
print max([max(Impact[i].values()) for i in range(1,28)])

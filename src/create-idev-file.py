# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 15:36:15 2018

Author: Rounak Meyur

Description: Creates a .idv response file to evaluate the deviations from the
plot files.
"""


import os
import cPickle as pkl
import itertools

workPath = os.getcwd()
pathBin = workPath + "/Binary Output/"
pathPlot = workPath + "/Plot Files/"
pathTemp = workPath + "/Temp Files/"

Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))
idev_file = "get-deviations.idv"
idev_file2 = "new.idv"

f = open(idev_file,'r')
lines = f.readlines()
start = lines[0]
end = lines[-1]
lines[2] = "Plot Files/{}.out\n"
lines[8] = "Temp Files/{}.txt\n"
content = ''.join([lines[t] for t in range(1,(len(lines)-1))])
f.close()

crux = start
for sub in range(1,28):
    IED_list = Sub2IED[sub].keys()
    IED_attacklist = []
    for r in range(1,len(IED_list)+1):
        IED_attacklist.extend(list(itertools.combinations(IED_list, r)))
    
    
    for alist in IED_attacklist:
        targets = ''.join([str(x) for x in alist])
        plotfilename = "ieee39sub"+str(sub)+"-attackIED"+targets
        tempfilename = "ieee39-devn-sub"+str(sub)+"-attackIED"+targets
        crux += content.format(plotfilename,tempfilename)

crux += end


f = open(idev_file2,'w')
f.write(crux)
f.close()


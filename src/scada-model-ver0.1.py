# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 21:33:35 2018

Author: Rounak Meyur

Description: Creates the SCADA model for each substation and evaluates the mean
time to compromise a HMI at every substation.
"""

import sys,os
import matplotlib.pyplot as plt
import numpy as np
# import cPickle as pkl

workPath = os.getcwd()
pathBin = workPath + "\\Binary Output\\"
pathLib = workPath + "\\Libraries\\"
pathFig = workPath + "\\Figures\\"
sys.path.append(pathLib)

import pySCADAlib
# reload(pySCADAlib)

#CVSS = {'ssh':10,'ftp':10,'htp':10,'bof':10,'xss':10}
CVSS = {'ssh':0.8,'ftp':6.4,'htp':9.3,'bof':6.8,'xss':4.5,'exe':10.0,'dos':5.0}
type_vul = {'ssh':'Z','ftp':'K','htp':'K','bof':'K','xss':'K','exe':'K','dos':'K'}
# list of choices for substation SCADA models: first 12: Model A, next 8: Model B and last 7: Model C
#choice = [0]*12+[1]*8+[2]*7
choice = [0]*27
subID = range(1,28)
figfile = "ModelA.png"


k_list=[5,1,0.5,0.001]
MTTC_all = []

for k in k_list:
    MTTC = []
    for i in range(len(choice)):
        if choice[i] == 0: MTTC.append(pySCADAlib.ModelA(CVSS,type_vul,k))
        elif choice[i] == 1: MTTC.append(pySCADAlib.ModelB(CVSS,type_vul,k))
        elif choice[i] == 2: MTTC.append(pySCADAlib.ModelC(CVSS,type_vul,k))
        elif choice[i] == 3: MTTC.append(pySCADAlib.ModelCC(CVSS,type_vul,k))
        else:
            # print "Wrong Model Choice!!! Exiting program"
            sys.exit(0)
    MTTC_all.append(MTTC)


# pkl.dump(MTTC_all,open(pathBin+"model-CC-pkl-file.p",'wb'))

f = plt.figure(figsize=(15,8))
plt.xticks(np.linspace(1,27,num=27))
plt.xlabel('Substations',fontsize=12.0)
plt.ylabel('Mean time to compromise (days)',fontsize=12.0)
plt.title('Mean time to compromise application server in LAN model A',fontsize=12.0)
plt.plot(subID,MTTC_all[0],marker='o',color='r',linestyle='-',markersize=5.0,label='expert')
plt.plot(subID,MTTC_all[1],marker='P',color='y',linestyle='-',markersize=5.0,label='professional')
plt.plot(subID,MTTC_all[2],marker='*',color='g',linestyle='-',markersize=5.0,label='intermediate')
plt.plot(subID,MTTC_all[3],marker='v',color='b',linestyle='-',markersize=5.0,label='amateur')
plt.legend(ncol=1,loc='best',prop={'size': 13})
f.savefig(pathFig+figfile, bbox_inches='tight')
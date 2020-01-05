# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 11:40:04 2018

Author: Rounak Meyur
"""

import os, sys
import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np


workPath = os.getcwd()

pathTemp = workPath + "\\Temp Files\\"
pathBin = workPath + "\\Binary Output\\"
pathLib = workPath + "\\Libraries\\"
pathFig = workPath + "\\Figures\\"
sys.path.append(pathLib)

import pySCADAlib
# reload(pySCADAlib)

subID = range(1,28)

Impact = pkl.load(open(pathBin+"Impact_pkl_file.p",'rb'))
Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))
Max_Impact = [np.mean(Impact[sub].values()) for sub in range(1,28)]
pkl.dump(Max_Impact,open("physical_impact_pkl_file.p",'wb'))

# Randomly select LAN model
CVSS = {'ssh':0.8,'ftp':6.4,'htp':9.3,'bof':6.8,'xss':4.5,'exe':10.0,'dos':5.0}
type_vul = {'ssh':'Z','ftp':'K','htp':'K','bof':'K','xss':'K','exe':'K','dos':'K'}
k = 10
Attack1 = []
LAN_model = np.random.randint(low=0,high=3,size=27)
for i in range(27):
    if LAN_model[i] == 0: MTTC = pySCADAlib.ModelA(CVSS,type_vul,k)
    elif LAN_model[i] == 1: MTTC = pySCADAlib.ModelB(CVSS,type_vul,k)
    elif LAN_model[i] == 2: MTTC = pySCADAlib.ModelC(CVSS,type_vul,k)
    else:
        print ("Wrong Model Choice!!! Exiting program")
        sys.exit(0)
    Attack1.append(1.0/MTTC)

Attack2 = []
for i in range(27):
    MTTC = pySCADAlib.ModelCC(CVSS,type_vul,k)
    Attack2.append(1.0/MTTC)

Net_Imp1 = [Attack1[i]*Max_Impact[i] for i in range(27)]
Net_Imp2 = [Attack2[i]*Max_Impact[i] for i in range(27)]
    
figfile = "Net-Impact1.png"
f = plt.figure(figsize=(13,6))
plt.xticks(np.linspace(1,27,num=27))
plt.xlabel('Substations',fontsize=12.0)
plt.ylabel('Impact of the attack',fontsize=15.0)
plt.plot(subID,Max_Impact,marker='o',color='g',linestyle='-',markersize=5.0,label='physical impact')
plt.plot(subID,Attack1,marker='P',color='b',linestyle='-',markersize=5.0,label='attack efficiency')
plt.plot(subID,Net_Imp1,marker='*',color='r',linestyle='-',markersize=5.0,label='risk of attack')
plt.title('Risk assessment of a cyber-physical attack on the substation SCADA system',fontsize=15)
plt.legend()
f.savefig(pathFig+figfile, bbox_inches='tight')

figfile = "Net-Impact2.png"
f = plt.figure(figsize=(13,6))
plt.xticks(np.linspace(1,27,num=27))
plt.xlabel('Substations',fontsize=12.0)
plt.ylabel('Impact of the attack',fontsize=15.0)
plt.plot(subID,Max_Impact,marker='o',color='g',linestyle='-',markersize=5.0,label='physical impact')
plt.plot(subID,Attack2,marker='P',color='b',linestyle='-',markersize=5.0,label='attack efficiency')
plt.plot(subID,Net_Imp2,marker='*',color='r',linestyle='-',markersize=5.0,label='risk of attack')
plt.title('Risk assessment of a cyber-physical attack on the control center SCADA system',fontsize=15)
plt.legend()
f.savefig(pathFig+figfile, bbox_inches='tight')
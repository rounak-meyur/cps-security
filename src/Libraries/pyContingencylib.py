"""
Created on Wed Oct 17 14:47:03 2018

Author: Rounak Meyur
"""

import sys,os
import psspy
from psspy import _i,_f



def InitSim(basepath,plotpath,cnv,snp,channels,out):
    '''
    '''
    # Load cnv and snp files
    try:
        psspy.case(basepath+cnv)
        psspy.case_title_data("IEEE 39 bus system", "Vulnerability assessment")
    except:
        print 'Error while opening file: %s'%cnv
        sys.exit(0)
    try:
        psspy.rstr(basepath+snp)
    except:
        print 'Error while opening file: %s'%snp
        sys.exit(0)
    
    # run channels
    psspy.delete_all_plot_channels()
    if os.path.isfile(channels):
        shell = sys.stdout
        f = open('idev_response-dynamic.txt','w')
        sys.stdout = f
        psspy.runrspnsfile(channels)
        f.close()
        sys.stdout = shell
    else:
    	 print 'No channels!!'
    
    # Define output file
    psspy.dynamics_solution_params([99,_i,_i,_i,_i,_i,_i,_i],[ 1.0,_f, 0.001, 0.004,_f,_f,_f,_f],"")
    psspy.set_relang(1,38,r"""1""")
    try:
        psspy.strt(0,plotpath+out)
    except:
        print 'error while initializing file: ',out
        sys.exit(0)
    
    return


def ProgressFile(path,log,suffix):
    '''
    '''
    psspy.progress_output(2,path+log,[2,0])
    psspy.report_output(2,path+log,[2,0])
    psspy.progress(' \n')
    psspy.progress('***************************************\n')
    psspy.progress('*            rundynamic %s \n'%suffix)
    psspy.progress('*\n')
    psspy.progress('***************************************\n')
    return


def GetIED(buslist):
    '''
    '''
    dict_IED = {}
    psspy.bsys(sid=1,numbus=len(buslist),buses=buslist)
    sid = 1
    
    ierr, MachCount = psspy.amachcount(sid, 4)
    ierr, MachNum = psspy.amachint(sid, 4, 'NUMBER')
    ierr, MachID = psspy.amachchar(sid, 4, 'ID')
    
    ierr, LoadCount = psspy.aloadcount(sid, 4)
    ierr, LoadNum = psspy.aloadint(sid, 4, 'NUMBER')
    ierr, LoadID = psspy.aloadchar(sid, 4, 'ID')
    
    owner = 1
    ties = 2
    flag = 2
    entry = 1
    ierr, LineCount = psspy.abrncount(sid, owner, ties, flag, entry)
    ierr, LineNum = psspy.abrnint(sid, owner, ties, flag, entry,['FROMNUMBER','TONUMBER'])
    ierr, LineID = psspy.abrnchar(sid, owner, ties, flag, entry,'ID')
    
    owner = 1
    ties = 1
    flag = 6
    entry = 2
    ierr, TxCount = psspy.abrncount(sid, owner, ties, flag, entry)
    ierr, TxNum = psspy.abrnint(sid, owner, ties, flag, entry,['FROMNUMBER','TONUMBER'])
    ierr, TxID = psspy.abrnchar(sid, owner, ties, flag, entry,'ID')
    
    count = 0
    for i in range(MachCount):
        count += 1
        dict_IED[count] = ['Mach',MachNum[0][i],MachID[0][i]]
    for i in range(LoadCount):
        count += 1
        dict_IED[count] = ['Load',LoadNum[0][i],LoadID[0][i]]
    for i in range(LineCount):
        count += 1
        dict_IED[count] = ['Line',LineNum[0][i],LineNum[1][i],LineID[0][i]]
    for i in range(TxCount):
        count += 1
        dict_IED[count] = ['Tx',TxNum[0][i],TxNum[1][i],TxID[0][i]]
        
    return dict_IED


def CreateContingency(dict_IED,IEDlist):
    '''
    '''
    for IED in IEDlist:
        if dict_IED[IED][0] == 'Mach':
            psspy.dist_machine_trip(dict_IED[IED][1],dict_IED[IED][2])
        elif dict_IED[IED][0] == 'Load':
            psspy.load_data_3(dict_IED[IED][1],dict_IED[IED][2], [0,_i,_i,_i,_i], [_f,_f,_f,_f,_f,_f])
        elif dict_IED[IED][0] == 'Line':
            psspy.dist_branch_trip(dict_IED[IED][1],dict_IED[IED][2],dict_IED[IED][3])
        elif dict_IED[IED][0] == 'Tx':
            psspy.dist_branch_trip(dict_IED[IED][1],dict_IED[IED][2],dict_IED[IED][3])
    return






































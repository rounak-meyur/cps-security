"""
Created on Wed Oct 17 14:23:24 2018

Author: Rounak Meyur

Description: This program runs a PSSE program to simulate the different physical
events in the power grid. The different events are the all possible combinations
of outages at each substation.
"""

from __future__ import with_statement
from contextlib import contextmanager

import os, sys
import cPickle as pkl
import itertools
workPath = os.getcwd()

@contextmanager
def silence(file_object=None):
    """
    Discard stdout (i.e. write to null device) or
    optionally write to given file-like object.
    """
    if file_object is None:
        file_object = open(os.devnull, 'w')

    old_stdout = sys.stdout
    try:
        sys.stdout = file_object
        yield
    finally:
        sys.stdout = old_stdout
    return


# To check for dynamic network convergence
import StringIO
output = StringIO.StringIO()


# Get the different directory loaction into different variables
pathBase = workPath + "\\Base Case\\"
pathPlot = workPath + "\\Plot Files\\"
pathTemp = workPath + "\\Temp Files\\"
pathProg = workPath + "\\Progress Files\\"
pathLib = workPath + "\\Libraries\\"
pathSet = workPath + "\\Settings\\"
pathBin = workPath + "\\Binary Output\\"

# Get the PSSE location in the system
sys.path.append(pathLib)
pssedir = r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN"""
sys.path.append (pssedir)
os.environ["PATH"] = os.environ["PATH"] + ";" + pssedir


## Import psspy and redirect
import psse34
import psspy
reload(psspy)
import redirect
redirect.psse2py()
with silence():
    psspy.psseinit(10000)

#
import pyContingencylib
reload(pyContingencylib)


# VARs definition
channels= 'channels.idv'
cnv = "ieee39_cnv.sav"
snp = "ieee39.snp"


#%%
Sub2IED = pkl.load(open(pathBin+"sub2ied_pkl_file.p",'rb'))

for sub in range(1,7):
    print "\n\n###################\nSubstation",sub
    IED_list = Sub2IED[sub].keys()
    IED_attacklist = []
    for r in range(1,len(IED_list)+1):
        IED_attacklist.extend(list(itertools.combinations(IED_list, r)))
    
    for alist in IED_attacklist:
        targets = ''.join([str(x) for x in alist])
        print "Target:",targets
        suffix = "sub"+str(sub)+"-attackIED"+targets
        out = "ieee39"+suffix+".out"
        log = "ieee39"+suffix+".txt"
        pyContingencylib.ProgressFile(pathProg,log,suffix)
        pyContingencylib.InitSim(pathBase,pathPlot,cnv,snp,channels,out)
        
        # Run initial time
        psspy.run(0, 1.0,99,15,0)
        # create contingency
        pyContingencylib.CreateContingency(Sub2IED[sub],alist)
        

        with silence(output):
            psspy.run()

        run_output = output.getvalue()
        if "NETWORK NOT CONVERGED" in run_output:
            raise SystemExit
        # Run remaining time
        psspy.run(0, 10.0,99,15,0)

#%%
#Sub = {1 : [39], 2 : [2, 30], 3 : [25, 37], 4 : [29, 38], 5 : [22, 35], 
#       6 : [23, 36], 7 : [19, 20, 33, 34], 8 : [10, 32], 9 : [6, 31], 10 : [9],
#       11 : [8], 12 : [7], 13 : [11, 12, 13], 14 : [5], 15 : [4], 16 : [3], 
#       17 : [1], 18 : [18], 19 : [26], 20 : [28], 21 : [24], 22 : [27], 
#       23 : [17], 24 : [16], 25 : [21], 26 : [15], 27 : [14]}
#
#Sub2IED = {s:pyContingencylib.GetIED(Sub[s]) for s in Sub}
#pkl.dump(Sub2IED,open(pathBin+"sub2ied_pkl_file.p",'wb'))
#sys.exit(0)

#%%






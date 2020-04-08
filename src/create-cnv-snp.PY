"""
Created on Wed Oct 17 14:23:24 2018

Author: Rounak Meyur

Description: This program runs a .idv response file (FORTRAN program) to create
the dynamic snapshot file and the converted case file for dynamic simulation.
"""

import psse34
import psspy
from psspy import _i
# MakeCnvSnp_.py
# VARs definition
study     = 'ieee39_flat'
mysav     = 'ieee39_v33'
mydyr     = 'ieee39.dyr'
simtime   =  10.0
title1    = 'ieee39'
title2    = 'flatstart'
conl      = 'Conl.idv'
channels  = 'channels.idv'
mylog = '%s.log'%study
#
psspy.progress_output(2,mylog,[0,0])
psspy.report_output(2,mylog,[0,0])
psspy.progress(' \n')
psspy.progress('***************************************\n')
psspy.progress('*            MakeCnvSnp %s \n'%study)
psspy.progress('*\n')
psspy.progress('***************************************\n')

psspy.case(mysav)
#psspy.runrspnsfile(re_add)			#adds RE topology
psspy.runrspnsfile(conl)
psspy.fnsl((_i,0,_i,_i,_i,_i,_i,0))
psspy.cong(0)
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.tysl(0)
psspy.save('%s_cnv'%study)
psspy.dyre_new([1,1,1,1],
               mydyr,
               r"""conec.flx""",
               r"""conet.flx""",
               r"""compile.bat""")
psspy.snap([-1,-1,-1,-1,-1],'%s'%study)
psspy.progress_output(1)

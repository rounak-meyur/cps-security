IEEE39bus = New England System - Power System + Dynamic data

Set-up for PSSe v.33:
1- Create a sav case from the raw file "IEEE39bus_v33.raw".
2- run MAKECNVSNP_.PY from within PSSe:  
  It creates a converted *.cnv file using the "conl.idv" and
  a snap *.snp file, using the "ieee39.dyr" file
3- run RUNFLAT_.PY from within PSSe:
  It performs a no-disturbance test, creating an *.out file
  with channels (monitored vars) defined in "channels.py"
4- run GETDEVNS_.IDV from within PSSPLT, the plotting tool in PSSe
  It output to a file the max deviations for selected channels
Steps 2 and 3 are logged.

To simulate adding three renewable (wind) generation plants to the IEEE39 network,
run the corresponding script with the "RE" (Renewable Energy) suffix: 
MAKECNVSNP_RE.PY, to add topology for three RE plants using RE_rdch.idv and do step 2 using the "ieee39_RE.dyr" file
RUNFLAT_RE.PY, to do step 3
and GETDEVNS_RE.IDV, to do step 4
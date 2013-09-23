#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys 
sys.path.append('/usr/lib/root/')
import ROOT
import sys
from math import sqrt,sin,cos

# ------------------------------------------------------------------------------------------------------------------//
#User declared cuts
METCut = 0.0
PtLCut = 25.0
PtUCut = 5000.0
EtaCut = 2.4

npdfs = 45
root_dir = "./ntuples/"
suffix = "_lhc7_ct66_"

outfile = "Templates_Wenu.root"

lumi = 0.015 #In fb, NYI

# ------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
  "struct MyStruct{ \
  float E_V; \
  float E_d1; \
  float E_d2; \
  float Px_V; \
  float Px_d1; \
  float Px_d2; \
  float Py_V; \
  float Py_d1; \
  float Py_d2; \
  float Pz_V; \
  float Pz_d1; \
  float Pz_d2; \
  float wt; \
  };"
)
from ROOT import MyStruct

# ------------------------------------------------------------------------------------------------------------------//
# using namespace RooFit

# ------------------------------------------------------------------------------------------------------------------//

etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.4]]
asymHigh =[0.0,0.0,0.0,0.0,0.0,0.0]
asymMid = [0.0,0.0,0.0,0.0,0.0,0.0]
asymLow = [0.0,0.0,0.0,0.0,0.0,0.0]

#-------------------------------------------------------------------------------------------------------------------//


for pdf in range(npdfs) :
  Wplus_ntp  = root_dir + "wp" + suffix + str(pdf).zfill(2)+".root"
  Wminus_ntp = root_dir + "wm" + suffix + str(pdf).zfill(2)+".root"
  nP = [0,0,0,0,0,0]
  nM = [0,0,0,0,0,0]
  n = [nP,nM]
  for j, ntp_name in  enumerate([Wplus_ntp, Wminus_ntp]) :
    print "using ntuple: ", ntp_name
    InFile = ROOT.TFile.Open(ntp_name) 
    # Set Up the branch aliases
    
    myTree = InFile.Get('h10')
    
    nEntries = myTree.GetEntriesFast()
    
    bE_V = myTree.GetBranch('E_V')
    bE_d1 = myTree.GetBranch('E_d1')
    bE_d2 = myTree.GetBranch('E_d2')
    bPx_V = myTree.GetBranch('Px_V')
    bPx_d1 = myTree.GetBranch('Px_d1')
    bPx_d2 = myTree.GetBranch('Px_d2')
    bPy_V = myTree.GetBranch('Py_V')
    bPy_d1 = myTree.GetBranch('Py_d1')
    bPy_d2 = myTree.GetBranch('Py_d2')
    bPz_V = myTree.GetBranch('Pz_V')
    bPz_d1 = myTree.GetBranch('Pz_d1')
    bPz_d2 = myTree.GetBranch('Pz_d2')
    bWT = myTree.GetBranch('WT00')
    
    c = MyStruct()
    
    bE_V.SetAddress(ROOT.AddressOf(c,'E_V'))
    bE_d1.SetAddress(ROOT.AddressOf(c,'E_d1'))
    bE_d2.SetAddress(ROOT.AddressOf(c,'E_d2'))
    bPx_V.SetAddress(ROOT.AddressOf(c,'Px_V'))
    bPx_d1.SetAddress(ROOT.AddressOf(c,'Px_d1'))
    bPx_d2.SetAddress(ROOT.AddressOf(c,'Px_d2'))
    bPy_V.SetAddress(ROOT.AddressOf(c,'Py_V'))
    bPy_d1.SetAddress(ROOT.AddressOf(c,'Py_d1'))
    bPy_d2.SetAddress(ROOT.AddressOf(c,'Py_d2'))
    bPz_V.SetAddress(ROOT.AddressOf(c,'Pz_V'))
    bPz_d1.SetAddress(ROOT.AddressOf(c,'Pz_d1'))
    bPz_d2.SetAddress(ROOT.AddressOf(c,'Pz_d2'))
    bWT.SetAddress(ROOT.AddressOf(c,'wt')) 
    
    nVec = ROOT.TLorentzVector()
    eVec = ROOT.TLorentzVector()
    wVec   = ROOT.TVector2() 
    metVec = ROOT.TVector2() 
    
    for i in range(0,nEntries):
      #if i==10 : break
      if (i%25000 == 0) : print "At event: " + str(i)
      myTree.GetEntry(i)
      eVec.SetPxPyPzE(c.Px_d1, c.Py_d1, c.Pz_d1, c.E_d1)
      nVec.SetPxPyPzE(c.Px_d2, c.Py_d2, c.Pz_d2, c.E_d2)#note mcfm flips these around
      if (eVec.Pt() > PtLCut) and (nVec.Pt() > METCut) :  
	for bin, etaRange in enumerate(etabins) :
	  if abs(eVec.PseudoRapidity()) > etaRange[0] and abs(eVec.PseudoRapidity()) < etaRange[1] :
	    (n[j])[bin]+=c.wt
  print nP,nM      
  for l in range(len(etabins)) :
    asym = (nP[l]-nM[l])/(nP[l]+nM[l])
    if pdf==0 : 
      asymHigh[l]=asym
      asymMid[l]=asym
      asymLow[l]=asym
    if asym>asymHigh[l] :
      asymHigh[l]=asym
    if asym<asymLow[l] :
      asymLow[l]=asym

print asymHigh
print asymMid
print asymLow

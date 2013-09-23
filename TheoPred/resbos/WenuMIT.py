#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys 
#sys.path.append('/usr/lib/root/')
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
W_ntp = ".root"####CHANGE
outfile = "Templates_Wenu.root"

# ------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
  "struct MyStruct{ \
  float aco; \
  float charge; \
  float eta; \
  float met; \
  float mt; \
  float pt; \
  };"
)
from ROOT import MyStruct

# ------------------------------------------------------------------------------------------------------------------//
# using namespace RooFit
ROOT.gROOT.SetBatch(True) # suppress the creation of canvases on the screen.. much much faster if over a remote connection
  
# ------------------------------------------------------------------------------------------------------------------//

# ------------------------------------------------------------------------------------------------------------------//

# ------------------------------------------------------------------------------------------------------------------//
#Output File
OutFile = ROOT.TFile(outfile,"RECREATE")

# ------------------------------------------------------------------------------------------------------------------//

etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.4],[0.0,1.4442],[1.566,2.5]]
suffix_=["","_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos","_EB_pos","_EE_pos",
	    "_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg","_EB_neg","_EE_neg"]
    
nmetbins_ = 100    
	    
pfMET_sel_ = [ROOT.TH1F("h_pfMET"+bin,"h_pfMET"+bin,nmetbins_,0.,100.) for bin in suffix_]
MT_sel_ = [ROOT.TH1F("h_MT"+bin,"h_MT"+bin,nmetbins_,0.,100.) for bin in suffix_]

#-------------------------------------------------------------------------------------------------------------------//
InFile = ROOT.TFile.Open(ntp_name) 
# Set Up the branch aliases
   
myTree = InFile.Get('h10')
   
nEntries = myTree.GetEntriesFast()

b_aco = myTree.GetBranch('aco')
b_charge = myTree.GetBranch('charge')
b_eta = myTree.GetBranch('eta')
b_met = myTree.GetBranch('met')
b_mt = myTree.GetBranch('mt')
b_pt = myTree.GetBranch('pt')
c = MyStruct()
b_aco.SetAddress(ROOT.AddressOf(c,'aco'))
b_charge.SetAddress(ROOT.AddressOf(c,'charge'))
b_eta.SetAddress(ROOT.AddressOf(c,'eta'))
b_met.SetAddress(ROOT.AddressOf(c,'met'))
b_mt.SetAddress(ROOT.AddressOf(c,'mt'))
b_pt.SetAddress(ROOT.AddressOf(c,'pt'))
    
for i in range(0,nEntries):
  #if i==10 : break
  if (i%25000 == 0) : print "At event: " + str(i)
  
  myTree.GetEntry(i)
  toFill = [0]
  for bin, etaRange in enumerate(etabins) :
    if abs(c.eta) > etaRange[0] and abs(c.eta) < etaRange[1] :
      j = bin+1
      if c.charge < 0: j = j+len(etabins)
      toFill.append(j)
    
  if (c.pt > PtLCut) :  #Thats it, we've passed the selection
    count = count+1
    for j in toFill :
      pfMET_sel_[j].Fill(c.met)
      MT_sel_[j].Fill(c.mt)

OutFile.cd()
direct = OutFile.mkdir('Templates_' + str(pdf).zfill(2))
direct.cd()
for h in pfMET_sel_ :
  h.Write()
for h in MT_sel_ :
  h.Write()


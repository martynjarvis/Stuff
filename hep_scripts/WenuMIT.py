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

PtUCut = 50000.0
EtaCut = 2.5

W_ntp = "/vols/cms02/mjarvis/ntuples/2DDigausWpfntuple_zrecoil_v70.root"
outfile = "Templates_Wenu_dec22_20MET.root"
# ------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
  "struct MyStruct{ \
  float aco; \
  int charge; \
  float eta; \
  float met; \
  float mt; \
  float pt; \
  float weight;\
  };"
)
from ROOT import MyStruct

# ------------------------------------------------------------------------------------------------------------------//
ROOT.gROOT.SetBatch(True) # suppress the creation of canvases on the screen.. much much faster if over a remote connection


# ------------------------------------------------------------------------------------------------------------------//
#Output File
OutFile = ROOT.TFile(outfile,"RECREATE")

# ------------------------------------------------------------------------------------------------------------------//

etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.4],[0.0,2.4]]
suffix_=["_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos","_inc_pos",
         "_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg","_inc_neg"]
wptbins = [[0.,4.],[4.,8.],[8.,12.],[12.,16.],[16.,24.],[24.,50.],[50.,75.],[75.,100.],[100.,999.9]]
wptsuffix_=["_wpt1_pos","_wpt2_pos","_wpt3_pos","_wpt4_pos","_wpt5_pos","_wpt6_pos","_wpt7_pos","_wpt8_pos","_wpt9_pos",
            "_wpt1_neg","_wpt2_neg","_wpt3_neg","_wpt4_neg","_wpt5_neg","_wpt6_neg","_wpt7_neg","_wpt8_neg","_wpt9_neg"]

nmetbins_ = 100    
	    
pfMET_sel_ = [ROOT.TH1F("h_pfMET"+bin,"h_pfMET"+bin,nmetbins_,0.,100.) for bin in suffix_]
MT_sel_ = [ROOT.TH1F("h_MT"+bin,"h_MT"+bin,nmetbins_,0.,150.) for bin in suffix_]
h_wpt_sel_ = [ROOT.TH1F("h_wpt_pfMET"+bin,   "h_wpt_pfMET"+bin,nmetbins_,0.,100.) for bin in wptsuffix_]
h_mt_wpt_sel_ = [ROOT.TH1F("h_wpt_MT"+bin,   "h_wpt_MT"+bin,nmetbins_,0.,150.) for bin in wptsuffix_]
 
#-------------------------------------------------------------------------------------------------------------------//
print "Opening file : " + W_ntp
InFile = ROOT.TFile.Open(W_ntp) 
# Set Up the branch aliases

for PtLCut in [25,30,35] :
  print "lepton PT cut: ", PtLCut
  dirNames = ["lowTree","midTree","highTree"]
  for dirName in dirNames :
    print "Opening tree : " + dirName
    myTree = InFile.Get(dirName)
      
    nEntries = myTree.GetEntriesFast()

    b_aco = myTree.GetBranch('aco')
    b_charge = myTree.GetBranch('charge')
    b_eta = myTree.GetBranch('eta')
    b_met = myTree.GetBranch('met')
    b_mt = myTree.GetBranch('mt')
    b_pt = myTree.GetBranch('pt')
    b_weight = myTree.GetBranch('weight')
    
    c = MyStruct()
    
    b_aco.SetAddress(ROOT.AddressOf(c,'aco'))
    b_charge.SetAddress(ROOT.AddressOf(c,'charge'))
    b_eta.SetAddress(ROOT.AddressOf(c,'eta'))
    b_met.SetAddress(ROOT.AddressOf(c,'met'))
    b_mt.SetAddress(ROOT.AddressOf(c,'mt'))
    b_pt.SetAddress(ROOT.AddressOf(c,'pt'))
    b_weight.SetAddress(ROOT.AddressOf(c,'weight'))
	
    for i in range(0,nEntries):
      #if i==10 : break
      if (i%25000 == 0) : print "At event: " + str(i) + "/"+str(nEntries)
      
      myTree.GetEntry(i)


      toFill = []
      for bin, etaRange in enumerate(etabins) :
	if abs(c.eta) > etaRange[0] and abs(c.eta) < etaRange[1] :
	  j = bin
	  #print c.charge
	  if c.charge < 0: 
	    j = j+len(etabins)
	    #print "negative!"
	  toFill.append(j)

	  
      toFillwpt = []# no inclusive bin
      #nvec.SetMagPhi(c.pfMEt,c.pfMEt_phi)
      #evec.SetMagPhi(c.pt,c.phi)
      #wvec.Set(evec.X()+nvec.X(),evec.Y()+nvec.Y())
      wpt = c.met*c.met+c.pt*c.pt+2*c.pt*c.met-c.mt*c.mt
      if wpt < 0 : print wpt
      wpt = sqrt(abs(wpt))
      for bin, wptRange in enumerate(wptbins) :
	if wpt > wptRange[0] and wpt < wptRange[1] and c.met > METCut and abs(c.eta)<EtaCut :
	  j = bin
	  if c.charge < 0: j = j+len(wptbins)
	  toFillwpt.append(j)
	
      if (c.pt > PtLCut) and (abs(c.eta)<1.4 or abs(c.eta)>1.6) : 
      # #Thats it, we've passed the selection count = count+1
	for j in toFill :
	  pfMET_sel_[j].Fill(c.met,c.weight)
	  MT_sel_[j].Fill(c.mt,c.weight)
	for j in toFillwpt :
	  h_wpt_sel_[j].Fill(c.met,c.weight)
	  h_mt_wpt_sel_[j].Fill(c.mt,c.weight)


    OutFile.cd()
    direct = OutFile.mkdir(dirName+str(PtLCut))
    direct.cd()
    ##endloop over dirs
    for h in pfMET_sel_ :
      h.Write()
      h.Reset()
    for h in MT_sel_ :
      h.Write()
      h.Reset()

    for h in h_wpt_sel_ :
      h.Write()
      h.Reset()
    for h in h_mt_wpt_sel_ :
      h.Write()
      h.Reset()


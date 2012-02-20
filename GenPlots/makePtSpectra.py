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
PtCut = 0.0
EtaCut = 2.4
EtaGap = [1.4,1.6]
EtaBins = [[0.0,0.2],[0.2,0.4],[0.4,0.6],[0.6,0.8],[0.8,1.0],[1.0,1.2],[1.2,1.4],[1.4,1.6],[1.6,1.8],[1.8,2.0],[2.0,2.2],[2.2,2.4]]


npdfs = 45
root_dir = "./ntuples/"
suffix = "_lhc7_ct66_"
prefix = "wm"

outfile = "pt_"+prefix+suffix+"all.root"
OutFile = ROOT.TFile.Open(outfile,"RECREATE") 

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

for pdf in range(npdfs) :
  ntp_name  = root_dir + prefix + suffix + str(pdf).zfill(2)+".root"
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
  wVec = ROOT.TLorentzVector()

  pdf_name  = str(pdf).zfill(2)
  OutFile.cd()


  e_pt = []
  n_pt = []
  w_pt = []
  for i,bin in enumerate(EtaBins):
    eta_name = str(i)+"_"
    e_pt.append(ROOT.TH1F("e_pt_"+eta_name+pdf_name,"e_pt_"+eta_name+pdf_name,5000,0.,100))
    n_pt.append(ROOT.TH1F("n_pt_"+eta_name+pdf_name,"n_pt_"+eta_name+pdf_name,5000,0.,100))  
    w_pt.append(ROOT.TH1F("w_pt_"+eta_name+pdf_name,"w_pt_"+eta_name+pdf_name,5000,0.,100))


  for i in range(0,nEntries):
    #if i==10 : break
    if (i%25000 == 0) : print "At event: " + str(i)
    #if (i%1 == 0) : print "At event: " + str(i)
    myTree.GetEntry(i)
    eVec.SetPxPyPzE(c.Px_d1, c.Py_d1, c.Pz_d1, c.E_d1)
    nVec.SetPxPyPzE(c.Px_d2, c.Py_d2, c.Pz_d2, c.E_d2)
    wVec.SetPxPyPzE(c.Px_V, c.Py_V, c.Pz_V, c.E_V)
    if (eVec.Pt() > PtCut) and (nVec.Pt() > METCut) :  
      for i,bin in enumerate(EtaBins):
        if abs(eVec.PseudoRapidity()) > bin[0] and abs(eVec.PseudoRapidity()) < bin[1] :
          e_pt[i].Fill(eVec.Pt(),c.wt)
          n_pt[i].Fill(nVec.Pt(),c.wt)
          w_pt[i].Fill(wVec.Pt(),c.wt)
  #clean up
  InFile.Close()

  OutFile.cd()
  for i,bin in enumerate(EtaBins):
    e_pt[i].Write()
    n_pt[i].Write()
    w_pt[i].Write()



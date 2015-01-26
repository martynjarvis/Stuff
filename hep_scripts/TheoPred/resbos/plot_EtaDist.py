#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
import sys
from math import sqrt

# ------------------------------------------------------------------------------------------------------------------//
#User declared cuts
METCut = 0.0
PtLCut = 25.0
PtUCut = 5000.0
EtaCut = 4

EtaBins = 20

Wplus_ntp = "./wplus.root"
Wminus_ntp = "./wminus.root"

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
ROOT.gROOT.SetBatch(True) # suppress the creation of canvases on the screen.. much much faster if over a remote connection
ROOT.gROOT.SetStyle("Plain") #To set plain bkgds for slides
ROOT.gStyle.SetTitleBorderSize(0)
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetCanvasColor(0)#Sets canvas colour white
ROOT.gStyle.SetOptStat(1110)#set no title on Stat box
ROOT.gStyle.SetLabelOffset(0.001)
ROOT.gStyle.SetLabelSize(0.05)
ROOT.gStyle.SetLabelSize(0.05,"Y")#Y axis
ROOT.gStyle.SetTitleSize(0.04)
ROOT.gStyle.SetTitleW(0.7)
ROOT.gStyle.SetTitleH(0.07)
ROOT.gStyle.SetOptTitle(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetAxisColor(1, "XYZ");
ROOT.gStyle.SetStripDecimals(ROOT.kTRUE);
ROOT.gStyle.SetTickLength(0.03, "XYZ");
ROOT.gStyle.SetNdivisions(510, "XYZ");
ROOT.gStyle.SetPadTickX(1);
ROOT.gStyle.SetPadTickY(1);
ROOT.gStyle.SetLabelColor(1, "XYZ");
ROOT.gStyle.SetLabelFont(42, "XYZ");
ROOT.gStyle.SetLabelOffset(0.007, "XYZ");
ROOT.gStyle.SetLabelSize(0.04, "XYZ");
ROOT.gStyle.SetHatchesLineWidth(3)

c1 = ROOT.TCanvas("nEvents","nEvents",600,600)
c2 = ROOT.TCanvas("asym","asym",600,600)

leg = ROOT.TLegend(0.5, 0.15, 0.7, 0.3)
leg.SetShadowColor(0)
leg.SetBorderSize(0)
leg.SetFillStyle(4100)
leg.SetFillColor(0)
leg.SetLineColor(0)

# ------------------------------------------------------------------------------------------------------------------//
#Output File
#OutName = 'Results'#+WP+list(Name.split('/'))[-1]
#OutFile = ROOT.TFile(OutName,'RECREATE')

# ------------------------------------------------------------------------------------------------------------------//
#Histograms
e_plus  = ROOT.TH1F("e_plus" ,"" ,EtaBins,-EtaCut,EtaCut)
e_minus = ROOT.TH1F("e_minus","",EtaBins,-EtaCut,EtaCut)
w_plus  = ROOT.TH1F("w_plus" ,"" ,EtaBins,-EtaCut,EtaCut)
w_minus = ROOT.TH1F("w_minus","",EtaBins,-EtaCut,EtaCut)
e_asym = ROOT.TH1F("e_asym","e_asym",EtaBins,-EtaCut,EtaCut)
w_asym = ROOT.TH1F("w_asym","w_asym",EtaBins,-EtaCut,EtaCut)

e_plus.SetTitle("W #rightarrow e#nu CTEQ6.6")
e_minus.SetTitle("W #rightarrow e#nu CTEQ6.6")
w_plus.SetTitle("W #rightarrow e#nu CTEQ6.6")
w_minus.SetTitle("W #rightarrow e#nu CTEQ6.6")

e_asym.SetTitle("Electron Asymmetry CTEQ6.6")
w_asym.SetTitle("W Asymmetry CTEQ6.6")

e_asym.GetYaxis().SetRangeUser(0.0,0.4)

# ------------------------------------------------------------------------------------------------------------------//
for ntp_name, e_hist, w_hist in zip([Wplus_ntp,Wminus_ntp],[e_plus,e_minus],[w_plus,w_minus]) :
  print "Using Ntuple" , ntp_name
  InFile = ROOT.TFile.Open(ntp_name) 

  # Set Up the branch aliases
  tree = InFile.Get('h10')

  #def setBranches() :
  nEntries = tree.GetEntriesFast()
  bE_V = tree.GetBranch('E_V')
  bE_d1 = tree.GetBranch('E_d1')
  bE_d2 = tree.GetBranch('E_d2')
  bPx_V = tree.GetBranch('Px_V')
  bPx_d1 = tree.GetBranch('Px_d1')
  bPx_d2 = tree.GetBranch('Px_d2')
  bPy_V = tree.GetBranch('Py_V')
  bPy_d1 = tree.GetBranch('Py_d1')
  bPy_d2 = tree.GetBranch('Py_d2')
  bPz_V = tree.GetBranch('Pz_V')
  bPz_d1 = tree.GetBranch('Pz_d1')
  bPz_d2 = tree.GetBranch('Pz_d2')
  bWT = tree.GetBranch('WT00')
  
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
  
  eVec = ROOT.TLorentzVector(c.Px_d1, c.Py_d1, c.Pz_d1, c.E_d1)
  wVec = ROOT.TLorentzVector(c.Px_V, c.Py_V, c.Pz_V, c.E_V)
  
  #nEntries = setBranches()
  e_hist.Reset()
  w_hist.Reset()
  for i in range(0,nEntries):
    tree.GetEntry(i)
    MET = sqrt(c.Py_d2**2 + c.Px_d2**2)
    PT  = sqrt(c.Py_d1**2 + c.Px_d1**2)
    if (PT > PtLCut) and (MET > METCut) :
      eVec.SetPxPyPzE(c.Px_d1, c.Py_d1, c.Pz_d1, c.E_d1)
      wVec.SetPxPyPzE(c.Px_V,  c.Py_V,  c.Pz_V,  c.E_V)
      e_hist.Fill(eVec.PseudoRapidity(),c.wt)
      w_hist.Fill(wVec.Rapidity(),c.wt)

    if (i%25000 == 0) : print "At event: " + str(i)
    
  eVec.Delete()
  wVec.Delete()
  
  e_hist.SetLineWidth(2)
  w_hist.SetLineWidth(2)
  c1.cd()
  if (ntp_name == Wplus_ntp) : 
    e_hist.SetMarkerColor(1)
    e_hist.SetMarkerStyle(20)
    w_hist.SetLineColor(1)
    w_hist.SetLineStyle(1)
    leg.AddEntry(e_hist,"electron (+) ","p")##
    leg.AddEntry(w_hist,"W (+) ","l")##
    e_hist.Draw("p")
    w_hist.Draw("same c")
  else :
    e_hist.SetMarkerColor(2)
    e_hist.SetMarkerStyle(20)
    w_hist.SetLineColor(2)
    w_hist.SetLineStyle(1)
    leg.AddEntry(e_hist,"electron (-) ","p")##
    leg.AddEntry(w_hist,"W (-) ","l")##
    e_hist.Draw("same p")
    w_hist.Draw("same c")
leg.Draw()
c1.SaveAs("etaDist.png")
  

#OutFile.cd()

#EBh_CaloMEt_x_TrckIso_.Write()

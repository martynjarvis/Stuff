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

#c1 = ROOT.TCanvas("canvas","canvas",1200,1200)
#c2 = ROOT.TCanvas("MET_shape_canv","MET_shape",1200,1200)

leg = ROOT.TLegend(0.7, 0.15, 0.9, 0.3)
leg.SetShadowColor(0)
leg.SetBorderSize(0)
leg.SetFillStyle(4100)
leg.SetFillColor(0)
leg.SetLineColor(0)
  
Rand = ROOT.TRandom3()

# ------------------------------------------------------------------------------------------------------------------//
bias_pll = [-2.671,2.997,-0.05845]
sigma_pll = [5.692,0.07289]

bias_tr = [0.01774,-0.2298,-0.02036]
sigma_tr = [5.98,0.04064]

# ------------------------------------------------------------------------------------------------------------------//
def METRecoilCor(METTr, METPll, PT) :
  #print "corr"
  #print PT
  #print METPll, bias_pll[0] + bias_pll[1]/sqrt(PT) + bias_pll[2]*PT
  #print sigma_pll[0] + sigma_pll[1]*PT
  #print METTr, bias_tr[0]  + bias_tr[1]/sqrt(PT)  + bias_tr[2]*PT
  #print sigma_tr[0]  + sigma_tr[1]*PT 
  #print "end corr"
  METPll = METPll + Rand.Gaus(bias_pll[0] + bias_pll[1]/sqrt(PT+1) + bias_pll[2]*PT, sigma_pll[0] + sigma_pll[1]*PT*0.8) 
  METTr  = METTr  + Rand.Gaus(0,  sigma_tr[0]  + sigma_tr[1]*PT*0.8) 
  return METTr,METPll

# ------------------------------------------------------------------------------------------------------------------//
#Output File
OutFile = ROOT.TFile(outfile,"RECREATE")

# ------------------------------------------------------------------------------------------------------------------//

etaBins = [0.0,0.4,0.8,1.2,1.6,2.0,2.4]
binLabels =  ["_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos","_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg"]
h_uncorr = [ ROOT.TH1F("h_sel"+suff,"h_sel"+suff,200,0,100) for suff in binLabels]
h_corr = [ ROOT.TH1F("h_MC_sel"+suff,"h_MC_sel"+suff,200,0,100) for suff in binLabels]

hist_PTvsYvsEta = ROOT.TH3F("PTvsYvsEta","PTvsYvsEta;Log_{10}(Pt);|Y|;Electron |#eta|", 100,-1.,3.,100,0.,6.,100,0.,6.)



#-------------------------------------------------------------------------------------------------------------------//


for pdf in range(npdfs) :
  Wplus_ntp  = root_dir + "wp" + suffix + str(pdf).zfill(2)+".root"
  Wminus_ntp = root_dir + "wm" + suffix + str(pdf).zfill(2)+".root"
  for j, ntp_name in  enumerate([Wplus_ntp, Wminus_ntp]) :
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
      if (eVec.Pt() > PtLCut) :  
	nVec.SetPxPyPzE(c.Px_d2, c.Py_d2, c.Pz_d2, c.E_d2)
	metVec.Set(nVec.Px(),nVec.Py())
	#print "~~~~~~~~~~~~~~~~~~~~~~~"
	#print "ME Px and Py before :",nVec.Px(),nVec.Py()
	#print "MET :", nVec.Pt()
	wVec.Set(c.Px_V, c.Py_V)
	angle  = metVec.DeltaPhi(wVec)
	#print "angle :",angle
	METTr  = metVec.Mod()*sin(angle)
	METPll = metVec.Mod()*cos(angle)
	#print "MET Trans, Parra",METTr,METPll
	#print "MET added",sqrt(METTr**2 + METPll**2)
	METTr,METPll = METRecoilCor(METTr, METPll, wVec.Mod())
	#print "MET Trans, Parra",METTr,METPll
	#print "MET added",sqrt(METTr**2 + METPll**2)
	metVec.Set(METPll,METTr)
	#print "ME Px and Py middle :",metVec.Px(),metVec.Py()
	#print "MET :", metVec.Mod()
	metVec = metVec.Rotate(wVec.Phi())
	#print "ME Px and Py after :",metVec.Px(),metVec.Py()
	#print "MET :", metVec.Mod()
	for i in range(len(etaBins)-1) :
	  if (abs(eVec.PseudoRapidity()) > etaBins[i]) and (abs(eVec.PseudoRapidity()) < etaBins[i+1]) :
	    h_uncorr[i+6*j].Fill(nVec.Pt(), c.wt)
	    h_corr[i+6*j].Fill(metVec.Mod(), c.wt)

  OutFile.cd()
  direct = OutFile.mkdir('Templates_' + str(pdf).zfill(2))
  direct.cd()
  #outFile.cd()

  for h1,h2 in zip(h_uncorr,h_corr) :
    h1.Write()
    h2.Write()
    h1.Reset()
    h2.Reset()
    #h1.SetLineColor(1)
    #h1.SetLineWidth(3)
    #h1.DrawCopy("")
    #h2.SetLineColor(2)
    #h2.SetLineWidth(3)
    #h2.DrawCopy("same")
    #c2.SaveAs("./WShape/"+h1.GetName()+".png")
  

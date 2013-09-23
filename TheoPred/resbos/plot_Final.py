#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys 
sys.path.append('/usr/lib/root/')
import ROOT
import sys
import math
from array import *

# ------------------------------------------------------------------------------------------------------------------//
#User declared cuts
METCut = [20,0,0,0]
PTCut = [25,25,30,35]
Corrected = True

# ------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
  "struct MyStruct{ \
  float pT_d1; \
  float pT_d2; \
  float y_d1; \
  float y_d2; \
  float pT_B; \
  float y_B; \
  float M_B; \
  float D_phi; \
  float cos_the_; \
  float phi_sta; \
  float DelR34; \
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

c1 = ROOT.TCanvas("canvas","canvas",600,600)
c2 = ROOT.TCanvas("asym","asym",600,600)

leg = ROOT.TLegend(0.6, 0.15, 0.9, 0.3)
leg.SetShadowColor(0)
leg.SetBorderSize(0)
leg.SetFillStyle(4100)
leg.SetFillColor(0)
leg.SetLineColor(0)

asym_MSTW = []
asym_MSTW_up = []
asym_MSTW_lo = []
asym_CTEQ = []
asym_CTEQ_up = []
asym_CTEQ_lo = []
data = []
stat = []
syst_up = []
syst_lo = []


#MSTW
#Lepton PT Cut 25.0
#MET Cut 20.0
asym_MSTW.append([0.132328837964,0.141873526698,0.168430463925,0.192339118476,0.232108035668,0.244957692913])
asym_MSTW_up.append([0.00402091593751,0.00420972972232,0.00465408262471,0.00589543600639,0.00759761324639,0.00844772347976])
asym_MSTW_lo.append([0.00984329836366,0.0085963606726,0.00607756317243,0.00538986078302,0.00314185032775,0.00321074510819])

#Lepton PT Cut 25.0
#MET Cut 0.0
asym_MSTW.append([0.132326857091,0.141872407798,0.168427423307,0.19233411794,0.232103845212,0.24495447786])
asym_MSTW_up.append([0.00402092792914,0.0042097314257,0.00465411250667, 0.00589551061044, 0.00759768116517,0.00844783416857])
asym_MSTW_lo.append([0.00984338105801,0.00859640027186,0.00607766066084,0.00538998981121,0.00314197473204,0.00321080722814])

#Lepton PT Cut 30.0
#MET Cut 0.0
asym_MSTW.append([0.107281012037,0.116757017602,0.142122352904,0.165597400557,0.214064565025,0.239430485529])
asym_MSTW_up.append([0.00342761811982,0.00370283954361,0.00480966600888,0.00599508809746,0.00752956135374,0.00824259077206])
asym_MSTW_lo.append([0.0100815796705,0.00873956224331,0.00609828729723,0.005816964262,0.00426272699021,0.00362089483866])

#Lepton PT Cut 35.0
#MET Cut 0.0
asym_MSTW.append([0.081386035989,0.089479790229,0.112722551566,0.135738580297,0.189408971503,0.228159962637])
asym_MSTW_up.append([0.00284459133462,0.00365970369749,0.00500854523931,0.00607084543796,0.00731887065365,0.00792065643992])
asym_MSTW_lo.append([0.0102642945406,0.00872576799545,0.00598092641204,0.00619245733533,0.00554583574144,0.00438718714788])

#CTEQ
#Lepton PT Cut 25.0
#MET Cut 20.0
asym_CTEQ.append([0.152765808427,0.1637474933,0.190886411251,0.214957666695,0.252370810218,0.260030033932])
asym_CTEQ_up.append([0.00385627188187,0.00351397108399,0.00271767498711,0.0017798414785,0.00077934211216,0.00050634836716])
asym_CTEQ_lo.append([0.00701191058323,0.00744168987133,0.00805777933626,0.0084606354572,0.00856543516394,0.00814622506338])

#Lepton PT Cut 25.0
#MET Cut 0.0
asym_CTEQ.append([0.152765102494,0.163745456917,0.190882246841,0.214952023845,0.252366654641,0.260029082676])
asym_CTEQ_up.append([0.00385631743792,0.00351405531876,0.00271781621208,0.00178000789644,0.000779421055548,0.00050639456378])
asym_CTEQ_lo.append([0.00701188956607,0.00744165180297,0.00805772018162,0.0084605561934,0.00856532064801,0.00814616101858])

#Lepton PT Cut 30.0
#MET Cut 0.0
asym_CTEQ.append([0.128451222778,0.138440623479,0.164971032432,0.187432539016,0.232958567952,0.252291562596])
asym_CTEQ_up.append([0.0035009411221,0.00345170193622,0.00317649132594,0.00270895140795,0.00140158230025,0.00123313008034])
asym_CTEQ_lo.append([0.00592160512801,0.00650221949072,0.00743037896512,0.00812806952013,0.00874220691895,0.00844138591726])

#Lepton PT Cut 35.0
#MET Cut 0.0
asym_CTEQ.append([0.102660792277,0.111478234214,0.135821883081,0.156642611572,0.205971543757,0.238594450412])
asym_CTEQ_up.append([0.00301685756724,0.00328755306128,0.00362510354597,0.00373524790485,0.00331087263012,0.00232777022303])
asym_CTEQ_lo.append([0.0047003137211,0.00543789681833,0.00667594522681,0.0077259651617,0.00896224277314,0.0088696214081])

#PT 25

data.append([0.1547,0.1620,0.1749,0.1990,0.2244,0.2663])
stat.append([0.0069,0.0068,0.0070,0.0105,0.0082,0.0086])
syst_up.append([0.0087,0.0089,0.0090,0.0100,0.0096,0.0105])
syst_lo.append([0.0087,0.0089,0.0090,0.0099,0.0096,0.0103]) 

data.append([0.1605,0.1656,0.1791,0.2050,0.2286,0.2710])
stat.append([0.0069,0.0068,0.0070,0.0105,0.0080,0.0085])
syst_up.append([0.0087,0.0089,0.0090,0.0100,0.0096,0.0105])
syst_lo.append([0.0087,0.0089,0.0090,0.0099,0.0096,0.0103])
    
data.append([0.1392,0.1486,0.1532,0.1686,0.2016,0.2437])
stat.append([0.008,0.008,0.0082,0.0122,0.0096,0.0101])
syst_up.append([0.0087,0.0089,0.0090,0.0100,0.0096,0.0105])
syst_lo.append([0.0087,0.0089,0.0090,0.0099,0.0096,0.0103])

data.append([0.1243,0.1188,0.135,0.1384,0.1808,0.2268])
stat.append([0.0097,0.0095,0.0099,0.0148,0.0118,0.0123])
syst_up.append([0.0087,0.0089,0.0090,0.0100,0.0096,0.0105])
syst_lo.append([0.0087,0.0089,0.0090,0.0099,0.0096,0.0103])

#X axis values

cleandata = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]

eta = array("d",[0.2,0.6,1.0,1.3,1.8,2.2])
eta_up = array("d",[0.2,0.2,0.2,0.1,0.2,0.2])
eta_lo = array("d",[0.2,0.2,0.2,0.1,0.2,0.2])


for i in range(len(data)) :
  c2.cd()
  #Add syst and stat in quadrature
  for bin in range(len(stat)) :
    syst_up[i][bin] = math.sqrt(syst_up[i][bin]**2+stat[i][bin]**2)
    syst_lo[i][bin] = math.sqrt(syst_lo[i][bin]**2+stat[i][bin]**2)

  #Convert Python lists to Arrays that ROOT will accept
  asym = array("d",cleandata)#data[i])
  asym_stat = array("d",cleandata)
  asym_syst_up = array("d",syst_up[i])
  asym_syst_lo = array("d",syst_lo[i])
  asym_cteq = array("d",asym_CTEQ[i])
  asym_cteq_up = array("d",asym_CTEQ_up[i])
  asym_cteq_lo = array("d",asym_CTEQ_lo[i])
  
  asym_mstw = array("d",asym_MSTW[i])
  asym_mstw_up = array("d",asym_MSTW_up[i])
  asym_mstw_lo = array("d",asym_MSTW_lo[i])

  #Set up TGraphAsymErrors objects for data (stat and syst+stat) and Theory
  Asym = ROOT.TGraphAsymmErrors(len(asym), eta, asym, eta_lo, eta_up, asym_stat, asym_stat)
  Asym_Syst = ROOT.TGraphAsymmErrors(len(asym), eta, asym, eta_lo, eta_up, asym_syst_lo, asym_syst_up)
  Asym_MSTW = ROOT.TGraphAsymmErrors(len(asym_mstw), eta, asym_mstw, eta_lo, eta_up, asym_mstw_lo, asym_mstw_up)
  Asym_CTEQ = ROOT.TGraphAsymmErrors(len(asym_cteq), eta, asym_cteq, eta_lo, eta_up, asym_cteq_lo, asym_cteq_up)
  #Drawing options
  Asym_Syst.SetLineColor(2)
  Asym_MSTW.SetFillStyle(3004);
  Asym_MSTW.SetFillColor(9);
  Asym_MSTW.SetLineColor(9);
  Asym_CTEQ.SetFillStyle(3002);
  Asym_CTEQ.SetFillColor(2);
  Asym_CTEQ.SetLineColor(2);

  #Legend
  leg.Clear()
  leg.AddEntry(Asym,"Asymmetry (stat)","l")##  
  leg.AddEntry(Asym_Syst,"Asymmetry (stat+syst)","l")##  
  leg.AddEntry(Asym_CTEQ,"CTEQ10W","LF")##  
  leg.AddEntry(Asym_MSTW,"MSTW08","LF")##  
  
  #Multigraph handles drawing multiple graphs
  mGraph = ROOT.TMultiGraph()
  mGraph.SetMaximum(0.4)
  mGraph.SetMinimum(0.)
  mGraph.Add(Asym_Syst,"p")
  mGraph.Add(Asym,"p")
  mGraph.Add(Asym_MSTW,"c3")
  mGraph.Add(Asym_CTEQ,"c3")
  mGraph.Draw("a")

  leg.Draw()
  name = "./Asym_"
  name += str(PTCut[i])
  if  METCut[i]>0 : name += "_MET"+str(METCut[i])
  if Corrected : name += "_cleaned"
  name += ".pdf"

  c2.SaveAs(name)


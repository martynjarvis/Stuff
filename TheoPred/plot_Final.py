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
ptcut = 25
metcut = 20
mtcut = 0
# ------------------------------------------------------------------------------------------------------------------//
ntp_dir = "./"
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

c1 = ROOT.TCanvas("canvas","canvas",0,0,800,600)
c2 = ROOT.TCanvas("asym","asym",0,0,800,600)

leg = ROOT.TLegend(0.6,0.15,0.9,0.3)
leg.SetShadowColor(0)
leg.SetBorderSize(0)
leg.SetFillStyle(4100)
leg.SetFillColor(0)
leg.SetLineColor(0)

#Predictions for lepton charge asymmetry at the 7 TeV LHC using
#MSTW 2008 NNLO PDFs with 90% C.L. asymmetric PDF uncertainties.
g_name = "g_asym_"+str(metcut)+"_"+str(ptcut)+"_"+str(ptcut)+"_"+str(mtcut)

f = open(g_name+'.txt', 'w')

#W_only_lord_CT10w..root  
#W_only_lord_cteq66..root  
#W_only_lord_MSTW200..root

InFile = ROOT.TFile.Open(ntp_dir+"W_only_lord_CT10w..root") 
g_asym_CTEQ10 = InFile.Get(g_name)

InFile = ROOT.TFile.Open(ntp_dir+"W_only_lord_cteq66..root") 
g_asym_CTEQ66 = InFile.Get(g_name)

InFile = ROOT.TFile.Open(ntp_dir+"W_only_lord_MSTW200..root") #W_only_tota_MSTW200.root"
g_asym_MSTW = InFile.Get(g_name)

asym_x   = array("d",[0.2, 0.6, 1.0, 1.3, 1.8, 2.2])
asym_xer = array("d",[0.2, 0.2, 0.2, 0.1, 0.2, 0.2])

if ptcut ==25 :
  asym   = array("d",[0.1541,0.1666,0.1728,0.1895,0.2331,0.2670])
  asym_stat =array("d",[0.0064,0.0064,0.0065,0.0096,0.0076,0.0077])
  asym_syst =array("d",[0.0108,0.0108,0.0110,0.0133,0.0118,0.0118])
if ptcut ==30 :
  asym   = array("d",[0.1330,0.1501,0.1508,0.1651,0.2082,0.2451])
  asym_stat =array("d",[0.0071,0.0071,0.0073,0.0106,0.0087,0.0086])
  asym_syst =array("d",[0.0113,0.0113,0.0117,0.0142,0.0124,0.0124])
if ptcut ==35 :
  asym   = array("d",[0.1191,0.1259,0.1350,0.1385,0.1834,0.2220])
  asym_stat =array("d",[0.0085,0.0084,0.0087,0.0128,0.0105,0.0105])
  asym_syst =array("d",[0.0122,0.0129,0.0127,0.0163,0.0141,0.0145])
if metcut ==20 :
  asym   = array("d",[0.1497,0.1606,0.1695,0.1866,0.2330,0.2700])
  asym_stat =array("d",[0.0064,0.0064,0.0065,0.0097,0.0076,0.0077])
  asym_syst =array("d",[0.0109,0.0109,0.0111,0.0137,0.0120,0.0122])
#x = array("d",[0.0])
#y = array("d",[0.0])

#x = ROOT.Double(0.0)
#y = ROOT.Double(0.0)

#f.write("\n\nCTEQ6.6")
#for i in range(g_asym_CTEQ66.GetN()) :
  #g_asym_CTEQ66.GetPoint(i, x, y)  
  #f.write("\n"+str(x)+"\t"+str(int(y*10000)/10000.0)+"\t+"+ str(int(g_asym_CTEQ66.GetErrorYhigh(i)*10000)/10000.0)+"\t-"+ str(int(g_asym_CTEQ66.GetErrorYlow(i)*10000)/10000.0))

#f.write("\n\nCT10W")
#for i in range(g_asym_CTEQ10.GetN()) :
  #g_asym_CTEQ10.GetPoint(i, x, y) 
  #f.write("\n"+str(x)+"\t"+str(int(y*10000)/10000.0)+"\t+"+ str(int(g_asym_CTEQ10.GetErrorYhigh(i)*10000)/10000.0)+"\t-"+ str(int(g_asym_CTEQ10.GetErrorYlow(i)*10000)/10000.0))

#f.write("\n\nMSTW08NNLO")
#for i in range(g_asym_MSTW.GetN()) :
  #g_asym_MSTW.GetPoint(i, x, y) 
  #f.write("\n"+str(x)+"\t"+str(int(y*10000)/10000.0)+"\t+"+ str(int(  g_asym_MSTW.GetErrorYhigh(i)*10000)/10000.0)+"\t-"+ str(int(  g_asym_MSTW.GetErrorYlow(i)*10000)/10000.0))

#f.close()

Asym_Stat   = ROOT.TGraphAsymmErrors(len(asym)  , asym_x  , asym  , asym_xer  , asym_xer  , asym_stat  , asym_stat)
Asym_Syst   = ROOT.TGraphAsymmErrors(len(asym)  , asym_x  , asym  , asym_xer  , asym_xer  , asym_syst  , asym_syst)

Asym_Syst.SetLineWidth(2)
Asym_Stat.SetLineWidth(2)

Asym_Stat.SetLineColor(1);
Asym_Syst.SetLineColor(2);

g_asym_CTEQ10.SetFillStyle(3001);
g_asym_CTEQ10.SetLineWidth(2)
g_asym_CTEQ10.SetFillColor(46);
g_asym_CTEQ10.SetLineColor(46)

g_asym_MSTW.SetFillStyle(1001);
g_asym_MSTW.SetLineWidth(2)
g_asym_MSTW.SetFillColor(33);
g_asym_MSTW.SetLineColor(38);

#Legend
leg.Clear()
leg.AddEntry(g_asym_CTEQ10,"CTEQ10","LF")##  
leg.AddEntry(g_asym_MSTW,"MSTWNNLO08","LF")##  
leg.AddEntry(Asym_Stat,"Asymmetry (stat)","lp")##  
leg.AddEntry(Asym_Syst,"Asymmetry (stat+syst)","lp")##  

#Multigraph handles drawing multiple graphs
mGraph = ROOT.TMultiGraph()
mGraph.SetMaximum(0.4)
mGraph.SetMinimum(0.)

mGraph.Add(g_asym_MSTW,"3c")
mGraph.Add(g_asym_CTEQ10,"3c")
mGraph.Add(g_asym_MSTW,"cX")

mGraph.Add(Asym_Syst,"p")
mGraph.Add(Asym_Stat,"p")

mGraph.Draw("a")

leg.Draw()
name = "./Asym_"
name += str(ptcut)
name += str(metcut)
name += ".pdf"

c2.SaveAs(name)



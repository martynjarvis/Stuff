#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('/usr/lib/root/')

import ROOT
#import sys
# ------------------------------------------------------------------------------------------------------------------//
#User declared cuts
METCut = 0.0
#PtLCut = 25.0
PtUCut = 5000.0
EtaCut = 2.4

EtaBins = 6

Wplus_ntp = "./ntuples/wplus.root"
Wminus_ntp = "./ntuples/wminus.root"

#Wplus_ntp =  "./ntuples/wp_lhc7_ct66_00.root"
#Wminus_ntp = "./ntuples/wm_lhc7_ct66_00.root"

lumi = 0.01 #In fb, NYI

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

leg = ROOT.TLegend(0.5, 0.15, 0.8, 0.3)
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
eta_plus  = ROOT.TH1F("eta_plus" ,"eta_plus" ,EtaBins,0.0,EtaCut)
eta_minus = ROOT.TH1F("eta_minus","eta_minus",EtaBins,0.0,EtaCut)
asym = ROOT.TH1F("asym","asym",EtaBins,0.0,EtaCut)
asym.SetTitle("Asymmetry")##
asym.GetYaxis().SetRangeUser(0.0,0.4)##
# ------------------------------------------------------------------------------------------------------------------//
   
#MITResults = ((0.1330,0.0113,0.0053),(0.1448,0.0113,0.0122),(0.1578,0.0118,0.0047),(0.1915,0.0159,0.0070),(0.2177,0.0144,0.0084),(0.2341,0.0148,0.0113))
#25

#OurResults = ((0.1662, 0.0064),(0.1751, 0.0064),(0.1878, 0.0065),(0.2078, 0.0085),(0.2484, 0.0077),(0.2809, 0.0081))	#updated 35pb-1 25GeV DF AS correct trigger
#OurResults = ((0.1437,0.0071),(0.157,0.0071),(0.164,0.0074),(0.1826,0.0096),(0.2314,0.0088),(0.2662,0.0092)) 		#updated 35pb-1 30GeV DF AS correct trigger
#OurResults = ((0.1329,0.0085),(0.1317,0.0085),(0.1422,0.0089),(0.1516,0.0117),(0.223,0.0112),(0.2582,0.0116)) 		#updated 35pb-1 35GeV DF AS correct trigger

#W_MC = ((0.1606,0.0069),(0.1683,0.0068),(0.1783,0.0071),(0.2029,0.0105),(0.2275,0.0083),(0.2702,0.0087))
#W_Sil = ((0.1605,0.0069),(0.1697,0.0068),(0.1802,0.007 ),(0.2033,0.0105),(0.2304,0.0082),(0.2741,0.0087))
#W_MET = ((0.1606,0.0069),(0.1668,0.0068),(0.1793,0.007 ),(0.2032,0.0105),(0.2246,0.0082),(0.2669,0.0086))
#W_Metcorr =((0.1548,0.0069),(0.1641,0.0068),(0.1771,0.007),(0.2025,0.0104),(0.2312,0.0082),(0.2753,0.0086))

SCET = ((0.1595,0.0069),(0.1692,0.0068),(0.1809,0.007),(0.2045,0.0105),(0.2336,0.0082),(0.2744,0.0087))
PT = ((0.1605,0.0069),(0.1697,0.0068),(0.1802,0.007),(0.2034,0.0105),(0.231,0.0082),(0.2736,0.0087))

#for j,PtLCut in enumerate([35.0]) :
  #for ntp_name, hist in zip([Wplus_ntp,Wminus_ntp],[eta_plus,eta_minus]) :
    #print "Using Ntuple" , ntp_name
    #InFile = ROOT.TFile.Open(ntp_name) 

    ## Set Up the branch aliases
    #tree = InFile.Get('h10')

    ##def setBranches() :
    #nEntries = tree.GetEntriesFast()
    #bpT_d1 = tree.GetBranch('pT_d1')
    #bpT_d2 = tree.GetBranch('pT_d2')
    #by_d1 = tree.GetBranch('y_d1')
    #by_d2 = tree.GetBranch('y_d2')
    #bpT_B = tree.GetBranch('pT_B')
    #by_B = tree.GetBranch('y_B')
    #bM_B = tree.GetBranch('M_B')
    #bD_phi = tree.GetBranch('D_phi')
    #bcos_the_ = tree.GetBranch('cos_the_')
    #bphi_sta = tree.GetBranch('phi_sta')
    #bDelR34 = tree.GetBranch('DelR34')
    #bWT = tree.GetBranch('WT00')
    #c = MyStruct()

    #bpT_d1.SetAddress(ROOT.AddressOf(c,'pT_d1'))
    #bpT_d2.SetAddress(ROOT.AddressOf(c,'pT_d2'))
    #by_d1.SetAddress(ROOT.AddressOf(c,'y_d1'))
    #by_d2.SetAddress(ROOT.AddressOf(c,'y_d2'))
    #bpT_B.SetAddress(ROOT.AddressOf(c,'pT_B'))
    #by_B.SetAddress(ROOT.AddressOf(c,'y_B'))
    #bM_B.SetAddress(ROOT.AddressOf(c,'M_B'))
    #bD_phi.SetAddress(ROOT.AddressOf(c,'D_phi'))
    #bcos_the_.SetAddress(ROOT.AddressOf(c,'cos_the_'))
    #bphi_sta.SetAddress(ROOT.AddressOf(c,'phi_sta'))
    #bDelR34.SetAddress(ROOT.AddressOf(c,'DelR34'))
    #bWT.SetAddress(ROOT.AddressOf(c,'wt'))    
    ##nEntries = setBranches()
    #hist.Reset()
    #for i in range(0,nEntries):
      #tree.GetEntry(i)
      #if (c.pT_d1 > PtLCut) and (c.pT_d1<PtUCut) and (c.pT_d2 > METCut) :
	#hist.Fill(abs(c.y_d1),c.wt)
      #if (i%25000 == 0) : print "At event: " + str(i)

    ##c1.cd()
    ##hist.Draw()
    ##c1.SaveAs(ntp_name[:-5]+".png")
    
  #c2.cd()
  ##asym = eta_plus.Clone()
  ##asym.Divide(eta_minus)
  #asym.Reset()
  #asym = eta_plus.GetAsymmetry(eta_minus)
  #asym.GetYaxis().SetRangeUser(0.0,0.4)##
  #asym.SetTitle("Asymmetry CTEQ6.6")##
  #asym.SetLineColor(j+38)
  #asym.SetLineWidth(3)
  #leg.AddEntry(asym,"CTEQ6.6 PT>" + str(PtLCut),"l")##
  #if (j==0) :
    #asym.DrawCopy("c hist")
  #else :
    #asym.DrawCopy("c hist same")

#c2.cd()
#asym.Reset()   
#for i, result in enumerate(MITResults) :
  #asym.SetBinContent(i+1,result[0]-(W_MC[i])[0])
  #asym.SetBinError(i+1,0)#asym.SetBinError(i+1,result[1])
#asym.SetLineColor(2)  
#asym.SetLineWidth(2)
#asym.SetMarkerStyle(20);
#ours = asym.Clone()
#leg.AddEntry(ours,"MIT Results (PT>25)","l")##  
#asym.DrawCopy("E1 same")   

#W_MC = ((0.1606,0.0069),(0.1683,0.0068),(0.1783,0.0071),(0.2029,0.0105),(0.2275,0.0083),(0.2702,0.0087))
#W_Sil = ((0.1605,0.0069),(0.1697,0.0068),(0.1802,0.007 ),(0.2033,0.0105),(0.2304,0.0082),(0.2741,0.0087))
#W_MET = ((0.1606,0.0069),(0.1668,0.0068),(0.1793,0.007 ),(0.2032,0.0105),(0.2246,0.0082),(0.2669,0.0086))
#W_Metcorr =((0.1548,0.0069),(0.1641,0.0068),(0.1771,0.007),(0.2025,0.0104),(0.2312,0.0082),(0.2753,0.0086))


asym.Reset()   
for i, result in enumerate(SCET) :
  asym.SetBinContent(i+1,result[0])
  asym.SetBinError(i+1,0.00000000000000000001)#result[1])
asym.SetLineColor(9)  
asym.SetLineWidth(2)
asym.SetMarkerStyle(20);
h0 = asym.Clone()
leg.AddEntry(h0,"SC E_{T} > 25 GeV","l")##  
asym.DrawCopy("E1")  

asym.Reset()   
for i, result in enumerate(PT) :
  asym.SetBinContent(i+1,result[0])
  asym.SetBinError(i+1,0.00000000000000000001)#result[1])
asym.SetLineColor(32)  
asym.SetLineWidth(2)
asym.SetMarkerStyle(20);
h1 = asym.Clone()
leg.AddEntry(h1,"Electron P_{T} > 25 GeV","l")##  
asym.DrawCopy("E1 same") 

leg.Draw()
c2.SaveAs("./ETPTCompare.pdf")
#OutFile.cd()

#EBh_CaloMEt_x_TrckIso_.Write()

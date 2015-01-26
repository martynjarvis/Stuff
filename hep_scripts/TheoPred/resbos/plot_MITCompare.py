#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys 
sys.path.append('/usr/lib/root/')
import ROOT
import sys
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

lumi = 0.015 #In fb, NYI

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

leg = ROOT.TLegend(0.7, 0.15, 0.9, 0.3)
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
#MITResults = ((0.1529,0.0102,0.0077),(0.1589,0.0102,0.0111),(0.1823,0.0106,0.0066),(0.2124,0.0143,0.0090),(0.2370,0.0126,0.0119),(0.2539,0.0131,0.0108),)
#OurResults = ((0.1634,0.0098),(0.1716,0.0098),(0.1948,0.0099),(0.2241,0.013),(0.2495,0.0115),(0.2661,0.0121))
#OurResults = ((0.1659,0.0074),(0.1752,0.0073),(0.1928,0.0075),(0.2169,0.0097),(0.246 ,0.0088),(0.2757,0.0092))#updated 35pb-1 25GeV
#OurResults = ((0.1444,0.0082),(0.1579,0.0081),(0.1659,0.0084),(0.1911,0.0109),(0.2267,0.01),(0.2612,0.0104))#updated 35pb-1 30GeV
#OurResults = ((0.1377,0.0097),(0.1316,0.0097),(0.1447,0.0101),(0.1588,0.0134),(0.2049,0.0128),(0.2507,0.0132))#updated 35pb-1 35GeV
#OurResults = ((0.1673, 0.0074),(0.1762, 0.0073),(0.1944, 0.0075),(0.2148, 0.0098),(0.2472, 0.0088),(0.2753, 0.0092))#updated 35pb-1 25GeV DF AS

#OurResults = ((0.1662, 0.0064),(0.1751, 0.0064),(0.1878, 0.0065),(0.2078, 0.0085),(0.2484, 0.0077),(0.2809, 0.0081))	#updated 35pb-1 25GeV DF AS correct trigger
#OurResults = ((0.1437,0.0071),(0.157,0.0071),(0.164,0.0074),(0.1826,0.0096),(0.2314,0.0088),(0.2662,0.0092)) 		#updated 35pb-1 30GeV DF AS correct trigger
#OurResults = ((0.1329,0.0085),(0.1317,0.0085),(0.1422,0.0089),(0.1516,0.0117),(0.223,0.0112),(0.2582,0.0116)) 		#updated 35pb-1 35GeV DF AS correct trigger

#OurResults = ((0.1541, 0.0069),(0.1639, 0.0068),(0.1741, 0.0071),(0.2015, 0.0105),(0.2319, 0.0082),(0.2716, 0.0087))	#updated 35pb-1 25GeV VBTF ntuples
#OurResults = ((0.1437,0.0071),(0.157,0.0071),(0.164,0.0074),(0.1826,0.0096),(0.2314,0.0088),(0.2662,0.0092)) 		#updated 35pb-1 30GeV VBTF ntuples
#OurResults = ((0.1329,0.0085),(0.1317,0.0085),(0.1422,0.0089),(0.1516,0.0117),(0.223,0.0112),(0.2582,0.0116)) 		#updated 35pb-1 35GeV VBTF ntuples

# #updated 35pb-1 25GeV VBTF ntuples MIT WSHAPE
OurResults    = ((0.1605,0.0069,0.0088,0.0087),(0.1662,0.0068,0.0088,0.0087),(0.1793,0.007,0.0089,0.0088),(0.2028,0.0105,0.0098,0.0097),(0.2241,0.0082,0.0094,0.0092),(0.2661,0.0086,0.0101,0.0098))
OurResultsCor = ((0.1604,0.0069,0.0088,0.0087),(0.1663,0.0068,0.0088,0.0087),(0.1795,0.007,0.0089,0.0088),(0.2045,0.0105,0.0098,0.0097),(0.2285,0.0081,0.0094,0.0092),(0.2717,0.0085,0.0101,0.0098))

MITResults    = ((0.15717,0.00662313,0.00660456),(0.165213,0.00661294,0.00675314),(0.176248,0.00691144,0.00765066),(0.19785,0.0101432,0.0134122),(0.233021,0.00802526,0.00222044),(0.267638,0.00814988,0.00468999))
MITResultsCor = ((0.156695,0.0066151,0.00660456),(0.164863,0.0066671,0.00675314),(0.176931,0.00688727,0.00765066),(0.199568,0.0100256,0.0134122),(0.236797,0.0078937,0.00222044),(0.271668,0.00815971,0.00468999))

for j,PtLCut in enumerate([25.0]) :
  for ntp_name, hist in zip([Wplus_ntp,Wminus_ntp],[eta_plus,eta_minus]) :
    print "Using Ntuple" , ntp_name
    InFile = ROOT.TFile.Open(ntp_name) 

    # Set Up the branch aliases
    tree = InFile.Get('h10')

    #def setBranches() :
    nEntries = tree.GetEntriesFast()
    bpT_d1 = tree.GetBranch('pT_d1')
    bpT_d2 = tree.GetBranch('pT_d2')
    by_d1 = tree.GetBranch('y_d1')
    by_d2 = tree.GetBranch('y_d2')
    bpT_B = tree.GetBranch('pT_B')
    by_B = tree.GetBranch('y_B')
    bM_B = tree.GetBranch('M_B')
    bD_phi = tree.GetBranch('D_phi')
    bcos_the_ = tree.GetBranch('cos_the_')
    bphi_sta = tree.GetBranch('phi_sta')
    bDelR34 = tree.GetBranch('DelR34')
    bWT = tree.GetBranch('WT00')
    c = MyStruct()

    bpT_d1.SetAddress(ROOT.AddressOf(c,'pT_d1'))
    bpT_d2.SetAddress(ROOT.AddressOf(c,'pT_d2'))
    by_d1.SetAddress(ROOT.AddressOf(c,'y_d1'))
    by_d2.SetAddress(ROOT.AddressOf(c,'y_d2'))
    bpT_B.SetAddress(ROOT.AddressOf(c,'pT_B'))
    by_B.SetAddress(ROOT.AddressOf(c,'y_B'))
    bM_B.SetAddress(ROOT.AddressOf(c,'M_B'))
    bD_phi.SetAddress(ROOT.AddressOf(c,'D_phi'))
    bcos_the_.SetAddress(ROOT.AddressOf(c,'cos_the_'))
    bphi_sta.SetAddress(ROOT.AddressOf(c,'phi_sta'))
    bDelR34.SetAddress(ROOT.AddressOf(c,'DelR34'))
    bWT.SetAddress(ROOT.AddressOf(c,'wt'))    
    #nEntries = setBranches()
    hist.Reset()
    for i in range(0,nEntries):
      tree.GetEntry(i)
      if (c.pT_d1 > PtLCut) and (c.pT_d1<PtUCut) and (c.pT_d2 > METCut) :
	hist.Fill(abs(c.y_d1),c.wt)
      if (i%25000 == 0) : print "At event: " + str(i)

    #c1.cd()
    #hist.Draw()
    #c1.SaveAs(ntp_name[:-5]+".png")
    
  c2.cd()
  #asym = eta_plus.Clone()
  #asym.Divide(eta_minus)
  asym.Reset()
  asym = eta_plus.GetAsymmetry(eta_minus)
  asym.GetYaxis().SetRangeUser(0.0,0.4)##
  asym.SetTitle("Asymmetry")##
  asym.SetLineColor(j+38)
  asym.SetLineWidth(3)
  leg.AddEntry(asym,"CTEQ6.6 PT>" + str(PtLCut),"l")##
  if (j==0) :
    asym.DrawCopy("c hist")
  else :
    asym.DrawCopy("c hist same")

c2.cd()
asym.Reset()   
for i, result in enumerate(MITResults) :
  asym.SetBinContent(i+1,result[0])
  asym.SetBinError(i+1,result[2])
asym.SetLineColor(2)  
asym.SetLineWidth(2)
asym.SetMarkerStyle(20);
ours = asym.Clone()
leg.AddEntry(ours,"MIT Results (PT>25)","l")##  
asym.DrawCopy("E1 same")   

  
asym.Reset()   
for i, result in enumerate(OurResults) :
  asym.SetBinContent(i+1,result[0])
  asym.SetBinError(i+1,result[2])
asym.SetLineColor(1)  
asym.SetLineWidth(2)
asym.SetMarkerStyle(20);
mit = asym.Clone()
leg.AddEntry(mit,"Our Results (PT>25)","l")##  
asym.DrawCopy("E1 same")  


leg.Draw()
c2.SaveAs("./asym.png")
#OutFile.cd()

#EBh_CaloMEt_x_TrckIso_.Write()

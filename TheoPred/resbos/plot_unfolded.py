#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/usr/lib/root/')
from math import sqrt
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

leg = ROOT.TLegend(0.6, 0.15, 0.9, 0.3)
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
#eta_plus  = ROOT.TH1F("eta_plus" ,"eta_plus" ,EtaBins*2,-EtaCut,EtaCut)
#eta_minus = ROOT.TH1F("eta_minus","eta_minus",EtaBins*2,-EtaCut,EtaCut)
asymPos = ROOT.TH1F("asymPos","asymPos",EtaBins,0,EtaCut)
asymNeg = ROOT.TH1F("asymNeg","asymNeg",EtaBins,0,EtaCut)
#asym.SetTitle("Asymmetry CTEQ6.6")##
asymPos.GetYaxis().SetRangeUser(0.0,0.4)##
asymNeg.GetYaxis().SetRangeUser(0.0,0.4)##
# ------------------------------------------------------------------------------------------------------------------//

PResults = ((0.1672,0.0097),(0.1699,0.0096),(0.1851,0.0099),(0.1989,0.015),(0.2396,0.0117),(0.2638,0.0126))
MResults = ((0.1536,0.0098 ),(0.1694,0.0097),(0.1752,0.01),(0.2077,0.0148 ),(0.2226,0.0116),(0.2826,0.012))
#PSCResults = ((0.1818,0.0094,0.0077,0.0076),(0.1718,0.0095,0.0078,0.0077),(0.1918,0.0098,0.0077,0.0076),(0.2049,0.0129,0.0078,0.0076),(0.245,0.0115,0.0139,0.0135),(0.2688,0.0124,0.0139,0.0134))
#MSCResults = ((0.1518,0.0096,0.0078,0.0077),(0.175,0.0096,0.0078,0.0077 ),(0.182,0.0098,0.0077,0.0076),(0.2172,0.0129,0.0077,0.0076),(0.2453,0.0114,0.0139,0.0135),(0.2977,0.0117,0.0137,0.0132))

#for j,PtLCut in enumerate([25.0]) :
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

    #c1.cd()
    #hist.Draw()
    #c1.SaveAs(ntp_name[:-5]+".png")
    
  #c2.cd()
  ##asym = eta_plus.Clone()
  ##asym.Divide(eta_minus)
  #asym.Reset()
  #asym = eta_plus.GetAsymmetry(eta_minus)
  #asym.GetYaxis().SetRangeUser(0.0,0.4)##
  #asym.SetTitle("Asymmetry CTEQ6.6")##
  #asym.SetLineColor(j+38)
  #asym.SetLineWidth(3)
  #h0 = asym.Clone()
  #leg.AddEntry(h0,"CTEQ6.6 PT>" + str(PtLCut),"l")##
  #if (j==0) :
    #asym.DrawCopy("c hist")
  #else :
    #asym.DrawCopy("c hist same")


c2.cd()
asymPos.Reset()   
for i, result in enumerate(PResults) :
  asymPos.SetBinContent(i+1,result[0])
  asymPos.SetBinError(i+1,result[1])
asymPos.SetLineColor(2)
asymPos.SetLineWidth(2)
asymPos.SetLineStyle(1)
asymPos.SetTitle("Asymmetry")
asymPos.SetMarkerStyle(20);
leg.AddEntry(asymPos,"Results (eta>0)","lp")##  
asymPos.DrawCopy("E1")   

  
asymNeg.Reset()   
for i, result in enumerate(MResults) :
  asymNeg.SetBinContent(i+1,result[0])
  asymNeg.SetBinError(i+1,result[1])
asymNeg.SetLineColor(1)  
asymNeg.SetLineWidth(2)
asymNeg.SetLineStyle(1)
asymNeg.SetTitle("Asymmetry")
asymNeg.SetMarkerStyle(21);
leg.AddEntry(asymNeg,"Results (eta<0)","lp")##  
asymNeg.DrawCopy("E1 same")  

leg.Draw()
c2.SaveAs("./Unfolded.pdf")




c1.cd()
Ratio = asymPos.Clone()
Ratio.GetYaxis().SetRangeUser(-3.0,3.0)##
Ratio.SetTitle("A(#eta>0), A(#eta<0) Compatibility")
for i, resp, resm in zip(range(EtaBins),PResults,MResults) :
  Ratio.SetBinContent(i+1,(resp[0]-resm[0])/sqrt(resp[1]**2+resm[1]**2))
  Ratio.SetBinError(i+1,0.00000000000000000000000000000000001)
Ratio.SetMarkerStyle(20);
Ratio.Draw("E1")
  #Ratio.Add(QCDSel, -1)


c1.SaveAs("./UnfoldedCompat.pdf")
#OutFile.cd()

#EBh_CaloMEt_x_TrckIso_.Write()

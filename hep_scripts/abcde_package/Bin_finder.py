#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------//
# Standard Imports
import ROOT
import os,sys,getopt,array
import math
# ----------------------------------------------------------------------------------------------------------------------//

root_name = "ResultsWENU_VBTFpreselection_wenuPlus.root"
dir_name  = "Templates_WP80_Ele25/"
hist_name = "h_wpt"
wpt_bins  = 6

# ----------------------------------------------------------------------------------------------------------------------//

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

# ----------------------------------------------------------------------------------------------------------------------//

c_wpt = ROOT.TCanvas("c_wpt","c_wpt",600,600)
c_wpt_int = ROOT.TCanvas("c_wpt_int","c_wpt_int",600,600)

InFile = ROOT.TFile.Open(root_name) 

h_wpt = InFile.Get(dir_name+hist_name)

n_entries = h_wpt.GetEntries()
n_bins    = h_wpt.GetNbinsX()

output = [-1]*wpt_bins
print output
print "%i entries in %i bins" % (n_entries,n_bins)

h_wpt_int = h_wpt.Clone("h_wpt_int")

for bin in range(n_bins) :
  cum_int = h_wpt.Integral(1,bin+1) 
  h_wpt_int.SetBinContent(bin, cum_int)
  for i in range(len(output)) :
    if output[i]< 0 and cum_int >(i+1)*(n_entries/wpt_bins) :
      print "upper edge: ",bin,cum_int
      output[i] = cum_int
  
  
c_wpt.cd()
h_wpt.Draw()
c_wpt.SaveAs("./h_wpt.pdf")  

c_wpt_int.cd()
h_wpt_int.Draw()
c_wpt_int.SaveAs("./h_wpt_int.pdf")

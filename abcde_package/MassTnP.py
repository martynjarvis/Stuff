# MassPlot.py - This script is just designed to run over the 
# Tag and probe to look at the background contributions.

# ------------------------------------------------------------//
# Standard imports -------------------------------------------//
import ROOT
import sys
# ------------------------------------------------------------//
# ABCDE imports ----------------------------------------------//
from conf.abcde_pars import Parameters as pars
# ------------------------------------------------------------//
# Setup ROOT -------------------------------------------------//
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetTitleOffset(1.4,"Y")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
# ------------------------------------------------------------//
# Get Some parameters ----------------------------------------//
Lumi	  = float(pars.LuminosityOfData_)
DataFile  = pars.DataFile_
WenuFiles = pars.WenuFiles_
WenuLumis = pars.WenuLumis_
QCDFiles  = pars.QCDFiles_
QCDLumis  = pars.QCDLumis_
EWKFiles  = pars.EWKFiles_
EWKLumis  = pars.EWKLumis_
ResultsFolder = pars.ResultsFolder_
# ------------------------------------------------------------//
# ------------------------------------------------------------//
Selection 	  = sys.argv[1]
plottingdir 	  = ResultsFolder+'/'+Selection+'Plots/'
backgroundUpScale = 50.
# ------------------------------------------------------------//
# Run over all of the files and make a ROOT files.
# Get the Mass plots from the files
wfiles = [ROOT.TFile(w) for w in WenuFiles]
qfiles = [ROOT.TFile(q) for q in QCDFiles]
efiles = [ROOT.TFile(e) for e in EWKFiles]
dfile  =  ROOT.TFile(DataFile)

h_d = dfile.Get('VBTF'+Selection+'/aux/'+Selection+'MassWP')
for W,L,i in zip(wfiles,WenuLumis,range(len(WenuFiles))):
	hi = W.Get('VBTF'+Selection+'/aux/'+Selection+'MassWP')
	hi.Scale(backgroundUpScale*Lumi/L)
	if i==0: 
		h_w = hi.Clone('cool'+str(i))
	else:
		h_w.Add(hi)

for W,L,i in zip(qfiles,QCDLumis,range(len(QCDFiles))):
	hi = W.Get('VBTF'+Selection+'/aux/'+Selection+'MassWP')
	print W.GetName(), ' ', hi.GetName()
	hi.Scale(backgroundUpScale*Lumi/L)
	if i==0: h_q = hi.Clone()
	else:	 h_q.Add(hi)
	
ewks = []
for W,L,i in zip(efiles,EWKLumis,range(len(EWKFiles))):
	print W.GetName()
	hi = W.Get('VBTF'+Selection+'/aux/'+Selection+'MassWP')
	hi.Scale(backgroundUpScale*Lumi/L)
	ewks.append(hi)
# ------------------------------------------------------------//
# ------------------------------------------------------------//
# Now we want to find the biggest contribution, no suprises
# that its probably the Z and its in the EWK set
Max 	= 0
index   = 0

for i,E in zip(range(len(ewks)),ewks):
 	newMax = E.GetBinContent(E.GetMaximumBin())  
	if newMax > Max: 
		Max = newMax
		index = i

h_z = ewks[index].Clone()
h_z.Scale(1./backgroundUpScale)
ewks.remove(ewks[index])
EWKFiles.remove(EWKFiles[index])
# ------------------------------------------------------------//
# ------------------------------------------------------------//
# Plot The distributions -------------------------------------//
c = ROOT.TCanvas('c','c',1200,900)
c.SetLogy()
# Data sets the titles ---------------------------------------//
# ------------------------------------------------------------//
h_z.SetTitle("Probe Selection - "+Selection)
h_z.GetXaxis().SetTitle('Mee GeV')
h_z.GetYaxis().SetTitle('Arbitrary Units')
h_z.SetMarkerStyle(8)
h_z.SetMarkerSize(0.8)
#h_z.Sumw2()
# ------------------------------------------------------------//
h_z.SetLineWidth(3)
h_z.SetLineColor(46)
h_w.SetFillColor(2)
h_w.SetFillStyle(3001)
h_q.SetFillStyle(3001)
h_q.SetFillColor(3)
for i,h_e in zip(range(len(ewks)),ewks):
  if i+4 == 10: i+=2 # no point in using white
  h_e.SetLineColor(i+4)
  h_e.SetLineWidth(3)
  
leg1 = ROOT.TLegend(0.6,0.45,0.9,0.9)
leg1.SetFillColor(0)

#leg1.AddEntry(h_d, "Data","P")
leg1.AddEntry(h_z, "Z #rightarrow ee","L")
leg1.AddEntry(h_w,"W #rightarrow e#nu","F")
leg1.AddEntry(h_q,"QCD","F")

for f,h_e in zip(EWKFiles,ewks): 
  leg1.AddEntry(h_e,((f.split('_'))[2].split('.'))[0],'L')
  
#h_d.Draw()
h_z.Draw('same')
for h_e in ewks: h_e.Draw('same')
h_q.Draw('same')
h_w.Draw('same')
leg1.Draw()
c.SaveAs(plottingdir+'Mass_TnP.gif')
# ------------------------------------------------------------//
# ------------------------------------------------------------//
# END

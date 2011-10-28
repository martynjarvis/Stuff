# ABCDEOptimize.py
# Nicholas Wardle - Imperial College
# This code is designed to run the ABCDEMethod over the 2D 
# phase space and produce 2D plots to help optimise the 
# boundary choices

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Standard Imports
import ROOT
import sys,os,getopt
import array
# ----------------------------------------------------------------------------------------------------------------------//
# Imports from the package
from conf.abcde_pars import *
from conf.classes import *
# Set up the C Functions -----------------------------------------------------------------------------------------------//
CFunc = C_Functions()
# ----------------------------------------------------------------------------------------------------------------------//
# Standard ROOT settings
# ----------------------------------------------------------------------------------------------------------------------//
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetTitleOffset(1.018,"Y")
ROOT.gStyle.SetTitleOffset(0.75,"X")
ROOT.gROOT.SetBatch(True);
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetTitleSize(0.05,'XY')
# ----------------------------------------------------------------------------------------------------------------------//
# Define a suitable Portion of the space in terms of MET/MT range and Bin numbers
# ----------------------------------------------------------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//
# ------------- User Supplied Data -------------------------------------------------------------------------------------//
optlist = ['-Help']
HELPME  = False
pars = Parameters()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# This is defined in abcde_pars.py
ResultsFolder		=	str(pars.ResultsFolder_)
WenuFiles		=	list(pars.WenuFiles_)
WenuNumbers		=	list(pars.WenuNumbers_)
WenuLumis		=	list(pars.WenuLumis_)
QCDFiles		=	list(pars.QCDFiles_)
QCDLumis		=	list(pars.QCDLumis_)
scaleto			=	float(pars.ScaleTo_)
PforCalo 		= 	str(pars.METType_)
IsoCut 			= 	str(pars.IDType_)
Cuts 			= 	range(pars.XRange_[0],pars.XRange_[1])
Iso_Cuts 		= 	range(pars.YRange_[0],pars.YRange_[1])
# ----------------------------------------------------------------------------------------------------------------------//
tmp,opts = getopt.getopt(sys.argv[0:],'',longopts=optlist)
args = sys.argv[1:]
for o in opts:
	if o == '-Help':
		HELPME = True
		args.remove(o)
if HELPME: 
	PrintHelp('ABCDEOptimize.py')
	sys.exit()
	
if (len(args) == 2) :
# Pick the selection to draw, this will also be the folder plots are drawn in
  Selection		=	str(args[0])	
  BorE			=	str(args[1])	

else:
  print 'Not Enough Command Line Arguments, use -Help '
  sys.exit()

# Tell User what is to be Done
print """Performing ABCDE method in 2D Plane defined by
	 %12s 	(%i -> %i)
	 %12s 	(%i -> %i)""" \
	 %(PforCalo,Cuts[0],Cuts[-1],IsoCut,Iso_Cuts[0],Iso_Cuts[-1])
print "E Box defied using: ", Selection 
print "Taking Events from: ", BorE == 'EB' and 'Barrel' or 'EndCap'

plottingdir = ResultsFolder+'/'+Selection+'Plots/'
if not os.path.isdir(plottingdir):
	print "Please make a folder called", plottingdir
	sys.exit()


# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Deprecated but change to floats here
if PforCalo == 'Mt':
  MET_Cuts = [float(2*c) for c in Cuts]

else:
  MET_Cuts = [float(c) for c in Cuts]

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Turns out to be easiest to set the the individial points in a 2D ROOT Graph ?
rootcounter = 0;
# -----------Open The Files, Wenu,and QCD backgrounds

WenuFileList 	=	[]
QCDFileList	=	[]


for W in WenuFiles:
	if os.path.isfile(W):
		print "Adding Signal File: ", W
		WenuFileList.append(ROOT.TFile(W))
	else:	
		print "No file was found named: ", W
		sys.exit()
for Q in QCDFiles:
	if os.path.isfile(Q):	
		print "Adding QCD Background File: ", Q
		QCDFileList.append(ROOT.TFile(Q))
	else:	
		print "No file was found named: ", Q
		sys.exit()
# ----------------------------------------------------------------------------------------------------------------------//
# ------------ Obtain the 2D histograms from each file -----------------------------------------------------------------//

for i, WenuFile,WenuLumi in zip(range(0,len(WenuFileList)),WenuFileList,WenuLumis):
	try:	hist2D_MEt_x_Iso_Wenutmp = \
	        WenuFile.Get('VBTF'+Selection+"/wenuana"+BorE+'/'+Selection+PforCalo+"MEt_x_"+IsoCut+BorE)
	except NameError:
		print "No Histogram Entry: ", \
		      'VBTF'+Selection+"/wenuana"+BorE+'/'+Selection+PforCalo+"MEt_x_"+IsoCut+BorE
		sys.exit()
	hist2D_MEt_x_Iso_Wenutmp.Scale(scaleto/WenuLumi)
	if i == 0:
		hist2D_MEt_x_Iso_Wenu = hist2D_MEt_x_Iso_Wenutmp.Clone()
	else:
		hist2D_MEt_x_Iso_Wenu.Add(hist2D_MEt_x_Iso_Wenutmp)

for i, QCDFile,QCDLumi in zip(range(0,len(QCDFileList)),QCDFileList,QCDLumis):
	try:	hist2D_MEt_x_Iso_QCDtmp = \
	        QCDFile.Get('VBTF'+Selection+"/wenuana"+BorE+'/'+Selection+PforCalo+"MEt_x_"+IsoCut+BorE)
	except NameError:
		print "No Histogram Entry: ", \
		      'VBTF'+Selection+"/wenuana"+BorE+'/'+Selection+PforCalo+"MEt_x_"+IsoCut+BorE
		sys.exit()
	hist2D_MEt_x_Iso_QCDtmp.Scale(scaleto/QCDLumi)
	if i == 0:
		hist2D_MEt_x_Iso_QCD = hist2D_MEt_x_Iso_QCDtmp.Clone()
	else:
		hist2D_MEt_x_Iso_QCD.Add(hist2D_MEt_x_Iso_QCDtmp)

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Check that Y range is in range of histogram:
MaxY = hist2D_MEt_x_Iso_Wenu.GetNbinsY()
if Iso_Cuts[-1] > MaxY: sys.exit("Y range too high!!! Only %i bins in Y" %MaxY)
# ----------- Set Up some empty lists to be filled on the Way ----------------------------------------------------------//

WFails 		= []
WPasses 	= []

QCDFails 	= []
QCDPasses 	= []

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

for cIsoCut in Iso_Cuts:

  CutBin = int(cIsoCut)
  Cutstr_fail = "WFail_"+str(cIsoCut)
  Cutstr_pass = "WPass_"+str(cIsoCut)

  WFails.append(hist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_fail,CutBin+1,hist2D_MEt_x_Iso_Wenu.GetNbinsY()+1))
  WPasses.append(hist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_pass,1,CutBin))

  Cutstr_fail = "QCDCorrFail_"+str(cIsoCut)
  Cutstr_pass = "QCDCorrPass_"+str(cIsoCut)
  QCDFails.append(hist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_fail,CutBin+1,hist2D_MEt_x_Iso_QCD.GetNbinsY()+1))
  QCDPasses.append(hist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_pass,1,CutBin))

# ----------------------------------------------------------------------------------------------------------------------//
# --- The all important 2D graphs --------------------------------------------------------------------------------------//
METCutsX = []
Graph2D=ROOT.TGraph2D()
dSepGraph2D = ROOT.TGraph2D()
# --- Now detemine the parameters for each of these guys and calculate a signal ----------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
for cIsoCut, Whist_pass,Whist_fail,QCDhist_pass,QCDhist_fail \
    in zip(Iso_Cuts,WPasses,WFails,QCDPasses,QCDFails):

  epsilon_A_list = [float(Whist_pass.Integral(Whist_pass.FindBin(cMEt),Whist_pass.GetNbinsX()+1))/ \
  			 (Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1)) for cMEt in MET_Cuts]
  epsilon_D_list = [float(Whist_fail.Integral(Whist_fail.FindBin(cMEt),Whist_fail.GetNbinsX()+1))/ \
  			 (Whist_fail.Integral(1,Whist_fail.GetNbinsX()+1)) for cMEt in MET_Cuts] 
  epsilon_W_list = [float(Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1))/ \
  			 (Whist_fail.Integral(1,Whist_fail.GetNbinsX()+1)+Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1))\
  			  for cMEt in MET_Cuts]
  
  MCSAlist = [float(Whist_pass.Integral(Whist_pass.FindBin(cMEt), Whist_pass.GetNbinsX() +1)) \
  		    for cMEt in MET_Cuts]
  MCSBlist = [float(Whist_pass.Integral(1,Whist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  MCSClist = [float(Whist_fail.Integral(1,Whist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  MCSDlist = [float(Whist_fail.Integral(Whist_fail.FindBin(cMEt), Whist_fail.GetNbinsX() +1)) \
  		    for cMEt in MET_Cuts]

  SAlist = [float(Whist_pass.Integral(Whist_pass.FindBin(cMEt), Whist_pass.GetNbinsX() +1)) for cMEt in MET_Cuts]
  SBlist = [float(Whist_pass.Integral(1,Whist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  SClist = [float(Whist_fail.Integral(1,Whist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  SDlist = [float(Whist_fail.Integral(Whist_fail.FindBin(cMEt), Whist_fail.GetNbinsX() +1)) for cMEt in MET_Cuts]
  
  # The MC Truth of the Wenu Sample After this we should add the QCD to each N
  Strue = SAlist[0]+SBlist[0]+SClist[0]+SDlist[0]

  QAlist = [float(QCDhist_pass.Integral(QCDhist_pass.FindBin(cMEt), QCDhist_pass.GetNbinsX() +1)) for cMEt in MET_Cuts]
  QBlist = [float(QCDhist_pass.Integral(1,QCDhist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  QClist = [float(QCDhist_fail.Integral(1,QCDhist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  QDlist = [float(QCDhist_fail.Integral(QCDhist_fail.FindBin(cMEt), QCDhist_fail.GetNbinsX() +1)) for cMEt in MET_Cuts]

  NAlist = [SA + QA for SA,QA in zip(SAlist,QAlist)]
  NBlist = [SB + QB for SB,QB in zip(SBlist,QBlist)]
  NClist = [SC + QC for SC,QC in zip(SClist,QClist)]
  NDlist = [SD + QD for SD,QD in zip(SDlist,QDlist)]
  
  S 	 = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,e_W) \
      	    for NA,NB,NC,ND,e_A,e_D,e_W in \
      	    zip(NAlist,NBlist,NClist,NDlist,epsilon_A_list,epsilon_D_list,epsilon_W_list)]

  # We Use the solution which doesnt assume eA = eD
  Su 	= [s[0] for s in S]
  dSep  = [s[2] for s in S] 	
    
  Bias 		= [(100*abs(s-Strue)/s) for s in Su]
  Derive 	= [abs(e)*(p/s) for s,e,p in zip(Su,dSep,epsilon_W_list)]

  # Set the points in the graph
  for i,B,DE in zip(range(len(Su)),Bias,Derive):
  
    METCutsX.append(MET_Cuts[i])

    Graph2D.SetPoint(rootcounter,float(MET_Cuts[i]),float(cIsoCut),B)
    dSepGraph2D.SetPoint(rootcounter,float(MET_Cuts[i]),float(cIsoCut),DE)
    rootcounter = rootcounter+1
    
# Finished all points in 2D space
# ----------------------------------------------------------------------------------------------------------------------//  
# ----------------------------------------------------------------------------------------------------------------------//
# Common axis labels:
ylab = str(IsoCut)+' Cut - Bin # out of '+str(MaxY)
xlab = PforCalo +' #slash{E}_{T} Cut (GeV)'
# ---- Set Up A Canvas to plot the Sensitivity to eP -------------------------------------------------------------------//
Q = ROOT.TCanvas("q","q",0,0,560,360)
Q.SetFrameFillColor(4)
dSepGraph2D.SetTitle('(dS/d#epsilon_{P})*#epsilon_{P}/S - '+BorE)
dSepGraph2D.GetXaxis().SetTitle(xlab)
dSepGraph2D.GetYaxis().SetTitle(ylab) 
dSepGraph2D.Draw("COLZ")
Q.SaveAs(plottingdir+'2D'+PforCalo+IsoCut+BorE+"_KFactor.gif")

# ---- Set Up A Canvas to plot the Bias --------------------------------------------------------------------------------//
C = ROOT.TCanvas("c","c",0,0,560,360)
C.SetFrameFillColor(4)
Graph2D.SetTitle('Signal Bias % at L = '+str(scaleto)+' pb ^{-1} '+BorE)
Graph2D.GetXaxis().SetTitle(xlab)
Graph2D.GetYaxis().SetTitle(ylab)
Graph2D.Draw("COLZ")
C.SaveAs(plottingdir+'2D'+PforCalo+IsoCut+BorE+"_Bias.gif")
# ----------------------------------------------------------------------------------------------------------------------//
# END
# ----------------------------------------------------------------------------------------------------------------------//
# Close the files
for W in WenuFileList:	W.Close()
for Q in QCDFileList:	Q.Close()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# END




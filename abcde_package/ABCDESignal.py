# ABCDESignal.py

# Nicholas Wardle
# Imperial College
# This code is designed to investigate the ABCDE method

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Standard Imports
import ROOT
import math
import array
import sys,os,getopt
# ----------------------------------------------------------------------------------------------------------------------//
# imports from package
from conf.abcde_pars import *
from conf.classes import *
# Set up the C Functions -----------------------------------------------------------------------------------------------//
CFunc = C_Functions()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Set some ROOT syles up
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetTitleOffset(1.4,"Y")
ROOT.gROOT.SetBatch(True)
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Define the systematic somehow in BoxA, BoxB, BoxC, and BoxD give as a fraction
# This hasn't been implemented in these studies yet so best left at 0,0,0,0 for now

Systematics = [0.,0.,0.,0.]
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
optlist = ['-Help']
HELPME = False
tmp,opts = getopt.getopt(sys.argv[0:],'',longopts=optlist)
args = sys.argv[1:]
for o in opts:
	if o == '-Help':
		HELPME = True
		args.remove(o)
if HELPME: 
	PrintHelp('ABCDESignal.py')
	sys.exit()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
pars = Parameters()
if (len(args) == 1) :

  ResultsFolder		=	str(pars.ResultsFolder_)
  WenuFiles		=	list(pars.WenuFiles_)
  WenuNumbers		=	list(pars.WenuNumbers_)
  WenuLumis		=	list(pars.WenuLumis_)

  QCDFiles		=	list(pars.QCDFiles_)
  QCDLumis		=	list(pars.QCDLumis_)

  EWKFiles		=	list(pars.EWKFiles_)
  EWKLumis		=	list(pars.EWKLumis_)

  DataFile		=	str(pars.DataFile_)
  LuminosityOfData	=	float(pars.LuminosityOfData_)

  UseDataDetectorParams	=	bool(pars.UseDataDetectorParams_)

  ErsatzFile		=	str(pars.ErsatzFile_)
  NuAccCorrFile		=	str(pars.NuAccCorrFile_)

  GetStatError		=	bool(pars.GetStatError_)
 
  SystematicsFile	=	list(pars.SystematicsFile_)
  SysHistHigh		=	list(pars.SysHistHigh_)
  SysHistNorm		=	list(pars.SysHistNorm_)
  SysHistLow		=	list(pars.SysHistLow_)

  METCut		=	list(pars.METCuts_)
  Iso_CutsEB 		=	list(pars.Iso_CutsEB_)
  Iso_CutsEE 		=	list(pars.Iso_CutsEE_)
  Iso_Cuts 		= 	Iso_CutsEB[:]

  PlusOrMinus		=	str(pars.PlusOrMinus_)
  EBOnly		=	bool(pars.EBOnly_)
  EEOnly		=	bool(pars.EEOnly_)
  UseErsatz		=	bool(pars.UseErsatz_)
  UseTagAndProbe	=	bool(pars.UseTagAndProbe_)
  scaleto		=	float(pars.ScaleTo_)
  TextOut		=	bool(pars.TextOut_)
  MakePlots		=	bool(pars.MakePlots_)

  MCRescaleToDataN	=	bool(pars.MCRescaleToDataN_)
  met			=	float(pars.MetPick_)

  CorrectTheMCSignal	=	bool(pars.CorrectTheMCSignal_)
  CorrectTheMCQCD	=	bool(pars.CorrectTheMCQCD_)
  Use2DAntiSelection	=	bool(pars.Use2DAntiSelection_)

  QCDCorrectionFile	=	str(pars.QCDCorrectionFile_)
  QCDCorrectionHisto	=	str(pars.QCDCorrectionHisto_)

  QCDAntiSelection2DFile=	str(pars.QCDAntiSelection2DFile_)

  SignalCorrectionFile	=	str(pars.SignalCorrectionFile_)
  SignalCorrectionHisto	=	str(pars.SignalCorrectionHisto_)

  RsEWK			=	bool(pars.RsEWK_)
  RsRes			=	float(pars.RsRes_)
  RsIndex		=	int(pars.RsIndex_)

  IterateABCDE		=	bool(pars.IterateABCDE_)
  Niterations		=	int(pars.Niterations_)

  PforCalo		=	str(pars.METType_)
  IsoCut		=	str(pars.IDType_)

# ----------------------------------------------------------------------------------------------------------------------// 
# Command line, only input is Selection choice -------------------------------------------------------------------------//
  Selection		=	str(sys.argv[1])
# ----------------------------------------------------------------------------------------------------------------------//
# Reassure the user what has been/will be done -------------------------------------------------------------------------//
  PrintWelcome()
  print				"\nUsing ",PforCalo," vs ", IsoCut
  print				"E box defined using: ",Selection

  if UseDataDetectorParams:
	Efficiency	=	float(pars.Efficiency_)
	Acceptance	=	float(pars.Acceptance_)
	scaleto		=	LuminosityOfData
	print			"MC will be scaled to Data Luminosity = ", scaleto
	print			"Using Data efficiency*Acc = ", Efficiency*Acceptance
	if UseTagAndProbe:
		print			"eP will be Taken from TagAndProbe\n" 
	elif UseErsatz:
		print			"eP will be Taken from Ersatz Template\n" 

  else: print			"Using MC efficiency*Acc, scaling ALL samples to ",scaleto

  CaloSectionString	=	''
  if EBOnly and EEOnly: 	sys.exit("Why you so stupid, stupid?\nCannot Have EBOnly and EEObly")
  if EBOnly: 
	print		"Using Barrel Events Only"
	CaloSectionString+='EB'
  if EEOnly: 
	print		"Using EndCap Events Only"
	CaloSectionString+='EE'
  if UseErsatz: print		"Using Parameters (eA,eD) from Ersatz Method"
  if PlusOrMinus in 'PlusMinus' and PlusOrMinus != '':
		print		"Using Electrons with charge ", PlusOrMinus
  if IterateABCDE and MCRescaleToDataN: 
		if Niterations < 1: 
			Niterations = 1
			print "Not iterating ABCDE, need at least N = 1 for a single iteration"
		else: 
			Niterations += 1
			print "Iterating the ABCDE Method wth %d iterations" %(Niterations-1)
  else :
		print "Not iterating ABCDE (Did you have MCRescaleToDataN set to False?)"
		Niterations = 1 
  if Use2DAntiSelection and CorrectTheMCQCD: 
  		print "Warning! You have set the QCD to be made from 1D and 2D template"
  		print "The 2D template will be used here"
  if RsEWK:
		print "Modyfying EWK resolution of EWK file: \n%s by fraction %.2f " \
		       %(EWKFiles[RsIndex], RsRes)

  print '\n'
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
else:
  print "Wrong Number of Arguments, use -Help"
  sys.exit()

plottingdir = ResultsFolder+'/'+Selection+'Plots/'
if not os.path.isdir(plottingdir):
	print "Please make a folder called", plottingdir
	sys.exit()

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Some Constants used here and there
TotalN = scaleto*reduce(lambda a,b: a+b, [float(N)/L for N,L in zip(WenuNumbers,WenuLumis)]) 
Norm   = 0
ASNorm = 0
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//
# -----------Open The Files, Wenu, QCD backgrounds and Data ------------------------------------------------------------//

WenuFileList 	=	[]
QCDFileList	=	[]
EWKFileList	=	[]

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
for E in EWKFiles:
	if os.path.isfile(E):	
		print "Adding EWK Background File: ", E
		EWKFileList.append(ROOT.TFile(E))
	else:	
		print "No file was found named: ", E
		sys.exit()
		
if os.path.isfile(DataFile):	
	DataFile = ROOT.TFile(DataFile)
else:				
   	print "No file was found named ",DataFile
	sys.exit()

if Use2DAntiSelection:
	if not (IsoCut == 'TrckRelIso'): 
		print "2D Anti-selection is only relevant with Trck RelIso currently"
		Use2DAntiSelection = False
	else:
		if os.path.isfile(QCDAntiSelection2DFile):
			QCDAntiSelection2D = ROOT.TFile(QCDAntiSelection2DFile)
		else:	
			print "No file was found named", QCDAntiSelection2DFile
			sys.exit()

if UseErsatz:
	if PforCalo == 'Mt':
		print 'Cannot Use Ersatz MT yet -> Defaulting to using Wenu MC'
		UseErsatz = False
	else:
	  ErsatzFile	= ROOT.TFile(ErsatzFile)
	  NuAccCorrFile	= ROOT.TFile(NuAccCorrFile)
# ----------------------------------------------------------------------------------------------------------------------//
# A file which holds all histograms and fit results from statistical error calculations

Stats_Out = ROOT.TFile(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_Stats_Out.root","RECREATE")

#Some alternate distribtions provided to determine systematic error

#Sys1File = ROOT.TFile("ElectronMet.root")
SysFiles = []
if len(SystematicsFile) == 0:	print "No Systematic Errors Given"
else:
  for Sys in SystematicsFile:
    sysName = list(Sys.split('.'))[0]+PlusOrMinus+'.root'
    if os.path.isfile(sysName):  SysFiles.append(ROOT.TFile(sysName))
    else:
	print "No File was found named: ", Sys
	sys.exit()

# ------------Obtain the 2D histograms from each file ------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Barrel

for i, WenuFile,WenuLumi in zip(range(0,len(WenuFileList)),WenuFileList,WenuLumis):
	EBhist2D_MEt_x_Iso_Wenutmp = WenuFile.Get('VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus)
	if EBhist2D_MEt_x_Iso_Wenutmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus
		print "In File: ",WenuFile.GetName()
		sys.exit()
	else:	EBhist2D_MEt_x_Iso_Wenutmp.Scale(scaleto/WenuLumi)
	if i == 0:
		EBhist2D_MEt_x_Iso_Wenu = EBhist2D_MEt_x_Iso_Wenutmp.Clone()
	else:
		EBhist2D_MEt_x_Iso_Wenu.Add(EBhist2D_MEt_x_Iso_Wenutmp)

for i, QCDFile,QCDLumi in zip(range(0,len(QCDFileList)),QCDFileList,QCDLumis):
	EBhist2D_MEt_x_Iso_QCDtmp = QCDFile.Get('VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus)
	if EBhist2D_MEt_x_Iso_QCDtmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus
		print "In File: ",QCDFile.GetName()
		sys.exit()
	else:	EBhist2D_MEt_x_Iso_QCDtmp.Scale(scaleto/QCDLumi)
	if i == 0:
		EBhist2D_MEt_x_Iso_QCD = EBhist2D_MEt_x_Iso_QCDtmp.Clone()
	else:
		EBhist2D_MEt_x_Iso_QCD.Add(EBhist2D_MEt_x_Iso_QCDtmp)

for i, EWKFile,EWKLumi in zip(range(0,len(EWKFileList)),EWKFileList,EWKLumis):
	EBhist2D_MEt_x_Iso_EWKtmp = EWKFile.Get('VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus)
	if EBhist2D_MEt_x_Iso_EWKtmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus
		print "In File: ",EWKFile.GetName()
		sys.exit()
	else:	EBhist2D_MEt_x_Iso_EWKtmp.Scale(scaleto/EWKLumi)
	if RsEWK and i == RsIndex: EBhist2D_MEt_x_Iso_EWKtmp = \
			  ReResolution(EBhist2D_MEt_x_Iso_EWKtmp,RsRes)
	if i == 0:
		EBhist2D_MEt_x_Iso_EWK = EBhist2D_MEt_x_Iso_EWKtmp.Clone()
	else:
		EBhist2D_MEt_x_Iso_EWK.Add(EBhist2D_MEt_x_Iso_EWKtmp)

if UseErsatz:
	EBhist2D_MEt_x_Iso_Ersatz = ErsatzFile.Get("ersatzPlotter/"+PforCalo+"MEt_x_"+IsoCut+'EB')
	if EBhist2D_MEt_x_Iso_Ersatz is None:
		print "No Histogram Entry: ", "ersatzPlotter/"+PforCalo+"MEt_x_"+IsoCut+'EB'
		print "In File : ", ErsatzFile.GetName()
		sys.exit()

EBhist2D_MEt_x_Iso_Data = DataFile.Get('VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus)
if EBhist2D_MEt_x_Iso_Data is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'+PlusOrMinus
		print "In File : ", DataFile.GetName()
		sys.exit()
else:	EBhist2D_MEt_x_Iso_Data.Scale(scaleto/LuminosityOfData)

if Use2DAntiSelection:
	EBhist_QCDAntiSelection = QCDAntiSelection2D.Get('VBTF'+Selection+"/qcdanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB')
	if EBhist_QCDAntiSelection is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/qcdanaEB/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EB'
		print "In File : ", QCDAntiSelection2D.GetName()
		sys.exit()
		

EBhist_TagAndProbe = DataFile.Get('VBTF'+Selection+"/tagandprobeEB/"+Selection+IsoCut+'EB'+PlusOrMinus)
if EBhist_TagAndProbe is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/tagandprobeEB/"+Selection+IsoCut+'EB'+PlusOrMinus
		print "In File: ", DataFile.GetName()
		sys.exit()

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Endcaps
for i, WenuFile,WenuLumi in zip(range(0,len(WenuFileList)),WenuFileList,WenuLumis):
	EEhist2D_MEt_x_Iso_Wenutmp = WenuFile.Get('VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus)
	if EEhist2D_MEt_x_Iso_Wenutmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus
		print "In File: ", WenuFile.GetName()
		sys.exit()
	else:	EEhist2D_MEt_x_Iso_Wenutmp.Scale(scaleto/WenuLumi)
	if i == 0:
		EEhist2D_MEt_x_Iso_Wenu = EEhist2D_MEt_x_Iso_Wenutmp.Clone()
	else:
		EEhist2D_MEt_x_Iso_Wenu.Add(EEhist2D_MEt_x_Iso_Wenutmp)

for i, QCDFile,QCDLumi in zip(range(0,len(QCDFileList)),QCDFileList,QCDLumis):
	EEhist2D_MEt_x_Iso_QCDtmp = QCDFile.Get('VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus)
	if EEhist2D_MEt_x_Iso_QCDtmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus
		print "In File: ", QCDFile.GetName()
		sys.exit()
	else:	EEhist2D_MEt_x_Iso_QCDtmp.Scale(scaleto/QCDLumi)
	if i == 0:
		EEhist2D_MEt_x_Iso_QCD = EEhist2D_MEt_x_Iso_QCDtmp.Clone()
	else:
		EEhist2D_MEt_x_Iso_QCD.Add(EEhist2D_MEt_x_Iso_QCDtmp)

for i, EWKFile,EWKLumi in zip(range(0,len(EWKFileList)),EWKFileList,EWKLumis):
	EEhist2D_MEt_x_Iso_EWKtmp = EWKFile.Get('VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus)
	if EEhist2D_MEt_x_Iso_EWKtmp is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus
		print "In File: ", EWKFile.GetName()
		sys.exit()
	else:	EEhist2D_MEt_x_Iso_EWKtmp.Scale(scaleto/EWKLumi)
	if RsEWK and i == RsIndex: EEhist2D_MEt_x_Iso_EWKtmp = \
			  ReResolution(EEhist2D_MEt_x_Iso_EWKtmp,RsRes)
	if i == 0:
		EEhist2D_MEt_x_Iso_EWK = EEhist2D_MEt_x_Iso_EWKtmp.Clone()

	else:
		EEhist2D_MEt_x_Iso_EWK.Add(EEhist2D_MEt_x_Iso_EWKtmp)

if UseErsatz:
	EEhist2D_MEt_x_Iso_Ersatz = ErsatzFile.Get("ersatzPlotter/"+PforCalo+"MEt_x_"+IsoCut+'EE')
	if EEhist2D_MEt_x_Iso_Ersatz is None:
		print "No Histogram Entry: ", "ersatzPlotter/",PforCalo,"MEt_x_",IsoCut,'EE',PlusOrMinus
		sys.exit()

EEhist2D_MEt_x_Iso_Data = DataFile.Get('VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus)
if EEhist2D_MEt_x_Iso_Data is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/wenuanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'+PlusOrMinus
		print "In File: ", DataFile.GetName()
		sys.exit()
else:	EEhist2D_MEt_x_Iso_Data.Scale(scaleto/LuminosityOfData)

if Use2DAntiSelection:
	EEhist_QCDAntiSelection = QCDAntiSelection2D.Get('VBTF'+Selection+"/qcdanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE')
	if EEhist_QCDAntiSelection is None:
		print "No Histogram Entry: ", 'VBTF'+Selection+"/qcdanaEE/"+Selection+PforCalo+"MEt_x_"+IsoCut+'EE'
		print "In File : ", QCDAntiSelection2D.GetName()
		sys.exit()

EEhist_TagAndProbe = DataFile.Get('VBTF'+Selection+"/tagandprobeEE/"+Selection+IsoCut+'EE'+PlusOrMinus)
if EEhist_TagAndProbe is None:
		print "No Histogram Entry: ",'VBTF'+Selection+"/tagandprobeEE/"+Selection+IsoCut+'EE'+PlusOrMinus
		print "In File: ", DataFile.GetName()
		sys.exit()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Thats it for the User Inputs and File inputting ---------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//
# Get The systematic Error histogramss:
if PforCalo =='Mt':
  print  "Warning, MT not supported currently!"

SysUp 		= []
SysNormal	= []
SysDown		= []
  
for Sys1,sh,sn,sl in zip(SysFiles,SysHistHigh,SysHistNorm,SysHistLow):

  systmp	 = Sys1.Get(sh)
  SysUp.append(systmp)
  if systmp is None:	sys.exit("No histogram %s in %s" %(sh,Sys1.GetName()))
  systmp 	= Sys1.Get(sn)
  SysNormal.append(systmp)
  if systmp is None:	sys.exit("No histogram %s in %s" %(sn,Sys1.GetName()))
  systmp 	= Sys1.Get(sl)
  SysDown.append(systmp)
  if systmp is None: sys.exit("No histogram %s in %s" %(sl,Sys1.GetName()))
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

EBstep = float(EBhist2D_MEt_x_Iso_Wenu.GetYaxis().GetXmax())/EBhist2D_MEt_x_Iso_Wenu.GetYaxis().GetNbins()
EEstep = float(EEhist2D_MEt_x_Iso_Wenu.GetYaxis().GetXmax())/EEhist2D_MEt_x_Iso_Wenu.GetYaxis().GetNbins()
step = EBstep


WFails 		= 	[]
WPasses 	= 	[]

QCDFails 	= 	[]
QCDPasses	= 	[]

EWKFails 	=	[]
EWKPasses 	=	[]

DataFails 	=	[]
DataPasses 	= 	[]

if UseErsatz:
  ErsatzPasses 	= 	[]
  ErsatzFails 	= 	[]
	
if Use2DAntiSelection:
  ASPasses	=	[]
  ASFails	=	[]

TagAndProbe_eP	= 	[]
TagAndProbe_epERR= 	[]

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Run over each choice of value for Reconstruction Variable cut, ie the one which separated AB/CD 

for cIsoCutEB,cIsoCutEE in zip(Iso_CutsEB,Iso_CutsEE):

  CutBinEE = int(cIsoCutEE)
  CutBinEB = int(cIsoCutEB)

  # TagAndProbe - pass is from 1,CutBinEB. Careful not to go into Y overflow!!!
  NumPassingEventsEB = EBhist_TagAndProbe.Integral(1,CutBinEB)
  NumPassingEventsEE = EEhist_TagAndProbe.Integral(1,CutBinEE)
  NumberEB	     = EBhist_TagAndProbe.Integral(1,EBhist_TagAndProbe.GetNbinsX())
  NumberEE	     = EEhist_TagAndProbe.Integral(1,EEhist_TagAndProbe.GetNbinsX())

  if EBOnly:	
  	TagAndProbe_eP.append(float(NumPassingEventsEB)/NumberEB)
  	TagAndProbe_epERR.append(CFunc.FracError(NumPassingEventsEB,NumberEB))
  elif EEOnly:	
  	TagAndProbe_eP.append(float(NumPassingEventsEE)/NumberEE)
  	TagAndProbe_epERR.append(CFunc.FracError(NumPassingEventsEE,NumberEE))
  	
  else:		
  	TagAndProbe_eP.append(float(NumPassingEventsEB+NumPassingEventsEE)/ \
				            (NumberEB+NumberEE))
	TagAndProbe_epERR.append(CFunc.FracError(NumPassingEventsEB+NumPassingEventsEE, \
					   NumberEB+NumberEE))		     

  # Wenu
  Cutstr_failEB = "EBWFail_"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEB = "EBWPass_"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_failEE = "EEWFail_"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEE = "EEWPass_"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

  WEE = EEhist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_failEE,CutBinEE+1,EEhist2D_MEt_x_Iso_Wenu.GetNbinsY())
  WEB = EBhist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist2D_MEt_x_Iso_Wenu.GetNbinsY())


  WEEP = EEhist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_passEE,0,CutBinEE)
  WEBP = EBhist2D_MEt_x_Iso_Wenu.ProjectionX(Cutstr_passEB,0,CutBinEB)
  
  SBarrel = float(WEB.Integral(1,WEB.GetNbinsX()+1) + \
  	    WEBP.Integral(1,WEB.GetNbinsX()+1))
  SEndCap = float(WEE.Integral(1,WEE.GetNbinsX()+1) + \
  	    WEEP.Integral(1,WEE.GetNbinsX()+1))

  if EBOnly:
	WFails.append(WEB)
        WPasses.append(WEBP)
  elif EEOnly:
	WFails.append(WEE)
        WPasses.append(WEEP)
  else:
	WEB.Add(WEE)
  	WEBP.Add(WEEP)
  	WFails.append(WEB)
  	WPasses.append(WEBP)
  
  #QCD
  Cutstr_failEB = "QCDCorrFail_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEB = "QCDCorrPass_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_failEE = "QCDCorrFail_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEE = "QCDCorrPass_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

  QEE = EEhist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_failEE,CutBinEE+1,EEhist2D_MEt_x_Iso_QCD.GetNbinsY())
  QEB = EBhist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist2D_MEt_x_Iso_QCD.GetNbinsY())

  QEEP = EEhist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_passEE,0,CutBinEE)
  QEBP = EBhist2D_MEt_x_Iso_QCD.ProjectionX(Cutstr_passEB,0,CutBinEB)


  if EBOnly:
	QCDFails.append(QEB)
        QCDPasses.append(QEBP)
  elif EEOnly:
	QCDFails.append(QEE)
        QCDPasses.append(QEEP)
  else:
	QEB.Add(QEE)
  	QEBP.Add(QEEP)
  	QCDFails.append(QEB)
  	QCDPasses.append(QEBP)


  #EWK
  Cutstr_failEB = "EWKCorrFail_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEB = "EWKCorrPass_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_failEE = "EWKCorrFail_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEE = "EWKCorrPass_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

  
  BEE = EEhist2D_MEt_x_Iso_EWK.ProjectionX(Cutstr_failEE,CutBinEE+1,EEhist2D_MEt_x_Iso_EWK.GetNbinsY())
  BEB = EBhist2D_MEt_x_Iso_EWK.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist2D_MEt_x_Iso_EWK.GetNbinsY())

  BEEP = EEhist2D_MEt_x_Iso_EWK.ProjectionX(Cutstr_passEE,0,CutBinEE)
  BEBP = EBhist2D_MEt_x_Iso_EWK.ProjectionX(Cutstr_passEB,0,CutBinEB)

  
  if EBOnly:
	EWKFails.append(BEB)
        EWKPasses.append(BEBP)
  elif EEOnly:
	EWKFails.append(BEE)
        EWKPasses.append(BEEP)
  else:
	BEB.Add(BEE)
  	BEBP.Add(BEEP)
  	EWKFails.append(BEB)
  	EWKPasses.append(BEBP)


  #Data
  Cutstr_failEB = "DataCorrFail_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEB = "DataCorrPass_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_failEE = "DataCorrFail_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
  Cutstr_passEE = "DataCorrPass_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

  DEE = EEhist2D_MEt_x_Iso_Data.ProjectionX(Cutstr_failEE,CutBinEE+1,EEhist2D_MEt_x_Iso_Data.GetNbinsY())
  DEB = EBhist2D_MEt_x_Iso_Data.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist2D_MEt_x_Iso_Data.GetNbinsY())

  DEEP = EEhist2D_MEt_x_Iso_Data.ProjectionX(Cutstr_passEE,0,CutBinEE)
  DEBP = EBhist2D_MEt_x_Iso_Data.ProjectionX(Cutstr_passEB,0,CutBinEB)

  if EBOnly:
	DataFails.append(DEB)
        DataPasses.append(DEBP)
  elif EEOnly:
	DataFails.append(DEE)
        DataPasses.append(DEEP)
  else:
	DEB.Add(DEE)
  	DEBP.Add(DEEP)
  	DataFails.append(DEB)
  	DataPasses.append(DEBP) 


  # Ersatz
  if UseErsatz:
    
    NuAccCorrhist = NuAccCorrFile.Get('NuAcceptanceCorr_'+PforCalo+'MEt'+PlusOrMinus)

    Cutstr_failEB = "ErsatzCorrFail_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_passEB = "ErsatzCorrPass_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_failEE = "ErsatzCorrFail_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_passEE = "ErsatzCorrPass_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

    ErsEE = EEhist2D_MEt_x_Iso_Ersatz.ProjectionX(Cutstr_failEE,CutBinEE+1,EEhist2D_MEt_x_Iso_Ersatz.GetNbinsY())
    ErsEB = EBhist2D_MEt_x_Iso_Ersatz.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist2D_MEt_x_Iso_Ersatz.GetNbinsY())

    ErsEEP = EEhist2D_MEt_x_Iso_Ersatz.ProjectionX(Cutstr_passEE,0,CutBinEE)
    ErsEBP = EBhist2D_MEt_x_Iso_Ersatz.ProjectionX(Cutstr_passEB,0,CutBinEB)

    if EBOnly:
        ErsEB.Sumw2()
        ErsEBP.Sumw2()  
	ErsatzFails.append(ErsEB)
        ErsatzPasses.append(ErsEBP)
    elif EEOnly:
        ErsEE.Sumw2()
        ErsEEP.Sumw2()  
	ErsatzFails.append(ErsEE)
        ErsatzPasses.append(ErsEEP)
    else:
        ErsEB.Sumw2()
        ErsEBP.Sumw2() 
	ErsEB.Add(ErsEE)
  	ErsEBP.Add(ErsEEP)
  	ErsatzFails.append(ErsEB)
  	ErsatzPasses.append(ErsEBP) 
 
    # For now need to sort out the WenuResults thing to give less bins :) 
    #ErsEB.Multiply(NuAccCorrhist)
    #ErsEBP.Multiply(NuAccCorrhist)
  
  # QCDAntiSelection  
  if Use2DAntiSelection:
    
    Cutstr_failEB = "AntiSelectioFail_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_passEB = "AntiSelectionPass_EB"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_failEE = "AntiSelection_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)
    Cutstr_passEE = "AntiSelection_EE"+str(cIsoCutEB)+'_'+str(cIsoCutEE)

    # Remember to definitely not go over the upper edge in Y as the antiselection has overflow there which
    # We dont want!
    
    ASEB = EBhist_QCDAntiSelection.ProjectionX(Cutstr_failEB,CutBinEB+1,EBhist_QCDAntiSelection.GetNbinsY())
    ASEE = EEhist_QCDAntiSelection.ProjectionX(Cutstr_failEE,CutBinEB+1,EEhist_QCDAntiSelection.GetNbinsY())
    
    ASEBP = EBhist_QCDAntiSelection.ProjectionX(Cutstr_passEE,0,CutBinEE)
    ASEEP = EEhist_QCDAntiSelection.ProjectionX(Cutstr_passEB,0,CutBinEB)
    
    
    if EBOnly:
	ASFails.append(ASEB)
        ASPasses.append(ASEBP)
    elif EEOnly:
	ASFails.append(ASEE)
        ASPasses.append(ASEEP)
    else:
	ASEB.Add(ASEE)
  	ASEBP.Add(ASEEP)
  	ASFails.append(ASEB)
  	ASPasses.append(ASEBP) 

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

# Decide on MET/MT cut ranges (the step will be based on the size of the bins) -----------------------------------------//

MetStep = DataPasses[0].GetBinWidth(1)
Cuts = range(METCut[0],METCut[1]+int(MetStep),int(MetStep))  

# The MET/MT Cuts (these should be considered as numbers not bin numbers though should be integer)

if PforCalo == 'Mt':
  Cuts = range(Cuts[0], 2*Cuts[-1], int(MetStep))
  MET_Cuts = [float(c) for c in Cuts]

# The Reconstruction Variable cuts are single valued here but mulitple choices can be investigated simulateously
# by the use of a list. Separate plots will be made for each cut.

else:
  MET_Cuts = [float(c) for c in Cuts]
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Run over the all of the 1D histos and make corrected ones from the sys file./ Data QCD file

if CorrectTheMCSignal:
	if PforCalo == 'Pf':
	  SignalCorrectionFile = list(SignalCorrectionFile.split('.'))[0]+PlusOrMinus+'.root'
	  if os.path.isfile(SignalCorrectionFile):
		print "\nCorrecting MC Signal using: ", SignalCorrectionHisto
		SignalData = ROOT.TFile(SignalCorrectionFile)
		Signalhisto = SignalData.Get(SignalCorrectionHisto)
		if Signalhisto is None: sys.exit("Correction Histogram: "+SignalCorrectionHisto+"NotFound")
	  else: sys.exit("No such file as %s" %(SignalCorrectionFile))
	  for i in range(0,len(WPasses)):
		WPasses[i],WFails[i] = CorrectHistos(WPasses[i],WFails[i],Signalhisto)
	  #SignalData.Close()

	else : print "No DATA corrected W for anything but Pf yet \
		Not Correcting the histos"

if Use2DAntiSelection:
   # In this case, we have already made sure that the Iso is TrckRelIso
   # Just replace the QCD histograms with the AntiSelections but normalised to the MC ones :)
   Norm   = float(QCDPasses[0].Integral(1,QCDPasses[0].GetNbinsX())) + \
   	    float(QCDFails[0].Integral(1,QCDFails[0].GetNbinsX()))
   
   ASNorm = float(ASPasses[0].Integral(1,ASPasses[0].GetNbinsX())) + \
   	    float(ASFails[0].Integral(1,ASFails[0].GetNbinsX()))
   	        	
   for i in range(len(QCDPasses)):
   	# Get The norms from the MC before we replace them
   	  	
   	ASPasses[i].Scale(Norm/ASNorm)
   	ASFails[i].Scale(Norm/ASNorm)
   	   	
   	QCDPasses[i] = ASPasses[i]
   	QCDFails[i]  = ASFails[i]
   	
   # And now the QCD is the anti-selected
   
   		
elif CorrectTheMCQCD: 
	if PforCalo == 'Pf':
	  if os.path.isfile(QCDCorrectionFile):  
		print "\nCorrecting MC QCD using: ", QCDCorrectionHisto
		QCDData = ROOT.TFile(QCDCorrectionFile)
		QCDhisto = QCDData.Get(QCDCorrectionHisto)
		if QCDhisto is None: sys.exit("Correction Histogram: "+QCDCorrectionHisto+"NotFound")
	  else: sys.exit("No such file as %s" %(QCDCorrectionFile))
	  for i in range(0,len(QCDPasses)):
		QCDPasses[i],QCDFails[i] = CorrectHistos(QCDPasses[i],QCDFails[i],QCDhisto)
	  #QCDData.Close()
	else : print "No DATA corrected QCD for anything but Pf yet \
		Not Correcting the histos"

		
# Done playing with the MC templates
# ----------------------------------------------------------------------------------------------------------------------//	       
# --- Now detemine the parameters for each of these guys and calculate a signal ----------------------------------//

for k,cIsoCut, Whist_pass,Whist_fail,QCDhist_pass,QCDhist_fail, \
    EWKhist_pass, EWKhist_fail, Dhist_pass,Dhist_fail \
    in zip(range(0,len(Iso_Cuts)),Iso_Cuts,WPasses,WFails,QCDPasses,QCDFails, \
    EWKPasses, EWKFails, DataPasses,DataFails):

  # Set Up some empty lists to fill with systematics
  # --------------------------------------------------------//
  epsilonUp_A_list	= []
  epsilonUp_D_list	= []
  epsilonDown_A_list	= []
  epsilonDown_D_list	= []
  SuMax			= []
  SuMin			= []
  SuMaxdata		= []
  SuMindata		= []
  SdMax			= []
  SdMin			= []
  SdMaxdata		= []
  SdMindata		= []
  # --------------------------------------------------------//
  # --------------------------------------------------------//  
  
  cIsoCut = step*cIsoCut
  cIsoCutEB = Iso_CutsEB[k]
  cIsoCutEE = Iso_CutsEE[k]
 
  MCSAlist = [float(Whist_pass.Integral(Whist_pass.FindBin(cMEt), Whist_pass.GetNbinsX() +1)) for cMEt in MET_Cuts]
  MCSBlist = [float(Whist_pass.Integral(1,Whist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  MCSClist = [float(Whist_fail.Integral(1,Whist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  MCSDlist = [float(Whist_fail.Integral(Whist_fail.FindBin(cMEt), Whist_fail.GetNbinsX() +1)) for cMEt in MET_Cuts]
  
  Dhist_pass.Sumw2()
  Dhist_fail.Sumw2()

  SAlist = [float(Whist_pass.Integral(Whist_pass.FindBin(cMEt), Whist_pass.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]
  SBlist = [float(Whist_pass.Integral(1,Whist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  SClist = [float(Whist_fail.Integral(1,Whist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  SDlist = [float(Whist_fail.Integral(Whist_fail.FindBin(cMEt), Whist_fail.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]

  Strue = float(Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1) + Whist_fail.Integral(1,Whist_fail.GetNbinsX()+1))


  epsilon_A_list = [sa/(sa+sb) \
                   for sa,sb in zip(SAlist,SBlist)]
  epsilon_D_list = [sd/(sd+sc) \
                   for sd,sc in zip(SDlist,SClist)] 

  eW = float(Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1))/(Whist_fail.Integral(1, \
		    Whist_fail.GetNbinsX()+1) +Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1))

  if not len(SystematicsFile) == 0:
  
   for Sys1Up,Sys1Normal,Sys1Down in zip(SysUp,SysNormal,SysDown):
     epsAUpOverNormal=\
     [(float(Sys1Up.Integral(Sys1Up.FindBin(cMEt),Sys1Up.GetNbinsX()+1))/(Sys1Up.Integral(1,Sys1Up.GetNbinsX()+1)))/\
     (float(Sys1Normal.Integral(Sys1Normal.FindBin(cMEt),Sys1Normal.GetNbinsX()+1))/(Sys1Normal.Integral(1, \
         Sys1Normal.GetNbinsX()+1))) \
      for cMEt in MET_Cuts]

     epsilonUp = [e*eA for e,eA in zip(epsAUpOverNormal,epsilon_A_list)]
     epsilonUp_A_list.append(epsilonUp)
     epsilonUp_D_list.append([e*d/a for e,d,a in zip(epsilonUp,epsilon_D_list,epsilon_A_list)])

     epsADownOverNormal=\
     [(float(Sys1Down.Integral(Sys1Down.FindBin(cMEt),Sys1Down.GetNbinsX()+1))/(Sys1Down.Integral(1, \
      Sys1Down.GetNbinsX()+1)))/(float(Sys1Normal.Integral(Sys1Normal.FindBin(cMEt), \
      Sys1Normal.GetNbinsX()+1))/(Sys1Normal.Integral(1,Sys1Normal.GetNbinsX()+1))) \
      for cMEt in MET_Cuts]

     epsilonDown = [e*eA for e,eA in zip(epsADownOverNormal,epsilon_A_list)]
     epsilonDown_A_list.append(epsilonDown)
     epsilonDown_D_list.append([e*d/a for e,d,a in zip(epsilonDown,epsilon_D_list,epsilon_A_list)])

  else:
   epsAUpOverNormal.append([1. for e in epsilon_A_list])
   epsADownOverNormal.append([1. for e in epsilon_A_list])
   epsilonUp_A_list.append([eA for eA in epsilon_A_list])
   epsilonUp_D_list.append([eD for eD in epsilon_D_list]) 
   epsilonDown_A_list.append([eA for eA in epsilon_A_list])
   epsilonDown_D_list.append([eD for eD in epsilon_D_list]) 

  if UseErsatz:

	Ershist_pass = ErsatzPasses[k]
	Ershist_fail = ErsatzFails[k]
	
  	epsilon_A_data_list = [float(Ershist_pass.Integral(Ershist_pass.FindBin(cMEt), \
		    Ershist_pass.GetNbinsX()+1))/(Ershist_pass.Integral(1,Ershist_pass.GetNbinsX()+1)) \
                   for cMEt in MET_Cuts]
	epsilon_D_data_list = [float(Ershist_fail.Integral(Ershist_fail.FindBin(cMEt), \
		    Ershist_fail.GetNbinsX()+1))/(Ershist_fail.Integral(1,Ershist_fail.GetNbinsX()+1)) \
                   for cMEt in MET_Cuts]

	# Not sure what to do yet for systematics in 2D Ersatz Case:
	"""
	for Sys1Up,Sys1Normal,Sys1Down in zip(SysUp,SysNormal,SysDown):
	epsilonUp_A_data_list.append([e*eA for e,eA in zip(epsAUpOverNormal,epsilon_A_data_list)])
	epsilonUp_D_data_list.append([e*d/a for e,d,a in zip(epsilonUp_A_data_list,epsilon_D_data_list,epsilon_A_data_list)])

	epsilonDown_A_data_list.append([e*eA for e,eA in zip(epsADownOverNormal,epsilon_A_data_list)])
	epsilonDown_D_data_list.append([e*d/a for e,d,a in zip(epsilonDown_A_data_list,epsilon_D_data_list,epsilon_A_data_list)])
	"""
  
  else:

  	epsilon_A_data_list = epsilon_A_list[:]
	epsilon_D_data_list = epsilon_D_list[:]

	epsilonUp_A_data_list = epsilonUp_A_list[:]
	epsilonUp_D_data_list = epsilonUp_D_list[:]

	epsilonDown_A_data_list = epsilonDown_A_list[:]
	epsilonDown_D_data_list = epsilonDown_D_list[:]


  QAlist = [float(QCDhist_pass.Integral(QCDhist_pass.FindBin(cMEt), QCDhist_pass.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]
  QBlist = [float(QCDhist_pass.Integral(1,QCDhist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  QClist = [float(QCDhist_fail.Integral(1,QCDhist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  QDlist = [float(QCDhist_fail.Integral(QCDhist_fail.FindBin(cMEt), QCDhist_fail.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]

  f_A_list = [float(QA)/(QA+QB) for QA,QB in zip(QAlist,QBlist)]
  f_D_list = [float(QD)/(QD+QC) for QD,QC in zip(QDlist,QClist)]
  f_W_list = [float(QA+QB)/(QD+QC+QA+QB) \
             for QA,QB,QD,QC in zip(QAlist,QBlist,QDlist,QClist)]

  EAlist = [float(EWKhist_pass.Integral(EWKhist_pass.FindBin(cMEt), EWKhist_pass.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]
  EBlist = [float(EWKhist_pass.Integral(1,EWKhist_pass.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  EClist = [float(EWKhist_fail.Integral(1,EWKhist_fail.FindBin(cMEt)-1))for cMEt in MET_Cuts]
  EDlist = [float(EWKhist_fail.Integral(EWKhist_fail.FindBin(cMEt), EWKhist_fail.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]

  #No need to add the EWK background to the N since I dont add them to the W MC Signal
  NAlist = [SA + QA for SA,QA in zip(SAlist,QAlist)]
  NBlist = [SB + QB for SB,QB in zip(SBlist,QBlist)]
  NClist = [SC + QC for SC,QC in zip(SClist,QClist)]
  NDlist = [SD + QD for SD,QD in zip(SDlist,QDlist)]
  
  DAlistTot = [float(Dhist_pass.Integral(Dhist_pass.FindBin(cMEt), Dhist_pass.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]
  DBlistTot = [float(Dhist_pass.Integral(1,Dhist_pass.FindBin(cMEt)-1)) \
	    for cMEt in MET_Cuts]
  DClistTot = [float(Dhist_fail.Integral(1,Dhist_fail.FindBin(cMEt)-1)) \
	    for cMEt in MET_Cuts]
  DDlistTot = [float(Dhist_fail.Integral(Dhist_fail.FindBin(cMEt), Dhist_fail.GetNbinsX() +1)) \
	    for cMEt in MET_Cuts]
# -----------------------------------------------------------------------------------------------------//
# -----------------------------------------------------------------------------------------------------//
#  The Calculation of the signal from MC and Data, Also Get the Bias Correction factor and its errors

  S = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eW) \
      for NA,NB,NC,ND,e_A,e_D in \
      zip(NAlist,NBlist,NClist,NDlist,epsilon_A_list,epsilon_D_list)]

  Su = [s[0] for s in S]
  Sd = [s[1] for s in S]

  BiasCorUp = [Strue/s for s in Su]
  BiasCorDn = [Strue/s for s in Sd]
  
  if Use2DAntiSelection:
    biasCorErrs  = [CFunc.BiasCorrStatError(sa,sb,sc,sd,qa,qb,qc,qd,Norm/ASNorm) for \
    		    		      sa,sb,sc,sd,qa,qb,qc,qd  in zip( \
    		    		      SAlist,SBlist,SClist,SDlist,		   
    		    		      QAlist,QBlist,QClist,QDlist)]		
    		    		             
    BiasCorUpE 	 = [b[0] for b in biasCorErrs]
    BiasCorDnE 	 = [b[1] for b in biasCorErrs]  
    
  else :
    BiasCorUpE 	 = [0 for s in Su]
    BiasCorDnE 	 = [0 for s in Sd]  
  
  for i in range(len(SystematicsFile)):
    SSysMax = ([CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eW) \
      for NA,NB,NC,ND,e_A,e_D in \
      zip(NAlist,NBlist,NClist,NDlist,epsilonUp_A_list[i],epsilonUp_D_list[i])])

    SuMax.append([s[0] for s in SSysMax])
    SdMax.append([s[1] for s in SSysMax])

    SSysMin = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eW) \
      for NA,NB,NC,ND,e_A,e_D in \
      zip(NAlist,NBlist,NClist,NDlist,epsilonDown_A_list[i],epsilonDown_D_list[i])]

    SuMin.append([s[0] for s in SSysMin])
    SdMin.append([s[1] for s in SSysMin])
  

# Now apply to Data instead of MC
# Temporary solution to the fact that eW MC != eW Data. Replace with actual tag and probe later --------------------//

  if UseTagAndProbe: 	
  	eWdata  = TagAndProbe_eP[k]
  elif UseErsatz:
	NumPass = float(Ersatshist_pass.Integral(0,Ersatzhist_pass.GetNbinsX()+1))
	Num 	= float(Ersatzhist_fail.Integral(0,Ersatzhist_fail.GetNbinsX()+1) + \
			Ersatzhist_fail.Integral(0,Ersatzhist_fail.GetNbinsX()+1))
	eWdata	= NumPass/Num
  else: eWdata	=	eW

# Remove the Electroweak Background from data... Now we do this as a ratio of N!
# This is know relative to total N but also want to redistribute according to eW
# ie the signal contribtions to AB and CD are different in MC and Data so they also
# should be for the EWK backgroudns, ie scale by eWData/ewMC

  YScale = eWdata/eW
  YFScale= (1-eWdata)/(1-eW)

# The EWK scaler is the one which will start at NData/NMC but will change to Sdata/Smc
  EWKScaler	= [(DAlistTot[0]+ \
		   DBlistTot[0]+ \
		   DClistTot[0]+ \
		   DDlistTot[0]) / \
		  (NAlist[0]+EAlist[0]+ \
		   NBlist[0]+EBlist[0]+ \
		   NClist[0]+EClist[0]+ \
		   NDlist[0]+EDlist[0]) for \
		   cMEt in MET_Cuts] 

  
  
  for i in range(Niterations):

	  OldEWKScaler = EWKScaler[:]
          #print OldEWKScaler
	  DAlist = [D-ES*YScale*e for ES,D,e in zip (EWKScaler,DAlistTot,EAlist)]
	  DBlist = [D-ES*YScale*e for ES,D,e in zip (EWKScaler,DBlistTot,EBlist)]
	  DClist = [D-ES*YFScale*e for ES,D,e in zip (EWKScaler,DClistTot,EClist)]
	  DDlist = [D-ES*YFScale*e for ES,D,e in zip (EWKScaler,DDlistTot,EDlist)]
	  
	  Sdata = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eWdata) \
	      for NA,NB,NC,ND,e_A,e_D in \
	      zip(DAlist,DBlist,DClist,DDlist,epsilon_A_data_list,epsilon_D_data_list)]
	  Sudata = [s[0] for s in Sdata]
	  Sddata = [s[1] for s in Sdata]

	  # With data, also get the Error from eW/del(eW)
	  Serrudata = [s[2] for s in Sdata]
	  Serrddata = [s[3] for s in Sdata]

	  EWKScaler = [(BiasCorUp[cMEt])*(Sudata[cMEt]/Su[cMEt]) \
	  	       for cMEt in range(len(MET_Cuts))]

  EWKScaler = OldEWKScaler[:]
  
  for n in range(len(SystematicsFile)):
    SSysMaxdata = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eWdata) \
      for NA,NB,NC,ND,e_A,e_D in \
      zip(DAlist,DBlist,DClist,DDlist,epsilonUp_A_data_list[n],epsilonUp_D_data_list[n])]

    SuMaxdata.append([s[0] for s in SSysMaxdata])
    SdMaxdata.append([s[1] for s in SSysMaxdata])

    SSysMindata = [CFunc.Signal(NA,NB,NC,ND,e_A,e_D,eWdata) \
      for NA,NB,NC,ND,e_A,e_D in \
      zip(DAlist,DBlist,DClist,DDlist,epsilonDown_A_data_list[n],epsilonDown_D_data_list[n])]

    SuMindata.append([s[0] for s in SSysMindata])
    SdMindata.append([s[1] for s in SSysMindata])
   
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# ----------- Random W trials- Used to calculate Stat Errors -----------------------------------------------------------//

# This is annoying not to have this as a function but at the moment the data is different to MC since we
# have to remove EWK from DATA, but for trials, must vary Poisson around total then remove EWK!
# Will try at some point to write a function which accepts all of these numbers and for each point, writes
# the histogram to the file and spits out the widths and centres.
# Actually, its possibly better to make A signal class with all the errors defined inside and can just get them

  rand = ROOT.TRandom3()
  fitup			= []
  fitdown		= []

  Dfitup 		= []
  Dfitdown		= []

  pullup 		= []
  pulldown 		= []

  FirstOrderErr_Sd 	= []
  FirstOrderDataErr_Sd	= []

  Stats_Out.mkdir(IsoCut+"="+str(Iso_CutsEB[k])+'_'+str(Iso_CutsEE[k]))
  Stats_Out.cd(IsoCut+"="+str(Iso_CutsEB[k])+'_'+str(Iso_CutsEE[k]))

  for j in range(0,len(MET_Cuts)):

    tmpCanv		= 	ROOT.TCanvas('tmpCanv'+str(j),'tmpCanv'+str(j),0,0,800,800)
    upname		=	"hist_deltaSup"+str(Iso_CutsEB[k])+'/'+str(Iso_CutsEE[k])+"_"+str(MET_Cuts[j])
    downname		=	"hist_deltaSdown"+str(Iso_CutsEB[k])+'/'+str(Iso_CutsEE[k])+"_"+str(MET_Cuts[j])

    hist_deltaSup	=	ROOT.TH1F(upname,upname,100,0.9*Su[j],1.3*Su[j])
    hist_deltaSdown	=	ROOT.TH1F(downname,downname,100,0.9*Sd[j],1.3*Sd[j])
    histData_deltaSup	=	ROOT.TH1F(upname+'data',upname+'data',100,0.95*Sudata[j],1.05*Sudata[j])
    histData_deltaSdown	=	ROOT.TH1F(downname+'data',downname+'data',100,0.95*Sddata[j],1.05*Sddata[j])
   
    if GetStatError:
      for i in range(1,10001):
        #statistical trial
        na = rand.Poisson(NAlist[j])
        nb = rand.Poisson(NBlist[j])
        nc = rand.Poisson(NClist[j])
        nd = rand.Poisson(NDlist[j])

        # The actual numbers from DATA (scaled) used for statistical trial

        Dna = rand.Poisson(DAlistTot[j])-YScale*EWKScaler[j]*EAlist[j]
        Dnb = rand.Poisson(DBlistTot[j])-YScale*EWKScaler[j]*EBlist[j]
        Dnc = rand.Poisson(DClistTot[j])-YFScale*EWKScaler[j]*EClist[j]
        Dnd = rand.Poisson(DDlistTot[j])-YFScale*EWKScaler[j]*EDlist[j]

        ea = epsilon_A_list[j]
        ed = epsilon_D_list[j]

        eadata = epsilon_A_data_list[j]
        eddata = epsilon_D_data_list[j]

        S     = CFunc.Signal(na,nb,nc,nd,ea,ed,eW)
        DataS = CFunc.Signal(Dna,Dnb,Dnc,Dnd,eadata,eddata,eWdata)

        if (not str(S[0]) == str(1e400*0)): hist_deltaSup.Fill(S[0])
        if (not str(DataS[0]) == str(1e400*0)):	histData_deltaSup.Fill(BiasCorUp[j]*DataS[0])

        hist_deltaSdown.Fill(S[1])
        histData_deltaSdown.Fill(BiasCorDn[j]*DataS[1])


      hist_deltaSup.Fit("gaus","Q","Q")
      hist_deltaSdown.Fit("gaus","Q","Q")

      histData_deltaSup.Fit("gaus","Q","Q")
      histData_deltaSdown.Fit("gaus","Q","Q")
   
      histData_deltaSup.Write()
      histData_deltaSdown.Write()


      fitup.append(hist_deltaSup.GetFunction("gaus").GetParameter(2))
      fitdown.append(hist_deltaSdown.GetFunction("gaus").GetParameter(2))


      Dfitup.append(histData_deltaSup.GetFunction("gaus").GetParameter(2))
      Dfitdown.append(histData_deltaSdown.GetFunction("gaus").GetParameter(2))

      pullup.append(hist_deltaSup.GetFunction("gaus").GetParameter(1))
      pulldown.append(hist_deltaSdown.GetFunction("gaus").GetParameter(1))

      FirstOrderErr_Sd.append(CFunc.SignalError_N(NAlist[j],NBlist[j],NClist[j],NDlist[j],ea,eW))
      FirstOrderDataErr_Sd.append(CFunc.SignalError_N(DAlist[j],DBlist[j],DClist[j],DDlist[j],eadata,eWdata))
    
    else:
      fitup.append(0)
      fitdown.append(0)
      Dfitup.append(0)
      Dfitdown.append(0)
      pullup.append(0)
      pulldown.append(0)
      FirstOrderErr_Sd.append(0)
      FirstOrderDataErr_Sd.append(0)
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# --------------------------------- Pylab/ROOT PLOTTING ----------------------------------------------------------------//

  if (MakePlots):

    if EBOnly:
      GraphTitle = IsoCut+'(Barrel) ='+str(EBstep*cIsoCutEB)
      TextRegion = str(EBstep*cIsoCutEB)
    elif EEOnly:
      GraphTitle = IsoCut+'(Endcap) ='+str(EEstep*cIsoCutEE)
      TextRegion = str(EEstep*cIsoCutEE)
    else:
      GraphTitle = IsoCut+'='+str(EBstep*cIsoCutEB)+'/'+str(EEstep*cIsoCutEE)
      TextRegion = str(EBstep*cIsoCutEB)+'-'+str(EEstep*cIsoCutEE)

# ------------------------------------------------------------------------------------------------------------------------//
# One plot for each systematic -------------------------------------------------------------------------------------------//
    
    for n in range(len(SystematicsFile)):
       SignalGraph = PyMultiGraphErrs(MET_Cuts,[Su,Sd,[Strue for i in MET_Cuts]], \
                            [SuMin[n],SdMin[n],[0]],[SuMax[n],SdMax[n],[0]], \
                            Title=GraphTitle, \
                            Ylabel="MC - Calculated Signal at "+str(scaleto)+"pb ^{-1}", \
                            Xlabel=PforCalo+" #slash{E}_{T} Cut", \
                  	    lables = ['#varepsilon_{A} != #varepsilon_{D}', \
			             '#varepsilon_{A} = #varepsilon_{D}','MC -Truth'] \
                            )
       SignalGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+\
       			 CaloSectionString+"_Signal_MC"+TextRegion+'sys_'+str(n)+".gif")
       del(SignalGraph)

       SignalDataGraph = PyMultiGraphErrs( MET_Cuts,[Sudata,Sddata], \
                            [SuMindata[n],SdMindata[n]],[SuMaxdata[n],SdMaxdata[n]], \
                            Title = GraphTitle, \
                            Ylabel = "Data - Calculated Signal at "+str(scaleto)+"pb ^{-1}", \
                            Xlabel = PforCalo+" #slash{E}_{T} Cut", \
                  	    lables = ['#varepsilon_{A} != #varepsilon_{D}','#varepsilon_{A} = #varepsilon_{D}'] \
			    )
       SignalDataGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+\
       			     CaloSectionString+"_Signal_Data"+TextRegion+'sys_'+str(n)+".gif")
       del(SignalDataGraph)

   
       SignalDataCorrGraph = PyMultiGraphErrs( MET_Cuts,[[SD*Strue/S for SD,S in zip(Sudata,Su)], \
			    [SD*Strue/S for SD,S in zip(Sddata,Sd)]], \
                            [[SD*Strue/S for SD,S in zip(SuMindata[n],Su)],[SD*Strue/S for SD,S in zip(SdMindata[n],Sd)]], \
                            [[SD*Strue/S for SD,S in zip(SuMaxdata[n],Su)],[SD*Strue/S for SD,S in zip(SdMaxdata[n],Sd)]], \
                            Title = GraphTitle, \
                            Ylabel = "Data - Corrected Signal at "+str(scaleto)+"pb ^{-1}", \
                            Xlabel = PforCalo+" #slash{E}_{T} Cut", \
                  	    lables = ['#varepsilon_{A} != #varepsilon_{D}','#varepsilon_{A} = #varepsilon_{D}'] \
			    )
       SignalDataCorrGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+ \
       				 CaloSectionString+"_Signal_DataCorr_"+TextRegion+'sys_'+str(n)+".gif")
       del(SignalDataCorrGraph)
    # -------------------------------------------------------------------------------------------------------------------//
    # -------------------------------------------------------------------------------------------------------------------//
        
    ErrorGraph = PyMultiGraph(MET_Cuts,[[100.*f/s for f,s in zip (fitup,Su)],[100.*f/s for f,s in zip (fitdown,Sd)], \
                                        [100.*f/s for f,s in zip (FirstOrderErr_Sd,Sd)]], \
                              Title = GraphTitle, \
                              Ylabel = "MC - Error #sigma_{S} %",Xlabel = PforCalo+" #slash{E}_{T} Cut", \
                              )
    ErrorGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_Error_Signal_MC"+TextRegion+".gif")
    del(ErrorGraph)
    

    ErrorDataGraph = PyMultiGraph(MET_Cuts, \
                              [[1.*f for f,s in zip (Dfitup,Sudata)],[1.*f for f,s in zip (Dfitdown,Sddata)], 
                               [1.*f for f,s in zip (FirstOrderDataErr_Sd,Sd)]], \
                              Title = GraphTitle, \
                              Ylabel = "Data -Error #sigma_{S} %",Xlabel = PforCalo+" #slash{E}_{T} Cut")
    ErrorDataGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_Error_Signal_Data"+TextRegion+".gif")
    del(ErrorDataGraph)

    BiasGraph = PyMultiGraph(MET_Cuts, \
                             [[abs(s-Strue)/Strue for s in Su],[abs(s-Strue)/Strue for s in Sd]], \
                             Title = GraphTitle, \
                             Ylabel = "|S-Strue|/ Strue_",Xlabel = PforCalo+" #slash{E}_{T} Cut",)
    BiasGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_s-strue_over_s-true_Bias_"+TextRegion+".eps")
    del(BiasGraph)

    PullGraph = PyMultiGraph(MET_Cuts, \
                             [[p-s for s,p in zip(Su,pullup)],[p-s for s,p in zip(Sd,pulldown)]], \
                             Title = GraphTitle, \
                             Ylabel = "s-Gaus(1)", Xlabel =PforCalo+" #slash{E}_{T} Cut")
    PullGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_s-Gaus1_"+TextRegion+".eps")
    del(PullGraph)

    EpsilonGraph = PyMultiGraph(MET_Cuts,[epsilon_D_list,epsilon_A_list], \
                                Title = GraphTitle, \
                                Ylabel="Epsilon A/D",Xlabel=PforCalo+" #slash{E}_{T} Cut")
    EpsilonGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_Epsilon_AorD_"+TextRegion+".eps")
    del(EpsilonGraph)

    FGraph = PyMultiGraph(MET_Cuts,[f_D_list,f_A_list], \
                          Title = GraphTitle, \
                          Ylabel = "F A/D",Xlabel=PforCalo+" #slash{E}_{T} Cut")
    FGraph.Print(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_F_AorD_"+TextRegion+".eps")
    del(FGraph)

  if MCRescaleToDataN:
    if met in MET_Cuts:
      metpick = MET_Cuts.index(met)
      print "\nHistograms (QCD/Wenu) scaled to Signal/QCD as from data @MetCut %.1f: \
	     \nUsing Signal = %.1f" %(MET_Cuts[metpick],(BiasCorUp[metpick])*Sudata[metpick])
    else : 
      print 'Choice of MET for rescale not in range, default to central Cut %.1f GeV' %MET_Cuts[-1]
      metpick = -1
# ----------------------------------------------------------------------------------------------------------------------//

    YScale 	= eWdata/eW
    YFScale	= (1-eWdata)/(1-eW)

    BiasCorr	=  Su[metpick]/Strue

    PassScaler	= BiasCorr*(Sudata[metpick]*eWdata)/(Strue*eW)
    FailScaler	= BiasCorr*Sudata[metpick]*(1-eWdata)/(Strue*(1-eW))
    print "Wenu MC A+B scaled by: ",BiasCorr*(Sudata[metpick]*eWdata)/(Strue*eW)
    print "Wenu MC C+D scaled by: ",BiasCorr*Sudata[metpick]*(1-eWdata)/(Strue*(1-eW))
    QCDPassScaler = (DAlist[metpick]+DBlist[metpick]) - BiasCorr*Sudata[metpick]*eWdata
    QCDFailScaler = (DClist[metpick]+DDlist[metpick]) - BiasCorr*Sudata[metpick]*(1-eWdata)
    print "QCD MC A+B scaled by: ",QCDPassScaler/QCDhist_pass.Integral(1,QCDhist_pass.GetNbinsX()+1)
    print "QCD MC C+D scaled by: ",QCDFailScaler/QCDhist_fail.Integral(1,QCDhist_fail.GetNbinsX()+1)

    Whist_pass.Scale(PassScaler)
    Whist_fail.Scale(FailScaler)

    QCDhist_pass.Scale(QCDPassScaler/QCDhist_pass.Integral(1,QCDhist_pass.GetNbinsX()+1))
    QCDhist_fail.Scale(QCDFailScaler/QCDhist_fail.Integral(1,QCDhist_fail.GetNbinsX()+1))

    # Now we scale EWK so that the fraction of it is the same as before Remeber Y Scale
  
    EWKhist_pass.Scale(YScale*EWKScaler[metpick])
    EWKhist_fail.Scale(YFScale*EWKScaler[metpick])
    
 
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Histogram Plotting 

print "W MC True Signal = ", Strue

c = ROOT.TCanvas("c","c",0,0,2400,len(Iso_Cuts)*900)
c.Divide(2,len(WFails),0.0005,0.0005)

for i,Whist_pass,Whist_fail,QCDhist_pass,QCDhist_fail, \
     EWK_pass,EWK_fail, Dhist_pass,Dhist_fail \
    in zip(range(1,len(WFails)+1),WPasses,WFails,QCDPasses,QCDFails, \
     EWKPasses,EWKFails, DataPasses,DataFails):

  j = 2*i
  c.cd(2*i-1)
  
  Total_pass = Whist_pass.Clone()
  Total_fail = Whist_fail.Clone()

  Total_pass.Add(QCDhist_pass)
  Total_pass.Add(EWK_pass)
  Total_fail.Add(QCDhist_fail)
  Total_fail.Add(EWK_fail)

  Total_pass.SetLineWidth(3)
  Total_fail.SetLineWidth(3)
 
  Whist_pass.SetFillColor(ROOT.kBlue-6)
  Whist_pass.SetLineColor(ROOT.kBlue-6)
  Whist_pass.SetFillStyle(1001)
  Whist_fail.SetFillColor(ROOT.kBlue-6)
  Whist_fail.SetLineColor(ROOT.kBlue-6)
  Whist_fail.SetFillStyle(1001)
  
  QCDhist_pass.SetFillColor(ROOT.kTeal+9)
  QCDhist_pass.SetFillStyle(3001)
  QCDhist_pass.SetLineColor(ROOT.kTeal+9)
  QCDhist_fail.SetFillColor(ROOT.kTeal+9)
  QCDhist_fail.SetFillStyle(3001)
  QCDhist_fail.SetLineColor(ROOT.kTeal+9)
  
  EWKhist_pass.SetFillColor(ROOT.kYellow-4)
  EWKhist_pass.SetFillStyle(3001)
  EWKhist_pass.SetLineColor(ROOT.kYellow-4)
  EWKhist_fail.SetFillColor(ROOT.kYellow-4)
  EWKhist_fail.SetFillStyle(3001)
  EWKhist_fail.SetLineColor(ROOT.kYellow-4)

  """
  Whist_pass.SetFillColor(41)
  Whist_pass.SetLineColor(41)
  Whist_pass.SetFillStyle(5001)
  Whist_fail.SetFillColor(41)
  Whist_fail.SetLineColor(41)
  Whist_fail.SetFillStyle(5001)

  QCDhist_pass.SetFillColor(35)
  QCDhist_pass.SetFillStyle(3001)
  QCDhist_pass.SetLineColor(35)
  QCDhist_fail.SetFillColor(35)
  QCDhist_fail.SetFillStyle(3001)
  QCDhist_fail.SetLineColor(35)

  EWKhist_pass.SetFillColor(30)
  EWKhist_pass.SetFillStyle(3001)
  EWKhist_pass.SetLineColor(30)
  EWKhist_fail.SetFillColor(30)
  EWKhist_fail.SetFillStyle(3001)
  EWKhist_fail.SetLineColor(30)
  """
  
  Dhist_pass.SetMarkerStyle(8)
  Dhist_pass.SetMarkerSize(0.5)
  Dhist_pass.SetMarkerColor(1)
  Dhist_fail.SetMarkerStyle(8)
  Dhist_fail.SetMarkerSize(0.5)
  Dhist_fail.SetMarkerColor(1)
  
  
  if UseErsatz:
	
	Ersatzhist_pass = ErsatzPasses[i-1]
	Ersatzhist_pass.SetMarkerStyle(22)
	Ersatzhist_pass.SetMarkerSize(0.5)
	Ersatzhist_pass.SetMarkerColor(2)
	Ersatzhist_pass.Scale(Whist_pass.Integral(1,Whist_pass.GetNbinsX()+1) \
			      /Ersatzhist_pass.Integral(1,Ersatzhisthist_pass.GetNbinsX()+1))

	Ersatzhist_fail = ErsatzFails[i-1]
	Ersatzhist_fail.SetMarkerStyle(22)
	Ersatzhist_fail.SetMarkerSize(0.5)
	Ersatzhist_fail.SetMarkerColor(2)
	Ersatzhist_fail.Scale(Whist_fail.Integral(1,Whist_fail.GetNbinsX()+1) \
			      /Ersatzhist_fail.Integral(1,Ersatzhist_fail.GetNbinsX()+1))

  if EBOnly:
    Titlestr = 'Pass'+IsoCut+"(Barrel) = "+str(EBstep*Iso_CutsEB[i-1])
  elif EEOnly:
    Titlestr = 'Pass'+IsoCut+"(EndCap) = "+str(EEstep*Iso_CutsEE[i-1])
  else:
    Titlestr = 'Pass'+IsoCut+" = "+str(EBstep*Iso_CutsEB[i-1])+'/'+str(EEstep*Iso_CutsEE[i-1])
 
  
  """
  # Adding the pass and fails together, Remove this very soon!
  ######################################################################################
  Dhist_pass.Add(Dhist_fail)
  EWKhist_pass.Add(EWKhist_fail)
  Whist_pass.Add(Whist_fail)
  QCDhist_pass.Add(QCDhist_fail)
  Total_pass.Add(Total_fail)
  print "I added the hists on the LEFT panel, remove this soon!!! "
  """
  

  Dhist_pass.SetTitle(Titlestr)

  leg1 = ROOT.TLegend(0.5,0.6,0.8,0.8)
  leg1.SetFillColor(0)
  leg1.AddEntry(Whist_pass, "W #rightarrow e #nu","F")
  leg1.AddEntry(QCDhist_pass,"QCD","F")
  leg1.AddEntry(EWK_pass,"EWK","F")
  leg1.AddEntry(Dhist_pass,"Data","P")
  if UseErsatz:	leg1.AddEntry(Ersatzhist_pass,'Ersatz','P')

  Dhist_pass.GetYaxis().SetTitle("Number of events at "+str(scaleto)+" pb^{ -1}")
  Dhist_pass.Draw()
  Total_pass.Draw("histsame")
  Whist_pass.Draw("histsame")
  QCDhist_pass.Draw("histsame")
  EWKhist_pass.Draw("histsame")
  Dhist_pass.Draw("same")
  if UseErsatz: Ersatzhist_pass.Draw('sameP')
  leg1.Draw()

  c.cd(j)

  if EBOnly: 
    Titlestr2 = 'Fail'+IsoCut+"(Barrel) = "+str(EBstep*Iso_CutsEB[i-1])
  elif EEOnly:
    Titlestr2 = 'Fail'+IsoCut+"(Endcap) = "+str(EEstep*Iso_CutsEE[i-1])
  else:
    Titlestr2 = 'Fail'+IsoCut+" = "+str(EBstep*Iso_CutsEB[i-1])+'/'+str(EEstep*Iso_CutsEE[i-1])
  
  Dhist_fail.SetTitle(Titlestr2)

  leg2 = ROOT.TLegend(0.5,0.6,0.8,0.8)
  leg2.SetFillColor(0)
  leg2.AddEntry(Whist_fail, "W #rightarrow e #nu","F")
  leg2.AddEntry(QCDhist_fail,"QCD","F")
  leg2.AddEntry(EWKhist_fail, "EWK","F")
  leg2.AddEntry(Dhist_fail,"Data","P")
  if UseErsatz:	leg2.AddEntry(Ersatzhist_fail,'Ersatz','P')

  
  Dhist_fail.GetYaxis().SetTitle("Number of events at "+str(scaleto)+" pb^{-1}")
  Dhist_fail.Draw()
  Total_fail.Draw("histsame")
  Whist_fail.Draw("histsame")
  QCDhist_fail.Draw("histsame")
  EWK_fail.Draw("histsame")
  Dhist_fail.Draw("same")
  if UseErsatz:	Ersatzhist_fail.Draw('sameP')
  leg2.Draw()

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Text File containing useful information, including cross-section calculation from the data 

  if UseTagAndProbe: 
  	ewdata = TagAndProbe_eP[i-1]
  	eWerr  = TagAndProbe_epERR[i-1]
  elif UseErsatz:
	NumPass = float(Ersatshist_pass.Integral(0,Ersatzhist_pass.GetNbinsX()+1))
	Num 	= float(Ersatzhist_fail.Integral(0,Ersatzhist_fail.GetNbinsX()+1) + \
			Ersatzhist_fail.Integral(0,Ersatzhist_fail.GetNbinsX()+1))
	eWdata	= NumPass/Num
	eWerr	= CFunc.FracError(NumPass,Num)
  else: 
  	ewdata = eW
  	eWerr  = 0
  	
  if UseDataDetectorParams: eff = 1000*Efficiency*Acceptance*scaleto
  else:	eff = 1000.0*(Strue/(TotalN))*scaleto
	
  if (TextOut):
    if EBOnly	:	TextIso = str(EBstep*Iso_CutsEB[i-1])
    elif EEOnly	:	TextIso = str(EEstep*Iso_CutsEE[i-1])
    else	:	TextIso = str(EBstep*Iso_CutsEB[i-1])+'-'+str(EEstep*Iso_CutsEE[i-1])
    TextOutFile = open(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString \
    		       +"_Numbers"+TextIso+'.txt','w')
    		       
    print "Results Being Printed in: ", \
	   plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+ \
	  "_Numbers"+TextIso+'.txt'

    # ------------------------------------------------------------------------------------------//
    # Some Headers for the Reults File ---------------------------------------------------------//
    TextOutFile.write("Results from ABCDE Method at %.3f\n" %LuminosityOfData)
    TextOutFile.write("2D Plane defined Using X = %s, Y = %s at %s\n" %(PforCalo,IsoCut,TextIso))
    if EBOnly: TextOutFile.write("Only Used Barrel Events\n")
    if EEOnly: TextOutFile.write("Only Used EndCap Events\n")
    if PlusOrMinus != ''  : TextOutFile.write("Only using electrons with charge: %s\n" %PlusOrMinus)
    if CorrectTheMCSignal : TextOutFile.write("Used Corrected Signal Template\n")
    if CorrectTheMCQCD    : TextOutFile.write("Used Corrected QCD Template\n")
    if Use2DAntiSelection : TextOutFile.write("Used AntiSelected QCD Template from Data\n")
    TextOutFile.write('\n')
    # ------------------------------------------------------------------------------------------//
    # ------------------------------------------------------------------------------------------//
       
    # Shouldve changed all later references to eW not ew, quick fix
    ew = eW

    for m,cut,ssa,ssb,ssc,ssd, \
        qa,qb,qc,qd,ewka, \
	ewkb,ewkc,ewkd,da,db, \
	dc,dd,su,sd,ea, \
	ed, \
        eadata,eddata,fa,fd,fup,fdown, \
	Dfup,Dfdown,dup,ddown,serrudata,serrddata \
        in zip( range(len(MET_Cuts)),
	MET_Cuts,SAlist,SBlist,SClist,SDlist, \
	QAlist,QBlist,QClist,QDlist,EAlist, \
	EBlist,EClist,EDlist,DAlistTot,DBlistTot, \
	DClistTot,DDlistTot,Su,Sd,epsilon_A_list, \
	epsilon_D_list, \
        epsilon_A_data_list,epsilon_D_data_list,f_A_list,f_D_list,fitup,fitdown, \
	Dfitup,Dfitdown,Sudata,Sddata,Serrudata,Serrddata \
	):
	
      Bcu = BiasCorUp[m]
      Bcd = BiasCorDn[m]
      BcuE = BiasCorUpE[m]
      BcdE = BiasCorDnE[m]

      TextOutFile.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

      TextOutFile.write("\nIsoLation"+PforCalo+IsoCut+"Isolation Cut EB/EE = "+ \
                        str(EBstep*Iso_CutsEB[i-1]) + '/' + \
                        str(EEstep*Iso_CutsEE[i-1]) +'\n')

      TextOutFile.write("Met Cut = " +str(cut)+'\n')
      TextOutFile.write("EfficiencyxAcc = 			%.3f \n" % (Strue/(TotalN)))
      TextOutFile.write("Data EfficiencyxAcc =			%.3f \n" % (eff/(scaleto*1000)))
      TextOutFile.write("BarrelEfficiencyxAcceptance =		%.3f \n" % (SBarrel/(TotalN)) )
      TextOutFile.write("EndCapEfficiencyxAcceptance =		%.3f \n" % (SEndCap/(TotalN)) )
      TextOutFile.write("Qa = 					%.3f \n" % (qa))
      TextOutFile.write("Qb = 					%.3f \n" % (qb))
      TextOutFile.write("Qc = 					%.3f \n" % (qc))
      TextOutFile.write("Qd = 					%.3f \n" % (qd))
      TextOutFile.write("Q  = 					%.3f \n" % (qa+qb+qc+qd))
      TextOutFile.write("Uncorrected Na = 			%.3f \n" % (qa+ssa+ewka))
      TextOutFile.write("Uncorrected Nb = 			%.3f \n" % (qb+ssb+ewkb))
      TextOutFile.write("Uncorrected Nc = 			%.3f \n" % (qc+ssc+ewkc))
      TextOutFile.write("Uncorrected Nd = 			%.3f \n" % (qd+ssd+ewkd))

      TextOutFile.write("Uncorrected Na (From Data) = 		%.3f \n" % (da))
      TextOutFile.write("Uncorrected Nb (From Data) = 		%.3f \n" % (db))
      TextOutFile.write("Uncorrected Nc (From Data) = 		%.3f \n" % (dc))
      TextOutFile.write("Uncorrected Nd (From Data) = 		%.3f \n" % (dd))
      TextOutFile.write("Total N (from Data) =			%.3f \n" % (da+db+dc+dd))

      TextOutFile.write("Sa (true/estimate/estimate(eA=eD))= 	%.3f / %.3f / %.3f \n" %(ssa, (su*ew*ea), (sd*ew*ea)))
      TextOutFile.write("Sb (true/estimate/estimate(eA=eD))= 	%.3f / %.3f / %.3f \n" %(ssb, (su*ew*(1-ea)), (sd*ew*(1-ea))))
      TextOutFile.write("Sc (true/estimate/estimate(eA=eD))= 	%.3f / %.3f / %.3f \n" \
                                                                %(ssc,(su*(1-ew)*(1-ed)),(sd*(1-ew)*(1-ea))))
      TextOutFile.write("Sd (true/estimate/estimate(eA=eD))= 	%.3f / %.3f / %.3f \n" \
      								%(ssd,(su*(1-ew)*(ed)),(sd*(1-ew)*(ea))))
      
      TextOutFile.write("EWKa/Lumi = 				%.3f \n" %(ewka/scaleto))
      TextOutFile.write("EWKb/Lumi = 				%.3f \n" %(ewkb/scaleto))
      TextOutFile.write("EWKc/Lumi = 				%.3f \n" %(ewkc/scaleto))
      TextOutFile.write("EWKd/Lumi = 				%.3f \n" %(ewkd/scaleto))

      TextOutFile.write("EWKAoverNA = 				%.3f \n" %(ewka/(qa+ewka+ssa)))
      TextOutFile.write("EWKBoverNB = 				%.3f \n" %(ewkb/(qb+ewkb+ssb)))
      TextOutFile.write("EWKCoverNC = 				%.3f \n" %(ewkc/(qc+ewkc+ssc)))
      TextOutFile.write("EWKDoverND = 				%.3f \n" %(ewkd/(qd+ewkd+ssd)))

      TextOutFile.write("MC epsilonA = 				%.3f \n" %(ea))
      TextOutFile.write("MC epsilonD = 				%.3f \n" %(ed))
      TextOutFile.write("MC epsilonP = 				%.3f \n" %(ew))

      TextOutFile.write("Data epsilonA = 			%.3f \n" %(eadata))
      TextOutFile.write("Data epsilonD = 			%.3f \n" %(eddata))
      TextOutFile.write("Data epsilonP = 			%.3f +/- %.3f(stat)\n" \
      								         %(ewdata,eWerr))
      
      TextOutFile.write("fA = 					%.3f \n" %(fa))
      TextOutFile.write("fD = 					%.3f \n" %(fd))

      TextOutFile.write("Results Assuming eA!=eD \n ---------------------------------------------------------------//\n")
      TextOutFile.write("Sa (true/Data) = 			%.3f / %.3f \n" %((ssa), (su*ewdata*ea)))
      TextOutFile.write("Sb (true/Data) = 			%.3f / %.3f \n" %((ssb), (su*ewdata*(1-ea))))
      TextOutFile.write("Sc (true/Data) = 			%.3f / %.3f \n" %((ssc), (su*(1-ewdata)*(1-ed))))
      TextOutFile.write("Sd (true/Data) = 			%.3f / %.3f \n" %((ssd), (su*(1-ewdata)*(ed))))
      TextOutFile.write("Signal =  				%.3f \n     +/- %5.3f (stat) \n"  %(su,fup))
      TextOutFile.write("ABCDE Bias	=			%.4f \n" %((su-Strue)/su))
      TextOutFile.write("Bias Corection = 			%.5f +/- %.5f\n" %(Bcu,BcuE))
      TextOutFile.write("Signal from Data (BiasCorr) = 		%.3f \n     +/- %5.3f (stat) \n \
      +/- %5.5f (bias stat)\n"					%(Bcu*dup,Dfup,BcuE*dup))      			           
      for n in range(len(SystematicsFile)) :
      	TextOutFile.write(	"  +%5.3f +%5.3f  (sys)\n"	%(Bcu*(SuMaxdata[n][m]-dup),\
      							    	  Bcu*(SuMindata[n][m]-dup)))
      							    		  
      if UseDataDetectorParams: TextOutFile.write(" +/- 	%5.3f (from eP err)\n" % (eWerr*serrudata))
      TextOutFile.write("K factor in Data	      =		%.3f\n" %(serrudata*ewdata/dup))
      TextOutFile.write('Cross-Section from Data (nb) = 	%.3f \n     +/- %5.3f (stat) \n \
      +/- %5.5f (bias stat)\n' 					%(Bcu*(dup/eff),(Dfup/eff),BcuE*(dup/eff)))
     
      for n in range(len(SystematicsFile)) :
      	TextOutFile.write(	"  +%5.3f +%5.3f (sys)\n"	%(Bcu*(SuMaxdata[n][m]-dup)/eff,\
      							          Bcu*(SuMindata[n][m]-dup)/eff))                
     
      if UseDataDetectorParams: TextOutFile.write(" +/- 	%5.3f (from eP err)\n" % (eWerr*serrudata/eff))
      
      TextOutFile.write("Results Assuming eA=eD \n ----------------------------------------------------------------//\n")
      TextOutFile.write("Sa (true/Data) = 			%.3f / %.3f \n" %(ssa,(sd*ew*ea),))
      TextOutFile.write("Sb (true/Data) = 			%.3f / %.3f \n" %(ssb,(sd*ew*(1-ea))))
      TextOutFile.write("Sc (true/Data) = 			%.3f / %.3f \n" %(ssc,sd*(1-ew)*(1-ea)))
      TextOutFile.write("Sd (true/Data) =			%.3f / %.3f \n" %(ssd,sd*(1-ew)*(ea)))
      TextOutFile.write("Signal (eA=eD) = 			%.3f \n     +/- %5.3f (stat) \n"  %(sd,fdown))
      TextOutFile.write("ABCDE Bias	=			%.3f \n" %((sd-Strue)/sd))
      TextOutFile.write("Bias Corection = 			%.5f +/- %.5f\n" %(Bcd,BcdE))
      TextOutFile.write("Signal from Data (BiasCorr) = 		%.3f \n     +/- %5.3f (stat) \n \
      +/- %5.5f (bias stat)"				        %(Bcd*ddown,Dfdown,BcdE*ddown))
      for n in range(len(SystematicsFile)) :
      	TextOutFile.write(	"  +%5.3f +%5.3f (sys)\n" 	%(Bcd*(SdMaxdata[n][m]-ddown),\
      							    	  Bcd*(SdMindata[n][m]-ddown)))
      							     
      if UseDataDetectorParams: TextOutFile.write(" +/- 	%5.3f (from eP err)\n" % (eWerr*serrddata))
      TextOutFile.write("K factor in Data	      =		%.3f\n" %(serrddata*ewdata/ddown))
      TextOutFile.write("Cross-Section from Data (nb) = 	%.4f \n     +/- %5.3f (stat) \n \
      +/- %5.5f (bias stat)" 					%(Bcd*(ddown/eff),(Dfdown/eff),BcdE*(ddown/eff)))
     
      for n in range(len(SystematicsFile)) :
      	TextOutFile.write(	"  +%5.3f +%5.3f (sys)\n"	%(Bcd*(SdMaxdata[n][m]-ddown)/eff,\
      							    	  Bcd*(SdMindata[n][m]-ddown)/eff))    
      if UseDataDetectorParams: TextOutFile.write(" +/- 	%5.3f (from eP err)\n" % (eWerr*serrddata/eff))
      
      TextOutFile.write("MC Truth Signal = 			%.3f\n" % Strue)
      TextOutFile.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
      TextOutFile.write("\n")
      
ROOT.gStyle.SetOptStat(0)
c.SaveAs(plottingdir+PforCalo+IsoCut+PlusOrMinus+CaloSectionString+"_Met.gif")

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Close the files :

Stats_Out.Close()

for W in WenuFileList:	W.Close()
for Q in QCDFileList:	Q.Close()
for E in EWKFileList:	E.Close()

DataFile.Close()

if Use2DAntiSelection: QCDAntiSelection2D.Close()
if not len(SystematicsFile) == 0: 
  for sys in SysFiles: sys.Close()

if UseErsatz:
  ErsatzFile.Close()
  NuAccCorrFile.Close()

if TextOut: TextOutFile.close()
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# END

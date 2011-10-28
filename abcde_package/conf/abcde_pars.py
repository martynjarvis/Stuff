# abcde_pars
# Nicholas Wardle - Imperial College

# Configuration for the ABCDE method

#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//  
class Parameters:

	ResultsFolder_		=	'results'

	WenuFiles_		=	['templates/ResultsWENU_VBTFpreselection_wenuPlus.root',
					 'templates/ResultsWENU_VBTFpreselection_wenuMinus.root']
	WenuNumbers_		=	[1997953,
					 1996734]
	WenuLumis_		=	[345.966,
					 506.271]

	#EMEnrichedSF		=	1.0
	EMEnrichedSF		=	1.516
	
	QCDFiles_		=	['templates/ResultsWENU_VBTFpreselection_qcdEm_20-30.root',
					 'templates/ResultsWENU_VBTFpreselection_qcdEm_30-80.root',
					 'templates/ResultsWENU_VBTFpreselection_qcdEm_80-170.root',
					 'templates/ResultsWENU_VBTFpreselection_qcdBce20-30.root',
					 'templates/ResultsWENU_VBTFpreselection_qcdBce30-80.root',
					 'templates/ResultsWENU_VBTFpreselection_qcdBce80-170.root',
					 'templates/ResultsWENU_VBTFpreselection_gj15-30.root',
					 'templates/ResultsWENU_VBTFpreselection_gj30-50.root',
					 'templates/ResultsWENU_VBTFpreselection_gj50-80.root',
					 'templates/ResultsWENU_VBTFpreselection_gj80-120.root',
					 'templates/ResultsWENU_VBTFpreselection_gj120-170.root'
					]
					
	QCDLumiScale_		=	1.0
	QCDLumis_		=	[QCDLumiScale_*14.900/EMEnrichedSF,
					 QCDLumiScale_*17.810/EMEnrichedSF,
					 QCDLumiScale_*57.875/EMEnrichedSF, 
					 QCDLumiScale_*16.975,
					 QCDLumiScale_*14.587,
					 QCDLumiScale_*111.473, 
					 QCDLumiScale_*5.392,
					 QCDLumiScale_*61.443,
					 QCDLumiScale_*369.628,
					 QCDLumiScale_*2343.951,
					 QCDLumiScale_*12158.263
					]
	
	EWKFiles_		=	['templates/ResultsWENU_VBTFpreselection_wtaunu.root',
					 'templates/ResultsWENU_VBTFpreselection_dyee.root',
					 'templates/ResultsWENU_VBTFpreselection_dytautau.root',
					 'templates/ResultsWENU_VBTFpreselection_ttbar.root',
					 'templates/ResultsWENU_VBTFpreselection_ww.root',
					 'templates/ResultsWENU_VBTFpreselection_wz.root',
					 'templates/ResultsWENU_VBTFpreselection_zz.root',
					 'templates/ResultsWENU_VBTFpreselection_wmunuPlus.root',
					 'templates/ResultsWENU_VBTFpreselection_wmunuMinus.root',
					]
					
	EWKLumiScale_		=	1.0

	EWKLumis_		=	[EWKLumiScale_*537.272,
					 EWKLumiScale_*1238.53,
					 EWKLumiScale_*1176.095,
					 EWKLumiScale_*10633.511,
					 EWKLumiScale_*74190.716,
					 EWKLumiScale_*211033.846,
					 EWKLumiScale_*493892.966,
					 EWKLumiScale_*345.966,
					 EWKLumiScale_*519.442,
					]

	DataFile_		=	'templates/DataResults25.root'
	LuminosityOfData_	= 	34.3

	GetStatError_		=	False
	#SystematicsFile_	= 	''
	SystematicsFile_	=	['templates/2DDigausWpfmet25_zrecoil_v54.root']
	SysHistHigh_		=	['hmet']
	SysHistNorm_		=	['mmet']
	SysHistLow_		=	['lmet']

	METType_		=	'Pf'
	METCuts_		=	[22,34]

	IDType_			=	'TrckRelIso'
	Iso_CutsEB_		=	[3]		
	Iso_CutsEE_		=	[6]

	UseDataDetectorParams_	=	True


	EffPrime_		=	1.#0.987	#Correction for non standard WP
	Efficiency_		=	0.857*0.917/EffPrime_
	Acceptance_		=	0.498816
	
	# Use 2D erstaz Template (Only useful for High luminosities)
	UseErsatz_		=	False	
	ErsatzFile_		=	'templates/ErsatzResults.root'
	NuAccCorrFile_		=	'templates/NeutrinoAcceptanceCorrection.root'
	UseTagAndProbe_		=	True

	ScaleTo_		= 	34.3
	PlusOrMinus_		=	''    # choose from '', 'Plus' and 'Minus'
	EBOnly_			=	False
	EEOnly_			=	False
	MakePlots_		=	True
	TextOut_		=	True

	Use2DAntiSelection_	=	True
	QCDAntiSelection2DFile_ =	'templates/AntiSelection25_sel80_NoCR.root'

	CorrectTheMCQCD_	=	False
	QCDCorrectionFile_	=	'templates/data_25Oct_histos.root'
	QCDCorrectionHisto_	=	'h_pfMET_WP80_antiDhiDfi90'

	CorrectTheMCSignal_	=	True
	SignalCorrectionFile_	=	'templates/2DDigausWpfmet25_zrecoil_v54.root'
	SignalCorrectionHisto_	=	'mmet'

 	RsEWK_			=	False
	RsRes_			=	0.6
  	RsIndex_		=	0	
	
	MCRescaleToDataN_	=	True
	MetPick_		=	28
	
	IterateABCDE_		=	True
	Niterations_		=	5
	
	# Options for 2D ABCDEOptimize.py
	# These two should be ranges
	XRange_			=	[15,38]
	YRange_			=	[1,10]
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------// 


# -*- coding: utf-8 -*-
# wenuanalyser_conf.py
# Nicholas Wardle - Imperial College
# Configuration file for use with WenuAnalyser.py

# --------------------------------------------------------------------------//
<<<<<<< analyser_conf.py
#nTupleDir_	 = '/vols/cms01/nw709/VBTFNtuples/Nov4ReReco/'
#nTupleDir_	 = '/vols/cms02/nw709/VBTFNtuples/dec22ReReco/'
nTupleDir_	 = '/vols/cms01/nw709/VBTFNtuples/'
=======
#nTupleDir_	 = '/vols/cms01/nw709/VBTFNtuples/Nov4ReReco/'
nTupleDir_	 = '/vols/cms01/nw709/VBTFNtuples/'
#nTupleDir_	 = '/vols/cms01/nw709/VBTFNtuples/full_data/'
>>>>>>> 1.4

#''dcap://gfe02.grid.hep.ph.ic.ac.uk:22128//pnfs/hep.ph.ic.ac.uk/data/cms/store/user/mjarvis/VBTF/'#castor/cern.ch/user/n/nckw/WENU/Ntuples/Fall10MC/'	# Where the ntuples are
cElecPtMin_ 	 = 25.		# The minimum SuperCluster Et 
nmetbins_	 = 100
nisobins_	 = 20
WPchoices_	 = ['80']

# --------------------------------------------------------------------------//
# WenuAnalyser.py configurables --------------------------------------------//

TagSelection_ 	 = '80TrckZero'
#TagSelection_ 	 = '80TrckRelIso'
TNPCorrFile_ 	 = 'templates/TagAndProbeCorrections.root'
MassMin_ 	 = 71.
MassMax_ 	 = 121.
ZeeFileName_ 	 = 'templates/ResultsWENU_VBTFpreselection_dyee.root'
WPlusFileName_ 	 = 'templates/ResultsWENU_VBTFpreselection_wenuPlus.root'
WMinusFileName_  = 'templates/ResultsWENU_VBTFpreselection_wenuMinus.root'
PlusLumi_	 = 345.966
MinusLumi_	 = 506.271
WMass_		 = 80.398
ZMass_		 = 90.188
# --------------------------------------------------------------------------//
# QCDAnalyser.py configurables ---------------------------------------------//

QCDSelection_ 	 = '80'
as_cEB_dEtaIn_ 	 = 0.007 
as_cEB_dPhiIn_ 	 = 0.06
as_cEE_dEtaIn_ 	 = 0.009
as_cEE_dPhiIn_ 	 = 0.04

# --------------------------------------------------------------------------//
# --------------------------------------------------------------------------//


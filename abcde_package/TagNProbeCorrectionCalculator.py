# TagAndProbeCorrector.py
# Nicholas Wardle

# Take in histograms from the WenuPlus and WenuMinus and Zee TnP, Produce
# A file to be read in at weights for TnP based on Eta,Pt and charge

import ROOT,os,sys
from conf.analyser_conf import *
# Change the filenames here. Should be a W+/W- and Zee MC file produced by The WenuAnalyser.py

# -------------------------------------------------------------------------------------------------//
# -------------------------------------------------------------------------------------------------//
# Try Getting the files	---------------------------------------------------------------------------//

if os.path.isfile(ZeeFileName_):
	print "Taking Probes from ", ZeeFileName_
	tnpFile  = ROOT.TFile(ZeeFileName_) 
else: sys.exit("No Z -> ee File found named %s" %ZeeFileName_)
if os.path.isfile(WPlusFileName_):
	print "Taking Positrons from ", WPlusFileName_
	WenuPlusFile  = ROOT.TFile(WPlusFileName_) 
else: sys.exit("No W+ -> enu File found named %s" %WPlusFileName_)
if os.path.isfile(WMinusFileName_):
	print "Taking Electrons from ", WMinusFileName_
	WenuMinusFile  = ROOT.TFile(WMinusFileName_) 
else: print sys.exit("No W- -> enu File found named %s" %WMinusFileName_)
# -------------------------------------------------------------------------------------------------//
# -------------------------------------------------------------------------------------------------//

# Use the Z file as the Template for the available Selections, Note It is assumed that the same exist
# In all 3 files
Dirs 	   = tnpFile.GetListOfKeys()
Selections = [d.GetName() for d in Dirs]
# Now we have the names as strings:
# -------------------------------------------------------------------------------------------------//
CorrectionList = []

for S in Selections:

	print "Found Selection", S
	# Get The MC dists
	h_Wp = WenuPlusFile.Get(S+'/aux/'+S[4:]+'ElectronPTVsEta')
	h_Wp.Scale(1./PlusLumi_)
	h_Wm = WenuMinusFile.Get(S+'/aux/'+S[4:]+'ElectronPTVsEta')
	h_Wm.Scale(1./MinusLumi_)
	h_Wp.Add(h_Wm)
	h_Wp.Scale(1./h_Wp.Integral())
	# And get the TnP from the Zee	
	h_Z = tnpFile.Get(S+'/aux/'+S[4:]+'ProbePTVsEta')
	h_Z.Scale(1./h_Z.Integral())
	# And divide for re-weighting factor:
	h_Wp.Divide(h_Z)
	h_Wp.SetName(S[4:]+'Corr')
	
	CorrectionList.append(h_Wp)
# -------------------------------------------------------------------------------------------------//	
print "Recreating Correction File:", TNPCorrFile_ 
OutFile = ROOT.TFile(TNPCorrFile_,'RECREATE')

for C in CorrectionList: C.Write()
OutFile.Close()
# -------------------------------------------------------------------------------------------------//
# -------------------------------------------------------------------------------------------------//	
# END

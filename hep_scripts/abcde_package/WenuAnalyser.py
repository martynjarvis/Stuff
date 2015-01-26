#!/usr/bin/python
# -*- coding: utf-8 -*-

# WenuAnalyser.py
# Nicholas Wardle - Imperial College
# This Analyser Produces the necessary Data/MC ROOT files for ABCDEOptimize.py
# Run As python WenuAnalyser filename (assuming they are in ntuples/)
#			     nmetbins_ (eg 25)
#			     nisobins_ (eg 10)
#			     WorkingPoint (70/85/80/90/95/SC etc...)
#		option       -doTnP		# Makes Tag and probe histograms
#		option	     -doCor    		# Reads in and applies reweight for tag and probe
#		option	     -doTrig=int	# applies trigger cut, & with int
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Standard Imports
import ROOT
import os,sys,getopt,array
import math
import bisect
#from eventlist38 import b_38
#from eventlist39 import b_39
## ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Import from package
from conf.classes import *
from conf.analyser_conf import *


# ----------------------------------------------------------------------------------------------------------------------//
ROOT.gROOT.SetBatch(True)
# ----------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
	"struct MyStruct{ \
	int miss; \
	float deta; \
	float dphi; \
	float hoe; \
	float dist; \
	float dcotth; \
	float pt; \
	float eta; \
	float phi; \
	float sceta; \
	float scet; \
	float caloMEt; \
	float pfMEt; \
	float pfMEt_phi; \
	float tcMEt; \
	float mt; \
	int gsfcharge; \
	int ctfcharge; \
	int scpixcharge; \
	float ecalreliso; \
	float trckreliso; \
	float hcalreliso; \
	float sigieie; \
	int secondelepass; \
	float secondeleet; \
	float hltdr; \
	int ecalDriven; \
	int eventTrigger; \
	};" 
)
ROOT.gROOT.ProcessLine( \
	"struct Meta{ \
	int runnumber; \
	int lumisection; \
	Long64_t eventnumber; \
	};"
)
from ROOT import MyStruct
from ROOT import Meta
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//
# First Get the User Input:
# So far only option is -doTnP
optlist = ['-doTnP','-doCor','-doTrig=','-Help']
tmp,opts = getopt.getopt(sys.argv[0:],'',longopts=optlist)
args = sys.argv[1:]
etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.4],[0.0,2.4]]
suffix_=["_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos","_inc_pos",
	 "_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg","_inc_neg"]



#wptbins = [[0,5],  [5,10],  [10,20],[20,50],[50,9999]]

wptbins = [[0.,4.],[4.,8.],[8.,12.],[12.,16.],[16.,24.],[24.,50.],[50.,75.],[75.,100.],[100.,99999.9]]
wptsuffix_=["_wpt1_pos","_wpt2_pos","_wpt3_pos","_wpt4_pos","_wpt5_pos","_wpt6_pos","_wpt7_pos","_wpt8_pos","_wpt9_pos",
            "_wpt1_neg","_wpt2_neg","_wpt3_neg","_wpt4_neg","_wpt5_neg","_wpt6_neg","_wpt7_neg","_wpt8_neg","_wpt9_neg",]

ptcuts = [25,30,35]
ptsuffix_ = ["","_30","_35"]

metCut = 0 

centval = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
nentries = [0,0,0,0,0,0,0,0]

#Check if user wants to correct the tag and probe
#Also check if there is a desired trigger
#You must know what triggerChoice corresponds to
corrTnP 	= False
selectTrig 	= False
doTagAndProbe   = False
HELPME 		= False

for o in opts:
	#if o in optlist:
	if o == '-doTnP':
		doTagAndProbe = True
		args.remove(o)
	if o == '-doCor':
		corrTnP = True
		args.remove(o)
	if o == '-Help':
		HELPME = True
		args.remove(o)
	if '-doTrig=' in o:
		TrigVal = int((o.split('='))[-1])
		selectTrig = True
		args.remove(o)
		
if HELPME: 
	PrintHelp('WenuAnalyser.py')
	sys.exit()
		
if len(args) == 1:
  Name = str(args[0])
#
else:
  print "Wrong number of arguments defulting to using wenu.root, use -Help"
  Name = 'wenu.root'


print "Using Ntuple" , Name
InFileName = nTupleDir_+'/'+Name
#InFileName = 'rfio:/castor/cern.ch/user/n/nckw/WENU/Ntuples/Fall10MC/'+Name
#if os.path.isfile(InFileName): 
InFile = ROOT.TFile.Open(InFileName)
#else: sys.exit("No File found Named %s" %(InFileName))

print "Filling Histograms for the Selections; " 
for WP in WPchoices_: print WP+',',
WP = WPchoices_[0]
print '\n',
if selectTrig: print "Selecting Trigger", TrigVal
			      
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

OutName = './Results'+Name
OutFile = ROOT.TFile(OutName,'RECREATE')

OutFile.cd()
di = OutFile.mkdir('Templates_WP80_Ele25')
di.cd()



# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

#WorkingPoints = {'70':WP70(),'80':WP80(),'85':WP85(),'90':WP90(),'95':WP95(),'SC':WPSC(),}
WorkingPoints = VBTFWP.copy()

# ------------------------------------------------------------------------------------------------------------------//
# Set up the relevant histograms
<<<<<<< WenuAnalyser.py
# ------------------------------------------------------------------------------------------------------------------//
# --------------------------------------------------------------------------------------------------//
##ETA CHARGE BINS
# SELECTED
=======
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# --------------------------------------------------------------------------------------------------//
##ETA CHARGE BINS
# SELECTED
>>>>>>> 1.4
pfMET_sel_    = [[ROOT.TH1F("h_pfMET"+bin+ptbin,   "h_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in suffix_] for ptbin in ptsuffix_]
pfMET_selp_    = [[ROOT.TH1F("h_pfMETp"+bin+ptbin,   "h_pfMETp"+bin+ptbin,nmetbins_,0.,100.)    for bin in suffix_] for ptbin in ptsuffix_]
pfMET_selm_    = [[ROOT.TH1F("h_pfMETm"+bin+ptbin,   "h_pfMETm"+bin+ptbin,nmetbins_,0.,100.)    for bin in suffix_] for ptbin in ptsuffix_]
pfMET_selcor_ = [[ROOT.TH1F("h_pfMETcor"+bin+ptbin,"h_pfMETcor"+bin+ptbin,nmetbins_,0.,100.) for bin in suffix_] for ptbin in ptsuffix_]
MT_sel_       = [[ROOT.TH1F("h_MT"+bin+ptbin,      "h_MT"+bin+ptbin,nmetbins_,0.,150.)       for bin in suffix_] for ptbin in ptsuffix_]
MT_selcor_    = [[ROOT.TH1F("h_MTcor"+bin+ptbin,   "h_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in suffix_] for ptbin in ptsuffix_]

# ANTISELECTED
pfMET_antisel_    = [[ROOT.TH1F("h_anti_pfMET"+bin+ptbin,   "h_anti_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in suffix_] for ptbin in ptsuffix_]
pfMET_antiselcor_ = [[ROOT.TH1F("h_anti_pfMETcor"+bin+ptbin,"h_anti_pfMETcor"+bin+ptbin,nmetbins_,0.,100.) for bin in suffix_] for ptbin in ptsuffix_]
MT_antisel_       = [[ROOT.TH1F("h_anti_MT"+bin+ptbin,      "h_anti_MT"+bin+ptbin,nmetbins_,0.,150.)       for bin in suffix_] for ptbin in ptsuffix_]
MT_antiselcor_    = [[ROOT.TH1F("h_anti_MTcor"+bin+ptbin,   "h_anti_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in suffix_] for ptbin in ptsuffix_]

<<<<<<< WenuAnalyser.py
# --------------------------------------------------------------------------------------------------//
##WPT CHARGE BINS
#pfMET_wpt_ = [ROOT.TH1F("h_wpt"+ptbin,   "h_wpt"+ptbin,nmetbins_,0.,100.) for ptbin in ptsuffix_]

# SELECTED
#pfMET_wpt_sel_        = [[ROOT.TH1F("h_wpt_pfMET"+bin+ptbin,   "h_wpt_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_selcor_        = [[ROOT.TH1F("h_wpt_pfMETcor"+bin+ptbin,   "h_wpt_pfMETcor"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_selcorEE_        = [[ROOT.TH1F("h_wpt_pfMETcorEE"+bin+ptbin,   "h_wpt_pfMETcorEE"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_selcorEB_        = [[ROOT.TH1F("h_wpt_pfMETcorEB"+bin+ptbin,   "h_wpt_pfMETcorEB"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_sel_        = [[ROOT.TH1F("h_wpt_MT"+bin+ptbin,   "h_wpt_MT"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_selcor_        = [[ROOT.TH1F("h_wpt_MTcor"+bin+ptbin,   "h_wpt_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_selcorEE_        = [[ROOT.TH1F("h_wpt_MTcorEE"+bin+ptbin,   "h_wpt_MTcorEE"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_selcorEB_        = [[ROOT.TH1F("h_wpt_MTcorEB"+bin+ptbin,   "h_wpt_MTcorEB"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#
## ANTISELECTED
#pfMET_wpt_antisel_    = [[ROOT.TH1F("h_wpt_anti_pfMET"+bin+ptbin,   "h_wpt_anti_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_antiselcor_    = [[ROOT.TH1F("h_wpt_anti_pfMETcor"+bin+ptbin,   "h_wpt_anti_pfMETcor"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_antiselcorEE_        = [[ROOT.TH1F("h_wpt_anti_pfMETcorEE"+bin+ptbin,   "h_wpt_anti_pfMETcorEE"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#pfMET_wpt_antiselcorEB_        = [[ROOT.TH1F("h_wpt_anti_pfMETcorEB"+bin+ptbin,   "h_wpt_anti_pfMETcorEB"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
##MT_wpt_antisel_    = [[ROOT.TH1F("h_wpt_anti_MT"+bin+ptbin,   "h_wpt_anti_MT"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_antiselcor_    = [[ROOT.TH1F("h_wpt_anti_MTcor"+bin+ptbin,   "h_wpt_anti_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_antiselcorEE_        = [[ROOT.TH1F("h_wpt_anti_MTcorEE"+bin+ptbin,   "h_wpt_MTcorEE"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
#MT_wpt_antiselcorEB_        = [[ROOT.TH1F("h_wpt_anti_MTcorEB"+bin+ptbin,   "h_wpt_MTcorEB"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
## --------------------------------------------------------------------------------------------------//
## ANTISELECTION STUDIES
dphis_ = ["85","80","70","60"]
detas_ = ["95","90","85","80","70"]
=======
# --------------------------------------------------------------------------------------------------//
##WPT CHARGE BINS
pfMET_wpt_ = [ROOT.TH1F("h_wpt"+ptbin,   "h_wpt"+ptbin,nmetbins_,0.,100.) for ptbin in ptsuffix_]

# SELECTED
pfMET_wpt_sel_        = [[ROOT.TH1F("h_wpt_pfMET"+bin+ptbin,   "h_wpt_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_selcor_        = [[ROOT.TH1F("h_wpt_pfMETcor"+bin+ptbin,   "h_wpt_pfMETcor"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_selcorEE_        = [[ROOT.TH1F("h_wpt_pfMETcorEE"+bin+ptbin,   "h_wpt_pfMETcorEE"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_selcorEB_        = [[ROOT.TH1F("h_wpt_pfMETcorEB"+bin+ptbin,   "h_wpt_pfMETcorEB"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_sel_        = [[ROOT.TH1F("h_wpt_MT"+bin+ptbin,   "h_wpt_MT"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_selcor_        = [[ROOT.TH1F("h_wpt_MTcor"+bin+ptbin,   "h_wpt_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_selcorEE_        = [[ROOT.TH1F("h_wpt_MTcorEE"+bin+ptbin,   "h_wpt_MTcorEE"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_selcorEB_        = [[ROOT.TH1F("h_wpt_MTcorEB"+bin+ptbin,   "h_wpt_MTcorEB"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]

# ANTISELECTED
pfMET_wpt_antisel_    = [[ROOT.TH1F("h_wpt_anti_pfMET"+bin+ptbin,   "h_wpt_anti_pfMET"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_antiselcor_    = [[ROOT.TH1F("h_wpt_anti_pfMETcor"+bin+ptbin,   "h_wpt_anti_pfMETcor"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_antiselcorEE_        = [[ROOT.TH1F("h_wpt_anti_pfMETcorEE"+bin+ptbin,   "h_wpt_anti_pfMETcorEE"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
pfMET_wpt_antiselcorEB_        = [[ROOT.TH1F("h_wpt_anti_pfMETcorEB"+bin+ptbin,   "h_wpt_anti_pfMETcorEB"+bin+ptbin,nmetbins_,0.,100.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_antisel_    = [[ROOT.TH1F("h_wpt_anti_MT"+bin+ptbin,   "h_wpt_anti_MT"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_antiselcor_    = [[ROOT.TH1F("h_wpt_anti_MTcor"+bin+ptbin,   "h_wpt_anti_MTcor"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_antiselcorEE_        = [[ROOT.TH1F("h_wpt_anti_MTcorEE"+bin+ptbin,   "h_wpt_MTcorEE"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
MT_wpt_antiselcorEB_        = [[ROOT.TH1F("h_wpt_anti_MTcorEB"+bin+ptbin,   "h_wpt_MTcorEB"+bin+ptbin,nmetbins_,0.,150.)    for bin in wptsuffix_] for ptbin in ptsuffix_]
# --------------------------------------------------------------------------------------------------//
# ANTISELECTION STUDIES
dphis_ = ["85","80","70","60"]
detas_ = ["95","90","85","80","70"]
>>>>>>> 1.4

dphis_ee_ = [0.04,0.03,0.02,0.02]
detas_ee_ = [0.01,0.009,0.007,0.007,0.005]

dphis_eb_ = [0.06,0.06,0.03,0.025]
detas_eb_ = [0.007,0.007,0.006,0.004,0.004]

pfMET_antisels_ = [[[[ROOT.TH1F("h_dphi"+dphi+"_deta"+deta+"_pfMET"+bin+ptbin,"h_dphi"+dphi+"_deta"+deta+"_pfMET"+bin+ptbin,nmetbins_,0.,100.) for bin in suffix_]for ptbin in ptsuffix_]for dphi in dphis_]for deta in detas_]
#MT_antisel_ =    [[[ROOT.TH1F("h_dphi"+dphi+"_deta"+deta+"_MT"+bin,   "h_dphi"+dphi+"_deta"+deta+"_MT"+bin,nmetbins_,0.,100.)    for bin in suffix_]for dphi in dphis_]for deta in detas_]


wvec=ROOT.TVector2() 
nvec=ROOT.TVector2() 
evec=ROOT.TVector2() 

#f = open('./Results'+Name+".txt", 'w')


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# Set Up the branch aliases
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
tree = InFile.Get('vbtfPresele_tree')
nEntries = tree.GetEntriesFast()
print "Found %i Events" %nEntries

bdeta = tree.GetBranch('ele_id_deta')
bdphi = tree.GetBranch('ele_id_dphi')
bdist = tree.GetBranch('ele_cr_dist')
bdcot = tree.GetBranch('ele_cr_dcot')
bmiss = tree.GetBranch('ele_cr_mhitsinner')
bhoe = tree.GetBranch('ele_id_hoe')
bpt = tree.GetBranch('ele_cand_et')
beta = tree.GetBranch('ele_cand_eta')
bphi = tree.GetBranch('ele_cand_phi')
bsceta = tree.GetBranch('ele_sc_eta')
bscet = tree.GetBranch('ele_sc_gsf_et')
bcaloMEt = tree.GetBranch('event_caloMET')
btcMEt = tree.GetBranch('event_tcMET')
bpfMEt = tree.GetBranch('event_pfMET')
bpfMEt_phi = tree.GetBranch('event_pfMET_phi')
bmt = tree.GetBranch('event_tcMT')
bgsfcharge = tree.GetBranch('ele_gsfCharge')
bctfcharge = tree.GetBranch('ele_ctfCharge')
bscpixcharge = tree.GetBranch('ele_scPixCharge')
btrckreliso = tree.GetBranch('ele_iso_track')
becalreliso = tree.GetBranch('ele_iso_ecal')
bhcalreliso = tree.GetBranch('ele_iso_hcal')
bsigieie = tree.GetBranch('ele_id_sihih')
bsecondelepass = tree.GetBranch('ele2nd_passes_selection')
beventTrigger = tree.GetBranch('event_triggerDecision')
#bsecondeleet = tree.GetBranch('ele2nd_sc_gsf_et')


b2ecalDriven = tree.GetBranch('ele2nd_ecalDriven')
b2dr = tree.GetBranch('ele2nd_hltmatched_dr')
b2deta = tree.GetBranch('ele2nd_id_deta')
b2dphi = tree.GetBranch('ele2nd_id_dphi')
b2dist = tree.GetBranch('ele2nd_cr_dist')
b2dcot = tree.GetBranch('ele2nd_cr_dcot')
b2miss = tree.GetBranch('ele2nd_cr_mhitsinner')
b2hoe = tree.GetBranch('ele2nd_id_hoe')
b2pt = tree.GetBranch('ele2nd_cand_et')
b2eta = tree.GetBranch('ele2nd_cand_eta')
b2phi = tree.GetBranch('ele2nd_cand_phi')
b2sceta = tree.GetBranch('ele2nd_sc_eta')
b2scet = tree.GetBranch('ele2nd_sc_gsf_et')
b2gsfcharge = tree.GetBranch('ele2nd_gsfCharge')
b2ctfcharge = tree.GetBranch('ele2nd_ctfCharge')
b2scpixcharge = tree.GetBranch('ele2nd_scPixCharge')
b2trckreliso = tree.GetBranch('ele2nd_iso_track')
b2ecalreliso = tree.GetBranch('ele2nd_iso_ecal')
b2hcalreliso = tree.GetBranch('ele2nd_iso_hcal')
b2sigieie = tree.GetBranch('ele2nd_id_sihih')

blumisection = tree.GetBranch('lumiSection')
brunnumber = tree.GetBranch('runNumber')
beventnumber = tree.GetBranch('eventNumber')

c = MyStruct()
e = MyStruct()
d = Meta()

bdeta.SetAddress(ROOT.AddressOf(c,'deta'))
bdphi.SetAddress(ROOT.AddressOf(c,'dphi'))
bdist.SetAddress(ROOT.AddressOf(c,'dist'))
bdcot.SetAddress(ROOT.AddressOf(c,'dcotth'))
bmiss.SetAddress(ROOT.AddressOf(c,'miss'))
bhoe.SetAddress(ROOT.AddressOf(c,'hoe'))
bpt.SetAddress(ROOT.AddressOf(c,'pt'))
beta.SetAddress(ROOT.AddressOf(c,'eta'))
bphi.SetAddress(ROOT.AddressOf(c,'phi'))
bsceta.SetAddress(ROOT.AddressOf(c,'sceta'))
bscet.SetAddress(ROOT.AddressOf(c,'scet'))
bcaloMEt.SetAddress(ROOT.AddressOf(c,'caloMEt'))
btcMEt.SetAddress(ROOT.AddressOf(c,'tcMEt'))
bpfMEt.SetAddress(ROOT.AddressOf(c,'pfMEt'))
bpfMEt_phi.SetAddress(ROOT.AddressOf(c,'pfMEt_phi'))
bmt.SetAddress(ROOT.AddressOf(c,'mt'))
bgsfcharge.SetAddress(ROOT.AddressOf(c,'gsfcharge'))
bctfcharge.SetAddress(ROOT.AddressOf(c,'ctfcharge'))
bscpixcharge.SetAddress(ROOT.AddressOf(c,'scpixcharge'))
btrckreliso.SetAddress(ROOT.AddressOf(c,'trckreliso'))
becalreliso.SetAddress(ROOT.AddressOf(c,'ecalreliso'))
bhcalreliso.SetAddress(ROOT.AddressOf(c,'hcalreliso'))
bsigieie.SetAddress(ROOT.AddressOf(c,'sigieie'))
beventTrigger.SetAddress(ROOT.AddressOf(c,'eventTrigger'))

b2ecalDriven.SetAddress(ROOT.AddressOf(e,'ecalDriven'))
b2dr.SetAddress(ROOT.AddressOf(e,'hltdr'))
b2deta.SetAddress(ROOT.AddressOf(e,'deta'))
b2dphi.SetAddress(ROOT.AddressOf(e,'dphi'))
b2dist.SetAddress(ROOT.AddressOf(e,'dist'))
b2dcot.SetAddress(ROOT.AddressOf(e,'dcotth'))
b2miss.SetAddress(ROOT.AddressOf(e,'miss'))
b2hoe.SetAddress(ROOT.AddressOf(e,'hoe'))
b2pt.SetAddress(ROOT.AddressOf(e,'pt'))
b2eta.SetAddress(ROOT.AddressOf(e,'eta'))
b2phi.SetAddress(ROOT.AddressOf(e,'phi'))
b2sceta.SetAddress(ROOT.AddressOf(e,'sceta'))
b2scet.SetAddress(ROOT.AddressOf(e,'scet'))
b2gsfcharge.SetAddress(ROOT.AddressOf(e,'gsfcharge'))
b2ctfcharge.SetAddress(ROOT.AddressOf(e,'ctfcharge'))
b2scpixcharge.SetAddress(ROOT.AddressOf(e,'scpixcharge'))
b2trckreliso.SetAddress(ROOT.AddressOf(e,'trckreliso'))
b2ecalreliso.SetAddress(ROOT.AddressOf(e,'ecalreliso'))
b2hcalreliso.SetAddress(ROOT.AddressOf(e,'hcalreliso'))
b2sigieie.SetAddress(ROOT.AddressOf(e,'sigieie'))

blumisection.SetAddress(ROOT.AddressOf(d,'lumisection'))
brunnumber.SetAddress(ROOT.AddressOf(d,'runnumber'))
beventnumber.SetAddress(ROOT.AddressOf(d,'eventnumber'))
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# Deprecated, check if there is second electron info
if bsecondelepass is not None:	
	bsecondelepass.SetAddress(ROOT.AddressOf(c,'secondelepass'))
	HasSecondElectronInfo = True
else:	HasSecondElectronInfo = False

count = 0
ZeeCounter = 0

# Begin the loop over events -----------------------------------------------------------//
# --------------------------------------------------------------------------------------//

for i in range(0,nEntries):

  tree.GetEntry(i)
  # Firstly , ignore the event if trigger was selected and it didnt pass that trigger :)
  if selectTrig:
  	if c.eventTrigger & TrigVal == 0: continue

  ## PFMET cut
  if c.pfMEt < metCut : continue
 
  charge = sum([c.gsfcharge,c.scpixcharge,c.ctfcharge])
  if abs(charge) > 3 : continue #charge is wrong
  #charge = charge/abs(charge)

  Elec = Electron(c.pt,c.eta,c.trckreliso,c.ecalreliso,c.hcalreliso,c.deta,c.dphi, \
		  c.sigieie,c.dist,c.dcotth,c.miss,c.hoe,c.sceta,c.scet,charge)
  ElecAnti = Electron(c.pt,c.eta,c.trckreliso,c.ecalreliso,c.hcalreliso,0,0, \
		  0,c.dist,c.dcotth,c.miss,c.hoe,c.sceta,c.scet,charge)
		  
  if HasSecondElectronInfo:
    Ele2nd = Electron(e.pt,e.eta,e.trckreliso,e.ecalreliso,e.hcalreliso,e.deta,e.dphi,\
		      e.sigieie,e.dist,e.dcotth,e.miss,e.hoe,e.sceta,e.scet,0)
    if Ele2nd.scet > 15. and Ele2nd.PassFullSelection('95'): continue
    del(Ele2nd)

  ##Find Eta Charge Bin(s)
  toFill = []#inclusive bin 
  
  for bin, etaRange in enumerate(etabins) :
    #if bin == 0 :  print "WTF"
    if abs(c.eta) > etaRange[0] and abs(c.eta) < etaRange[1] :
      centval[bin] += abs(c.eta)
      nentries[bin] += 1
      j = bin
      if charge < 0: j = j+len(etabins)
      toFill.append(j)
	  
<<<<<<< WenuAnalyser.py
#  toFillwpt = []# no inclusive bin
#  nvec.SetMagPhi(c.pfMEt,c.pfMEt_phi)
#  evec.SetMagPhi(c.pt,c.phi)
#  wvec.Set(evec.X()+nvec.X(),evec.Y()+nvec.Y())
#  wpt = wvec.Mod()
#  for bin, wptRange in enumerate(wptbins) :
#    if wpt > wptRange[0] and wpt < wptRange[1] :
#      j = bin
#      if charge < 0: j = j+len(wptbins)
#      toFillwpt.append(j)
=======
  toFillwpt = []# no inclusive bin
  nvec.SetMagPhi(c.pfMEt,c.pfMEt_phi)
  evec.SetMagPhi(c.pt,c.phi)
  wvec.Set(evec.X()+nvec.X(),evec.Y()+nvec.Y())
  wpt = wvec.Mod()
  for bin, wptRange in enumerate(wptbins) :
    if wpt > wptRange[0] and wpt < wptRange[1] :
      j = bin
      if charge < 0: j = j+len(wptbins)
      toFillwpt.append(j)
>>>>>>> 1.4
	  
  #print toFillwpt,wpt
  ##Selection
#  x = (d.runnumber,d.lumisection,d.eventnumber)
    
  passSel = True
  passSel = passSel and (Elec.IsFiducial())
  passSel = passSel and (c.gsfcharge==c.scpixcharge==c.ctfcharge) 
  passSel = passSel and (Elec.PassFullSelection(WP))    

  ##begin horrific edit of my code to remove deta cut
  #passSel = passSel and (ElecAnti.PassFullSelection(WP))    
  ##passAS = passAS and (ElecAnti.IsFiducial())
  #if (Elec.isEB ==1):
  #  passSel = passSel and (Elec.PassFullSelection(WP))
  #elif (Elec.isEE == 1):
  #  passSel = passSel and (abs(Elec.dphi) < 0.03) and (abs(Elec.sigieie) <0.03)  ##no deta

  #bIn39 = False
  
  #if passSel : 
    #index =  bisect.bisect_left(b_38, x)
    #if index != len(b_38) and b_38[index] == x:
      #bIn38 = True
      ##print x,b_exclude[index]
    #else :
      #bIn38 = False
  
  #if passSel : 
    #index =  bisect.bisect_left(b_39, x)
    #if index != len(b_39) and b_39[index] == x:
      #bIn39 = True
      ##print x,b_exclude[index]
    #else :
      #bIn39 = False
  
  #if (not bIn38) and bIn39 : 
    #passSel=False # remove event
    ##print "removing: ",x
  
<<<<<<< WenuAnalyser.py
  if passSel :  
 #   f.write("\n"+str(x))
=======
  if passSel :  
    f.write("\n"+str(x))
>>>>>>> 1.4
    for i in range(len(ptcuts)) :
<<<<<<< WenuAnalyser.py
      if  (c.pt > ptcuts[i]) :#Fill uncorrected Templates
        #pfMET_wpt_[i].Fill(wpt)
        #for j in toFillwpt :
         # (pfMET_wpt_sel_[i])[j].Fill(c.pfMEt)
         # (MT_wpt_sel_[i])[j].Fill(c.mt)
          #if (Elec.isEB ==1):(pfMET_wpt_selEE_[i])[j].Fill(c.pfMEt)
          #if (Elec.isEE ==1):(pfMET_wpt_selEB_[i])[j].Fill(c.pfMEt)
          #if (Elec.isEB ==1):(MT_wpt_selEB_[i])[j].Fill(c.mt)
          #if (Elec.isEE ==1):(MT_wpt_selEE_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_sel_[i])[j].Fill(c.pfMEt)
          (MT_sel_[i])[j].Fill(c.mt)
      if (Elec.corPT(d.runnumber) > ptcuts[i]) : #Fill corrected Templates
        #for j in toFillwpt :
         # (pfMET_wpt_selcor_[i])[j].Fill(c.pfMEt)
         # (MT_wpt_selcor_[i])[j].Fill(c.mt)
         # if (abs(c.eta) > 0.8):(pfMET_wpt_selcorEE_[i])[j].Fill(c.pfMEt)
         # if (abs(c.eta) < 0.8):(pfMET_wpt_selcorEB_[i])[j].Fill(c.pfMEt)
         # if (abs(c.eta) > 0.8):(MT_wpt_selcorEE_[i])[j].Fill(c.mt)
         # if (abs(c.eta) < 0.8):(MT_wpt_selcorEB_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_selcor_[i])[j].Fill(c.pfMEt)
          (MT_selcor_[i])[j].Fill(c.mt)
      if (c.eta > 0.0) and (Elec.corPT(d.runnumber) > ptcuts[i])  : # Positive Eta
        for j in toFill :
          (pfMET_selp_[i])[j].Fill(c.pfMEt)
      if (c.eta < 0.0) and (Elec.corPT(d.runnumber) > ptcuts[i])  : # Negative Eta 
        for j in toFill :
          (pfMET_selm_[i])[j].Fill(c.pfMEt)
=======
      if  (c.pt > ptcuts[i]) :#Fill uncorrected Templates
        pfMET_wpt_[i].Fill(wpt)
        for j in toFillwpt :
          (pfMET_wpt_sel_[i])[j].Fill(c.pfMEt)
          (MT_wpt_sel_[i])[j].Fill(c.mt)
          #if (Elec.isEB ==1):(pfMET_wpt_selEE_[i])[j].Fill(c.pfMEt)
          #if (Elec.isEE ==1):(pfMET_wpt_selEB_[i])[j].Fill(c.pfMEt)
          #if (Elec.isEB ==1):(MT_wpt_selEB_[i])[j].Fill(c.mt)
          #if (Elec.isEE ==1):(MT_wpt_selEE_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_sel_[i])[j].Fill(c.pfMEt)
          (MT_sel_[i])[j].Fill(c.mt)
      if (Elec.corPT(d.runnumber) > ptcuts[i]) : #Fill corrected Templates
        for j in toFillwpt :
          (pfMET_wpt_selcor_[i])[j].Fill(c.pfMEt)
          (MT_wpt_selcor_[i])[j].Fill(c.mt)
          if (abs(c.eta) > 0.8):(pfMET_wpt_selcorEE_[i])[j].Fill(c.pfMEt)
          if (abs(c.eta) < 0.8):(pfMET_wpt_selcorEB_[i])[j].Fill(c.pfMEt)
          if (abs(c.eta) > 0.8):(MT_wpt_selcorEE_[i])[j].Fill(c.mt)
          if (abs(c.eta) < 0.8):(MT_wpt_selcorEB_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_selcor_[i])[j].Fill(c.pfMEt)
          (MT_selcor_[i])[j].Fill(c.mt)
      if (c.eta > 0.0) and (Elec.corPT(d.runnumber) > ptcuts[i])  : # Positive Eta
        for j in toFill :
          (pfMET_selp_[i])[j].Fill(c.pfMEt)
      if (c.eta < 0.0) and (Elec.corPT(d.runnumber) > ptcuts[i])  : # Negative Eta 
        for j in toFill :
          (pfMET_selm_[i])[j].Fill(c.pfMEt)
>>>>>>> 1.4

  ##Antiselection
  passAS = True
# passAS = passAS and (ElecAnti.scet > cElecPtMin_)
  passAS = passAS and (ElecAnti.PassID(QCDSelection_))
  passAS = passAS and (ElecAnti.PassHcalRelIso(QCDSelection_))
  passAS = passAS and (ElecAnti.PassEcalRelIso(QCDSelection_))
  passAS = passAS and (ElecAnti.PassTrckRelIso(QCDSelection_))
  passAS = passAS and (ElecAnti.IsFiducial())
<<<<<<< WenuAnalyser.py
  
#  AS studies 
#  if passAS :
#    for i in range(len(ptcuts)) :
#      if (Elec.corPT(d.runnumber) > ptcuts[i]) : 
#        for dphi,dphi_ee,dphi_eb in zip(range(len(dphis_)),dphis_ee_,dphis_eb_) :
#          for deta,deta_ee,deta_eb in zip(range(len(detas_)),detas_ee_,detas_eb_) :
#            if ((Elec.isEB == 1) and (Elec.dphi > dphi_eb) and (Elec.deta > deta_eb)) or ((Elec.isEE == 1) and (Elec.dphi > dphi_ee) and (Elec.deta > deta_ee)) :
#              for j in toFill :
#                (((pfMET_antisels_[deta])[dphi])[i])[j].Fill(c.pfMEt)
 
  #Nominal AS
=======
  
  #AS studies 
  if passAS :
    for i in range(len(ptcuts)) :
      if (Elec.corPT(d.runnumber) > ptcuts[i]) : 
        for dphi,dphi_ee,dphi_eb in zip(range(len(dphis_)),dphis_ee_,dphis_eb_) :
          for deta,deta_ee,deta_eb in zip(range(len(detas_)),detas_ee_,detas_eb_) :
            if ((Elec.isEB == 1) and (Elec.dphi > dphi_eb) and (Elec.deta > deta_eb)) or ((Elec.isEE == 1) and (Elec.dphi > dphi_ee) and (Elec.deta > deta_ee)) :
              for j in toFill :
                (((pfMET_antisels_[deta])[dphi])[i])[j].Fill(c.pfMEt)
 
  #Nominal AS
>>>>>>> 1.4
  if (Elec.isEB ==1):
    passAS = passAS and (Elec.deta > as_cEB_dEtaIn_) and (Elec.dphi > as_cEB_dPhiIn_)
  elif (Elec.isEE == 1):
    passAS = passAS and (Elec.deta > as_cEE_dEtaIn_) and (Elec.dphi > as_cEE_dPhiIn_)
  if passAS :
    for i in range(len(ptcuts)) :
      if  (c.pt > ptcuts[i]) :
<<<<<<< WenuAnalyser.py
#        for j in toFillwpt :
#          (pfMET_wpt_antisel_[i])[j].Fill(c.pfMEt)
#          (MT_wpt_antisel_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_antisel_[i])[j].Fill(c.pfMEt)
          (MT_antisel_[i])[j].Fill(c.mt)
=======
        for j in toFillwpt :
          (pfMET_wpt_antisel_[i])[j].Fill(c.pfMEt)
          (MT_wpt_antisel_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_antisel_[i])[j].Fill(c.pfMEt)
          (MT_antisel_[i])[j].Fill(c.mt)
>>>>>>> 1.4
      if (Elec.corPT(d.runnumber) > ptcuts[i]) : 
<<<<<<< WenuAnalyser.py
#        for j in toFillwpt :
#          (pfMET_wpt_antiselcor_[i])[j].Fill(c.pfMEt)
#          (MT_wpt_antiselcor_[i])[j].Fill(c.mt)
#          if (abs(c.eta) > 0.8):(pfMET_wpt_antiselcorEE_[i])[j].Fill(c.pfMEt)
#          if (abs(c.eta) < 0.8):(pfMET_wpt_antiselcorEB_[i])[j].Fill(c.pfMEt)
#          if (abs(c.eta) > 0.8):(MT_wpt_antiselcorEE_[i])[j].Fill(c.mt)
#          if (abs(c.eta) < 0.8):(MT_wpt_antiselcorEB_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_antiselcor_[i])[j].Fill(c.pfMEt)
          (MT_antiselcor_[i])[j].Fill(c.mt)

=======
        for j in toFillwpt :
          (pfMET_wpt_antiselcor_[i])[j].Fill(c.pfMEt)
          (MT_wpt_antiselcor_[i])[j].Fill(c.mt)
          if (abs(c.eta) > 0.8):(pfMET_wpt_antiselcorEE_[i])[j].Fill(c.pfMEt)
          if (abs(c.eta) < 0.8):(pfMET_wpt_antiselcorEB_[i])[j].Fill(c.pfMEt)
          if (abs(c.eta) > 0.8):(MT_wpt_antiselcorEE_[i])[j].Fill(c.mt)
          if (abs(c.eta) < 0.8):(MT_wpt_antiselcorEB_[i])[j].Fill(c.mt)
        for j in toFill :
          (pfMET_antiselcor_[i])[j].Fill(c.pfMEt)
          (MT_antiselcor_[i])[j].Fill(c.mt)

>>>>>>> 1.4
  del(Elec)
  del(ElecAnti)
#print "number of TnP Zee: ", ZeeCounter
#print "number of passing electrons: ", count

# -------------------------------------------------------------------------------------------------------------------//
# -------------------------------------------------------------------------------------------------------------------//
di.cd()
<<<<<<< WenuAnalyser.py



# SELECTED
for h1 in pfMET_sel_: 
=======



# SELECTED
for h1 in pfMET_sel_: 
  for h in h1 :
    h.Write()   
for h1 in pfMET_selp_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_selm_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_selcor_:
  for h in h1 :
    h.Write()   
for h1 in MT_sel_:
  for h in h1 :
    h.Write()   
for h1 in MT_selcor_:
  for h in h1 :
    h.Write()   

# ANTISELECTED
for h1 in pfMET_antisel_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_antiselcor_:
  for h in h1 :
    h.Write()   
for h1 in MT_antisel_:
  for h in h1 :
    h.Write()   
for h1 in MT_antiselcor_:
  for h in h1 :
    h.Write()   

# --------------------------------------------------------------------------------------------------//
##WPT CHARGE BINS
for h1 in pfMET_wpt_:
  h1.Write()   

# SELECTED
for h1 in pfMET_wpt_sel_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in pfMET_selp_:
=======
for h1 in pfMET_wpt_selcor_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_wpt_selcorEE_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_wpt_selcorEB_:
  for h in h1 :
    h.Write()   
for h1 in MT_wpt_sel_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in pfMET_selm_:
=======
for h1 in MT_wpt_selcor_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in pfMET_selcor_:
=======
for h1 in MT_wpt_selcorEE_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in MT_sel_:
=======
for h1 in MT_wpt_selcorEB_:
  for h in h1 :
    h.Write()   

# ANTISELECTED
for h1 in pfMET_wpt_antisel_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in MT_selcor_:
=======
for h1 in pfMET_wpt_antiselcor_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py

# ANTISELECTED
for h1 in pfMET_antisel_:
=======
for h1 in pfMET_wpt_antiselcorEE_:
  for h in h1 :
    h.Write()   
for h1 in pfMET_wpt_antiselcorEB_:
  for h in h1 :
    h.Write()   
for h1 in MT_wpt_antisel_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in pfMET_antiselcor_:
=======
for h1 in MT_wpt_antiselcor_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in MT_antisel_:
=======
for h1 in MT_wpt_antiselcorEE_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   
<<<<<<< WenuAnalyser.py
for h1 in MT_antiselcor_:
=======
for h1 in MT_wpt_antiselcorEB_:
>>>>>>> 1.4
  for h in h1 :
    h.Write()   

## --------------------------------------------------------------------------------------------------//
###WPT CHARGE BINS
#for h1 in pfMET_wpt_:
#  h1.Write()   
#
## SELECTED
#for h1 in pfMET_wpt_sel_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_selcor_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_selcorEE_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_selcorEB_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_sel_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_selcor_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_selcorEE_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_selcorEB_:
#  for h in h1 :
#    h.Write()   
#
## ANTISELECTED
#for h1 in pfMET_wpt_antisel_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_antiselcor_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_antiselcorEE_:
#  for h in h1 :
#    h.Write()   
#for h1 in pfMET_wpt_antiselcorEB_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_antisel_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_antiselcor_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_antiselcorEE_:
#  for h in h1 :
#    h.Write()   
#for h1 in MT_wpt_antiselcorEB_:
#  for h in h1 :
#    h.Write()   
#
OutFile.Close()
print "Results Saved in ", OutName
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# END
#print centval
#print nentries
#for cv,ne in zip(centval, nentries) :
#  print cv/ne

# QCDAnalyser.py
# Designed to produce Anti-selected Templates:
# Depends on ABCDEClasses.py

# Run As python QCDAnalyser filename (assuming they are in ntuples/)
#			     nmetbins_ (eg 25)
#			     nisobins_ (eg 10)
#			     WorkingPoint (70/85/80/90/95/SC etc...)
#		option	     -doTrig=int	# applies trigger cut, & with int
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Standars Imports
import ROOT
import sys,getopt,os
# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//
# Import from package
from conf.analyser_conf import *
from conf.classes import *

# ----------------------------------------------------------------------------------------------------------------------//
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

from ROOT import MyStruct
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//
# from the user, we want filename, nmetbins_, nisobins_, 
# list of WP choices (available in ABCDEClasses.py)


optlist = ['-doTrig=','-Help']
tmp,opts = getopt.getopt(sys.argv[0:],'',longopts=optlist)
args = sys.argv[1:]

selectTrig = False
HELPME     = False

for o in opts:
	if o == '-Help':
		HELPME = True
		args.remove(o)
	if '-doTrig=' in o:
		TrigVal = int((o.split('='))[-1])
		selectTrig = True
		args.remove(o)

		
if HELPME: 
	PrintHelp('QCDAnalyser.py')
	sys.exit()
	
if len(args) == 1:
  Name = str(args[0])


else:
  print "Wrong number of arguments defulting to using qcd.uroot, use -Help"
  Name = 'qcd.root'


print "Using Ntuple" , Name
InFileName = nTupleDir_+'/'+Name
#InFileName = 'rfio:/castor/cern.ch/user/n/nckw/WENU/Ntuples/Fall10MC/'+Name
if os.path.isfile(InFileName): InFile = ROOT.TFile.Open(InFileName)
else: sys.exit("No File found Named %s" %(InFileName))

print "Using Selection for QCD events:", QCDSelection_
print "Filling Histograms for the Selections; " 
for WP in WPchoices_: print WP+',',
print '\n',

if selectTrig: print "Selecting Trigger", TrigVal
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

OutName = 'templates/AntiSelection'+Name
OutFile = ROOT.TFile(OutName,'RECREATE')

# Now we make a Folder for each choice of the anti-selections:
for WP in WPchoices_ :

  OutFile.cd()
  di = OutFile.mkdir('VBTF'+WP)
  di.cd()

  di.mkdir('qcdanaEE')
  di.mkdir('qcdanaEB')

# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

WorkingPoints = VBTFWP.copy()
# Set up the histograms, this time we only actually have TrckRelIso and EcalRelIso vs the 4 MET types:

# Barrel
EBh_CaloMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"CaloMEt_x_TrckRelIsoEB","Calo #{E}_{T} vs TrckRelIso;Calo #slash{E}_{T};\
				       TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_TrckIso)\
			     for WP in WPchoices_]
EBh_PfMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"PfMEt_x_TrckRelIsoEB","Pf #{E}_{T} vs TrckRelIso;Pf #slash{E}_{T};\
			             TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_TrckIso)\
			   for WP in WPchoices_]
EBh_TcMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"TcMEt_x_TrckRelIsoEB","Tc #{E}_{T} vs TrckRelIso;Tc #slash{E}_{T};\
			             TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_TrckIso)\
			   for WP in WPchoices_]
EBh_MtMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"MtMEt_x_TrckRelIsoEB","Mt  vs TrckRelIso;M_{T};\
			             TrckIso/Pt;Arbitrary Units",nmetbins_,0.,200.,nisobins_,0.,WorkingPoints[WP].cEB_TrckIso)\
			   for WP in WPchoices_]

EBh_CaloMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"CaloMEt_x_EcalRelIsoEB","Calo #{E}_{T} vs EcalRelIso;Calo #slash{E}_{T};\
				       EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			     for WP in WPchoices_]
EBh_PfMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"PfMEt_x_EcalRelIsoEB","Pf #{E}_{T} vs EcalRelIso;Pf #slash{E}_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]
EBh_TcMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"TcMEt_x_EcalRelIsoEB","Tc #{E}_{T} vs EcalRelIso;Tc #slash{E}_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]
EBh_MtMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"MtMEt_x_EcalRelIsoEB","Mt  vs EcalRelIso;M_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,200.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]

#EndCap
EEh_CaloMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"CaloMEt_x_TrckRelIsoEE","Calo #{E}_{T} vs TrckRelIso;Calo #slash{E}_{T};\
				       TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEE_TrckIso)\
		             for WP in WPchoices_]
EEh_PfMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"PfMEt_x_TrckRelIsoEE","Pf #{E}_{T} vs TrckRelIso;Pf #slash{E}_{T};\
			             TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEE_TrckIso)\
			   for WP in WPchoices_]
EEh_TcMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"TcMEt_x_TrckRelIsoEE","Tc #{E}_{T} vs TrckRelIso;Tc #slash{E}_{T};\
				     TrckIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEE_TrckIso)\
			   for WP in WPchoices_]
EEh_MtMEt_x_TrckRelIso_ = [ROOT.TH2F(WP+"MtMEt_x_TrckRelIsoEE","Mt  vs TrckRelIso;M_{T};\
			             TrckIso/Pt;Arbitrary Units",nmetbins_,0.,200.,nisobins_,0.,WorkingPoints[WP].cEE_TrckIso)\
			   for WP in WPchoices_]

EEh_CaloMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"CaloMEt_x_EcalRelIsoEE","Calo #{E}_{T} vs EcalRelIso;Calo #slash{E}_{T};\
				       EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			     for WP in WPchoices_]
EEh_PfMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"PfMEt_x_EcalRelIsoEE","Pf #{E}_{T} vs EcalRelIso;Pf #slash{E}_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]
EEh_TcMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"TcMEt_x_EcalRelIsoEE","Tc #{E}_{T} vs EcalRelIso;Tc #slash{E}_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,100.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]
EEh_MtMEt_x_EcalRelIso_ = [ROOT.TH2F(WP+"MtMEt_x_EcalRelIsoEE","Mt  vs EcalRelIso;M_{T};\
			             EcalIso/Pt;Arbitrary Units",nmetbins_,0.,200.,nisobins_,0.,WorkingPoints[WP].cEB_EcalIso)\
			   for WP in WPchoices_]
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

# Set Up the branch aliases
# ------------------------------------------------------------------------------------------------------------------//
tree = InFile.Get('vbtfPresele_tree')
nEntries = tree.GetEntriesFast()

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
bmt = tree.GetBranch('event_tcMT')
bgsfcharge = tree.GetBranch('ele_gsfCharge')
bctfcharge = tree.GetBranch('ele_ctfCharge')
bscpixcharge = tree.GetBranch('ele_scPixCharge')
btrckreliso = tree.GetBranch('ele_iso_track')
becalreliso = tree.GetBranch('ele_iso_ecal')
bhcalreliso = tree.GetBranch('ele_iso_hcal')
bsigieie = tree.GetBranch('ele_id_sihih')
bsecondelepass = tree.GetBranch('ele2nd_passes_selection')
bsecondeleet = tree.GetBranch('ele2nd_sc_gsf_et')
beventTrigger = tree.GetBranch('event_triggerDecision')


c = MyStruct()

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
bmt.SetAddress(ROOT.AddressOf(c,'mt'))
bgsfcharge.SetAddress(ROOT.AddressOf(c,'gsfcharge'))
bctfcharge.SetAddress(ROOT.AddressOf(c,'ctfcharge'))
bscpixcharge.SetAddress(ROOT.AddressOf(c,'scpixcharge'))
btrckreliso.SetAddress(ROOT.AddressOf(c,'trckreliso'))
becalreliso.SetAddress(ROOT.AddressOf(c,'ecalreliso'))
bhcalreliso.SetAddress(ROOT.AddressOf(c,'hcalreliso'))
bsigieie.SetAddress(ROOT.AddressOf(c,'sigieie'))
beventTrigger.SetAddress(ROOT.AddressOf(c,'eventTrigger'))

if bsecondelepass is not None:	
	bsecondelepass.SetAddress(ROOT.AddressOf(c,'secondelepass'))
	bsecondeleet.SetAddress(ROOT.AddressOf(c,'secondeleet'))
	HasSecondElectronInfo = True
else:	HasSecondElectronInfo = False

# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//
# Run over the events:

for i in range(0,nEntries):
  tree.GetEntry(i)

  # Firstly , ignore the event if trigger was selected and it didnt pass that trigger :)
  if selectTrig:
  	if c.eventTrigger & TrigVal == 0: continue
  
  charge = sum([c.gsfcharge,c.scpixcharge,c.ctfcharge])/abs(sum([c.gsfcharge,c.scpixcharge,c.ctfcharge]))

  if HasSecondElectronInfo:
  	if c.secondelepass >= 1 and c.secondeleet > cElecPtMin_: continue

  # Note carefully here that I make sure the electron passes dEta dPhi Cut byt setting to 0,0
  # This is because we want to apply the antiselection to these values later!
  Elec = Electron(c.pt,c.eta,c.trckreliso,c.ecalreliso,c.hcalreliso,0,0, \
		  0,c.dist,c.dcotth,c.miss,c.hoe,c.sceta,c.scet,charge)
 
  # The third Zero is SigiEiE, no need to cut on it
  
  
  if Elec.scet < cElecPtMin_: continue

  for it,WP in zip(range(len(WPchoices_)),WPchoices_):
	 # if (not Elec.PassConvRej(QCDSelection_) ):	continue
	  if (not Elec.PassID(QCDSelection_) ):		continue
	  if (not Elec.PassHcalRelIso(QCDSelection_)):	continue
	  if (not Elec.IsFiducial()): 			continue

	
	  # Fill the Histograms for Relative Tracker Isolation
	  if Elec.PassEcalRelIso(QCDSelection_) and \
	     Elec.PassTrckRelIso(WP):
	     
	   if (Elec.isEB ==1):
  	    # Now that we have an 'electron', apply the anti-selection:
	    if c.deta > as_cEB_dEtaIn_ and \
	       c.dphi > as_cEB_dPhiIn_:

		EBh_CaloMEt_x_TrckRelIso_[it].Fill(c.caloMEt,Elec.trckreliso)
		EBh_PfMEt_x_TrckRelIso_[it].Fill(c.pfMEt,Elec.trckreliso)
		EBh_TcMEt_x_TrckRelIso_[it].Fill(c.tcMEt,Elec.trckreliso)
		EBh_MtMEt_x_TrckRelIso_[it].Fill(c.mt,Elec.trckreliso)

	   elif (Elec.isEE == 1):

	    if c.deta > as_cEE_dEtaIn_ and \
	       c.dphi > as_cEE_dPhiIn_:
	
		EEh_CaloMEt_x_TrckRelIso_[it].Fill(c.caloMEt,Elec.trckreliso)
		EEh_PfMEt_x_TrckRelIso_[it].Fill(c.pfMEt,Elec.trckreliso)
		EEh_TcMEt_x_TrckRelIso_[it].Fill(c.tcMEt,Elec.trckreliso)
		EEh_MtMEt_x_TrckRelIso_[it].Fill(c.mt,Elec.trckreliso)
	
	
	  # Fill the Histograms for Relative Tracker Isolation
	  if Elec.PassTrckRelIso(QCDSelection_) and \
	     Elec.PassEcalRelIso(WP):
	  	  	     
	   if (Elec.isEB ==1):
  	    # Now that we have an 'electron', apply the anti-selection:
	    if c.deta > as_cEB_dEtaIn_ and \
	       c.dphi > as_cEB_dPhiIn_:

		EBh_CaloMEt_x_EcalRelIso_[it].Fill(c.caloMEt,Elec.ecalreliso)
		EBh_PfMEt_x_EcalRelIso_[it].Fill(c.pfMEt,Elec.ecalreliso)
		EBh_TcMEt_x_EcalRelIso_[it].Fill(c.tcMEt,Elec.ecalreliso)
		EBh_MtMEt_x_EcalRelIso_[it].Fill(c.mt,Elec.ecalreliso)

	   elif (Elec.isEE == 1):

	    if c.deta > as_cEE_dEtaIn_ and \
	       c.dphi > as_cEE_dPhiIn_:
	
		EEh_CaloMEt_x_EcalRelIso_[it].Fill(c.caloMEt,Elec.ecalreliso)
		EEh_PfMEt_x_EcalRelIso_[it].Fill(c.pfMEt,Elec.ecalreliso)
		EEh_TcMEt_x_EcalRelIso_[it].Fill(c.tcMEt,Elec.ecalreliso)
		EEh_MtMEt_x_EcalRelIso_[it].Fill(c.mt,Elec.ecalreliso)
	  
  del(Elec)

# Thats all thats needed for the antiselection
# ------------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------------//

for it,WP in zip(range(len(WPchoices_)),WPchoices_):

	OutFile.cd()
	
	OutFile.cd('VBTF'+WP+'/qcdanaEB')

	EBh_CaloMEt_x_TrckRelIso_[it].Write()
	EBh_PfMEt_x_TrckRelIso_[it].Write()
	EBh_TcMEt_x_TrckRelIso_[it].Write()
	EBh_MtMEt_x_TrckRelIso_[it].Write()
	
	EBh_CaloMEt_x_EcalRelIso_[it].Write()
	EBh_PfMEt_x_EcalRelIso_[it].Write()
	EBh_TcMEt_x_EcalRelIso_[it].Write()
	EBh_MtMEt_x_EcalRelIso_[it].Write()

	OutFile.cd('VBTF'+WP+'/qcdanaEE')

	EEh_CaloMEt_x_TrckRelIso_[it].Write()
	EEh_PfMEt_x_TrckRelIso_[it].Write()
	EEh_TcMEt_x_TrckRelIso_[it].Write()
	EEh_MtMEt_x_TrckRelIso_[it].Write()
		
	EEh_CaloMEt_x_EcalRelIso_[it].Write()
	EEh_PfMEt_x_EcalRelIso_[it].Write()
	EEh_TcMEt_x_EcalRelIso_[it].Write()
	EEh_MtMEt_x_EcalRelIso_[it].Write()


OutFile.Close()

print "Results Saved in ", OutName
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
# END

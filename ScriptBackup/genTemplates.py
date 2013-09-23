#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setupSUSY
from libFrameworkSUSY import *
from libWCharge       import *
from libSSDL      import *
from icf.core import PSet, Analysis
from icf.config import defaultConfig

import icf.utils as utils

#Import MC PSETS
# from Wenu_Spring10_START3X_V26_S09_v1 import *
# from EWK import *
# from QCD import *
# from AlexSamples import *

#Import DATA PSETS
from data.Electron_dec4_after148000 import *
from data.Electron_dec4_before148000 import *
from data.EG_dec4 import *

from data.EG_dec22 import *
from data.Electron_dec22_before148000 import *
from data.Electron_dec22_after148000 import *
 
from data.EG_Run2010A_Nov4ReReco_v1 import *
from data.Electron_Run2010B_Nov4ReReco_v1 import *

# from data.EG_Run2010A_Sep17ReReco_v2 import *
# from data.Electron_Run2010B_PromptReco_v2_p1 import *
# from data.Electron_Run2010B_PromptReco_v2_p2 import *
# from data.Electron_Run2010B_PromptReco_v2_p3 import *
# from data.Electron_Run2010B_PromptReco_v2_p4 import *
# from data.Electron_Run2010B_PromptReco_v2_p5 import *

##CHANGE THIS TO CHANGE FROM DATA TO MC
bData = True#False#False#True#False#False? True?

#Standard Cuts
conf = defaultConfig.copy()
conf.Ntuple.Jets.Prefix="ak5JetPF"
conf.Ntuple.Jets.Suffix="Pat"
conf.Ntuple.Electrons.Prefix="electron"
conf.Ntuple.Electrons.Suffix="Pat"
conf.Common.Jets.PtCut=40.0
conf.Common.Jets.EtaCut=5.0
conf.Common.Jets.ApplyID=True
conf.Common.Jets.TightID=False
conf.Common.Muons.EtaCut = 2.4
conf.Common.Muons.PtCut = 15.0
conf.Common.Muons.TrkIsoCut = -1.
conf.Common.Muons.CombIsoCut = 0.1
conf.Common.Electrons.PtCut = 15.0
conf.Common.Electrons.EtaCut = 2.4
conf.Common.Electrons.ApplyID=False

# Create the analysis
a = Analysis("Templates")

# Filters and Corrections
# Jet Energy Scale Corrections
# if bData :
  #from PFJetCorrections import * 
  #corPset =  CorrectionPset()
  #JetCorrections = JESCorrections( corPset.ps() )
  #a.AddJetFilter("PreCC",JetCorrections)
  # Good event
  # selection = OP_GoodEventSelection()

# Create a Tree called Main
tree = Tree("Main")

trigger_bits = ("HLT_Photon10_L1R", # Runs 132440-137028
		"HLT_Photon15_Cleaned_L1R", #Runs 138564-140401
		"HLT_Ele15_SW_CaloEleId_L1R", #Runs 141956-144114
		"HLT_Ele17_SW_CaloEleId_L1R", #Runs 146428-147116
		"HLT_Ele17_SW_TightEleId_L1R", #Runs 147196-148102
		"HLT_Ele22_SW_TighterCaloIdIsol_L1R_v1", #OR
		#"HLT_Ele17_SW_TighterEleIdIsol_L1R_v2", #Runs 148822-149063
		"HLT_Ele22_SW_TighterCaloIdIsol_L1R_v2", #OR
		#"HLT_Ele17_SW_TighterEleIdIsol_L1R_v3", #Runs 149181-149442
		)
      
triggers = PSet(Triggers=trigger_bits)
Trigg = OP_MultiTrigger(triggers.ps())

# Cuts
ZeroMuons = OP_NumComMuons("==", 0)

#use sc position of running on data
bUseSCEta = bData #Currently only in 3_8X data, not in 3_6X MC
#bUseSCEnergy = True

WP80_Ele25 = PSet(
        ElecET     = 25.0,
        ChCheck=True,
        ConvCheck=True,
        EleVeto=True,
        ElePtVeto=15.0,
        UseSCEta = bUseSCEta,
        UseSCEnergy = False,
        CorVersion = 1,## 0=3_8X, 1=3_9X
        WorkingPoint = 80
)

# WP80_Ele30 = PSet(
        # ElecET     = 30.0,
        # ChCheck=True,
        # ConvCheck=True,
        # EleVeto=True,
        # ElePtVeto=15.0,
        # UseSCEta = bUseSCEta,
        # UseSCEnergy = False,
        # WorkingPoint = 80
# )

# WP80_Ele25_SC = PSet(
        # ElecET     = 25.0,
        # ChCheck=True,
        # ConvCheck=True,
        # EleVeto=True,
        # ElePtVeto=15.0,
        # UseSCEta = bUseSCEta,
        # UseSCEnergy = True,
        # WorkingPoint = 80
# )

# WP80_Ele30_SC = PSet(
        # ElecET     = 30.0,
        # ChCheck=True,
        # ConvCheck=True,
        # EleVeto=True,
        # ElePtVeto=15.0,
        # UseSCEta = bUseSCEta,
        # UseSCEnergy = True,
        # WorkingPoint = 80
# )

Templates_WP80_Ele25=AsymTemplateHistos("Templates_WP80_Ele25",WP80_Ele25.ps())
# Templates_WP80_Ele30=ChAsymTemplateHistos("Templates_WP80_Ele30",WP80_Ele30.ps())
# Templates_WP80_Ele25_SC=ChAsymTemplateHistos("Templates_WP80_Ele25_SC",WP80_Ele25_SC.ps())
# Templates_WP80_Ele30_SC=ChAsymTemplateHistos("Templates_WP80_Ele30_SC",WP80_Ele30_SC.ps())
# Set up CUT flow
a += tree
if bData :
  tree.Attach(Trigg)
  tree.TAttach(Trigg,ZeroMuons)
else :
  tree.Attach(ZeroMuons)


test=PSet(
	Name="test",
	Format=("ICF",2),
	File=["/vols/cms02/mjarvis/ntuples/ElectronDec22_1_1_Fv2.root"],
	Weight=1.,
)
  
  
#Inclusive cuts
tree.TAttach(ZeroMuons,Templates_WP80_Ele25) #
# tree.TAttach(Templates_WP80_Ele25,Templates_WP80_Ele30) # 
# tree.TAttach(ZeroMuons,Templates_WP80_Ele25_SC) #
# tree.TAttach(Templates_WP80_Ele25_SC,Templates_WP80_Ele30_SC) # 
#For Testing
#Electron_Run2010B_PromptReco_v2_p1.LastEntry=1
	
if bData :
  samples =[
	#test
#       EGRUN2010A_Dec4,
# 	ElectronRUN2010B_Dec4_before148000, 
# 	ElectronRUN2010B_Dec4_after148000,
      # EG_Run2010A_Nov4ReReco_v1,
       # Electron_Run2010B_Nov4ReReco_v1
 	EGRUN2010A_Dec22,
	ElectronRUN2010B_Dec22_before148000, 
	ElectronRUN2010B_Dec22_after148000,
  ]
else :
  samples =[
   #PhotonJet_Pt30,
   #PhotonJet_Pt15,
   #ttbarTauola,
   #Wenu_Spring10_START3X_V26_S09_v1,
   #QCD_BCtoE_Pt20to30,
   #QCD_BCtoE_Pt30to80,
   #QCD_BCtoE_Pt80to170,
   #DYee_M1to10,
   #DYee_M10to20,
   #Wtaunu,
   #ZJets_madgraph,
   #QCD_EMEnriched_Pt20to30,
   #QCD_EMEnriched_Pt30to80,
   #QCD_EMEnriched_Pt80to170,
   #WminusToENu,
   #WplusToENu,
   #WminusToTauNu,
   #WplusToTauNu,
   #Zee_M20,
   #Ztautau_M20,
   #WToENu_TuneZ2_7TeV_pythia6,
   # WToTauNu_TuneZ2_7TeV_pythia6_tauola,
  ]

a.Run(".", conf, samples)

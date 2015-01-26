# -*- coding: utf-8 -*-
# selections.py
# Nicholas Wardle - Imperial College

# The Various Selections, use with classes.py


#----------------------------------------------------//
#----------------------------------------------------//
class WP70:

 # 70%Working point
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.025
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.03
 cEB_dEtaIn	=	0.004
 cEB_EcalIso	=	0.06
 cEB_HcalIso	=	0.03
 cEB_TrckIso	=	0.05

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.02 
 cEE_dEtaIn	=	0.005 
 cEE_EcalIso	=	0.025
 cEE_HcalIso	=	0.02
 cEE_TrckIso	=	0.025
#----------------------------------------------------//
#----------------------------------------------------//
class WP80:

 # 80% Working point
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.06
 cEB_dEtaIn	=	0.004
 cEB_EcalIso	=	0.07
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.09

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.03 
 cEE_dEtaIn	=	0.007 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.04
#----------------------------------------------------//
#----------------------------------------------------//
class WP85:

 # 85% Working point
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.06
 cEB_dEtaIn	=	0.006
 cEB_EcalIso	=	0.08
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.09

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.04 
 cEE_dEtaIn	=	0.007 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.05
#----------------------------------------------------//
#----------------------------------------------------//
class WP90:

 # 90% Working Point
 cmiss		=	1
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.12
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.8 
 cEB_dEtaIn	=	0.007 
 cEB_EcalIso	=	0.09
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.12

 cEE_HoE	=	0.05
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.7 
 cEE_dEtaIn	=	0.009
 cEE_EcalIso	=	0.06
 cEE_HcalIso	=	0.03
 cEE_TrckIso	=	0.05
#----------------------------------------------------//
#----------------------------------------------------//
class WP95:
  cmiss		=	1
  cdCotTh	=	-1 # effectively N/A
  cDist		=	-1	  # effectively N/A

  cEB_HoE	=	0.15
  cEB_siEiE	=	0.01
  cEB_dPhiIn	=	0.8 
  cEB_dEtaIn	=	0.007 
  cEB_EcalIso	=	2.00
  cEB_HcalIso	=	0.12
  cEB_TrckIso	=	0.15

  cEE_HoE	=	0.07
  cEE_siEiE	=	0.03 
  cEE_dPhiIn	=	0.7 
  cEE_dEtaIn	=	0.01 
  cEE_EcalIso	=	0.06
  cEE_HcalIso	=	0.05
  cEE_TrckIso	=	0.08
#----------------------------------------------------//
#----------------------------------------------------//
class WPSC:

 cmiss		=	500
 cdCotTh	=	-1
 cDist		=	-1

 cEB_HoE	=	10000
 cEB_siEiE	=	0.05
 cEB_dPhiIn	=	10000
 cEB_dEtaIn	=	10000
 cEB_EcalIso	=	5.0
 cEB_HcalIso	=	10000
 cEB_TrckIso	=	0.5

 cEE_HoE	=	10000
 cEE_siEiE	=	0.06 
 cEE_dPhiIn	=	10000 
 cEE_dEtaIn	=	10000 
 cEE_EcalIso	=	1.0
 cEE_HcalIso	=	10000
 cEE_TrckIso	=	1.0
#----------------------------------------------------//
#----------------------------------------------------//
class WP80dEtaIn:

 # 80% Working point, dEta extended
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.06
 cEB_dEtaIn	=	0.01 
 cEB_EcalIso	=	0.07
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.09

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.03 
 cEE_dEtaIn	=	0.015 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.04
#----------------------------------------------------//
#----------------------------------------------------//
class WP80TrckRelIso:

 # 80% Working point, TrckRelIso extended
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.06
 cEB_dEtaIn	=	0.004
 cEB_EcalIso	=	0.07
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.2

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.03 
 cEE_dEtaIn	=	0.007 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.1
#----------------------------------------------------//
#----------------------------------------------------//
class WP80dPhiIn:

 # 80% Working point, dPhi extended
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.12
 cEB_dEtaIn	=	0.004
 cEB_EcalIso	=	0.07
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.09

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.06 
 cEE_dEtaIn	=	0.007 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.04
#----------------------------------------------------//
#----------------------------------------------------//
class WP80TrckZero:

 # 80% Working point but very tight trckreliso
 cmiss		=	0
 cdCotTh	=	0.02
 cDist		=	0.02

 cEB_HoE	=	0.04
 cEB_siEiE	=	0.01
 cEB_dPhiIn	=	0.06
 cEB_dEtaIn	=	0.004
 cEB_EcalIso	=	0.07
 cEB_HcalIso	=	0.10
 cEB_TrckIso	=	0.00001

 cEE_HoE	=	0.025
 cEE_siEiE	=	0.03 
 cEE_dPhiIn	=	0.03 
 cEE_dEtaIn	=	0.007 
 cEE_EcalIso	=	0.05
 cEE_HcalIso	=	0.025
 cEE_TrckIso	=	0.00001
#----------------------------------------------------//
#----------------------------------------------------//

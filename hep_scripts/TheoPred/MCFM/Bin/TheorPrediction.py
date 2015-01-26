#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys 
sys.path.append('/usr/lib/root/')
import ROOT
import sys
from math import sqrt,sin,cos

# ------------------------------------------------------------------------------------------------------------------//
#User declared cuts
METCut = [20, 0.0, 0.0, 0.0]
PtLCut = [25.0,25.0,30.0,35.0]
PtUCut = 5000.0
EtaCut = 2.4


ntp_dir = "./ntuple/"


# ------------------------------------------------------------------------------------------------------------------//

ROOT.gROOT.ProcessLine( \
  "struct MyStruct{ \
  float E_3; \
  float E_4; \
  float E_5; \
  float px3; \
  float px4; \
  float px5; \
  float py3; \
  float py4; \
  float py5; \
  float pz3; \
  float pz4; \
  float pz5; \
  float PDF01; \
  float PDF02; \
  float PDF03; \
  float PDF04; \
  float PDF05; \
  float PDF06; \
  float PDF07; \
  float PDF08; \
  float PDF09; \
  float PDF10; \
  float PDF11; \
  float PDF12; \
  float PDF13; \
  float PDF14; \
  float PDF15; \
  float PDF16; \
  float PDF17; \
  float PDF18; \
  float PDF19; \
  float PDF10; \
  float PDF21; \
  float PDF22; \
  float PDF23; \
  float PDF24; \
  float PDF25; \
  float PDF26; \
  float PDF27; \
  float PDF28; \
  float PDF29; \
  float PDF30; \
  float PDF31; \
  float PDF32; \
  float PDF33; \
  float PDF34; \
  float PDF35; \
  float PDF36; \
  float PDF37; \
  float PDF38; \
  float PDF39; \
  float PDF40; \
  float PDF41; \
  float PDF42; \
  float PDF43; \
  float PDF44; \
  float PDF45; \
  float PDF46; \
  float PDF47; \
  float PDF48; \
  float PDF49; \
  float PDF50; \
  float PDF51; \
  float PDF52; \
  };"
)
from ROOT import MyStruct

# ------------------------------------------------------------------------------------------------------------------//
# using namespace RooFit

# ------------------------------------------------------------------------------------------------------------------//

etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.4]]
asymHigh =[0.0,0.0,0.0,0.0,0.0,0.0]
asymMid = [0.0,0.0,0.0,0.0,0.0,0.0]
asymLow = [0.0,0.0,0.0,0.0,0.0,0.0]

#-------------------------------------------------------------------------------------------------------------------//

output = "W_only_tota_cteq66."

#Wplus_ntp  = ["W_only_tota_MSTW200_80__80__plus.root" ,"W_only_tota_MSTW200_80__80__plus_1.root" ,"W_only_tota_MSTW200_80__80__plus_2.root"]
#Wminus_ntp = ["W_only_tota_MSTW200_80__80__minus.root","W_only_tota_MSTW200_80__80__minus_1.root","W_only_tota_MSTW200_80__80__minus_2.root"]

Wplus_ntp  = ["W_only_tota_cteq66._80__80__plus.root" ,"W_only_tota_cteq66._80__80__plus_1.root" ,"W_only_tota_cteq66._80__80__plus_2.root"]
Wminus_ntp = ["W_only_tota_cteq66._80__80__minus.root","W_only_tota_cteq66._80__80__minus_1.root","W_only_tota_cteq66._80__80__minus_2.root"]



npdfs = 44


#Wplus_ntp  = ["W_only_tota_CT10w.L_80__80__plus_3.root"]
#Wminus_ntp = ["W_only_tota_CT10w.L_80__80__minus_3.root"]


nP = []
nM = []
for i in range(len(PtLCut)):
  nP_cut = []
  nM_cut = []
  for j in range(npdfs):
    nP_cut.append([0.,0.,0.,0.,0.,0.])
    nM_cut.append([0.,0.,0.,0.,0.,0.])
  nP.append(nP_cut)
  nM.append(nM_cut)
######################f
###########Wplus_ntp
######################f
for ntp_name in Wplus_ntp :
    print "using ntuple: ", ntp_name
    InFile = ROOT.TFile.Open(ntp_dir+ntp_name) 
    # Set Up the branch aliases
    
    myTree = InFile.Get('h10')
    
    nEntries = myTree.GetEntriesFast()   
    bE_3 = myTree.GetBranch('E_3')
    bE_4 = myTree.GetBranch('E_4')
    bE_5 = myTree.GetBranch('E_5')
    bpx3 = myTree.GetBranch('px3')
    bpx4 = myTree.GetBranch('px4')
    bpx5 = myTree.GetBranch('px5')
    bpy3 = myTree.GetBranch('py3')
    bpy4 = myTree.GetBranch('py4')
    bpy5 = myTree.GetBranch('py5')
    bpz3 = myTree.GetBranch('pz3')
    bpz4 = myTree.GetBranch('pz4')
    bpz5 = myTree.GetBranch('pz5')
    
    bpdf = []
    for j in range(npdfs):
      #print 'PDF'+str(j+1).zfill(2)
      bpdf.append(myTree.GetBranch('PDF'+str(j+1).zfill(2)))
         
    c = MyStruct()

    bE_3.SetAddress(ROOT.AddressOf(c,'E_3'))
    bE_4.SetAddress(ROOT.AddressOf(c,'E_4'))
    bE_5.SetAddress(ROOT.AddressOf(c,'E_5'))
    bpx3.SetAddress(ROOT.AddressOf(c,'px3'))
    bpx4.SetAddress(ROOT.AddressOf(c,'px4'))
    bpx5.SetAddress(ROOT.AddressOf(c,'px5'))
    bpy3.SetAddress(ROOT.AddressOf(c,'py3'))
    bpy4.SetAddress(ROOT.AddressOf(c,'py4'))
    bpy5.SetAddress(ROOT.AddressOf(c,'py5'))
    bpz3.SetAddress(ROOT.AddressOf(c,'pz3'))
    bpz4.SetAddress(ROOT.AddressOf(c,'pz4'))
    bpz5.SetAddress(ROOT.AddressOf(c,'pz5'))
       
    for j in range(npdfs):
      #print 'PDF'+str(j+1).zfill(2)
      #print j
      if (j != 19) :bpdf[j].SetAddress(ROOT.AddressOf(c,'PDF'+str(j+1).zfill(2)))
        
    #there is a subtlety here
    #note mcfm flips these around
    #W+to(v(p3) + e+(p4)) NLO
    #W−to(e-(p3) + vbar(p4)) NLO
    
    nVec = ROOT.TLorentzVector()
    eVec = ROOT.TLorentzVector()
   
    for i in range(0,nEntries):
      #if i==10 : break
      if ((i+1)%50000 == 0) : print "At event: " + str(i) + "/"+str(nEntries)
      myTree.GetEntry(i)
      eVec.SetPxPyPzE(c.px4, c.py4, c.pz4, c.E_4)
      nVec.SetPxPyPzE(c.px3, c.py3, c.pz3, c.E_3)		#note mcfm flips these around

      for bin, etaRange in enumerate(etabins) : 		#First check eta ranges
	if abs(eVec.PseudoRapidity()) > etaRange[0] and abs(eVec.PseudoRapidity()) < etaRange[1] :
      	  pdflist = (c.PDF01,c.PDF02,c.PDF03,c.PDF04,c.PDF05,c.PDF06,c.PDF07,c.PDF08,c.PDF09,c.PDF10, #this is a fix so I can iterate over the pdf weights (damn ROOT!)
	  c.PDF11,c.PDF12,c.PDF13,c.PDF14,c.PDF15,c.PDF16,c.PDF17,c.PDF18,c.PDF19,"WTF",
	  c.PDF21,c.PDF22,c.PDF23,c.PDF24,c.PDF25,c.PDF26,c.PDF27,c.PDF28,c.PDF29,c.PDF30,
	  c.PDF31,c.PDF32,c.PDF33,c.PDF34,c.PDF35,c.PDF36,c.PDF37,c.PDF38,c.PDF39,c.PDF40,
	  c.PDF41,c.PDF42,c.PDF43,c.PDF44,c.PDF45,c.PDF46,c.PDF47,c.PDF48,c.PDF49,c.PDF50,
	  c.PDF51,c.PDF52)#
	  for i,ptcut,metcut in zip(range(len(PtLCut)),PtLCut,METCut) : 	#iterate over PT/MET cuts
	    if (eVec.Pt() > ptcut) and (nVec.Pt() > metcut) : 	#Check PT/MET cuts
	      #print "test"
	      for j in range(npdfs): 				#Each event is weighted differently for each pdf
		if (j != 19) :((nP[i])[j])[bin]+=pdflist[j]
	      
######################f
###########Wminus_ntp
######################f	      
for ntp_name in Wminus_ntp :
    print "using ntuple: ", ntp_name
    InFile = ROOT.TFile.Open(ntp_dir+ntp_name) 
    # Set Up the branch aliases
    
    myTree = InFile.Get('h10')
    
    nEntries = myTree.GetEntriesFast()   
    bE_3 = myTree.GetBranch('E_3')
    bE_4 = myTree.GetBranch('E_4')
    bE_5 = myTree.GetBranch('E_5')
    bpx3 = myTree.GetBranch('px3')
    bpx4 = myTree.GetBranch('px4')
    bpx5 = myTree.GetBranch('px5')
    bpy3 = myTree.GetBranch('py3')
    bpy4 = myTree.GetBranch('py4')
    bpy5 = myTree.GetBranch('py5')
    bpz3 = myTree.GetBranch('pz3')
    bpz4 = myTree.GetBranch('pz4')
    bpz5 = myTree.GetBranch('pz5')
    
    bpdf = []
    for j in range(npdfs):
      bpdf.append(myTree.GetBranch('PDF'+str(j+1).zfill(2)))
         
    c = MyStruct()

    bE_3.SetAddress(ROOT.AddressOf(c,'E_3'))
    bE_4.SetAddress(ROOT.AddressOf(c,'E_4'))
    bE_5.SetAddress(ROOT.AddressOf(c,'E_5'))
    bpx3.SetAddress(ROOT.AddressOf(c,'px3'))
    bpx4.SetAddress(ROOT.AddressOf(c,'px4'))
    bpx5.SetAddress(ROOT.AddressOf(c,'px5'))
    bpy3.SetAddress(ROOT.AddressOf(c,'py3'))
    bpy4.SetAddress(ROOT.AddressOf(c,'py4'))
    bpy5.SetAddress(ROOT.AddressOf(c,'py5'))
    bpz3.SetAddress(ROOT.AddressOf(c,'pz3'))
    bpz4.SetAddress(ROOT.AddressOf(c,'pz4'))
    bpz5.SetAddress(ROOT.AddressOf(c,'pz5'))
    
    for j in range(npdfs):
      if (j != 19) : bpdf[j].SetAddress(ROOT.AddressOf(c,'PDF'+str(j+1).zfill(2))) 
    
    #there is a subtlety here
    #note mcfm flips these around
    #W+to(v(p3) + e+(p4)) NLO
    #W−to(e-(p3) + vbar(p4)) NLO
    
    nVec = ROOT.TLorentzVector()
    eVec = ROOT.TLorentzVector()
   
    for i in range(0,nEntries):
      #if i==10 : break
      if ((i+1)%50000 == 0) : print "At event: " + str(i) + "/"+str(nEntries)
      myTree.GetEntry(i)
      eVec.SetPxPyPzE(c.px3, c.py3, c.pz3, c.E_3)
      nVec.SetPxPyPzE(c.px4, c.py4, c.pz4, c.E_4)  		#note mcfm flips these around
     
      for bin, etaRange in enumerate(etabins) : 		#First check eta ranges
	if abs(eVec.PseudoRapidity()) > etaRange[0] and abs(eVec.PseudoRapidity()) < etaRange[1] :
      	  pdflist = (c.PDF01,c.PDF02,c.PDF03,c.PDF04,c.PDF05,c.PDF06,c.PDF07,c.PDF08,c.PDF09,c.PDF10, #this is a fix so I can iterate over the pdf weights (damn ROOT!)
	  c.PDF11,c.PDF12,c.PDF13,c.PDF14,c.PDF15,c.PDF16,c.PDF17,c.PDF18,c.PDF19,"WTF",
	  c.PDF21,c.PDF22,c.PDF23,c.PDF24,c.PDF25,c.PDF26,c.PDF27,c.PDF28,c.PDF29,c.PDF30,
	  c.PDF31,c.PDF32,c.PDF33,c.PDF34,c.PDF35,c.PDF36,c.PDF37,c.PDF38,c.PDF39,c.PDF40,
	  c.PDF41,c.PDF42,c.PDF43,c.PDF44,c.PDF45,c.PDF46,c.PDF47,c.PDF48,c.PDF49,c.PDF50,
	  c.PDF51,c.PDF52)#
	  for i,ptcut,metcut in zip(range(len(PtLCut)),PtLCut,METCut) : 	#iterate over PT/MET cuts
	    if (eVec.Pt() > ptcut) and (nVec.Pt() > metcut) : 	#Check PT/MET cuts
	      #print "test"
	      for j in range(npdfs): 				#Each event is weighted differently for each pdf
		if (j != 19) :((nM[i])[j])[bin]+=pdflist[j]


f = open(output+'.txt', 'w')

for i,ptcut,metcut in zip(range(len(PtLCut)),PtLCut,METCut) :
  print "Lepton PT Cut",ptcut
  print "MET Cut",metcut
  f.write("MET Cut"+str(metcut)+"\n")
  f.write("Lepton PT Cut"+str(ptcut)+"\n")

  for j in range(npdfs):

    for l in range(len(etabins)) :
      if (j == 19) : continue
      asym = (((nP[i])[j])[l]-((nM[i])[j])[l])/(((nP[i])[j])[l]+((nM[i])[j])[l])
      if j==0 : 
	asymHigh[l]=asym
	asymMid[l]=asym
	asymLow[l]=asym
      if asym>asymHigh[l] :
	asymHigh[l]=asym
      if asym<asymLow[l] :
	asymLow[l]=asym

  temp = "High = ["
  for a in asymHigh :
    temp+=str(a)+","
  temp+="]\n"
  f.write(temp)
  
  temp = "Mid = ["
  for a in asymMid :
    temp+=str(a)+","
  temp+="]\n"
  f.write(temp)

  temp = "Low = ["
  for a in asymLow :
    temp+=str(a)+","
  temp+="]\n"
  f.write(temp)
  
  for etarange, asymH, asym, asymL in zip(etabins,asymHigh,asymMid,asymLow) :
    print etarange,asym,"+",asymH-asym,"-",asym-asymL
    
f.close()

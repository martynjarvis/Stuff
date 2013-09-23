#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import commands
import  shutil
  
npdfs = 45
grid_dir = "./grids/45pdfs/"
root_dir = "./ntuples/"
prefix = "wm_lhc7_ct66"

for i in range(npdfs) :
  print "PDF number " + str(i).zfill(2)
  
  gridfile_w321 = grid_dir+prefix+"_w321."+str(i).zfill(2)+".out"
  gridfile_yk = grid_dir+prefix+"_yk."+str(i).zfill(2)+".out"
  
  print "Using gridfiles " + gridfile_w321 + " and " + gridfile_yk
  
  resbos_in = open("./resbos.in", 'w')

  output = "\n".join([
"1,10,20000,50,20000,1234567                     > # runs; iterations; MC even",
"%s                               > Main data grid" % (gridfile_w321),
"%s                               > Y piece grid (same PDF or -)" % (gridfile_yk),
"0, 0, 0, 0, 0, 0                                > iwgt,kKFacP&Y,iYG,iMG,iMM",
"15.0, -2.5, 0.5, 4000.0, 2.5                   > Cuts(1): pTlmin,ymin,DelR,pTlmax,ymax",
"70, 110., 0., 300., -5.0, 5.0                   > Cuts(2):QMn,QMx,QTMn,QTMx,yWmin,yWmax",
"0, 1000, 0.0                                   > Cuts(3):min,max trans. mass, min missing ET",
"1.0, 172.0, 115.0                              > Luminosity (pb^-1), mt,mH",
"ROOTNT1                                         > Output fromat",
"1.0, 400, 0, 5, 0, 0, 0,0                       > qT_Sep, PDF,Proc,Sc,ACut,iSub,iHQApp",
"WW,0                                            > hDecay, i_decay",
"-1,-1                                           > W/Z mass width and width",
"",
"",
"",
""])

  resbos_in.write(output)
  resbos_in.close()

  print "Running"
  
  temp = commands.getstatusoutput("./resbos")
      #Succesful?
  if temp[0] != 0 : #256 is a warning
    print "\tError occured:"
    for line in temp[1].split("\n") :
      print line
    print temp[0]
    break
    
  print "Succesful"
  shutil.move("./resbos.root",root_dir+prefix+"_"+str(i).zfill(2)+".root") #move file
  print "ROOT file made"
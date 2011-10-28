#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import re
import os
import sys
import commands
from sets import Set

path = "./"
path = raw_input("Path? ["+path+"] :\n") 
if path == "" :  path = "./"

temp = commands.getstatusoutput("ls %s" % (path))
#Succesful?
if temp[0] != 0 : 
  print "\tError occured:"
  print temp
  sys.exit()
  
fileRE = re.compile('([a-zA-Z0-9_]+_[0-9]+\.root)')

lines = fileRE.findall(temp[1])

output = []

for line in lines :
  end =  (line.split("_"))[-1]
  line = line.replace(end, "")
  
  output.append(line)
  
outputUnique = Set(output)

n = len(outputUnique)

for i, line in enumerate(outputUnique) :
  oldFile = path+"/"+line+"*.root"
  newFile = path+"/"+line[:-1]+".root"
  print "making file [%i/%i]: %s" % (i+1,n,newFile)
  temp = commands.getstatusoutput("hadd -f %s %s" % (newFile, oldFile))
  if temp[0] != 0 : #Unsuccesful
    print "\tError occured:"
    print temp
    sys.exit()
  else : #Succesful
    temp = commands.getstatusoutput("rm %s" % (path+"/"+line+"*.root"))
    if temp[0] != 0 : #Unsuccesful
      print "\tUnable to delete file: %s" % (path+"/"+line+"*.root")

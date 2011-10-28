#!/usr/bin/env python
import errno

import os
import os.path
import commands
import re
import sys
from copy import deepcopy

header_eq="="*50
header_dash="-"*50

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# def ensure_dir(f):
#     d = os.path.dirname(f)
#     if not os.path.exists(d):
#         os.makedirs(d)

def ensure_dir(path):
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST:
        pass
      else: raise


YourSusyDir = commands.getoutput('echo $SUSY_WORKING_SW_DIR') #Get the susy working Dir
print YourSusyDir
YourScriptsDir = commands.getoutput('pwd')


def BatchRun(samples,analysis,config,outputDir,nFilesPerJob):

    print header_eq
    print "Running Batch Analysis"
    print header_eq
    print "On %d sample(s):" % len(samples)
    for sample in samples:
        print "\t%s " % (sample.Name)
    print header_eq

    #copy contents of file
    folder = YourScriptsDir+"/tmp/"
    ensure_dir(folder) # where we'll put all our files
    filename = sys.argv[0]
    file = open(filename,"r")
    code = file.read()

    #re for things we need to change
    p = re.compile('samples\s?=\s?\[*?.*?\]', re.DOTALL)
    q = re.compile('BatchRun\(*?.*?\)')

    #loop over each suplied sample, then fragment in to subsamples each of 10 files
    for sample in samples:
        tmpSamplePset = deepcopy(sample)
        filesList = list(chunks(sample.File,nFilesPerJob))

        #Loop over fragments of samples
        for files,i in zip(filesList,range(len(filesList))) :
            fragName = sample.Name +"_part"+str(i)
            print "submitting " + folder + fragName + " to batch queue."

            #replace samples in copy of file to fragment samples
            tmpSamplePset.Name = "\"" + fragName + "\""
            tmpSamplePset.File = files
            string = "sample = PSet("
            for (k,v) in  tmpSamplePset._flatten().iteritems() :
               string += "\n\t%s = %s ,"% (k,v)
            string +="\n)"
            string += "\nsamples=[sample]"
            newCode = p.sub(string, code)
            ensure_dir(outputDir+"/"+sample.Name)
            #replace batch run with normal "a.run()"
            string = analysis+".Run( \""+outputDir +sample.Name +"/\"," +config +", samples)"
            newCode = q.sub(string, newCode)

            #write .py
            temp = open(folder+filename[:-3]+analysis+"_"+fragName+".py", 'w')
            temp.write(newCode)
            temp.close()

            #write .sh that we will submit to batch
            temp = open(folder+filename[:-3]+analysis+"_"+fragName+".sh", 'w')
            script = '\n'.join([
                '#!/bin/sh',
                'source '+YourSusyDir+'/setup.sh',#Need to be changed to be more portable
                'cd '+ YourScriptsDir+"/tmp/",# There is a $SUSY_WORKING_DIR path, " how to make python expand this"
                filename[:-3]+analysis+"_"+fragName+".py"
                ])
            temp.write(script)
            temp.close()

            #make executable
            os.chmod(folder+filename[:-3]+analysis+"_"+fragName+".py",0777)

            #Submit
            output = commands.getstatusoutput("qsub -q hep.q " + folder+filename[:-3]+analysis+"_"+fragName+".sh")
            #Succesful?
            if output[0] != 0 :
                print "\tError occured:"
                print output
                break
            else :
                print output[1]


        #make clean up script that
        #hadd root files
        #deletes fragments of root files
        #deletes .py and .sh


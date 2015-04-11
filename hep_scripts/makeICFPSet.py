#!/usr/bin/env python

#Generates psets
#Uses 'lcg-ls' which requires grid to be sourced and a valid grid proxy (voms-proxy-init)
#Does not add the correct crosssections, this will need to be done by hand.

import commands

import configuration_SCBooks as conf,sys,os,readline,getpass,string,fileinput,socket,datetime,re

user = getpass.getuser()
db = conf.lockedDB()
db.connect()

paths=[]
shortNames=[]
xsecs=[]

rows = db.execute('''select job.rowid,state,path,dataset,rpath,node
                     from job join tag on tag.rowid=job.tagid join dset on dset.rowid=job.dsetid
                     where user="'''+user+'''" order by state,path''').fetchall()
for row in rows:
    print ('\t'.join([str(item) for item in row]))[0:90]+"..."
jobnumber = raw_input("\n\n\tWhich job?  ")

for row in rows:
	if jobnumber == str(row['rowid']):
		datasets = (row['dataset']).split(',')
		if len(datasets) > 1 :
			for dset in datasets :
				path = (row['rpath'])+'/'+string.replace(dset[1:], '/', '.')
				paths.append(path)
				shortName = (string.split(dset, '/'))[1] + "_" + (string.split(dset, '/'))[2]
				shortName = string.replace(shortName,'-','_')
				shortNames.append(shortName)
				xsecs.append(0.0)
				#Would be nice if this information was in the database.
		else :
			dset = datasets[0]
			path = (row['rpath'])
			paths.append(path)
			shortName = (string.split(dset, '/'))[1] + "_" + (string.split(dset, '/'))[2]
			shortName = string.replace(shortName,'-','_')
			shortNames.append(shortName)
			xsecs.append(0.0)
		break
db.disconnect()

for path, shortName, xsec in zip(paths, shortNames, xsecs) :
	# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "Generating " + shortName + '.py'
	# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	# print "\tPath: " + path
	
	prefix = '\n' + '\t' +  "\"dcap://gfe02.grid.hep.ph.ic.ac.uk:22128/"# + path + '/'
	suffix = '\" ,'

	temp = commands.getstatusoutput("lcg-ls srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=" + path + "/")# | grep -E SusyCAF_Tree_[0-9]\{1\}[0-9]\{0,1\}[0-9]\{0,1\}_[0-9] -o")

	if temp[0] != 0 :
		print "\tError occured:"
		print temp
		break

	infile = temp[1].split('\n')
	infile.sort()

	toRemove = []
	for i,line1 in enumerate(infile[:-1]) : 
		if (((line1.split('/'))[-1]).split('_'))[2] == (((infile[i+1].split('/'))[-1]).split('_'))[2] :
			#print "\tDuplicates: " + line1
			toRemove.append(i)
		# for line2 in infile[i+1:] :
			# if line1[:-1] == line2[:-1] :

	
	toRemove.sort()
	toRemove.reverse()
	for i in toRemove :
		del infile[i]

	outfile = open(shortName+'.py','w')

	filenames = []
	for line in infile : 
		line = line.rstrip()
		line = prefix + line + suffix 
		filenames.append(line)

	#header
	header = '\n'.join([
		'from icf.core import PSet',
		'',
		'%s=PSet(' % shortName,
		'\tName=\"%s\",' % shortName,
		'\tFormat=(\"ICF\",2),',
		'\tFile=['
		])
	outfile.write(header)

	#body
	for line in filenames :
		outfile.write(line)

	#footer
	footer = '\n'.join([
		'',
		'\t],',
		'\tCrossSection=%d,' % xsec,
		')'
		])
	outfile.write(footer)
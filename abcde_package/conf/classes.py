# -*- coding: utf-8 -*-
# classes.py
# Nicholas Wardle - Imperial College

from selections import *

#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//  
VBTFWP = {'70':WP70(),'80':WP80(),'85':WP85(),'90':WP90(),'95':WP95(),'SC':WPSC(), \
	  '80dEtaIn':WP80dEtaIn(),'80TrckRelIso':WP80TrckRelIso(),'80dPhiIn':WP80dPhiIn(),
	  '80TrckZero':WP80TrckZero()}
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//  
def PrintWelcome():
	print """
//-----------------------------------------------------------------------//
//-----------------------------------------------------------------------//		
//-----	ABCDE Method for W cross-section measurement @ CMS. -------------//
//-----	Author Nicholas Wardle - Imperial College -----------------------//      
//-----	nw709@imperial.ac.uk --------------------------------------------//
//-----------------------------------------------------------------------//	      
//-----	This code is still under development but is intended to be ------//
//-----	user friendly and entirely configuarble from within config ------//
//-----	package.  -------------------------------------------------------//
//-----------------------------------------------------------------------//
//-----------------------------------------------------------------------//
	      """



def PrintHelp(whoisit):
	
	if whoisit == 'WenuAnalyser.py':
	
		print """
			WenuAnalyser.py
			This Code runs over the ntuples produced by the EWK group 
			to fill histograms for the ABCDE Method.
			
			Configuration for this code can be found in conf/analyser_conf.py
			
			the ntuples should be placed in nTupleDir_.
			
			Command Line Arguments:
				
				1  Name   	The Name of the Ntuple to be run over
				
			Options:
				
				-doTnP		Run Tag and probe to produce histograms
						to calculate the efficincy parameter eP
				-doCor		Read in and apply corrections to Tag and 
						probe produced by TagNProbeCalculator.py
				-doTrig=Val	Val should be an integer, A trigger cut
						will be applied based on & with this int
				-help		print this
		      """
		      
	if whoisit == 'QCDAnalyser.py':
	
		print """
			QCDAnalyser.py
			This Code runs over the ntuples produced by the EWK group 
			to fill histograms for the ABCDE Method. (Produces Antiseleciton)
			
			Configuration for this code can be found in conf/analyser_conf.py
			
			the ntuples should be placed in nTupleDir_.
			
			Command Line Arguments:
				
				1  Name   	The Name of the Ntuple to be run over
				
			Options:
				
				-doTrig=Val	Val should be an integer, A trigger cut
						will be applied based on & with this int
				-help		print this
		      """	

	if whoisit == 'ABCDEOptimize.py':
	
		print """
			ABCDEOptimize.py
			This code performs the ABCDE method for Monte Carlo and produces
			2D optimisation plots. It is designed to run over the templates
			produced by WenuAnalyser.py
			
			the templates should be in templates/
			
			this code is configurable from conf/abcde_pars.py
			
			Command Line Arguments:
				
				1  Selection	The Selection Choice to look at. The results
						will also be saved in 'Selection'Plots.
				2  EB/EE        Choose from Barrel or Endcap events
						EB = Barrel
						EE = Endcap
				
			Options:
				
				-help		print this
		      """
	if whoisit == 'ABCDESignal.py':
	
		print """
			ABCDESignal.py
			This code performs the ABCDE method for Monte Carlo and Data.
			It is designed to run over the templates produced by WenuAnalyser.py.
			This Code produces the final result of the method.
			
			the templates should be in templates/
			
			this code is configurable from conf/abcde_pars.py
			
			Command Line Arguments:
				
				1  Selection	The Selection Choice to look at. The results
						will also be saved in 'Selection'Plots.
				
			Options:
				
				-help		print this
		      """				
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//
# A class which contains number crucnhers:
class C_Functions():
  def __init__(self):
    # Need to talk to the C functions
    import array
    self.array = array
    
    try: ROOT
    except NameError:
      import ROOT
      
    ROOT.gROOT.SetBatch(True)	
      
    # Compile the c_funcs
    ROOT.gROOT.ProcessLine(".L conf/c_functions.C++")

    from ROOT import signal
    from ROOT import bias_corr_stat_error
    from ROOT import frac_error	      
     
    self.c_signal 		= signal
    self.c_bias_corr_stat_error = bias_corr_stat_error
    self.c_frac_error		= frac_error
    
  def Signal(self,NA,NB,NC,ND,e_A,e_D,e_W):
     # array to return results:
     ptr = self.array.array('d',[0,0,0,0])
     
     self.c_signal(NA,NB,NC,ND,e_A,e_D,e_W,ptr)
     return ptr[0],ptr[1],ptr[2],ptr[3]
     
  def FracError(self,a,b):
     # array to return results:
     ptr = self.array.array('d',[0])
     
     self.c_frac_error(a,b,ptr)
     return ptr[0]
     
  def BiasCorrStatError(self,Sa,Sb,Sc,Sd,Qa,Qb,Qc,Qd,Scale):
     # array to return results:
     ptr   = self.array.array('d',[0,0])
     
     self.c_bias_corr_stat_error(Sa,Sb,Sc,Sd,Qa,Qb,Qc,Qd,Scale,ptr)
     return ptr[0],ptr[1]
     
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------// 
# The Signal calculation from ABCDE method, Give S = SA+SB+SC+SD
# Returns a tuple, (S1,S2) where S1 is from the assumption eA != eD and S2 from eA=eD

def Signal(NA,NB,NC,ND,e_A,e_D,e_W):

    a = e_W*(e_W-1.)*(e_A-e_D)
    c = float(ND*NB) - float(NA*NC)
    b = (NA+NB+NC+ND)*e_A*e_W + NA - e_A*(NA+NB) - e_W*(NA+ND)

    #return b,(-1*c)
    sd = -1.*c/b
    errd = abs((c/(b*b))*(float(NA+NB+NC+ND)*e_A - float(NA+ND)))

    if abs(a) <  0.001:
      su = sd
      erru = errd

    else:
      b = float(NA)*(1.+e_D*e_W - e_D - e_W) \
    - float(NB)*(e_D -e_D*e_W) \
    + float(NC)*e_A*e_W \
    - float(ND)*(e_W - e_W*e_A)

      # propagation of eW errors on Signal
      dela = (e_D- e_A) + 2*e_W*(e_A-e_D)
      delb = -1*float(NA+ND) + float(NA+NB)*e_D + float(NC+ND)*e_A
      
      if abs(b*b - 4.*a*c) < 0.001:
        su = -1.*b/(2.*a)
        sqr = 0
      else:
        sqr =(b*b - 4.*a*c)**0.5
        su = (-1.*b + sqr)/(2.*a)

      erru = abs(dela*(-1*su/a) - (1./(2*a))*delb + (1.0/(sqr*4 *a))*(2*b*delb - 4*c*dela))

    return su,sd,erru,errd
    

# ----------------------------------------------------------------------------------------------------------------------//
# ----------------------------------------------------------------------------------------------------------------------//

def SignalError_N(NA,NB,NC,ND,e_A,e_W):


    c = float(ND*NB) - float(NA*NC)
    b = -1*((NA+NB+NC+ND)*e_A*e_W + NA - e_A*(NA+NB) - e_W*(NA+ND))
    s = c/b

    dSdNA = ((1-e_W)*(1-e_A)*s 	- NC)/b
    dSdNB = (-1*(1-e_W)*e_A*s 	+ ND)/b
    dSdNC = (e_W*e_A*s 		- NA)/b
    dSdND = (-1*e_W*(1-e_A)*s 	+ NB)/b
    ret = ((dSdNA**2)*NA +(dSdNB**2)*NB +(dSdNC**2)*NC +(dSdND**2)*ND )**0.5
    return ret

# ----------------------------------------------------------------------------------------------------------------------//
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//  
# Define the error on the fraction of two numbers!
def FracError(a,b):

	a = float(a)
	b = float(b)
	c = float(b-a) # b is normally pass+fail
	
	frac = a/b
	try: ROOT
      	except NameError:
          import ROOT
          ROOT.gROOT.SetBatch(True)
	#return frac*(((1./a) + (1./b))**0.5)
	k_ = ROOT.TCanvas('k_','k_',0,0,100,100)
	h_ = ROOT.TH1F('h_','h_',100,frac*0.98,frac*1.02)
	r = ROOT.TRandom3()
	for i in range(50000): 
		ap = r.Poisson(a)
		cp = r.Poisson(c)
		h_.Fill(float(ap)/(ap+cp))
	h_.Fit('gaus','Q','Q')
	return h_.GetFunction('gaus').GetParameter(2)
#---------------------------------------------------------------------------------------------//  
#---------------------------------------------------------------------------------------------//  
def BiasCorrStatError(Sa,Sb,Sc,Sd,Qa,Qb,Qc,Qd,Scale):
	
	try: ROOT
      	except NameError: 
      		import ROOT
      		ROOT.gROOT.SetBatch(True)
      	#Correcton factor will never be too large 
      	ea = float(Sa)/(Sa+Sb)
      	ed = float(Sd)/(Sd+Sc)
      	ew = float(Sa+Sb)/(Sa+Sb+Sd+Sc)
 	st = sum([Sa,Sb,Sc,Sd])
 
 	na = float(Qa + Sa)
      	nb = float(Qb + Sb)
      	nc = float(Qc + Sc)      		
      	nd = float(Qd + Sd)
 	
 	s1,s2,e1,e2 =  Signal(na,nb,nc,nd,ea,ed,ew)
 	cen1 = st/s1
 	cen2 = st/s2
 	
      	tmp_u = ROOT.TH1F('tmp_u','tmp_u',100,cen1*(1-0.01),cen1*(1+0.01)) 
      	tmp_d = ROOT.TH1F('tmp_d','tmp_d',100,cen2*(1-0.01),cen2*(1+0.01))       	
      	rnd = ROOT.TRandom3()
      	
      	ea = float(Sa)/(Sa+Sb)
      	ed = float(Sd)/(Sd+Sc)
      	ew = float(Sa+Sb)/(Sa+Sb+Sd+Sc)
 	st = sum([Sa,Sb,Sc,Sd])
      	
      	for i in range(20001):
      		qa = Scale*rnd.Poisson((1./Scale)*Qa)
      		qb = Scale*rnd.Poisson((1./Scale)*Qb)
      		qc = Scale*rnd.Poisson((1./Scale)*Qc)
      		qd = Scale*rnd.Poisson((1./Scale)*Qd)
      		
      		na = float(qa + Sa)
      		nb = float(qb + Sb)
      		nc = float(qc + Sc)      		
      		nd = float(qd + Sd)
      		
      		su,sd,e1,e2 = \
      		   Signal(na,nb,nc,nd,ea,ed,ew)
      		   
      		tmp_u.Fill(st/su)      		     
      		tmp_d.Fill(st/sd)      		               	
          	
	tmp_u.Fit('gaus','Q','Q')
	tmp_d.Fit('gaus','Q','Q')
	#tmp_u.Draw()
	#raw_input('hoi')
	
	return tmp_u.GetFunction('gaus').GetParameter(2),\
	       tmp_d.GetFunction('gaus').GetParameter(2)
	       
#---------------------------------------------------------------------------------------------//
#---------------------------------------------------------------------------------------------//  
# A little function which makes pretend MC for AB and CD regions 
# based on some overall data corrected template
# MIT templates changed range so we'll just have to chop it off
def CorrectHistos(Pass,Fail,Input):

	try: ROOT
      	except NameError: import ROOT
          
	Total = Pass.Clone()
	Total.Add(Fail)

	# Dont just copy the input, create Pass,Fail
	# Histos and then fill bins with input.
	Nbins = Pass.GetNbinsX()
	OutputPass = ROOT.TH1F(Pass.GetName()+'tmp',Pass.GetName()+'tmp',\
			       Nbins,\
			       Pass.GetBinLowEdge(1),\
			       Pass.GetBinLowEdge(Nbins+1))
			       
	OutputFail = ROOT.TH1F(Fail.GetName()+'tmp',Fail.GetName()+'tmp',\
			       Nbins,\
			       Fail.GetBinLowEdge(1),\
			       Fail.GetBinLowEdge(Nbins+1))
	
	for i in range(1,Nbins+2): # Must include overflow
		OutputPass.SetBinContent(i,Input.GetBinContent(i))
		OutputFail.SetBinContent(i,Input.GetBinContent(i))
	#OutputPass = Input.Clone()
	#OutputFail = Input.Clone()

	RatioPass = Pass.Clone()
	RatioPass.Divide(Total)

	RatioFail = Fail.Clone()
	RatioFail.Divide(Total)

	BI = Input.GetBinWidth(0)
	BP = Pass.GetBinWidth(0)
	
		
	if BI <= BP :	
		OutputPass.Rebin(int(BP//BI))
		OutputFail.Rebin(int(BP//BI))
	else :
		print "Cannot Rebin: \
			Input Width = %s \
			MC width = %s "%(BI,BP)
		return Pass, Fail
	
	OutputPass.Multiply(RatioPass)
	OutputFail.Multiply(RatioFail)

	OutputPass.Scale(Pass.Integral(0,Pass.GetNbinsX()+1)/ \
				       OutputPass.Integral(0, \
				       OutputPass.GetNbinsX()+1))
	OutputFail.Scale(Fail.Integral(0,Fail.GetNbinsX()+1)/ \
				       OutputFail.Integral(0, \
				       OutputFail.GetNbinsX()+1))
	
	return OutputPass, OutputFail

#---------------------------------------------------------------------------------------------//
#---------------------------------------------------------------------------------------------//
# A function which assumes gaussian behaviour and changes width accordingly
def ReResolution(Hist,sc):

      RsMax_ = 55
      
      try: ROOT
      except NameError: import ROOT
      # Hist is going to be a 2D histogram
      NbinsY  = Hist.GetNbinsY()
      HistNew = Hist.Clone()
      for j in range(1,NbinsY+1):
        HistOld = Hist.ProjectionX('proj'+str(j),j,j)
        Nbins   = HistOld.GetNbinsX()
        cen     = HistOld.GetMean()
        oldwid  = HistOld.GetRMS()
        newwid  = oldwid*(1+sc)
	        
	for i in range(1,min(RsMax_,Nbins+2)):
		content = HistOld.GetBinContent(i)
		x	= HistOld.GetBinLowEdge(i)+0.5*\
			  HistOld.GetBinWidth(i)
	 	upscale = ROOT.TMath.Gaus(x,cen,newwid,True)/\
	 		  ROOT.TMath.Gaus(x,cen,oldwid,True)
	 	bin 	= Hist.GetBin(i,j) 
		HistNew.SetBinContent(bin,content*upscale)
	
      HistNew.Scale(Hist.Integral()/HistNew.Integral())
      
      ###################################################
      #c = ROOT.TCanvas('hg','hg',0,0,800,800)
      #ROOT.gROOT.SetStyle('Plain')
      #ROOT.gROOT.SetBatch(False)
      #old = Hist.ProjectionX('p')
      #new = HistNew.ProjectionX('t')
      #old.SetLineWidth(3)
      #new.SetLineWidth(3)
      #new.SetLineColor(4)
      #old.Draw()
      #new.Draw('same')
      #raw_input('aha')
      ###################################################
      
      return HistNew
#---------------------------------------------------------------------------------------------//  	
#---------------------------------------------------------------------------------------------//  
class PyROOTDecorator:
	def __call__(self,f):
		def wrap(init_self,*args,**kwargs):
		  if len(args) != init_self.Nargs: print init_self.__doc__
		  else : return f(init_self,args,**kwargs)
		return wrap

# A python class containing a TMultiGraph 
class PyMultiGraph:

    """
	    PyMultiGraph: A rather specific Use of the TMultiGraph for use with the ABCDE Method
	    Idea is to take python arrays and plot them - one for the X axis and as many as you like for the Y axis
	    
	    Input: PyMultiGraph(Xaxis,Yaxis,Title='PyMultiGraphErrs', Xlabel='X',Ylabel='Y')

	    Xaxis:	A list for the values along X-axis
	    Yaxis:	A list of lists for the Y values (X and each Y should be same dimension) 
	    Title=:	A string for the Title, (optional)
	    Xlabel=:	String for the X-axis label, (optional)
	    Ylabel=:	String for the Y-axis label, (optional)
	    
	    Dependance on following modules:
    		ROOT.TMultiGraph
    		ROOT.TCanvas
    		array.array

    """

    Nargs=2
    @PyROOTDecorator()
    def __init__(self,args,**kwargs):

      Xaxis = args[0]
      Yaxis = args[1]
      #Optional Parameter Defaults
      Title='PyMultiGraph'
      Xlabel='X'
      Ylabel='Y'
      
      try: ROOT
      except NameError:
        import ROOT as root
        self.root = root
        self.root.gROOT.SetBatch(True)

      try: array
      except: import array

      try: self.title = kwargs['Title']
      except KeyError: self.title = str(Title)
      try: self.ylabel = kwargs['Ylabel']
      except KeyError: self.ylabel = str(Ylabel)
      try:  self.xlabel = kwargs['Xlabel']
      except KeyError: self.xlabel = str(Xlabel)
      
      self.MG = self.root.TMultiGraph(self.title, \
                                 self.title)
      
      xaxis = array.array('d',Xaxis)
      try: 			yaxis = [array.array('d', y) for y in Yaxis]
      except TypeError:	yaxis =  [array.array('d',Yaxis)]

      T = ['null' for y in Yaxis]         
      
      for i,y in zip(range(0,len(yaxis)),yaxis):
        T[i] = self.root.TGraph(len(Xaxis),xaxis,y)
	T[i].SetLineColor(i+2)	#Start From Red
        self.MG.Add(T[i])
              
    def Print(self,filename):
      self.C = self.root.TCanvas(self.title, \
                                 self.title,0,0,1600,900)
      self.MG.Draw("AL")
      self.MG.GetXaxis().SetTitle(self.xlabel)
      self.MG.GetYaxis().SetTitle(self.ylabel)
      self.C.SaveAs(str(filename))

#---------------------------------------------------------------------------------------------------------------------//
#---------------------------------------------------------------------------------------------------------------------//


class PyMultiGraphErrs:

    """
    PyMultiGraphErrs: A rather specific Use of the TGraphAsymmErrors for use with the ABCDE Method
    Idea is to take python arrays and plot them - one for the X axis and as many as you like for the Y axis
    
    Input: PyMultiGraph(Xaxis,Yaxis,Yerrsd,Yeersu,Title='PyMultiGraphErrs', Xlabel='X',Ylabel='Y')

    Xaxis:	A list for the values along X-axis
    Yaxis:	A list of lists for the Y values (X and each Y should be same dimension) 
    Yerrsd:	A list of lists the lower bound on the Y values
    Yeersu:	A list on lists the upper bound of the Y values
		The format of a single list (ie not a list of one element) is supported for Y and errs, 
		however the errors and y must be of the same format (eg cannot have [list1,list2],[1,2])
		. If the errors are to be zero for a particular Y axis, then in place of an array of zeros
		one can use a [0]. eg Yaxis = [list1,list2], Yerrsd = [[0],[0]], Yerrsu = [[0,[0]] will plot lists
		1 and 2 with an error band of zero
    Title=:	A string for the Title,
    Xlabel=:	String for the X-axis label
    Ylabel=:	String for the Y-axis label


    Dependance on following modules:
    		ROOT.TMultiGraph
    		ROOT.TGraphAsymmErrors
    		ROOT.TCanvas
    		array.array
    """
    Nargs = 4
    @PyROOTDecorator()
    def __init__(self,args,**kwargs):

      Xaxis = args[0]
      Yaxis = args[1]
      Yerrsd = args[2]
      Yerrsu = args[3]
       #Optional Parameter Defaults
      Title='PyMultiGraphErr'
      Xlabel='X'
      Ylabel='Y'
      Lables='null'
      
      try: ROOT
      except NameError:
        import ROOT as root
        self.root = root
        self.root.gROOT.SetBatch(True)

      try: array
      except: import array

      try: self.title = kwargs['Title']
      except KeyError: self.title = str(Title)
      try: self.ylabel = kwargs['Ylabel']
      except KeyError: self.ylabel = str(Ylabel)
      try:  self.xlabel = kwargs['Xlabel']
      except KeyError: self.xlabel = str(Xlabel)
      try:  self.lables = kwargs['lables']
      except KeyError: self.lables = Lables

      self.MG = self.root.TMultiGraph(self.title, \
                                 self.title)
      self.Leg = self.root.TLegend(0.2,0.65,0.35,0.8)
      self.Leg.SetFillColor(0)
 
      xaxis = array.array('d',Xaxis)
      try :	yaxis = [array.array('d', y) for y in Yaxis]
      except TypeError:	yaxis = [array.array('d', Yaxis)]

      try:	yerrsup = [array.array('d', [abs(s-k) for k,s in zip(y,ya)]) \
      			   for y,ya in zip(Yaxis,Yerrsu)]
      except TypeError:	yerrsup = array.array('d', [abs(s-k) for k,s in zip(Yaxis,Yerrsu)])
      try:	yerrsdown = [array.array('d', [abs(k-s) for k,s in zip(y,ya)]) \
      			   for y,ya in zip(Yaxis,Yerrsd)]
      except TypeError:	yerrsdown = array.array('d', [abs(k-s) for k,s in zip(Yaxis,Yerrsd)])

      T = ['null' for y in Yaxis]         
      zeros = array.array('d',[0 for i in Xaxis])
      almostzeros = array.array('d',[0.01 for i in Xaxis])
      for i,y in zip(range(0,len(yaxis)),yaxis):
        yu = yerrsup[i]
        yd = yerrsdown[i]

        if len(yd) >1:
          T[i] = self.root.TGraphAsymmErrors(len(Xaxis),xaxis,y, \
                                             zeros,zeros,yd,yu)
          T[i].SetFillColor(i+2)	#Start From Red
          T[i].SetFillStyle(3017)
          T[i].SetLineColor(i+2)	#Start From Red
	  T[i].SetLineWidth(3)

        else :
          T[i] = self.root.TGraphAsymmErrors(len(Xaxis),xaxis,y, \
                                             zeros,zeros,almostzeros,almostzeros)
          T[i].SetLineColor(i+2)	#Start From Red
          T[i].SetFillColor(i+2)

        self.MG.Add(T[i])
	if not self.lables == 'null':
		self.Leg.AddEntry(T[i],self.lables[i],'L')

    def Print(self,filename):
      self.C = self.root.TCanvas(self.title, \
                            self.title,0,0,1600,900)
      self.MG.Draw("AL3") #AL3 for band
      self.MG.GetXaxis().SetTitle(self.xlabel)
      self.MG.GetYaxis().SetTitle(self.ylabel)
      if not self.lables == 'null': self.Leg.Draw()
      self.C.SaveAs(str(filename))

#----------------------------------------------------------------------------------------------//
#----------------------------------------------------------------------------------------------//
class Electron:
	
	def __init__(self, pt_,eta_,trckreliso_,ecalreliso_,hcalreliso_,deta_,dphi_,
		     sigieie_,dist_,dcotth_,miss_,hoe_,sceta_,scet_,gsfcharge_):

		self.WorkingPoints = VBTFWP

		self.pt=pt_
		self.eta=abs(eta_)
		self.trckreliso = trckreliso_
		self.ecalreliso = ecalreliso_
		self.hcalreliso = hcalreliso_
		self.deta = abs(deta_)
		self.dphi = abs(dphi_)
		self.sigieie = sigieie_
		self.dist = abs(dist_)
		self.dcotth = abs(dcotth_)
		self.miss = miss_
		self.hoe = hoe_
		self.sceta = abs(sceta_)
		self.scet = scet_
		self.gsfcharge = gsfcharge_

		if abs(self.sceta) < 1.4442:
			self.isEE = 0
			self.isEB = 1
		elif abs(self.sceta) > 1.566 and \
		     abs(self.sceta) < 2.5:
			self.isEE = 1
			self.isEB = 0
		else:
		#     print "Err, not fiducial", self.sceta
		     self.isEE = 0
		     self.isEB = 0	 

	def Print(self):
		print "pt: ",self.pt
		print "eta: ",self.sceta
		print "isEE: ",self.isEE
		print "isEB: ",self.isEB
		print "trckreliso: ", self.trckreliso
		print "ecalreliso: ", self.ecalreliso
		print "hcalreliso: ", self.hcalreliso
		print "deta: ", self.deta
		print "dphi: ", self.dphi
		print "sigieie: ", self.sigieie
		print "dist: ", self.dist
		print "dcotth: ", self.dcotth
		print "miss: ", self.miss
		print "hoe: ", self.hoe
		print "sceta: ", self.sceta
		print "scet: ", self.scet

	def corET(self,run) :
		corr = 1.0
		#EScaleCor=[1.00258,1.00592,1.01212,1.01931,1.03928,1.03389] # NOV4 3_8
		EScaleCor=[0.993988,0.995745,0.999162,1.00794,0.995463,1.00034]# DEC22 3_9
		#if (run<148000)  : EScaleCor=[0.994 ,0.997 ,0.997 ,1.010 ,0.999 ,0.998]
		#elif (run>=148000) : EScaleCor=[0.994 ,0.995 ,0.999 ,1.006 ,0.989 ,1.008]	
		#else : return self.pt	
		etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.5]]
		for bin, etaRange in enumerate(etabins) :
			if abs(self.sceta) > etaRange[0] and abs(self.sceta) < etaRange[1] :
				corr = EScaleCor[bin]
		return self.scet*corr
	
	def corPT(self,run) :
		corr = 1.0
		#EScaleCor=[1.00258,1.00592,1.01212,1.01931,1.03928,1.03389] # NOV4 3_8
		EScaleCor=[0.993988,0.995745,0.999162,1.00794,0.995463,1.00034]# DEC22 3_9
		#if (run<148000)  : EScaleCor=[0.994 ,0.997 ,0.997 ,1.010 ,0.999 ,0.998]
		#elif (run>=148000) : EScaleCor=[0.994 ,0.995 ,0.999 ,1.006 ,0.989 ,1.008]	
		#else : return self.pt
		etabins = [[0.0,0.4],[0.4,0.8],[0.8,1.2],[1.2,1.4],[1.6,2.0],[2.0,2.5]]
		for bin, etaRange in enumerate(etabins) :
		  if abs(self.sceta) > etaRange[0] and abs(self.sceta) < etaRange[1] :
		    corr = EScaleCor[bin]
		return self.pt*corr
	
	def PassFullSelection(self,WP):
		passid = False
		if (abs(self.dist) > self.WorkingPoints[WP].cDist or \
		    abs(self.dcotth) > self.WorkingPoints[WP].cdCotTh) and \
		    (self.miss <= self.WorkingPoints[WP].cmiss):

			if self.isEB == 1:
				if (abs(self.dphi) < self.WorkingPoints[WP].cEB_dPhiIn) and \
				   (abs(self.deta) < self.WorkingPoints[WP].cEB_dEtaIn) and \
				    self.sigieie < self.WorkingPoints[WP].cEB_siEiE and \
				    self.hoe < self.WorkingPoints[WP].cEB_HoE:

					if(self.hcalreliso < self.WorkingPoints[WP].cEB_HcalIso and \
					   self.ecalreliso < self.WorkingPoints[WP].cEB_EcalIso and \
					   self.trckreliso < self.WorkingPoints[WP].cEB_TrckIso):
					  passid = True

			if self.isEE == 1:
				if (abs(self.dphi) < self.WorkingPoints[WP].cEE_dPhiIn) and \
				   (abs(self.deta) < self.WorkingPoints[WP].cEE_dEtaIn and \
				    self.sigieie < self.WorkingPoints[WP].cEE_siEiE and \
				    self.hoe < self.WorkingPoints[WP].cEE_HoE):

					if(self.hcalreliso < self.WorkingPoints[WP].cEE_HcalIso and \
					   self.ecalreliso < self.WorkingPoints[WP].cEE_EcalIso and \
					   self.trckreliso < self.WorkingPoints[WP].cEE_TrckIso):
					  passid = True
		return passid

	def IsFiducial(self):
		if abs(self.eta) < 1.4: return True
		elif abs(self.eta) > 1.6 and abs(self.eta) < 2.4 : return True
		else : return False
#		return self.isEB ==1 or self.isEE ==1
 	
 	# Define a load of specific clauses
	def PassConvRej(self,WP):

		if (abs(self.dist) > self.WorkingPoints[WP].cDist or \
		    abs(self.dcotth) > self.WorkingPoints[WP].cdCotTh) and \
		   (self.miss <= self.WorkingPoints[WP].cmiss):
			return True
		else:
			return False

	def PassIsolation(self,WP):
		if self.isEB == 1:
			if(self.hcalreliso < self.WorkingPoints[WP].cEB_HcalIso and \
			   self.ecalreliso < self.WorkingPoints[WP].cEB_EcalIso and \
			   self.trckreliso < self.WorkingPoints[WP].cEB_TrckIso):
			  return True
		elif self.isEE == 1:
			if(self.hcalreliso < self.WorkingPoints[WP].cEE_HcalIso and \
			   self.ecalreliso < self.WorkingPoints[WP].cEE_EcalIso and \
			   self.trckreliso < self.WorkingPoints[WP].cEE_TrckIso):
			  return True
		else:
			return False
			
	def PassTrckRelIso(self,WP):
		if self.isEB == 1:
			if self.trckreliso < self.WorkingPoints[WP].cEB_TrckIso:
			  return True
		elif self.isEE == 1:
			if self.trckreliso < self.WorkingPoints[WP].cEE_TrckIso:
			  return True
		else:
			return False
			
	def PassHcalRelIso(self,WP):
		if self.isEB == 1:
			if self.hcalreliso < self.WorkingPoints[WP].cEB_HcalIso:
			  return True
		elif self.isEE == 1:
			if self.hcalreliso < self.WorkingPoints[WP].cEE_HcalIso:
			  return True
		else:
			return False

	def PassEcalRelIso(self,WP):
		if self.isEB == 1:
			if self.ecalreliso < self.WorkingPoints[WP].cEB_EcalIso:
			  return True
		elif self.isEE == 1:
			if self.ecalreliso < self.WorkingPoints[WP].cEE_EcalIso:
			  return True
		else:
			return False

	def PassID(self,WP):
		if self.isEB == 1:
			if (abs(self.dphi) < self.WorkingPoints[WP].cEB_dPhiIn) and \
			   (abs(self.deta) < self.WorkingPoints[WP].cEB_dEtaIn) and \
			    self.sigieie < self.WorkingPoints[WP].cEB_siEiE and \
			    self.hoe < self.WorkingPoints[WP].cEB_HoE:
				  return True

		elif self.isEE == 1:
			if (abs(self.dphi) < self.WorkingPoints[WP].cEE_dPhiIn) and \
			   (abs(self.deta) < self.WorkingPoints[WP].cEE_dEtaIn and \
			    self.sigieie < self.WorkingPoints[WP].cEE_siEiE and \
			    self.hoe < self.WorkingPoints[WP].cEE_HoE):
				  return True
		else:
			return False
			
#---------------------------------------------------------------------------------------------//
#---------------------------------------------------------------------------------------------//






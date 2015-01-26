import getopt # command line parser
import sys
from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
import os

#TODO: Add scatter plots,
#output_dir = "/vols/cms03/mjarvis/h2gglobe/Macros/"
output_dir = "/vols/cms03/mjarvis/CMSSW_4_2_8/src/HiggsAnalysis/HiggsTo2photons/h2gglobe/Macros/"

def main():

    shortopts  = "M:C:"
    opts, args = getopt.getopt( sys.argv[1:], shortopts )
    for mass in mass_list:
        for cat in cat_list:
            #mass = 115
            #cat = 0

            #for o, a in opts:
            #    if o in ("-M"):
            #        mass = int(a)
            #    elif o in ("-C", "--cat"):
            #        cat = int(a)
            #if cat<0:
            #    cat = "all"

            for plot in plots:
                name = plot 
                name = name.replace("[CAT]",str(cat))
                name = name.replace("[MASS]",str(mass))
                html = open("./plots/%s.html" % name, 'w')

                #print header index (mass then cat)
                html.write(mass_header)
                for mass_ind in mass_list:
                    output = mass_line.replace("[PLOT]",plot)
                    output = output.replace("[MASS]",str(mass_ind))
                    output = output.replace("[CAT]",str(cat))
                    html.write(output)

                html.write(cat_header)
                for cat_ind in cat_list:
                    output = cat_line.replace("[PLOT]",plot)
                    output = output.replace("[MASS]",str(mass))
                    output = output.replace("[CAT]",str(cat_ind))
                    html.write(output)

                output = template.replace("[PLOT]",plot)
                output = output.replace("[MASS]",str(mass))
                output = output.replace("[CAT]",str(cat))
                html.write(output)
                html.close()
            
            

            outfname = output_dir+"/TMVA_%s_%s.root" % (str(mass),str(cat))
            print outfname
            gROOT.SetMacroPath( "./" )
            gROOT.Macro       ( "./plotall.C(\"%s\")"% outfname )    
            wrong_names = ["CorrelationMatrixS","CorrelationMatrixB","rejBvsS","variables_id_c1"]
            for wrong_name in wrong_names : 
                print "renaming: %s" % wrong_name
                try: 
                    os.rename("./plots/"+wrong_name+".png", "./plots/"+wrong_name+"_"+str(mass)+"_"+str(cat)+".png")
                    os.rename("./plots/"+wrong_name+".pdf", "./plots/"+wrong_name+"_"+str(mass)+"_"+str(cat)+".pdf")
                except:
                    print "FILE DOES NOT EXIST"



    #gApplication.Run() 


mass_header = '''
<html>
<body>
<big>
Mass hypothesis:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
'''
mass_line ='<a href="[PLOT].html">[MASS]</a>&nbsp;&nbsp;&nbsp;\n'
#mass_list = [115,120,121,123,125,130,135,140,150]
mass_list = [123]

cat_header = '''
<br><br>

Category:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
'''
cat_line = '<a href="[PLOT].html">Cat [CAT]</a>&nbsp;&nbsp;&nbsp;\n'
#cat_list = [0,1,2,3,"all"]
cat_list = ["all"]

template = '''
<br><br>

<table border="0">
<tr>
<td>Correlation Matricies:</td>
<td><a href="CorrelationMatrixB_[MASS]_[CAT].html">Background</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="CorrelationMatrixS_[MASS]_[CAT].html">Signal</a>&nbsp;&nbsp;&nbsp;</td>
</tr>

<tr>
<td>MVA Input variables:</td>
<td><a href="variables_id_c1_[MASS]_[CAT].html">Page 1</a>&nbsp;&nbsp;&nbsp;</td>
</tr>

<tr>
<td>Likelihood Outputs:</td>
<td><a href="mva_Likelihood_[MASS]_[CAT].html">Likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="mva_LikelihoodD_[MASS]_[CAT].html">Decorrelated likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="mva_LikelihoodPCA_[MASS]_[CAT].html">PCA-transformed likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="mva_LikelihoodKDE_[MASS]_[CAT].html">Kernel density estimator likelihood</a>&nbsp;&nbsp;&nbsp;</td>
</tr>

<tr>
<td>Likelihood Overtraining:</td>
<td><a href="overtrain_Likelihood_[MASS]_[CAT].html">Likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="overtrain_LikelihoodD_[MASS]_[CAT].html">Decorrelated likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="overtrain_LikelihoodPCA_[MASS]_[CAT].html">PCA-transformed likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="overtrain_LikelihoodKDE_[MASS]_[CAT].html">Kernel density estimator likelihood</a>&nbsp;&nbsp;&nbsp;</td>
</tr>

<tr>
<td>Performance:</td>
<td><a href="rejBvsS_[MASS]_[CAT].html">Bkg Rej, vs Sig Eff.</a>&nbsp;&nbsp;&nbsp;</td>
</tr>
</table> 

<br>
<table border="0">
<tr>
<td>Mass PDF:</td>
<td><a href="Likelihood_[MASS]_[CAT]_refs_c1.html">Likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodD_[MASS]_[CAT]_refs_c1.html">Decorrelated likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodPCA_[MASS]_[CAT]_refs_c1.html">PCA-transformed likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodKDE_[MASS]_[CAT]_refs_c1.html">Kernel density estimator likelihood</a>&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>

<td>BDT PDF:</td>
<td><a href="Likelihood_[MASS]_[CAT]_refs_c2.html">Likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodD_[MASS]_[CAT]_refs_c2.html">Decorrelated likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodPCA_[MASS]_[CAT]_refs_c2.html">PCA-transformed likelihood</a>&nbsp;&nbsp;&nbsp;</td>
<td><a href="LikelihoodKDE_[MASS]_[CAT]_refs_c2.html">Kernel density estimator likelihood</a>&nbsp;&nbsp;&nbsp;</td>
</tr>
</table> 
<br>

<a href="[PLOT].pdf"><img src="[PLOT].png"></a>
</body>
</html>
'''

#<a href="[PLOT].png"><img src="[PLOT].png" width="1400"></a>

plots = ["CorrelationMatrixB_[MASS]_[CAT]", "CorrelationMatrixS_[MASS]_[CAT]",\
"Likelihood_[MASS]_[CAT]_refs_c1","Likelihood_[MASS]_[CAT]_refs_c2",\
"LikelihoodD_[MASS]_[CAT]_refs_c1","LikelihoodD_[MASS]_[CAT]_refs_c2",\
"LikelihoodPCA_[MASS]_[CAT]_refs_c1","LikelihoodPCA_[MASS]_[CAT]_refs_c2",\
"LikelihoodKDE_[MASS]_[CAT]_refs_c1","LikelihoodKDE_[MASS]_[CAT]_refs_c2",\
"mva_Likelihood_[MASS]_[CAT]", "overtrain_Likelihood_[MASS]_[CAT]", 
"mva_LikelihoodD_[MASS]_[CAT]", "overtrain_LikelihoodD_[MASS]_[CAT]", 
"mva_LikelihoodPCA_[MASS]_[CAT]", "overtrain_LikelihoodPCA_[MASS]_[CAT]", 
"mva_LikelihoodKDE_[MASS]_[CAT]", "overtrain_LikelihoodKDE_[MASS]_[CAT]", 
"rejBvsS_[MASS]_[CAT]", "variables_id_c1_[MASS]_[CAT]"]

if __name__ == "__main__":
    main()

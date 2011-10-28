#include "TMath.h"
#include "TH1F.h"
#include "TF1.h"
#include "TRandom3.h"
#include "TCanvas.h"
#include "TStyle.h"
// ------------------------------------------------------------------------------------------------------//
// ------------------------------------------------------------------------------------------------------//
void signal(double NA, double NB, double NC, double ND, 
            double e_A, double e_D, double e_W, double *ret){

	double a = e_W*(e_W-1.)*(e_A-e_D);
    	double c = (ND*NB) - (NA*NC);
   	double b = (NA+NB+NC+ND)*e_A*e_W + NA - e_A*(NA+NB) - e_W*(NA+ND);
   	
   	double sd   = -1*c/b;
   	double errd = fabs((c/(b*b))*((NA+NB+NC+ND)*e_A - (NA+ND)));
   	
   	ret[1] = sd;
   	ret[3] = errd;
   	
   	if(fabs(a) < 0.001){
   	  ret[0] = sd;
   	  ret[2] = errd;
	}
	else{
	
	  b = (NA)*(1.+e_D*e_W - e_D - e_W)
    	    - (NB)*(e_D -e_D*e_W) 
    	    + (NC)*e_A*e_W 
    	    - (ND)*(e_W - e_W*e_A);
	
	  double dela = (e_D- e_A) + 2*e_W*(e_A-e_D);
	  double delb = -1*(NA+ND) + (NA+NB)*e_D + (NC+ND)*e_A;
	
  	  double su;
	  double sqr;
	
	  if(fabs(b*b - 4.*a*c) < 0.001){
          
            su  = -1.*b/(2.*a);
            sqr = 0;
      	  }
      	  else{
            sqr = TMath::Sqrt(b*b - 4.*a*c);
            su  = (-1.*b + sqr)/(2.*a);
	  }
          double erru = fabs(dela*(-1*su/a)
                      - (1./(2*a))*delb 
                      + (1.0/(sqr*4 *a))*(2*b*delb - 4*c*dela));
	  ret[0] = su;
	  ret[2] = erru;
	  
	  // Remember that we always return su,sd,erru,errd
	}
}
// ------------------------------------------------------------------------------------------------------//
// ------------------------------------------------------------------------------------------------------//
void frac_error(double a, double b, double *ret){

	double c = (b-a);
	gStyle->SetOptFit(0011);
	gStyle->SetOptStat(0); 
	TCanvas *can = new TCanvas("can","can",900,600);

	double frac = a/b;
	TH1F *h_    = new TH1F("h_","h_",100,frac*0.98,frac*1.02);
	TRandom3 *r  = new TRandom3();
	
	for(int i=0;i<50000;i++){
	 
	  double ap = r->Poisson(a);
	  double cp = r->Poisson(c);
	  h_->Fill((double)ap/(ap+cp));
	  
	}
	
	h_->Fit("gaus","Q","Q");
		
	h_->Draw();
	can->SaveAs("statEP.png");
	double val = h_->GetFunction("gaus")->GetParameter(2);
	delete h_;
	
	ret[0] = val;
}
// ------------------------------------------------------------------------------------------------------//
// ------------------------------------------------------------------------------------------------------//
void bias_corr_stat_error(double Sa, double Sb, double Sc, double Sd,
		          double Qa, double Qb, double Qc, double Qd, 
		          double Scale, double *ret){
 
      	double ea = (Sa)/(Sa+Sb);
      	double ed = (Sd)/(Sd+Sc);
      	double ew = (Sa+Sb)/(Sa+Sb+Sd+Sc);
 	double st = Sa+Sb+Sc+Sd;
 
 	double na = (Qa + Sa);
      	double nb = (Qb + Sb);
      	double nc = (Qc + Sc);     		
      	double nd = (Qd + Sd);
 	
 	double S[4] = {0,0,0,0};
 	signal(na,nb,nc,nd,ea,ed,ew,S);
 	
 	double s1 = S[0];
 	double s2 = S[2];
 	
 	double cen1 = st/s1;
 	double cen2 = st/s2;
 	
      	TH1F *tmp_u = new TH1F("tmp_u","tmp_u",100,cen1*(1-0.01),cen1*(1+0.01)); 
      	TH1F *tmp_d = new TH1F("tmp_d","tmp_d",100,cen2*(1-0.01),cen2*(1+0.01));
      	
      	TRandom3 *rnd = new TRandom3();
      	      	
      	for(int i=0;i<50000; i++){
      	
      		double qa = Scale*rnd->Poisson((1./Scale)*Qa);
      		double qb = Scale*rnd->Poisson((1./Scale)*Qb);
      		double qc = Scale*rnd->Poisson((1./Scale)*Qc);
      		double qd = Scale*rnd->Poisson((1./Scale)*Qd);
      		
      		na = (qa + Sa);
      		nb = (qb + Sb);
      		nc = (qc + Sc);     		
      		nd = (qd + Sd);
      		
      		signal(na,nb,nc,nd,ea,ed,ew,S);

      		tmp_u->Fill(st/S[0]);      		     
      		tmp_d->Fill(st/S[2]);      		               	
          	
        }
        
	tmp_u->Fit("gaus","Q","Q");
	tmp_d->Fit("gaus","Q","Q");

	double val1 = tmp_u->GetFunction("gaus")->GetParameter(2);
	double val2 = tmp_d->GetFunction("gaus")->GetParameter(2);
	delete tmp_u;
	delete tmp_d;
	
	ret[0] = val1;
	ret[1] = val2;
}
// ------------------------------------------------------------------------------------------------------//
// ------------------------------------------------------------------------------------------------------//
// End

/*
Based on UserCode/Futyan/macros/WenuTemplateFit.cc
See WCharge/scripts/genTemplates.py for an example of how to run the code.
*/

#include "AsymTemplateHistos.hh"
#include "KinSuite.hh"
#include <fstream>

using namespace std;
//using namespace Event;

AsymTemplateHistos::AsymTemplateHistos(const std::string & folderName,
Utils::ParameterSet &pset
):
mFolderName(folderName)
{
	elecET     = pset.Get<double>("ElecET");
	chChk      = pset.Get<bool>("ChCheck");
	lepPtVeto  = pset.Get<double>("ElePtVeto");
	convChk    = pset.Get<bool>("ConvCheck");
	lepVeto    = pset.Get<bool>("EleVeto");	
	wp         = pset.Get<int>("WorkingPoint");
	scEta      = pset.Get<bool>("UseSCEta");
	scEnergy   = pset.Get<bool>("UseSCEnergy");
	CorVersion = pset.Get<int>("CorVersion");
	//(0=95%,1=90%,2=85%,3=80%,4=70%,5=60%)
	ieff=-1;
	if (wp==95) ieff=0;
	if (wp==90) ieff=1;
	if (wp==85) ieff=2;
	if (wp==80) ieff=3;
	if (wp==70) ieff=4;
	if (wp==60) ieff=5;
	if (ieff<0){
		cout<<"Working point "<<wp<<" unknown"<<endl
		<<"Working points accepted are 60,70,80,85,90,95"<<endl
		<<"Job is going to stop"<<endl;
		assert(0);
	} 
	//mMissingHits=0;
	//mDCot=0.02;
	//mDist=0.02;
}

void AsymTemplateHistos::Start(Event::Data & ev) {
	initDir(ev.OutputFile(), mFolderName.c_str());
	BookHistos();
}
AsymTemplateHistos::~AsymTemplateHistos() {

}

/*
~~~BOOK HISTOS~~~
*/
void  AsymTemplateHistos::BookHistos() {
	int nBins = 100;
	for (int ih=0;ih<EtaChBins_;ih++){
		for (int ipt=0; ipt<PtBins; ipt++) {
			TString sel          = "h_pfMET"+etabin[ih]+ptbin[ipt];
			TString antisel      = "h_anti_pfMET"+etabin[ih]+ptbin[ipt];
			TString selcor       = "h_pfMETcor"+etabin[ih]+ptbin[ipt];
			TString antiselcor   = "h_anti_pfMETcor"+etabin[ih]+ptbin[ipt];
			h_sel[ih][ipt]       = new TH1F(sel,sel,nBins,0,100.);
			h_antisel[ih][ipt]   = new TH1F(antisel,antisel,nBins,0,100.);
			h_selcor[ih][ipt]    = new TH1F(selcor    ,selcor    ,nBins,0,100.);
			h_antiselcor[ih][ipt]= new TH1F(antiselcor,antiselcor,nBins,0,100.);	 
		}  
	}   
	for (int ih=0;ih<WptChBins_;ih++){
		for (int ipt=0; ipt<PtBins; ipt++) {
			TString sel= "h_wpt_pfMET"+wptbin[ih]+ptbin[ipt];
			TString antisel= "h_wpt_anti_pfMET"+wptbin[ih]+ptbin[ipt];
			h_wpt_sel[ih][ipt]    = new TH1F(sel,sel,nBins,0,100.);
			h_wpt_antisel[ih][ipt]= new TH1F(antisel,antisel,nBins,0,100.);	 
			//TODO add corrected ET wpt histograms
		}  
	}  
}
/*
~~~PROCESS~~~
*/
bool AsymTemplateHistos::Process(Event::Data & ev) {
	w=ev.GetEventWeight();
	double met = ev.PFMET().Pt();
	double met_phi = ev.PFMET().Phi();
	//ONLY 1 GOOD ELECTRON && VETO ON THE SECOND 
	// int nSel=0;
	int nSelVeto=0;
	int nSelVetoCor=0;
	// std::vector<Lepton const *>::const_iterator goodLep;

	//ANTI EVENT SELECTION
	int nSel[PtBins]={0,0,0};
	int nSelCor[PtBins]={0,0,0};
	//int nVetoSel[PtBins]={0,0,0};
	int nAntiSel[PtBins]={0,0,0};
	int nAntiSelCor[PtBins]={0,0,0};

	// std::vector<Lepton const *>::const_iterator dfiLep[AntiEvBins];
	// std::vector<Lepton const *>::const_iterator dhiLep[AntiEvBins];
	
	std::vector<Lepton const *>::const_iterator goodLepCor[PtBins];
	std::vector<Lepton const *>::const_iterator goodLep[PtBins];
	
	std::vector<Lepton const *>::const_iterator antiLepCor[PtBins];
	std::vector<Lepton const *>::const_iterator antiLep[PtBins];

	for (std::vector<Lepton const *>::const_iterator lep=ev.LD_CommonElectrons().accepted.begin();  lep != ev.LD_CommonElectrons().accepted.end();  ++lep) {
		//Selection
		int i = (*lep)->GetIndex();	
		double eta = (scEta)    ? ev.GetElectronESuperClusterEta(i) : (*lep)->Eta();
		//double Et  = (scEnergy) ? ev.GetElectronESuperClusterOverP(i)*ev.GetElectronTrkPt(i) : (*lep)->Et();
		double Et  = (scEnergy) ? ev.GetElectronEcalEnergy(i)/cosh(eta) : (*lep)->Et();
		double corEt = cor(Et,eta,ev.RunNumber());

		if (!fid(eta)) continue;
		bool chargeOk = (chChk) ? (((*lep)->GetCharge()==ev.GetElectronSCCharge(i)) && ((*lep)->GetCharge()==ev.GetElectronKFCharge(i))) : true;
		bool convOk = (convChk) ? (passConv(ev.GetElectronGsfTrackTrackerExpectedHitsInner(i) , ev.GetElectronDCot(i), ev.GetElectronDist(i), ieff) ) : true; 
		bool iso = passIsolation((*lep)->GetTrkIsolation()/(*lep)->Pt(), (*lep)->GetEcalIsolation()/(*lep)->Pt(), (*lep)->GetHcalIsolation()/(*lep)->Pt(),eta,ieff);
		bool id = passID(ev.GetElectronSigmaIetaIeta(i), ev.GetElectronDeltaPhiAtVtx(i), ev.GetElectronDeltaEtaAtVtx(i), ev.GetElectronHoE(i),eta,ieff);

		bool veto_convOk = (convChk) ? (passConv(ev.GetElectronGsfTrackTrackerExpectedHitsInner(i) , ev.GetElectronDCot(i), ev.GetElectronDist(i), 0) ) : true; 
		bool veto_iso = passIsolation((*lep)->GetTrkIsolation()/(*lep)->Pt(), (*lep)->GetEcalIsolation()/(*lep)->Pt(), (*lep)->GetHcalIsolation()/(*lep)->Pt(),eta,0);
		bool veto_id = passID(ev.GetElectronSigmaIetaIeta(i), ev.GetElectronDeltaPhiAtVtx(i), ev.GetElectronDeltaEtaAtVtx(i), ev.GetElectronHoE(i),eta,0);
		
		if (iso && id && chargeOk && convOk){
			for (int ipt=0;ipt<PtBins;ipt++){ 
				if (Et>ptcut[ipt]){
					nSel[ipt]++;
					goodLep[ipt]=lep;
				}
				if (corEt>ptcut[ipt]){
					nSelCor[ipt]++;
					goodLepCor[ipt]=lep;
				}
			}
		}
		if (veto_iso && veto_id && veto_convOk){
			if (Et   >lepPtVeto) nSelVeto++;
			if (corEt>lepPtVeto) nSelVetoCor++;
		}
		
		// David's anti-selection
		// Pass WP80 :
		// no Conversion rejection
		// All Isolation cuts
		// Electron ID (only H/E cut)
		// Anti WP90/85 (Deta/Dphi)
		// Deta > 0.007/0.009 (EB/EE)
		// Dphi > 0.06/0.04  (EB/EE)

		bool AS_convOk = true;//(convChk) ? (passConv(ev.GetElectronGsfTrackTrackerExpectedHitsInner(i) , ev.GetElectronDCot(i), ev.GetElectronDist(i), 0) ) : true; //Removed cut
		bool AS_iso = passIsolation((*lep)->GetTrkIsolation()/(*lep)->Pt(), (*lep)->GetEcalIsolation()/(*lep)->Pt(), (*lep)->GetHcalIsolation()/(*lep)->Pt(),eta,3);//3 = WP80
		bool AS_id = passID(0., 0., 0., ev.GetElectronHoE(i),eta,3);//3 = WP80 //only HoE
		bool pass_dfi = passID_AS (ev.GetElectronDeltaPhiAtVtx(i), 0., eta ,as_dphi);
		bool pass_dhi = passID_AS (0., ev.GetElectronDeltaEtaAtVtx(i), eta ,as_deta);
		
		for (int ipt=0;ipt<PtBins;ipt++){ 
			if (Et>ptcut[ipt]){
				if (AS_convOk && AS_iso && AS_id && (!pass_dfi) && (!pass_dhi)){
					nAntiSel[ipt]++;
					antiLep[ipt]=lep;
				}
			}
			if (corEt>ptcut[ipt]){
				if (AS_convOk && AS_iso && AS_id && (!pass_dfi) && (!pass_dhi)){
					nAntiSelCor[ipt]++;
					antiLepCor[ipt]=lep;
				}
			}
		}
	}
	//TDirectory *currentDirectory= ev.OutputFile()->GetDirectory(mFolderName.c_str());	
	for (int ipt=0;ipt<PtBins;ipt++){ //Loop over Pt Bins
		//Uncorrected
		if ((nSel[ipt]==1)&&(nSelVeto==1)){
		  	int ih = getEta(goodLep[ipt]);	
			int iwpt = getWpt(goodLep[ipt],met,met_phi);
			h_sel[0][ipt]->Fill(met,w);
			if (ih>0) h_sel[ih][ipt]->Fill(met,w);
			if (iwpt>0) h_wpt_sel[iwpt][ipt]->Fill(met,w);
		}
		if (nAntiSel[ipt]==1){
		        int ih = getEta(antiLep[ipt]);	
			int iwpt = getWpt(antiLep[ipt],met,met_phi);
			h_antisel[0][ipt]->Fill(met,w);
			if (ih>0) h_antisel[ih][ipt]->Fill(met,w);
			if (iwpt>0) h_wpt_antisel[iwpt][ipt]->Fill(met,w);
		}
		//Corrected //TODO add corrected ET wpt histograms
		if ((nSelCor[ipt]==1)&&(nSelVetoCor==1)){
		        int ih = getEta(goodLepCor[ipt]);	
			int iwpt = getWpt(goodLepCor[ipt],met,met_phi);
			if (ipt == 0) { cout<<"RUN= "<<ev.RunNumber()<<" LUMIS= "<<ev.LumiSection()<<" EVENT= "<<ev.EventNumber()<<endl;}
			h_selcor[0][ipt]->Fill(met,w);
			if (ih>0) h_selcor[ih][ipt]->Fill(met,w);
			//if (iwpt>0) h_wpt_sel[iwpt][ipt]->Fill(met,w);
		}
		if (nAntiSelCor[ipt]==1){
		  	int ih = getEta(antiLepCor[ipt]);	
			int iwpt = getWpt(antiLepCor[ipt],met,met_phi);
			h_antiselcor[0][ipt]->Fill(met,w);
			if (ih>0) h_antiselcor[ih][ipt]->Fill(met,w);
			//if (iwpt>0) h_wpt_antisel[iwpt][ipt]->Fill(met,w);
		}
	}
	return true;
} // end of Process method

std::ostream& AsymTemplateHistos::Description(std::ostream &ostrm) {
	ostrm << "AsymTemplateHistos plots made here: (histograms in ";
	ostrm << mFolderName << ")";
	return ostrm;
}

bool AsymTemplateHistos::passIsolation (double track, double ecal, double hcal, double eta, int ieff)
{
	return CheckCuts(track, ecal, hcal, 0., 0., 0., 0.,  eta, ieff ); 
}

bool AsymTemplateHistos::passID (double sihih, double dfi, double dhi,double hoe, double eta, int ieff)
{
	return CheckCuts(0., 0., 0., sihih, dfi, dhi, hoe,  eta, ieff );
}

bool AsymTemplateHistos::passConv (int v_missHits, double v_DCot, double v_Dist, int ieff)
{
	if ((v_missHits <= MissHits_[ieff]) && 
			(fabs(v_DCot) > DCot_[ieff] || fabs(v_Dist) >  Dist_[ieff]) ) return true;
	return false;
}

bool AsymTemplateHistos::passID_AS(double v_dfi, double v_dhi, double eta, int ieff){
	if (fabs(eta)< 1.479) {	  
		if (
				fabs(v_dfi) < Dphi_[ieff] && fabs(v_dhi) < Deta_[ieff] ) return true;
	}
	else {
		if (fabs(v_dfi) < Dphi_ee_[ieff] && fabs(v_dhi) < Deta_ee_[ieff] ) return true;
	}
	return false;
}

bool AsymTemplateHistos::fid(double eta) {
	return  (fabs(eta)<2.4 && (  fabs(eta) < 1.4  || fabs(eta) > 1.6 ));//(  fabs(eta) < 1.4442  || fabs(eta) > 1.56 ));
}

int AsymTemplateHistos::getEta(std::vector<Lepton const *>::const_iterator lep){
	//cout<<"test1"<<endl;
	double eta= (*lep)->Eta();
	double charge = (*lep)->GetCharge();
	//double pt= (*lep)->Pt();
	bool acc= (((fabs(eta)<1.6)&&(fabs(eta)>1.4))|| (fabs(eta)>2.4));
	bool cha = (charge==0);
	//cout<<"test2"<<endl;
	int ih = -1;
	for (int ieta=0;ieta<EtaBins;ieta++){ 
		if (fabs(eta)<etabinup[ieta]){
			ih = ieta+1; // bin 0 is inclusive bin
			break;
		}
	}
	//cout<<"test3"<<endl;
	if (ih < 0) return -1; // no eta bin found
	if (cha)    return -1;
	if (acc)    return -1;
	if (charge<0) ih+=EtaBins; // positive bins go 1,2,3,4,5,6, negative go 7,8,9,10,11,12
	//cout<<"test4"<<endl;
	return ih;
}

int AsymTemplateHistos::getWpt(std::vector<Lepton const *>::const_iterator lep, double met, double met_phi){
	double charge = (*lep)->GetCharge();
	double pt= (*lep)->Pt();
	int wpt = -1;
	for (int iwpt=0;iwpt<WptBins;iwpt++){ 
		double measured_Wpt = sqrt(met*met+pt*pt+pt*met*cos(met_phi-(*lep)->Phi()));
		if (measured_Wpt>wptbinlow[iwpt]){
			wpt = iwpt; // note: no +1 since we do not have an inclusive bin here
			//note : no break since these are the lower bin edges
		}
	}
	if (wpt < 0) return -1; // no wpt bin found (should be impossible)
	if (charge<0) wpt+=WptBins; // positive bins go 0,1,2,3,4, negative go 5,6,7,8,9	
	return wpt;
}

double AsymTemplateHistos::cor(double et,double eta,int runNumber){
	int ih = -1;
	for (int ieta=0;ieta<EtaBins;ieta++){ 
		if (fabs(eta)<etabinup[ieta]){
			ih = ieta;
			break;
		}
	}
	if (CorVersion == 0) return et*Sca_38_[ih];
	else if (CorVersion == 1 && runNumber<148000) return et*Sca_39_p1_[ih];
	else if (CorVersion == 1 && runNumber>=148000) return et*Sca_39_p2_[ih];
	else return et;
}

bool AsymTemplateHistos::CheckCuts(double v_trk, double v_ecal, double v_hcal, 
double v_sihih, double v_dfi, double v_dhi, double v_hoe,
double eta, int ieff){
	if (fabs(eta)< 1.479) {	  
		if (
				v_trk  <  Trk_[ieff]    && 
				v_ecal <  Ecal_[ieff]   &&
				v_hcal <  Hcal_[ieff]   &&
				v_sihih < sihih_[ieff]  &&
				fabs(v_dfi) < Dphi_[ieff]   &&
				fabs(v_dhi) < Deta_[ieff]   &&
				fabs(v_hoe)< HoE_[ieff]    
				) return true;
	}
	else {
		if (v_trk <  Trk_ee_[ieff] && 
				v_ecal < Ecal_ee_[ieff] &&
				v_hcal < Hcal_ee_[ieff] &&
				v_sihih <sihih_ee_[ieff] &&
				fabs(v_dfi) <Dphi_ee_[ieff] &&
				//MICHELE DA SCOMMENTARE   
				fabs(v_dhi) <Deta_ee_[ieff] &&
				fabs(v_hoe)< HoE_ee_[ieff] 
				) return true;
	}
	return false;
}


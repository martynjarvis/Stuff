#ifndef AsymTemplateHistos_h
#define AsymTemplateHistos_h

#include "TH1D.h"
#include "TH2D.h"
#include "EventData.hh"
#include "Operation.hh"
#include "PlottingBase.hh"
#include "Utils.hh"

using namespace Event;
const static int PtBins=3;

const static int EtaBins = 6;
const static int EtaChBins_=EtaBins*2+1;

const static int WptBins = 5;
const static int WptChBins_ = WptBins*2;

// Anti WP90/85 (Deta/Dphi)
// Deta > 0.007/0.009 (EB/EE)
// Dphi > 0.06/0.04  (EB/EE)


//const double Sca_38_[EtaBins]    = {0.9996,1.0027,1.0091,1.0165,1.0370,1.0331}; old
const double Sca_38_[EtaBins]    = {1.00258,1.00592,1.01212,1.01931,1.03928,1.03389};
const double Sca_39_p1_[EtaBins] = {0.994 ,0.997 ,0.997 ,1.010 ,0.999 ,0.998 }; //Before 148000
const double Sca_39_p2_[EtaBins] = {0.994 ,0.995 ,0.999 ,1.006 ,0.989 ,1.008 }; //After and including 148000

const static int as_dphi = 2;
const static int as_deta = 1;

//(95%,90%,85%,80%,70%,60%)

 const int AntiEvBins_ = 6;

const int MissHits_[AntiEvBins_] = {1,1,1,0,0,0};
const double DCot_[AntiEvBins_] = {0.0, 0.02, 0.02, 0.02, 0.02, 0.02};
const double Dist_[AntiEvBins_] = {0.0, 0.02, 0.02, 0.02, 0.02, 0.02};

const double Trk_[AntiEvBins_] = {0.15,0.12,0.09,0.09,0.05,0.04};
const double Ecal_[AntiEvBins_] = {2.00,0.09,0.08,0.07,0.06,0.04};
const double Hcal_[AntiEvBins_] = {0.12,0.10,0.10,0.10,0.03,0.03};
const double sihih_[AntiEvBins_] = {0.01,0.01,0.01,0.01,0.01,0.01};  
const double Dphi_[AntiEvBins_] = {0.8,0.8,0.06,0.06,0.03,0.025};
const double Deta_[AntiEvBins_] = {0.007,0.007,0.006,0.004,0.004,0.004};
const double HoE_[AntiEvBins_] = {0.5,0.12,0.04,0.04,0.025,0.025};

const double Trk_ee_[AntiEvBins_] = {0.08,0.05,0.05,0.04,0.025,0.025};
const double Ecal_ee_[AntiEvBins_] = {0.06,0.06,0.05,0.05,0.025,0.02};
const double Hcal_ee_[AntiEvBins_] = {0.05,0.03,0.025,0.025,0.02,0.02};
const double sihih_ee_[AntiEvBins_] = {0.03,0.03,0.03,0.03,0.03,0.03};
const double Dphi_ee_[AntiEvBins_] = {0.7,0.7,0.04,0.03,0.02,0.02};
const double Deta_ee_[AntiEvBins_] = {0.01,0.009,0.007,0.007,0.005,0.005};
const double HoE_ee_[AntiEvBins_] = {0.07,0.05,0.025,0.025,0.025,0.025};

const double etabinup[EtaBins] = {0.4,0.8,1.2,1.6,2.0,2.4};//Note: this is the upper bin edge 
const TString etabin[EtaChBins_]={"",
	"_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos",
	"_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg"};

const double wptbinlow[WptBins] = {0,5,10,20,50};//Note: this is the lower bin edge 
const TString wptbin[WptChBins_]={"_wpt1_pos","_wpt2_pos","_wpt3_pos","_wpt4_pos","_wpt5_pos",
	"_wpt1_neg","_wpt2_neg","_wpt3_neg","_wpt4_neg","_wpt5_neg"};

const double ptcut[PtBins] = {25.,30.,35.};
const TString ptbin[PtBins]={"","_30","_35"};


class AsymTemplateHistos : public PlottingBase {
public:
	// Standard Operation methods.
	AsymTemplateHistos(const std::string & filename,
	Utils::ParameterSet &);
	~AsymTemplateHistos(); //!< Destructor.

	void Start(Event::Data & ev); //!< Start processing
	bool Process(Event::Data & ev); //!< Processes the event, returning true if it passes the operation.

	std::ostream& Description(std::ostream& ostrm); //!< Describes the operation, for analysis output to terminal/log file.
	void BookHistos();
	bool passIsolation (double track, double ecal, double hcal, double eta, int ieff);
	bool passID (double sihih, double dfi, double dhi,double hoe, double eta, int ieff);
	bool passConv (int v_missHits, double v_DCot, double v_Dist, int ieff);
	bool passID_AS(double v_dfi, double v_dhi, double eta, int ieff);  
	bool fid(double eta);
	int getEta(std::vector<Lepton const *>::const_iterator lep);
	int getWpt(std::vector<Lepton const *>::const_iterator lep, double met, double met_phi);
	double cor(double et,double eta,int runNumber);
	bool CheckCuts(double v_trk,double v_ecal,double v_hcal,double v_sihih,double v_dfi,double v_dhi,double v_hoe,double eta,int ieff);

private:
	std::string mFolderName;
	double elecET;
	TH1F * h_antisel[EtaChBins_][PtBins];
	TH1F * h_sel[EtaChBins_][PtBins]; 
	TH1F * h_selcor[EtaChBins_][PtBins];
	TH1F * h_antiselcor[EtaChBins_][PtBins];
	TH1F * h_wpt_sel[WptChBins_][PtBins];
	TH1F * h_wpt_antisel[WptChBins_][PtBins];
	bool chChk;
	bool convChk;
	bool lepVeto;
	double lepPtVeto;
	int wp;
	bool scEta;
	bool scEnergy;
	int ieff;
	double w;
	int CorVersion;
}; //
#endif








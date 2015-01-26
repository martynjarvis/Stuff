#include <vector>
#include <sstream>
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TGraph.h"
#include "TLegend.h"
#include "TProfile.h"
#include "TF1.h"
#include "TMath.h"
#include "TRandom1.h"
//#include "/home/pharris/Analysis/W/condor/run/CMSSW_3_8_4/src/MitWlnu/NYStyle/test/NYStyle.h"
#include "RecoilCorrector.hh"


//The MC sample to be corrected.
//TFile *fZMCFile = new TFile("../RecoilNtuples/Recoil_DYToEE_M_20_TuneZ2_7TeV_pythia6_Spring11_PU_S1_START311_V1G1_v1.root");
TFile *fZMCFile = new TFile("./ntuple_Wp.root");
TTree *fZMCTree = (TTree*) fZMCFile->FindObjectAny("FitRecoil");

//The data file to be compared to
//TFile *fDataFile = new TFile("../RecoilNtuples/Recoil_SingleElectron_Run2011A.root");
TFile *fDataFile = new TFile("./ntuple_dataWp.root");
TTree *fZDataTree = (TTree*) fDataFile->FindObjectAny("FitRecoil"); 

//The templates used in the correction
void corrector_v2(int iNJet=-1,std::string iNameZDat = "recoilfits/recoil_data.root",
		  std::string iNameZMC  = "recoilfits/recoil_Z.root",
		  std::string iNameWMC  = "recoilfits/recoil_Wp.root") { 
  RecoilCorrector corrector1(iNameWMC);        // W events
  //RecoilCorrector corrector1(iNameZMC);      // Z events 
  corrector1.addMCFile      (iNameZMC);
  corrector1.addDataFile    (iNameZDat);

  float lGenPt = 0; float lGenPhi = 0; float lLepPt = 0; float lLepPhi = 0; float lMet = 0; float lMPhi = 0; int lNJet = 0; float lWeight = 0; int lState = 0; float lEta = 0; float lLepPhi1 = 0; float lLepPhi2 = 0; float lLepPt1 = 0; float lLepPt2 = 0; float lTKMet = 0; float lTKMPhi = 0;
  fZMCTree->SetBranchAddress("genpt"       ,&lGenPt); float lMass = 0;
  fZMCTree->SetBranchAddress("genphi"      ,&lGenPhi);
  fZMCTree->SetBranchAddress("leppt"       ,&lLepPt);
  fZMCTree->SetBranchAddress("lepphi"      ,&lLepPhi);
  fZMCTree->SetBranchAddress("pfmet"       ,&lMet);
  fZMCTree->SetBranchAddress("pfmetphi"    ,&lMPhi);
  fZMCTree->SetBranchAddress("trkmet"      ,&lTKMet);
  fZMCTree->SetBranchAddress("trkmetphi"   ,&lTKMPhi);
  fZMCTree->SetBranchAddress("njet"        ,&lNJet);
  fZMCTree->SetBranchAddress("weight"      ,&lWeight);
  fZMCTree->SetBranchAddress("mass"        ,&lMass);

  TFile *lOFile = new TFile("dy_select_corr.root","RECREATE"); lOFile->cd();
  TTree *lTree = new TTree("Events","Events");
  int lFNJet = 0; float lFMet = 0; float lFPt = 0; float lFWeight = 0; float lFU1 = 0; float lFU2 = 0; float lNMet = 0; float lFState = 0; float lFEta = 0; float lFLepPhi1 = 0; float lFLepPhi2 = 0; float lFMPhi = 0; float lFTKMet = 0; float lFTKMPhi = 0; float lFLepPt1 = 0; float lFLepPt2 = 0; float lFMass = 0; float lFLepPhi = 0;
  lTree->Branch("njet"  ,&lFNJet    ,"lNJet/I");
  lTree->Branch("pfmet" ,&lFMet     ,"lFMet/F");
  lTree->Branch("pfmetphi"  ,&lFMPhi    ,"lFMPhi/F");
  lTree->Branch("trkmet" ,&lFTKMet   ,"lFTKMet/F");
  lTree->Branch("trkmetphi",&lFTKMPhi  ,"lFTKMPhi/F");
  lTree->Branch("pt"    ,&lFPt      ,"lFPt/F");
  lTree->Branch("phi"  ,&lFLepPhi ,"lFLepPhi/F");
  //lTree->Branch("phi1"  ,&lFLepPhi1 ,"lFLepPhi1/F");
  //lTree->Branch("phi2"  ,&lFLepPhi2 ,"lFLepPhi2/F");
  //lTree->Branch("pt1"   ,&lFLepPt1  ,"lFLepPt1/F");
  //lTree->Branch("pt2"   ,&lFLepPt2  ,"lFLepPt2/F");
  lTree->Branch("pfu1"    ,&lFU1      ,"lFU1/F");
  lTree->Branch("pfu2"    ,&lFU2      ,"lFU2/F");
  lTree->Branch("eta"   ,&lFEta     ,"lFEta/F");
  lTree->Branch("weight",&lFWeight  ,"lFWeight/F");
  //lTree->Branch("state" ,&lFState   ,"lFState/I");
  lTree->Branch("mass"  ,&lFMass   ,"lFMass/F");

  TH1F* lDMet = new TH1F("dMET","dMET"   ,100,0,100); lDMet->Sumw2();  lDMet->SetMarkerStyle(kFullCircle); lDMet->SetLineWidth(1);
  TH1F* lMMet0 = new TH1F("mMET0","mMET0",100,0,100); lMMet0->Sumw2(); lMMet0->SetLineColor(kRed); lMMet0->SetLineWidth(1);
  TH1F* lMMet1 = new TH1F("mMET1","mMET1",100,0,100); lMMet1->Sumw2(); lMMet1->SetLineColor(kBlue); lMMet1->SetLineWidth(1);
  TH1F* lMMet2 = new TH1F("mMET2","mMET2",100,0,100); lMMet2->Sumw2(); lMMet2->SetLineColor(kOrange); lMMet2->SetLineWidth(1);
  TH1F* lMMet3 = new TH1F("mMET3","mMET3",100,0,100); lMMet3->Sumw2(); lMMet3->SetLineColor(kViolet); lMMet3->SetLineWidth(1);

  int lN = 1;  //Number of iterations ===> To increase stats (be careful with this)
  for(int i0 = 0; i0 < fZMCTree->GetEntries(); i0++) {//Loop W MC events
    fZMCTree->GetEntry(i0);//get entry from tree
    if(iNJet != lNJet && iNJet != -1) continue;//cut on njets....
    //set pointers for output from corrector
    //lNMet = pMet;
    double pMet     = lMet;
    double pPFMet0 = lMet;   
    double pPFMet1 = lMet;  
    double pPFMet2 = lMet;  
    double pPFMPhi0 = lMPhi;
    double pPFMPhi1 = lMPhi;
    double pPFMPhi2 = lMPhi;
    if(lLepPt > 0) lMMet0->Fill(pMet);
    
    //Fill output tree 
    lFMass   = lMass;
    //lGenPt  = lLepPt;  
    //lGenPhi = lLepPhi; 
    lFEta    = lEta;
    lFPt     = lLepPt;
    lFNJet   = lNJet;
    lFWeight = lWeight/lN;//*lWH->GetBinContent(lWH->FindBin(lGenPt));
    lFState   = lState;
    lFLepPhi  = lLepPhi;
    lFLepPhi1 = lLepPhi1;
    lFLepPhi2 = lLepPhi2;
    lFLepPt1  = lLepPt1;
    lFLepPt2  = lLepPt2;

    for(int i1 = 0; i1 < lN; i1++) { //not sure why we might wish to apply this iterativly
        //it seems as though u1... etc should be empty pointers, not derived.
        // the only things that need to be passes are met,metphi as pointers and,genpt,genphi,leppt,lepphi
      double pU1 = 0; double pU2 = 0; double pU21 = 0; double pU22 = 0; double pU11 = 0; double pU12 = 0;
      corrector1.CorrectAll(pPFMet0,pPFMPhi0,lGenPt,lGenPhi,lLepPt,lLepPhi, pU1, pU2, 0);
      corrector1.CorrectAll(pPFMet1,pPFMPhi1,lGenPt,lGenPhi,lLepPt,lLepPhi,pU11,pU12, 1);   //High Uncertainty
      corrector1.CorrectAll(pPFMet2,pPFMPhi2,lGenPt,lGenPhi,lLepPt,lLepPhi,pU21,pU22,-1);  //Low  Uncertainty
      lFMet    = pPFMet0;
      lFMPhi   = pPFMPhi0;
      lFU1     = pU1;
      lFU2     = pU2;
      if(lLepPt > 0) lMMet1->Fill(pPFMet0,lWeight);
      if(lLepPt > 0) lMMet2->Fill(pPFMet1,lWeight);
      if(lLepPt > 0) lMMet3->Fill(pPFMet2,lWeight);
      lTree->Fill();
    }
  }
  lTree->Write();

  TCanvas *lC0 = new TCanvas("c0","c0",800,600); lC0->cd(); 
  //lC0->SetLogy();
  std::stringstream lSNJet; 
  if(iNJet == -1) lSNJet << "njet > -1";
  if(iNJet != -1) lSNJet << " njet == " << iNJet;
  fZDataTree->Draw("pfmet>>dMET",lSNJet.str().c_str());//&& nbtag == 0");
  
  TLegend *lL = new TLegend(0.6,0.6,0.9,0.9); lL->SetFillColor(0); lL->SetBorderSize(0);
  lL->AddEntry(lDMet,"data","lp");
  lL->AddEntry(lMMet0,"MC","l");       lMMet0->SetMarkerStyle(kFullCircle); lMMet0->SetMarkerColor(kRed);
  lL->AddEntry(lMMet1,"MC corrected","lp"); 
  lL->AddEntry(lMMet2,"MC +#sigma","lp"); 
  lL->AddEntry(lMMet3,"MC -#sigma","lp"); 

  lDMet->Scale(1./lDMet->Integral());
  lMMet0->Scale(1./lMMet0->Integral());
  lMMet1->Scale(1./lMMet1->Integral());
  lMMet2->Scale(1./lMMet2->Integral());
  lMMet3->Scale(1./lMMet3->Integral());
  lDMet->Scale(lMMet1->Integral(40,100)/lDMet->Integral(40,100));



  //lDMet->GetYaxis()->SetRangeUser(0.00001,1.);
  lDMet->GetYaxis()->SetRangeUser(0.,0.1);//Use this if not using a log y axis
  lDMet->GetXaxis()->SetTitle("#slash{E_{T}} (GeV)");
  lDMet->Draw("EP");
  lMMet0->Draw(" hist sames");
  lMMet1->Draw(" hist sames");
  lMMet2->Draw(" hist sames");
  lMMet3->Draw(" hist sames");
  lL->Draw();
}

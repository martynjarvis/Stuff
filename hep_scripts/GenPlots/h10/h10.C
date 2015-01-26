#define h10_cxx
// The class definition in h10.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.

// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// Root > T->Process("h10.C")
// Root > T->Process("h10.C","some options")
// Root > T->Process("h10.C+")
//

#include "h10.h"
#include <TH2.h>
#include <TStyle.h>


void h10::Begin(TTree * /*tree*/)
{
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).


  TString option = GetOption();
  if (option.Contains("m")){
    _charge = -1;
  }
  else if (option.Contains("p")){
    _charge = 1;
  }

  lep_ET = 35.;
  int nBins = 100;

  std::string WNew = "./Recoil_SingleElectron.root";
  std::string ZDat = "./Recoil_SingleElectron.root";
  std::string ZMC = "./Recoil_SingleElectron.root";

  corrector = new RecoilCorrector(WNew);
  corrector->addMCFile(ZMC);
  corrector->addDataFile(ZDat);

  outfile = new TFile("Template_"+option+".root","RECREATE"); 
  outfile->cd();
  for (int ih=0;ih<EtaChBins_;ih++){
    TString sel         = "h_eta_pfMET"+etabin[ih];
    h_eta_sel[ih]       = new TH1F(sel,sel,nBins,0,100.);
  }
}

void h10::SlaveBegin(TTree * /*tree*/)
{
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

}

Bool_t h10::Process(Long64_t entry)
{
  // The Process() function is called for each entry in the tree (or possibly
  // keyed object in the case of PROOF) to be processed. The entry argument
  // specifies which entry in the currently loaded tree is to be processed.
  // It can be passed to either h10::GetEntry() or TBranch::GetEntry()
  // to read either all or the required parts of the data. When processing
  // keyed objects with PROOF, the object is already loaded and is available
  // via the fObject pointer.
  //
  // This function should contain the "body" of the analysis. It can contain
  // simple or elaborate selection criteria, run algorithms on the data
  // of the event and typically fill histograms.
  //
  // The processing can be stopped by calling Abort().
  //
  // Use fStatus to set the return value of TTree::Process().
  //
  // The return value is currently not used.
  if (entry % 1000 == 0){
    std::cout<<"Entry: "<<entry<<std::endl;
  }

  GetEntry(entry);

  w=WT00;
  TLorentzVector * nVec = new TLorentzVector() ;
  TLorentzVector * eVec = new TLorentzVector() ;
  TLorentzVector * wVec = new TLorentzVector() ;

  nVec->SetPxPyPzE(Px_d2, Py_d2, Pz_d2, E_d2);
  eVec->SetPxPyPzE(Px_d1, Py_d1, Pz_d1, E_d1);
  wVec->SetPxPyPzE(Px_V, Py_V, Pz_V, E_V);

  //std::cout<<"e PT: "<<eVec->Pt()<<std::endl;

  if (eVec->Pt()>lep_ET){
    double met = nVec->Pt();
    //std::cout<<"met: "<<met<<std::endl;
    double met_phi = nVec->Phi();
    double pfU1 = 0.;
    double pfU2 = 0.;

    corrector->CorrectAll(met,met_phi,
        wVec->Pt(),wVec->Phi(),
        eVec->Pt(),eVec->Phi(),
        pfU1,pfU2,0.);

    //std::cout<<"met cor: "<<met<<std::endl;
    int ih = getEta(eVec);	
    if (ih>=0) h_eta_sel[ih]->Fill(met,w);

  }
  delete nVec;
  delete eVec;
  delete wVec;
  return kTRUE;
}

void h10::SlaveTerminate()
{
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

}

void h10::Terminate()
{
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.
  outfile->cd();
  outfile->Write();
  outfile->Close();
  //for (int ih=0;ih<EtaChBins_;ih++){
  //  TString sel         = "h_eta_pfMET"+etabin[ih];
  //  h_eta_sel[ih]->Write(sel); 
  //}
}


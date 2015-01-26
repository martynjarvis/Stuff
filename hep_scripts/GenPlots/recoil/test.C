#define test_cxx
// The class definition in test.h has been generated automatically
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
// Root > T->Process("test.C")
// Root > T->Process("test.C","some options")
// Root > T->Process("test.C+")
//

#include "test.h"
#include <TH2.h>
#include <TStyle.h>


void test::Begin(TTree * /*tree*/)
{
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).

  lep_ET = 35.;
  lep_eta = 2.4;
  lep_crack_1 = 1.4442;
  lep_crack_2 = 1.56;

  TString option = GetOption();
  outfile = new TFile("ntuple_Wp.root","RECREATE"); 
  bZ = false;
  outfile->cd();
  iTree = new TTree("FitRecoil","FitRecoil");
  SetTree(iTree);


}

void test::SlaveBegin(TTree * /*tree*/)
{
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

}

Bool_t test::Process(Long64_t entry)
{
  // The Process() function is called for each entry in the tree (or possibly
  // keyed object in the case of PROOF) to be processed. The entry argument
  // specifies which entry in the currently loaded tree is to be processed.
  // It can be passed to either test::GetEntry() or TBranch::GetEntry()
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

  if (eVec->Pt()>lep_ET){
    if (fabs(eVec->Eta())<lep_eta){
      if (fabs(eVec->Eta())<lep_crack_1 || fabs(eVec->Eta())>lep_crack_2){
        //std::cout<<"met: "<<met<<std::endl;
        if (bZ){
          if (fabs(nVec->Eta())<lep_crack_1 || fabs(nVec->Eta())>lep_crack_2){
            TVector2 * MET = new TVector2(0.,0.);

            TVector2 sumLepton(Px_d1+Px_d2, Py_d1+Py_d2);

            SetTreeVariables(wVec, wVec, &sumLepton, MET, MET, w, 0, iTree);

            delete MET;
          }
        }
        else{
          double met = nVec->Pt();
          double met_phi = nVec->Phi();
          TVector2 * MET = new TVector2(0.,0.);

          TVector2 sumLepton(Px_d1, Py_d1);

          MET->SetMagPhi(met,met_phi);
          SetTreeVariables(wVec, wVec, &sumLepton, MET, MET, w, 0, iTree);

          delete MET;
        }
      }
    }
  }
  delete nVec;
  delete eVec;
  delete wVec;
  return kTRUE;

}

void test::SlaveTerminate()
{
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

}

void test::Terminate()
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

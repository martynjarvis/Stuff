//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Jan 16 10:31:05 2012 by ROOT version 5.26/00
// from TTree h10/h10
// found on file: wm_lhc7_ct66_00.root
//////////////////////////////////////////////////////////

#ifndef h10_h
#define h10_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TLorentzVector.h>

#include "RecoilCorrector.hh"

const static int EtaBins = 11;
const static int EtaChBins_=EtaBins*2;
const static double etabinlow[EtaBins] = {0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.6,1.8,2.0,2.2};
const static double etabinup[EtaBins]  = {0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.8,2.0,2.2,2.4};
const static TString etabin[EtaChBins_]={ 
  "_eta1_pos","_eta2_pos","_eta3_pos","_eta4_pos","_eta5_pos","_eta6_pos","_eta7_pos","_eta8_pos","_eta9_pos","_eta10_pos","_eta11_pos", 
  "_eta1_neg","_eta2_neg","_eta3_neg","_eta4_neg","_eta5_neg","_eta6_neg","_eta7_neg","_eta8_neg","_eta9_neg","_eta10_neg","_eta11_neg" };

class h10 : public TSelector {
  public :
    TTree          *fChain;   //!pointer to the analyzed TTree or TChain

    // Declaration of leaf types
    Float_t         Px_d1;
    Float_t         Py_d1;
    Float_t         Pz_d1;
    Float_t         E_d1;
    Float_t         Px_d2;
    Float_t         Py_d2;
    Float_t         Pz_d2;
    Float_t         E_d2;
    Float_t         Px_V;
    Float_t         Py_V;
    Float_t         Pz_V;
    Float_t         E_V;
    Float_t         WT00;
    Int_t           _charge;
    float           w;

    RecoilCorrector *corrector;
    TH1F * h_eta_sel[EtaChBins_]; 
    double lep_ET;
    TFile * outfile;

    // List of branches
    TBranch        *b_Px_d1;   //!
    TBranch        *b_Py_d1;   //!
    TBranch        *b_Pz_d1;   //!
    TBranch        *b_E_d1;   //!
    TBranch        *b_Px_d2;   //!
    TBranch        *b_Py_d2;   //!
    TBranch        *b_Pz_d2;   //!
    TBranch        *b_E_d2;   //!
    TBranch        *b_Px_V;   //!
    TBranch        *b_Py_V;   //!
    TBranch        *b_Pz_V;   //!
    TBranch        *b_E_V;   //!
    TBranch        *b_WT00;   //!

    h10(TTree * /*tree*/ =0) { }
    virtual ~h10() { }
    virtual Int_t   Version() const { return 2; }
    virtual void    Begin(TTree *tree);
    virtual void    SlaveBegin(TTree *tree);
    virtual void    Init(TTree *tree);
    virtual Bool_t  Notify();
    virtual Bool_t  Process(Long64_t entry);
    virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
    virtual void    SetOption(const char *option) { fOption = option; }
    virtual void    SetObject(TObject *obj) { fObject = obj; }
    virtual void    SetInputList(TList *input) { fInput = input; }
    virtual TList  *GetOutputList() const { return fOutput; }
    virtual void    SlaveTerminate();
    virtual void    Terminate();
    virtual Int_t   getEta(TLorentzVector* lep);

    ClassDef(h10,0);
};

#endif

#ifdef h10_cxx
void h10::Init(TTree *tree)
{
  // The Init() function is called when the selector needs to initialize
  // a new tree or chain. Typically here the branch addresses and branch
  // pointers of the tree will be set.
  // It is normally not necessary to make changes to the generated
  // code, but the routine can be extended by the user if needed.
  // Init() will be called many times when running on PROOF
  // (once per file to be processed).

  // Set branch addresses and branch pointers
  if (!tree) return;
  fChain = tree;
  fChain->SetMakeClass(1);

  fChain->SetBranchAddress("Px_d1", &Px_d1, &b_Px_d1);
  fChain->SetBranchAddress("Py_d1", &Py_d1, &b_Py_d1);
  fChain->SetBranchAddress("Pz_d1", &Pz_d1, &b_Pz_d1);
  fChain->SetBranchAddress("E_d1", &E_d1, &b_E_d1);
  fChain->SetBranchAddress("Px_d2", &Px_d2, &b_Px_d2);
  fChain->SetBranchAddress("Py_d2", &Py_d2, &b_Py_d2);
  fChain->SetBranchAddress("Pz_d2", &Pz_d2, &b_Pz_d2);
  fChain->SetBranchAddress("E_d2", &E_d2, &b_E_d2);
  fChain->SetBranchAddress("Px_V", &Px_V, &b_Px_V);
  fChain->SetBranchAddress("Py_V", &Py_V, &b_Py_V);
  fChain->SetBranchAddress("Pz_V", &Pz_V, &b_Pz_V);
  fChain->SetBranchAddress("E_V", &E_V, &b_E_V);
  fChain->SetBranchAddress("WT00", &WT00, &b_WT00);
}

int h10::getEta(TLorentzVector * lep){
  double eta= fabs((lep)->Eta());
  double charge = _charge;
  //bool acc= (((fabs(eta)<1.6)&&(fabs(eta)>1.4))|| (fabs(eta)>2.4));
  //bool cha = (charge==0);
  int ih = -1;
  for (int ieta=0;ieta<EtaBins;ieta++){ 
    if ( (eta>etabinlow[ieta]) && (eta<etabinup[ieta]) ) {
      ih = ieta; 
      break;
    }
  }
  if (ih < 0) return -1; // no eta bin found
  //if (cha)    return -1;
  //if (acc)    return -1;
  if (charge<0) ih+=EtaBins; // positive bins go 0,1,2,3,4,5, negative go 6,7,8,9,10,11
  //cout<<"test:"<<ih<<endl;
  return ih;
}

Bool_t h10::Notify()
{
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  return kTRUE;
}

#endif // #ifdef h10_cxx

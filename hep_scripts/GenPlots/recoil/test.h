//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Feb  1 18:00:43 2012 by ROOT version 5.27/06b
// from TTree h10/h10
// found on file: z0_lhc7_ct66.root
//////////////////////////////////////////////////////////

#ifndef test_h
#define test_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TLorentzVector.h>
#include <TVector2.h>

class test : public TSelector {
public :
    float lep_ET ;
    float lep_eta;
    float lep_crack_1;
    float lep_crack_2;
    TFile * outfile;
   //OUTPUT TREE
    // lepton properties
    float _leppt;
    float _lepphi;

    // boson properties
    float _genpt;
    float _genphi;
    float _mass;
    float _pt;
    float _y;
    float _phi;

    //pfmet
    float _pfmet;
    float _pfmetphi;
    float _pfmt;
    float _pfu1;
    float _pfu2;

    //track met
    float _trkmet;
    float _trkmetphi;
    float _trkmt;
    float _trku1;
    float _trku2;

    float _weight;
    int _njet;

    TTree * iTree;

    double w;
   bool bZ;
   //INPUT TREE
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

   test(TTree * /*tree*/ =0) { }
   virtual ~test() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual void    SetTree(TTree *tree);
   virtual void    SetTreeVariables(TLorentzVector *genBoson, TLorentzVector *recoBoson, TVector2 *sumLepton, TVector2 *pfMET, TVector2 *trkMET, float wt, int nJet, TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   ClassDef(test,0);
};

#endif

#ifdef test_cxx
void test::Init(TTree *tree)
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

void test::SetTree(TTree *tree){

  // lepton properties
  tree->Branch("leppt", &_leppt ,"leppt/F");
  tree->Branch("lepphi", &_lepphi ,"lepphi/F");

  // boson properties
  tree->Branch("genpt", &_genpt ,"genpt/F");
  tree->Branch("genphi", &_genphi ,"genphi/F");
  tree->Branch("mass", &_mass ,"mass/F");
  tree->Branch("pt", &_pt ,"pt/F");
  tree->Branch("y", &_y ,"y/F");
  tree->Branch("phi", &_phi ,"phi/F");

  //pfmet
  tree->Branch("pfmet", &_pfmet ,"pfmet/F");
  tree->Branch("pfmetphi", &_pfmetphi ,"pfmetphi/F");
  tree->Branch("pfmt", &_pfmt ,"pfmt/F");
  tree->Branch("pfu1", &_pfu1 ,"pfu1/F");
  tree->Branch("pfu2", &_pfu2 ,"pfu2/F");

  //track met
  tree->Branch("trkmet", &_trkmet ,"trkmet/F");
  tree->Branch("trkmetphi", &_trkmetphi ,"trkmetphi/F");
  tree->Branch("trkmt", &_trkmt ,"trkmt/F");
  tree->Branch("trku1", &_trku1 ,"trku1/F");
  tree->Branch("trku2", &_trku2 ,"trku2/F");

  tree->Branch("weight", &_weight ,"weight/F");
  tree->Branch("njet", &_njet ,"njet/I");
}

void test::SetTreeVariables(TLorentzVector *genBoson, TLorentzVector *recoBoson,
    TVector2 *sumLepton,
    TVector2 *pfMET, TVector2 *trkMET,
    float wt, int nJet, TTree *tree){


  // Transverse Recoil Vector
  TVector2 * pfU = new TVector2(0.,0.);
  (*pfU) -= *pfMET;
  (*pfU) -= *sumLepton;

  TVector2 * trkU = new TVector2(0.,0.);
  (*trkU) -= *trkMET;
  (*trkU) -= *sumLepton;

  // Transverse Decomposed in to components parallel and perpendicular to
  // boson PT
  TVector2 qT;
  qT.SetMagPhi(genBoson->Pt(),genBoson->Phi());
  // I think this is correct, it doesn;t make sense with the W boson, to use the
  // Reco since the W boson = MET+Lepton, which it equal and oposite to the
  // Recoil = -Met-Lepton
  //
  // For the Z data, I use the reco Z. I think this is correct
  // Indeed this is all correct, more detailed in Phil's Thesis.
  float dPhi = pfU->DeltaPhi(qT);
  //cout<<"~~~~~~~~~~~~~~~~"<<endl;
  //cout<<"TEST: pfU  ="<<pfU->Mod()<<endl;
  //cout<<"TEST: pfUfi="<<pfU->Phi()<<endl;
  //cout<<"TEST: qTU  ="<<qT.Mod()<<endl;
  //cout<<"TEST: qTfi ="<<qT.Phi()<<endl;
  //cout<<"TEST: dphi ="<<dPhi<<endl;
  _pfu1 = pfU->Mod()*cos(dPhi);
  //cout<<"TEST: pfU1 ="<<_pfu1<<endl;
  _pfu2 = pfU->Mod()*sin(dPhi);
  //cout<<"TEST: pfU2 ="<<_pfu2<<endl;

  dPhi = trkU->DeltaPhi(qT);
  _trku1 = trkU->Mod()*cos(dPhi);
  _trku2 = trkU->Mod()*sin(dPhi);

  // boson properties
  _genpt = genBoson->Pt();
  _genphi = genBoson->Phi();
  _mass = recoBoson->M();
  _pt = recoBoson->Pt();
  _y = recoBoson->Rapidity();
  _phi = recoBoson->Phi();

  // lepton properties
  _leppt = sumLepton->Mod();
  _lepphi = sumLepton->Phi();

  //pfmet
  _pfmet = pfMET->Mod();
  _pfmetphi = pfMET->Phi_mpi_pi(pfMET->Phi());
  _pfmt = sqrt(2)*sqrt(sumLepton->Mod()*pfMET->Mod() 
      -sumLepton->Mod()*pfMET->Mod()
      *cos(pfMET->DeltaPhi(*sumLepton)));

  //track met
  _trkmet = trkMET->Mod();
  _trkmetphi = trkMET->Phi_mpi_pi(trkMET->Phi());
  _trkmt = sqrt(2)*sqrt(sumLepton->Mod()*trkMET->Mod() 
      -sumLepton->Mod()*trkMET->Mod()
      *cos(trkMET->DeltaPhi(*sumLepton)));

  _weight = wt;
  _njet = nJet;
  tree->Fill();
}

Bool_t test::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef test_cxx

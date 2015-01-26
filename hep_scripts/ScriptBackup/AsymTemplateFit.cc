/*********************************************************************************
*********************************************************************************/

#include <algorithm>

void AsymTemplateFit(int ieff=80, float lumi=33.7, int ptCut=25, int METCut=0, int reco = 0,bool corr=false ,bool DATA=true)
{
  gROOT->SetBatch();
  gROOT->Reset();   
  gROOT->SetStyle("Plain");// #To set plain bkgds for slides
  gStyle->SetTitleBorderSize(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetLineWidth(0.25);
  gStyle->SetCanvasColor(0);//#Sets canvas colour white
  gStyle->SetLabelOffset(0.001);
  gStyle->SetLabelSize(0.05);
  gStyle->SetLabelSize(0.05,"Y");//#Y axis
  gStyle->SetTitleSize(0.04);
  gStyle->SetTitleW(0.7);
  gStyle->SetTitleH(0.07);
  gStyle->SetOptTitle(1);
  gStyle->SetAxisColor(1, "XYZ");
  gStyle->SetStripDecimals(true);
  gStyle->SetTickLength(0.03, "XYZ");
  gStyle->SetNdivisions(510, "XYZ");
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetLabelColor(1, "XYZ");
  gStyle->SetLabelFont(42, "XYZ");
  gStyle->SetLabelOffset(0.007, "XYZ");
  gStyle->SetLabelSize(0.04, "XYZ");
  gStyle->SetHatchesLineWidth(3);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1111);
  gSystem->Load("libRooFit") ;
  using namespace RooFit;

  TString ptStr;
  if (ptCut==25) {
    ptStr="";
  } else if (ptCut==30) {
    ptStr="_30";
  } else if (ptCut==35) {
    ptStr="_35";
  }
  else {
    cout << "ptCut (4th argument) must be 25, 30 or 35" << endl;
  }
 
  
  TString str_eff;
  if (ieff==60) str_eff="_WP60";
  else if (ieff==70) str_eff="_WP70";
  else if (ieff==80) str_eff="_WP80";
  else if (ieff==85) str_eff="_WP85";
  else if (ieff==90) str_eff="_WP90";
  else if (ieff==95) str_eff="_WP95";
  else {
    cout << "input argument (signal efficiency point) must be 60, 70, 80 ,85, 90 or 95" << endl;
    return;
  }
  TString TemplateLocation="./Templates/";

  TString DIR="Templates" + str_eff + "_Ele" + "25";//This will be changed
  
  float EWKfrac = 1.0;
   
  //wShape = 1 Silvia's MET recoil templates
  //wShape = 2 MIT Z recoil templates
  //wShape = 3 MIT recoil templates with eta corrections
  //wShape = 4 Silvia's Ersatz with eta corrections
  //wShape = 5 DW Ersatz with eta corrections
//   bool bUseMETRecoil = false;
//   bool bUseMITMETRecoil = false;
//   bool bUseMITMETRecoilCorr = false;
//   bool bUseErsatz = false; 
       
  //EventSelection
  TString data_Ev="h_pfMET";
  TString data_AntiEv="h_anti_pfMET";
  
  TString Ev="h_pfMET";
  TString AntiEv="h_anti_pfMET";
  
  if (corr) {
    data_Ev+="cor";
    data_AntiEv+="cor";
  }
  
  TString Suffix=ptStr;
  TString SAVDIR="./";//"~/public/html/";
  TString FORMAT=".png";//pdf";
  
  TLegend *l5_2 = new TLegend(0.7,0.5,0.9,0.9);
  TLegend *l5_0 = new TLegend(0.7,0.5,0.9,0.9);
  TLegend *l5_1 = new TLegend(0.1,0.6,0.4,0.9);

  TLegend *l5_4 = new TLegend(0.7,0.7,0.9,0.9);
  TLegend *l5_3 = new TLegend(0.7,0.7,0.9,0.9);
  TLegend *l5_7 = new TLegend(0.7,0.7,0.9,0.9);
  
  int binMETCut = METCut/2+1;
  int nbins=50;
  int rebinFactor=2;

  TString Titles[12]={"Positrons |#eta|<0.4","Electrons |#eta|<0.4","Positrons 0.4<|#eta|<0.8",
    "Electrons 0.4<|#eta|<0.8","Positrons 0.8<|#eta|<1.2","Electrons 0.8<|#eta|<1.2",
    "Positrons 1.2<|#eta|<1.6","Electrons 1.2<|#eta|<1.6","Positrons 1.6<|#eta|<2.0",
    "Electrons 1.6<|#eta|<2.0","Positrons 2.0<|#eta|<2.4","2.0<Electrons |#eta|<2.4"};
  TFile *file[19];
//Data
  if (reco == 0) {
    SAVDIR+="Sep17_";
    file[0] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_data.root");
  }
  else if (reco == 1 ){
    SAVDIR+="Nov4_";
    file[0] = TFile::Open(TemplateLocation+"Templates_data_Nov4.root");//ResultsWENU_VBTFpreselection_data_nov4.root");
  }
  else if (reco == 2 ) {
    SAVDIR+="Dec4_";
    file[0] = TFile::Open(TemplateLocation+"Templates_dec4.root");
  }
  else if (reco == 3 ) {
    SAVDIR+="Dec22_";
    file[0] = TFile::Open(TemplateLocation+"Templates_dec22.root");
  }

//MC
  file[2] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdEm_20-30.root");
  file[3] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdEm_30-80.root");
  file[4] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdEm_80-170.root");
  file[5] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdBce20-30.root");
  file[6] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdBce30-80.root");
  file[7] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_qcdBce80-170.root");
  file[8] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_gj15-30.root");
  file[9] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_gj30-50.root");

  file[11] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_wenuPlus.root");
  file[12] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_wenuMinus.root");

  //file[14] = TFile::Open(TemplateLocation+"Templates_DYee_M1to10.root");
  file[15] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_dytautau.root");
  file[16] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_dyee.root");
  file[17] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_wtaunu.root");
  file[18] = TFile::Open(TemplateLocation+"ResultsWENU_VBTFpreselection_ttbar.root");

  TString bins[12]={"_eta1_pos","_eta1_neg","_eta2_pos","_eta2_neg","_eta3_pos","_eta3_neg","_eta4_pos","_eta4_neg","_eta5_pos","_eta5_neg","_eta6_pos","_eta6_neg"};
  TH1F* hh_data_sel[12];  TH1F* hh_wenu_sel[12];  TH1F* hh_ewk_sel[12]; TH1F* hh_qcd_sel[12];
  TH1F* hh_data_sel_antisel[12];TH1F*  hh_bkg_sel_template[12]; TH1F *hh_ewk_sel_fit[12];
  TH1F* hh_wenu_sel_fit[12];
  TH1F* hh_tot_sel_fit[12];  TH1F* hh_wenuewk_sel[12];TH1F* hh_bkg_sel_template_fit[12];
  for (int ib=0; ib<12;ib++){
    hh_data_sel[ib]= new TH1F("h_data_sel"+bins[ib], "data_sel"+bins[ib], 100,0.,100.);;
    hh_wenu_sel[ib]=new TH1F("h_wenu_sel"+bins[ib],"wenu_sel"+bins[ib],100,0.,100.);
    hh_ewk_sel[ib] = new TH1F("h_ewk_sel"+bins[ib],"ewk_sel"+bins[ib],100,0.,100.);
    hh_qcd_sel[ib] = new TH1F("h_qcd_sel"+bins[ib],"qcd_sel"+bins[ib],100,0.,100.);
    hh_data_sel_antisel[ib] = new TH1F("h_data_sel_antisel"+bins[ib], "data_sel_antisel"+bins[ib], 100,0.,100.);
    hh_bkg_sel_template[ib]  = new TH1F("h_bkg_sel_template"+bins[ib], "data_bkg_sel_template"+bins[ib], nbins,0.,100.);
    hh_wenu_sel_fit[ib] = new TH1F("h_wenu_fit"+bins[ib],"wenu_fit"+bins[ib],nbins,0.,100.);
    hh_ewk_sel_fit[ib] = new TH1F("h_ewk_fit"+bins[ib],"ewk_fit"+bins[ib],nbins,0.,100.);
    hh_bkg_sel_template_fit[ib] = new TH1F("h_bkg_template_fit"+bins[ib], "bkg_template_fit"+bins[ib], nbins,0.,100.);  
    hh_wenuewk_sel[ib] = new TH1F("h_wenuewk_sel"+bins[ib],"wenuewk_sel"+bins[ib],nbins,0.,100.);
    hh_tot_sel_fit[ib] = new TH1F("h_tot_sel_fit"+bins[ib],"tot_sel_fit"+bins[ib],nbins,0.,100.);
  }

  TCanvas *c0 = new TCanvas("c0","Canvas0",1680,1050);
  c0->Divide(4,3);
  c0->SetFillColor(10);

  TCanvas *c1 = new TCanvas("c1","Canvas1",1680,1050);
  c1->Divide(4,3);
  c1->SetFillColor(10);
  TCanvas *c2 = new TCanvas("c2","Canvas2");
  c2->SetFillColor(10);
  if (!DATA){
    TCanvas *c3 = new TCanvas("c3","Canvas3",1680,1050);
    c3->Divide(4,3);
  }

  TCanvas *c4 = new TCanvas("c4","Canvas4",1680,1050);
  c4->SetFillColor(10);
  c4->Divide(4,3);
  TCanvas *c5 = new TCanvas("c5","Canvas5");

  TH1D *POS=new TH1D("POS","POS",6,0,2.4);
  TH1D *NEG=new TH1D("NEG","NEG",6,0,2.4);
  TH1D *BPOS=new TH1D("BPOS","BPOS",6,0,2.4);
  TH1D *BNEG=new TH1D("BNEG","BNEG",6,0,2.4);


  TH1 *ASY;
  
  double w[19];
  //for (unsigned i=1; i<19; i++) w[i]=lumi;  //w[i]=(w[i]/10.)*lumi;
  w[0] = 1;
  w[1] = (1.0/345.966)*lumi;

  w[2] = (1.0/14.900)*lumi;
  w[3] = (1.0/17.810)*lumi;
  w[4] = (1.0/57.875)*lumi;
  w[5] = (1.0/16.975)*lumi;
  w[6] = (1.0/14.587)*lumi;
  w[7] = (1.0/111.473)*lumi;
  w[8] = (1.0/5.392)*lumi;
  w[9] = (1.0/61.443)*lumi;

  w[11] = (1.0/345.966)*lumi;
  w[12] = (1.0/506.271)*lumi;

  w[15] = (1.0/1176.095)*lumi;
  w[16] = (1.0/1238.53)*lumi;
  w[17] = (1.0/537.272)*lumi;
  w[18] = (1.0/10633.511)*lumi;
 
  //EWK XSEC UNC.
  for (unsigned i=15; i<19; i++) {
    w[i]*=EWKfrac;
  }

  TH1F *h1;

  for (int ib=0; ib<12;ib++){
    
  cout<<"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;  
  cout<<"Eta Charge Bin:"<<Titles[ib]<<endl;  
  
    if (DATA){
      file[0]->cd(DIR);
      gDirectory->GetObject(data_Ev+bins[ib]+Suffix,h1);
 //    gDirectory->GetObject(Ev+bins[ib],h1);//(data_Ev+bins[ib],h1);
	  //h1->Rebin(2);
      hh_data_sel[ib]->Add(h1);
      gDirectory->GetObject(data_AntiEv+bins[ib]+Suffix,h1);//
      //h1->Rebin(2); //opps i changed the AS binning but no the selection
      hh_data_sel_antisel[ib]->Add(h1);
	  //return;
    }
    else{
      for (unsigned i=2; i<19; i++) {
        //   why 2? I removed wenu and added combined sample
        if (i>9&&i<11) continue;	
        if (i>2&&i<15) continue;	
        file[i]->cd(DIR);
        gDirectory->GetObject(Ev+bins[ib]+Suffix,h1);
        hh_data_sel[ib]->Add(h1,w[i]);
        gDirectory->GetObject(AntiEv+bins[ib]+Suffix,h1);
        hh_data_sel_antisel[ib]->Add(h1,w[i]);	
      }
    }

    //Wenuplus and minus
    file[11]->cd(DIR);
    gDirectory->GetObject(Ev+bins[ib]+Suffix,h1);
    h1->Sumw2();
    hh_wenu_sel[ib]->Add(h1,w[11]);
    
    file[12]->cd(DIR);
    gDirectory->GetObject(Ev+bins[ib],h1);
    h1->Sumw2();
    hh_wenu_sel[ib]->Add(h1,w[12]);
   
//     if (bUseMETRecoil) {
//       cout<<"Using Silvia's MET Recoil W->e nu template shapes."<<endl;  
//       TFile *Wenufile = TFile::Open(TemplateLocation+"Templates_Wenu_Silvia.root");//*******
//       double nWenu = hh_wenu_sel[ib]->Integral();
//       TString WenuDIR="Templates_00";
//       hh_wenu_sel[ib]->Reset();				
//       Wenufile->cd(WenuDIR);				
//       gDirectory->GetObject("h_MC_sel"+bins[ib],h1);	//"h_corr"+bins[ib],h1);//
//       //h1->Sumw2();
//       h1->Rebin(2);//200 -> 100
//       hh_wenu_sel[ib]->Add(h1,1.0*nWenu/(h1->Integral()));
//     }
//     else if (bUseMITMETRecoil) {
//      cout<<"Using MIT's MET Recoil W->e nu template shapes."<<endl;  
//      TFile *MITfile =  TFile::Open(TemplateLocation+"Templates_Wenu_dec22.root");
  TFile *MITfile;
  if (reco == 0) {
    MITfile = TFile::Open(TemplateLocation+"Templates_Wenu.root");
  }
  else if (reco == 1 ){
    MITfile =TFile::Open(TemplateLocation+"Templates_Wenu.root");
  }
  else if (reco == 2 ) {
    MITfile = TFile::Open(TemplateLocation+"Templates_Wenu_dec22.root");//TODO
  }
  else if (reco == 3 ) {
    MITfile = TFile::Open(TemplateLocation+"Templates_Wenu_dec22.root");
  }


      //hh_wenu_sel[ib]->Rebin(rebinFactor/2);
      double nWenu = hh_wenu_sel[ib]->Integral();
      TString WenuDIR;
      if (ptCut==25) {
	WenuDIR="midTree25";
      } else if (ptCut==30) {
	WenuDIR="midTree30";
      } else if (ptCut==35) {
	WenuDIR="midTree35";
      }
      hh_wenu_sel[ib]->Reset();				
      MITfile->cd(WenuDIR);				
      gDirectory->GetObject("h_pfMET"+bins[ib],h1);	
      //h1->Sumw2();
      hh_wenu_sel[ib]->Add(h1,1.00001*nWenu/(h1->Integral()));	
//     }
//     else if (bUseMITMETRecoilCorr) {
//       cout<<"Using MIT template shapes (with eta binning fudge factor)"<<endl;   
//       TFile *MITfile =  TFile::Open(TemplateLocation+"Templates_Wenu_MITCorrected.root");
//       //hh_wenu_sel[ib]->Rebin(rebinFactor/2);
//       double nWenu = hh_wenu_sel[ib]->Integral();
//       TString WenuDIR="corr";
//       hh_wenu_sel[ib]->Reset();				
//       MITfile->cd(WenuDIR);				
//       gDirectory->GetObject("h_corr"+bins[ib],h1);	
//       //h1->Sumw2();
//       hh_wenu_sel[ib]->Add(h1,1.001*nWenu/(h1->Integral()));	
//     }
//     else if (bUseErsatz) {
//       cout<<"ERROR: NOT UPDATED YET."<<endl;    
//       return;
//     }
    for (unsigned i=15; i<19; i++) {
      file[i]->cd(DIR);
      gDirectory->GetObject(Ev+bins[ib]+Suffix,h1);
      h1->Sumw2();  
      hh_ewk_sel[ib]->Add(h1,w[i]);
    }
    for (unsigned i=2; i<10; i++) {
      file[i]->cd(DIR);
      gDirectory->GetObject(Ev+bins[ib],h1);
      h1->Sumw2();  
      hh_qcd_sel[ib]->Add(h1,w[i]);
    }

    hh_data_sel[ib]->Rebin(rebinFactor);
    hh_ewk_sel[ib]->Rebin(rebinFactor);
    hh_qcd_sel[ib]->Rebin(rebinFactor);
    hh_wenu_sel[ib]->Rebin(rebinFactor);
    hh_data_sel_antisel[ib]->Rebin(rebinFactor);
    
    // & $0.0<| \eta |<0.4$  & 13791 & 4127 & 18138\\ 
// Integral(Int_t binx1, Int_t binx2, Option_t* option = "") const
//    cout<<"Using range: "<<hh_wenu_sel[ib]->GetXaxis()->GetBinLowEdge(binMETCut)<<" to " 
//<<hh_wenu_sel[ib]->GetXaxis()->GetBinUpEdge(nbins)<<endl;
//	cout<<hh_wenu_sel[ib]->Integral(binMETCut,nbins)<<" & 
//"<<hh_ewk_sel[ib]->Integral(binMETCut,nbins)+hh_qcd_sel[ib]->Integral(binMETCut,nbins)<<" & 
//"<<hh_data_sel[ib]->Integral(binMETCut,nbins)<<endl;
	
    cout<<"NEvents = "<<hh_data_sel[ib]->Integral(binMETCut,nbins)<<endl;     
    hh_wenuewk_sel[ib]->Add(hh_wenu_sel[ib]);
    hh_wenuewk_sel[ib]->Add(hh_ewk_sel[ib]);
    hh_bkg_sel_template[ib]->Add(hh_data_sel_antisel[ib]);
       
    RooRealVar pfMET("pfMET","pfMET",0.,100.);
    RooRealVar fsig("fsig","signal fraction",0.5,0.,1.);

    TH1*  hhhh_wenuewk_sel = (TH1*)hh_wenuewk_sel[ib]->Clone();
    TH1*  hhhh_bkg_sel_template =(TH1*)hh_bkg_sel_template[ib]->Clone();
    TH1*  hhhh_data_sel =(TH1*)hh_data_sel[ib]->Clone();
    
    RooDataHist roohist_wenuewk_sel("roohist_wenuewk_sel","wenuewk with pfMET",pfMET,hhhh_wenuewk_sel);
    RooDataHist roohist_bkg_sel_template("roohist_bkg_sel_template","bkg_template with pfMET",pfMET,hhhh_bkg_sel_template);
    RooHistPdf pdf_wenuewk_sel("pdf_wenuewk_sel","wenuewk with pfMET",RooArgList(pfMET),roohist_wenuewk_sel);
    RooHistPdf pdf_bkg_sel_template("pdf_bkg_sel_template","bkg_template with pfMET",RooArgList(pfMET),roohist_bkg_sel_template);
    RooDataHist roohist_data_sel("roohist_data_sel","data with pfMET",pfMET,hhhh_data_sel);
 
    RooRealVar nsig("nsig","signal fraction",0.,1000000.);
    RooRealVar nbkg("nbkg","background fraction",0.,1000000.);  
    RooAddPdf model_sel("model_sel","model_sel",RooArgList(pdf_wenuewk_sel,pdf_bkg_sel_template),RooArgList(nsig,nbkg));
    model_sel.fitTo(roohist_data_sel,Extended(kTRUE),SumW2Error(kFALSE),InitialHesse(kTRUE),PrintLevel(-2)); 
    
    double nwenuewk_fit = nsig.getVal();
    double nwenuewk_fit_err = nsig.getError();
    double relSigErr=nwenuewk_fit_err/nwenuewk_fit;

    double nbkg_fit = nbkg.getVal();
    double nbkg_fit_err = nbkg.getError();
    double relBkgErr=nbkg_fit_err/nbkg_fit;

    //ROOFIT PLOT
    c0->cd(ib+1);
    RooPlot* xframe =  pfMET.frame();
    roohist_data_sel.plotOn(xframe,  MarkerColor(kBlack));
    model_sel.plotOn(xframe, Name("model_sel"), DrawOption("L"));
    xframe->Draw();

    double ScaleBkg= nbkg_fit/hh_bkg_sel_template[ib]->Integral();
    double ScaleSignal=nwenuewk_fit/hhhh_wenuewk_sel->Integral();
    double relfrac_wenu=hh_wenu_sel[ib]->Integral()/hhhh_wenuewk_sel->Integral();

    hh_wenu_sel_fit[ib]->Reset();
    hh_wenu_sel_fit[ib]->Add(hh_wenu_sel[ib]);
    hh_ewk_sel_fit[ib]->Reset();
    hh_ewk_sel_fit[ib]->Add(hh_ewk_sel[ib]);
    hh_bkg_sel_template_fit[ib]->Reset();
    hh_bkg_sel_template_fit[ib]->Add(hh_bkg_sel_template[ib]);

    hh_wenu_sel_fit[ib]->Scale(ScaleSignal);
    hh_ewk_sel_fit[ib]->Scale(ScaleSignal);
    hh_bkg_sel_template_fit[ib]->Scale(ScaleBkg);

    float NSignal =hh_wenu_sel_fit[ib]->Integral(binMETCut,nbins);//nwenuewk_fit*relfrac_wenu;
    float NBackground =hh_bkg_sel_template_fit[ib]->Integral(binMETCut,nbins) + hh_ewk_sel_fit[ib]->Integral(binMETCut,nbins);//nbkg_fit+(nwenuewk_fit*(1-relfrac_wenu));
 
    if (ib==0)POS->SetBinContent(1,NSignal);
    if (ib==1)NEG->SetBinContent(1,NSignal);  
    if (ib==2)POS->SetBinContent(2,NSignal);
    if (ib==3)NEG->SetBinContent(2,NSignal); 
    if (ib==4)POS->SetBinContent(3,NSignal);
    if (ib==5)NEG->SetBinContent(3,NSignal);    
    if (ib==6)POS->SetBinContent(4,NSignal);
    if (ib==7)NEG->SetBinContent(4,NSignal);  
    if (ib==8)POS->SetBinContent(5,NSignal);
    if (ib==9)NEG->SetBinContent(5,NSignal); 
    if (ib==10)POS->SetBinContent(6,NSignal);
    if (ib==11)NEG->SetBinContent(6,NSignal);         
    if (ib==0)POS->SetBinError(1,NSignal*relSigErr);
    if (ib==1)NEG->SetBinError(1,NSignal*relSigErr);  
    if (ib==2)POS->SetBinError(2,NSignal*relSigErr);
    if (ib==3)NEG->SetBinError(2,NSignal*relSigErr); 
    if (ib==4)POS->SetBinError(3,NSignal*relSigErr);
    if (ib==5)NEG->SetBinError(3,NSignal*relSigErr);    
    if (ib==6)POS->SetBinError(4,NSignal*relSigErr);
    if (ib==7)NEG->SetBinError(4,NSignal*relSigErr);  
    if (ib==8)POS->SetBinError(5,NSignal*relSigErr);
    if (ib==9)NEG->SetBinError(5,NSignal*relSigErr); 
    if (ib==10)POS->SetBinError(6,NSignal*relSigErr);
    if (ib==11)NEG->SetBinError(6,NSignal*relSigErr);    

    cout << endl;
    cout << "NSignal = " << NSignal << endl;
    cout << "NBackground = " << NBackground << endl;
    
    c1->cd(ib+1);
    hh_data_sel[ib]->SetMarkerSize(.01);
    hh_data_sel[ib]->SetMarkerStyle(20);
    
    hh_wenu_sel_fit[ib]->SetFillColor(42);
    hh_ewk_sel_fit[ib]->SetFillColor(45);
    hh_bkg_sel_template_fit[ib]->SetFillColor(9);
    
    hh_wenu_sel_fit[ib]->SetLineWidth(0.25);
    hh_ewk_sel_fit[ib]->SetLineWidth(0.25);
    hh_bkg_sel_template_fit[ib]->SetLineWidth(0.25);
    
    
    THStack *h_back_sel_fit = new THStack("h_back_sel_fit","Fit: " + Titles[ib]); 
    
    h_back_sel_fit->Add(hh_bkg_sel_template_fit[ib]); 
    h_back_sel_fit->Add(hh_ewk_sel_fit[ib]);
    h_back_sel_fit->Add(hh_wenu_sel_fit[ib]);
    
    hh_tot_sel_fit[ib]->Reset();
    hh_tot_sel_fit[ib]->Add(hh_ewk_sel_fit[ib]);
    hh_tot_sel_fit[ib]->Add(hh_bkg_sel_template_fit[ib]);
    hh_tot_sel_fit[ib]->Add(hh_wenu_sel_fit[ib]);
    hh_tot_sel_fit[ib]->SetLineStyle(2);
    hh_tot_sel_fit[ib]->SetLineColor(3);
    hh_data_sel[ib]->SetMinimum(0);

    hh_data_sel[ib]->SetTitle(Titles[ib]);
    //hh_data_sel[ib]->GetYaxis()->SetTitleOffset(0.4);
    //hh_data_sel[ib]->GetYaxis()->SetTitleSize(0.1);
    //hh_data_sel[ib]->GetXaxis()->SetTitleOffset(0.5);
    //hh_data_sel[ib]->GetXaxis()->SetTitleSize(0.1);
    //hh_data_sel[ib]->GetXaxis()->SetLabelSize(.06);
    //hh_data_sel[ib]->GetYaxis()->SetLabelSize(.06);


    hh_data_sel[ib]->GetXaxis()->SetRange(0,100);
    hh_data_sel[ib]->GetXaxis()->SetTitle("PFMet (GeV)");
    hh_data_sel[ib]->GetYaxis()->SetTitle("Events/2 GeV");
    h_back_sel_fit->Draw("hist");
    hh_data_sel[ib]->Draw("e same");

    for (int j=1;j<nbins+1;j++) {
      float dcomp=(hh_wenuewk_sel[ib]->GetBinContent(j)>0)?	hh_wenuewk_sel[ib]->GetBinError(j)/hh_wenuewk_sel[ib]->GetBinContent(j):0;
      float drelSig=sqrt(relSigErr*relSigErr+dcomp*dcomp);
      float dSig=hh_wenuewk_sel[ib]->GetBinContent(j)*ScaleSignal*drelSig;
      
      float dcomp=(hh_bkg_sel_template[ib]->GetBinContent(j)>0.)?hh_bkg_sel_template[ib]->GetBinError(j)/hh_bkg_sel_template[ib]->GetBinContent(j):0.;
      float drelBkg=sqrt(relBkgErr*relBkgErr+dcomp*dcomp);
      float dBkg=drelBkg*ScaleBkg*hh_bkg_sel_template[ib]->GetBinError(j);
      float ErrTot=sqrt(dSig*dSig+dBkg*dBkg);
      hh_tot_sel_fit[ib]->SetBinError(j,ErrTot);
    }
//    Double_t chi2ndof = hh_data_sel[ib]->Chi2Test(hh_tot_sel_fit[ib],"CHI2/NDF");
//    Double_t chi2ndofUW = hh_data_sel[ib]->Chi2Test(hh_tot_sel_fit[ib],"UW CHI2/NDF");
//    Double_t chi2 = hh_data_sel[ib]->Chi2Test(hh_tot_sel_fit[ib],"CHI2"); 
//    Double_t chi2UW = hh_data_sel[ib]->Chi2Test(hh_tot_sel_fit[ib],"UW CHI2"); 
//    cout<<"CHI2 "<<chi2<<"CHI2NDOF "<<chi2ndof<<endl;
//    cout<<"CHI2 "<<chi2UW<<"CHI2NDOF "<<chi2ndofUW<<endl;
  
    if (ib==0){
      l5_2->AddEntry(hh_data_sel[ib],"data","p");
      l5_2->AddEntry(hh_bkg_sel_template_fit[ib],"QCD","F");
      l5_2->AddEntry(hh_wenu_sel_fit[ib],"Signal","F");
      l5_2->AddEntry(hh_ewk_sel_fit[ib],"EWK","F");
      //l5_2->AddEntry(hh_tot_sel_fit[ib],"Fit","l");

      l5_2->Draw();
    }
    //MICHELE
    c4->cd(ib+1);
    //c5->cd();
    
    TH1 *jgg= new TH1F("h_data_selj"+bins[ib], bins[ib], nbins,0.,100.);
    TH1 *agg= (TH1*)hh_data_sel[ib]->Clone();
    TH1 *bgg= (TH1*)hh_tot_sel_fit[ib]->Clone();
    
    jgg->SetTitle(Titles[ib]);
    jgg->Divide(agg,bgg,1,1);
    jgg->SetMarkerStyle(20);
    jgg->SetMarkerSize(0.3); 
    jgg->SetMarkerColor(1);
    jgg->SetLineColor(1);
    jgg->SetMinimum(0.4);
    jgg->SetMaximum(2.4);
    jgg->Draw("pe");
    TLine* line=new TLine(0.0, 1.0 , 100, 1.0);
    line->SetLineColor(2);
    line->Draw("same");
    //
    if (!DATA){
      c3->cd(ib+1); 
      hh_data_sel[ib]->SetMaximum(50);
      hh_data_sel[ib]->SetMinimum(0);
      hh_data_sel[ib]->SetFillColor(3);
      hh_data_sel[ib]->Draw();
      TH1F* cici=(TH1F*)hh_data_sel[ib]->Clone();
      cici->Add(hh_wenu_sel[ib],-1);
      cici->SetFillColor(2); 
      cici->Draw("same"); 
      TH1F* cucu=(TH1F*)cici->Clone();
      cucu->Add(hh_ewk_sel[ib],-1);
      cucu->SetFillColor(5);
      cucu->Draw("same");

      if (ib==0){
        l5_0->AddEntry(hh_data_sel[ib],"W->e#nu","f");
        l5_0->AddEntry(cici,"EWK","f");
        l5_0->AddEntry(cucu,"QCD","f");
        l5_0->Draw();
      }

    }
    
    
  }
  ASY=POS->GetAsymmetry(NEG);
  int SystCont=4;
  float systPos[6][4];
  float systNeg[6][4];
  cout<<"SW "<<endl;
  for (int ibin=0;ibin<6;ibin++){
    for (int icon=0;icon<SystCont;icon++){
      systPos[ibin][icon]=0.;
      systNeg[ibin][icon]=0.;
    }   	
  }  
  c2->cd();

  //MISCHARGE RATE EFFECT
  float mischarge_rate[6]={0.0,0.0,0.0,0.0018,0.0025,0.0039};
  float mischarge_max[6]={0.0008,0.0007,0.0007,0.0043,0.0055,0.0082};
  float mischarge_min[6]={0.0,0.0,0.0,0.0004,0.0008,0.0026};
  for (int ibin=0; ibin<6; ibin++){
    systPos[ibin][0]=ASY->GetBinContent(ibin+1)*((1/(1-2*mischarge_max[ibin]))-(1/(1-2*mischarge_rate[ibin])));
    systNeg[ibin][0]=ASY->GetBinContent(ibin+1)*((1/(1-2*mischarge_rate[ibin]))-(1/(1-2*mischarge_min[ibin])));
    ASY->SetBinContent(ibin+1,ASY->GetBinContent(ibin+1)/(1-2*mischarge_rate[ibin]));
  }
  
  //RELATIVE EFFICIENCY
  
  TH1F *NEGP=(TH1F*)NEG->Clone();
  TH1F *NEGM=(TH1F*)NEG->Clone();
  float Deltaerr[6]={0.018,0.018,0.018,0.018,0.018,0.018}; 
  for (int  ibin=0; ibin<6; ibin++){
    NEGP->SetBinContent(ibin+1,NEG->GetBinContent(ibin+1)*(1.+Deltaerr[ibin]));
    NEGM->SetBinContent(ibin+1,NEG->GetBinContent(ibin+1)*(1.-Deltaerr[ibin]));
  }

  TH1F *ASYP=POS->GetAsymmetry(NEGP);
  TH1F *ASYM=POS->GetAsymmetry(NEGM);
  for (int  ibin=0; ibin<6; ibin++){
    ASYP->SetBinContent(ibin+1,ASYP->GetBinContent(ibin+1)/(1-2*mischarge_rate[ibin]));
    ASYM->SetBinContent(ibin+1,ASYM->GetBinContent(ibin+1)/(1-2*mischarge_rate[ibin]));    
    systNeg[ibin][1]=ASY->GetBinContent(ibin+1)-ASYP->GetBinContent(ibin+1);
    systPos[ibin][1]=ASYM->GetBinContent(ibin+1)-ASY->GetBinContent(ibin+1);
  }
  float systRes[6]={0.0007,0.0008,0.0018,0.0045,0.0035,0.0051};
  for (int  ibin=0; ibin<6; ibin++){
    systNeg[ibin][2]=systRes[ibin];
    systPos[ibin][2]=systRes[ibin];
  }

  ASY->GetXaxis()->SetTitle("|#eta|");
  ASY->GetYaxis()->SetTitle("Asymmetry");
  ASY->SetTitle("Electron Charge Asymmetry");
  ASY->SetMarkerColor(1); 
  ASY->SetLineColor(1); 
  ASY->SetMarkerStyle(20);
  ASY->SetMarkerColor(1);
  ASY->SetLineColor(1);
  ASY->SetMarkerStyle(20);
  ASY->SetMinimum(-0.0);
  ASY->SetMaximum(+0.5); 
  
  ASY->Draw();
  
  float totsystmax[6]={0.,0.,0.,0.,0.,0.};
  float totsystmin[6]={0.,0.,0.,0.,0.,0.};

  for (int it=0; it<6;it++){
    float errsystmin=0;
    float errsystmax=0; 
    for (int icon=0; icon<SystCont;icon++){
      errsystmax+=(systPos[it][icon]*systPos[it][icon]);
         errsystmin+=(systNeg[it][icon]*systNeg[it][icon]);         
    }
    totsystmax[it]=sqrt(errsystmax); 
    totsystmin[it]=sqrt(errsystmin);  
  } 
  
  for (int ibi=0; ibi<6;ibi++){
	cout<<"BIN "<<ibi+1<<" "<<int(10000*ASY->GetBinContent(ibi+1))/10000.<<" +/- "
	<<int(10000.*ASY->GetBinError(ibi+1))/10000.<<" (stat) +"
	<<int(10000.*totsystmax[ibi])/10000.<<" - " 
	<<int(10000.*totsystmin[ibi])/10000.<<endl;
  }
		
  TH1F *ASYSYST= (TH1F*)ASY->Clone(); 
  for (int ibi=0; ibi<6;ibi++){
    float stat=ASY->GetBinError(ibi+1);
    float syst=max(totsystmax[ibi],totsystmin[ibi]);
    float toterr=sqrt(stat*stat+syst*syst);
    ASYSYST->SetBinError(ibi+1,toterr);
  }
  c2->cd(); 
  ASYSYST->SetMarkerColor(2);
  ASYSYST->SetLineColor(2);

  ASYSYST->Draw();
  ASY->Draw("same");

  l5_4->AddEntry(ASY,"Only Statistical","l");
  l5_4->AddEntry(ASYSYST,"Stat. + Syst. error","l");
  
  if (DATA) {
    l5_4->Draw("same");
    c2->SaveAs(SAVDIR+"asy"+FORMAT);
    c1->SaveAs(SAVDIR+"data"+FORMAT);
  }
  if(!DATA){
    l5_4->Draw("same");
    c2->SaveAs(SAVDIR+"final"+FORMAT);
    c3->SaveAs(SAVDIR+"PfMETbins"+FORMAT); 
  }
  c4->SaveAs(SAVDIR+"fitratio"+FORMAT);
  c0->SaveAs(SAVDIR+"roofit"+FORMAT);
}

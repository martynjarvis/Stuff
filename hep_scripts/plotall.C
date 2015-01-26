#include "variables.C"
#include "correlations.C"
#include "efficiencies.C"
#include "mvas.C"
#include "likelihoodrefs.C"
#include "BDTControlPlots.C"

void plotall( TString fin)
{
cout<<fin<<endl;
gROOT->SetBatch();
  cout << "=== execute: variables()" << endl;
  variables( fin, "InputVariables_Id", "TMVA Input Variables",false, false );

  cout << "=== execute: correlations()" << endl;
  correlations( fin, false,false,false);

  cout << "=== execute: mvas()" << endl;
  mvas( fin ,0, false);
  mvas( fin,3 , false);

  cout << "=== execute: efficiencies()" << endl;
  efficiencies( fin ,2, false);

  cout << "=== execute: liklihoodrefs()" << endl;
  likelihoodrefs( fin , false);

  //cout << "=== execute: BDTControlPlots()" << endl;
  //BDTControlPlots(fin , false);

}

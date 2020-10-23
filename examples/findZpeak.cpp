#include <TChain.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TH1F.h>
#include <string>
#include <iostream>

std::string const DATADIR = "./data/";

int main(){

  TChain ch("Z/DecayTree");

  std::string const sqrts = "5"/*TeV*/,
    stripping = "32",
    year = "2017",
    polarity = "Down",
    stream = "EW";
  std::string const path = DATADIR + sqrts + "TeV_" + year + "_" + stripping + "_" + polarity + "_" + stream + ".root";

  ch.Add(path.c_str());

  int const nbins = 100;
  float const xmin = 10.,
    xmax = 400.;

  TH1F hist("hist_name","Z Boson Mass Fit",nbins,xmin,xmax);

  std::string expression = "1E-3*sqrt(2*((mup_PT*cosh(mup_ETA))*(mum_PT*cosh(mum_ETA))*(1-cos((2*atan(exp(-mup_ETA)))+(2*atan(exp(-mum_ETA)))))))>>";
  expression += hist.GetName();

  ch.Draw(expression.c_str());

  TLine l = TLine(91.19,5.,91.19,1900);
  l.SetLineColor(kRed);
  l.Draw();

  TCanvas canv;
  canv.Range( xmin, 0., xmax, 150. );

  hist.Draw();
  l.Draw();

  canv.SaveAs("plot.pdf");

  return 0;
}

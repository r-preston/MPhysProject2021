#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <string>
#include <iostream>

std::string const DATADIR = "/storage/epp2/phshgg/MPhysProject2021/";

int main(){

  TChain ch("WpIso/DecayTree");

  std::string const sqrts = "5"/*TeV*/,
    stripping = "32",
    year = "2017",
    polarity = "Down",
    stream = "EW";
  std::string const path = DATADIR + sqrts + "TeV_" + year + "_" + stripping + "_" + polarity + "_" + stream + ".root";

  ch.Add(path.c_str());

  int const nbins = 100;
  float const xmin = 15.,
    xmax = 60.;

  TH1F hist("hist_name","title",nbins,xmin,xmax);

  std::string expression = "1.e-3*mu_PT>>";
  expression += hist.GetName();

  ch.Draw(expression.c_str());

  TCanvas canv;

  hist.Draw();

  canv.SaveAs("plot.pdf");

  return 0;
}
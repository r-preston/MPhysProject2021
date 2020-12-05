#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TH2F.h>
#include <THStack.h>
#include <TMath.h>
#include <string>
#include <vector>
#include <iostream>

std::string const DATADIR = "/storage/epp2/phshgg/DVTuples__v23/";
std::string const plots_dir = "plots/";

struct path_data {
  std::string const DATADIR,
    sqrts,
    stripping,
    year,
    polarity,
    stream;
};

struct plot_config {
  std::string const charge,
    chain,
    expression;
  int const nbins;
  float const xmin,
    xmax;
  std::string const label,
    unit;

  //create constructor to allow struct to configure correctly in the emplace_back function
  plot_config(std::string const charge, std::string const chain, std::string const expression, int const nbins, float const xmin, float const xmax, std::string const label, std::string const unit)
    :charge(std::move(charge))
    ,chain(std::move(chain))
    ,expression(std::move(expression))
    ,nbins(nbins)
    ,xmin(xmin)
    ,xmax(xmax)
    ,label(std::move(label))
    ,unit(std::move(unit))
  {}
};

struct plot_config_2D {
  std::string const charge,
    chain;
  int const xbins, 
    ybins;
  float const xmin,
    xmax,
    ymin,
    ymax;
};

std::vector<plot_config> plot_configurations;

TH1F* make_TH1F(struct path_data path_in, struct plot_config hist_input, std::string hist_name, std::string hist_text) {
  TChain ch(hist_input.chain.c_str());
  std::string path = path_in.DATADIR + path_in.sqrts + "TeV_" + path_in.year + "_" + path_in.stripping + "_" + path_in.polarity + "_" + path_in.stream + ".root";
  ch.Add(path.c_str());
  
  TH1F *hist = new TH1F(hist_name.c_str(), hist_text.c_str(), hist_input.nbins, hist_input.xmin, hist_input.xmax);
  std::string expression = hist_input.expression +">>"+ hist->GetName();
  ch.Draw(expression.c_str());
  return hist;
}


void plot_data(struct path_data path_in, struct plot_config hist_input) {

  std::string x_axis = hist_input.label + " " + hist_input.unit,
    hist_text = ";" + x_axis + ";Events",
    hist_name = hist_input.label + " " +  hist_input.charge + " Experimental Data";

  TH1F *hist = make_TH1F(path_in, hist_input, hist_input.charge, hist_text);

  hist->SetName(hist_name.c_str());
	
  TCanvas canv;
  hist->SetStats(false);
  hist->Draw("E");

  canv.BuildLegend();
  std::string const filename = plots_dir + hist_input.charge +  "_distribution_" + hist_input.label + ".pdf";
  canv.SaveAs(filename.c_str());
}


void isolate_signal(struct path_data path_in, struct plot_config_2D hist_input) {
  TChain ch(hist_input.chain.c_str());
  std::string path = path_in.DATADIR + path_in.sqrts + "TeV_" + path_in.year + "_" + path_in.stripping + "_" + path_in.polarity + "_" + path_in.stream + ".root";
  ch.Add(path.c_str());
  
  TH2F *hist = new TH2F("twoDtest",";Isolation;1/mu_PT", hist_input.xbins, hist_input.xmin, hist_input.xmax, hist_input.ybins, hist_input.ymin, hist_input.ymax);
    std::string x_expression = "TMath::Log10(TMath::Max(0.1,1.e-3*mu_PTSUMCONE040))", 
    y_expression = "1/(1.e-3*mu_PT)",
    expression = y_expression + ":" + x_expression + ">>" + hist->GetName();

  ch.Draw(expression.c_str());

  std::string hist_title = hist_input.charge + " isolated signal data";

  hist->SetName(hist_title.c_str());
  TCanvas canv;
  hist->SetStats(false);
  hist->Draw("E");

  canv.BuildLegend();
  std::string const filename = plots_dir + hist_input.charge + "_isolated_signal.pdf";
  canv.SaveAs(filename.c_str());
  return;
}


int main() {
  
  /*Measurement Chain*/
  path_data const path = {DATADIR, "5", "32", "2017", "Down", "EW"};

  //W+
  plot_configurations.emplace_back("W+","WpIso/DecayTree","1.e-3*mu_PT", 100, 15., 60., "mu_PT", "(GeV)");
  //W-
  plot_configurations.emplace_back("W-","WmIso/DecayTree","1.e-3*mu_PT", 100, 15., 60., "mu_PT", "(GeV)");

  for (auto const & plot_configuration : plot_configurations) {
    plot_data(path, plot_configuration);
  }

  plot_config_2D Wp_config = {"W+","WpIso/DecayTree", 100, 100, 0., 2.5, 0., 0.068}; 
  plot_config_2D Wm_config = {"W-","WmIso/DecayTree", 100, 100, 0., 2.5, 0., 0.068}; 
  

  isolate_signal(path, Wp_config);
  isolate_signal(path, Wm_config);

  return 0;
}

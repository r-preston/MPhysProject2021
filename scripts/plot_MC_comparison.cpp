#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <THStack.h>
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
	std::string const expression;
	int const nbins;
	float const xmin,
	xmax;
	std::string const label,
	unit;

  //create constructor to allow struct to configure correctly in the emplace_back function
  plot_config(std::string const expression, int const nbins, float const xmin, float const xmax, std::string const label, std::string const unit)
    :expression(std::move(expression))
    ,nbins(nbins)
    ,xmin(xmin)
    ,xmax(xmax)
    ,label(std::move(label))
    ,unit(std::move(unit))
  {}
};

std::vector<plot_config> plot_configurations;


TH1F* make_TH1F(struct path_data path_in, struct plot_config hist_input, std::string hist_name, std::string hist_text) {
	TChain ch("Z/DecayTree");
	std::string path = path_in.DATADIR + path_in.sqrts + "TeV_" + path_in.year + "_" + path_in.stripping + "_" + path_in.polarity + "_" + path_in.stream + ".root";
	ch.Add(path.c_str());
	
	TH1F *hist = new TH1F(hist_name.c_str(), hist_text.c_str(), hist_input.nbins, hist_input.xmin, hist_input.xmax);
	std::string expression = hist_input.expression +">>"+ hist->GetName();
	ch.Draw(expression.c_str());
	//hist->SetTitle("");
	return hist;
}

void plot_data_sim(struct path_data mnt_in, struct path_data sim_in, struct plot_config hist_input) {

        std::string x_axis = hist_input.label + " " + hist_input.unit,
	  sim_name = hist_input.label + " Simulation Data",
	  hist_text = ";" + x_axis,
	  mnt_name = hist_input.label + " Experimental Data";
	//std::string hist_title = "Measurement vs Simulation for " + hist_input.label;

	TH1F *hist_mnt = make_TH1F(mnt_in, hist_input, "measurement", hist_text);
	TH1F *hist_sim = make_TH1F(sim_in, hist_input, "simulation", hist_text);
	
	hist_mnt->SetName(mnt_name.c_str());
	hist_sim->SetName(sim_name.c_str());

	hist_sim->Scale(hist_mnt->Integral()/hist_sim->Integral());
	
	float ymax,
	  ymax_mnt = hist_mnt->GetMaximum(),
	  ymax_sim = hist_sim->GetMaximum();
	if (ymax_mnt > ymax_sim) {
	  ymax = 1.15*ymax_mnt;
	}
	else {
	  ymax = 1.15*ymax_sim;
	}

	TCanvas canv;
	hist_mnt->SetStats(false);
	hist_mnt->Draw("E");
	hist_sim->Draw("SAME HIST");
     	hist_mnt->GetYaxis()->SetRangeUser(0,ymax);
	hist_sim->SetLineColor(kAzure);

	canv.BuildLegend();
	std::string const filename = plots_dir + "Measurement_" + hist_input.label + ".pdf";
	canv.SaveAs(filename.c_str());
}

int main() {

	/*Measurement Chain*/
	path_data const measurement_in = {DATADIR, "5", "32", "2017", "Down", "EW"};

	/*Simulation Chain*/
	path_data const simulation_in = {DATADIR, "13", "28r1", "2016", "Down", "Z_Sim09h"};
	
	//mup
	plot_configurations.emplace_back("1.e-3*mup_PT", 100, 15., 60., "mup_PT", "(GeV)");
	plot_configurations.emplace_back("mup_ETA", 100, 1.5, 5., "mup_ETA", "");
	plot_configurations.emplace_back("mup_PHI", 100, -4., 4., "mup_PHI", "");
	//mum
	plot_configurations.emplace_back("1.e-3*mum_PT", 100, 15., 60., "mum_PT", "(GeV)");
	plot_configurations.emplace_back("mum_ETA", 100, 1.5, 5., "mum_ETA", "");
	plot_configurations.emplace_back("mum_PHI", 100, -4., 4., "mum_PHI", "");
	//dimuon
	plot_configurations.emplace_back("1.e-3*Z_M", 100, 35, 120, "Z_M", "(GeV)");

	for (auto const & plot_configuration : plot_configurations) {
	  plot_data_sim(measurement_in, simulation_in, plot_configuration);
	}
	
	return 0;
}

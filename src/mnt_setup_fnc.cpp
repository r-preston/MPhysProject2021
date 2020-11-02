#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <THStack.h>
#include <string>
#include <iostream>

std::string const DATADIR = "/storage/epp2/phshgg/DVTuples__v23/";

struct path_data {
	std::string const DATADIR,
	sqrts,
	stripping,
	year,
	polarity,
	stream;
};

struct input {
	std::string const expression;
	int const nbins;
	float const xmin,
	xmax;
	std::string const label,
	unit;
};

TH1F* make_TH1F(struct path_data path_in, struct input hist_input, std::string hist_name, std::string hist_setup) {
	TChain ch("Z/DecayTree");
	std::string path = path_in.DATADIR + path_in.sqrts + "TeV_" + path_in.year + "_" + path_in.stripping + "_" + path_in.polarity + "_" + path_in.stream + ".root";
	ch.Add(path.c_str());
	
	TH1F *hist = new TH1F(hist_name.c_str(), hist_setup.c_str(), hist_input.nbins, hist_input.xmin, hist_input.xmax);
	std::string expression = hist_input.expression +">>"+ hist->GetName();
	ch.Draw(expression.c_str());
	return hist;
}

void plot_histogram(struct path_data mnt_in, struct path_data sim_in, struct input hist_input) {
	std::string hist_title = "Measurement vs Simulation for " + hist_input.label,
		x_axis = hist_input.label + " " + hist_input.unit,
		hist_text = hist_title + ";" + x_axis;
	
	TH1F *hist_mnt = make_TH1F(mnt_in, hist_input, "measurement", hist_text);
	TH1F *hist_sim = make_TH1F(sim_in, hist_input, "simulation", hist_text);
	
	hist_sim->Scale(hist_mnt->Integral()/hist_sim->Integral());
	
	TCanvas canv;
	hist_sim->SetStats(false);
	hist_sim->Draw("HIST");
	hist_mnt->Draw("SAME E");
	std::string const filename = "Measurement_" + hist_input.label + ".png";
	canv.SaveAs(filename.c_str());
}

int main() {

	/*Measurement Chain*/
	path_data const measurement_in = {DATADIR, "5", "32", "2017", "Down", "EW"};

	/*Simulation Chain*/
	path_data const simulation_in = {DATADIR, "13", "28r1", "2016", "Down", "Z_Sim09h"};
	
	
	/*input property_in = {"expression", nbins, xmin., xmax., "label", "unit"};
	plot_histogram(measurement_in, simulation_in, property_in);*/
	
	/*mup*/
	input const mup_PT_in = {"1.e-3*mup_PT", 100, 15., 60., "mup_PT", "(GeV)"};
	plot_histogram(measurement_in, simulation_in, mup_PT_in);
	
	input const mup_ETA_in = {"mup_ETA", 100, 1.5, 5., "mup_ETA", ""};
	plot_histogram(measurement_in, simulation_in, mup_ETA_in);
	
	input const mup_PHI_in = {"mup_PHI", 100, -4., 4., "mup_PHI", ""};
	plot_histogram(measurement_in, simulation_in, mup_PHI_in);
	
	/*mum*/
	input const mum_PT_in = {"1.e-3*mum_PT", 100, 15., 60., "mum_PT", "(GeV)"};
	plot_histogram(measurement_in, simulation_in, mum_PT_in);
	
	input const mum_ETA_in = {"mum_ETA", 100, 1.5, 5., "mum_ETA", ""};
	plot_histogram(measurement_in, simulation_in, mum_ETA_in);
	
	input const mum_PHI_in = {"mum_PHI", 100, -4., 4., "mum_PHI", ""};
	plot_histogram(measurement_in, simulation_in, mum_PHI_in);
	
	/*dimuon*/
	input const Z_M_in = {"1.e-3*Z_M", 100, 35, 120, "Z_M", "(GeV)"};
	plot_histogram(measurement_in, simulation_in, Z_M_in);
	
	
	return 0;
}

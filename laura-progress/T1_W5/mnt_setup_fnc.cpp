#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <THStack.h>
#include <string>
#include <iostream>

std::string const DATADIR = "/storage/epp2/phshgg/DVTuples__v23/";

struct path_data {
	std::string const DATADIR;
	std::string sqrts,
	stripping,
	year,
	polarity,
	stream;
};

void make_histogram(struct path_data path_in, std::string hist_name, std::string hist_setup, int const nbins, float const xmin, float const xmax, std::string expression, THStack *hist_stack) {
	TChain ch("Z/DecayTree");
	std::string path = path_in.DATADIR + path_in.sqrts + "TeV_" + path_in.year + "_" + path_in.stripping + "_" + path_in.polarity + "_" + path_in.stream + ".root";
	ch.Add(path.c_str());
	
	TH1F *hist = new TH1F(hist_name.c_str(), hist_setup.c_str(), nbins, xmin, xmax);
	expression += hist->GetName();
	ch.Draw(expression.c_str());
	hist_stack->Add(hist);
}


int main() {

	/*Measurement Chain*/
	path_data measurement_in = {DATADIR, "5", "32", "2017", "Down", "EW"};

	/*Simulation Chain*/
	path_data simulation_in = {DATADIR, "13", "28r1", "2016", "Down", "Z_Sim09h"};
	
	/*Branch Input*/
	std::string const muon_prop = "mum_PHI",
		muon_prop_unit = " ";
	
	/*Histogram Set-up*/
	std::string hist_title = "Measurement vs Simulation for " + muon_prop,
		x_axis = muon_prop + muon_prop_unit,
		hist_setup = hist_title + ";" + x_axis,
		expression = muon_prop + ">>";
		/*expression = "1.e-3*" + muon_prop + ">>"; version for PT in GeV*/
	
	int const nbins = 100;
	float const xmin = -4.,
		xmax = 4.;
	
	/*Make Histogram*/
	THStack *hist_main = new THStack(muon_prop.c_str(), hist_setup.c_str());
	
	make_histogram(measurement_in, "measurement", hist_setup, nbins, xmin, xmax, expression, hist_main);
	make_histogram(simulation_in, "simulation", hist_setup, nbins, xmin, xmax, expression, hist_main);
	
	TCanvas canv;
	hist_main->Draw("E");
	std::string const filename = "Measurement_" + muon_prop + ".pdf";
	canv.SaveAs(filename.c_str());
	
	return 0;
}

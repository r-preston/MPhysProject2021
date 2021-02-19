#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <THStack.h>
#include <string>
#include <TF1.h>
#include <TLegend.h>
#include <TPaveStats.h>
#include <TMath.h>
#include <TFractionFitter.h>
#include <math.h>
#include <iostream>
#include <fstream>

std::string const data_file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root";
std::string const W_sim_file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2015_24r1_Down_W_Sim09d.root";
std::string const Z_sim_file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2015_24r1_Down_Z_Sim09d.root";
std::string const plots_dir = "plots/";

struct fit_fractions {
  double K_frac, 
    K_err, 
    sim_frac, 
    sim_err, 
    Z_frac, 
    Z_err,
    chi_squared;
  int ndf;
  std::string K_label,
    sim_label,
    Z_label,
    chi_squared_ndf;
};


void output_histogram(TH1F* histogram, std::string name) {
  // prints histogram for testing purposes
  TCanvas canv;
  histogram->Draw("HIST");
  histogram->SetStats(false);
  histogram->GetXaxis()->CenterTitle(true);
  histogram->GetYaxis()->CenterTitle(true);
  canv.BuildLegend();
  std::string filename = plots_dir + name + ".png";
  canv.SaveAs(filename.c_str());
  canv.Close();
  return;
}


TH1F* make_histogram(std::string input_path, std::string chain, std::string hist_name, double x_low, double x_high, std::string in_expression, std::string cuts) {
  std::string full_chain = chain + "/DecayTree";
  TChain ch(full_chain.c_str());
  ch.Add(input_path.c_str());

  TH1F *hist = new TH1F(hist_name.c_str(),";p_{T} (GeV);Events",100,x_low,x_high);
  std::string expression = in_expression + ">>" + hist_name;
  ch.Draw(expression.c_str(), cuts.c_str());
  return hist;
}


TH1F* background_fit(std::string chain, std::string boson, double slope) {

  std::string full_chain = chain + "/DecayTree";
  TChain ch(full_chain.c_str());
  ch.Add(data_file_path.c_str());
  
  std::string hist_name = "W" + boson + "hist_back";
  TH1F *hist_back = new TH1F(hist_name.c_str(),";p_{T} (GeV);Events",100,15.,60.);
  std::string expression = "mu_PT*1.e-3>>" + hist_name;
  ch.Draw(expression.c_str());
  
  TF1 *function = new TF1("expo_fit","[0]*TMath::Exp(-[1]*x)",15.,60.);
  function->SetParameter(0,1.);
  function->SetParameter(1,1.);
  hist_back->Fit(function->GetName());
  function->SetLineColor(2);
  
  // output plot with fit
  TCanvas canv1;
  hist_back->Draw();
  hist_back->GetXaxis()->CenterTitle(true);
  hist_back->GetYaxis()->CenterTitle(true);
  hist_back->GetXaxis()->SetTitleSize(0.04);
  hist_back->GetXaxis()->SetLabelSize(0.04);
  hist_back->GetYaxis()->SetTitleOffset(1);
  hist_back->GetYaxis()->SetTitleSize(0.04);
  hist_back->GetYaxis()->SetLabelSize(0.04);

  canv1.Update();
  canv1.Modified();
  TPaveStats *st = (TPaveStats*)hist_back->FindObject("stats");
  st->SetOptStat(0);
  st->SetOptFit(1111);
  st->SetX1NDC(0.55);
  st->SetX2NDC(0.9);
  st->SetY1NDC(0.6);
  st->SetY2NDC(0.78);
  st->Draw();  
  TLegend *legend = new TLegend(0.4,0.78,0.9,0.9);
  std::string plot_label = "W^{" + boson + "} Track Transverse Momentum";
  legend->AddEntry(hist_back,plot_label.c_str(),"l");
  legend->AddEntry(function, "Exponential Fit", "l");
  legend->SetTextSize(0.04);
  legend->Draw();

  std::string const filename = plots_dir + "W" + boson + "_expo_back_plot.png";
  canv1.SaveAs(filename.c_str());
  canv1.Close();

  // make background template from fit
  function->SetParameter(1,slope);
  std::string template_name = "W^{" + boson + "} Background Template from Exp Fit"; 
  TH1F *background_template = new TH1F(template_name.c_str(),";p_{T} (GeV);Events",100,20.,60.);
  for (int i=0; i<100000; i++) {background_template->Fill(function->GetRandom());}

  return background_template;
}


void produce_fit_model(std::string boson, fit_fractions fractions, TH1F* hist_iso, TH1F* hist_sim, TH1F* background_template, TH1F* Z_background, std::string name) {
  hist_sim->Scale(fractions.sim_frac*hist_iso->Integral()/hist_sim->Integral()); //data_integral/signal_integral
  background_template->Scale(fractions.K_frac*hist_iso->Integral()/background_template->Integral()); //data_integral/background_integral
  Z_background->Scale(fractions.Z_frac*hist_iso->Integral()/Z_background->Integral());

  TH1F *fit_model = new TH1F(name.c_str(),";p_{T} (GeV); Events",100,20.,60.);
  fit_model->Add(hist_sim, background_template);
  fit_model->Add(Z_background);

  TCanvas fit_canv;
  fit_model->Draw("HIST");
  //fit_model->SetFillColor(5);
  background_template->Draw("SAME HIST");
  background_template->SetLineColor(4);
  //background_template->SetFillColor(4);
  hist_iso->Draw("SAME E");
  hist_sim->Draw("SAME HIST");
  hist_sim->SetLineColor(2);
  Z_background->Draw("SAME HIST");
  Z_background->SetLineColor(8);
  
  fit_model->SetStats(false);
  fit_model->GetXaxis()->CenterTitle(true);
  fit_model->GetXaxis()->SetTitleOffset(1.1);
  fit_model->GetYaxis()->CenterTitle(true);
  fit_model->GetYaxis()->SetTitleOffset(1.5);

  TLegend *fit_legend = new TLegend(0.5,0.68,0.9,0.9);
  std::string boson_label = "W^{" + boson + "} ",
    fit_label = boson_label + "Fit Model",
    signal_label = boson_label + "Signal Histogram",
    data_label = boson_label + "Data Histogram";
  fit_legend->AddEntry(fit_model, fit_label.c_str(), "l");
  fit_legend->AddEntry(background_template, "K/#pi #rightarrow #mu#nu", "l");
  fit_legend->AddEntry(hist_sim, signal_label.c_str(), "l");
  fit_legend->AddEntry(Z_background, "Z Background", "l");
  fit_legend->AddEntry(hist_iso, data_label.c_str(), "lep"); //"Isolated W^{+} Signal", "lep");
  fit_legend->Draw();
    
  TPaveText *statBox = new TPaveText(0.55,0.46,0.9,0.68, "NDC");
  statBox->SetFillStyle(0);
  statBox->SetTextAlign(12);
  statBox->AddText(fractions.K_label.c_str());
  statBox->AddText(fractions.sim_label.c_str());
  statBox->AddText(fractions.Z_label.c_str());
  statBox->AddText(fractions.chi_squared_ndf.c_str());
  statBox->SetBorderSize(1); //removes shadow
  statBox->SetTextFont(fit_legend->GetTextFont());
  statBox->Draw();    


  std::string const fit_filename = plots_dir + "W" + boson + "_fit_model.png";
  fit_canv.SaveAs(fit_filename.c_str());
  fit_canv.Close();
}


fit_fractions fraction_fitter(std::string boson, double Z_fraction, double Z_error, TH1F* hist_iso, TH1F* hist_sim, TH1F* background_template, TH1F* Z_background) {
  fit_fractions output;
  TCanvas fraction_canv;
  TObjArray *mc = new TObjArray(3);
  mc->Add(background_template);
  mc->Add(hist_sim);
  mc->Add(Z_background);
  TFractionFitter *fit = new TFractionFitter(hist_iso, mc);
  fit->Constrain(2,Z_fraction-Z_error,Z_fraction+Z_error);
  //ROOT::Fit::Fitter *fitter = fit->GetFitter();
  //fitter->SetParameter(2, "Z_background", 0.2, 0., 0.2, 0.2);
  //fitter->Config().ParSettings(2).Set("Z_background",0.2,0.,0.2,0.2); //name,value,step,lower bound,upper bound
  Int_t status = fit->Fit();
  std::cout << "fit status: " << status;
  if (status == 0) {
    TH1F *result = (TH1F*) fit->GetPlot();
    hist_iso->Draw("E");
    result->Draw("SAME");

    hist_iso->SetStats(false);
    hist_iso->GetXaxis()->CenterTitle(true);
    hist_iso->GetYaxis()->CenterTitle(true);

    fit->GetResult(0, output.K_frac, output.K_err);
    fit->GetResult(1, output.sim_frac, output.sim_err);
    fit->GetResult(2, output.Z_frac, output.Z_err);
    std::string K_frac_str = std::to_string(round(output.K_frac*1000)/1000); K_frac_str.resize(5);
    std::string K_err_str = std::to_string(round(output.K_err*1000)/1000); K_err_str.resize(5);
    std::string sim_frac_str = std::to_string(round(output.sim_frac*1000)/1000); sim_frac_str.resize(5);
    std::string sim_err_str = std::to_string(round(output.sim_err*1000)/1000); sim_err_str.resize(5);
    std::string Z_frac_str = std::to_string(round(output.Z_frac*1000)/1000); Z_frac_str.resize(5);
    std::string Z_err_str = std::to_string(round(output.Z_err*1000)/1000); Z_err_str.resize(5);
    output.K_label = "K/#pi #rightarrow #mu#nu: " + K_frac_str + " #pm " + K_err_str;
    output.sim_label = "Signal Simulation: " + sim_frac_str + " #pm " + sim_err_str;
    output.Z_label = "Z background: " + Z_frac_str + " #pm " + Z_err_str;

    output.chi_squared = fit->GetChisquare();
    output.ndf = fit->GetNDF();
    std::string chi_squared_str = std::to_string(round(output.chi_squared*10)/10); chi_squared_str.resize(5);
    output.chi_squared_ndf = "#chi^{2}/ndf: " + chi_squared_str + "/" + std::to_string(output.ndf); 
    
    TLegend *fraction_legend = new TLegend(0.5,0.76,0.9,0.9);
    std::string data_label = "Isolated W^{" + boson + "} Data";
    fraction_legend->AddEntry(hist_iso, data_label.c_str(), "lep");
    fraction_legend->AddEntry(result, "Fit from TFractionFitter", "l");
    fraction_legend->Draw();

    TPaveText *statBox = new TPaveText(0.55,0.56,0.9,0.76, "NDC");
    statBox->SetFillStyle(0);
    statBox->SetTextAlign(12);
    statBox->AddText(output.K_label.c_str());
    statBox->AddText(output.sim_label.c_str());
    statBox->AddText(output.Z_label.c_str());
    statBox->AddText(output.chi_squared_ndf.c_str());
    statBox->SetBorderSize(1); //removes shadow
    statBox->SetTextFont(fraction_legend->GetTextFont());
    statBox->Draw();    
  }
  std::string const fraction_filename = plots_dir + "W" + boson + "_fraction_fit.png";
  fraction_canv.SaveAs(fraction_filename.c_str());
  fraction_canv.Close();
  return output;
}


void output_values(std::string boson, double Z_frac, double Z_err, fit_fractions fractions, double signal_events, double W_in_Z_sim_events, double W_data_events, double Z_data_events, double Z_in_Z_sim_events) {
  std::string file_name = "results_json/" + boson + "_back_output.json";
  std::ofstream output_file;
  output_file.open(file_name.c_str());
  if (output_file.is_open()) {
    // output calculated Z fraction
    output_file << "{\"Z_frac_calc\": " + std::to_string(Z_frac) + ", \"Z_frac_err_calc\": " + std::to_string(Z_err);
    // output fit fractions and fit statistics
    output_file << ", \"K_frac\": " + std::to_string(fractions.K_frac) + ", \"K_frac_err\": " + std::to_string(fractions.K_err);
    output_file << ", \"signal_frac\": " + std::to_string(fractions.sim_frac) + ", \"signal_frac_err\": " + std::to_string(fractions.sim_err);
    output_file << ", \"Z_frac\": " + std::to_string(fractions.Z_frac) + ", \"Z_frac_err\": " + std::to_string(fractions.Z_err);
    output_file << ", \"chi_squared\": " + std::to_string(fractions.chi_squared) + ", \"ndf\": " + std::to_string(fractions.ndf);
    // output numbers of events
    output_file << ", \"pi_K_events\": 10000";
    output_file << ", \"signal_events\": " + std::to_string(signal_events);
    output_file << ", \"W_in_Z_sim_events\": " + std::to_string(W_in_Z_sim_events);
    output_file << ", \"W_data_events\": " + std::to_string(W_data_events);
    output_file << ", \"Z_data_events\": " + std::to_string(Z_data_events);
    output_file << ", \"Z_in_Z_sim_events\": " + std::to_string(Z_in_Z_sim_events);
    // end file
    output_file << "}";
    output_file.close();
  }
  else {printf("Error opening file %s\n", file_name.c_str());}
  return;
}


int main() {

  // make background template
  TH1F *Wp_background_template = background_fit("WpSingleTrackNoBias","+",0.2);
  TH1F *Wm_background_template = background_fit("WmSingleTrackNoBias","-",0.2);

  // initialise W cuts
  std::string isolation_cut = "TMath::Log10(TMath::Max(0.1,1.e-3*mu_PTSUMCONE040)) < 3", 
    pT_cut = "mu_PT*1.e-3 > 20",
    eta_cut = "mu_ETA > 2 && mu_ETA < 4.5",
    W_cuts = isolation_cut + " && " + pT_cut + " && " + eta_cut;
  std::string W_expression = "mu_PT*1e-3";
  // get isolated data
  TH1F *Wp_hist_iso = make_histogram(data_file_path, "WpIso", "Wp_hist_iso", 20., 60., W_expression, W_cuts);
  TH1F *Wm_hist_iso = make_histogram(data_file_path, "WmIso", "Wm_hist_iso", 20., 60., W_expression, W_cuts);
  double Wp_events_data = Wp_hist_iso->Integral();
  double Wm_events_data = Wm_hist_iso->Integral();
  
  // get signal data (simulation)
  TH1F *Wp_hist_sim = make_histogram(W_sim_file_path, "WpIso", "Wp_hist_sim", 20., 60., W_expression, W_cuts);
  TH1F *Wm_hist_sim = make_histogram(W_sim_file_path, "WmIso", "Wm_hist_sim", 20., 60., W_expression, W_cuts);
  double Wp_sim_events = Wp_hist_sim->Integral();
  double Wm_sim_events = Wm_hist_sim->Integral();

  // get Z background
  TH1F *Wp_Z_background = make_histogram(Z_sim_file_path, "WpIso", "Wp_Z_background", 20., 60., W_expression, W_cuts);
  double Wp_events_Z_sim = Wp_Z_background->Integral();
  TH1F *Wm_Z_background = make_histogram(Z_sim_file_path, "WmIso", "Wm_Z_background", 20., 60., W_expression, W_cuts);
  double Wm_events_Z_sim = Wm_Z_background->Integral();
  // get Z fraction
  std::string Z_cuts = "Z_M*1e-3 > 60 && Z_M*1e-3 < 120 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5";
  std::string Z_expression = "Z_M*1e-3";
  TH1F *hist_Z_events_data = make_histogram(data_file_path, "Z", "hist_Z_events_data", 60., 120., Z_expression, Z_cuts);
  double Z_events_data = hist_Z_events_data->Integral();
  TH1F *hist_Z_events_Z_sim = make_histogram(Z_sim_file_path, "Z", "hist_Z_events_Z_sim", 60., 120., Z_expression, Z_cuts);
  double Z_events_Z_sim = hist_Z_events_Z_sim->Integral();

  double Z_sim_scaling = Z_events_data/Z_events_Z_sim;
  double Wp_Z_frac = (Wp_events_Z_sim*Z_sim_scaling)/Wp_events_data;
  double Wp_Z_frac_err = Wp_Z_frac * (pow(Z_events_data,-0.5) + pow(Z_events_Z_sim,-0.5) + pow(Wp_events_data,-0.5) + pow(Wp_events_Z_sim,-0.5));
  double Wm_Z_frac = (Wm_events_Z_sim*Z_sim_scaling)/Wm_events_data;
  double Wm_Z_frac_err = Wm_Z_frac * (pow(Z_events_data,-0.5) + pow(Z_events_Z_sim,-0.5) + pow(Wm_events_data,-0.5) + pow(Wm_events_Z_sim,-0.5));
  
  // TFractionFitter
  fit_fractions Wp_fractions = fraction_fitter("+",Wp_Z_frac,Wp_Z_frac_err,Wp_hist_iso,Wp_hist_sim,Wp_background_template,Wp_Z_background);
  fit_fractions Wm_fractions = fraction_fitter("-",Wm_Z_frac,Wm_Z_frac_err,Wm_hist_iso,Wm_hist_sim,Wm_background_template,Wm_Z_background);

  // produce fit model and output data comparison
  produce_fit_model("+",Wp_fractions,Wp_hist_iso,Wp_hist_sim,Wp_background_template,Wp_Z_background, "Wp_fit_model");
  produce_fit_model("-",Wm_fractions,Wm_hist_iso,Wm_hist_sim,Wm_background_template,Wm_Z_background, "Wm_fit_model");

  /*
  printf("Wp Fraction = %lf + %lf\n",Wp_Z_frac,Wp_Z_frac_err);
  printf("Wm Fraction = %lf + %lf\n",Wm_Z_frac,Wm_Z_frac_err);
  printf("Z events in Wp = %lf, in Wm = %lf\n", Wp_events_Z_sim*Z_sim_scaling,Wm_events_Z_sim*Z_sim_scaling);
  printf("Entries: Z in Z data = %lf, Z in Z sim = %lf, Wp in Z sim = %lf, Wp total = %lf, Wm in Z sim = %lf, Wm total = %lf\n", Z_events_data, Z_events_Z_sim, Wp_events_Z_sim, Wp_events_data, Wm_events_Z_sim, Wm_events_data);
  printf("Signal entries: Wp = %lf, Wm = %lf\n", Wp_sim_events, Wm_sim_events);
  */

  // Output values
  output_values("Wp",Wp_Z_frac,Wp_Z_frac_err,Wp_fractions,Wp_sim_events,Wp_events_Z_sim,Wp_events_data,Z_events_data,Z_events_Z_sim);
  output_values("Wm",Wm_Z_frac,Wm_Z_frac_err,Wm_fractions,Wm_sim_events,Wm_events_Z_sim,Wm_events_data,Z_events_data,Z_events_Z_sim);

  return 0;
}

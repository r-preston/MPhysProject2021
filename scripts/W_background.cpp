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
    Z_err;
  std::string K_label,
    sim_label,
    Z_label;
};

struct events {
  double value,
    rel_err;
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


TH1F* make_histogram(std::string input_path, std::string chain, std::string hist_name, std::string cuts) {
  std::string full_chain = chain + "/DecayTree";
  TChain ch(full_chain.c_str());
  ch.Add(input_path.c_str());

  TH1F *hist = new TH1F(hist_name.c_str(),";p_{T} (GeV);Events",100,20.,60.);
  std::string expression = "mu_PT*1.e-3>>" + hist_name;
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
    
  TPaveText *statBox = new TPaveText(0.55,0.54,0.9,0.68, "NDC");
  statBox->SetFillStyle(0);
  statBox->SetTextAlign(12);
  statBox->AddText(fractions.K_label.c_str());
  statBox->AddText(fractions.sim_label.c_str());
  statBox->AddText(fractions.Z_label.c_str());
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
  //fitter->SetParameter(2,"Z_background",0.2,0.,0.,0.);
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
    std::string K_frac_s = std::to_string(round(output.K_frac*1000)/1000); K_frac_s.resize(5);
    std::string K_err_s = std::to_string(round(output.K_err*1000)/1000); K_err_s.resize(5);
    std::string sim_frac_s = std::to_string(round(output.sim_frac*1000)/1000); sim_frac_s.resize(5);
    std::string sim_err_s = std::to_string(round(output.sim_err*1000)/1000); sim_err_s.resize(5);
    std::string Z_frac_s = std::to_string(round(output.Z_frac*10000)/10000); Z_frac_s.resize(6);
    std::string Z_err_s = std::to_string(round(output.Z_err*10000)/10000); Z_err_s.resize(6);
    output.K_label = "K/#pi #rightarrow #mu#nu: " + K_frac_s + " #pm " + K_err_s;
    output.sim_label = "Signal Simulation: " + sim_frac_s + " #pm " + sim_err_s;
    output.Z_label = "Z background: " + Z_frac_s + " #pm " + Z_err_s;
    
    TLegend *fraction_legend = new TLegend(0.5,0.76,0.9,0.9);
    std::string data_label = "Isolated W^{" + boson + "} Data";
    fraction_legend->AddEntry(hist_iso, data_label.c_str(), "lep");
    fraction_legend->AddEntry(result, "Fit from TFractionFitter", "l");
    fraction_legend->Draw();

    TPaveText *statBox = new TPaveText(0.55,0.62,0.9,0.76, "NDC");
    statBox->SetFillStyle(0);
    statBox->SetTextAlign(12);
    statBox->AddText(output.K_label.c_str());
    statBox->AddText(output.sim_label.c_str());
    statBox->AddText(output.Z_label.c_str());
    statBox->SetBorderSize(1); //removes shadow
    statBox->SetTextFont(fraction_legend->GetTextFont());
    statBox->Draw();    
  }
  std::string const fraction_filename = plots_dir + "W" + boson + "_fraction_fit.png";
  fraction_canv.SaveAs(fraction_filename.c_str());
  fraction_canv.Close();
  return output;
}


events count_events(std::string chain, std::string file, std::string cuts) {
  events output;
  std::string full_chain = chain + "/DecayTree";
  TChain ch(full_chain.c_str());
  ch.Add(file.c_str());
  output.value = ch.GetEntries(cuts.c_str());
  output.rel_err = sqrt(output.value)/output.value;
  return output;
}


int main() {

  // make background template
  TH1F *Wp_background_template = background_fit("WpSingleTrackNoBias","+",0.2);
  TH1F *Wm_background_template = background_fit("WmSingleTrackNoBias","-",0.2);

  // get isolated data
  std::string isolation_cut = "TMath::Log10(TMath::Max(0.1,1.e-3*mu_PTSUMCONE040)) < 3", 
    pT_cut = "mu_PT*1.e-3 > 20",
    iso_cuts = isolation_cut + " && " + pT_cut;
  TH1F *Wp_hist_iso = make_histogram(data_file_path, "WpIso", "Wp_hist_iso", iso_cuts);
  TH1F *Wm_hist_iso = make_histogram(data_file_path, "WmIso", "Wm_hist_iso", iso_cuts);
  
  // get signal data (simulation)
  TH1F *Wp_hist_sim = make_histogram(W_sim_file_path, "WpIso", "Wp_hist_sim", iso_cuts);
  TH1F *Wm_hist_sim = make_histogram(W_sim_file_path, "WmIso", "Wm_hist_sim", iso_cuts);

  // get Z background
  TH1F *Wp_Z_background = make_histogram(Z_sim_file_path, "WpIso", "Wp_Z_background", iso_cuts);
  TH1F *Wm_Z_background = make_histogram(Z_sim_file_path, "WmIso", "Wm_Z_background", iso_cuts);
  // get Z fraction
  std::string Z_cuts = "Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5",
    W_cuts = "mu_PT > 20.e3 && mu_ETA > 2 && mu_ETA < 4.5";
  events Z_in_Z_data = count_events("Z",data_file_path,Z_cuts);
  events Z_in_Z_sim = count_events("Z",Z_sim_file_path,Z_cuts);

  events Wp_events = count_events("WpIso",data_file_path,W_cuts);
  events Wm_events = count_events("WmIso",data_file_path,W_cuts);

  double Wp_Z_frac = (Z_in_Z_data.value + Z_in_Z_sim.value)/Wp_events.value;
  double Wp_Z_frac_err = Wp_Z_frac * (Z_in_Z_data.rel_err + Z_in_Z_sim.rel_err + Wp_events.rel_err);
  double Wm_Z_frac = (Z_in_Z_data.value + Z_in_Z_sim.value)/Wm_events.value;
  double Wm_Z_frac_err = Wm_Z_frac * (Z_in_Z_data.rel_err + Z_in_Z_sim.rel_err + Wm_events.rel_err);
  
  // TFractionFitter
  fit_fractions Wp_fractions = fraction_fitter("+",Wp_Z_frac,Wp_Z_frac_err,Wp_hist_iso,Wp_hist_sim,Wp_background_template,Wp_Z_background);
  fit_fractions Wm_fractions = fraction_fitter("-",Wm_Z_frac,Wm_Z_frac_err,Wm_hist_iso,Wm_hist_sim,Wm_background_template,Wm_Z_background);
  //printf("Wp fractions = K: %lf + %lf, sim: %lf + %lf, Z: %lf + %lf\n",Wp_fractions.K_frac,Wp_fractions.K_err,Wp_fractions.sim_frac,Wp_fractions.sim_err,Wp_fractions.Z_frac,Wp_fractions.Z_err);
  //printf("Wm fractions = K: %lf + %lf, sim: %lf + %lf, Z: %lf + %lf\n",Wm_fractions.K_frac,Wm_fractions.K_err,Wm_fractions.sim_frac,Wm_fractions.sim_err,Wm_fractions.Z_frac,Wm_fractions.Z_err);

  // produce fit model and output data comparison
  produce_fit_model("+",Wp_fractions,Wp_hist_iso,Wp_hist_sim,Wp_background_template,Wp_Z_background, "Wp_fit_model");
  produce_fit_model("-",Wm_fractions,Wm_hist_iso,Wm_hist_sim,Wm_background_template,Wm_Z_background, "Wm_fit_model");
 
  //printf("Entries: Z in Z data = %lf, Z in Z sim = %lf, Wp total = %lf, Wm total = %lf\n", Z_in_Z_data, Z_in_Z_sim, Wp_events, Wm_events);
  //printf("Wm err - %lf, Wp err - %lf\n",Wp_Z_frac_err,Wm_Z_frac_err);
  printf("Wp Fraction = %lf + %lf\n",Wp_Z_frac,Wp_Z_frac_err);
  printf("Wm Fraction = %lf + %lf\n",Wm_Z_frac,Wm_Z_frac_err);
  return 0;
}

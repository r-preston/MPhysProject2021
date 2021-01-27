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

std::string const data_file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root";
std::string const sim_file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2015_24r1_Down_W_Sim09d.root";
std::string const plots_dir = "plots/";

int main() {

  // CREATE BACKGROUND FIT //
  TChain ch("WpSingleTrackNoBias/DecayTree");
  ch.Add(data_file_path.c_str());

  TH1F *hist_back = new TH1F("hist_back",";p_{T} (GeV);Events",100,15.,60.);
  std::string expression = "mu_PT*1.e-3>>hist_back";
  ch.Draw(expression.c_str());
  
  TF1 *function = new TF1("expo_fit","[0]*TMath::Exp(-[1]*x)",15.,60.);
  function->SetParameter(0,1.);
  function->SetParameter(1,2.5);
  hist_back->Fit(function->GetName());
  function->SetLineColor(2);
  
  // make histogram template from fit
  TH1F *background_template = new TH1F("Background Template from Exp Fit",";p_{T} (GeV);Events",100,20.,60.);
  for (int i=0; i<100000; i++) {background_template->Fill(function->GetRandom());}

  // output plot with fit
  TCanvas canv;
  hist_back->Draw();
  hist_back->GetXaxis()->CenterTitle(true);
  hist_back->GetYaxis()->CenterTitle(true);
  hist_back->GetXaxis()->SetTitleSize(0.04);
  hist_back->GetXaxis()->SetLabelSize(0.04);
  hist_back->GetYaxis()->SetTitleOffset(1);
  hist_back->GetYaxis()->SetTitleSize(0.04);
  hist_back->GetYaxis()->SetLabelSize(0.04);

  canv.Update();
  canv.Modified();
  
  TPaveStats *st = (TPaveStats*)hist_back->FindObject("stats");
  st->SetOptStat(0);
  st->SetOptFit(1111);
  st->SetX1NDC(0.55);
  st->SetX2NDC(0.9);
  st->SetY1NDC(0.6);
  st->SetY2NDC(0.78);
  st->Draw();
  
  TLegend *legend = new TLegend(0.4,0.78,0.9,0.9);
  legend->AddEntry(hist_back,"W^{+} Track Transverse Momentum","l");
  legend->AddEntry(function, "Exponential Fit", "l");
  legend->SetTextSize(0.04);
  legend->Draw();

  std::string const filename = plots_dir + "W_expo_back_plot.png";
  canv.SaveAs(filename.c_str());
  // finish output fit plot

  // END OF BACKGROUND FIT, BEGIN DATA COMPARISON

  // get isolated data
  TChain ch_iso("WpIso/DecayTree");
  ch_iso.Add(data_file_path.c_str());
  TH1F *hist_iso = new TH1F("hist_iso",";p_{T} (GeV);Events",100,20.,60.);
  expression = "mu_PT*1.e-3>>hist_iso";
  std::string isolation_cut = "TMath::Log10(TMath::Max(0.1,1.e-3*mu_PTSUMCONE040)) < 3", 
    pT_cut = "mu_PT*1.e-3 > 20",
    iso_cuts = isolation_cut + " && " + pT_cut;
  ch_iso.Draw(expression.c_str(), iso_cuts.c_str());

  //get signal data (simulation)
  TChain ch_sim("WpIso/DecayTree");
  ch_sim.Add(sim_file_path.c_str());
  TH1F *hist_sim = new TH1F("hist_sim",";p_{T} (GeV);Events",100,20.,60.);
  expression = "mu_PT*1.e-3>>hist_sim";
  ch_sim.Draw(expression.c_str(), iso_cuts.c_str());

  // produce fit model
  double signal_fraction = 0.5;
  hist_sim->Scale(signal_fraction*hist_iso->Integral()/hist_sim->Integral()); //data_integral/signal_integral
  background_template->Scale((1-signal_fraction)*hist_iso->Integral()/background_template->Integral()); //data_integral/background_integral

  TH1F *fit_model = new TH1F("fit_model",";p_{T} (GeV); Events",100,20.,60.);
  fit_model->Add(hist_sim, background_template);

  // Plot fit model
  TCanvas fit_canv;
  fit_model->Draw("HIST");
  fit_model->SetFillColor(5);
  background_template->Draw("SAME HIST");
  background_template->SetFillColor(4);
  hist_iso->Draw("SAME Ep");

  fit_model->SetStats(false);
  fit_model->GetXaxis()->CenterTitle(true);
  fit_model->GetXaxis()->SetTitleOffset(1.1);
  fit_model->GetYaxis()->CenterTitle(true);
  fit_model->GetYaxis()->SetTitleOffset(1.5);

  TLegend *fit_legend = new TLegend(0.5,0.72,0.9,0.9);
  fit_legend->AddEntry(fit_model, "Fit model", "f");
  fit_legend->AddEntry(background_template, "K/#pi #rightarrow #mu#nu", "f");
  fit_legend->AddEntry(hist_iso, "Isolated W^{+} Signal", "lep");
  fit_legend->Draw();

  std::string const fit_filename = plots_dir + "W_fit_model.png";
  fit_canv.SaveAs(fit_filename.c_str());


  // TFractionFitter
  /*
  TCanvas fraction_canv;
  TObjArray *mc = new TObjArray(1);
  mc->Add(background_template);
  TFractionFitter *fit = new TFractionFitter(hist_iso, mc);
  Int_t status = fit->Fit();
  std::cout << "fit status: " << status;
  if (status == 0) {
    TH1F *result = (TH1F*) fit->GetPlot();
    hist_iso->Draw("E");
    result->Draw("SAME");
  }
  std::string const fraction_filename = plots_dir + "W_fraction_fit.png";
  fit_canv.SaveAs(fraction_filename.c_str());
  */


  /* PLOT BACKGROUND_TEMPLATE
  TCanvas back_canv;
  background_template->Draw();
  background_template->SetStats(false);
  TLegend *back_legend = new TLegend(0.4,0.78,0.9,0.9);
  back_legend->AddEntry(background_template,"Background Template from Exponential Fit","l");
  back_legend->Draw();

  std::string const back_filename = plots_dir + "W_background_template.png";
  back_canv.SaveAs(back_filename.c_str());
  */

  return 0;
}

#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <THStack.h>
#include <string>
#include <TF1.h>
#include <TLegend.h>
#include <TPaveStats.h>

std::string const file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root";
std::string const plots_dir = "plots/";

int main() {

  TChain ch("WpSingleTrackNoBias/DecayTree");
  ch.Add(file_path.c_str());

  TH1F *hist = new TH1F("hist",";p_{T} (GeV);Events",100,15.,60.);
  std::string expression = "mu_PT*1.e-3>>hist";
  ch.Draw(expression.c_str());
  
  TF1 *fit = new TF1("expo_fit","expo",15,60);
  fit->SetLineColor(2);
  hist->Fit("expo_fit");
  
  TCanvas canv;
  hist->Draw();

  hist->GetXaxis()->CenterTitle(true);
  hist->GetYaxis()->CenterTitle(true);
  hist->GetXaxis()->SetTitleSize(0.04);
  hist->GetXaxis()->SetLabelSize(0.04);
  hist->GetYaxis()->SetTitleOffset(1);
  hist->GetYaxis()->SetTitleSize(0.04);
  hist->GetYaxis()->SetLabelSize(0.04);

  canv.Update();
  canv.Modified();
  
  TPaveStats *st = (TPaveStats*)hist->FindObject("stats");
  st->SetOptStat(0);
  st->SetOptFit(1111);
  st->SetX1NDC(0.55);
  st->SetX2NDC(0.9);
  st->SetY1NDC(0.6);
  st->SetY2NDC(0.78);
  st->Draw();
  
  TLegend *legend = new TLegend(0.4,0.78,0.9,0.9);
  legend->AddEntry(hist,"W^{+} Track Transverse Momentum","l");
  legend->AddEntry(fit, "Exponential Fit", "l");
  legend->SetTextSize(0.04);
  legend->Draw();

  std::string const filename = plots_dir + "W_expo_back_plot.png";
  canv.SaveAs(filename.c_str());
 
  return 0;
}

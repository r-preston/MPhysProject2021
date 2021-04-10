#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
from array import array
import math
import os

# Used for final report: create zoomed in plot of both W xsecs compared to theory and 7 and 8 TeV measurements

def Wp_theory():
    gre = ROOT.TGraphErrors(19);
    gre.SetName("Graph0");
    gre.SetTitle("Graph");
    gre.SetFillColor(1);
   
    ci = ROOT.TColor.GetColor("#ff0000");
    gre.SetLineColor(ci);
    gre.SetLineWidth(2);
    gre.SetMarkerStyle(20);
    gre.SetPoint(0,2,55.81644);
    gre.SetPointError(0,0,0.106449);
    gre.SetPoint(1,3,169.2912);
    gre.SetPointError(1,0,0.3504109);
    gre.SetPoint(2,4,355.9231);
    gre.SetPointError(2,0,0.772978);
    gre.SetPoint(3,5,510.098);
    gre.SetPointError(3,0,1.344652);
    gre.SetPoint(4,6,705.0895);
    gre.SetPointError(4,0,1.805724);
    gre.SetPoint(5,7,908.8186);
    gre.SetPointError(5,0,2.903108);
    gre.SetPoint(6,8,1126.259);
    gre.SetPointError(6,0,3.258412);
    gre.SetPoint(7,9,1338.557);
    gre.SetPointError(7,0,3.93392);
    gre.SetPoint(8,10,1544.101);
    gre.SetPointError(8,0,4.41897);
    gre.SetPoint(9,11,1754.364);
    gre.SetPointError(9,0,6.022293);
    gre.SetPoint(10,12,1959.431);
    gre.SetPointError(10,0,6.161057);
    gre.SetPoint(11,13,2177.632);
    gre.SetPointError(11,0,7.538669);
    gre.SetPoint(12,14,2393.976);
    gre.SetPointError(12,0,7.999908);
    gre.SetPoint(13,15,2557.823);
    gre.SetPointError(13,0,10.31271);
    gre.SetPoint(14,16,2754.785);
    gre.SetPointError(14,0,10.67382);
    gre.SetPoint(15,17,2942.312);
    gre.SetPointError(15,0,12.98126);
    gre.SetPoint(16,18,3158.145);
    gre.SetPointError(16,0,11.71054);
    gre.SetPoint(17,19,3306.39);
    gre.SetPointError(17,0,15.44113);
    gre.SetPoint(18,20,3484.935);
    gre.SetPointError(18,0,15.69135);
      
    Graph_Graph17 = ROOT.TH1F("Graph_Graph17","Graph",100,0.2,21.8);
    Graph_Graph17.SetMinimum(50.13899);
    Graph_Graph17.SetMaximum(3845.118);
    Graph_Graph17.SetDirectory(0);
    Graph_Graph17.SetStats(0);
    Graph_Graph17.SetLineWidth(2);
    Graph_Graph17.SetMarkerStyle(20);
    Graph_Graph17.GetXaxis().SetNdivisions(505);
    Graph_Graph17.GetXaxis().SetLabelFont(132);
    Graph_Graph17.GetXaxis().SetLabelOffset(0.01);
    Graph_Graph17.GetXaxis().SetLabelSize(0.06);
    Graph_Graph17.GetXaxis().SetTitleSize(0.06);
    Graph_Graph17.GetXaxis().SetTitleOffset(1.1);
    Graph_Graph17.GetXaxis().SetTitleFont(132);
    Graph_Graph17.GetYaxis().SetNdivisions(506);
    Graph_Graph17.GetYaxis().SetLabelFont(132);
    Graph_Graph17.GetYaxis().SetLabelOffset(0.01);
    Graph_Graph17.GetYaxis().SetLabelSize(0.06);
    Graph_Graph17.GetYaxis().SetTitleSize(0.06);
    Graph_Graph17.GetYaxis().SetTitleFont(132);
    Graph_Graph17.GetZaxis().SetLabelFont(132);
    Graph_Graph17.GetZaxis().SetLabelSize(0.06);
    Graph_Graph17.GetZaxis().SetTitleSize(0.06);
    Graph_Graph17.GetZaxis().SetTitleFont(132);
    gre.SetHistogram(Graph_Graph17);
    return gre;


def Wm_theory():
    gre = ROOT.TGraphErrors(19);
    gre.SetName("Graph1");
    gre.SetTitle("Graph");
    gre.SetFillColor(1);

    ci = ROOT.TColor.GetColor("#ff0000");
    gre.SetLineColor(ci);
    gre.SetLineWidth(2);
    gre.SetMarkerStyle(20);
    gre.SetPoint(0,2,45.8);
    gre.SetPointError(0,0,0.2);
    gre.SetPoint(1,3,151.5867);
    gre.SetPointError(1,0,0.3278794);
    gre.SetPoint(2,4,301.3271);
    gre.SetPointError(2,0,0.5989437);
    gre.SetPoint(3,5,430.9132);
    gre.SetPointError(3,0,1.017377);
    gre.SetPoint(4,6,565.626);
    gre.SetPointError(4,0,1.210156);
    gre.SetPoint(5,7,701.1258);
    gre.SetPointError(5,0,2.049885);
    gre.SetPoint(6,8,843.4793);
    gre.SetPointError(6,0,2.540942);
    gre.SetPoint(7,9,978.5042);
    gre.SetPointError(7,0,3.793097);
    gre.SetPoint(8,10,1120.532);
    gre.SetPointError(8,0,3.18583);
    gre.SetPoint(9,11,1253.042);
    gre.SetPointError(9,0,3.838623);
    gre.SetPoint(10,12,1381.146);
    gre.SetPointError(10,0,4.668509);
    gre.SetPoint(11,13,1521.508);
    gre.SetPointError(11,0,4.876128);
    gre.SetPoint(12,14,1648.683);
    gre.SetPointError(12,0,5.180606);
    gre.SetPoint(13,15,1789.207);
    gre.SetPointError(13,0,6.676192);
    gre.SetPoint(14,16,1909.586);
    gre.SetPointError(14,0,7.7596);
    gre.SetPoint(15,17,2043.151);
    gre.SetPointError(15,0,7.511781);
    gre.SetPoint(16,18,2159.585);
    gre.SetPointError(16,0,7.80703);
    gre.SetPoint(17,19,2294.989);
    gre.SetPointError(17,0,8.552556);
    gre.SetPoint(18,20,2432.562);
    gre.SetPointError(18,0,8.775901);
    
    Graph_Graph18 = ROOT.TH1F("Graph_Graph18","Graph",100,0.2,21.8);
    Graph_Graph18.SetMinimum(41.04);
    Graph_Graph18.SetMaximum(2680.912);
    Graph_Graph18.SetDirectory(0);
    Graph_Graph18.SetStats(0);
    Graph_Graph18.SetLineWidth(2);
    Graph_Graph18.SetMarkerStyle(20);
    Graph_Graph18.GetXaxis().SetNdivisions(505);
    Graph_Graph18.GetXaxis().SetLabelFont(132);
    Graph_Graph18.GetXaxis().SetLabelOffset(0.01);
    Graph_Graph18.GetXaxis().SetLabelSize(0.06);
    Graph_Graph18.GetXaxis().SetTitleSize(0.06);
    Graph_Graph18.GetXaxis().SetTitleOffset(1.1);
    Graph_Graph18.GetXaxis().SetTitleFont(132);
    Graph_Graph18.GetYaxis().SetNdivisions(506);
    Graph_Graph18.GetYaxis().SetLabelFont(132);
    Graph_Graph18.GetYaxis().SetLabelOffset(0.01);
    Graph_Graph18.GetYaxis().SetLabelSize(0.06);
    Graph_Graph18.GetYaxis().SetTitleSize(0.06);
    Graph_Graph18.GetYaxis().SetTitleFont(132);
    Graph_Graph18.GetZaxis().SetLabelFont(132);
    Graph_Graph18.GetZaxis().SetLabelSize(0.06);
    Graph_Graph18.GetZaxis().SetTitleSize(0.06);
    Graph_Graph18.GetZaxis().SetTitleFont(132);
    gre.SetHistogram(Graph_Graph18);
    return gre;



    

## MAIN
# W bosons
n_W = 2
x_W = array('d',[7,8])
ex_W = array('d',[0,0])

# Wp boson
with open('results_json/Wp_xsec.json') as json_file:
    Wp_input = json.load(json_file)
Wp_5 = Wp_input["xsec"]
Wp_5_err = Wp_input["xsec_err"]
Wp_5_stat = Wp_input["xsec_err_stat"]

y_Wp = array('d',[878.0, 1093.6])
ey_Wp = array('d',[math.sqrt(2.1**2+6.7**2+9.3**2+15.0**2), math.sqrt(2.1**2+7.2**2+10.9**2+12.7**2)])
# 7 = 2014, 8 = 2016

Wp_theory_trend = Wp_theory()

# Wm boson
with open('results_json/Wm_xsec.json') as json_file:
    Wm_input = json.load(json_file)
Wm_5 = Wm_input["xsec"]
Wm_5_err = Wm_input["xsec_err"]
Wm_5_stat = Wm_input["xsec_err_stat"]

y_Wm = array('d',[689.5, 818.4])
ey_Wm = array('d',[math.sqrt(2.0**2+5.3**2+6.3**2+11.8**2), math.sqrt(1.9**2+5**2+7**2+9.5**2)])
# 7 = 2014, 8 = 2016

Wm_theory_trend = Wm_theory()

canv = ROOT.TCanvas()
Wp_xsec_5TeV = ROOT.TGraphErrors(1)
Wp_xsec_5TeV.SetPoint(0,5,Wp_5);
Wp_xsec_5TeV.SetPointError(0,0,Wp_5_err);
Wp_xsec_5TeV.SetMarkerSize(0.75)
Wp_xsec_5TeV.SetMarkerColor(8)
Wp_xsec_5TeV.SetLineColor(1)
Wp_xsec_5TeV.GetXaxis().SetLimits(4.45,8.55)
Wp_xsec_5TeV.GetYaxis().SetRangeUser(350,1420)
Wp_xsec_5TeV.SetMarkerStyle(20)

Wp_xsec_5TeV_stat = ROOT.TGraphErrors(1)
Wp_xsec_5TeV_stat.SetPoint(0,5,Wp_5);
Wp_xsec_5TeV_stat.SetPointError(0,0,Wp_5_stat);
Wp_xsec_5TeV_stat.SetMarkerSize(0.75)
Wp_xsec_5TeV_stat.SetMarkerColor(8)
Wp_xsec_5TeV_stat.SetLineColor(1)
Wp_xsec_5TeV_stat.GetXaxis().SetLimits(4.45,8.55)
Wp_xsec_5TeV_stat.GetYaxis().SetRangeUser(350,1420)
Wp_xsec_5TeV_stat.SetMarkerStyle(20)

Wp_xsec_plot = ROOT.TGraphErrors(n_W,x_W,y_Wp,ex_W,ey_Wp)
Wp_xsec_plot.GetXaxis().SetLimits(4.45,8.55)
Wp_xsec_plot.SetMarkerSize(0.75)
Wp_xsec_plot.GetYaxis().SetRangeUser(350,1420)
Wp_xsec_plot.SetMarkerStyle(20)
Wp_xsec_plot.SetTitle("")

Wp_theory_trend.GetXaxis().SetLimits(4.45,8.55)
Wp_theory_trend.SetMinimum(350)
Wp_theory_trend.SetMaximum(1420)

#Wm
Wm_xsec_5TeV = ROOT.TGraphErrors(1)
Wm_xsec_5TeV.SetPoint(0,5,Wm_5);
Wm_xsec_5TeV.SetPointError(0,0,Wm_5_err);
Wm_xsec_5TeV.SetMarkerSize(0.75)
Wm_xsec_5TeV.SetMarkerColor(8)
Wm_xsec_5TeV.SetLineColor(1)
Wm_xsec_5TeV.GetXaxis().SetLimits(4.45,8.55)
Wm_xsec_5TeV.GetYaxis().SetRangeUser(350,1420)
Wm_xsec_5TeV.SetMarkerStyle(24)

Wm_xsec_5TeV_stat = ROOT.TGraphErrors(1)
Wm_xsec_5TeV_stat.SetPoint(0,5,Wm_5);
Wm_xsec_5TeV_stat.SetPointError(0,0,Wm_5_stat);
Wm_xsec_5TeV_stat.SetMarkerSize(0.75)
Wm_xsec_5TeV_stat.SetMarkerColor(8)
Wm_xsec_5TeV_stat.SetLineColor(1)
Wm_xsec_5TeV_stat.GetXaxis().SetLimits(4.45,8.55)
Wm_xsec_5TeV_stat.GetYaxis().SetRangeUser(350,1420)
Wm_xsec_5TeV_stat.SetMarkerStyle(24)

Wm_xsec_plot = ROOT.TGraphErrors(n_W,x_W,y_Wm,ex_W,ey_Wm)
Wm_xsec_plot.GetXaxis().SetLimits(4.45,8.55)
Wm_xsec_plot.SetMarkerSize(0.75)
Wm_xsec_plot.GetYaxis().SetRangeUser(350,1420)
Wm_xsec_plot.SetMarkerStyle(24)
Wm_xsec_plot.SetTitle("")

Wm_theory_trend.GetXaxis().SetLimits(4.45,8.55)
Wm_theory_trend.SetMinimum(350)
Wm_theory_trend.SetMaximum(1420)



multiplot = ROOT.TMultiGraph()
multiplot.GetXaxis().SetLimits(4.45,8.55)
multiplot.SetMinimum(350)
multiplot.SetMaximum(1420)

multiplot.SetTitle("")
multiplot.GetXaxis().SetTitle("#sqrt{s} (TeV)")
multiplot.GetXaxis().CenterTitle(1)
multiplot.GetXaxis().SetTitleSize(0.04)
multiplot.GetXaxis().SetLabelSize(0.04)
multiplot.GetYaxis().SetTitle("#sigma_{W} (pb)")
multiplot.GetYaxis().CenterTitle(1)
multiplot.GetYaxis().SetTitleSize(0.04)
multiplot.GetYaxis().SetLabelSize(0.04)
multiplot.GetYaxis().SetTitleOffset(1.2)

multiplot.Add(Wp_theory_trend,"c")
multiplot.Add(Wp_xsec_5TeV,"AP")
multiplot.Add(Wp_xsec_5TeV_stat,"AP")
multiplot.Add(Wp_xsec_plot,"AP")
multiplot.Add(Wm_theory_trend,"c")
multiplot.Add(Wm_xsec_5TeV,"AP")
multiplot.Add(Wm_xsec_5TeV_stat,"AP")
multiplot.Add(Wm_xsec_plot,"AP")
multiplot.Draw("AP")

legend = ROOT.TLegend(0.1,0.68,0.6,0.9)
legend.AddEntry(Wp_xsec_plot, "W^{+} #rightarrow #mu^{+} #nu_{#mu}", "ep")
legend.AddEntry(Wm_xsec_plot, "W^{-} #rightarrow #mu^{-} #bar#nu_{#mu}", "ep")
legend.AddEntry(Wp_xsec_5TeV, "New 5 TeV Measurements", "ep") 
legend.AddEntry(Wp_theory_trend, "DYNNLO+MSTW08 Predictions", "l")
legend.SetTextSize(0.04)
legend.Draw()

filename = "plots/W_both_xsec_plot.pdf"
canv.SaveAs(filename)
canv.Close()


#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
from array import array
import math

def make_xsec_plot(boson, label, n, x, ex, y, ey, theory):
    canv = ROOT.TCanvas()

    xsec_plot = ROOT.TGraphErrors(n,x,y,ex,ey)
    xsec_plot.GetXaxis().SetLimits(4.1,13.9)
    xsec_plot.SetMarkerSize(0.75)
    if boson == "Z":
        xsec_plot.GetYaxis().SetRangeUser(25,225)
        xsec_plot.SetMarkerStyle(25)
    elif boson == "Wp":
        xsec_plot.GetYaxis().SetRangeUser(410,2450)
        xsec_plot.SetMarkerStyle(20)
    elif boson == "Wm":
        xsec_plot.GetYaxis().SetRangeUser(350,1690)
        xsec_plot.SetMarkerStyle(24)

    xsec_plot.SetTitle("")
    y_axis = "#sigma_{" + label + "} (pb)"
    xsec_plot.GetXaxis().SetTitle("#sqrt{s} (TeV)")
    xsec_plot.GetXaxis().CenterTitle(1)
    xsec_plot.GetXaxis().SetTitleSize(0.04)
    xsec_plot.GetXaxis().SetLabelSize(0.04)
    xsec_plot.GetYaxis().SetTitle(y_axis)
    xsec_plot.GetYaxis().CenterTitle(1)
    xsec_plot.GetYaxis().SetTitleSize(0.04)
    xsec_plot.GetYaxis().SetLabelSize(0.04)
    xsec_plot.GetYaxis().SetTitleOffset(1.15)
    xsec_plot.Draw("AP")
    theory.Draw("same c")

    legend = ROOT.TLegend(0.1,0.78,0.4,0.9)
    experimental_label = "LHCb #sigma_{" + label + "}"
    legend.AddEntry(xsec_plot, experimental_label, "ep")
    legend.AddEntry(theory, "DYNNLO+MSTW08", "l")
    legend.SetTextSize(0.04)
    legend.Draw()

    filename = "plots/"+boson+"_xsec_plot.png"
    canv.SaveAs(filename)
    canv.Close()
    return xsec_plot



#def all_xsec_plot(nz, xz, exz, yz, eyz, nw, xw, exw, ywp, eywp, ywm, eywm, Z_theory, Wp_theory, Wm_theory):
def all_xsec_plot(Z_plot, Z_theory, Wp_plot, Wp_theory, Wm_plot, Wm_theory):
    canv = ROOT.TCanvas()
    canv.SetLogy()

    #Z_plot.SetMarkerStyle(20)
    #Z_plot.SetMarkerSize(0.75)
    #Wp_plot.SetMarkerStyle(22)
    #Wp_plot.SetMarkerSize(0.75)
    #Wm_plot.SetMarkerStyle(23)
    #Wm_plot.SetMarkerSize(0.75)

    multiplot = ROOT.TMultiGraph()
    multiplot.GetXaxis().SetLimits(2.0,15.0)
    multiplot.SetMinimum(30.)
    multiplot.SetMaximum(2500.)

    multiplot.SetTitle("")
    multiplot.GetXaxis().SetTitle("#sqrt{s} (TeV)")
    multiplot.GetXaxis().CenterTitle(1)
    multiplot.GetXaxis().SetTitleSize(0.04)
    multiplot.GetXaxis().SetLabelSize(0.04)
    multiplot.GetYaxis().SetTitle("#sigma (Pb)")
    multiplot.GetYaxis().CenterTitle(1)
    multiplot.GetYaxis().SetTitleSize(0.04)
    multiplot.GetYaxis().SetLabelSize(0.04)
    multiplot.GetYaxis().SetTitleOffset(1)
   
    multiplot.Add(Z_theory,"c")
    multiplot.Add(Wp_theory,"c")
    multiplot.Add(Wm_theory,"c")
    multiplot.Add(Z_plot,"P")
    multiplot.Add(Wp_plot,"P")
    multiplot.Add(Wm_plot,"P")
    multiplot.Draw("AP")

    legend = ROOT.TLegend(0.6,0.1,0.9,0.3)
    legend.AddEntry(Z_theory, "DYNNLO+MSTW08", "l")
    legend.AddEntry(Wp_plot, "W^{+} #rightarrow #mu^{+} #nu_{#mu}", "ep")
    legend.AddEntry(Wm_plot, "W^{-} #rightarrow #mu^{-} #bar#nu_{#mu}", "ep")
    legend.AddEntry(Z_plot, "Z #rightarrow #mu^{+} #mu^{-}", "ep")
    legend.SetTextSize(0.04)
    legend.Draw()

    canv.Modified()
    canv.SaveAs("plots/all_xsecs_plot.png")
    canv.Close()


def make_ratio_plot(ratio, label, n, x, ex, y, ey, theory):
    canv = ROOT.TCanvas()
    ratio_plot = ROOT.TGraphErrors(n,x,y,ex,ey)
    ratio_plot.GetXaxis().SetLimits(4.5,8.5)
    ratio_plot.SetMarkerStyle(8)
    ratio_plot.SetTitle("")
    ratio_plot.GetXaxis().SetTitle("#sqrt{s} (TeV)")
    ratio_plot.GetXaxis().CenterTitle(1)
    ratio_plot.GetYaxis().SetTitle(label)
    ratio_plot.GetYaxis().CenterTitle(1)
    ratio_plot.Draw("AP")
    theory.Draw("c")

    legend = ROOT.TLegend(0.6,0.78,0.9,0.9)
    legend.AddEntry(ratio_plot, "LHCb #sigma_{" + label + "}", "ep")
    legend.AddEntry(theory, "DYNNLO+MSTW08", "l")
    legend.SetTextSize(0.04)
    legend.Draw()

    filename = "plots/"+ratio+"_ratio_plot.png"
    canv.SaveAs(filename)
    canv.Close()


def Z_theory():
    gre = ROOT.TGraphErrors(19);
    gre.SetName("Graph2");
    gre.SetTitle("Graph");
    gre.SetFillColor(1);

    ci = ROOT.TColor.GetColor("#ff0000");
    gre.SetLineColor(ci);
    gre.SetLineWidth(2);
    gre.SetMarkerStyle(20);
    gre.SetPoint(0,2,1.610353);
    gre.SetPointError(0,0,0.003089874);
    gre.SetPoint(1,3,8.471595);
    gre.SetPointError(1,0,0.01932682);
    gre.SetPoint(2,4,20.51431);
    gre.SetPointError(2,0,0.04558532);
    gre.SetPoint(3,5,36.20083);
    gre.SetPointError(3,0,0.09373648);
    gre.SetPoint(4,6,54.30165);
    gre.SetPointError(4,0,0.1376057);
    gre.SetPoint(5,7,73.36457);
    gre.SetPointError(5,0,0.2258884);
    gre.SetPoint(6,8,94.2233);
    gre.SetPointError(6,0,0.2701851);
    gre.SetPoint(7,9,114.5502);
    gre.SetPointError(7,0,0.3495494);
    gre.SetPoint(8,10,134.3898);
    gre.SetPointError(8,0,0.4008405);
    gre.SetPoint(9,11,154.531);
    gre.SetPointError(9,0,0.5230851);
    gre.SetPoint(10,12,174.5487);
    gre.SetPointError(10,0,0.5222072);
    gre.SetPoint(11,13,194.4331);
    gre.SetPointError(11,0,0.6131347);
    gre.SetPoint(12,14,213.2666);
    gre.SetPointError(12,0,0.7358615);
    gre.SetPoint(13,15,231.7848);
    gre.SetPointError(13,0,0.8716615);
    gre.SetPoint(14,16,249.1646);
    gre.SetPointError(14,0,0.8382152);
    gre.SetPoint(15,17,267.9907);
    gre.SetPointError(15,0,0.9506001);
    gre.SetPoint(16,18,282.812);
    gre.SetPointError(16,0,1.321404);
    gre.SetPoint(17,19,303.6655);
    gre.SetPointError(17,0,1.077402);
    gre.SetPoint(18,20,316.5302);
    gre.SetPointError(18,0,1.336074);
    
    Graph_Graph19 = ROOT.TH1F("Graph_Graph19","Graph",100,0.2,21.8);
    Graph_Graph19.SetMinimum(1.446537);
    Graph_Graph19.SetMaximum(349.4922);
    Graph_Graph19.SetDirectory(0);
    Graph_Graph19.SetStats(0);
    Graph_Graph19.SetLineWidth(2);
    Graph_Graph19.SetMarkerStyle(20);
    Graph_Graph19.GetXaxis().SetNdivisions(505);
    Graph_Graph19.GetXaxis().SetLabelFont(132);
    Graph_Graph19.GetXaxis().SetLabelOffset(0.01);
    Graph_Graph19.GetXaxis().SetLabelSize(0.06);
    Graph_Graph19.GetXaxis().SetTitleSize(0.06);
    Graph_Graph19.GetXaxis().SetTitleOffset(1.1);
    Graph_Graph19.GetXaxis().SetTitleFont(132);
    Graph_Graph19.GetYaxis().SetNdivisions(506);
    Graph_Graph19.GetYaxis().SetLabelFont(132);
    Graph_Graph19.GetYaxis().SetLabelOffset(0.01);
    Graph_Graph19.GetYaxis().SetLabelSize(0.06);
    Graph_Graph19.GetYaxis().SetTitleSize(0.06);
    Graph_Graph19.GetYaxis().SetTitleFont(132);
    Graph_Graph19.GetZaxis().SetLabelFont(132);
    Graph_Graph19.GetZaxis().SetLabelSize(0.06);
    Graph_Graph19.GetZaxis().SetTitleSize(0.06);
    Graph_Graph19.GetZaxis().SetTitleFont(132);
    gre.SetHistogram(Graph_Graph19);
    return gre;


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


def WW_ratio_theory():
    gre = ROOT.TGraphErrors(19);
    gre.SetName("Graph0");
    gre.SetTitle("Graph");
    gre.SetFillColor(2);
    gre.SetFillStyle(3005);
   
    ci = ROOT.TColor.GetColor("#ff0000");
    gre.SetLineColor(ci);
    gre.SetLineWidth(2);
    gre.SetMarkerStyle(20);
    r = 55.81644/45.9;
    r_err = r*math.sqrt((0.106449/55.81644)**2+(0.2/45.9)**2);
    gre.SetPoint(0,2,r);
    gre.SetPointError(0,0,r_err);
    r = 169.2912/151.5867;
    r_err = r*math.sqrt((0.3504109/169.2912)**2+(0.3278794/151.5867)**2);
    gre.SetPoint(1,3,r);
    gre.SetPointError(1,0,r_err);
    r = 355.9231/301.3271;
    r_err = r*math.sqrt((0.772978/355.9231)**2+(0.5989437/301.3271)**2);
    gre.SetPoint(2,4,r);
    gre.SetPointError(2,0,r_err);
    r = 510.098/430.9132;
    r_err = r*math.sqrt((1.344652/510.098)**2+(1.017377/430.9132)**2);
    gre.SetPoint(3,5,r);
    gre.SetPointError(3,0,r_err);
    r = 705.0895/565.626;
    r_err = r*math.sqrt((1.805724/705.0895)**2+(1.210156/565.626)**2);
    gre.SetPoint(4,6,r);
    gre.SetPointError(4,0,r_err);
    r = 908.8186/701.1258;
    r_err = r*math.sqrt((2.903108/908.8186)**2+(2.049885/701.1258)**2);
    gre.SetPoint(5,7,r);
    gre.SetPointError(5,0,r_err);
    r = 1126.259/843.4793;
    r_err = r*math.sqrt((3.258412/1126.259)**2+(2.540942/843.4793)**2);
    gre.SetPoint(6,8,r);
    gre.SetPointError(6,0,r_err);
    r = 1338.557/978.5042;
    r_err = r*math.sqrt((3.93392/1338.557)**2+(3.793097/978.5042)**2);
    gre.SetPoint(7,9,r);
    gre.SetPointError(7,0,r_err);
    r = 1544.101/1120.532;
    r_err = r*math.sqrt((4.41897/1544.101)**2+(3.18583/1120.532)**2);
    gre.SetPoint(8,10,r);
    gre.SetPointError(8,0,r_err);
    r = 1754.364/1253.042;
    r_err = r*math.sqrt((6.022293/1754.364)**2+(3.838623/1253.042)**2);
    gre.SetPoint(9,11,r);
    gre.SetPointError(9,0,r_err);
    r = 1959.431/1381.146;
    r_err = r*math.sqrt((6.161057/1959.431)**2+(4.668509/1381.146)**2);
    gre.SetPoint(10,12,r);
    gre.SetPointError(10,0,r_err);
    r = 2177.632/1521.508;
    r_err = r*math.sqrt((7.538669/2177.632)**2+(4.876128/1521.508)**2);
    gre.SetPoint(11,13,r);
    gre.SetPointError(11,0,r_err);
    r = 2393.976/1648.683;
    r_err = r*math.sqrt((7.999908/2393.976)**2+(5.180606/1648.683)**2);
    gre.SetPoint(12,14,r);
    gre.SetPointError(12,0,r_err);
    r = 2557.823/1789.207;
    r_err = r*math.sqrt((10.31271/2557.823)**2+(6.676192/1789.207)**2);
    gre.SetPoint(13,15,r);
    gre.SetPointError(13,0,r_err);
    r = 2754.785/1909.586;
    r_err = r*math.sqrt((10.67382/2754.785)**2+(7.7596/1909.586)**2);
    gre.SetPoint(14,16,r);
    gre.SetPointError(14,0,r_err);
    r = 2942.312/2043.151;
    r_err = r*math.sqrt((12.98126/2942.312)**2+(7.511781/2043.151)**2);
    gre.SetPoint(15,17,r);
    gre.SetPointError(15,0,r_err);
    r = 3158.145/2159.585;
    r_err = r*math.sqrt((11.71054/3158.145)**2+(7.80703/2159.585)**2);
    gre.SetPoint(16,18,r);
    gre.SetPointError(16,0,r_err);
    r = 3306.39/2294.989;
    r_err = r*math.sqrt((15.44113/3306.39)**2+(8.552556/2294.989)**2);
    gre.SetPoint(17,19,r);
    gre.SetPointError(17,0,r_err);
    r = 3484.935/2432.562;
    r_err = r*math.sqrt((15.69135/3484.935)**2+(8.775901/2432.562)**2);
    gre.SetPoint(18,20,r);
    gre.SetPointError(18,0,r_err);
      
    Graph_Graph17 = ROOT.TH1F("Graph_Graph17","Graph",100,0.2,21.8);
    Graph_Graph17.GetXaxis().SetLimits(4.5,8.5)
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



    

## MAIN
# Z boson
with open('results_json/Z_xsec.json') as json_file:
    Z_input = json.load(json_file)

n_Z = 4
x_Z = array('d',[5.0,7.0,8.0,13.0])
ex_Z = array('d',[0,0,0,0])

Z_5 = Z_input["xsec"]
Z_5_err = Z_input["xsec_err"]

y_Z = array('d',[Z_5, 76.0, 95.0, 198.0])
ey_Z = array('d',[Z_5_err, math.sqrt(0.3**2+0.5**2+1**2+1.3**2), math.sqrt(0.3**2+0.7**2+1.1**2+1.1**2), math.sqrt(0.9**2+4.7**2+7.7**2)])
# 7 = 2015, 8 = 2016, 13 = 2016

Z_theory_trend = Z_theory() 
Z_plot = make_xsec_plot("Z", "Z", n_Z, x_Z, ex_Z, y_Z, ey_Z, Z_theory_trend)

# W bosons
n_W = 3
x_W = array('d',[5,7,8])
ex_W = array('d',[0,0,0])

# Wp boson
with open('results_json/Wp_xsec.json') as json_file:
    Wp_input = json.load(json_file)
Wp_5 = Wp_input["xsec"]
Wp_5_err = Wp_input["xsec_err"]

y_Wp = array('d',[Wp_5, 878.0, 1093.6])
ey_Wp = array('d',[Wp_5_err, math.sqrt(2.1**2+6.7**2+9.3**2+15.0**2), math.sqrt(2.1**2+7.2**2+10.9**2+12.7**2)])
# 7 = 2014, 8 = 2016

Wp_theory_trend = Wp_theory()
Wp_plot = make_xsec_plot("Wp", "W^{+}", n_W, x_W, ex_W, y_Wp, ey_Wp, Wp_theory_trend)

# Wm boson
with open('results_json/Wm_xsec.json') as json_file:
    Wm_input = json.load(json_file)
Wm_5 = Wm_input["xsec"]
Wm_5_err = Wm_input["xsec_err"]

y_Wm = array('d',[Wm_5, 689.5, 818.4])
ey_Wm = array('d',[Wm_5_err, math.sqrt(2.0**2+5.3**2+6.3**2+11.8**2), math.sqrt(1.9**2+5**2+7**2+9.5**2)])
# 7 = 2014, 8 = 2016

Wm_theory_trend = Wm_theory()
Wm_plot = make_xsec_plot("Wm", "W^{-}", n_W, x_W, ex_W, y_Wm, ey_Wm, Wm_theory_trend)

# plot all xsec
all_xsec_plot(Z_plot, Z_theory_trend, Wp_plot, Wp_theory_trend, Wm_plot, Wm_theory_trend)
#all_xsec_plot(n_Z, x_Z, ex_Z, y_Z, ey_Z, n_W, x_W, ex_W, y_Wp, ey_Wp, y_Wm, ey_Wm, Z_theory_trend, Wp_theory_trend, Wm_theory_trend)


# Ratios
with open('results_json/Ratios.json') as json_file:
    ratios_input = json.load(json_file)
WW_ratio_5 = ratios_input["WW_ratio"]
WW_ratio_5_err = ratios_input["WW_error"]
WZ_ratio_5 = ratios_input["WZ_ratio"]
WZ_ratio_5_err = ratios_input["WZ_error"]

y_WW_ratio = array('d',[WW_ratio_5, 1.274, 1.336])
ey_WW_ratio = array('d',[WW_ratio_5_err, math.sqrt(0.005**2+0.009**2+0.002**2), math.sqrt(0.004**2+0.005**2+0.002**2)])
# 7 = 2014, 8 = 2016
WW_ratio_theory_plot = WW_ratio_theory()
make_ratio_plot("WW", "W^{+}/W^{-}", n_W, x_W, ex_W, y_WW_ratio, ey_WW_ratio, WW_ratio_theory_plot)

y_WZ_ratio = array('d', [WZ_ratio_5, 20.63, 20.13])
ey_WZ_ratio = array('d', [WZ_ratio_5_err, math.sqrt(0.09**2+0.12**2+0.05**2), math.sqrt(0.06**2+0.11**2+0.04**2)])
# 7 = 2014, 8 = 2016

#make_ratio_plot("WZ", "W/Z", n_W, x_W, ex_W, y_WZ_ratio, ey_WZ_ratio)

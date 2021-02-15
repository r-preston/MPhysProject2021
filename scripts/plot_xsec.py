#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
from array import array

def make_plot(boson, label, n, x, ex, y, ey):
    canv = ROOT.TCanvas()
    xsec_plot = ROOT.TGraphErrors(n,x,y,ex,ey)
    xsec_plot.SetMarkerStyle(8)
    xsec_plot.SetTitle("")
    y_axis = "#sigma_{" + label + "} (pb)"
    xsec_plot.GetXaxis().SetTitle("Energy (TeV)")
    xsec_plot.GetXaxis().CenterTitle(1)
    xsec_plot.GetYaxis().SetTitle(y_axis)
    xsec_plot.GetYaxis().CenterTitle(1)
    xsec_plot.Draw("AP")
    filename = "plots/"+boson+"_xsec_plot.png"
    canv.SaveAs(filename)
    canv.Close()
    


# Z boson
with open('xsec.json') as json_file:
    Z_input = json.load(json_file)

n_Z = 4
x_Z = array('d',[5.0,7.0,8.0,13.0])
ex_Z = array('d',[0,0,0,0])

Z_5 = Z_input["xsec"]
Z_5_err = Z_input["xsec_err"]

y_Z = array('d',[Z_5, 76.0, 95.0, 198.0])
ey_Z = array('d',[Z_5_err, 0.3+0.5+1+1.3, 0.3+0.7+1.1+1.1, 0.9+4.7+7.7])
# 7 = 2015, 8 = 2016, 13 = 2016

make_plot("Z", "Z", n_Z, x_Z, ex_Z, y_Z, ey_Z)

# W bosons
n_W = 3
x_W = array('d',[5,7,8])
ex_W = array('d',[0,0,0])

# Wp boson
with open('Wp_xsec.json') as json_file:
    Wp_input = json.load(json_file)
Wp_5 = Wp_input["xsec"]
Wp_5_err = Wp_input["xsec_err"]

y_Wp = array('d',[Wp_5, 861.0, 1093.6])
ey_Wp = array('d',[Wp_5_err, 2+11.2+14.7, 2.1+7.2+10.9+12.7])
# 7 = 2014, 8 = 2016

make_plot("Wp", "W^+", n_W, x_W, ex_W, y_Wp, ey_Wp)

# Wm boson
with open('Wm_xsec.json') as json_file:
    Wm_input = json.load(json_file)
Wm_5 = Wm_input["xsec"]
Wm_5_err = Wm_input["xsec_err"]

y_Wm = array('d',[Wm_5, 675.8, 818.4])
ey_Wm = array('d',[Wm_5_err, 1.9+8.8+11.6, 1.9+5+7+9.5])
# 7 = 2014, 8 = 2016

make_plot("Wm", "W^-", n_W, x_W, ex_W, y_Wm, ey_Wm)

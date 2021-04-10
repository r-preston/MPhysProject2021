#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
import math
import os

# measure Z boson xsec only.


def dimuon_plot(chain): 
    #Output Invariant mass distribution of dimuon system in fiducial region
    hist = ROOT.TH1F("dimuon_hist",";M_{#mu#mu} (GeV);Candidates",100,60.,120.)
    expression = "1.e-3*Z_M>>" + hist.GetName() 
    ch.Draw(expression,"Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5")
    canv = ROOT.TCanvas()
    hist.Draw()
    hist.SetStats(0)
    hist.GetXaxis().CenterTitle(1)
    hist.GetXaxis().SetTitleSize(0.04)
    hist.GetXaxis().SetLabelSize(0.04)
    hist.GetYaxis().CenterTitle(1)
    hist.GetYaxis().SetTitleSize(0.04)
    hist.GetYaxis().SetLabelSize(0.04)
    hist.GetYaxis().SetTitleOffset(1.05)

    legend = ROOT.TLegend(0.55,0.8,0.9,0.9)
    legend.AddEntry(hist, "Invariant dimuon mass of Z candidates","l")
    #legend.SetTextSize(0.04)
    legend.Draw()

    canv.SaveAs("plots/Z_dimuon_plot.pdf")
    canv.Close()
   

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

#Output Invariant mass distribution of dimuon system in fiducial region
#dimuon_plot(ch)

#Calculate Z xsec
count = ch.GetEntries("Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5")

count_rel_unc = math.sqrt(count)/count

with open('results_json/luminosity.json') as json_file:
    luminosity = json.load(json_file)

lumi = luminosity["luminosity"]
lumi_err = luminosity["luminosity_err"]

with open('results_json/efficiencies.json') as json_file:
    efficiencies = json.load(json_file)

trig_eff = efficiencies["trigger_efficiency"]
trig_eff_rel_unc = efficiencies["trigger_eff_error"]

xsec = count/(lumi*trig_eff)

xsec_err_stat = xsec * (count_rel_unc)
xsec_err_lumi = xsec * (lumi_err/lumi)
xsec_err_eff = xsec * (trig_eff_rel_unc)
xsec_err = math.sqrt(xsec_err_stat**2 + xsec_err_eff**2 + xsec_err_lumi**2)

#print('Z Count = {}'.format(count))
#print('Z Count Relative Uncertainty = {}'.format(count_rel_unc))

#print('Z Cross Section (pb) = {}'.format(xsec))
#print('XSec Error (pb) = {}'.format(xsec_err))
#print('Stat Error (pb) = {}'.format(xsec_err_stat))
#print('Efficiency Error (pb) = {}'.format(xsec_err_eff))
#print('Luminosity Error (pb) = {}'.format(xsec_err_lumi))

data_output = {"count":count, "count_rel_uncertainty":count_rel_unc, "xsec":xsec, "xsec_err":xsec_err, "xsec_err_stat":xsec_err_stat, "xsec_err_eff":xsec_err_eff, "xsec_err_lumi":xsec_err_lumi}

with open('results_json/Z_xsec.json', 'w') as outfile:
    json.dump(data_output,outfile)

stat_txt = "{"+"\\"+"rm stat}"
eff_txt = "{"+"\\"+"rm eff}"
lumi_txt = "{"+"\\"+"rm lumi}"
xsec_unit = "\\"+"rm pb"

current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')

with open(save_path+'Z_xsec_output.tex', 'w') as texfile:
    texfile.write("\\"+"begin{equation}\n")
    texfile.write("\sigma_{{Z\\xrightarrow{{}}\mu^+\mu^-}} = {:.{prec}f} \pm {:.{prec}f}_{stat_txt} \pm {:.{prec}f}_{eff_txt} \pm {:.{prec}f}_{lumi_txt} \; {xsec_unit},\n".format(xsec, xsec_err_stat, xsec_err_eff, xsec_err_lumi, stat_txt=stat_txt,  eff_txt=eff_txt, lumi_txt=lumi_txt, xsec_unit=xsec_unit, prec=2))
    texfile.write("\\"+"end{equation}")

with open(save_path+'counts_output.tex', 'w') as texfile:
    texfile.write("Counts in Fiducial Region = ${} \pm {:.0f} \; \\rm counts$\\\\".format(count, count*count_rel_unc))
    texfile.write("Counts Relative Uncertainty = ${:.4f}$\\\\".format(count_rel_unc))

with open(save_path+'Z_xsec_value.tex', 'w') as texfile:
    texfile.write("${:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f}$".format(xsec, xsec_err_stat, xsec_err_eff, xsec_err_lumi, stat_txt=stat_txt,  eff_txt=eff_txt, lumi_txt=lumi_txt, prec=2))

#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
import math

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

count = ch.GetEntries("Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5")

count_err = math.sqrt(count)/count

with open('luminosity.json') as json_file:
    luminosity = json.load(json_file)

lumi = luminosity["luminosity"]
lumi_err = luminosity["luminosity_err"]

with open('efficiencies.json') as json_file:
    efficiencies = json.load(json_file)

trig_eff = efficiencies["trigger_efficiency"]
trig_eff_err = efficiencies["trigger_eff_error"]

xsec = count/(lumi*trig_eff)
xsec_err = xsec * (count_err + trig_eff_err + lumi_err/lumi)

xsec_err_stat = xsec * count_err
xsec_err_eff = xsec * trig_eff_err
xsec_err_lumi = xsec * lumi_err/lumi

print('Z Count = {}'.format(count))
print('Z Count Relative Uncertainty = {}'.format(count_err))

print('Z Cross Section (pb) = {}'.format(xsec))
print('XSec Error (pb) = {}'.format(xsec_err))

print('Stat Error (pb) = {}'.format(xsec_err_stat))
print('Efficiency Error (pb) = {}'.format(xsec_err_eff))
print('Luminosity Error (pb) = {}'.format(xsec_err_lumi))

data_output = {"Z_count":count, "Z_count_rel_uncertainty":count_err, "Z_xsec":xsec, "Z_xsec_err":xsec_err}

with open('Z_xsec.json', 'w') as outfile:
    json.dump(data_output,outfile)

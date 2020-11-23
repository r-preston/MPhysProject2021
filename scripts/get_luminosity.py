#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

rfile = ROOT.TFile(file_path)
lumi_tuple = rfile.Get('GetIntegratedLuminosity/LumiTuple')

total_lumi = 0.0

total_lumi = sum([entry.IntegratedLuminosity for entry in lumi_tuple])
  
total_lumi_err = total_lumi*0.05

print('Integrated Luminosity (pb-1) = {}'.format(total_lumi))
print('IL 5% error (pb-1) = {}'.format(total_lumi_err))

data = {'luminosity':total_lumi, 'luminosity_err':total_lumi_err}

with open('luminosity.json', 'w') as outfile:
    json.dump(data,outfile)


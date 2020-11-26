#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
import os

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

rfile = ROOT.TFile(file_path)
lumi_tuple = rfile.Get('GetIntegratedLuminosity/LumiTuple')

total_lumi = sum([entry.IntegratedLuminosity for entry in lumi_tuple])

percent_err = 0.05
total_lumi_err = total_lumi*percent_err

#print('Integrated Luminosity (pb-1) = {}'.format(total_lumi))
#print('IL 5% error (pb-1) = {}'.format(total_lumi_err))

data = {'luminosity':total_lumi, 'luminosity_err':total_lumi_err}

with open('luminosity.json', 'w') as outfile:
    json.dump(data,outfile)

current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')
lumi_unit = "{" + "\\" + "rm pb^{-1}}"

with open(save_path+'lumi_output.tex', 'w') as texfile:
    texfile.write("Integrated Luminosity $L$ assumed to have percentage uncertainty of {}\%.\\\\".format(percent_err*100))
    texfile.write("$L = {:.{prec}f} \pm {:.{prec}f} \; {}$\\\\".format(total_lumi, total_lumi_err, lumi_unit, prec=1))

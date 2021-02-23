#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
import math
import os

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

fiducial_cuts = "Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5"

mup_trigger = float(ch.GetEntries(fiducial_cuts + " && mup_L0MuonDecision_TOS == 1"))
mum_trigger = float(ch.GetEntries(fiducial_cuts + " && mum_L0MuonDecision_TOS == 1"))
both_trigger = float(ch.GetEntries(fiducial_cuts + " && mup_L0MuonDecision_TOS == 1 && mum_L0MuonDecision_TOS == 1"))
N_total = float(ch.GetEntries(fiducial_cuts))

mup_eff = both_trigger/mum_trigger
mup_eff_err = math.sqrt(mup_eff*(1-mup_eff)/N_total)

mum_eff = both_trigger/mup_trigger
mum_eff_err = math.sqrt(mum_eff*(1-mum_eff)/N_total)

mup_mum_eff = mup_eff + mum_eff - mup_eff * mum_eff
mup_mum_eff_err = math.sqrt(mup_mum_eff*(1-mup_mum_eff)/N_total)


#print("Either Trigger Efficiency = {}".format(mup_mum_eff))
#print("Either Trigger Efficiency Relative Uncertainty = {}".format(mup_mum_eff_err))
#print("mup = {}, mum = {}, either = {}".format(mup_eff, mum_eff, mup_mum_eff))

data ={"mup_efficiency":mup_eff, "mup_eff_error":mup_eff_err, "mum_efficiency":mum_eff, "mum_eff_error":mum_eff_err, "trigger_efficiency":mup_mum_eff, "trigger_eff_error":mup_mum_eff_err}

with open('results_json/efficiencies.json', 'w') as outfile:
    json.dump(data,outfile)

current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')

with open(save_path+'trig_eff_output.tex', 'w') as texfile:
    texfile.write("Positive muon $\mu^+$ Trigger Efficiency $\\varepsilon^{{\mu^+}}$ = ${:.{prec}f} \pm {:.{prec}f}$\\\\".format(mup_eff, mup_eff*mup_eff_err, prec=3))
    texfile.write("Positive muon relative uncertainty = ${:.{prec}f}$\\\\".format(mup_eff_err, prec=4))
    texfile.write("Negative muon $\mu^-$ Trigger Efficiency $\\varepsilon^{{\mu^-}}$ = ${:.{prec}f} \pm {:.{prec}f}$\\\\".format(mum_eff, mum_eff*mum_eff_err, prec=3))
    texfile.write("Negative muon relative uncertainty = ${:.{prec}f}$\\\\".format(mum_eff_err, prec=4))
    texfile.write("Trigger Efficiency of Either muon $\\varepsilon^{{\mu\mu}}_{{\\rm trigger}}$ = ${:.{prec}f} \pm {:.{prec}f}$\\\\".format(mup_mum_eff, mup_mum_eff*mup_mum_eff_err, prec=4))
    texfile.write("Either muon Relative Uncertainty = ${:.{prec}f}$\\\\".format(mup_mum_eff_err, prec=5))

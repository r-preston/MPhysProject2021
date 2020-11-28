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

mup_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1"))
mum_trigger = float(ch.GetEntries("mum_L0MuonDecision_TOS == 1"))
both_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1 && mum_L0MuonDecision_TOS == 1"))
N_total = float(ch.GetEntries())

mup_eff = both_trigger/mum_trigger
mum_eff = both_trigger/mup_trigger

mup_mum_eff = mup_eff + mum_eff - mup_eff * mum_eff
mup_mum_eff_err = math.sqrt(mup_mum_eff*(1-mup_mum_eff)/N_total)


#print("Trigger Efficiency = {}".format(mup_mum_eff))
#print("Trigger Efficiency Relative Uncertainty = {}".format(mup_mum_eff_err))

data ={"mup":mup_eff, "mum":mum_eff, "trigger_efficiency":mup_mum_eff, "trigger_eff_error":mup_mum_eff_err}

with open('efficiencies.json', 'w') as outfile:
    json.dump(data,outfile)

current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')

with open(save_path+'trig_eff_output.tex', 'w') as texfile:
    texfile.write("Trigger Efficiency = ${:.{prec}f} \pm {:.{prec}f}$\\\\".format(mup_mum_eff, mup_mum_eff*mup_mum_eff_err, prec=4))
    texfile.write("Trigger Efficiency Relative Uncertainty = ${:.{prec}f}$\\\\".format(mup_mum_eff_err, prec=5))


#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json

data = {}

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

mup_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1"))
mum_trigger = float(ch.GetEntries("mum_L0MuonDecision_TOS == 1"))
both_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1 && mum_L0MuonDecision_TOS == 1"))


mup_eff = both_trigger/mum_trigger
mum_eff = both_trigger/mup_trigger

mup_mum_eff = mup_eff * mum_eff

print("Trigger Efficiency = {}".format(mup_mum_eff))

data ={"trigger_efficiency":mup_mum_eff}

with open('data.txt', 'r+') as outfile:
    data_file = json.load(outfile)
    data_file.update(data)
    outfile.seek(0)
    json.dump(data_file,outfile)

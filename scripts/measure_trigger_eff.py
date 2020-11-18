#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

mup_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1"))
mum_trigger = float(ch.GetEntries("mum_L0MuonDecision_TOS == 1"))
both_trigger = float(ch.GetEntries("mup_L0MuonDecision_TOS == 1 && mum_L0MuonDecision_TOS == 1"))


mup_eff = both_trigger/mum_trigger
mum_eff = both_trigger/mup_trigger

both_eff = 2*both_trigger/(mum_trigger+mup_trigger)

mup_mum_eff = mup_eff + mum_eff - both_eff

print(mup_trigger)
print(mum_trigger)
print(both_trigger)
print(mup_eff)
print(mum_eff)
print(both_eff)
print(mup_mum_eff)

#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

#import math
#mass = 0.105 #GeV
#mass2 = mass*mass

datadir = '/storage/epp2/phshgg/DVTuples__v23/'

ch_mnt = ROOT.TChain('Z/DecayTree')
ch_mnt.Add(datadir + '5TeV_2017_32_Down_EW.root')

ch_sim = ROOT.TChain('Z/DecayTree')
ch_sim.Add(datadir + '13TeV_2016_28r1_Down_Z_Sim09h.root')


# BRANCH INPUT
muon_prop = 'mup_PT'
muon_prop_unit = ' (GeV)'


# HISTOGRAM SET UP
hist_title = 'Measurement vs Simulation for ' + muon_prop
x_axis = muon_prop + muon_prop_unit
hist_setup = hist_title + ";" + x_axis

nbins = 100
xmin = 15
xmax = 60

hist_main = ROOT.THStack(muon_prop, hist_setup)

hist_mnt = ROOT.TH1F('measurement', hist_setup, nbins, xmin, xmax)

hist_sim = ROOT.TH1F('simulation', hist_setup, nbins, xmin, xmax)

# DATA ENTRY
if muon_prop == 'mup_PT' and muon_prop_unit == ' (GeV)': #Convert MeV -> GeV for mup_PT
    muon_branch = '1.e-3*mup_PT>>'
else:
    muon_branch = muon_prop + '>>'

ch_mnt.Draw(muon_branch+hist_mnt.GetName())
ch_sim.Draw(muon_branch+hist_sim.GetName())
    

# PLOT HISTOGRAM
hist_main.Add(hist_mnt)
hist_main.Add(hist_sim)
canv = ROOT.TCanvas()
hist_main.Draw('E')
canv.SaveAs('Measurement_' + muon_prop + ".pdf")

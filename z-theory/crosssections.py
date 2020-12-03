#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.stats import norm
#from functools import reduce

data_dir = './'
muon_ch = ROOT.TChain('mutree')
muon_ch.Add(data_dir+'zmuons.root')

xsec_ch = ROOT.TChain('xtree')
xsec_ch.Add(data_dir+'zmuons.root')

for e in xsec_ch:
  event_data = {
    'weight': e.weight,
    "num_generated": e.num_generated,
    "total_cross_section": e.total_cross_section,
    "numerical_error": e.numerical_error
  }
  break;

error_ratio = event_data['numerical_error']/event_data['total_cross_section']

print("Muon pair weighting: {:.2f}pb".format(event_data['weight']))
print("Events generated: {}".format(event_data['num_generated']))
print("Total cross section: ({:.2f} {} {:.2f})pb".format(event_data['total_cross_section'],  u"\u00B1".encode("utf-8"), event_data['numerical_error']))

mass_xsec = 0
pt_xsec = 0
eta_xsec = 0

for e in muon_ch:

  mup_P = ROOT.TLorentzVector()
  mup_P.SetPtEtaPhiM(e.mup_PT,
                     e.mup_ETA,
                     e.mup_PHI,
                     0.105
                    )

  mum_P = ROOT.TLorentzVector()
  mum_P.SetPtEtaPhiM(e.mum_PT,
                     e.mum_ETA,
                     e.mum_PHI,
                     0.105
                    )

  P = mup_P + mum_P
  M = P.Mag()  # convert to GeV

  if (M > 60) and (M < 120):
    mass_xsec += 1

  if(e.mup_PT > 20) and (e.mum_PT > 20):
    pt_xsec += 1

  if (e.mum_ETA > 2) and (e.mum_ETA < 4.5) and (e.mup_ETA > 2) and (e.mup_ETA < 4.5):
    eta_xsec += 1

mass_xsec *= event_data['weight']
pt_xsec *= event_data['weight']
eta_xsec *= event_data['weight']


print("\nCross section for 60GeV < M < 120GeV")
print("({:.2f} {} {:.2f})pb".format(mass_xsec, u"\u00B1".encode("utf-8"), mass_xsec*error_ratio))

print("\nCross section for pT > 20GeV")
print("({:.2f} {} {:.2f})pb".format(pt_xsec, u"\u00B1".encode("utf-8"), pt_xsec*error_ratio))

print("\nCross section for 2 < pseudorapidity < 4.5")
print("({:.2f} {} {:.2f})pb".format(eta_xsec, u"\u00B1".encode("utf-8"), eta_xsec*error_ratio))

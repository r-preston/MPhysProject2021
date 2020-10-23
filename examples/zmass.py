#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

data_dir = './data/'

ch = ROOT.TChain('Z/DecayTree')
ch.Add(data_dir+'5TeV_2017_32_Down_EW.root')

W = []

for e in ch:

  mup_P = ROOT.TLorentzVector()
  mup_P.SetPtEtaPhiE(e.mup_PT,
                     e.mup_ETA,
                     e.mup_PHI,
                     np.sqrt(105**2+(e.mup_PT*np.cosh(e.mup_ETA))**2)
                    )

  mum_P = ROOT.TLorentzVector()
  mum_P.SetPtEtaPhiE(e.mum_PT,
                     e.mum_ETA,
                     e.mum_PHI,
                     np.sqrt(105**2+(e.mum_PT*np.cosh(e.mum_ETA))**2)
                    )

  P = mup_P + mum_P

  W.append(P.Mag()*1E-3) # convert to GeV

# plot histogram
plt.hist(W, bins=100, range=(0,160), density=True)

# fit gaussian to histogram because why not
'''
mu, std = norm.fit(W)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
'''

plt.vlines(91.18, 0, 0.08,colors='red')


plt.show()
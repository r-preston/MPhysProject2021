#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

import math

ch = ROOT.TChain('Z/DecayTree')
ch.Add('/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root')

mass = 0.105 #GeV
mass2 = mass*mass

nbins = 100
xmin = 40.
xmax = 120.

hist = ROOT.TH1F('Invariant Mass of Z','Invariant Mass of Z->mu mu Decay;Invariant Mass (GeV)',nbins,xmin,xmax)
    
for entry in ch:
    #energy = sqrt(mass**2 + PT**2 * cosh(ETA)**2)
    
    mum_PT = entry.mum_PT*0.001 #MeV x 10 **3 -> GeV
    v_mum = ROOT.TLorentzVector()
    v_mum.SetPtEtaPhiE(mum_PT,
                       entry.mum_ETA,
                       entry.mum_PHI,
                       math.sqrt(mass2 + mum_PT*mum_PT * math.cosh(entry.mum_ETA)*math.cosh(entry.mum_ETA))
                       ) 
    
    mup_PT = entry.mup_PT*0.001 #MeV x 10 **3 -> GeV
    v_mup = ROOT.TLorentzVector()
    v_mup.SetPtEtaPhiE(mup_PT, 
                       entry.mup_ETA,
                       entry.mup_PHI,
                       math.sqrt(mass2 + mup_PT*mup_PT * math.cosh(entry.mup_ETA)*math.cosh(entry.mup_ETA))
                       ) 
    
    v = v_mum + v_mup

    IMass = v.Mag()
    hist.Fill(IMass)

#plot histogram with ROOT
canv = ROOT.TCanvas()
hist.Draw("E")
canv.SaveAs('ZMassPlots_ROOT.pdf')
   



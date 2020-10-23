#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

ch = ROOT.TChain('Z/DecayTree')
ch.Add('/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root')

import math

mass = 0.105*10**(-3)

def energy(mass, PT, ETA):
    temp = PT**2 * (math.cosh(ETA))**2
    return math.sqrt(mass**2+temp)

def calculation(mass, mup_PT, mup_ETA, mup_PHI, mum_PT, mum_ETA, mum_PHI, mup_energy, mum_energy):
 
    angles = math.cos(mup_PHI - mum_PHI) + math.sinh(mup_ETA)*math.sinh(mum_ETA)
    IMass = 2*(mass + mup_energy*mum_energy - mup_PT*mum_PT*angles)

    print("By calculation:", IMass)
    
for entry in ch:
    mum_PT = entry.mum_PT
    mum_ETA = entry.mum_ETA
    mum_PHI = entry.mum_PHI

    mup_PT = entry.mup_PT
    mup_ETA = entry.mup_ETA
    mup_PHI = entry.mup_PHI
    
    mup_energy = energy(mass, mup_PT, mup_ETA)
    mum_energy = energy(mass, mum_PT, mum_ETA)
    
    v_mum = ROOT.TLorentzVector()
    v_mup = ROOT.TLorentzVector()

    v_mum.SetPtEtaPhiE(mum_PT,mum_ETA,mum_PHI,mum_energy)
    v_mup.SetPtEtaPhiE(mup_PT,mup_ETA,mup_PHI,mup_energy)
    v = v_mum + v_mup

    IMassRoot = v.Mag2()

    print("By ROOT", IMassRoot)
    calculation(mass, mup_PT, mup_ETA, mup_PHI, mum_PT, mum_ETA, mum_PHI, mup_energy, mum_energy)


#This works out the calculation correctly provided energy is calculated correctly
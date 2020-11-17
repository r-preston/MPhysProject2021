#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"

rfile = ROOT.TFile(file_path)
lumi_tuple = rfile.Get('GetIntegratedLuminosity/LumiTuple')

total_lumi = 0.0
#total_lumi_err_sum = 0.0

for entry in lumi_tuple:
    #print(entry.IntegratedLuminosity, entry.IntegratedLuminosityErr)
    total_lumi += entry.IntegratedLuminosity
    #total_lumi_err_sum += entry.IntegratedLuminosityErr*entry.IntegratedLuminosityErr
    
#print(total_lumi)
#total_lumi_err = total_lumi_err_sum**0.5
#print(total_lumi_err)

ch = ROOT.TChain('Z/DecayTree')
ch.Add(file_path)

count = 0

for entry in ch:
    if(entry.Z_M*0.001 > 60 and entry.Z_M*0.001 < 120
       and entry.mup_PT*0.001 > 20 and entry.mum_PT*0.001 > 20
       and entry.mup_ETA > 2 and entry.mup_ETA < 4.5 and entry.mum_ETA > 2 and entry.mum_ETA < 4.5):
        count += 1

print('count = {}'.format(count))
xsec = count/total_lumi
xsec_err = xsec - (count/(total_lumi*1.05))
print('xsec = {}'.format(xsec))
print('xsec error = {}'.format(xsec_err))

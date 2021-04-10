#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT
import json
import math
import os

def xsec_calc(W_data, lumi, lumi_err, trig_eff, trig_eff_rel_unc):
    signal_frac = W_data["signal_frac"]
    signal_frac_err_stat = W_data["signal_frac_err_stat"]    
    signal_frac_err_sys = W_data["signal_frac_err_sys"]    
    W_events = W_data["W_data_events"]
    W_events_rel_unc = math.sqrt(W_events)/W_events

    counts = signal_frac * W_events
    counts_err_stat = counts * math.sqrt((signal_frac_err_stat/signal_frac)*(signal_frac_err_stat/signal_frac) + W_events_rel_unc*W_events_rel_unc)
    counts_err_sys = counts * (signal_frac_err_sys/signal_frac)

    xsec = counts/(lumi*trig_eff)
    
    xsec_err_stat = xsec * (counts_err_stat/counts)
    xsec_err_lumi = xsec * (lumi_err/lumi)
    xsec_err_eff = xsec * (trig_eff_rel_unc)
    xsec_err_track = xsec * (counts_err_sys/counts)
    xsec_err_sys = math.sqrt(xsec_err_eff**2 + xsec_err_track**2)
    xsec_err = math.sqrt(xsec_err_stat**2 + xsec_err_lumi**2 + xsec_err_sys**2)

    xsec_err_events = xsec*W_events_rel_unc
    xsec_err_signal = xsec*(signal_frac_err_stat/signal_frac)

    # statistical breakdown
    events_err = xsec*W_events_rel_unc
    signal_err = xsec*(signal_frac_err_stat/signal_frac)
    #print("Count err = {}, {}%".format(events_err,W_events_rel_unc*100))
    #print("Signal frac stat err = {}, {}%".format(signal_err,(signal_frac_err_stat/signal_frac)*100))
    #print("Original = {}, separate = {}".format(xsec_err_stat, math.sqrt(events_err**2 + signal_err**2)))

    # testing 
    #signal_test_err = math.sqrt(signal_frac_err_stat**2 + signal_frac_err_sys**2)
    #test_err = xsec * math.sqrt(W_events_rel_unc**2 + (lumi_err/lumi)**2 + trig_eff_rel_unc**2 + (signal_test_err/signal_frac)**2)
    #print("Propagated = {}, derived = {}".format(xsec_err, test_err))

    return xsec, xsec_err, xsec_err_stat, xsec_err_lumi, xsec_err_eff, xsec_err_track, xsec_err_sys, xsec_err_events, xsec_err_signal, counts, counts_err_stat, counts_err_sys


def Z_xsec_calc(lumi, lumi_err, trig_eff, trig_eff_rel_unc):
    # included to avoid floating point errors due to read in from other code
    file_path = "/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root"
    ch = ROOT.TChain('Z/DecayTree')
    ch.Add(file_path)
    count = ch.GetEntries("Z_M > 60.e3 && Z_M < 120.e3 && mup_PT > 20.e3 && mum_PT > 20.e3 && mup_ETA > 2 && mup_ETA < 4.5 && mum_ETA > 2 && mum_ETA < 4.5")
    count_rel_unc = math.sqrt(count)/count
    
    xsec = count/(lumi*trig_eff)

    xsec_err_stat = xsec * (count_rel_unc)
    xsec_err_lumi = xsec * (lumi_err/lumi)
    xsec_err_eff = xsec * (trig_eff_rel_unc)
    xsec_err = math.sqrt(xsec_err_stat**2 + xsec_err_eff**2 + xsec_err_lumi**2)
    #print("Z_xsec = {} + {} + {}".format(xsec,xsec_err_stat,xsec_err_eff))
    #print("statistical % = {}".format(count_rel_unc*100)) #statistical breakdown
    return xsec, xsec_err_stat, xsec_err_eff



# retrieve luminosity
with open('results_json/luminosity.json') as json_file:
    luminosity = json.load(json_file)
lumi = luminosity["luminosity"]
lumi_err = luminosity["luminosity_err"]

# retrieve trigger efficiency
with open('results_json/efficiencies.json') as json_file:
    efficiencies = json.load(json_file)
mup_eff = efficiencies["mup_efficiency"]
mup_eff_rel_unc = efficiencies["mup_eff_error"]
mum_eff = efficiencies["mum_efficiency"]
mum_eff_rel_unc = efficiencies["mum_eff_error"]
either_eff = efficiencies["trigger_efficiency"]
either_eff_rel_unc = efficiencies["trigger_eff_error"]

# retrive background data
with open('results_json/Wp_back_output.json') as json_file:
    Wp_back = json.load(json_file)

with open('results_json/Wm_back_output.json') as json_file:
    Wm_back = json.load(json_file)

# calculate cross sections
Wp_xsec, Wp_xsec_err, Wp_xsec_err_stat, Wp_xsec_err_lumi, Wp_xsec_err_eff, Wp_xsec_err_track, Wp_xsec_err_sys, Wp_xsec_err_events, Wp_xsec_err_signal, Wp_events, Wp_events_err_stat, Wp_events_err_sys = xsec_calc(Wp_back, lumi, lumi_err, mup_eff, mup_eff_rel_unc)
Wm_xsec, Wm_xsec_err, Wm_xsec_err_stat, Wm_xsec_err_lumi, Wm_xsec_err_eff, Wm_xsec_err_track, Wm_xsec_err_sys, Wm_xsec_err_events, Wm_xsec_err_signal, Wm_events, Wm_events_err_stat, Wm_events_err_sys = xsec_calc(Wm_back, lumi, lumi_err, mum_eff, mum_eff_rel_unc)

# output cross sections
Wp_xsec_output = {"count":Wp_events, "count_error_stat":Wp_events_err_stat, "count_error_sys":Wp_events_err_sys, "xsec":Wp_xsec, "xsec_err":Wp_xsec_err, "xsec_err_events":Wp_xsec_err_events, "xsec_err_signal":Wp_xsec_err_signal, "xsec_err_stat":Wp_xsec_err_stat, "xsec_err_lumi":Wp_xsec_err_lumi, "xsec_err_eff":Wp_xsec_err_eff, "xsec_err_track":Wp_xsec_err_track, "xsec_err_sys":Wp_xsec_err_sys}
with open('results_json/Wp_xsec.json', 'w') as outfile:
    json.dump(Wp_xsec_output,outfile)

Wm_xsec_output = {"count":Wm_events, "count_error_stat":Wm_events_err_stat, "count_error_sys":Wm_events_err_sys, "xsec":Wm_xsec, "xsec_err":Wm_xsec_err, "xsec_err_events":Wm_xsec_err_events, "xsec_err_signal":Wm_xsec_err_signal, "xsec_err_stat":Wm_xsec_err_stat, "xsec_err_lumi":Wm_xsec_err_lumi, "xsec_err_eff":Wm_xsec_err_eff, "xsec_err_track":Wm_xsec_err_track, "xsec_err_sys":Wm_xsec_err_sys}
with open('results_json/Wm_xsec.json', 'w') as outfile:
    json.dump(Wm_xsec_output,outfile)

#print('Wp events = {} + {}'.format(Wp_events, Wp_events_err))
#print('Wp xsec = {} + {}'.format(Wp_xsec, Wp_xsec_err))
#print('Wp xsec = {} + {} + {} + {}'.format(Wp_xsec, Wp_xsec_err_stat, Wp_xsec_err_sys, Wp_xsec_err_lumi))

#print('Wm events = {} + {}'.format(Wm_events, Wm_events_err))
#print('Wm xsec = {} + {}'.format(Wm_xsec, Wm_xsec_err))
#print('Wm xsec = {} + {} + {} + {}'.format(Wm_xsec, Wm_xsec_err_stat, Wm_xsec_err_sys, Wm_xsec_err_lumi))


# calculate Wp/Wm ratio
Wp_Wm_ratio = Wp_xsec/Wm_xsec
Wp_Wm_ratio_stat = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_stat/Wp_xsec)**2 + (Wm_xsec_err_stat/Wm_xsec)**2)
Wp_Wm_ratio_sys = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_sys/Wp_xsec)**2 + (Wm_xsec_err_sys/Wm_xsec)**2)
Wp_Wm_ratio_err = math.sqrt(Wp_Wm_ratio_stat**2 + Wp_Wm_ratio_sys**2)

Wp_Wm_ratio_eff = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_eff/Wp_xsec)**2 + (Wm_xsec_err_eff/Wm_xsec)**2)
Wp_Wm_ratio_track = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_track/Wp_xsec)**2 + (Wm_xsec_err_track/Wm_xsec)**2)
Wp_Wm_ratio_events = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_events/Wp_xsec)**2 + (Wm_xsec_err_events/Wm_xsec)**2)
Wp_Wm_ratio_signal = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_signal/Wp_xsec)**2 + (Wm_xsec_err_signal/Wm_xsec)**2)

#print("WW events = {}, {}%; WW signal = {}, {}%".format(Wp_Wm_ratio_events,Wp_Wm_ratio_events/Wp_Wm_ratio*100,Wp_Wm_ratio_signal,Wp_Wm_ratio_signal/Wp_Wm_ratio*100))

# testing and output
#r = Wp_events/Wm_events * mum_eff/mup_eff
#r_err = r*math.sqrt((Wp_events_err/Wp_events)**2 + (Wm_events_err/Wm_events)**2 + mum_eff_rel_unc**2 + mup_eff_rel_unc**2)
#print('Wp/Wm = {} + {} stat + {} eff'.format(Wp_Wm_ratio, Wp_Wm_ratio_stat, Wp_Wm_ratio_eff))
#print('Wp/Wm = {} + {} derived + {} propagated'.format(r, r_err, Wp_Wm_ratio_err))
#print("{}, {}".format(Wp_Wm_ratio_sys, math.sqrt(Wp_Wm_ratio_eff**2 + Wp_Wm_ratio_track**2)))

# calculate (Wp+Wm)/Z ratio
#retrieve Z xsec
Z_xsec, Z_xsec_err_stat, Z_xsec_err_eff = Z_xsec_calc(lumi, lumi_err, either_eff, either_eff_rel_unc)
W_Z_ratio = (Wp_xsec+Wm_xsec)/Z_xsec
Wp_coeff = ((Wp_events/mup_eff)**2)/((Wp_events/mup_eff + Wm_events/mum_eff)**2)
Wm_coeff = ((Wm_events/mum_eff)**2)/((Wp_events/mup_eff + Wm_events/mum_eff)**2)

W_Z_ratio_stat = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_stat/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_stat/Wm_xsec)**2) + (Z_xsec_err_stat/Z_xsec)**2)
W_Z_ratio_sys = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_sys/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_sys/Wm_xsec)**2) + (Z_xsec_err_eff/Z_xsec)**2)
W_Z_ratio_err = math.sqrt(W_Z_ratio_stat**2 + W_Z_ratio_sys**2)

W_Z_ratio_eff = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_eff/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_eff/Wm_xsec)**2) + (Z_xsec_err_eff/Z_xsec)**2)
W_Z_ratio_track = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_track/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_track/Wm_xsec)**2))
W_Z_ratio_events = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_events/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_events/Wm_xsec)**2) + (Z_xsec_err_stat/Z_xsec)**2)
W_Z_ratio_signal = W_Z_ratio * math.sqrt(Wp_coeff*((Wp_xsec_err_signal/Wp_xsec)**2) + Wm_coeff*((Wm_xsec_err_signal/Wm_xsec)**2))

#print("{}, {}".format(W_Z_ratio_sys, math.sqrt(W_Z_ratio_eff**2 + W_Z_ratio_track**2)))
#print('W/Z = {} + {} + {}'.format(W_Z_ratio, W_Z_ratio_stat, W_Z_ratio_eff))
#print("WZ events = {}, {}%; WZ signal = {}, {}%".format(W_Z_ratio_events,W_Z_ratio_events/W_Z_ratio*100,W_Z_ratio_signal,W_Z_ratio_signal/W_Z_ratio*100))

# output ratios
ratio_output = {"WW_ratio":Wp_Wm_ratio, "WW_error":Wp_Wm_ratio_err, "WW_stat":Wp_Wm_ratio_stat, "WW_sys": Wp_Wm_ratio_sys, "WW_eff":Wp_Wm_ratio_eff, "WW_track":Wp_Wm_ratio_track, "WW_events":Wp_Wm_ratio_events, "WW_signal":Wp_Wm_ratio_signal, "WZ_ratio":W_Z_ratio, "WZ_error":W_Z_ratio_err, "WZ_stat":W_Z_ratio_stat, "WZ_sys": W_Z_ratio_sys, "WZ_eff":W_Z_ratio_eff, "WZ_track":W_Z_ratio_track, "WZ_events":W_Z_ratio_events, "WZ_signal":W_Z_ratio_signal}
with open('results_json/Ratios.json','w') as outfile:
    json.dump(ratio_output,outfile)

# testing and output
#with open('results_json/Z_xsec.json') as Z_xsec_file:
#    Z_xsec_input = json.load(Z_xsec_file)

#Z_events = Z_xsec_input["count"]
#Z_events_rel_unc = Z_xsec_input["count_rel_uncertainty"] 

#pos_err = (Wp_events/mup_eff)*math.sqrt((mup_eff_rel_unc)**2+(Wp_events_err/Wp_events)**2)
#neg_err = (Wm_events/mum_eff)*math.sqrt((mum_eff_rel_unc)**2+(Wm_events_err/Wm_events)**2)
#W_err = math.sqrt(pos_err**2 + neg_err**2)
#numerator = (Wp_events/mup_eff)+(Wm_events/mum_eff) 
#R = (numerator)/(Z_events/either_eff)
#R_err = R*math.sqrt((W_err/numerator)**2 + either_eff_rel_unc**2 + Z_events_rel_unc**2)

#A = ((Wp_events/mup_eff)/numerator)**2
#B = (Wm_events/mum_eff)**2/numerator**2
#print("A = {}, B = {}, wp coef = {}, wm coef = {}".format(A,B,Wp_coeff,Wm_coeff))

#derived_stat = R*math.sqrt(A*(Wp_events_err/Wp_events)**2+B*(Wm_events_err/Wm_events)**2+(Z_events_rel_unc)**2)
#derived_eff = R*math.sqrt(A*(mup_eff_rel_unc)**2+B*(mum_eff_rel_unc)**2+(either_eff_rel_unc)**2)
#derived_both = math.sqrt(derived_stat**2 + derived_eff**2)
#print("derived = {} + {}, propagated = {} + {}".format(R, R_err, W_Z_ratio, W_Z_ratio_err))
#print("derived = {} stat + {} eff, sum = {}".format(derived_stat,derived_eff,derived_both))
#print("derived = {}. propagated = {}".format(

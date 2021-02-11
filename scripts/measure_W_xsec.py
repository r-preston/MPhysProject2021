#!/usr/bin/env python
import json
import math
import os

def xsec_calc(W_data, lumi, lumi_err):
    signal_frac = W_data["signal_frac"]
    signal_frac_err = W_data["signal_frac_err"]    
    W_events = W_data["W_data_events"]
    W_events_rel_unc = math.sqrt(W_events)/W_events

    counts = signal_frac * W_events
    counts_err = counts * math.sqrt((signal_frac_err/signal_frac)*(signal_frac_err/signal_frac) + W_events_rel_unc*W_events_rel_unc)

    xsec = counts/lumi
    xsec_err_stat = xsec * (counts_err/counts )
    xsec_err_lumi = xsec * (lumi_err/lumi)    
    xsec_err = xsec_err_stat + xsec_err_lumi

    return xsec, xsec_err, xsec_err_stat, xsec_err_lumi, counts, counts_err



# retrieve luminosity
with open('luminosity.json') as json_file:
    luminosity = json.load(json_file)
lumi = luminosity["luminosity"]
lumi_err = luminosity["luminosity_err"]

# retrive background data
with open('Wp_back_output.json') as json_file:
    Wp_back = json.load(json_file)

with open('Wm_back_output.json') as json_file:
    Wm_back = json.load(json_file)

# calculate cross sections
Wp_xsec, Wp_xsec_err, Wp_xsec_err_stat, Wp_xsec_err_lumi, Wp_events, Wp_events_err = xsec_calc(Wp_back, lumi, lumi_err)
Wm_xsec, Wm_xsec_err, Wm_xsec_err_stat, Wm_xsec_err_lumi, Wm_events, Wm_events_err = xsec_calc(Wm_back, lumi, lumi_err)

# output cross sections
Wp_xsec_output = {"count":Wp_events, "count_error":Wp_events_err, "xsec":Wp_xsec, "xsec_err":Wp_xsec_err, "xsec_err_stat":Wp_xsec_err_stat, "xsec_err_lumi":Wp_xsec_err_lumi}
with open('Wp_xsec.json', 'w') as outfile:
    json.dump(Wp_xsec_output,outfile)

Wm_xsec_output = {"count":Wm_events, "count_error":Wm_events_err, "xsec":Wm_xsec, "xsec_err":Wm_xsec_err, "xsec_err_stat":Wm_xsec_err_stat, "xsec_err_lumi":Wm_xsec_err_lumi}
with open('Wm_xsec.json', 'w') as outfile:
    json.dump(Wm_xsec_output,outfile)


print('Wp events = {} + {}'.format(Wp_events, Wp_events_err))
print('Wp xsec = {} + {}'.format(Wp_xsec, Wp_xsec_err))
print('Wp xsec = {} + {} + {}'.format(Wp_xsec, Wp_xsec_err_stat, Wp_xsec_err_lumi))

print('Wm events = {} + {}'.format(Wm_events, Wm_events_err))
print('Wm xsec = {} + {}'.format(Wm_xsec, Wm_xsec_err))
print('Wm xsec = {} + {} + {}'.format(Wm_xsec, Wm_xsec_err_stat, Wm_xsec_err_lumi))


# calculate Wp/Wm ratio
Wp_Wm_ratio = Wp_xsec/Wm_xsec
Wp_Wm_ratio_err = Wp_Wm_ratio * math.sqrt((Wp_xsec_err/Wp_xsec)**2+(Wm_xsec_err/Wm_xsec)**2)

Wp_Wm_ratio_stat = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_stat/Wp_xsec)**2+(Wm_xsec_err_stat/Wm_xsec)**2)
Wp_Wm_ratio_lumi = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_lumi/Wp_xsec)**2+(Wm_xsec_err_lumi/Wm_xsec)**2)
combo_test = Wp_Wm_ratio * math.sqrt((Wp_xsec_err_lumi/Wp_xsec)**2+(Wm_xsec_err_lumi/Wm_xsec)**2 + (Wp_xsec_err_stat/Wp_xsec)**2+(Wm_xsec_err_stat/Wm_xsec)**2)

print('Wp/Wm = {} + {}'.format(Wp_Wm_ratio, Wp_Wm_ratio_err))
print('Wp/Wm, separeted error = {} + {} stat + {} lumi  (+ {} sum vs {} combo test)'.format(Wp_Wm_ratio, Wp_Wm_ratio_stat,Wp_Wm_ratio_lumi,Wp_Wm_ratio_stat+Wp_Wm_ratio_lumi,combo_test))

# calculate (Wp+Wm)/Z ratio
#retrieve Z xsec
with open('xsec.json') as Z_xsec_file:
    Z_xsec_input = json.load(Z_xsec_file)
Z_xsec = Z_xsec_input["xsec"]
Z_xsec_err = Z_xsec_input["xsec_err"]
Z_xsec_err_stat = Z_xsec_input["xsec_err_stat"]

W_Z_ratio = (Wp_xsec+Wm_xsec)/Z_xsec
W_Z_ratio_err = W_Z_ratio * math.sqrt((Wp_xsec_err**2 + Wm_xsec_err**2)/(Wp_xsec + Wm_xsec)**2 + (Z_xsec_err/Z_xsec)**2)
W_Z_ratio_stat = W_Z_ratio * math.sqrt((Wp_xsec_err_stat**2 + Wm_xsec_err_stat**2)/(Wp_xsec + Wm_xsec)**2 + (Z_xsec_err_stat/Z_xsec)**2)

print('W/Z = {} + {}'.format(W_Z_ratio, W_Z_ratio_err))
print('W/Z, stat error = {} + {}'.format(W_Z_ratio, W_Z_ratio_stat))

# output ratios
ratio_output = {"WW_ratio":Wp_Wm_ratio, "WW_error":Wp_Wm_ratio_err, "WZ_ratio":W_Z_ratio, "WZ_error":W_Z_ratio_err, "WW_error_stat":Wp_Wm_ratio_stat, "WZ_error_stat":W_Z_ratio_stat}
with open('Ratios.json','w') as outfile:
    json.dump(ratio_output,outfile)

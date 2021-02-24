#!/usr/bin/env python
import json
import math
import os

def xsec_calc(W_data, lumi, lumi_err, trig_eff, trig_eff_rel_unc):
    signal_frac = W_data["signal_frac"]
    signal_frac_err = W_data["signal_frac_err"]    
    W_events = W_data["W_data_events"]
    W_events_rel_unc = math.sqrt(W_events)/W_events

    counts = signal_frac * W_events
    counts_err = counts * math.sqrt((signal_frac_err/signal_frac)*(signal_frac_err/signal_frac) + W_events_rel_unc*W_events_rel_unc)

    xsec = counts/(lumi*trig_eff)
    xsec_err = xsec*math.sqrt((counts_err/counts)**2+(lumi_err/lumi)**2+trig_eff_rel_unc**2)
    xsec_err_stat = xsec_err * (counts_err/counts)**2/(xsec_err/xsec)**2
    xsec_err_lumi = xsec_err * (lumi_err/lumi)**2/(xsec_err/xsec)**2    
    xsec_err_eff = xsec_err * trig_eff_rel_unc**2/(xsec_err/xsec)**2
    #print("{} added vs {} propagation".format(xsec_err_stat+xsec_err_lumi+xsec_err_eff,xsec_err))
    return xsec, xsec_err, xsec_err_stat, xsec_err_lumi, xsec_err_eff, counts, counts_err



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

# retrive background data
with open('results_json/Wp_back_output.json') as json_file:
    Wp_back = json.load(json_file)

with open('results_json/Wm_back_output.json') as json_file:
    Wm_back = json.load(json_file)

# calculate cross sections
Wp_xsec, Wp_xsec_err, Wp_xsec_err_stat, Wp_xsec_err_lumi, Wp_xsec_err_eff, Wp_events, Wp_events_err = xsec_calc(Wp_back, lumi, lumi_err, mup_eff, mup_eff_rel_unc)
Wm_xsec, Wm_xsec_err, Wm_xsec_err_stat, Wm_xsec_err_lumi, Wm_xsec_err_eff, Wm_events, Wm_events_err = xsec_calc(Wm_back, lumi, lumi_err, mum_eff, mum_eff_rel_unc)

# output cross sections
Wp_xsec_output = {"count":Wp_events, "count_error":Wp_events_err, "xsec":Wp_xsec, "xsec_err":Wp_xsec_err, "xsec_err_stat":Wp_xsec_err_stat, "xsec_err_lumi":Wp_xsec_err_lumi, "xsec_err_eff":Wp_xsec_err_eff}
with open('results_json/Wp_xsec.json', 'w') as outfile:
    json.dump(Wp_xsec_output,outfile)

Wm_xsec_output = {"count":Wm_events, "count_error":Wm_events_err, "xsec":Wm_xsec, "xsec_err":Wm_xsec_err, "xsec_err_stat":Wm_xsec_err_stat, "xsec_err_lumi":Wm_xsec_err_lumi, "xsec_err_eff":Wm_xsec_err_eff}
with open('results_json/Wm_xsec.json', 'w') as outfile:
    json.dump(Wm_xsec_output,outfile)


#print('Wp events = {} + {}'.format(Wp_events, Wp_events_err))
#print('Wp xsec = {} + {}'.format(Wp_xsec, Wp_xsec_err))
#print('Wp xsec = {} + {} + {} + {}'.format(Wp_xsec, Wp_xsec_err_stat, Wp_xsec_err_eff, Wp_xsec_err_lumi))

#print('Wm events = {} + {}'.format(Wm_events, Wm_events_err))
#print('Wm xsec = {} + {}'.format(Wm_xsec, Wm_xsec_err))
#print('Wm xsec = {} + {} + {} + {}'.format(Wm_xsec, Wm_xsec_err_stat, Wm_xsec_err_eff, Wm_xsec_err_lumi))


# calculate Wp/Wm ratio
Wp_Wm_ratio = Wp_xsec/Wm_xsec
Wp_stat = Wp_xsec_err/(Wp_xsec**2) * Wp_xsec_err_stat
Wm_stat = Wm_xsec_err/(Wm_xsec**2) * Wm_xsec_err_stat
Wp_eff  = Wp_xsec_err/(Wp_xsec**2) * Wp_xsec_err_eff
Wm_eff  = Wm_xsec_err/(Wm_xsec**2) * Wm_xsec_err_eff
Wp_Wm_ratio_err = Wp_Wm_ratio * math.sqrt(Wp_stat + Wm_stat + Wp_eff + Wm_eff)
Wp_Wm_ratio_stat= Wp_Wm_ratio_err * (Wp_stat + Wm_stat)/((Wp_Wm_ratio_err/Wp_Wm_ratio)**2)
Wp_Wm_ratio_eff = Wp_Wm_ratio_err * (Wp_eff + Wm_eff)/((Wp_Wm_ratio_err/Wp_Wm_ratio)**2)

# testing and output
#r = Wp_events/Wm_events * mum_eff/mup_eff
#r_err = r*math.sqrt((Wp_events_err/Wp_events)**2 + (Wm_events_err/Wm_events)**2 + mum_eff_rel_unc**2 + mup_eff_rel_unc**2)
#print('Wp/Wm = {} + {} stat + {} eff'.format(Wp_Wm_ratio, Wp_Wm_ratio_stat, Wp_Wm_ratio_eff))
#print('Wp/Wm = {} + {} separate + {} derived + {} propagated'.format(r, Wp_Wm_ratio_stat+Wp_Wm_ratio_eff, r_err, Wp_Wm_ratio_err))

# calculate (Wp+Wm)/Z ratio
#retrieve Z xsec
with open('results_json/Z_xsec.json') as Z_xsec_file:
    Z_xsec_input = json.load(Z_xsec_file)
Z_xsec = Z_xsec_input["xsec"]
Z_xsec_err = Z_xsec_input["xsec_err"]
Z_xsec_err_stat = Z_xsec_input["xsec_err_stat"]
Z_xsec_err_eff = Z_xsec_input["xsec_err_eff"]

Z_events = Z_xsec_input["count"]
Z_events_rel_unc = Z_xsec_input["count_rel_uncertainty"] 
either_eff = efficiencies["trigger_efficiency"]
either_eff_rel_unc = efficiencies["trigger_eff_error"]

W_Z_ratio = (Wp_xsec+Wm_xsec)/Z_xsec
Z_stat = Z_xsec_err/(Z_xsec**2) * Z_xsec_err_stat
Z_eff = Z_xsec_err/(Z_xsec**2) * Z_xsec_err_eff

Wp_coeff = ((Wp_events/mup_eff)**2)/((Wp_events/mup_eff + Wm_events/mum_eff)**2)
Wm_coeff = ((Wm_events/mum_eff)**2)/((Wp_events/mup_eff + Wm_events/mum_eff)**2)

W_Z_ratio_err = W_Z_ratio * math.sqrt(Wp_coeff*Wp_stat + Wm_coeff*Wm_stat + Z_stat + Wp_coeff*Wp_eff + Wm_coeff*Wm_eff + Z_eff)
W_Z_ratio_stat = W_Z_ratio_err * (Wp_coeff*Wp_stat + Wm_coeff*Wm_stat + Z_stat)/((W_Z_ratio_err/W_Z_ratio)**2)
W_Z_ratio_eff = W_Z_ratio_err * (Wp_coeff*Wp_eff + Wm_coeff*Wm_eff + Z_eff)/((W_Z_ratio_err/W_Z_ratio)**2)

#print('W/Z = {} + {} + {}'.format(W_Z_ratio, W_Z_ratio_stat, W_Z_ratio_eff))

# output ratios
ratio_output = {"WW_ratio":Wp_Wm_ratio, "WW_error":Wp_Wm_ratio_err, "WW_stat":Wp_Wm_ratio_stat, "WW_eff":Wp_Wm_ratio_eff, "WZ_ratio":W_Z_ratio, "WZ_error":W_Z_ratio_err, "WZ_stat":W_Z_ratio_stat, "WZ_eff":W_Z_ratio_eff}
with open('results_json/Ratios.json','w') as outfile:
    json.dump(ratio_output,outfile)

# testing and output
#pos_err = (Wp_events/mup_eff)*math.sqrt((mup_eff_rel_unc)**2+(Wp_events_err/Wp_events)**2)
#neg_err = (Wm_events/mum_eff)*math.sqrt((mum_eff_rel_unc)**2+(Wm_events_err/Wm_events)**2)
#W_err = math.sqrt(pos_err**2 + neg_err**2)
#numerator = (Wp_events/mup_eff)+(Wm_events/mum_eff) 
#R = (numerator)/(Z_events/either_eff)
#R_err = R*math.sqrt((W_err/numerator)**2 + either_eff_rel_unc**2 + Z_events_rel_unc**2)

#A = (Wp_events/mup_eff)**2/numerator**2
#B = (Wm_events/mum_eff)**2/numerator**2
#print("A = {}, B = {}, wp coef = {}, wm coef = {}".format(A,B,Wp_coeff,Wm_coeff))

#print("Separate = {} + {}, derived = {} + {}, propagated = {} + {}".format(W_Z_ratio, W_Z_ratio_stat+W_Z_ratio_eff, R, R_err, W_Z_ratio, W_Z_ratio_err))

#!/usr/bin/env python
import json
import math
import os

def Z_fraction_output(save_path, boson, json_in):
    with open(save_path+boson+'_Z_frac_output.tex', 'w') as texfile:
        texfile.write("{} Calculated Z fraction = ${:.{prec}f} \pm {:.{prec}f}$\\\\".format(boson, json_in["Z_frac_calc"], json_in["Z_frac_err_calc"], prec=3))
    
def fit_fraction_output(save_path, boson, json_in):
    with open(save_path+boson+'_fit_fracs_output.tex', 'w') as texfile:
        texfile.write("{} $\pi/K$ background fraction = ${:.{prec}f} \pm {:.{prec}f}$\\\\\n".format(boson, json_in["K_frac"], json_in["K_frac_err"], prec=3))
        texfile.write("{} Signal fraction = ${:.{prec}f} \pm {:.{prec}f}$\\\\\n".format(boson, json_in["signal_frac"], json_in["signal_frac_err"], prec=3))
        texfile.write("{} $Z$ background fraction = ${:.{prec}f} \pm {:.{prec}f}$\\\\\n".format(boson, json_in["Z_frac"], json_in["Z_frac_err"], prec=3))
        texfile.write("{} TFractionFitter fit $\chi^2/$ndf = {:.{prec}f}/{}\\\\\n".format(boson, json_in["chi_squared"], json_in["ndf"], prec=1))

def event_table_output(save_path, Wp, Wm):
    Wp_Z_predicted = Wp["W_in_Z_sim_events"]*Wp["Z_data_events"]/Wp["Z_in_Z_sim_events"]
    Wp_Z_predicted_err = Wp_Z_predicted*(Wp["W_in_Z_sim_events"]**(-0.5) + Wp["Z_data_events"]**(-0.5) + Wp["Z_in_Z_sim_events"]**(-0.5))

    Wm_Z_predicted = Wm["W_in_Z_sim_events"]*Wm["Z_data_events"]/Wm["Z_in_Z_sim_events"]
    Wm_Z_predicted_err = Wm_Z_predicted*(Wm["W_in_Z_sim_events"]**(-0.5) + Wm["Z_data_events"]**(-0.5) + Wm["Z_in_Z_sim_events"]**(-0.5))

    with open(save_path+'W_event_table_output.tex','w') as texfile:
        texfile.write("\\begin{table}[h]\n")
        texfile.write("\\centering\n")
        texfile.write("\\begin{tabular}{lcc}\n")

        texfile.write("\\hline\n & Number of $W^+$ events & Number of $W^-$ events\\\\\n\\hline\n")
        texfile.write("$\pi/K$ Background & {:.{prec}f} & {:.{prec}f} \\\\\n".format(Wp["pi_K_events"],Wm["pi_K_events"],prec=0))
        texfile.write("$W$ Signal & {:.{prec}f} & {:.{prec}f} \\\\\n".format(Wp["signal_events"],Wm["signal_events"],prec=0))
        texfile.write("$W$ events in $Z$ simulation & {:.{prec}f} & {:.{prec}f} \\\\\n".format(Wp["W_in_Z_sim_events"],Wm["W_in_Z_sim_events"],prec=0))
        texfile.write("$Z$ events in $Z$ simulation & \multicolumn{{2}}{{c}}{{{:.{prec}f}}} \\\\\n".format(Wp["Z_in_Z_sim_events"],prec=0,open_bra="{",close="}"))
        texfile.write("$Z$ in Experimental Data & \multicolumn{{2}}{{c}}{{{:.{prec}f}}} \\\\\n".format(Wp["Z_data_events"],prec=0,open_bra="{",close="}"))
        texfile.write("Predicted $Z$ events in $W$ Data & ${:.{prec}f} \pm {:.{prec}f}$ & ${:.{prec}f} \pm {:.{prec}f}$ \\\\\n".format(Wp_Z_predicted, Wp_Z_predicted_err, Wm_Z_predicted, Wm_Z_predicted_err, prec=0))
        texfile.write("$W$ in Experimental Data & {:.{prec}f} & {:.{prec}f} \\\\\n".format(Wp["W_data_events"],Wm["W_data_events"],prec=0))

        texfile.write("\\hline\n")
        texfile.write("\\end{tabular}\n")
        texfile.write("\\caption{\small Number of events selected after cuts for $W^+$ and $W^-$ for each background contributions and $W$ experimental data. Additionally, the predicted number of $Z$ events in the $W$ data is given, with the decay trees used to calculate this.}\n")
        texfile.write("\\label{tab: W events}\n")
        texfile.write("\\end{table}\n")


with open('Wp_output.json') as json_file:
    Wp_output = json.load(json_file)

with open('Wm_output.json') as json_file:
    Wm_output = json.load(json_file)

current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')

Z_fraction_output(save_path, "Wp", Wp_output)
Z_fraction_output(save_path, "Wm", Wm_output)

fit_fraction_output(save_path, "Wp", Wp_output)
fit_fraction_output(save_path, "Wm", Wm_output)

event_table_output(save_path, Wp_output, Wm_output)

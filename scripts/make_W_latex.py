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
        texfile.write("{} Signal fraction = ${:.{prec}f} \pm {:.{prec}f}_{{\\rm stat}} \pm {:.{prec}f}_{{\\rm sys}}$\\\\\n".format(boson, json_in["signal_frac"], json_in["signal_frac_err_stat"], json_in["signal_frac_err_sys"], prec=3))
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

def xsec_output (save_path, boson, label, json_in):
    xsec = json_in["xsec"]
    xsec_err_stat = json_in["xsec_err_stat"]
    xsec_err_lumi = json_in["xsec_err_lumi"]
    xsec_err_sys = json_in["xsec_err_sys"]    

    with open(save_path+boson+'_xsec_output.tex', 'w') as texfile:
        texfile.write("\\"+"begin{equation}\n")
        texfile.write("\sigma_{} = {:.{prec}f} \pm {:.{prec}f}_{{\\rm stat}} \pm {:.{prec}f}_{{\\rm sys}} \pm {:.{prec}f}_{{\\rm lumi}} \; {{\\rm pb}},\n".format(label, xsec, xsec_err_stat, xsec_err_sys, xsec_err_lumi, prec=0))
        texfile.write("\\"+"end{equation}\n")
    
    with open(save_path+boson+'_xsec_value.tex', 'w') as texfile:
        texfile.write("${:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f}$".format(xsec, xsec_err_stat, xsec_err_sys, xsec_err_lumi, prec=0))


def systematic_table(save_path, Wp_xsec_json, Wm_xsec_json, ratios_json):
    with open(save_path+'sys_unc_table_output.tex','w') as texfile:
        Wp_xsec_err_eff = Wp_xsec_json["xsec_err_eff"]
        Wp_xsec_err_track = Wp_xsec_json["xsec_err_track"]
        Wp_xsec_err_sys = Wp_xsec_json["xsec_err_sys"]    
        Wm_xsec_err_eff = Wm_xsec_json["xsec_err_eff"]
        Wm_xsec_err_track = Wm_xsec_json["xsec_err_track"]
        Wm_xsec_err_sys = Wm_xsec_json["xsec_err_sys"]    
        WW_ratio_eff = ratios_json["WW_eff"]
        WW_ratio_track = ratios_json["WW_track"]
        WW_ratio_sys = ratios_json["WW_sys"]
        WZ_ratio_eff = ratios_json["WZ_eff"]
        WZ_ratio_track = ratios_json["WZ_track"]
        WZ_ratio_sys = ratios_json["WZ_sys"]

        texfile.write("\\begin{table}[h]\n")
        texfile.write("\\centering\n")
        texfile.write("\\begin{tabular}{lcccc}\n")

        texfile.write("\\hline\n Source & $\sigma_{W+}$ ($\%$) & $\sigma_{W-}$ ($\%$) & $R_{WW}$ ($\%$) & $R_{WZ}$ ($\%$) \\\\\n\\hline\n")

        texfile.write("Trigger Efficiency & {:.{prec}f} & {:.{prec}f} & {:.{prec}f} & {:.{prec}f}\\\\\n".format((Wp_xsec_err_eff**2/Wp_xsec_err_sys**2),(Wm_xsec_err_eff**2/Wm_xsec_err_sys**2),(WW_ratio_eff**2/WW_ratio_sys**2),(WZ_ratio_eff**2/WZ_ratio_sys**2),prec=4))
        texfile.write("Track Cut on $\pi/K$ Background & {:.{prec}f} & {:.{prec}f} & {:.{prec}f} & {:.{prec}f}\\\\\n".format((Wp_xsec_err_track**2/Wp_xsec_err_sys**2),(Wm_xsec_err_track**2/Wm_xsec_err_sys**2),(WW_ratio_track**2/WW_ratio_sys**2),(WZ_ratio_track**2/WZ_ratio_sys**2),prec=4))

        texfile.write("\\hline\n")
        texfile.write("\\end{tabular}\n")
        texfile.write("\\caption{\small Sources of systematic uncertainties in $W$ boson cross sections, and both cross section ratios $R_{WW}$ and $R_{WZ}$.}\n")
        texfile.write("\\label{tab: W events}\n")
        texfile.write("\\end{table}\n")


with open('results_json/Wp_back_output.json') as json_file:
    Wp_background = json.load(json_file)

with open('results_json/Wm_back_output.json') as json_file:
    Wm_background = json.load(json_file)

with open('results_json/Wp_xsec.json') as json_file:
    Wp_xsec_input = json.load(json_file)

with open('results_json/Wm_xsec.json') as json_file:
    Wm_xsec_input = json.load(json_file)

with open('results_json/Ratios.json') as json_file:
    Ratios = json.load(json_file)


current_dir = os.getcwd()
save_path = os.path.join(current_dir, 'doc/measurement_doc/results/')

Z_fraction_output(save_path, "Wp", Wp_background)
Z_fraction_output(save_path, "Wm", Wm_background)

fit_fraction_output(save_path, "Wp", Wp_background)
fit_fraction_output(save_path, "Wm", Wm_background)

event_table_output(save_path, Wp_background, Wm_background)

Wp_decay = "{W^+\\xrightarrow{}\mu^+\\nu}"
Wm_decay = "{W^-\\xrightarrow{}\mu^-\\bar{\\nu}}"
Z_decay = "{Z\\xrightarrow{}\mu^+\mu^-}"

xsec_output(save_path, "Wp", Wp_decay, Wp_xsec_input)
xsec_output(save_path, "Wm", Wm_decay, Wm_xsec_input)


# ratios
WW_ratio = Ratios["WW_ratio"]
WW_ratio_err = Ratios["WW_error"]
WW_ratio_stat = Ratios["WW_stat"]
WW_ratio_sys = Ratios["WW_sys"]
with open(save_path+'WW_ratio_output.tex','w') as texfile:
    texfile.write("\\"+"begin{equation}\n")
    texfile.write("\\frac{{\sigma_{}}}{{\sigma_{}}} = {:.{prec}f} \pm {:.{prec}f}_{{\\rm stat}} \pm {:.{prec}f}_{{\\rm sys}},\n".format(Wp_decay, Wm_decay, WW_ratio, WW_ratio_stat, WW_ratio_sys, prec=2))
    texfile.write("\\"+"end{equation}\n")

with open(save_path+'WW_value.tex','w') as texfile:
    texfile.write("${:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f}$".format(WW_ratio, WW_ratio_stat, WW_ratio_sys, prec=2))

WZ_ratio = Ratios["WZ_ratio"]
WZ_ratio_err = Ratios["WZ_error"]
WZ_ratio_stat = Ratios["WZ_stat"]
WZ_ratio_sys = Ratios["WZ_sys"]
with open(save_path+'WZ_ratio_output.tex','w') as texfile:
    texfile.write("\\"+"begin{equation}\n")
    texfile.write("\\frac{{\sigma_{}+\sigma_{}}}{{\sigma_{}}} = {:.{prec}f} \pm {:.{prec}f}_{{\\rm stat}} \pm {:.{prec}f}_{{\\rm sys}}.\n".format(Wp_decay, Wm_decay, Z_decay, WZ_ratio, WZ_ratio_stat, WZ_ratio_sys, prec=1))
    texfile.write("\\"+"end{equation}\n")

with open(save_path+'WZ_value.tex','w') as texfile:
    texfile.write("${:.{prec}f} \pm {:.{prec}f} \pm {:.{prec}f}$".format(WZ_ratio, WZ_ratio_stat, WZ_ratio_sys, prec=1))

# systematic uncertainty table
systematic_table(save_path, Wp_xsec_input, Wm_xsec_input, Ratios)

# Term 1, Week 4
Upload of work done during week 4, 26/10/2020 to 01/11/2020.

* [Main Record of Work (Week 4)](T1_W4_Doc.pdf)
* [Photos of written notes (Week 4)](T1_W4_Written_Notes.pdf)

Main Record contains lists of activities attempted each day, a reference table to the relevant page in the written notes, and a reference table for the uploaded documents. Contains notes about other files uploaded, which have been listed under the relevant date in the main record document.

Work done this week relates to Issue [#5](https://github.com/r-preston/MPhysProject2021/issues/5).

## 26/10/2020
* Monitoring Interview

## 27/10/2020
* [ZMass_Final.py](ZMass_Final.py) - More correct and efficient calculation of Z invariant mass using TLorentzVector. 
* [measurement_plot_setup_label.py](measurement_plot_setup_label.py) - Histogram plotting for mup_PT for measurement and simulation data

ZMass_Final is improved version of [Week 2 attempt](https://github.com/r-preston/MPhysProject2021/blob/master/laura-progress/T1_W2/ZMassAttempt_ROOT.py), using TLorentzVector to find invariant mass.

## 29/10/2020
* [mnt_setup_fnc.cpp](mnt_setup_fnc.cpp) - Histogram plotting for mup_PT for measurement and simulation data in C++
* [Makefile for mnt_setup_fnc.cpp](Makefile)

Decision to work in C++, translated histogram plotting in python from 27/11 to C++ code. C++ seems more intuitive for ROOT.
Introduced use of a structure for path input, and use of a function to create each histogram for measurement and simulation.

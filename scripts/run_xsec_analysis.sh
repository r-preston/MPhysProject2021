make
./plot_MC_comparison.exe
./scripts/get_luminosity.py
./scripts/measure_trigger_eff.py
./scripts/measure_xsec.py
cd doc/measurement_doc/
pdflatex measurement_report.tex
cd ../..

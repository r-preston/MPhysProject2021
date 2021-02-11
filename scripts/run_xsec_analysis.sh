make
./plot_MC_comparison.exe
./scripts/get_luminosity.py
./scripts/measure_trigger_eff.py
./scripts/measure_xsec.py

./plot_W_dist.exe
./W_background.exe
./scripts/make_W_latex.py

cd doc/measurement_doc/
pdflatex measurement_report.tex
gio open measurement_report.pdf
cd ../..

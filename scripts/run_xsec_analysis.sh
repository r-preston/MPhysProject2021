make
./plot_MC_comparison.exe
./scripts/get_luminosity.py
./scripts/measure_trigger_eff.py
./scripts/measure_xsec.py

./plot_W_dist.exe
./W_background.exe
./scripts/measure_W_xsec.py
./scripts/make_W_latex.py

./scripts/plot_xsec.py
./scripts/plot_all_xsecs.py
./scripts/plot_W_xsec.py

cd doc/measurement_doc/
pdflatex measurement_report.tex
bibtex measurement_report
pdflatex measurement_report.tex
pdflatex measurement_report.tex
gio open measurement_report.pdf
cd ../..

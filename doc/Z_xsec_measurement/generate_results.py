#!/usr/bin/env python
import os





# generate pdf analysis notes
pdflatex_run = os.system("pdflatex Z_xsec_measurement.tex")
print("pdflatex ran with exit code %d" % pdflatex_run)
bibtex_run = os.system("bibtex Z_xsec_measurement")
print("bibtex ran ran with exit code %d" % bibtex_run)
pdflatex_run = os.system("pdflatex Z_xsec_measurement.tex")
print("pdflatex ran ran with exit code %d" % pdflatex_run)
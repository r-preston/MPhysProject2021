#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True) #prevents ROOT trying to open a GUI

DATADIR='/storage/epp2/phshgg/MPhysProject2021/'

def main():

    import ROOT

    ch  = ROOT.TChain('WpIso/DecayTree')
    ch.Add( DATADIR + '{sqrts}TeV_{year}_{stripping}_{polarity}_{stream}.root'.format(sqrts='5',year='2017',stripping='32',polarity='Down',stream='EW'))

    nbins = 100
    xmin = 15.
    xmax = 60.

    hist = ROOT.TH1F('hist_name','title',nbins,xmin,xmax)

    ch.Draw('1.e-3*mu_PT>>'+hist.GetName())

    canv = ROOT.TCanvas()

    hist.Draw()

    canv.SaveAs('plot.pdf')

if __name__ == '__main__':
    main()
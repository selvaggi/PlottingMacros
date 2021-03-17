#!/usr/bin/env python


####
#python readTree.py /eos/user/s/selvaggi/heppyTrees/hhgen/mgp8_pp_vhh_lambda140_5f_hhbbbb/FCChhAnalyses.FCChh.hhgen.TreeProducer.TreeProducer_1/tree.root hhen_plots/vhh_lambda140.root


import ROOT, math, sys
from array import array
import itertools

## This example  prints basic information about the tree content ##


#________________________________________________________________________

inputFile = sys.argv[1]
outputFile = sys.argv[2]

histo_h1_pt = ROOT.TH1F('h1_pt','h1_pt',400,0,1000.)
histo_h2_pt = ROOT.TH1F('h2_pt','h2_pt',400,0,500.)
histo_hh_pt = ROOT.TH1F('hh_pt','hh_pt',400,0,1000.)
histo_hh_m = ROOT.TH1F('hh_m','hh_m',400,200,1000.)



f = ROOT.TFile.Open(inputFile)
tree=f.Get("events")
nev = tree.GetEntries()

#nev = 10
for iev in range(0,nev) :
    tree.GetEntry(iev)

    if (iev+1)%10000 == 0:
       print ' ... processed {} events ...'.format(iev+1)
       
    '''
    print ' '    
    print ' -------------- new event -----------------'
    print ' '    
    '''

  ###### loop over rec particles ######

    i = 0
    
    '''
    ## this is if these leafs were actually vectors

    print ''
    print '  -- event --'
    print ''
    for h1_pt, h2_pt, hh_pt, hh_m, weight in itertools.izip(
                                                 getattr(tree, 'h1_pt'),
                                                 getattr(tree, 'h2_pt'),
                                                 getattr(tree, 'hh_pt'),
                                                 getattr(tree, 'hh_m'),
                                                 getattr(tree, 'weight')
                                                   ):
    '''
    h1_pt   =  getattr(tree, 'h1_pt')
    h2_pt   =  getattr(tree, 'h2_pt')
    hh_pt   =  getattr(tree, 'hh_pt')
    hh_m    =  getattr(tree, 'hh_m')
    weight  =  getattr(tree, 'weight')

    histo_h1_pt.Fill(h1_pt,weight)
    histo_h2_pt.Fill(h2_pt,weight) 
    histo_hh_pt.Fill(hh_pt,weight) 
    histo_hh_m.Fill(hh_m,weight)

    #print h1_pt, h2_pt, hh_pt, hh_m, weight

# Show resulting histograms
out_root = ROOT.TFile(outputFile,"RECREATE")

histo_h1_pt.Write()
histo_h2_pt.Write()
histo_hh_pt.Write()
histo_hh_m.Write() 

import ROOT, math, sys
from array import array
import itertools
import numpy as np

#___________________________
def pairs(list):
        result = []
        for p1 in range(len(list)):
                for p2 in range(p1+1,len(list)):
                        result.append([list[p1],list[p2]])
        return result
#_____________________________________

inputFile = sys.argv[1]
outputFile = sys.argv[2]


nbinsx=10000
xmin_res=0.
xmax_res=2.


histos = dict()
histos_norm = dict()


histos_spike = dict()
histos2D_spike = dict()


vars= ['reg','sd', 'tg']
samples = ['higgs','qcd']

cat_spike = ['cat0','cat1','cat2','cat3','cat4','cat5','cat6']
var_spike = ['msd','mreg','mgen','pt']


ptbins = [(200.,100000.), (200.,300.), (300.,500.), (500.,1000.), (1000.,100000.)]
massbins = [(0.,1000.), (0.,50.), (50.,100.), (100.,150.), (150.,200.)]


decays = ['all','qq','cc','bb']


for var in vars:
    for sample in samples:
        for decay in decays:
            for ptbin in ptbins:
                for mbin in massbins:
                    histname = '{}_{}_{}_pt{}_{}_m{}_{}'.format(var,sample,decay,ptbin[0],ptbin[1],mbin[0],mbin[1])
                    histos[histname] = ROOT.TH1F("h{}".format(histname), "h{}".format(histname), nbinsx, 0. ,500.0)
                    histos_norm[histname] = ROOT.TH1F("hd{}".format(histname), "hd{}".format(histname), nbinsx, xmin_res, xmax_res)

histo_QCD_msd_mreg = ROOT.TH2F("histo_QCD_msd_mreg", "histo_QCD_msd_mreg", 100, 0, 400,  100, 0, 400)

pairings = pairs(var_spike)

for cat in cat_spike:
    for var in var_spike:
        histname = '{}_{}'.format(cat,var)
        histos_spike[histname] = ROOT.TH1F("h{}".format(histname), "h{}".format(histname), 400, 0. ,2000.0)

    for vs in pairings:
        histname = '{}_{}_{}'.format(cat,vs[0],vs[1])
        histos2D_spike[histname] = ROOT.TH2F("h{}".format(histname), "h{}".format(histname), 100, 0. ,2000.0, 100, 0. ,2000.0)


f = ROOT.TFile.Open(inputFile)
tree=f.Events

nev = tree.GetEntries()
#nev = 100000


iev = 0
for j in tree :
    iev += 1
    if (iev)%1000 == 0:
       print ' ... processed {} jets ...'.format(iev)

    if iev > nev:
        break

    jets = []

    #print j.output


    '''for i in range(ev.njets):

        jet = Jet()
        jet.pt = ev.jets_pt[i]
        jet.eta = ev.jets_eta[i]
        jet.phi = ev.jets_phi[i]
        jet.energy = ev.jets_energy[i]
    '''


    dreg_norm = -999.
    dsd_norm = -999.

    if j.orig_fj_genjet_targetmass > 0:
        dreg_norm = (j.output)/j.orig_fj_genjet_targetmass
        dsd_norm = (j.orig_fj_sdmass)/j.orig_fj_genjet_targetmass

    if j.orig_fj_genjet_targetmass < 0.:
        continue


    #if j.orig_fj_genjet_targetmass < 109 or j.orig_fj_genjet_targetmass > 141 :
    #    if j.orig_fj_pt < 200 or j.orig_fj_pt > 400 :
    #        continue


    if j.orig_fj_isQCD:
        #histo_QCD_msd_mreg.Fill(j.orig_fj_sdmass, j.output)
        histo_QCD_msd_mreg.Fill(j.orig_fj_genjet_targetmass, j.output)


    cate=''
    if j.output < 0.6988*j.orig_fj_genjet_targetmass and j.output > 0.6986*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat1'
    if j.output < 0.9316*j.orig_fj_genjet_targetmass and j.output > 0.9314*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat2'
    if j.output < 1.118*j.orig_fj_genjet_targetmass and j.output > 1.1178*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat3'
    if j.output < 1.3974*j.orig_fj_genjet_targetmass and j.output > 1.3972*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat4'
    if j.output < 1.8632*j.orig_fj_genjet_targetmass and j.output > 1.863*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat5'
    if j.output < 1.7*j.orig_fj_genjet_targetmass and j.output > 1.6*j.orig_fj_genjet_targetmass and j.orig_fj_isH:
        cate='cat6'

    #if 'cat' in cate:
    #    cate='cat0'


    val = dict()
    val['msd'] = j.orig_fj_sdmass
    val['mreg'] = j.output
    val['mgen'] = j.orig_fj_genjet_targetmass
    val['pt'] = j.orig_fj_pt

    for cat in cat_spike:
        if cat==cate:
            
            #print cat
            for var in var_spike:
                histname = '{}_{}'.format(cat,var)            
                histos_spike[histname].Fill(val[var])

            for vs in pairings:
                histname = '{}_{}_{}'.format(cat,vs[0],vs[1])
                histos2D_spike[histname].Fill(val[vs[0]],val[vs[1]])


    for var in vars:

        val = 0
        dval = 0
        
        if var == 'sd':
            val = j.orig_fj_sdmass
            dval = dsd_norm

        elif var == 'reg':
            val = j.output
            dval = dreg_norm

        elif var == 'tg':
            val = j.orig_fj_genjet_targetmass
            dval = -1


        for sample in samples:
            
            if sample == 'higgs':
                if not j.orig_fj_isH:
                    continue
            if sample == 'qcd':
                if not j.orig_fj_isQCD:
                    continue

            for decay in decays:
                
                for ptbin in ptbins:

                     pt = j.orig_fj_pt
                     
                     if pt > ptbin[0] and pt < ptbin[1]:
                     
                         for mbin in massbins:
                         
                             if j.orig_fj_genjet_targetmass > mbin[0] and j.orig_fj_genjet_targetmass < mbin[1]:

                                 histname = '{}_{}_{}_pt{}_{}_m{}_{}'.format(var,sample,decay,ptbin[0],ptbin[1],mbin[0],mbin[1])

                                 #if val < 1.1022*j.orig_fj_genjet_targetmass and val > 1.102*j.orig_fj_genjet_targetmass:
                                 #if val < *j.orig_fj_genjet_targetmass and val > 1.102*j.orig_fj_genjet_targetmass:

                                 if decay == 'all':

                                     histos[histname].Fill(val)
                                     histos_norm[histname].Fill(dval)

                                 elif decay == 'bb':
                                     if j.orig_fj_nbHadrons > 0:
                                         histos[histname].Fill(val)
                                         histos_norm[histname].Fill(dval)

                                 elif decay == 'cc':
                                     if j.orig_fj_ncHadrons > 0:
                                         histos[histname].Fill(val)
                                         histos_norm[histname].Fill(dval)

                                 elif decay == 'qq':
                                     if j.orig_fj_ncHadrons == 0 and j.orig_fj_nbHadrons == 0:
                                         histos[histname].Fill(val)
                                         histos_norm[histname].Fill(dval)


out_root = ROOT.TFile(outputFile,"RECREATE")

for var in vars:
    for sample in samples:
        for decay in decays:
            for ptbin in ptbins:
                for mbin in massbins:
                    histname = '{}_{}_{}_pt{}_{}_m{}_{}'.format(var,sample,decay,ptbin[0],ptbin[1],mbin[0],mbin[1])
                    histos[histname].Write()
                    histos_norm[histname].Write()

for cat in cat_spike:
    for var in var_spike:
        histname = '{}_{}'.format(cat,var)
        histos_spike[histname].Write()

    for vs in pairings:
        histname = '{}_{}_{}'.format(cat,vs[0],vs[1])
        histos2D_spike[histname].Write()



histo_QCD_msd_mreg.Write()

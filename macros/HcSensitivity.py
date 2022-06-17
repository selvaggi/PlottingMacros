import math, sys

rel_unc_sig = 0.30
rel_unc_ggh = 0.0
rel_unc_bbh = rel_unc_ggh
rel_unc_other = 0.0
rel_unc_gamma = 0.0


bkg_yield_unc = {
    'ggh': (29.74, rel_unc_ggh),
    'qqh': (9.54, rel_unc_other),
    'tth': (0.03, rel_unc_other),
    'vh':  (3.65, rel_unc_other),
    'bbh': (3.57, rel_unc_bbh),
    'aa':  (615., rel_unc_gamma),
    'aj':  (705., rel_unc_gamma),
}

sig_yield_unc = (5., rel_unc_sig)


lumis = [ 137,  193,  272,  383,  540,  761, 1072, 1510, 2129, 3000]

for lumi in lumis:

    scale = float(lumi)/137.

    NS = scale* sig_yield_unc[0]
    NS_stat = math.sqrt(NS)
    NS_syst = sig_yield_unc[1] * NS
    NS_syst2 = NS_syst**2

    NB = 0.
    NB_syst2 = 0.

    for proc, vals in bkg_yield_unc.iteritems():

        NB += scale* vals[0]
        NB_syst2 += (scale * vals[0] * vals[1])**2
        #print '{}:  NB = {:.2f}, stat.err  = {:.2f}, systt. err =  {:.2f}'.format(proc, scale* vals[0], math.sqrt(scale* vals[0]), scale* (vals[0] * vals[1]))

    NB_syst = math.sqrt(NB_syst2)
    NB_stat = math.sqrt(NB)

    NggH = scale* bkg_yield_unc['ggh'][0]
    NggH_stat = math.sqrt(NggH)
    NggH_syst = NggH * bkg_yield_unc['ggh'][1]

    significance = NS / math.sqrt( NS + NB + NS_syst2 + NB_syst2)
    dxsec = 1. / significance
    dcoupling = 0.5*dxsec

    if NB_syst > NB_stat:
        print 'becomes syst. dominated !!!'


    print '--------------------------------------------------------------------'
    print 'NS              = {:.2e}' .format(NS)
    print 'NS_stat         = {:.2e}' .format(NS_stat)
    print 'NS_syst         = {:.2e}' .format(NS_syst)
    print ''
    print 'NB              = {:.2e}' .format(NB)
    print 'NB_stat         = {:.2e}' .format(NB_stat)
    print 'NB_syst         = {:.2e}' .format(NB_syst)
    print ''
    print 'NggH              = {:.2e}' .format(NggH)
    print 'NggH_stat         = {:.2e}' .format(NggH_stat)
    print 'NggH_syst         = {:.2e}' .format(NggH_syst)
    print ''
    print 'lumi  ( fb-1)   = {:.3f}'.format(lumi)
    print 'significance    = {:.3f}'.format(significance)
    print 'd xsec/xsec (%) = {:.2f}'.format(dxsec)
    print 'd yc / yc (%)   = {:.2f}'.format(dcoupling)

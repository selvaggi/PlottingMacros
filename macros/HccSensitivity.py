# python HccSensitivity.py 1.00 0.00 0.00
# python HccSensitivity.py 0.70 0.10 0.10
# python HccSensitivity.py 0.80 0.025 0.025
# python HccSensitivity.py 0.90 0.10 0.10


# python HccSensitivity.py 0.90 0.05 0.10
# python HccSensitivity.py 0.80 0.02 0.03



import math, sys


eff_c = float(sys.argv[1])
eff_b = float(sys.argv[2])
eff_g = float(sys.argv[3])

N=1e06

#eff_c=0.70
#eff_b=0.10
#eff_g=0.10

#eff_c=0.80
#eff_b=0.025
#eff_g=0.025

#eff_c=0.90
#eff_b=0.10
#eff_g=0.05

#eff_c=1.00
#eff_b=0.00
#eff_g=0.00

#eff_c=1.00
#eff_b=1.00
#eff_g=1.00


br_bb=0.5809
br_cc=2.884E-02 
br_gg=8.180E-02 


N_bb= N * br_bb
N_cc= N * br_cc
N_gg= N * br_gg

N_bb_tag= N_bb * eff_b**2
N_cc_tag= N_cc * eff_c**2
N_gg_tag= N_gg * eff_g**2

N_s = N_cc_tag
N_b = N_bb_tag + N_gg_tag

significance = float(N_s) / math.sqrt(N_s + N_b)
dxsec = 1./significance
dcoupling = 0.5*dxsec

print '--  results  -- '

print 'N higgs = {:.0f}'.format(N)

print ''
print 'br cc = {:.2f}'.format(br_bb)
print 'br bb = {:.2f}'.format(br_cc)
print 'br gg = {:.2f}'.format(br_gg)
print ''

print 'eff c-tagging = {:.2f}'.format(eff_c)
print 'eff b-mistag  = {:.2f}'.format(eff_b)
print 'eff g-mistag  = {:.2f}'.format(eff_g)
print ''
print 'N cc  = {:.0f}'.format(N_cc)
print 'N bb  = {:.0f}'.format(N_bb)
print 'N gg  = {:.0f}'.format(N_gg)
print ''
print 'N cc tag = {:.0f}'.format(N_cc_tag)
print 'N bb tag = {:.0f}'.format(N_bb_tag)
print 'N gg tag = {:.0f}'.format(N_gg_tag)
print ''
print ''
print 'N s = {:.0f}'.format(N_s)
print 'N b = {:.0f}'.format(N_b)
print ''

print 'significance    = {:.1f}'.format(significance)
print 'd xsec/xsec (%) = {:.2f}'.format(dxsec*100)
print 'd yc / yc (%)   = {:.2f}'.format(dcoupling*100)


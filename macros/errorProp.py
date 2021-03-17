import math


#______________________________________________
def rel_unc(No, Ns, rel_lumi, rel_effS):
    
    rel_stat_sq = float(No)/(Ns*Ns)
    rel_lumi_sq = rel_lumi * rel_lumi
    rel_eff_sq  = rel_effS * rel_effS
    
    rel_unc = math.sqrt(rel_stat_sq + rel_lumi_sq + rel_eff_sq)
    
    return rel_unc

#______________________________________________
def rel_unc_uncorr(No, Ns, Nb, rel_lumi, rel_effS, rel_effB):
    
    rel_stat_sq = float(No)/(Ns*Ns)
    rel_lumi_sq = rel_lumi * rel_lumi
    rel_effS_sq  = rel_effS * rel_effS
    rel_effB_sq  = (rel_effB * rel_effB)*(Nb*Nb)/(Ns*Ns)

    rel_unc = math.sqrt(rel_stat_sq + rel_lumi_sq + rel_effS_sq + rel_effB_sq)

    return rel_unc

#______________________________________________
def rel_unc_corr(No, Ns, Nb, rel_lumi, rel_effS, rel_effB):
    
    rel_stat_sq = float(No)/(Ns*Ns)
    rel_lumi_sq = rel_lumi * rel_lumi
    rel_eff_sq  = (rel_effS * rel_effB)*(No*No)/(Ns*Ns)

    rel_unc = math.sqrt(rel_stat_sq + rel_lumi_sq + rel_eff_sq)

    return rel_unc




Ns = 10000
Nb = 5000

No = Ns + Nb

rel_lumi = 0.00
rel_effS = 0.02

rel_effB = 0.02

#rel_lumi = 0.0
#rel_effS = 0.0
#rel_effB = 0.0


## if no uncertainty on the background
print rel_unc(No, Ns, rel_lumi, rel_effS)

## if no uncertainty on the background
print rel_unc_uncorr(No, Ns, Nb, rel_lumi, rel_effS, rel_effB)


## if no uncertainty on the background
print rel_unc_corr(No, Ns, Nb, rel_lumi, rel_effS, rel_effB)

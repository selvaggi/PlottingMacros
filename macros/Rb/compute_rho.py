import ROOT, sys


def compute_rho(f_b, eff_b_same, eff_b_oppo):
    integral = f_b.Integral()
    if integral != 0:
        f_b.Scale(1.0 / integral)
    
    rho_b_num = 0
    rho_b_den = 0

    for i in range(f_b.GetNbinsX()):
        f_b_i = f_b.GetBinContent(i)
        eff_b_same_i = eff_b_same.GetBinContent(i)
        eff_b_oppo_i = eff_b_oppo.GetBinContent(i)
        
        rho_b_num += f_b_i * eff_b_same_i * eff_b_oppo_i
        rho_b_den += f_b_i * eff_b_same_i
    
    rho_b = rho_b_num / (rho_b_den)**2 - 1
    return rho_b


inputFile = sys.argv[1]
## using aleph definition
f = ROOT.TFile.Open(inputFile)

f_b_p = f.Get("h_jet_p")
eff_b_same_p = f.Get("eff_tagjet_same_p")
eff_b_oppo_p = f.Get("eff_tagjet_oppo_p")

rho_b_p = compute_rho(f_b_p, eff_b_same_p, eff_b_oppo_p)

print(rho_b_p)
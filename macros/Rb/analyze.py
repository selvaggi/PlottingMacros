import ROOT, math, sys
from array import array
import itertools
import numpy as np
import ctypes


# ___________________________
def pairs(list):
    result = []
    for p1 in range(len(list)):
        for p2 in range(p1 + 1, len(list)):
            result.append([list[p1], list[p2]])
    return result

# _____________________________________

inputFile = sys.argv[1]
outputFile = sys.argv[2]

f = ROOT.TFile.Open(inputFile)
tree = f.events

nev = tree.GetEntries()
# nev = 100000

h_jet_p = ROOT.TH1F("h_jet_p", "h_jet_p", 45, 0.0 ,90.0)

## aleph definition of same / oppo 
h_jet_same_p = ROOT.TH1F("h_jet_same_p", "h_jet_same_p", 45, 0.0 ,90.0)
h_jet_oppo_p = ROOT.TH1F("h_jet_oppo_p", "h_jet_oppo_p", 45, 0.0 ,90.0)
h_jet_oppotag_p = ROOT.TH1F("h_jet_oppotag_p", "h_jet_oppotag_p", 45, 0.0 ,90.0)

cut_value = 0.995

iev = 0

n_same_side =0
n_same_side_stag =0
n_same_side_dtag =0

for ev in tree:
    iev += 1
    if (iev) % 1000 == 0:
        print(" ... processed {} events ...".format(iev))

    if iev > nev:
        break
    
    ## extract two hardest bhadrons
    b_hadrons = []
    for i in range(ev.n_bhadrons):
        b_hadrons.append((i, ev.bhadron_e[i]))

    b_hadrons_indices = [index for index, energy in sorted(b_hadrons, key=lambda x: x[1], reverse=True)]
    b_hadrons_indices = b_hadrons_indices[:2]

    for i in range(ev.event_njet):
        #print(ev.jet_p[i])

        n_bhadrons_same = 0
        n_bhadrons_stagged_same = 0
        n_bhadrons_dtagged_same = 0

        h_jet_p.Fill(ev.jet_p[i])
        
        tlv_j = ROOT.TLorentzVector()
        tlv_j.SetPxPyPzE(ev.jet_px[i], ev.jet_py[i], ev.jet_pz[i], ev.jet_e[i])
        v_j = tlv_j.Vect()
        # loop over the two hardest bhadrons and find out whether their in this jet hemisphere

        jb_scalar_products = []
        for j in b_hadrons_indices:
            tlv_b = ROOT.TLorentzVector()
            tlv_b.SetPxPyPzE(ev.bhadron_px[j], ev.bhadron_py[j], ev.bhadron_pz[j], ev.bhadron_e[j])
            v_b = tlv_b.Vect()
            jb_dot = v_j.Dot(v_b)
            jb_scalar_products.append(jb_dot)
            #print(jb_dot)  
            if jb_dot > 0:
                n_bhadrons_same += 1

        if ev.recojet_isB[i] > cut_value:
            h_jet_same_p.Fill(ev.jet_p[i])

            for dotprod in jb_scalar_products:
                if dotprod > 0:
                    n_bhadrons_stagged_same += 1

            if i == 0:
                h_jet_oppo_p.Fill(ev.jet_p[1])
                if ev.recojet_isB[1] > cut_value:
                    h_jet_oppotag_p.Fill(ev.jet_p[i])
                    
                    for dotprod in jb_scalar_products:
                        if dotprod > 0:
                            n_bhadrons_dtagged_same += 1

            else:
                h_jet_oppo_p.Fill(ev.jet_p[0])
                if ev.recojet_isB[0] > cut_value:
                    h_jet_oppotag_p.Fill(ev.jet_p[i])
                    for dotprod in jb_scalar_products:
                        if dotprod > 0:
                            n_bhadrons_dtagged_same += 1

    if n_bhadrons_same == 2:
        n_same_side +=1
    if n_bhadrons_stagged_same == 2:
        n_same_side_stag +=1
    if n_bhadrons_dtagged_same == 2:
        n_same_side_dtag +=1

print("")
print(f"eff same side: {n_same_side/nev:.6f}")
print(f"eff same side (single tag): {n_same_side_stag/nev:.6f}")
print(f"eff same side (double tag): {n_bhadrons_dtagged_same/nev:.6f}")
print("")
out_root = ROOT.TFile(outputFile,"RECREATE")

h_jet_p.Write()
h_jet_same_p.Write()
h_jet_oppo_p.Write()
h_jet_oppotag_p.Write()

h_jet_p.Sumw2()
h_jet_same_p.Sumw2()
h_jet_oppo_p.Sumw2()
h_jet_oppotag_p.Sumw2()

eff_tagjet_same_p = h_jet_same_p.Clone()
eff_tagjet_same_p.SetName("eff_tagjet_same_p")
eff_tagjet_same_p.Divide(h_jet_p)
eff_tagjet_same_p.Write()

eff_doubletag_same_p = h_jet_oppotag_p.Clone()
eff_doubletag_same_p.SetName("eff_doubletag_same_p")
eff_doubletag_same_p.Divide(h_jet_p)
eff_doubletag_same_p.Write()

ed = ctypes.c_double(0)
es = ctypes.c_double(0)
#print h, h.Integral(0, h.GetNbinsX()+1)

num_s = h_jet_same_p.IntegralAndError(0, h_jet_same_p.GetNbinsX()+1, es)
num_d = h_jet_oppotag_p.IntegralAndError(0, h_jet_oppotag_p.GetNbinsX()+1, ed)
num_ed = ed.value
num_es = es.value

den_d = h_jet_p.IntegralAndError(0, h_jet_p.GetNbinsX()+1, ed)
den_s = den_d
den_ed = ed.value
den_es = den_ed

d = num_d/den_d
s = num_s/den_s
ed = d * math.sqrt(1/num_ed + 1/den_ed)
es = s * math.sqrt(1/num_es + 1/den_es)

rho_b = d/s**2 - 1.
rho_b_err = math.sqrt(ed**2 + 4*es**2/s**2)/s**2

print(d, ed, s, ed, d/s**2, d/s**2 -1)

print(f"rho_b : {rho_b:.4f} +/- {rho_b_err:.4f}")
print("")

rho_b = eff_doubletag_same_p.Clone()
rho_b.SetName("rho_b")

for i in range(rho_b.GetNbinsX()):
    d = eff_doubletag_same_p.GetBinContent(i)
    ed = eff_doubletag_same_p.GetBinError(i)
    s = eff_tagjet_same_p.GetBinContent(i)
    es = eff_tagjet_same_p.GetBinError(i)
    
    if s > 0:
        bin_rho_b = d/s**2 - 1
        bin_rho_b_err = math.sqrt(ed**2 + 4*es**2/s**2)/s**2
        #print(d, ed, s, es, d/s**2 - 1, math.sqrt(ed**2 + 4*es**2/s**2)/s**2)
        print(f"{i}, rho_b: {bin_rho_b:.4f} +/- {bin_rho_b_err:.4f}")
        rho_b.SetBinContent(i, bin_rho_b)
        rho_b.SetBinError(i, bin_rho_b_err)
    else:
        rho_b.SetBinContent(i, 0)
        rho_b.SetBinError(i, 0)

rho_b.Write()      

eff_tagjet_oppo_p = h_jet_oppo_p.Clone()
eff_tagjet_oppo_p.SetName("eff_tagjet_oppo_p")
eff_tagjet_oppo_p.Divide(h_jet_p)
eff_tagjet_oppo_p.Write()




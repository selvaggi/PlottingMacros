import ROOT, math, sys
from array import array
import itertools
import numpy as np
import ctypes
from utils import *


# _____________________________________

inputFile = sys.argv[1]
outputFile = sys.argv[2]

f = ROOT.TFile.Open(inputFile)
tree = f.events

nev = tree.GetEntries()
nev_req = 25000
if nev_req <= nev:
    nev = nev_req
    
extractSameSide = False
events_to_extract = []

vetoSameSide = False
antivetoSameSide = False

h_jet_p = ROOT.TH1F("h_jet_p", "h_jet_p", 45, 0.0, 90.0)

## aleph definition of same / oppo
h_jet_same_p = ROOT.TH1F("h_jet_same_p", "h_jet_same_p", 45, 0.0, 90.0)
h_jet_oppo_p = ROOT.TH1F("h_jet_oppo_p", "h_jet_oppo_p", 45, 0.0, 90.0)
h_jet_oppotag_p = ROOT.TH1F("h_jet_oppotag_p", "h_jet_oppotag_p", 45, 0.0, 90.0)

h_nbhadrons_per_hemisphere = ROOT.TH2F("h_nbhadrons_per_hemisphere", "h_nbhadrons_per_hemisphere", 4, -0.5, 3.5, 4, -0.5, 3.5)

iev = 0

n_same_side = 0
n_same_side_stag = 0
n_same_side_dtag = 0

n_2b_tag = 0
n_0b_tag = 0
n_2b = 0
n_0b = 0


n_presel = 0

n_stag = 0
n_dtag = 0

cut_value = 0


n_presel_nosame = 0 
n_presel_same = 0 

n_stag_same = 0
n_dtag_same = 0

n_stag_nosame = 0
n_dtag_nosame = 0

for ev in tree:
    iev += 1
    if (iev) % 10000 == 0:
        print(" ... processed {} events ...".format(iev))

    if iev > nev:
        break

    ## apply preselection

    if ev.event_njet != 2:
        continue
    if abs(math.cos(ev.jet_theta[0])) > 0.7:
        continue
    if abs(math.cos(ev.jet_theta[1])) > 0.7:
        continue

    ## veto events with 2 bhadrons in same hemispehere
    
    
    if not extractSameSide and antivetoSameSide:
        from utils import events_same_hemisphere
        if iev not in events_same_hemisphere:
            continue
    
    if not extractSameSide and vetoSameSide:
        from utils import events_same_hemisphere
        if iev in events_same_hemisphere:
            continue
    
    n_presel += 1
    

    ## extract two hardest bhadrons
    b_hadrons = []
    for i in range(ev.n_bhadrons):
        b_hadrons.append((i, ev.bhadron_e[i]))

    b_hadrons_indices = [
        index for index, energy in sorted(b_hadrons, key=lambda x: x[1], reverse=True)
    ]
    b_hadrons_indices = b_hadrons_indices[:2]

    b1_v = ROOT.TVector3(ev.bhadron_px[0], ev.bhadron_py[0], ev.bhadron_pz[0])
    b2_v = ROOT.TVector3(ev.bhadron_px[1], ev.bhadron_py[1], ev.bhadron_pz[1])
    
    
    #for j in b_hadrons_indices:
    #    print(ev.bhadron_e[j])
    
    #if len(b_hadrons_indices) != 2:
    #    continue

    ## compute information about two jets
    j1_p4 = ROOT.TLorentzVector(ev.jet_px[0], ev.jet_py[0], ev.jet_pz[0], ev.jet_e[0])
    j1_s = logtr(ev.recojet_isB[0])
    j2_p4 = ROOT.TLorentzVector(ev.jet_px[1], ev.jet_py[1], ev.jet_pz[1], ev.jet_e[1])
    j2_s = logtr(ev.recojet_isB[1])
    
    jets = [j1_p4, j2_p4]
    
    ## compute information about bhadrons jets
    b_hadrons = []
    for i in range(ev.n_bhadrons):
        b_hadrons.append(ROOT.TLorentzVector(ev.bhadron_px[i], ev.bhadron_py[i], ev.bhadron_pz[i], ev.bhadron_e[i]))   
    b_hadrons = sorted(b_hadrons, key=lambda v: v.P(), reverse=True)
    b_hadrons = b_hadrons[:2]
    
    n_bhadrons_j1, n_bhadrons_j2 = compute_nbhadrons_in_jets(j1_p4, j2_p4, b_hadrons)
    h_nbhadrons_per_hemisphere.Fill(n_bhadrons_j1, n_bhadrons_j2)
    
    h_jet_p.Fill(j1_p4.P())
    h_jet_p.Fill(j2_p4.P())

    if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
        events_same_hemisphere.append(iev)
        n_same_side += 1
        n_presel_same += 1
        
    else:
        n_presel_nosame += 1
    
        
    ## check individual eps_2b and eps_0b
    if n_bhadrons_j1 == 2:
        n_2b += 1
        if j1_s > cut_value:
            n_2b_tag += 1
            
    if n_bhadrons_j2 == 2:
        n_2b += 1
        if j2_s > cut_value:
            n_2b_tag += 1
   
    if n_bhadrons_j1 == 0:
        n_0b += 1
        if j1_s > cut_value:
            n_0b_tag += 1
    
    if n_bhadrons_j2 == 0:
        n_0b += 1
        if j2_s > cut_value:
            n_0b_tag += 1


    if j1_s > cut_value:
        n_stag += 1
        
        if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
            n_stag_same += 1            
        else:
            n_stag_nosame += 1        
        
        h_jet_same_p.Fill(j1_p4.P())        
        h_jet_oppo_p.Fill(j2_p4.P())

        if n_bhadrons_j1 == 2:
            n_same_side_stag += 1

        if j2_s > cut_value:
            h_jet_oppotag_p.Fill(j1_p4.P())
            n_dtag += 1
            
            if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
                n_dtag_same += 1            
            else:
                n_dtag_nosame += 1  
        
    if j2_s > cut_value:
        n_stag += 1
        
        if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
            n_stag_same += 1            
        else:
            n_stag_nosame += 1  
        
        h_jet_same_p.Fill(j2_p4.P())
        h_jet_oppo_p.Fill(j1_p4.P())

        if n_bhadrons_j2 == 2:
            n_same_side_stag += 1
            
        if j1_s > cut_value:
            h_jet_oppotag_p.Fill(j2_p4.P())    
            
             
     
if extractSameSide:
    print(events_same_hemisphere)


print("=================================================================")
print("")
print(f"cut value: {cut_value:.3f}")
print("")
print(f"number of analysed events: {nev}")
print(f"number of pre-sel  events: {n_presel}")
print(f"pre-sel efficiency: {100*n_presel/nev:.3f} %")
print("")



if not vetoSameSide:
    eff2 = n_2b_tag/n_2b
    eff0 = n_0b_tag/n_0b
    print(f"number of hemispheres with 2 b: {n_2b}")
    print(f"number of hemispheres with 0 b: {n_0b}")
    print(f"tagging eff when 2 bhadrons in jet: {100*eff2:.1f} %")
    print(f"tagging eff when 0 bhadrons in jet: {100*eff0:.1f} %")

print("")
print("on cleaned events")
eff_stag_nosame = n_stag_nosame / (2 * n_presel_nosame)
eff_dtag_nosame = n_dtag_nosame / (n_presel_nosame)
rho_b_nosame = eff_dtag_nosame / eff_stag_nosame**2 - 1
print("")
print(f"number of events: {n_presel_nosame}")
print(f"number of hemispheres: {2 * n_presel_nosame}")
print(f"number of single tag hemispheres: {n_stag_nosame}")
print(f"number of double tags hemispheres: {n_dtag_nosame}")
print(f"eff single-tag: {100*eff_stag_nosame:.1f} %")
print(f"eff double-tag: {100*eff_dtag_nosame:.1f} %")
print(f"rho b: {100*rho_b_nosame:.3f} %")
print("")

print("")
print("on same hemisphere events")
eff_stag_same = n_stag_same / (2 * n_presel_same)
eff_dtag_same = n_dtag_same / (n_presel_same)
rho_b_same = eff_dtag_same / eff_stag_same**2 - 1
print("")
print(f"number of events: {n_presel_same}")
print(f"number of hemispheres: {2 * n_presel_same}")
print(f"number of single tag hemispheres: {n_stag_same}")
print(f"number of double tags hemispheres: {n_dtag_same}")
print(f"eff single-tag: {100*eff_stag_same:.1f} %")
print(f"eff double-tag: {100*eff_dtag_same:.1f} %")
print(f"rho b: {100*rho_b_same:.3f} %")
print("")

print("")
print("on all events")
print("")
eff_stag = n_stag / (2 * n_presel)
eff_dtag = n_dtag / (n_presel)
rho_b = eff_dtag / eff_stag**2 - 1
print(f"number of events: {n_presel}")
print(f"number of hemispheres: {2 * n_presel}")
print(f"number of single tag hemispheres: {n_stag}")
print(f"number of double tags events: {n_dtag}")
print(f"eff single-tag: {100*eff_stag:.1f} %")
print(f"eff double-tag: {100*eff_dtag:.1f} %")
print(f"rho b: {100*rho_b:.3f} %")
print("")
print("")
print("")
compute_analytical_rho(rho_b_nosame, n_dtag_nosame, n_dtag_same, n_stag_nosame, n_stag_same, n_presel_nosame, n_presel_same)


#C = 4*n_presel*n_dtag/(n_stag**2)
#print(C)



#print(f"how often event with 2-hadron in same side: {100*n_same_side/(n_presel):.6f} %")
#print(f"eff same side (single tag): {100*n_same_side_stag/(n_stag):.6f} %")
#print(f"eff same side (double tag): {100*n_same_side_dtag/(n_dtag):.6f} %")
#print("")

out_root = ROOT.TFile(outputFile, "RECREATE")

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
# print h, h.Integral(0, h.GetNbinsX()+1)

num_s = h_jet_same_p.IntegralAndError(0, h_jet_same_p.GetNbinsX() + 1, es)
num_d = h_jet_oppotag_p.IntegralAndError(0, h_jet_oppotag_p.GetNbinsX() + 1, ed)
num_ed = ed.value
num_es = es.value

den_d = h_jet_p.IntegralAndError(0, h_jet_p.GetNbinsX() + 1, ed)
den_s = den_d
den_ed = ed.value
den_es = den_ed

d = num_d / den_d
s = num_s / den_s
ed = d * math.sqrt(1 / num_ed + 1 / den_ed)
es = s * math.sqrt(1 / num_es + 1 / den_es)

rho_b = d / s**2 - 1.0
rho_b_err = math.sqrt(ed**2 + 4 * es**2 / s**2) / s**2

"""
print(f"rho_b : {rho_b:.4f} +/- {rho_b_err:.4f}")
print("")

rho_b = eff_doubletag_same_p.Clone()
rho_b.SetName("rho_b")

for i in range(rho_b.GetNbinsX()):
    d = eff_doubletag_same_p.GetBinContent(i)
    ed = eff_doubletag_same_p.GetBinError(i)
    s = eff_tagjet_same_p.GetBinContent(i)
    es = eff_tagjet_same_p.GetBinError(i)
    p = eff_tagjet_same_p.GetBinCenter(i)

    if s > 0:
        bin_rho_b = d / s**2 - 1
        bin_rho_b_err = math.sqrt(ed**2 + 4 * es**2 / s**2) / s**2
        # print(d, ed, s, es, d/s**2 - 1, math.sqrt(ed**2 + 4*es**2/s**2)/s**2)
        print(f"p: {p:.0f}, rho_b: {bin_rho_b:.4f} +/- {bin_rho_b_err:.4f}")
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

h_nbhadrons_per_hemisphere.Write()

"""
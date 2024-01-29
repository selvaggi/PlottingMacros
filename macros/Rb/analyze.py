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


# cut_values = [-1.0, -0.5, 0, 0.5, 1]
cut_values = [-1.0, -0.5, 0]

h_jet_p = dict()

## aleph definition of same / oppo
h_jet_same_p = dict()
h_jet_oppo_p = dict()
h_jet_oppotag_p = dict()

h_nbhadrons_per_hemisphere = dict()

n_same_side = dict()
n_same_side_stag = dict()
n_same_side_dtag = dict()

n_2b_tag = dict()
n_0b_tag = dict()
n_2b = dict()
n_0b = dict()


n_presel = dict()

n_stag = dict()
n_dtag = dict()


n_presel_nosame = dict()
n_presel_same = dict()

n_stag_same = dict()
n_dtag_same = dict()

n_stag_nosame = dict()
n_dtag_nosame = dict()

eff2 = dict()
eff0 = dict()

eff_stag_nosame = dict()
eff_dtag_nosame = dict()
rho_b_nosame = dict()

eff_stag_same = dict()
eff_dtag_same = dict()
rho_b_same = dict()

eff_stag = dict()
eff_dtag = dict()
rho_b = dict()


for cut_value in cut_values:
    h_jet_p[cut_value] = ROOT.TH1F(f"h_jet_p__{cut_value:.1f}", f"h_jet_p__{cut_value:.1f}", 45, 0.0, 90.0)

    ## aleph definition of same / oppo
    h_jet_same_p[cut_value] = ROOT.TH1F(f"h_jet_same_p__{cut_value:.1f}", f"h_jet_same_p__{cut_value:.1f}", 45, 0.0, 90.0)
    h_jet_oppo_p[cut_value] = ROOT.TH1F(f"h_jet_oppo_p__{cut_value:.1f}", f"h_jet_oppo_p__{cut_value:.1f}", 45, 0.0, 90.0)
    h_jet_oppotag_p[cut_value] = ROOT.TH1F(
        f"h_jet_oppotag_p__{cut_value:.1f}", f"h_jet_oppotag_p__{cut_value:.1f}", 45, 0.0, 90.0
    )

    h_nbhadrons_per_hemisphere[cut_value] = ROOT.TH2F(
        f"h_nbhadrons_per_hemisphere__{cut_value:.1f}",
        f"h_nbhadrons_per_hemisphere__{cut_value:.1f}",
        4,
        -0.5,
        3.5,
        4,
        -0.5,
        3.5,
    )

    n_same_side[cut_value] = 0
    n_same_side_stag[cut_value] = 0
    n_same_side_dtag[cut_value] = 0

    n_2b_tag[cut_value] = 0
    n_0b_tag[cut_value] = 0
    n_2b[cut_value] = 0
    n_0b[cut_value] = 0

    n_presel[cut_value] = 0

    n_stag[cut_value] = 0
    n_dtag[cut_value] = 0

    n_presel_nosame[cut_value] = 0
    n_presel_same[cut_value] = 0

    n_stag_same[cut_value] = 0
    n_dtag_same[cut_value] = 0

    n_stag_nosame[cut_value] = 0
    n_dtag_nosame[cut_value] = 0
    
    iev = 0
    for ev in tree:
        iev += 1
        if (iev) % 100000 == 0:
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

        n_presel[cut_value] += 1

        ## extract two hardest bhadrons
        b_hadrons = []
        for i in range(ev.n_bhadrons):
            b_hadrons.append((i, ev.bhadron_e[i]))

        b_hadrons_indices = [
            index
            for index, energy in sorted(b_hadrons, key=lambda x: x[1], reverse=True)
        ]
        b_hadrons_indices = b_hadrons_indices[:2]

        b1_v = ROOT.TVector3(ev.bhadron_px[0], ev.bhadron_py[0], ev.bhadron_pz[0])
        b2_v = ROOT.TVector3(ev.bhadron_px[1], ev.bhadron_py[1], ev.bhadron_pz[1])

        # for j in b_hadrons_indices:
        #    print(ev.bhadron_e[j])

        # if len(b_hadrons_indices) != 2:
        #    continue

        ## compute information about two jets
        j1_p4 = ROOT.TLorentzVector(
            ev.jet_px[0], ev.jet_py[0], ev.jet_pz[0], ev.jet_e[0]
        )
        j1_s = logtr(ev.recojet_isB[0])
        j2_p4 = ROOT.TLorentzVector(
            ev.jet_px[1], ev.jet_py[1], ev.jet_pz[1], ev.jet_e[1]
        )
        j2_s = logtr(ev.recojet_isB[1])

        jets = [j1_p4, j2_p4]

        ## compute information about bhadrons jets
        b_hadrons = []
        for i in range(ev.n_bhadrons):
            b_hadrons.append(
                ROOT.TLorentzVector(
                    ev.bhadron_px[i],
                    ev.bhadron_py[i],
                    ev.bhadron_pz[i],
                    ev.bhadron_e[i],
                )
            )
        b_hadrons = sorted(b_hadrons, key=lambda v: v.P(), reverse=True)
        b_hadrons = b_hadrons[:2]

        n_bhadrons_j1, n_bhadrons_j2 = compute_nbhadrons_in_jets(
            j1_p4, j2_p4, b_hadrons
        )
        h_nbhadrons_per_hemisphere[cut_value].Fill(n_bhadrons_j1, n_bhadrons_j2)

        h_jet_p[cut_value].Fill(j1_p4.P())
        h_jet_p[cut_value].Fill(j2_p4.P())

        if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
            events_same_hemisphere.append(iev)
            n_same_side[cut_value] += 1
            n_presel_same[cut_value] += 1

        else:
            n_presel_nosame[cut_value] += 1

        ## check individual eps_2b and eps_0b
        if n_bhadrons_j1 == 2:
            n_2b[cut_value] += 1
            if j1_s > cut_value:
                n_2b_tag[cut_value] += 1

        if n_bhadrons_j2 == 2:
            n_2b[cut_value] += 1
            if j2_s > cut_value:
                n_2b_tag[cut_value] += 1

        if n_bhadrons_j1 == 0:
            n_0b[cut_value] += 1
            if j1_s > cut_value:
                n_0b_tag[cut_value] += 1

        if n_bhadrons_j2 == 0:
            n_0b[cut_value] += 1
            if j2_s > cut_value:
                n_0b_tag[cut_value] += 1

        if j1_s > cut_value:
            n_stag[cut_value] += 1

            if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
                n_stag_same[cut_value] += 1
            else:
                n_stag_nosame[cut_value] += 1

            h_jet_same_p[cut_value].Fill(j1_p4.P())
            h_jet_oppo_p[cut_value].Fill(j2_p4.P())

            if n_bhadrons_j1 == 2:
                n_same_side_stag[cut_value] += 1

            if j2_s > cut_value:
                h_jet_oppotag_p[cut_value].Fill(j1_p4.P())
                n_dtag[cut_value] += 1

                if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
                    n_dtag_same[cut_value] += 1
                else:
                    n_dtag_nosame[cut_value] += 1

        if j2_s > cut_value:
            n_stag[cut_value] += 1

            if n_bhadrons_j1 == 2 or n_bhadrons_j2 == 2:
                n_stag_same[cut_value] += 1
            else:
                n_stag_nosame[cut_value] += 1

            h_jet_same_p[cut_value].Fill(j2_p4.P())
            h_jet_oppo_p[cut_value].Fill(j1_p4.P())

            if n_bhadrons_j2 == 2:
                n_same_side_stag[cut_value] += 1

            if j1_s > cut_value:
                h_jet_oppotag_p[cut_value].Fill(j2_p4.P())

    if extractSameSide:
        print(events_same_hemisphere)

    print("=================================================================")
    print("")
    print(f"cut value: {cut_value:.3f}")
    print("")
    print(f"number of analysed events: {nev}")
    print(f"number of pre-sel  events: {n_presel[cut_value]}")
    print(f"pre-sel efficiency: {100*n_presel[cut_value]/nev:.3f} %")
    print("")

    eff2[cut_value] = n_2b_tag[cut_value] / n_2b[cut_value]
    eff0[cut_value] = n_0b_tag[cut_value] / n_0b[cut_value]
    print(f"number of hemispheres with 2 b: {n_2b[cut_value]}")
    print(f"number of hemispheres with 0 b: {n_0b[cut_value]}")
    print(f"tagging eff when 2 bhadrons in jet: {100*eff2[cut_value]:.1f} %")
    print(f"tagging eff when 0 bhadrons in jet: {100*eff0[cut_value]:.1f} %")

    print("")
    print("on cleaned events")
    eff_stag_nosame[cut_value] = n_stag_nosame[cut_value] / (
        2 * n_presel_nosame[cut_value]
    )
    eff_dtag_nosame[cut_value] = n_dtag_nosame[cut_value] / (n_presel_nosame[cut_value])
    rho_b_nosame[cut_value] = (
        eff_dtag_nosame[cut_value] / eff_stag_nosame[cut_value] ** 2 - 1
    )
    print("")
    print(f"number of events: {n_presel_nosame[cut_value]}")
    print(f"number of hemispheres: {2 * n_presel_nosame[cut_value]}")
    print(f"number of single tag hemispheres: {n_stag_nosame[cut_value]}")
    print(f"number of double tags hemispheres: {n_dtag_nosame[cut_value]}")
    print(f"eff single-tag: {100*eff_stag_nosame[cut_value]:.1f} %")
    print(f"eff double-tag: {100*eff_dtag_nosame[cut_value]:.1f} %")
    print(f"rho b: {100*rho_b_nosame[cut_value]:.3f} %")
    print("")

    print("")
    print("on same hemisphere events")
    eff_stag_same[cut_value] = n_stag_same[cut_value] / (2 * n_presel_same[cut_value])
    eff_dtag_same[cut_value] = n_dtag_same[cut_value] / (n_presel_same[cut_value])
    rho_b_same[cut_value] = eff_dtag_same[cut_value] / eff_stag_same[cut_value] ** 2 - 1
    print("")
    print(f"number of events: {n_presel_same[cut_value]}")
    print(f"number of hemispheres: {2 * n_presel_same[cut_value]}")
    print(f"number of single tag hemispheres: {n_stag_same[cut_value]}")
    print(f"number of double tags hemispheres: {n_dtag_same[cut_value]}")
    print(f"eff single-tag: {100*eff_stag_same[cut_value]:.1f} %")
    print(f"eff double-tag: {100*eff_dtag_same[cut_value]:.1f} %")
    print(f"rho b: {100*rho_b_same[cut_value]:.3f} %")
    print("")

    print("")
    print("on all events")
    print("")
    eff_stag[cut_value] = n_stag[cut_value] / (2 * n_presel[cut_value])
    eff_dtag[cut_value] = n_dtag[cut_value] / (n_presel[cut_value])
    rho_b[cut_value] = eff_dtag[cut_value] / eff_stag[cut_value] ** 2 - 1
    print(f"number of events: {n_presel[cut_value]}")
    print(f"number of hemispheres: {2 * n_presel[cut_value]}")
    print(f"number of single tag hemispheres: {n_stag[cut_value]}")
    print(f"number of double tags events: {n_dtag[cut_value]}")
    print(f"eff single-tag: {100*eff_stag[cut_value]:.1f} %")
    print(f"eff double-tag: {100*eff_dtag[cut_value]:.1f} %")
    print(f"rho b: {100*rho_b[cut_value]:.3f} %")
    print("")
    print("")
    print("")
    compute_analytical_rho(
        rho_b_nosame[cut_value],
        n_dtag_nosame[cut_value],
        n_dtag_same[cut_value],
        n_stag_nosame[cut_value],
        n_stag_same[cut_value],
        n_presel_nosame[cut_value],
        n_presel_same[cut_value],
    )


# C = 4*n_presel*n_dtag/(n_stag**2)
# print(C)


# print(f"how often event with 2-hadron in same side: {100*n_same_side/(n_presel):.6f} %")
# print(f"eff same side (single tag): {100*n_same_side_stag/(n_stag):.6f} %")
# print(f"eff same side (double tag): {100*n_same_side_dtag/(n_dtag):.6f} %")
# print("")


out_root = ROOT.TFile(outputFile, "RECREATE")
"""
h_jet_p[cut_value].Write()
h_jet_same_p[cut_value].Write()
h_jet_oppo_p[cut_value].Write()
h_jet_oppotag_p[cut_value].Write()

h_jet_p[cut_value].Sumw2()
h_jet_same_p[cut_value].Sumw2()
h_jet_oppo_p[cut_value].Sumw2()
h_jet_oppotag_p[cut_value].Sumw2()

eff_tagjet_same_p[cut_value] = h_jet_same_p[cut_value].Clone()
eff_tagjet_same_p[cut_value].SetName("eff_tagjet_same_p")
eff_tagjet_same_p[cut_value].Divide(h_jet_p[cut_value])
eff_tagjet_same_p[cut_value].Write()

eff_doubletag_same_p[cut_value] = h_jet_oppotag_p[cut_value].Clone()
eff_doubletag_same_p[cut_value].SetName("eff_doubletag_same_p")
eff_doubletag_same_p[cut_value].Divide(h_jet_p[cut_value])
eff_doubletag_same_p[cut_value].Write()

ed = ctypes.c_double(0)
es = ctypes.c_double(0)
# print h, h.Integral(0, h.GetNbinsX()+1)

num_s = h_jet_same_p[cut_value].IntegralAndError(0, h_jet_same_p[cut_value].GetNbinsX() + 1, es)
num_d = h_jet_oppotag_p[cut_value].IntegralAndError(0, h_jet_oppotag_p[cut_value].GetNbinsX() + 1, ed)
num_ed = ed.value
num_es = es.value

den_d = h_jet_p[cut_value].IntegralAndError(0, h_jet_p[cut_value].GetNbinsX() + 1, ed)
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

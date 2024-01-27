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

debug = True
if debug:
    nev = 1000
    display_events = [808]


h_jet_p = ROOT.TH1F("h_jet_p", "h_jet_p", 45, 0.0, 90.0)

## aleph definition of same / oppo
h_jet_same_p = ROOT.TH1F("h_jet_same_p", "h_jet_same_p", 45, 0.0, 90.0)
h_jet_oppo_p = ROOT.TH1F("h_jet_oppo_p", "h_jet_oppo_p", 45, 0.0, 90.0)
h_jet_oppotag_p = ROOT.TH1F("h_jet_oppotag_p", "h_jet_oppotag_p", 45, 0.0, 90.0)

cut_value = 0.0

iev = 0

n_same_side = 0
n_same_side_stag = 0
n_same_side_dtag = 0


n_presel = 0

n_stag = 0
n_dtag = 0


for ev in tree:
    iev += 1
    if (iev) % 1000 == 0:
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

    if debug:
        if iev in [808]:
            create_event_display(ev)

    ## veto events with 2 bhadrons in same hemispehere
    from utils import events_same_hemisphere

    # events_same_hemisphere = []
    # events_same_hemisphere = [808]
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

    for i in range(ev.event_njet):
        # print(ev.jet_p[i])

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
            tlv_b.SetPxPyPzE(
                ev.bhadron_px[j], ev.bhadron_py[j], ev.bhadron_pz[j], ev.bhadron_e[j]
            )
            v_b = tlv_b.Vect()
            jb_dot = v_j.Dot(v_b)
            jb_scalar_products.append(jb_dot)
            # print(jb_dot)
            if jb_dot > 0:
                n_bhadrons_same += 1

        if logtr(ev.recojet_isB[i]) > cut_value:
            n_stag += 1
            h_jet_same_p.Fill(ev.jet_p[i])

            for dotprod in jb_scalar_products:
                if dotprod > 0:
                    n_bhadrons_stagged_same += 1

            if i == 0:
                h_jet_oppo_p.Fill(ev.jet_p[1])
                if logtr(ev.recojet_isB[1]) > cut_value:
                    h_jet_oppotag_p.Fill(ev.jet_p[i])
                    n_dtag += 1
                    for dotprod in jb_scalar_products:
                        if dotprod > 0:
                            n_bhadrons_dtagged_same += 1

            else:
                h_jet_oppo_p.Fill(ev.jet_p[0])
                if logtr(ev.recojet_isB[0]) > cut_value:
                    h_jet_oppotag_p.Fill(ev.jet_p[i])
                    n_dtag += 1
                    for dotprod in jb_scalar_products:
                        if dotprod > 0:
                            n_bhadrons_dtagged_same += 1

    if n_bhadrons_same == 2:
        events_same_hemisphere.append(iev)
        n_same_side += 1
    if n_bhadrons_stagged_same == 2:
        n_same_side_stag += 1
    if n_bhadrons_dtagged_same == 2:
        n_same_side_dtag += 1


print("")
print(f"number of analysed events: {nev}")
print(f"number of pre-sel  events: {n_presel}")
print(f"pre-sel efficiency: {100*n_presel/nev:.3f} %")
print("")

print(f"cut score: {cut_value:.3f}")
print("")

eff_stag = n_stag / (2 * n_presel)
eff_dtag = n_dtag / (2 * n_presel)
rho_b = eff_dtag / eff_stag**2 - 1

print(f"eff single-tag: {100*eff_stag:.1f} %")
print(f"eff double-tag: {100*eff_dtag:.1f} %")
print(f"rho b: {100*rho_b:.1f} %")

print("")

print(f"eff same side: {100*n_same_side/(n_presel):.6f} %")
print(f"eff same side (single tag): {100*n_same_side_stag/(n_stag):.6f} %")
print(f"eff same side (double tag): {100*n_same_side_dtag/(n_dtag):.6f} %")
print("")
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

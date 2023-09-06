import ROOT, math, sys
from ROOT import TLorentzVector
from array import array
import itertools
import numpy as np
from collections import Counter

hmass_S1 = ROOT.TH1F("hmass_S1", "hmass_S1", 100, 0.0, 200.0)
hmass_S2 = ROOT.TH1F("hmass_S2", "hmass_S2", 100, 0.0, 200.0)

hmass_S1_ideal = ROOT.TH1F("hmass_S1_ideal", "hmass_S1_ideal", 100, 0.0, 200.0)
hmass_S2_ideal = ROOT.TH1F("hmass_S2_ideal", "hmass_S2_ideal", 100, 0.0, 200.0)

hmass_S1_fjbest = ROOT.TH1F("hmass_S1_fjbest", "hmass_S1_fjbest", 100, 0.0, 200.0)
hmass_S2_fjbest = ROOT.TH1F("hmass_S2_fjbest", "hmass_S2_fjbest", 100, 0.0, 200.0)

hmass_S1_fjcomb = ROOT.TH1F("hmass_S1_fjcomb", "hmass_S1_fjcomb", 100, 0.0, 200.0)
hmass_S2_fjcomb = ROOT.TH1F("hmass_S2_fjcomb", "hmass_S2_fjcomb", 100, 0.0, 200.0)


hmass2_S1 = ROOT.TH1F("hmass2_S1", "hmass2_S1", 100, 0.0, 200.0)
hmass2_S2 = ROOT.TH1F("hmass2_S2", "hmass2_S2", 100, 0.0, 200.0)

hdp_pf = ROOT.TH1F("hdp_pf", "hdp_pf", 100, 0.0, 0.1)
hde_pf = ROOT.TH1F("hde_pf", "hde_pf", 100, 0.0, 0.1)
hdr_pf = ROOT.TH1F("hdr_pf", "hdr_pf", 100, 0.0, 0.1)

hdp_rg = ROOT.TH1F("hdp_rg", "hdp_rg", 100, 0.0, 0.1)
hde_rg = ROOT.TH1F("hde_rg", "hde_rg", 100, 0.0, 0.1)
hdr_rg = ROOT.TH1F("hdr_rg", "hdr_rg", 100, 0.0, 0.1)


def count_and_expose_duplicates(lst):
    counter = Counter(lst)
    return {item: count for item, count in counter.items() if count > 1}


inputFile = (
    "/eos/experiment/fcc/ee/generation/DelphesStandalone/ZZssss_v1/tree/tree_22.root"
)

inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletFlatMass_ZH_v1/tree/tree_22.root"

inputFile = "/afs/cern.ch/work/s/selvaggi/private/Delphes/test.root"
#inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/tree/tree_1.root"
#inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/tree4/tree_20.root"

f = ROOT.TFile.Open(inputFile)
tree = f.tree

nev = tree.GetEntries()

nev = 100

for i, ev in enumerate(tree):

    if i % 1000 == 0:
        print(" ... processed {} events ...".format(i))

    if i > nev:
        break

    p4_S1 = TLorentzVector()
    p4_S2 = TLorentzVector()
    p4_S1_rg = TLorentzVector()
    p4_S2_rg = TLorentzVector()
    p4_S1_g = TLorentzVector()
    p4_S2_g = TLorentzVector()

    px1 = 0
    py1 = 0
    pz1 = 0
    e1 = 0
    px2 = 0
    py2 = 0
    pz2 = 0
    e2 = 0

    print("---- new event -----", i + 1)

    # if len(ev.gencand_matchid) != len(set(ev.gencand_matchid)):
    #    print("found genduplicates")

    # for j in range(ev.n_gencand):
    #    print(j, ev.gencand_matchid[j], ev.gencand_e[j], ev.gencand_pid[j])

    # print(count_and_expose_duplicates(ev.gencand_matchid))
    # print("")
    for j in range(ev.n_pfcand):
        if ev.pfcand_isS1[j]:
            p4_S1 += TLorentzVector(
                ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]
            )
            px1 += ev.pfcand_px[j]
            py1 += ev.pfcand_py[j]
            pz1 += ev.pfcand_pz[j]
            e1 += ev.pfcand_e[j]

        elif ev.pfcand_isS2[j]:
            p4_S2 += TLorentzVector(
                ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]
            )

            px2 += ev.pfcand_px[j]
            py2 += ev.pfcand_py[j]
            pz2 += ev.pfcand_pz[j]
            e2 += ev.pfcand_e[j]



    for j in range(ev.n_recogen):
        if ev.recogen_isS1[j]:
            p4_S1_rg += TLorentzVector(
                ev.recogen_px[j], ev.recogen_py[j], ev.recogen_pz[j], ev.recogen_e[j]
            )

        elif ev.recogen_isS2[j]:
            p4_S2_rg += TLorentzVector(
                ev.recogen_px[j], ev.recogen_py[j], ev.recogen_pz[j], ev.recogen_e[j]
            )

    for j in range(ev.n_gencand):
        if ev.gencand_isS1[j]:
            p4_S1_g += TLorentzVector(
                ev.gencand_px[j], ev.gencand_py[j], ev.gencand_pz[j], ev.gencand_e[j]
            )

        elif ev.gencand_isS2[j]:
            p4_S2_g += TLorentzVector(
                ev.gencand_px[j], ev.gencand_py[j], ev.gencand_pz[j], ev.gencand_e[j]
            )

    # print(j, ev.pfcand_matchid[j], ev.pfcand_e[j], ev.pfcand_pid[j])

    # if len(ev.pfcand_matchid) != len(set(ev.pfcand_matchid)):
    #    print("found pfduplicates")

    print("")

    print(
        "gen mass 1: {:.2f}, recogen mass 1: {:.2f}, pf mass 1: {:.2f}".format(
            p4_S1_g.M(), p4_S1_rg.M(), p4_S1.M()
        )
    )
    print(
        "gen mass 2: {:.2f}, recogen mass 2: {:.2f}, pf mass 2: {:.2f}".format(
            p4_S2_g.M(), p4_S2_rg.M(), p4_S2.M()
        )
    )
    for j in range(ev.n_gencand):
        # if len(ev.recogen_matchid) != len(set(ev.recogen_matchid)):
        #    print("found recogenduplicates")

        # for j in range(ev.n_recogen):
        #    print(j, ev.recogen_matchid[j], ev.recogen_e[j], ev.recogen_pid[j])

        # print(count_and_expose_duplicates(ev.recogen_matchid))

        print(
            "N: {}, PID: {}, E: {:.2f}, P: {:.2f}, Theta: {:.2f}, Phi: {:.2f}, M: {:.2f}, X: {:.2f}, Y: {:.2f}, Z: {:.2f}, S1: {}, S2: {}, ID: {},  ".format(
                j,
                ev.gencand_pid[j],
                ev.gencand_e[j],
                ev.gencand_p[j],
                ev.gencand_ptheta[j],
                ev.gencand_pphi[j],
                ev.gencand_mass[j],
                ev.gencand_vx[j],
                ev.gencand_vy[j],
                ev.gencand_vz[j],
                ev.gencand_isS1[j],
                ev.gencand_isS2[j],
                ev.gencand_matchid[j],
            )
        )

        for k in range(ev.n_recogen):
            if ev.recogen_matchid[k] == ev.gencand_matchid[j]:
                delta_p = abs(ev.gencand_p[j] - ev.recogen_p[k]) / ev.gencand_p[j]
                delta_e = abs(ev.gencand_e[j] - ev.recogen_e[k]) / ev.gencand_e[j]
                delta_r = math.sqrt(
                    (ev.gencand_ptheta[j] - ev.recogen_ptheta[k]) ** 2
                    + (ev.gencand_pphi[j] - ev.recogen_pphi[k]) ** 2
                )
                hdp_rg.Fill(delta_p)
                hde_rg.Fill(delta_e)
                hdr_rg.Fill(delta_r)
                
                print(
                    "  recogen PID: {}, E: {:.2f}, P: {:.2f}, Theta: {:.2f}, Phi: {:.2f}, M: {:.2f}, X: {:.2f}, Y: {:.2f}, Z: {:.2f}, S1: {}, S2: {}, dp: {:.3f}, de: {:.3f}, dr: {:.3f}".format(
                        ev.recogen_pid[k],
                        ev.recogen_e[k],
                        ev.recogen_p[k],
                        ev.recogen_ptheta[k],
                        ev.recogen_pphi[k],
                        ev.recogen_mass[k],
                        ev.recogen_vx[k],
                        ev.recogen_vy[k],
                        ev.recogen_vz[k],
                        ev.recogen_isS1[k],
                        ev.recogen_isS2[k],
                        delta_p,
                        delta_e,
                        delta_r,
                    )
                )
        for k in range(ev.n_pfcand):
            if ev.pfcand_matchid[k] == ev.gencand_matchid[j]:
                delta_p = abs(ev.gencand_p[j] - ev.pfcand_p[k]) / ev.gencand_p[j]
                delta_e = abs(ev.gencand_e[j] - ev.pfcand_e[k]) / ev.gencand_e[j]
                delta_r = math.sqrt(
                    (ev.gencand_ptheta[j] - ev.pfcand_ptheta[k]) ** 2
                    + (ev.gencand_pphi[j] - ev.pfcand_pphi[k]) ** 2
                )
                hdp_pf.Fill(delta_p)
                hde_pf.Fill(delta_e)
                hdr_pf.Fill(delta_r)
               
                print(
                    "  pfcand PID: {}, E: {:.2f}, P: {:.2f}, Theta: {:.2f}, Phi: {:.2f}, M: {:.2f}, X: {:.2f}, Y: {:.2f}, Z: {:.2f}, S1: {}, S2: {}, dp: {:.3f}, de: {:.3f}, dr: {:.3f}".format(
                        ev.pfcand_pid[k],
                        ev.pfcand_e[k],
                        ev.pfcand_p[k],
                        ev.pfcand_ptheta[k],
                        ev.pfcand_pphi[k],
                        ev.pfcand_mass[k],
                        ev.pfcand_vx[k],
                        ev.pfcand_vy[k],
                        ev.pfcand_vz[k],
                        ev.pfcand_isS1[k],
                        ev.pfcand_isS2[k],
                        delta_p,
                        delta_e,
                        delta_r,
                    )
                )
        print("")
    mass1 = math.sqrt(e1**2 - px1**2 - py1**2 - pz1**2)
    mass2 = math.sqrt(e2**2 - px2**2 - py2**2 - pz2**2)

    hmass_S1.Fill(p4_S1.M())
    hmass_S2.Fill(p4_S2.M())

    hmass2_S1.Fill(mass1)
    hmass2_S2.Fill(mass2)


out_root = ROOT.TFile("out.root", "RECREATE")

hmass_S1.Write()
hmass_S2.Write()

hmass2_S1.Write()
hmass2_S2.Write()

hdp_pf.Write()
hde_pf.Write()
hdr_pf.Write()

hdp_rg.Write()
hde_rg.Write()
hdr_rg.Write()


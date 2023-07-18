import ROOT, math, sys
from ROOT import TLorentzVector
from array import array
import itertools
import numpy as np


hmass_S1 = ROOT.TH1F("hmass_S1", "hmass_S1", 100, 0.0, 200.0)
hmass_S2 = ROOT.TH1F("hmass_S2", "hmass_S2", 100, 0.0, 200.0)

hmass2_S1 = ROOT.TH1F("hmass2_S1", "hmass2_S1", 100, 0.0, 200.0)
hmass2_S2 = ROOT.TH1F("hmass2_S2", "hmass2_S2", 100, 0.0, 200.0)


inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ZZssss_v1/tree/tree_22.root"

inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletFlatMass_ZH_v1/tree/tree_22.root"

inputFile = "/afs/cern.ch/work/s/selvaggi/private/Delphes/test.root"


f = ROOT.TFile.Open(inputFile)
tree = f.tree

nev = tree.GetEntries()

nev = 1000

for i, ev in enumerate(tree):

    if i % 1000 == 0:
        print(" ... processed {} events ...".format(i))

    if i > nev:
        break

    p4_S1 = TLorentzVector()
    p4_S2 = TLorentzVector()

    px1 = 0
    py1 = 0
    pz1 = 0
    e1 = 0
    px2 = 0
    py2 = 0
    pz2 = 0
    e2 = 0

    for j in range(ev.n_pfcand):
        if ev.pfcand_isS1[j]:
            p4_S1 += TLorentzVector(ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j])
            px1 += ev.pfcand_px[j]
            py1 += ev.pfcand_py[j]
            pz1 += ev.pfcand_pz[j]
            e1 += ev.pfcand_e[j]

        elif ev.pfcand_isS2[j]:
            p4_S2 += TLorentzVector(ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j])

            px2 += ev.pfcand_px[j]
            py2 += ev.pfcand_py[j]
            pz2 += ev.pfcand_pz[j]
            e2 += ev.pfcand_e[j]

    mass1 = math.sqrt(e1 ** 2 - px1 ** 2 - py1 ** 2 - pz1 ** 2)
    mass2 = math.sqrt(e2 ** 2 - px2 ** 2 - py2 ** 2 - pz2 ** 2)

    hmass_S1.Fill(p4_S1.M())
    hmass_S2.Fill(p4_S2.M())

    hmass2_S1.Fill(mass1)
    hmass2_S2.Fill(mass2)


out_root = ROOT.TFile("out.root", "RECREATE")

hmass_S1.Write()
hmass_S2.Write()

hmass2_S1.Write()
hmass2_S2.Write()

import ROOT, math, sys
from ROOT import TLorentzVector
from array import array
import itertools
import numpy as np


hmass_S1 = ROOT.TH1F("hmass_S1", "hmass_S1", 100, 0.0, 200.0)
hmass_S2 = ROOT.TH1F("hmass_S2", "hmass_S2", 100, 0.0, 200.0)

hmass2_S1 = ROOT.TH1F("hmass2_S1", "hmass2_S1", 100, 0.0, 200.0)
hmass2_S2 = ROOT.TH1F("hmass2_S2", "hmass2_S2", 100, 0.0, 200.0)

hbinary_loss = ROOT.TH1F("hbinary_loss", "hbinary_loss", 100, 0.0, 1.0)
henergy_loss = ROOT.TH1F("henergy_loss", "henergy_loss", 100, 0.0, 1.0)
hmass_loss = ROOT.TH1F("hmass_loss", "hmass_loss", 100, 0.0, 1.0)

h2_be = ROOT.TH2F("h2_be", "h2_be", 100, 0.0, 1.0, 100, 0.0, 1.0)
h2_bm = ROOT.TH2F("h2_bm", "h2_bm", 100, 0.0, 1.0, 100, 0.0, 1.0)
h2_em = ROOT.TH2F("h2_em", "h2_em", 100, 0.0, 1.0, 100, 0.0, 1.0)

inputFile = "tree_98.root"

f = ROOT.TFile.Open(inputFile)
tree = f.tree

nev = tree.GetEntries()

nev = 10000

for i, ev in enumerate(tree):

    if i % 100 == 0:
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

    jet1 = []
    jet2 = []
    jet3 = []
    jet4 = []

    s1_truth = []
    s2_truth = []
    none_truth = []

    for j in range(ev.n_pfcand):
        if ev.pfcand_isS1[j]:
            p4_S1 += TLorentzVector(ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j])
            px1 += ev.pfcand_px[j]
            py1 += ev.pfcand_py[j]
            pz1 += ev.pfcand_pz[j]
            e1 += ev.pfcand_e[j]
            s1_truth.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))

        elif ev.pfcand_isS2[j]:
            p4_S2 += TLorentzVector(ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j])

            px2 += ev.pfcand_px[j]
            py2 += ev.pfcand_py[j]
            pz2 += ev.pfcand_pz[j]
            e2 += ev.pfcand_e[j]
            s2_truth.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))

        else:
            none_truth.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))

        if ev.pfcand_jetnumber[j] == 1:
            jet1.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))
        elif ev.pfcand_jetnumber[j] == 2:
            jet2.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))
        elif ev.pfcand_jetnumber[j] == 3:
            jet3.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))
        elif ev.pfcand_jetnumber[j] == 4:
            jet4.append((ev.pfcand_px[j], ev.pfcand_py[j], ev.pfcand_pz[j], ev.pfcand_e[j]))

    def energy_loss(s1_reco, s2_reco, s1_truth, s2_truth):

        def singlet_loss(s_reco, s_truth): 
            delta_e = 0
            etot = 0
            for rcand in s_reco:
                etot += rcand[3]
                if rcand not in s_truth:
                    delta_e += rcand[3]
            for tcand in s_truth:
                etot += rcand[3]
                if tcand not in s_reco:
                    delta_e += tcand[3]
        
            return delta_e/etot

        #print("11", singlet_loss(s1_reco, s1_truth))
        #print("22", singlet_loss(s2_reco, s2_truth))
        #print("12", singlet_loss(s1_reco, s2_truth))
        #print("21", singlet_loss(s2_reco, s1_truth))

        return min(singlet_loss(s1_reco, s1_truth), singlet_loss(s1_reco, s1_truth), singlet_loss(s1_reco, s2_truth), singlet_loss(s2_reco, s1_truth))

    def binary_loss(s1_reco, s2_reco, s1_truth, s2_truth):

        def singlet_loss(s_reco, s_truth): 
            delta_n = 0
            ntot = 0
            for rcand in s_reco:
                ntot += 1
                if rcand not in s_truth:
                    delta_n += 1
            for tcand in s_truth:
                ntot += 1
                if tcand not in s_reco:
                    delta_n += 1
        
            return delta_n/ntot

        #print("11", singlet_loss(s1_reco, s1_truth))
        #print("22", singlet_loss(s2_reco, s2_truth))
        #print("12", singlet_loss(s1_reco, s2_truth))
        #print("21", singlet_loss(s2_reco, s1_truth))

        return min(singlet_loss(s1_reco, s1_truth), singlet_loss(s1_reco, s1_truth), singlet_loss(s1_reco, s2_truth), singlet_loss(s2_reco, s1_truth))


    energy_loss_1234 = energy_loss((jet1+jet2), (jet3+jet4), s1_truth, s2_truth)
    energy_loss_1324 = energy_loss((jet1+jet3), (jet2+jet4), s1_truth, s2_truth)
    energy_loss_1423 = energy_loss((jet1+jet4), (jet2+jet3), s1_truth, s2_truth)

    binary_loss_1234 = binary_loss((jet1+jet2), (jet3+jet4), s1_truth, s2_truth)
    binary_loss_1324 = binary_loss((jet1+jet3), (jet2+jet4), s1_truth, s2_truth)
    binary_loss_1423 = binary_loss((jet1+jet4), (jet2+jet3), s1_truth, s2_truth)

    def mass(cands):

        px = 0.
        py = 0.
        pz = 0.
        e = 0.
        for cand in cands:
            px += cand[0]
            py += cand[1]
            pz += cand[2]
            e += cand[3]

        #print(e, px, py, pz, math.sqrt(e ** 2 - px ** 2 - py ** 2 - pz ** 2))        
        return math.sqrt(e ** 2 - px ** 2 - py ** 2 - pz ** 2)
   
    #print(len(jet1), len(jet2), len(jet1+jet2))
    mass_12 = mass(jet1+jet2)
    mass_13 = mass(jet1+jet3)
    mass_14 = mass(jet1+jet4)
    mass_23 = mass(jet2+jet3)
    mass_24 = mass(jet2+jet4)
    mass_34 = mass(jet3+jet4)
    mass1_truth = mass(s1_truth)
    mass2_truth = mass(s2_truth)
    
    def mass_loss(m1_reco, m1_truth, m2_reco, m2_truth):
        mloss = abs(m1_reco - m1_truth)/m1_truth + abs(m2_reco - m2_truth)/m2_truth
        #print(m1_reco, m1_truth, m2_reco, m2_truth, mloss)
        return mloss

    mass_loss_1234 = mass_loss(mass_12, mass1_truth, mass_34, mass2_truth)
    mass_loss_1324 = mass_loss(mass_13, mass1_truth, mass_24, mass2_truth)
    mass_loss_1423 = mass_loss(mass_14, mass1_truth, mass_23, mass2_truth)

    min_energy_loss = min(energy_loss_1234, energy_loss_1324, energy_loss_1423)
    min_binary_loss = min(binary_loss_1234, binary_loss_1324, binary_loss_1423)
    min_mass_loss = min(mass_loss_1234, mass_loss_1324, mass_loss_1423)

    #print("loss 12,34, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1234, binary_loss_1234, mass_loss_1234))
    #print("loss 12,34, M12: {:.4f}, M34: {:.4f}".format(mass_12,mass_34))
    #print("loss 13,24, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1324, binary_loss_1324, mass_loss_1324)) 
    #print("loss 13,24, M13: {:.4f}, M24: {:.4f}".format(mass_13,mass_24))
    #print("loss 14,23, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1423, binary_loss_1423, mass_loss_1423))
    #print("loss 14,24, M14: {:.4f}, M23: {:.4f}".format(mass_14,mass_23))
    #print("min_loss", min_energy_loss, min_binary_loss, min_mass_loss)

    mass1 = math.sqrt(e1 ** 2 - px1 ** 2 - py1 ** 2 - pz1 ** 2)
    mass2 = math.sqrt(e2 ** 2 - px2 ** 2 - py2 ** 2 - pz2 ** 2)

    henergy_loss.Fill(min_energy_loss)
    hmass_loss.Fill(min_mass_loss)
    hbinary_loss.Fill(min_binary_loss)

    h2_be.Fill(min_binary_loss,min_energy_loss)
    h2_bm.Fill(min_binary_loss,min_mass_loss)
    h2_em.Fill(min_energy_loss,min_mass_loss)

    hmass_S1.Fill(p4_S1.M())
    hmass_S2.Fill(p4_S2.M())

    hmass2_S1.Fill(mass1)
    hmass2_S2.Fill(mass2)


out_root = ROOT.TFile("out.root", "RECREATE")

hmass_S1.Write()
hmass_S2.Write()

hmass2_S1.Write()
hmass2_S2.Write()

henergy_loss.Write()
hmass_loss.Write()
hbinary_loss.Write()

h2_be.Write()
h2_bm.Write()
h2_em.Write()

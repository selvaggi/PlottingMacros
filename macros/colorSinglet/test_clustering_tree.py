import ROOT, math, sys
from ROOT import TLorentzVector
from array import array
import itertools
import numpy as np


hmass_S1 = ROOT.TH1F("hmass_S1", "hmass_S1", 400, 0.0, 200.0)
hmass_S2 = ROOT.TH1F("hmass_S2", "hmass_S2", 400, 0.0, 200.0)

hmass2_S1 = ROOT.TH1F("hmass2_S1", "hmass2_S1", 400, 0.0, 200.0)
hmass2_S2 = ROOT.TH1F("hmass2_S2", "hmass2_S2", 400, 0.0, 200.0)

hbinary_loss = ROOT.TH1F("hbinary_loss", "hbinary_loss", 100, 0.0, 1.0)
henergy_loss = ROOT.TH1F("henergy_loss", "henergy_loss", 100, 0.0, 1.0)
hmass_loss = ROOT.TH1F("hmass_loss", "hmass_loss", 100, 0.0, 1.0)

h2_be = ROOT.TH2F("h2_be", "h2_be", 100, 0.0, 1.0, 100, 0.0, 1.0)
h2_bm = ROOT.TH2F("h2_bm", "h2_bm", 100, 0.0, 1.0, 100, 0.0, 1.0)
h2_em = ROOT.TH2F("h2_em", "h2_em", 100, 0.0, 1.0, 100, 0.0, 1.0)

hmass_S1_ideal = ROOT.TH1F("hmass_S1_ideal", "hmass_S1_ideal", 400, 0.0, 200.0)
hmass_S2_ideal = ROOT.TH1F("hmass_S2_ideal", "hmass_S2_ideal", 400, 0.0, 200.0)

hmass_S1_fjbestmass = ROOT.TH1F(
    "hmass_S1_fjbestmass", "hmass_S1_fjbestmass", 400, 0.0, 200.0
)
hmass_S2_fjbestmass = ROOT.TH1F(
    "hmass_S2_fjbestmass", "hmass_S2_fjbestmass", 400, 0.0, 200.0
)

hmass_S1_fjbestenergy = ROOT.TH1F(
    "hmass_S1_fjbestenergy", "hmass_S1_fjbestenergy", 400, 0.0, 200.0
)
hmass_S2_fjbestenergy = ROOT.TH1F(
    "hmass_S2_fjbestenergy", "hmass_S2_fjbestenergy", 400, 0.0, 200.0
)

hmass_S1_fjbestbinary = ROOT.TH1F(
    "hmass_S1_fjbestbinary", "hmass_S1_fjbestbinary", 400, 0.0, 200.0
)
hmass_S2_fjbestbinary = ROOT.TH1F(
    "hmass_S2_fjbestbinary", "hmass_S2_fjbestbinary", 400, 0.0, 200.0
)


hmass_S1_fjcombz = ROOT.TH1F("hmass_S1_fjcombz", "hmass_S1_fjcombz", 400, 0.0, 200.0)
hmass_S2_fjcombz = ROOT.TH1F("hmass_S2_fjcombz", "hmass_S2_fjcombz", 400, 0.0, 200.0)

hmass_S1_fjcombzh = ROOT.TH1F("hmass_S1_fjcombzh", "hmass_S1_fjcombzh", 400, 0.0, 200.0)
hmass_S2_fjcombzh = ROOT.TH1F("hmass_S2_fjcombzh", "hmass_S2_fjcombzh", 400, 0.0, 200.0)

inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/tree2/tree_20.root"
inputFile = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/tree3/tree_58.root"

inputFile = sys.argv[1]
outputFile = sys.argv[2]

f = ROOT.TFile.Open(inputFile)
tree = f.tree

nev = tree.GetEntries()

# nev = 1000

collection = "pfcand"


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

    var_ncands = "n_{}".format(collection)
    var_px = "{}_px".format(collection)
    var_py = "{}_py".format(collection)
    var_pz = "{}_pz".format(collection)
    var_e = "{}_e".format(collection)
    var_isS1 = "{}_isS1".format(collection)
    var_isS2 = "{}_isS2".format(collection)
    var_isNone = "{}_isNone".format(collection)
    var_jetnumber = "{}_jetnumber".format(collection)

    for j in range(getattr(ev, var_ncands)):
        if getattr(ev, var_isS1)[j]:
            p4_S1 += TLorentzVector(
                getattr(ev, var_px)[j],
                getattr(ev, var_py)[j],
                getattr(ev, var_pz)[j],
                getattr(ev, var_e)[j],
            )
            s1_truth.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )

        elif getattr(ev, var_isS2)[j]:
            p4_S2 += TLorentzVector(
                getattr(ev, var_px)[j],
                getattr(ev, var_py)[j],
                getattr(ev, var_pz)[j],
                getattr(ev, var_e)[j],
            )
            s2_truth.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )

        else:
            none_truth.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )

        if getattr(ev, var_jetnumber)[j] == 1:
            jet1.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )
        elif getattr(ev, var_jetnumber)[j] == 2:
            jet2.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )
        elif getattr(ev, var_jetnumber)[j] == 3:
            jet3.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )
        elif getattr(ev, var_jetnumber)[j] == 4:
            jet4.append(
                (
                    getattr(ev, var_px)[j],
                    getattr(ev, var_py)[j],
                    getattr(ev, var_pz)[j],
                    getattr(ev, var_e)[j],
                )
            )

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

            return delta_e / etot

        # print("11", singlet_loss(s1_reco, s1_truth))
        # print("22", singlet_loss(s2_reco, s2_truth))
        # print("12", singlet_loss(s1_reco, s2_truth))
        # print("21", singlet_loss(s2_reco, s1_truth))

        return min(
            singlet_loss(s1_reco, s1_truth),
            singlet_loss(s1_reco, s1_truth),
            singlet_loss(s1_reco, s2_truth),
            singlet_loss(s2_reco, s1_truth),
        )

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

            return delta_n / ntot

        # print("11", singlet_loss(s1_reco, s1_truth))
        # print("22", singlet_loss(s2_reco, s2_truth))
        # print("12", singlet_loss(s1_reco, s2_truth))
        # print("21", singlet_loss(s2_reco, s1_truth))

        return min(
            singlet_loss(s1_reco, s1_truth),
            singlet_loss(s1_reco, s1_truth),
            singlet_loss(s1_reco, s2_truth),
            singlet_loss(s2_reco, s1_truth),
        )

    energy_loss_1234 = energy_loss((jet1 + jet2), (jet3 + jet4), s1_truth, s2_truth)
    energy_loss_1324 = energy_loss((jet1 + jet3), (jet2 + jet4), s1_truth, s2_truth)
    energy_loss_1423 = energy_loss((jet1 + jet4), (jet2 + jet3), s1_truth, s2_truth)

    binary_loss_1234 = binary_loss((jet1 + jet2), (jet3 + jet4), s1_truth, s2_truth)
    binary_loss_1324 = binary_loss((jet1 + jet3), (jet2 + jet4), s1_truth, s2_truth)
    binary_loss_1423 = binary_loss((jet1 + jet4), (jet2 + jet3), s1_truth, s2_truth)

    def mass(cands):

        px = 0.0
        py = 0.0
        pz = 0.0
        e = 0.0
        for cand in cands:
            px += cand[0]
            py += cand[1]
            pz += cand[2]
            e += cand[3]

        # print(e, px, py, pz, math.sqrt(e ** 2 - px ** 2 - py ** 2 - pz ** 2))
        return math.sqrt(e**2 - px**2 - py**2 - pz**2)

    # print(len(jet1), len(jet2), len(jet1+jet2))
    mass_12 = mass(jet1 + jet2)
    mass_13 = mass(jet1 + jet3)
    mass_14 = mass(jet1 + jet4)
    mass_23 = mass(jet2 + jet3)
    mass_24 = mass(jet2 + jet4)
    mass_34 = mass(jet3 + jet4)

    m1 = mass(s1_truth)
    m2 = mass(s2_truth)
    
    if m1 > m2:
        mass1_truth = m1
        mass2_truth = m2
    else:
        mass1_truth = m2
        mass2_truth = m1
       
        
    print(mass1_truth, mass2_truth)

    masses = [mass_12, mass_13, mass_14, mass_23, mass_24, mass_34]
    pair1 = (mass_12, mass_34)
    pair2 = (mass_13, mass_24)
    pair3 = (mass_14, mass_23)
    pair4 = (mass_34, mass_12)
    pair5 = (mass_24, mass_13)
    pair6 = (mass_23, mass_14)

    pair1_sorted = sorted(pair1)
    pair2_sorted = sorted(pair2)
    pair3_sorted = sorted(pair3)

    masses_sorted = sorted(masses, key=lambda x: abs(x - 91.2))

    def chisq(pair, m1, sigma1, m2, sigma2):
        return ((pair[0] - m1)/ sigma1)**2 + ((pair[1] - m2)/ sigma2)**2
    
    pairs = [pair1, pair2, pair3, pair4, pair5, pair6]
    
    chisqs = dict()
    
    ## params ZHssss
    tgt_m1 = 91.2
    tgt_m2 = 125
    tgt_sig1 = 2.8
    tgt_sig2 = 1.5
   
    ## params ZHjjjj
    tgt_m1 = 91.2
    tgt_m2 = 125
    tgt_sig1 = 3.8
    tgt_sig2 = 5.8
  
    ## params vvWWjjjj
    tgt_m1 = 40
    tgt_m2 = 80
    tgt_sig1 = 30
    tgt_sig2 = 2.5
 
  
    for pair in pairs:
        chisqs[pair] = chisq(pair, tgt_m1, tgt_sig1, tgt_m2, tgt_sig2)
    
    best_zh_pair = min(chisqs, key=chisqs.get)
    
    
    mass_s1_fjcomb = -1
    mass_s2_fjcomb = -1

    if masses_sorted[0] == pair1_sorted[0]:
        mass_s2_fjcomb = pair1_sorted[0]
        mass_s1_fjcomb = pair1_sorted[1]

    elif masses_sorted[0] == pair2_sorted[0]:
        mass_s2_fjcomb = pair2_sorted[0]
        mass_s1_fjcomb = pair2_sorted[1]

    else:
        mass_s2_fjcomb = pair3_sorted[0]
        mass_s1_fjcomb = pair3_sorted[1]

    def mass_loss(m1_reco, m1_truth, m2_reco, m2_truth):
        #print(m1_reco, m1_truth, m2_reco, m2_truth)
        mloss = abs(m1_reco - m1_truth) / m1_truth + abs(m2_reco - m2_truth) / m2_truth
        return mloss

    """
    mass_loss_1234 = mass_loss(mass_12, mass1_truth, mass_34, mass2_truth)
    mass_loss_1324 = mass_loss(mass_13, mass1_truth, mass_24, mass2_truth)
    mass_loss_1423 = mass_loss(mass_14, mass1_truth, mass_23, mass2_truth)

    min_energy_loss = min(energy_loss_1234, energy_loss_1324, energy_loss_1423)
    min_binary_loss = min(binary_loss_1234, binary_loss_1324, binary_loss_1423)
    min_mass_loss = min(mass_loss_1234, mass_loss_1324, mass_loss_1423)

    mass_s1_fjbestmass = -1
    mass_s2_fjbestmass = -1
    mass_s1_fjbestenergy = -1
    mass_s2_fjbestenergy = -1
    mass_s1_fjbestbinary = -1
    mass_s2_fjbestbinary = -1

    if min_mass_loss == mass_loss_1234:
        mass_s1_fjbestmass = mass_12
        mass_s2_fjbestmass = mass_34
    elif min_mass_loss == mass_loss_1324:
        mass_s1_fjbestmass = mass_13
        mass_s2_fjbestmass = mass_24
    else:
        mass_s1_fjbestmass = mass_14
        mass_s2_fjbestmass = mass_23

    if min_energy_loss == energy_loss_1234:
        mass_s1_fjbestenergy = mass_12
        mass_s2_fjbestenergy = mass_34
    elif min_energy_loss == energy_loss_1324:
        mass_s1_fjbestenergy = mass_13
        mass_s2_fjbestenergy = mass_24
    else:
        mass_s1_fjbestenergy = mass_14
        mass_s2_fjbestenergy = mass_23

    if min_binary_loss == binary_loss_1234:
        mass_s1_fjbestbinary = mass_12
        mass_s2_fjbestbinary = mass_34
    elif min_binary_loss == binary_loss_1324:
        mass_s1_fjbestbinary = mass_13
        mass_s2_fjbestbinary = mass_24
    else:
        mass_s1_fjbestbinary = mass_14
        mass_s2_fjbestbinary = mass_23

    # print("loss 12,34, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1234, binary_loss_1234, mass_loss_1234))
    # print("loss 12,34, M12: {:.4f}, M34: {:.4f}".format(mass_12,mass_34))
    # print("loss 13,24, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1324, binary_loss_1324, mass_loss_1324))
    # print("loss 13,24, M13: {:.4f}, M24: {:.4f}".format(mass_13,mass_24))
    # print("loss 14,23, EL: {:.4f}, BL: {:.4f}, ML: {:.4f}".format(energy_loss_1423, binary_loss_1423, mass_loss_1423))
    # print("loss 14,24, M14: {:.4f}, M23: {:.4f}".format(mass_14,mass_23))
    # print("min_loss", min_energy_loss, min_binary_loss, min_mass_loss)
    
    henergy_loss.Fill(min_energy_loss)
    hmass_loss.Fill(min_mass_loss)
    hbinary_loss.Fill(min_binary_loss)

    h2_be.Fill(min_binary_loss, min_energy_loss)
    h2_bm.Fill(min_binary_loss, min_mass_loss)
    h2_em.Fill(min_energy_loss, min_mass_loss)

    hmass_S1.Fill(p4_S1.M())
    hmass_S2.Fill(p4_S2.M())

    hmass_S1_ideal.Fill(p4_S1.M())
    hmass_S2_ideal.Fill(p4_S2.M())

    hmass_S1_fjbestmass.Fill(mass_s1_fjbestmass)
    hmass_S2_fjbestmass.Fill(mass_s2_fjbestmass)

    hmass_S1_fjbestenergy.Fill(mass_s1_fjbestenergy)
    hmass_S2_fjbestenergy.Fill(mass_s2_fjbestenergy)

    hmass_S1_fjbestbinary.Fill(mass_s1_fjbestbinary)
    hmass_S2_fjbestbinary.Fill(mass_s2_fjbestbinary)

    hmass_S1_fjcombz.Fill(mass_s1_fjcomb)
    hmass_S2_fjcombz.Fill(mass_s2_fjcomb)
    """
    #hmass_S1_ideal.Fill(p4_S1.M())
    #hmass_S2_ideal.Fill(p4_S2.M())
    hmass_S1_ideal.Fill(mass1_truth)
    hmass_S2_ideal.Fill(mass2_truth)
  
    hmass_S1_fjcombzh.Fill(best_zh_pair[1])
    hmass_S2_fjcombzh.Fill(best_zh_pair[0])
  
    

out_root = ROOT.TFile(outputFile, "RECREATE")

hmass_S1.Write()
hmass_S2.Write()

henergy_loss.Write()
hmass_loss.Write()
hbinary_loss.Write()

h2_be.Write()
h2_bm.Write()
h2_em.Write()

hmass_S1_ideal.Write()
hmass_S2_ideal.Write()

hmass_S1_fjbestmass.Write()
hmass_S2_fjbestmass.Write()
hmass_S1_fjbestenergy.Write()
hmass_S2_fjbestenergy.Write()
hmass_S1_fjbestbinary.Write()
hmass_S2_fjbestbinary.Write()

hmass_S1_fjcombz.Write()
hmass_S2_fjcombz.Write()
hmass_S1_fjcombzh.Write()
hmass_S2_fjcombzh.Write()

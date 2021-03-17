import ROOT, math
from ROOT import TF1, TCanvas, TLegend, TH1F, TRandom3



try:
  input = raw_input
except:
  pass


nev = 10000


eA = 1.0
eB = 1.0

deA = 0.02*eA
deB = 0.02*eB

corrFactor = 0.5

heA =TH1F("heA","heA",100,0.0,2.0)
heB =TH1F("heB","heB",100,0.0,2.0)

heR =TH1F("heR","heR",100,0.5,1.5)

r = TRandom3()

for iev in xrange(nev):

    deltaA = r.Gaus(0,deA)
    deltaB = r.Gaus(0,deB)

    genA = eA+deltaA

    # uncorrelated case
    #genB = eB+deltaB

    # correlated case
    genB = eB+corrFactor*deltaA

    print eA, deltaA, genA

    heA.Fill(genA)
    heB.Fill(genB)
    heR.Fill(genA/genB)


out_root = ROOT.TFile("out.root","RECREATE")


heA.Write()
heB.Write()
heR.Write()


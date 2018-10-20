import ROOT, math
from ROOT import TF1, TCanvas, TLegend, TH1F, TRandom3



try:
  input = raw_input
except:
  pass


nev = 100000
m0 = 10.
reso = 0.03 # in %

hmass1 =TH1F("mass1","mass1",100,9.5,10.5)
hmass2 =TH1F("mass2","mass2",100,9.5,10.5)
hmass3 =TH1F("mass3","mass3",100,9.5,10.5)

r = TRandom3()

absreso = reso*m0

for iev in xrange(nev):
    m1 = r.Gaus(m0,reso)
    hmass1.Fill(m1)

    m2 =  r.Gaus(m1,reso*math.sqrt(15))
    hmass2.Fill(m2)

    m3 =  r.Gaus(m2,reso)
    hmass3.Fill(m3)


hmass1.SetLineColor(ROOT.kRed)
#hmass1.Draw()

hmass2.SetLineColor(ROOT.kBlue)
hmass2.Draw("")

hmass3.SetLineColor(ROOT.kGreen +2)
#hmass3.Draw("same")

input("Press Enter to continue...")


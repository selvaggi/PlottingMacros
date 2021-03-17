import ROOT, math
import numpy as np
from ROOT import TF1, TCanvas, TLegend, TH1F, TRandom3, THStack

delta=0.01
m0 = 125.*(1.+delta)
m_min=50.
m_max=200.


sigma = 0.10 # in %
Ns0= 100
Nb0perGeV=100000


nev = int( (m_max-m_min)*Nb0perGeV )

reso = m0*sigma # in %

hmassSig = TH1F("massSig","massSig", 100, 50., 200.)
hmassBkg = TH1F("massBkg","massBkg", 100, 50., 200.)

r = TRandom3()

absreso = reso*m0

for iev in xrange(nev):
    m = r.Gaus(m0,reso)
    
    weight=float(Ns0)/nev
    hmassSig.Fill(m, weight)
    hmassBkg.Fill(r.Uniform(50.,250))


# define stacked histo
hStack = ROOT.THStack("hstack","")

hmassBkg.SetLineWidth(0)
hmassBkg.SetFillColor(ROOT.kAzure+1)

hmassSig.SetLineWidth(0)
hmassSig.SetFillColor(ROOT.kRed)

hStack.Add(hmassBkg)
hStack.Add(hmassSig)

#hStack.Draw("hist")
#input("Press Enter to continue...")


gr = ROOT.TGraph()
gr.SetLineColor(ROOT.kBlue)
gr.SetLineWidth(3)
gr.SetMarkerSize(0.)
gr.SetMarkerColor(ROOT.kBlue)


## perform signficance scan

i=0
#for alpha in np.arange(0., 5.1, 0.1):
for alpha in np.arange(2., 2.1, 0.2):


    ma = m0 - alpha*reso
    mb = m0 + alpha*reso    
    
    
    bin_ma = hmassBkg.GetXaxis().FindBin(ma)
    bin_mb = hmassBkg.GetXaxis().FindBin(mb)
    
    
    ns = hmassSig.Integral(bin_ma,bin_mb)
    nb = hmassBkg.Integral(bin_ma,bin_mb)

    significance = ns/math.sqrt(ns+nb)

    #print alpha, ma, mb, ns, nb, significance
    print i, alpha , significance
    gr.SetPoint(i, alpha , significance)
    i+=1

    
gr.Draw()

input("Press Enter to continue...")

    

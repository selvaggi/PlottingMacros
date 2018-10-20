import ROOT
from ROOT import TFile, TRatioPlot, TCanvas, gPad, TLegend

try:
  input = raw_input
except:
  pass


ROOT.gStyle.SetOptStat(0)

hfile = TFile('/afs/cern.ch/work/s/selvaggi/public/out.root')
hfile = TFile('/eos/experiment/fcc/hh/generation/DelphesStandalone/QCD_Pt2000/histosQCD/out/histosQCD.root')

h0 = hfile.Get('hCumReco')
h1 = hfile.Get('hCumRecoUp')
h2 = hfile.Get('hCumRecoDown')

scale = 156/h0.GetBinContent(1)

h0.Scale(scale)
h1.Scale(scale)
h2.Scale(scale)

h0.SetLineColor(ROOT.kBlack)
h1.SetLineColor(ROOT.kBlue)
h2.SetLineColor(ROOT.kRed)

h0.SetLineWidth(2)
h1.SetLineWidth(2)
h2.SetLineWidth(2)

minx = 2000.
maxx = 5000.
miny = 1.
maxy = 100.

minratio=0.8
maxratio=1.2

h1.SetTitle("")
h1.GetXaxis().SetTitle("p_{T} [GeV]")
h1.GetYaxis().SetTitle("#sigma (p_{T}) > p_{T}^{min}) (pb)")

h1.GetXaxis().SetRangeUser(minx,maxx)

h1.SetMinimum(miny)
#h1.SetMaximum(maxy)

c1 = TCanvas("c1", "ratio 1")
c1.Clear()

rp1 = TRatioPlot(h1, h0)
rp1.Draw()
rp1.SetSplitFraction(0.5)

rp1.GetLowerRefGraph().SetMinimum(minratio)
rp1.GetLowerRefGraph().SetMaximum(maxratio)

rp1.GetLowerRefGraph().SetLineColor(ROOT.kBlue)
rp1.GetLowerRefGraph().SetMarkerColor(ROOT.kBlue)
rp1.GetLowerRefGraph().SetLineWidth(2)



rp1.GetUpperPad().cd()

h2.Draw("same hist")
h1.Draw("same hist")
h0.Draw("same hist")

gPad.SetLogy()

legend = TLegend(0.63,0.65,0.88,0.85)
legend.SetFillColor(0)
#legend.SetFillStyle(0)
legend.SetLineColor(0)
legend.SetShadowColor(10)
#legend.SetTextSize(0.030)

legend.AddEntry( h0,"no JES","l")
legend.AddEntry( h1,"JES up (2%)","l")
legend.AddEntry( h2,"JES down (2%)","l")

legend.Draw()

c2 = TCanvas("c2", "ratio 2")
c2.Clear()

rp2 = TRatioPlot(h2,h0)
rp2.Draw()
g2 = rp2.GetLowerRefGraph()

g2.SetLineColor(ROOT.kRed)
g2.SetMarkerColor(ROOT.kRed)
g2.SetLineWidth(2)

c1.cd()

rp1.GetLowerPad().cd()
g2.Draw("same")

c1.Update()
c1.Print("jes_dijet.pdf")


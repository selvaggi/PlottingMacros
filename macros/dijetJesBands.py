import ROOT
from ROOT import TFile, TRatioPlot, TCanvas, gPad, TLegend
import numpy as np
import math
from array import array

try:
  input = raw_input
except:
  pass


def fillTH1errors(h,hup,hdown):
   for i in xrange(0,h.GetNbinsX()):

      ptcen = h.GetXaxis().GetBinCenter(i)
      err = 0.5*(hup.GetBinContent(i) - hdown.GetBinContent(i))

      print ptcen, hup.GetBinContent(i), h.GetBinContent(i), hdown.GetBinContent(i), err, err/h.GetBinContent(i)
      h.SetBinError(i, err)
      print h.GetBinContent(i), h.GetBinError(i)


def redGraph(h,g):
    for i in xrange(g.GetN()):
	g.SetPoint(i,h.GetBinCenter(i),1.)
	g.SetPointError(i, h.GetBinWidth(i)/2., h.GetBinWidth(i)/2., h.GetBinError(i)/h.GetBinContent(i), h.GetBinError(i)/h.GetBinContent(i))
	print 'graph: ', g.GetX()[i], g.GetY()[i], g.GetErrorY(i)



ROOT.gStyle.SetOptStat(0)

hfile = TFile('/afs/cern.ch/work/s/selvaggi/public/out.root')
hfile = TFile('/eos/experiment/fcc/hh/generation/DelphesStandalone/QCD_Pt4000/histosQCD/out/histosQCD.root')

h0 = hfile.Get('hCumReco')
h0up = hfile.Get('hCumRecoUp10')
h0down = hfile.Get('hCumRecoDown10')

h1 = hfile.Get('hCumReco').Clone()
h1up = hfile.Get('hCumRecoUp05')
h1down = hfile.Get('hCumRecoDown05')


h2 = hfile.Get('hCumReco').Clone()
h2up = hfile.Get('hCumRecoUp02')
h2down = hfile.Get('hCumRecoDown02')


fillTH1errors(h0,h0up,h0down)
fillTH1errors(h1,h1up,h1down)
fillTH1errors(h2,h2up,h2down)


scale0 = 1/h0.GetBinContent(1)
scale1 = 1/h1.GetBinContent(1)
scale2 = 1/h2.GetBinContent(1)

h0.Scale(scale0)
h0up.Scale(scale0)
h0down.Scale(scale0)


h1.Scale(scale1)
h1up.Scale(scale1)
h1down.Scale(scale1)

h2.Scale(scale2)
h2up.Scale(scale2)
h2down.Scale(scale2)

h0.SetLineColor(ROOT.kBlue-10)
h0up.SetLineColor(ROOT.kBlue-10)
h0down.SetLineColor(ROOT.kBlue-10)

h1.SetLineColor(ROOT.kBlue-7)
h1up.SetLineColor(ROOT.kBlue-7)
h1down.SetLineColor(ROOT.kBlue-7)

h2.SetLineColor(ROOT.kBlue)
h2up.SetLineColor(ROOT.kBlue)
h2down.SetLineColor(ROOT.kBlue)


h0.SetLineWidth(1)
h0up.SetLineWidth(1)
h0down.SetLineWidth(1)

h1.SetLineWidth(1)
h1up.SetLineWidth(1)
h1down.SetLineWidth(1)


h2.SetLineWidth(1)
h2up.SetLineWidth(1)
h2down.SetLineWidth(1)


minx = 5.
maxx = 20.
#miny = 1.
#maxy = 100.

minratio=0.85
maxratio=1.15

c1 = TCanvas("c1", "ratio 1", 800, 800)
c1.Clear()

rp1 = TRatioPlot(h1,h1)

rp1.Draw()
g1 = rp1.GetLowerRefGraph()
g1.SetLineColor(ROOT.kBlue-7)
g1.SetFillColor(ROOT.kBlue-7)
#g1.SetFillColorAlpha(ROOT.,0.2)

g1.SetLineWidth(2)

c2 = TCanvas("c2", "ratio 2")
c2.Clear()

rp2 = TRatioPlot(h2,h2)
rp2.Draw()
g2 = rp2.GetLowerRefGraph()
g2.SetLineColor(ROOT.kBlue)
g2.SetFillColor(ROOT.kBlue)
#g2.SetFillColorAlpha(ROOT.,0.5)
g2.SetLineWidth(2)


h0.SetTitle("")
h0.GetXaxis().SetTitle("p_{T}^{min} [TeV]")
h0.GetYaxis().SetTitle("#sigma (p_{T}) > p_{T}^{min}) (pb)")

h0.GetYaxis().SetTitleOffset(1.23)

h0.GetXaxis().SetRangeUser(minx,maxx)

c0 = TCanvas("c0", "ratio 0")
c0.Clear()

rp0 = TRatioPlot(h0, h0)
rp0.Draw()


# set split fraction by hand
sf = 0.5
fInsetWidth = 0.0025
pm = fInsetWidth
width = gPad.GetWNDC()
height = gPad.GetHNDC()
f = height/width
rp0.GetUpperPad().SetPad(pm*f, sf, 1.-pm*f, 1.-pm)
rp0.GetLowerPad().SetPad(pm*f, pm, 1.-pm*f, sf)

rp0.GetUpperPad().cd()

gPad.SetLogy()

h0.Draw("e same")
h1.Draw("e same")
h2.Draw("e same")

legend = TLegend(0.60,0.60,0.88,0.85)
legend.SetFillColor(0)
#legend.SetFillStyle(0)
legend.SetLineColor(0)
legend.SetShadowColor(10)
#legend.SetTextSize(0.030)

rp0.GetLowerPad().cd()


g0 = rp0.GetLowerRefGraph()
g0.SetMinimum(minratio)
g0.SetMaximum(maxratio)
g0.SetLineColor(ROOT.kBlue-10)
g0.SetFillColor(ROOT.kBlue-10)

redGraph(h0,g0)
redGraph(h1,g1)
redGraph(h2,g2)


g0.Draw("e3")
g1.Draw("same e3")
g2.Draw("same e3")

g0.GetYaxis().SetNdivisions(101)
g0.GetYaxis().SetTitle("#Delta #sigma / #sigma")

rp0.GetLowerPad().Update()
rp0.GetLowerPad().SetGridy()

ll =[]

rangek = xrange(-3,4,1)
for k in rangek:
   l = 1.00 + float(k)*0.05
   ll.append(l)



lines = array( 'd',  ll)
print lines
rp0.GetLowerPad().Update()
rp0.SetGridlines(lines,len(xrange(-3,4,1)))

rp0.GetUpperPad().cd()

legend.AddEntry( h0,"JES #pm 1%","l")
legend.AddEntry( h1,"JES #pm 0.5%","l")
legend.AddEntry( h2,"JES #pm 0.2% ","l")
legend.Draw()



c0.Update()
c0.Print("jes_dijet.pdf")

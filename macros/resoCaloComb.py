import ROOT
from ROOT import TF1, TCanvas, TLegend, TH1F

try:
  input = raw_input
except:
  pass

#________________________________________________________________

xmin = 3.
xmax = 150.
ymin = 0.
ymax = 100.

# actual plotting
c = TCanvas("c","c",600,600)
c.SetTicks(1,1)
c.SetLeftMargin(0.14)
c.SetRightMargin(0.08)
c.SetGridx()
c.SetGridy()
ROOT.gStyle.SetOptStat(0000000)    

f = TF1("f","0.25*sqrt(2500./x^2 + 5./x + 1.)",xmin,xmax)

h_eg =TH1F("h_eg","",100,xmin,xmax)
h_mu =TH1F("h_mu","",100,xmin,xmax)

h_eg_cons =TH1F("h_eg_cons","",100,xmin,xmax)
h_mu_cons =TH1F("h_mu_cons","",100,xmin,xmax)

h_eg.Add(f, 1.8)
h_mu.Add(f, 1.0)

h_eg_cons.Add(f, 4.0)
h_mu_cons.Add(f, 2.2)

h_eg.GetXaxis().SetTitle("p_{T} [GeV]")
h_eg.GetYaxis().SetTitle("#delta_{#varepsilon}/#varepsilon (%)")
h_eg.GetYaxis().SetTitleOffset(1.95)
h_eg.GetXaxis().SetTitleOffset(1.40)
#h_eg.GetXaxis().SetRangeUser(3.,100.)

h_eg.SetMaximum(ymax)
h_eg.SetMinimum(ymin)

h_eg.SetLineWidth(4)
h_mu.SetLineWidth(4)

h_eg.SetLineColor(ROOT.kOrange+6)
h_mu.SetLineColor(ROOT.kGreen+2)

h_eg.Draw('l')
h_mu.Draw('lsame')

h_eg_cons.SetLineWidth(4)
h_mu_cons.SetLineWidth(4)

h_eg_cons.SetLineStyle(7)
h_mu_cons.SetLineStyle(7)

h_eg_cons.SetLineColor(ROOT.kOrange+10)
h_mu_cons.SetLineColor(ROOT.kGreen+3)

h_eg_cons.Draw('lsame')
h_mu_cons.Draw('lsame')


# draw legend
legend = TLegend(0.63,0.65,0.88,0.85)
legend.SetFillColor(0)
#legend.SetFillStyle(0)
legend.SetLineColor(0)
legend.SetShadowColor(10)
legend.SetTextSize(0.030)
legend.SetTextFont(42)

legend.AddEntry( h_eg,"e, #gamma (optim.)","l")
legend.AddEntry( h_eg_cons,"e, #gamma (cons.)","l")
legend.AddEntry(h_mu,"#mu (optim.)","l")
legend.AddEntry(h_mu_cons,"#mu (cons.)","l")

legend.Draw()

input("Press Enter to continue...")


c.Print('effunc.pdf', 'pdf')

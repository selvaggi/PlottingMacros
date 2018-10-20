import ROOT, math
from ROOT import TF1, TCanvas, TLegend, TH1F, TRandom3



try:
  input = raw_input
except:
  pass


nev = 100000


energy = 100

# EM fraction
mean_fem = 0.5
sigma_fem = 0.00001

# pi0 response
mean_rpi0 = 0.8
sigma_rpi0 = 0.025


# non-pi0 response
mean_rhad = 0.4
sigma_rhad = 0.15

h_fem =TH1F("h_fem","h_fem",100,0.0,1.0)

h_rpi0 =TH1F("h_rpi0","h_rpi0",200,0.0,200.0)
h_rhad =TH1F("h_rhad","h_rhad",200,0.0,200.0)

h_r =TH1F("h_r","h_r",200,0.0,200.0)

r = TRandom3()

for iev in xrange(nev):

    fem = r.Landau(mean_fem,sigma_fem)
    
    Epi0 = r.Gaus(fem*energy*mean_rpi0, fem*energy*sigma_rpi0)
    Ehad = r.Gaus((1-fem)*energy*mean_rhad, (1-fem)*energy*sigma_rhad)

    E = Epi0 + Ehad

    h_fem.Fill(fem)

    h_rpi0.Fill(Epi0)
    h_rhad.Fill(Ehad)

    h_r.Fill(E)


out_root = ROOT.TFile("out.root","RECREATE")

h_fem.Write()
h_rpi0.Write()
h_rhad.Write()

h_r.Write()


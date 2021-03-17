import ROOT, math
from ROOT import TF1, TCanvas, TLegend, TH1F, TRandom3, TVector3



try:
  input = raw_input
except:
  pass


pmiss=10.
pbib=5.

nev = 100000

hp1 =TH1F("","",100,0, 50)
hp2 =TH1F("","",100,0, 50)

r = TRandom3()


p_nobib_av = 0.
p_bib_av = 0.


for iev in xrange(nev):
   
   
    theta1 = r.Uniform(0,math.pi)
    #theta2 = r.Uniform(0,2*math.pi)

    '''
    p_nobib = TVector3()
    p_bib = TVector3()

    p_nobib.SetXYZ( pmiss*math.cos(theta1),  pmiss*math.sin(theta1), 0.)
    p_bib.SetXYZ( pbib*math.cos(theta2),  pbib*math.sin(theta2), 0.)    
    
    p_bib = p_bib + p_nobib

    #print p_bib.Pt(), p_nobib.Pt() 
    '''

    print math.cos(theta1), 2.*pmiss*pbib*math.cos(theta1)

    val_p_bib = pmiss
    val_p_nobib = math.sqrt(2.*pmiss*pbib*math.cos(theta1))

    hp2.Fill(val_p_bib)
    hp1.Fill(val_p_nobib)

    p_bib_av += val_p_bib
    p_nobib_av += val_p_nobib


p_bib_av = p_bib_av/float(nev)
p_nobib_av = p_nobib_av/float(nev)


print p_nobib_av, p_bib_av


c = TCanvas()

hp1.SetLineColor(ROOT.kRed)
hp1.Draw()

hp2.SetLineColor(ROOT.kBlue)
hp2.Draw("same")


c.Print("missinget.png")

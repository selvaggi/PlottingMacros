

#____________________________________________________________________________________________    
    
    
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''
def pol(x, a, b, c):
    return a*x**2 + b*x + c

x = np.array( [0.50, 0.90, 0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.10,1.50])
y = np.array([1.92258,1.41752,1.36266,1.35191,1.34124,1.33063,1.32011,1.30965,1.29927,1.28896,1.27872,1.26856,1.25848,1.20914,0.88070])

fitting_parameters, covariance = curve_fit(pol, x, y)
a, b, c = fitting_parameters

x_min = 0  
x_max = 3                                #min/max values for x axis

x_fit = np.linspace(x_min, x_max, 100)   #range of x values used for the fit function
plt.plot(x, y, 'o', label='data')
plt.plot(x_fit, pol(x_fit, *fitting_parameters), '-', label='Fit')

plt.axis([x_min, x_max, 0, 3])
plt.legend()

#plt.show()
	

##### here predict k factor for 27 TeV based on 100 TeV ########

x = np.array( ['-1.000', '-0.500','0.000','0.500','0.750','0.800','0.850','0.875','0.900','0.925','0.950','0.975','1.000','1.025','1.050','1.075','1.100','1.125','1.150','1.200','1.250','1.500','2.000','2.500','3.000'] )

#xsec_kl100 = 0.1399* 2. * 0.58
#xsec_kl100 = 1.224 * 2. * 0.58

xsec_kl100 = 1.224 

for xval in x:

    xsec = float(pol(float(xval), *fitting_parameters) / pol(1.00, *fitting_parameters)) * xsec_kl100
    
    klstr = xval.replace('.', '')
    klstr = klstr[:-1]
    #print "'mg_pp_hh_5f_kl_{}':['HH, H->bb, H undec., kl = {}','inclusive','','{}','1.0','1.0'],".format(klstr,xval,xsec)
    
    #print "'mg_pp_hh_lambda{}_5f':['HH, H->bb, H undec., kl = {}','','','{}','1.0','1.0'],".format(klstr,xval,xsec)

    print xval,xsec
'''

import ROOT
from ROOT import *
import optparse
import os
import math


def getYield(h, lumi):
    
    err = ROOT.Double()
    yld = h.IntegralAndError(0, h.GetNbinsX()+1, err)
    raw = h.GetEntries()
    yld *= intLumi

    return yld

colors = []
colors.append(kRed);
colors.append(kOrange-3);
colors.append(kGreen+2);
colors.append(kBlue-3);
colors.append(kRed-9);
colors.append(kYellow+2);
colors.append(kMagenta+1);


path='/afs/cern.ch/work/s/selvaggi/private/Analysis/FCC/FlatTreeAnalyzer/vbs_wwss/'


#kappas = ['050', '090', '095', '100', '105', '110','130', '150']
kappas = ['090', '095', '100', '105', '110']
#kappas = ['050', '070','080','090', '095', '100', '105', '110','120','130', '150']


#vals = [135740,118000,106000,108000,131000]
#errs = [3300, 3000, 2700, 2700, 3000]


# actual plotting
c = TCanvas("c","c",600,600)
c.SetTicks(1,1)
c.SetLeftMargin(0.14)
c.SetRightMargin(0.08)
#c.SetGridx()
#c.SetGridy()



sel = '0'
intLumi = 30000000.

fname = path + 'root_W^_pmW^_pmjj100/histos.root'
f = TFile.Open(fname)

mg = TMultiGraph()
graphs = {}

leg = {}
leg[0]="m_{l^{+}l^{+}} > 50 GeV"
leg[2]="m_{l^{+}l^{+}} > 400 GeV"
leg[4]="m_{l^{+}l^{+}} > 800 GeV"

for j in [4,2,0]:

    sel = '{}'.format(j)

    hmll_sig0 = f.Get("W^{{#pm}} W^{{#pm}} j j 100_sel{}_mll".format(sel)).Clone()
    
    print ' ---  selection: {} ----'.format(j)
    s0 =  getYield(hmll_sig0, intLumi)

    graph = TGraphErrors()
    graphs[j] = graph

    graphs[j].SetLineWidth(3)
    graphs[j].SetLineColor(colors[j])
    graphs[j].SetMarkerColor(colors[j])
    graphs[j].SetTitle(leg[j])


    for i in range(len(kappas)):

	k =  kappas[i]

	fname2 = path + 'root_W^_pmW^_pmjj{}/histos.root'.format(k)
	f2 = TFile.Open(fname2)

	hmll_sig = f2.Get("W^{{#pm}} W^{{#pm}} j j {}_sel{}_mll".format(k,sel))
	s =  getYield(hmll_sig, intLumi)

	hmll_b1 = f.Get("WW(TT,TL)_sel{}_mll".format(sel))
	b1 =  getYield(hmll_b1, intLumi)

	hmll_b2 = f.Get("WZ_sel{}_mll".format(sel))
	b2 =  getYield(hmll_b2, intLumi)

	b = b1+b2

	dmu_mu = math.sqrt(s + b)/s
	#print s, b1, b2, dmu_mu, dmu_mu*s
	err = dmu_mu*s

	rel_sigma = s/s0
	rel_err = dmu_mu*rel_sigma

	knew = k[:1] + '.' + k[1:]
	kf=float(knew)

        print 'kw:', kf, 'S:', s,'B:', b, 'stat.err: ', dmu_mu, 'S/S0:',rel_sigma, 'err(S/S0):', rel_err

	graphs[j].SetPoint(i,kf, rel_sigma)
	graphs[j].SetPointError(i,0.,rel_err)

    mg.Add(graphs[j])

c.cd()


mg.Draw('ACP')

mg.GetXaxis().SetTitle("#kappa_{W}")
mg.GetYaxis().SetTitle("#sigma / #sigma_{SM}")

lege = c.BuildLegend(0.45,0.70,0.80,0.88)
lege.SetFillColor(0)
lege.SetFillStyle(0)
lege.SetLineColor(0)
lege.Draw() 

Text = TPaveText(0.58, 0.88,0.93,0.95,'brNDC')
#Text.SetNDC() 
Text.SetTextAlign(31);
Text.SetTextSize(0.04) 
leftText = "FCC-hh Simulation (Delphes)"
re = "#sqrt{s} = 100 TeV, L = 30 ab^{-1}"
text = '#it{' + leftText +'}'
#Text.DrawLatex(0.90, 0.92, text) 
Text.AddText(text)
Text.SetFillStyle(0)
Text.SetLineStyle(0)
Text.SetBorderSize(0)
Text.Draw("same")

Text3 = TPaveText(0.37, 0.55, 0.67, 0.65,'brNDC')
text = '#bf{#it{VBS - W^{#pm}_{L} W^{#pm}_{L}}}'

Text3.SetTextAlign(22);
Text3.SetTextSize(0.045) 
Text3.AddText(text)
#Text2.SetFillStyle(0)
Text3.SetFillColor(kWhite)
Text3.SetLineStyle(0)
Text3.SetBorderSize(0)
Text3.Draw()

c.SaveAs("ll_vbs.png")



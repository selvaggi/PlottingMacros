import ROOT
from ROOT import gROOT
import optparse
import os
import math
import itertools
import re
import collections


#_____________________________________________________________________________________________________
def drawMultiGraph(mg, title, lt, rt, fname,  ymin, ymax, xmin, xmax, log, bl = True):

    #myStyle()
    gROOT.SetBatch(True)
    canvas = ROOT.TCanvas('bla', 'bla', 600, 600) 
    canvas.SetLogy(log)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)
    ROOT.gStyle.SetOptStat(0000000)    
    
    mg.Draw("AL")

    mg.GetXaxis().SetTitleSize(0.035)
    mg.GetYaxis().SetTitleSize(0.035)
    
    mg.GetXaxis().SetRangeUser(xmin, xmax)

    mg.GetYaxis().SetTitleOffset(1.75)
    mg.GetXaxis().SetTitleOffset(1.35)

    mg.SetMinimum(ymin)
    mg.SetMaximum(ymax)
    
    if log: ROOT.gPad.SetLogy()

    if bl:
        leg = canvas.BuildLegend(0.55,0.70,0.88,0.88)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.Draw() 

    Text = ROOT.TLatex()
    
    Text.SetNDC() 
    Text.SetTextAlign(31);
    Text.SetTextSize(0.04) 

    text = '#it{' + lt +'}'
    
    Text.DrawLatex(0.90, 0.92, text) 

    '''
    rt = re.split(",", rt)
    text = '#bf{#it{' + rt[0] +'}}'
    
    Text.SetTextAlign(22);
    Text.SetNDC(ROOT.kTRUE) 
    Text.SetTextSize(0.04) 
    Text.DrawLatex(0.30, 0.83, text)
    
    Text.SetTextAlign(22);
    text = '#bf{#it{' + rt[1] +'}}'
    Text.SetTextSize(0.036) 
    Text.DrawLatex(0.30, 0.76, text)
    #Text.DrawLatex(0.18, 0.78, rt[1])

    if len(rt)>2:
        text = '#it{#bf{' + rt[2] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.05) 
        Text.DrawLatex(0.69, 0.27, text)

    if len(rt)>3:
        text = '#it{#bf{' + rt[3] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.04) 
        Text.DrawLatex(0.71, 0.20, text)
    '''
    
    canvas.RedrawAxis()
    canvas.Update()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()
 
    pdir = os.path.dirname(fname)
    name = os.path.basename(fname)
    name = title + '_' + name
    
    filename = 'darkPhotonContour'
    
    canvas.Print('{}.pdf'.format(filename), 'pdf')
    canvas.Print('{}.png'.format(filename), 'png')

#------------------------------------------------------------------------------------------------------------------------

def produceGraph(infile, title, index):

    f = ROOT.TFile.Open(infile)
    histSign = f.Get("histSignificance")

    print title
    nbins_m = histSign.GetNbinsX()
    nbins_eps = histSign.GetNbinsY()
    x = []
    y = []

    for i in range(nbins_m):
        for j in range(nbins_eps):
            sign = histSign.GetBinContent(i+1,j+1)

            ma = histSign.GetXaxis().GetBinCenter(i+1)
            logepssq = histSign.GetYaxis().GetBinCenter(j+1)
            #print ma, logepssq, sign

            if sign > 2.:
                x.append(ma)
                y.append(logepssq)
                break

    gr = ROOT.TGraph()
    gr.SetTitle(title)

    gr.SetLineColor(colors[index])
    gr.SetLineWidth(3)
    gr.SetMarkerSize(0.0001)
    gr.SetFillColor(0)

    i=0
    for m, e in itertools.izip(x,y):
        print m, e, 10**e
        gr.SetPoint(i,m,10**e)
        i+=1

    return gr 

colors = []
colors.append(ROOT.kRed);
colors.append(ROOT.kOrange-3);
colors.append(ROOT.kGreen+2);
colors.append(ROOT.kBlue-3);
colors.append(ROOT.kBlack);
colors.append(ROOT.kOrange-3);
colors.append(ROOT.kRed-9);
colors.append(ROOT.kYellow+2);
colors.append(ROOT.kMagenta+1);


prefix = '/afs/cern.ch/work/s/selvaggi/private/Delphes/'

titles = collections.OrderedDict()

#titles[prefix+'dp_cmsPhaseII_ee_s001_HF_3000invfb.root'] = 'CMS-PhaseII (HF), (ee)'
titles[prefix+'dp_LHCb_mumu_s001_HF_500invfb.root'] = 'LHCb, (#mu#mu)'
titles[prefix+'dp_cmsPhaseII_ee_s001_Nose_3000invfb.root'] = 'CMS-PhaseII (Nose), (ee)'
#titles[prefix+'dp_cmsPhaseII_mumu_s05_HF_3000invfb.root'] = 'CMS-PhaseII (HF), (#mu#mu)'
#titles[prefix+'dp_cmsPhaseII_mumu_s05_Nose_3000invfb.root'] = 'CMS-PhaseII (Nose), (#mu#mu)'


mgContour = ROOT.TMultiGraph()
mgContour.SetTitle(";m_{Z_{D}} [GeV]; #varepsilon^{2}")

i = 0
grs = []
for f, t in titles.items():
   gr = produceGraph(f, t, i)
   mgContour.Add(gr)
   i +=1

lt=''
rt=''
fname = 'bla'

ymin = 1.e-8
ymax = 1.e-5
xmax = 10.
xmin = 60.

drawMultiGraph(mgContour, 'sign', lt, rt, fname, ymin, ymax, xmin, xmax, True, True)


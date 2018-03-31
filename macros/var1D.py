'''
python macros/var1D.py  --f1 files/histo_h4mu_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_h4mu_13tev.root --h2 eta1 --l2 '13 TeV' --tx '\eta_{\ell}^{max}' --xmin 0. --xmax 8.0 --norm --cap_in '#sqrt{s} = 100 TeV, , gg #to H #to 4#ell' --cap_upr 'FCC-hh Simulation' --out plots/etalep; 
python macros/var1D.py  --f1 files/histo_vbf_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_vbf_13tev.root --h2 eta1 --l2 '13 TeV' --tx '#eta_{j}^{max}' --xmin 0. --xmax 8 --norm --cap_in '#sqrt{s} = 100 TeV, p_{T}^{jet} > 25 GeV, VBF Higgs' --cap_upr 'FCC-hh Simulation' --out plots/vbfjet
'''

import optparse
import ROOT, sys, re, os
from ROOT import TFile, TH1F, TCanvas, TLegend, THStack

#______________________________________________________________________________
def split_comma_args(args):
    new_args = []
    for arg in args:
        new_args.extend( arg.split(',') )
    return new_args

#_____________________________________________________________________________
def options():
    parser = optparse.OptionParser(description="generic 1D plotter")
    # file1 ...
    parser.add_option('--f1', dest='f1', type=str, default='histo1.root')
    parser.add_option('--h1', dest='h1', type=str, default='hpt')
    parser.add_option('--l1', dest='l1', type=str, default='ggH')

    # file2 ...
    parser.add_option('--f2', dest='f2', type=str, default='histo2.root')
    parser.add_option('--h2', dest='h2', type=str, default='hpt')
    parser.add_option('--l2', dest='l2', type=str, default='VBF')    
    
    # general parameters
    parser.add_option('--tx', dest='tx', type=str, default='p_{T}')    
    parser.add_option('--ty', dest='ty', type=str, default='normalized event rate')    
    parser.add_option('--cap_upr', dest='cap_upr', type=str, default='FCC-hh Simulation (Delphes)')    
    
    # if commas are present text is distributed among various lines
    parser.add_option('--cap_in', dest='cap_in', type=str, default='#sqrt{s} = 100 TeV, L = 30 ab^{-1}')    

    parser.add_option('--xmin', dest='xmin', type=float)    
    parser.add_option('--xmax', dest='xmax', type=float)    
    parser.add_option('--ymin', dest='ymin', type=float)    
    parser.add_option('--ymax', dest='ymax', type=float)    

    parser.add_option('--norm', dest='norm', default=False, action='store_true')
    parser.add_option('--log', dest='log', default=False, action='store_true')
    parser.add_option('--rebin', dest='rebin', type=int, default=1)

    parser.add_option('--out', dest='out', type=str, default='plots/plot')

    return parser.parse_args()

#______________________________________________________________________________
def main():
    
    ops, args = options()

    args = split_comma_args(args)

    # define canvas
    canvas = ROOT.TCanvas("", "", 600, 600) 
    canvas.SetLogy(ops.log)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0000000)    

    # get files
    hfile1 = ROOT.TFile(ops.f1)
    hfile2 = ROOT.TFile(ops.f2)

    # get and initialize histos
    h1 = hfile1.Get(ops.h1)
    h2 = hfile2.Get(ops.h2)
    h1.SetTitle(ops.l1)
    h2.SetTitle(ops.l2)
    h1.GetXaxis().SetTitle(ops.tx)
    h1.GetYaxis().SetTitle(ops.ty)
    #h1.GetYaxis().SetTitleOffset(1.75)
    #h1.GetXaxis().SetTitleOffset(1.40)
    h1.GetYaxis().SetTitleOffset(1.6)
    h1.GetXaxis().SetTitleOffset(1.0)
    h1.GetXaxis().SetTitleSize(0.045)
    h1.GetYaxis().SetTitleSize(0.045)
    h1.SetLineWidth(3)
    h1.SetLineColor(ROOT.kBlue)
    h1.SetLineStyle(1)
    h2.SetLineWidth(3)
    h2.SetLineStyle(ROOT.kRed)
    h2.SetLineStyle(7)

    if ops.norm:
        h1.Scale(1./h1.Integral(0, h1.GetNbinsX()+1))
        h2.Scale(1./h2.Integral(0, h2.GetNbinsX()+1))

    h1.Rebin(ops.rebin)
    h2.Rebin(ops.rebin)

    # set histogram boundaries
    maxi = max(h1.GetMaximum(), h2.GetMaximum())
    
    if ops.xmin is not None and ops.xmax is not None: 
       print 'here'
       h1.GetXaxis().SetRangeUser(ops.xmin, ops.xmax)
    
    if not ops.ymax:
       if not ops.log:
           h1.SetMaximum(maxi*1.7)
       else:
           h1.SetMaximum(maxi*100.)
    else:
       h1.SetMaximum(ops.ymax)
       
    if ops.ymin:
       h1.SetMinimum(ops.ymin)



    h1.Draw('hist ')
    h2.Draw('same hist')

    # build legend
    leg = TLegend(0.65,0.70,0.90,0.88)
    leg.AddEntry(h1,ops.l1,"l")
    leg.AddEntry(h2,ops.l2,"l")
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.Draw() 


    # add captions
    Text = ROOT.TLatex()
    Text.SetNDC() 
    Text.SetTextAlign(31);
    Text.SetTextSize(0.04) 

    # start with upright
    text = '#it{' + ops.cap_upr +'}'
    Text.DrawLatex(0.90, 0.92, text) 

    # now text inside
    rt = re.split(",", ops.cap_in)
    text = '#bf{#it{   ' + rt[0] +'}}'
    
    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE) 
    #Text.SetTextSize(0.04) 
    Text.DrawLatex(0.28, 0.83, text)
    
    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE) 
    text = '#bf{#it{' + rt[1] +'}}'
    if 'ell' in text:
       text = text.replace('#','\\')
    Text.SetTextSize(0.03) 
    Text.DrawLatex(0.28, 0.76, text)

    print rt[0]
    print rt[1]
    

    # this happens only if additional text
    if len(rt)>2:
        text = '#it{#bf{' + rt[2] +'}}'
        if 'ell' in text:
	   text = text.replace('#','\\')
	Text.SetTextSize(0.05) 
        Text.DrawLatex(0.72, 0.50, text)

    if len(rt)>3:
        text = '#it{#bf{' + rt[3] +'}}'
        if 'ell' in text:
	   text = text.replace('#','\\')
        Text.SetTextSize(0.04) 
        Text.DrawLatex(0.72, 0.40, text)

    canvas.RedrawAxis()
    canvas.Update()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    pdir = os.path.dirname(ops.out)
    name = os.path.basename(ops.out)
    filename = pdir + '/' + name
    
    if not os.path.exists(pdir):
       os.makedirs(pdir)
    canvas.Print('{}.png'.format(filename), 'png')
    canvas.Print('{}.eps'.format(filename), 'eps')

#______________________________________________________________________________
if __name__ == '__main__': 
    main()

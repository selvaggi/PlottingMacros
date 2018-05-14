'''
python macros/var1D.py  --f1 files/histo_h4mu_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_h4mu_13tev.root --h2 eta1 --l2 '13 TeV' --tx '\eta_{\ell}^{max}' --xmin 0. --xmax 8.0 --norm --cap_in 'p_{T}^{\ell} > 3 \;GeV, , gg #to H #to 4#ell' --cap_upr 'FCC-hh Simulation' --out plots/etalep
python macros/var1D.py  --f1 files/histo_vbf_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_vbf_13tev.root --h2 eta1 --l2 '13 TeV' --tx '#eta_{j}^{max}' --xmin 0. --xmax 8 --norm --cap_in 'p_{T}^{jet} > 25 \;GeV, ,VBF Higgs' --cap_upr 'FCC-hh Simulation' --out plots/vbfjet
python macros/var1D.py  --f1 ../../../ntuple-tools/FccDiJet200GeV/out/FccDiJet200GeV.root --h1 rp_hc_ak4 --l1 'prompt jet'  --f2 ../../../ntuple-tools/Fcc200PU/out/Fcc200PU.root --h2 rp_hc_ak4 --l2 'pile-up jet (200PU)'  --f3 ../../../ntuple-tools/Fcc1000PU/out/Fcc1000PU.root --h3 rp_hc_ak4 --l3 'pile-up jet (1000PU)' --ty '< d E / d R >'  --ymax 0.05  --tx 'R' --cap_in 'p_{T}^{jet} > 100 \;GeV , , HCAL' --cap_upr 'FCC-hh Simulation' --out plots/pu_lat_hcal --draw_opt 'hist';
python macros/var1D.py  --f1 ../../../ntuple-tools/FccDiJet200GeV/out/FccDiJet200GeV.root --h1 rp_ec_ak4 --l1 'prompt jet'  --f2 ../../../ntuple-tools/Fcc200PU/out/Fcc200PU.root --h2 rp_ec_ak4 --l2 'pile-up jet (200PU)'  --f3 ../../../ntuple-tools/Fcc1000PU/out/Fcc1000PU.root --h3 rp_ec_ak4 --l3 'pile-up jet (1000PU)' --ty '< d E / d R >' --ymax 0.07  --tx 'R' --cap_in 'p_{T}^{jet} > 100 \;GeV , , ECAL' --cap_upr 'FCC-hh Simulation' --out plots/pu_lat_ecal --draw_opt 'hist'
'''

import argparse

#_____________________________________________________________________________
def options():
    parser = argparse.ArgumentParser(description="generic 1D plotter")

    # file1 ...
    parser.add_argument('--f1', dest='f1', type=str, help='first file containing TH1', default='histo1.root')
    parser.add_argument('--h1', dest='h1', type=str, help='name of TH1 in file1', default='hpt')
    parser.add_argument('--l1', dest='l1', type=str, help='label for TH1 in file1 to be appeared in the legend', default='ggH')

    # file2 ...
    parser.add_argument('--f2', dest='f2', type=str, help='second file containing TH1', default='')
    parser.add_argument('--h2', dest='h2', type=str, help='name of TH1 in file1', default='')
    parser.add_argument('--l2', dest='l2', type=str, help='label for TH1 in file1 to be appeared in the legend', default='')    

    # file3 ...
    parser.add_argument('--f3', dest='f3', type=str, help='second file containing TH1', default='')
    parser.add_argument('--h3', dest='h3', type=str, help='name of TH1 in file1', default='')
    parser.add_argument('--l3', dest='l3', type=str, help='label for TH1 in file1 to be appeared in the legend', default='')    

    # general parameters
    parser.add_argument('--tx', dest='tx', type=str, help='title of x-axis', default='p_{T}')    
    parser.add_argument('--ty', dest='ty', type=str, help='title of y-axis', default='normalized event rate')    
    parser.add_argument('--cap_upr', dest='cap_upr', type=str, help='caption to appear in top right corner', default='FCC-hh Simulation (Delphes)')    
    
    # if commas are present text is distributed among various lines
    parser.add_argument('--cap_in', dest='cap_in', type=str, help='caption to appear in the canvas (separation with comma for multiple captions)', default='#sqrt{s} = 100 TeV, L = 30 ab^{-1}')    

    parser.add_argument('--xmin', dest='xmin', type=float, help='minimum x value')    
    parser.add_argument('--xmax', dest='xmax', type=float, help='maximum x value')    
    parser.add_argument('--ymin', dest='ymin', type=float, help='minimum y value')    
    parser.add_argument('--ymax', dest='ymax', type=float, help='maximum y value')    

    parser.add_argument('--norm', dest='norm', default=False, help='normalize histograms to 1', action='store_true')
    parser.add_argument('--log', dest='log', default=False, help='plot y-axis in log scale', action='store_true')
    parser.add_argument('--rebin', dest='rebin', type=int, help='rebin by amount specified', default=1)

    parser.add_argument('--draw_opt', dest='draw_opt', type=str, help='specifiy root draw option', default='hist')

    parser.add_argument('--out', dest='out', type=str, help='output filename', default='plots/plot')

    return parser.parse_args()

#______________________________________________________________________________
def main():
    
    ops = options()

    import ROOT, sys, re, os
    from ROOT import TFile, TH1F, TCanvas, TLegend, THStack
        
    # define canvas
    canvas = ROOT.TCanvas("", "", 600, 600) 
    canvas.SetLogy(ops.log)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.16)
    canvas.SetRightMargin(0.08)
    canvas.SetBottomMargin(0.12)
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0000000)    

    # get files
    hfile1 = ROOT.TFile(ops.f1)
    
    # get and initialize histos
    h1 = hfile1.Get(ops.h1)
    h1.SetTitle(ops.l1)
    h1.GetXaxis().SetTitle(ops.tx)
    h1.GetYaxis().SetTitle(ops.ty)
    #h1.GetYaxis().SetTitleOffset(1.75)
    #h1.GetXaxis().SetTitleOffset(1.40)
    h1.GetYaxis().SetTitleOffset(1.6)
    h1.GetXaxis().SetTitleOffset(1.0)
    h1.GetXaxis().SetTitleSize(0.045)
    h1.GetYaxis().SetTitleSize(0.045)
    h1.SetLineWidth(4)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineStyle(2)
    h1.SetTitle('')

    if ops.norm:
        h1.Scale(1./h1.Integral(0, h1.GetNbinsX()+1))

    h1.Rebin(ops.rebin)

    # set histogram boundaries
    maxi = h1.GetMaximum()
        
    draw_option = ops.draw_opt

    h1.Draw(draw_option)

    draw_option = 'same '+draw_option

    legsize = 0.06
    ylegsize = legsize

    # if option 2 is defined
    max2 = 0
    if ops.f2:
        hfile2 = ROOT.TFile(ops.f2)
        h2 = hfile2.Get(ops.h2)
        h2.SetTitle(ops.l2)
        h2.SetLineWidth(4)
        h2.SetLineColor(ROOT.kRed)
        h2.SetLineStyle(1)
        if ops.norm:
           h2.Scale(1./h2.Integral(0, h2.GetNbinsX()+1))
        h2.Rebin(ops.rebin)
        max2 =  h2.GetMaximum() 
        maxi = max(maxi, max2)
        ylegsize += legsize

        h2.Draw(draw_option)

    # if option 3 is defined
    max3 = 0
    if ops.f3:
        hfile3 = ROOT.TFile(ops.f3)
        h3 = hfile3.Get(ops.h3)
        h3.SetTitle(ops.l3)
        h3.SetLineWidth(4)
        h3.SetLineColor(ROOT.kBlue)
        h3.SetLineStyle(7)
        if ops.norm:
           h3.Scale(1./h3.Integral(0, h3.GetNbinsX()+1))
        h3.Rebin(ops.rebin)
        max3 =  h3.GetMaximum() 
        maxi = max(maxi, max3)
        ylegsize += legsize

        h3.Draw(draw_option)
        legsize += 0.06


    if ops.xmin is not None and ops.xmax is not None: 
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


    # build legend
    leg = TLegend(0.55,0.88-legsize,0.90,0.88)
    leg.AddEntry(h1,ops.l1,"l")
    if ops.f2:
        leg.AddEntry(h2,ops.l2,"l")
    if ops.f3:
        leg.AddEntry(h3,ops.l3,"l")

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
    text = text.replace('#','\\')
    
    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE) 
    #Text.SetTextSize(0.04) 
    Text.DrawLatex(0.30, 0.83, text)
    
    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE) 
    text = '#bf{#it{' + rt[1] +'}}'
    if 'ell' in text:
       text = text.replace('#','\\')
    Text.SetTextSize(0.03) 
    Text.DrawLatex(0.30, 0.76, text)

    print rt[0]
    print rt[1]

    # this happens only if additional text
    if len(rt)>2:
        text = '#it{#bf{' + rt[2] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.05) 
        Text.DrawLatex(0.69, 0.60, text)

    if len(rt)>3:
        text = '#it{#bf{' + rt[3] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.04) 
        Text.DrawLatex(0.69, 0.50, text)

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
    canvas.Print('{}.pdf'.format(filename), 'pdf')

#______________________________________________________________________________
if __name__ == '__main__': 
    main()

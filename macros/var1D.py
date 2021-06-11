'''
python macros/var1D.py  --f1 files/histo_h4mu_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_h4mu_13tev.root --h2 eta1 --l2 '13 TeV' --tx '\eta_{\ell}^{max}' --xmin 0. --xmax 8.0 --norm --cap_in 'p_{T}^{\ell} > 3 \;GeV, , gg #to H #to 4#ell' --cap_upr 'FCC-hh Simulation' --out plots/etalep
python macros/var1D.py  --f1 files/histo_vbf_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_vbf_13tev.root --h2 eta1 --l2 '13 TeV' --tx '#eta_{j}^{max}' --xmin 0. --xmax 8 --norm --cap_in 'p_{T}^{jet} > 25 \;GeV, ,VBF Higgs' --cap_upr 'FCC-hh Simulation' --out plots/vbfjet
python macros/var1D.py  --f1 ../../../ntuple-tools/FccDiJet200GeV/out/FccDiJet200GeV.root --h1 ep_ak4 --l1 'prompt jet'  --f2 ../../../ntuple-tools/Fcc200PU/out/Fcc200PU.root --h2 ep_ak4 --l2 'pile-up jet (200PU)'  --f3 ../../../ntuple-tools/Fcc1000PU/out/Fcc1000PU.root --h3 ep_ak4 --l3 'pile-up jet (1000PU)' --ymax 0.50 --xmax 18 --ty '< E_{layer}^{(i)} / E_{jet} >' --tx 'layer number' --cap_in 'p_{T}^{jet} > 100 \;GeV , , ' --cap_upr 'FCC-hh Simulation' --out plots/pu_long --draw_opt 'hist';
python macros/var1D.py  --f1 ../../../ntuple-tools/FccDiJet200GeV/out/FccDiJet200GeV.root --h1 rp_hc_ak4 --l1 'prompt jet'  --f2 ../../../ntuple-tools/Fcc200PU/out/Fcc200PU.root --h2 rp_hc_ak4 --l2 'pile-up jet (200PU)'  --f3 ../../../ntuple-tools/Fcc1000PU/out/Fcc1000PU.root --h3 rp_hc_ak4 --l3 'pile-up jet (1000PU)' --ty '< d E / d R >'   --tx 'R' --cap_in 'p_{T}^{jet} > 100 \;GeV , , HCAL' --cap_upr 'FCC-hh Simulation' --out plots/pu_lat_hcal --draw_opt 'hist'
python macros/var1D.py  --f1 ../../../ntuple-tools/FccDiJet200GeV/out/FccDiJet200GeV.root --h1 rp_ec_ak4 --l1 'prompt jet'  --f2 ../../../ntuple-tools/Fcc200PU/out/Fcc200PU.root --h2 rp_ec_ak4 --l2 'pile-up jet (200PU)'  --f3 ../../../ntuple-tools/Fcc1000PU/out/Fcc1000PU.root --h3 rp_ec_ak4 --l3 'pile-up jet (1000PU)' --ty '< d E / d R >'  --tx 'R' --cap_in 'p_{T}^{jet} > 100 \;GeV , , ECAL' --cap_upr 'FCC-hh Simulation' --out plots/pu_lat_ecal --draw_opt 'hist'

python macros/var1D.py  --f1 /eos/experiment/fcc/hh/generation/DelphesStandalone/QCD_Pt50/histosQCD/out/histosQCD.root --h1 cumRecoMet04 --l1 '|#eta| < 4'  --f2 /eos/experiment/fcc/hh/generation/DelphesStandalone/QCD_Pt50/histosQCD/out/histosQCD.root --h2 cumRecoMet05 --l2 '|#eta| < 5'  --f3 /eos/experiment/fcc/hh/generation/DelphesStandalone/QCD_Pt50/histosQCD/out/histosQCD.root --h3 cumRecoMet06 --l3 '|#eta| < 6' --ty 'P(E_{T}^{miss} > E_{T}^{miss}(min))' --tx 'E_{T}^{miss}(min)' --cap_in 'p_{T}^{jet} > 50 \;GeV, , QCD events' --cap_upr 'FCC-hh Simulation' --out plots/Recomet_reso --draw_opt 'hist' --log --norm1stbin --ymin 1e-5 --xmin 0 --xmax 150;

python macros/var1D.py  --f1 /afs/cern.ch/work/s/selvaggi/private/Analysis/FCC/FlatTreeAnalyzer/BatchOutput/hmumu_fcc/sel_H_125/root_H_125/histos.root --h1 H(125)_sel0_mh --l1 'FCC'  --f2 /afs/cern.ch/work/s/selvaggi/private/Analysis/FCC/FlatTreeAnalyzer/BatchOutput/hmumu_helhc/sel_H_125/root_H_125/histos.root --h2 H(125)_sel0_mh --l2 'CMS' --tx 'm_{#mu #mu}' --xmin 122.5 --xmax 127.5 --norm --cap_in 'p_{T}^{\ell} > 3 \;GeV, , gg #to H #to 4#ell' --cap_upr 'FCC-hh Simulation' --out plots/mmumu


python macros/var1D.py  --f1 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HFNose/histos/out/histos.root --h1 histEta2 --l1 'm_{Z_{D}} = 15 GeV'  --f2 /eos/user/s/selvaggi/DelphesNose/pp_zd_m35_HFNose/histos/out/histos.root --h2 histEta2 --l2 'm_{Z_{D}} = 35 GeV'  --f3 /eos/user/s/selvaggi/DelphesNose/pp_zd_m55_HFNose/histos/out/histos.root --h3 histEta2 --l3 'm_{Z_{D}} = 55 GeV' --ty 'a. u.' --tx '#eta_{lep}^{max}' --out plots/darkphot_etamax --draw_opt 'hist' --norm --cap_in '#sqrt{s} = 14 TeV,' --cap_upr 'CMS-PhaseII Simulation (Delphes)'
python macros/var1D.py  --f1 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HFNose/histos/out/histos.root --h1 histRecoEECF_M --l1 'HF-Nose'  --f2 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HF/histos/out/histos.root --h2 histRecoEECF_M --l2 'HF'  --ty 'a. u.' --tx 'm_{e^{+}e^{-}} [GeV/c^{2}]' --out plots/darkphot_mee --draw_opt 'hist' --norm  --cap_in '#sqrt{s} = 14 TeV, m_{Z_{D}} = 15 GeV , ' --cap_upr 'CMS-PhaseII Simulation (Delphes)' --xmin 10. --xmax 20.
python macros/var1D.py  --f2 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HFNose/histos/out/histos.root --h2 histRecoMMCF_M --l2 'Cen-Fwd'  --f1 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HF/histos/out/histos.root --h1 histRecoMMCC_M --l1 'Cen-Cen' --f3 /eos/user/s/selvaggi/DelphesNose/pp_zd_m15_HFNose/histos/out/histos.root --h3 histRecoMMFF_M --l3 'Fwd-Fwd'   --ty 'a. u.' --tx 'm_{#mu^{+}#mu^{-}} [GeV/c^{2}]' --out plots/darkphot_mmumu --draw_opt 'hist' --norm  --cap_in '#sqrt{s} = 14 TeV, , ' --cap_upr 'CMS-PhaseII Simulation (Delphes)' --xmin 10. --xmax 20.


'''

import argparse

import ROOT, sys, re, os
from ROOT import TFile, TH1F, TCanvas, TLegend, THStack, gROOT

'''
colours = [
    ROOT.kRed+1,
    ROOT.kGreen+2,
    ROOT.kBlue+1,
    ROOT.kOrange+1,
    ROOT.kPink+1,
]


styles = [
    2,
    1,
    1,
    1,
    1
]
'''

colours = [
    ROOT.kRed-3,
    ROOT.kRed+1,
    ROOT.kRed+3,
    ROOT.kRed+5,
    ROOT.kRed+5,
]


styles = [
    1,
    1,
    1,
    1,
    1
]



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

    # file4 ...
    parser.add_argument('--f4', dest='f4', type=str, help='second file containing TH1', default='')
    parser.add_argument('--h4', dest='h4', type=str, help='name of TH1 in file1', default='')
    parser.add_argument('--l4', dest='l4', type=str, help='label for TH1 in file1 to be appeared in the legend', default='')

    # file5 ...
    parser.add_argument('--f5', dest='f5', type=str, help='second file containing TH1', default='')
    parser.add_argument('--h5', dest='h5', type=str, help='name of TH1 in file1', default='')
    parser.add_argument('--l5', dest='l5', type=str, help='label for TH1 in file1 to be appeared in the legend', default='')




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
    parser.add_argument('--norm1stbin', dest='norm1stbin', default=False, help='normalize histograms to 1', action='store_true')
    parser.add_argument('--normlastbin', dest='normlastbin', default=False, help='normalize histograms to 1', action='store_true')
    parser.add_argument('--normnbin', dest='normnbin', help='normalize histograms to 1', type=int, default=-1)
    parser.add_argument('--normrange', dest='normrange', help='normalize histograms to 1 using defined range xmin, xmax',  action='store_true')
    parser.add_argument('--legsmall', dest='legsmall', help='small leg size (for many entries)',  action='store_true')

    parser.add_argument('--log', dest='log', default=False, help='plot y-axis in log scale', action='store_true')
    parser.add_argument('--gridx', dest='gridx', default=False, help='plot x-axis grid', action='store_true')
    parser.add_argument('--gridy', dest='gridy', default=False, help='plot y-axis grid', action='store_true')
    parser.add_argument('--png', dest='png', default=False, help='print png', action='store_true')
    parser.add_argument('--rebin', dest='rebin', type=int, help='rebin by amount specified', default=1)

    parser.add_argument('--overflow', dest='overflow', default=False, help='add overflow and underflow bins', action='store_true')

    parser.add_argument('--draw_opt', dest='draw_opt', type=str, help='specifiy root draw option', default='hist')

    parser.add_argument('--out', dest='out', type=str, help='output filename', default='plots/plot')

    return parser.parse_args()

#____________________________________________________________________________________________________
def addOverflow(h):

   # This function paint the histogram h with an extra bin for overflows

   name  = h.GetName()
   title = h.GetTitle()
   nx    = h.GetNbinsX()+2
   bw = h.GetBinWidth(nx)
   x1 = h.GetBinLowEdge(1)-bw
   x2 = h.GetBinLowEdge(nx)

   # Book a temporary histogram having ab extra bin for overflows
   htmp = ROOT.TH1F(name, title, nx, x1, x2)

   # Fill the new histogram including the extra bin for overflows
   for i in range(0,nx):
      htmp.Fill(htmp.GetBinCenter(i+1), h.GetBinContent(i))


   # Restore the number of entries
   htmp.SetEntries(h.GetEntries());
   return htmp


#______________________________________________________________________________
def main():

    ops = options()

    gROOT.SetBatch(True)


    # define canvas
    canvas = ROOT.TCanvas("", "", 600, 600)
    canvas.SetLogy(ops.log)
    canvas.SetGridx(ops.gridx)
    canvas.SetGridy(ops.gridy)
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
    h1.Rebin(ops.rebin)
    if ops.overflow:
       h1 = addOverflow(h1)

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
    #h1.SetLineColor(ROOT.kBlack)
    h1.SetLineColor(colours[0])
    h1.SetLineStyle(styles[0])
    h1.SetTitle('')

    if ops.norm:
        h1.Scale(1./h1.Integral(0, h1.GetNbinsX()+1))

    if ops.norm1stbin:
        scale = h1.GetBinContent(1)
        h1.Scale(1/scale)
    if ops.normlastbin:
        scale = h1.GetBinContent(h1.GetNbinsX())
        h1.Scale(1/scale)
    if ops.normnbin >=0:
        scale = h1.GetBinContent(ops.normnbin)
        h1.Scale(1/scale)

    if ops.normrange:
        axis = h1.GetXaxis()
        bmin = axis.FindBin(ops.xmin)
        bmax = axis.FindBin(ops.xmax)
        scale = h1.Integral(bmin, bmax)
        h1.Scale(1/scale)


    # set histogram boundaries
    maxi = h1.GetMaximum()

    draw_option = ops.draw_opt

    h1.Draw(draw_option)

    draw_option = 'same '+draw_option

    legsize = 0.10
    if ops.legsmall:
        legsize = 0.05

    ylegsize = legsize

    # if option 2 is defined
    max2 = 0
    if ops.f2:
        hfile2 = ROOT.TFile(ops.f2)
        h2 = hfile2.Get(ops.h2)
        h2.Rebin(ops.rebin)

        if ops.overflow:
           h2 = addOverflow(h2)

        h2.SetTitle(ops.l2)
        h2.SetLineWidth(4)
        h2.SetLineColor(colours[1])
        h2.SetLineStyle(styles[1])
        if ops.norm:
           h2.Scale(1./h2.Integral(0, h2.GetNbinsX()+1))

        if ops.norm1stbin:
            scale = h2.GetBinContent(1)
            h2.Scale(1/scale)

        if ops.normlastbin:
            scale = h2.GetBinContent(h2.GetNbinsX())
            h2.Scale(1/scale)

        if ops.normnbin >=0:
            scale = h2.GetBinContent(ops.normnbin)
            h2.Scale(1/scale)

        if ops.normrange:
            axis = h2.GetXaxis()
            bmin = axis.FindBin(ops.xmin)
            bmax = axis.FindBin(ops.xmax)
            scale = h2.Integral(bmin, bmax)
            h2.Scale(1/scale)


        max2 =  h2.GetMaximum()
        maxi = max(maxi, max2)
        ylegsize += legsize

        h2.Draw(draw_option)

    # if option 3 is defined
    max3 = 0
    if ops.f3:
        hfile3 = ROOT.TFile(ops.f3)
        h3 = hfile3.Get(ops.h3)
        h3.Rebin(ops.rebin)

        if ops.overflow:
           h3 = addOverflow(h3)
        h3.SetTitle(ops.l3)
        h3.SetLineWidth(4)
        h3.SetLineColor(colours[2])
        h3.SetLineStyle(styles[2])
        if ops.norm:
           h3.Scale(1./h3.Integral(0, h3.GetNbinsX()+1))

        if ops.norm1stbin:
            scale = h3.GetBinContent(1)
            h3.Scale(1/scale)

        if ops.normlastbin:
            scale = h3.GetBinContent(h3.GetNbinsX())
            h3.Scale(1/scale)

        if ops.normnbin >=0:
            scale = h3.GetBinContent(ops.normnbin)
            h3.Scale(1/scale)

        if ops.normrange:
            axis = h3.GetXaxis()
            bmin = axis.FindBin(ops.xmin)
            bmax = axis.FindBin(ops.xmax)
            scale = h3.Integral(bmin, bmax)
            h3.Scale(1/scale)

        max3 =  h3.GetMaximum()
        maxi = max(maxi, max3)
        ylegsize += legsize

        h3.Draw(draw_option)
        legsize += legsize


    max4 = 0
    if ops.f4:
        hfile4 = ROOT.TFile(ops.f4)
        h4 = hfile4.Get(ops.h4)
        h4.Rebin(ops.rebin)
        if ops.overflow:
           h4 = addOverflow(h4)
        h4.SetTitle(ops.l4)
        h4.SetLineWidth(4)
        h4.SetLineColor(colours[3])
        h4.SetLineStyle(styles[3])
        if ops.norm:
           h4.Scale(1./h4.Integral(0, h4.GetNbinsX()+1))

        if ops.norm1stbin:
            scale = h4.GetBinContent(1)
            h4.Scale(1/scale)

        if ops.normlastbin:
            scale = h4.GetBinContent(h4.GetNbinsX())
            h4.Scale(1/scale)

        if ops.normnbin >=0:
            scale = h4.GetBinContent(ops.normnbin)
            h4.Scale(1/scale)

        if ops.normrange:
            axis = h4.GetXaxis()
            bmin = axis.FindBin(ops.xmin)
            bmax = axis.FindBin(ops.xmax)
            scale = h4.Integral(bmin, bmax)
            h4.Scale(1/scale)

        max4 =  h4.GetMaximum()
        maxi = max(maxi, max4)
        ylegsize += legsize

        h4.Draw(draw_option)
        legsize += legsize


    max5 = 0
    if ops.f5:
        hfile5 = ROOT.TFile(ops.f5)
        h5 = hfile5.Get(ops.h5)
        if ops.overflow:
           h5 = addOverflow(h5)
        h5.SetTitle(ops.l5)
        h5.SetLineWidth(4)
        h5.SetLineColor(colours[4])
        h5.SetLineStyle(styles[4])
        if ops.norm:
           h5.Scale(1./h5.Integral(0, h5.GetNbinsX()+1))

        if ops.norm1stbin:
            scale = h5.GetBinContent(1)
            h5.Scale(1/scale)

        if ops.normlastbin:
            scale = h5.GetBinContent(h5.GetNbinsX())
            h5.Scale(1/scale)

        if ops.normnbin >=0:
            scale = h5.GetBinContent(ops.normnbin)
            h5.Scale(1/scale)

        if ops.normrange:
            axis = h5.GetXaxis()
            bmin = axis.FindBin(ops.xmin)
            bmax = axis.FindBin(ops.xmax)
            scale = h5.Integral(bmin, bmax)
            h5.Scale(1/scale)

        h5.Rebin(ops.rebin)
        max5 =  h5.GetMaximum()
        maxi = max(maxi, max5)
        ylegsize += legsize

        h5.Draw(draw_option)
        legsize += legsize




    h1.Draw(draw_option)

    if ops.xmin is not None and ops.xmax is not None:
       h1.GetXaxis().SetRangeUser(ops.xmin, ops.xmax)

    if not ops.ymax:
       if not ops.log:
           h1.SetMaximum(maxi*1.4)
       else:
           h1.SetMaximum(maxi*100.)
    else:
       h1.SetMaximum(ops.ymax)

    if ops.ymin:
       h1.SetMinimum(ops.ymin)


    # build legend
    leg = TLegend(0.50,0.86-legsize,0.90,0.86)
    if ops.legsmall:
        leg = TLegend(0.65,0.86-legsize,0.90,0.86)


    leg.AddEntry(h1,ops.l1,"l")
    if ops.f2:
        leg.AddEntry(h2,ops.l2,"l")
    if ops.f3:
        leg.AddEntry(h3,ops.l3,"l")
    if ops.f4:
        leg.AddEntry(h4,ops.l4,"l")
    if ops.f5:
        leg.AddEntry(h5,ops.l5,"l")


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
    #text = text.replace('#','\\')

    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE)
    #Text.SetTextSize(0.04)
    Text.DrawLatex(0.37, 0.83, text)

    Text.SetTextAlign(22)
    Text.SetNDC(ROOT.kTRUE)
    text = '#bf{#it{' + rt[1] +'}}'
    if 'ell' in text:
       text = text.replace('#','\\')
    Text.SetTextSize(0.03)
    Text.DrawLatex(0.37, 0.76, text)


    # this happens only if additional text
    if len(rt)>2:
        text = '#it{#bf{' + rt[2] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.03)
        Text.DrawLatex(0.37, 0.70, text)

    if len(rt)>3:
        text = '#it{#bf{' + rt[3] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.03)
        Text.DrawLatex(0.50, 0.60, text)


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

    if ops.png:
        canvas.Print('{}.bmp'.format(filename), 'bmp')
    #canvas.Print('{}.eps'.format(filename), 'eps')
    else:
        canvas.Print('{}.pdf'.format(filename), 'pdf')

#______________________________________________________________________________
if __name__ == '__main__':
    main()

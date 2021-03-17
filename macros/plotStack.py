
#python plotStack --h histRecoMM_M --fd out_pp_ll_zd.root --ld 'data' --fb1 out_pp_ll_sm.root --lb1 'Drell-Yan' --wb1 1.8  --rebin 2 --xmin 30. --xmax 110.  --tx 'm_{#mu#mu} [GeV]' --ty 'number of events' --out plots/test; display plots/test.pdf

import argparse

#_____________________________________________________________________________
def options():
    parser = argparse.ArgumentParser(description="generic 1D data vs Background and signal")

    parser.add_argument('--h', dest='h', type=str, help='name of TH1', default='hpt')

    # files ...
    parser.add_argument('--fd', dest='fd', type=str, help='file containing pseudo data', default='histoD.root')
    parser.add_argument('--fs', dest='fs', type=str, help='file containing signal hypothesis', default='')
    parser.add_argument('--fb1', dest='fb1', type=str, help='file containing background hypothesis 1', default='histoB.root')
    parser.add_argument('--fb2', dest='fb2', type=str, help='file containing background hypothesis 2', default='')

    # labels
    parser.add_argument('--ld', dest='ld', type=str, help='label for TH1 in data file to be appeared in the legend', default='')    
    parser.add_argument('--ls', dest='ls', type=str, help='label for TH1 in signal file to be appeared in the legend', default='')    
    parser.add_argument('--lb1', dest='lb1', type=str, help='label for TH1 in bck1 file to be appeared in the legend', default='')    
    parser.add_argument('--lb2', dest='lb2', type=str, help='label for TH1 in bck2 file to be appeared in the legend', default='')    

    # labels
    parser.add_argument('--wd', dest='wd', type=float, help='weight for TH1 in data file to be appeared in the legend', default=1.)    
    parser.add_argument('--ws', dest='ws', type=float, help='weight for TH1 in signal file to be appeared in the legend', default=1.)    
    parser.add_argument('--wb1', dest='wb1', type=float, help='weight for TH1 in bck1 file to be appeared in the legend', default=1.)    
    parser.add_argument('--wb2', dest='wb2', type=float, help='weight for TH1 in bck2 file to be appeared in the legend', default=1.)    

    # general parameters
    parser.add_argument('--tx', dest='tx', type=str, help='title of x-axis', default='p_{T}')    
    parser.add_argument('--ty', dest='ty', type=str, help='title of y-axis', default='normalized event rate')    
    parser.add_argument('--cap_upr', dest='cap_upr', type=str, help='caption to appear in top right corner', default='')    
    
    # if commas are present text is distributed among various lines
    parser.add_argument('--cap_in', dest='cap_in', type=str, help='caption to appear in the canvas (separation with comma for multiple captions)', default='#sqrt{s} = 14 TeV, L = 10 pb^{-1}')    

    parser.add_argument('--xmin', dest='xmin', type=float, help='minimum x value')    
    parser.add_argument('--xmax', dest='xmax', type=float, help='maximum x value')    
    parser.add_argument('--ymin', dest='ymin', type=float, help='minimum y value')    
    parser.add_argument('--ymax', dest='ymax', type=float, help='maximum y value')    

    parser.add_argument('--log', dest='log', default=False, help='plot y-axis in log scale', action='store_true')
    parser.add_argument('--rebin', dest='rebin', type=int, help='rebin by amount specified', default=1)

    #parser.add_argument('--draw_opt', dest='draw_opt', type=str, help='specifiy root draw option', default='hist')

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


    # define stacked histo
    hStack = ROOT.THStack("hstack","")

    draw_option = 'same hist'

    legsize = 0.09
    ylegsize = legsize
    maxi = 0

    # if option 2 is defined
    max2 = 0
    if ops.fb1:
        hfileb1 = ROOT.TFile(ops.fb1)
        hb1 = hfileb1.Get(ops.h)
        hb1.SetTitle(ops.lb1)
        hb1.SetLineWidth(0)
        hb1.SetLineColor(29)
        hb1.SetFillColor(29)

        hb1.Scale(ops.wb1)
        hb1.Rebin(ops.rebin)

        max_ =  hb1.GetMaximum() 
        maxi = max(maxi, max_)
        ylegsize += legsize
        
        hStack.Add(hb1)
        
        #hb1.Draw(draw_option)

    # if option 3 is defined
    if ops.fb2:
        hfileb2 = ROOT.TFile(ops.fb2)
        hb2 = hfileb2.Get(ops.h)
        hb2.SetTitle(ops.lb2)
        hb2.SetLineWidth(0)
        hb2.SetLineColor(38)
        hb2.SetFillColor(38)
        hb2.Scale(ops.wb2)

        hb2.Rebin(ops.rebin)

        max_ =  hb2.GetMaximum() 
        maxi = max(maxi, max_)
        ylegsize += legsize

        #hb2.Draw(draw_option)
        hStack.Add(hb2)
        
        legsize += legsize

    if ops.fs:
        hfiles = ROOT.TFile(ops.fs)
        hs = hfiles.Get(ops.h)
        hs.SetTitle(ops.ls)
        hs.SetLineWidth(0)
        hs.SetFillColor(46)
	
        hs.Scale(ops.ws)

        hs.Rebin(ops.rebin)
        max_ =  hs.GetMaximum() 
        maxi = max(maxi, max_)
        ylegsize += legsize

        #hs.Draw(draw_option)

        hStack.Add(hs)
        legsize += legsize

    print 'pass', hStack

    hStack.Draw("hist")

    if ops.xmin is not None and ops.xmax is not None: 
       hStack.GetXaxis().SetRangeUser(ops.xmin, ops.xmax)

    # get data files
    hfiled = ROOT.TFile(ops.fd)
    
    # get and initialize histos
    hd = hfiled.Get(ops.h)
    hd.SetTitle(ops.ld)
    hd.SetLineWidth(3)
    hd.SetLineColor(ROOT.kBlack)
    hd.SetMarkerSize(0.5)
    hd.SetMarkerStyle(8)
    hd.SetTitle('')
    hd.Scale(ops.wd)

    max_ =  hd.GetMaximum() 
    maxi = max(maxi, max_)

    hd.Rebin(ops.rebin)

    # set histogram boundaries
    hd.Draw("same E")

    if not ops.ymax:
       if not ops.log:
           hStack.SetMaximum(maxi*1.5)
       else:
           hStack.SetMaximum(maxi*100.)
    else:
       hStack.SetMaximum(ops.ymax)


    if not ops.ymin:
       if not ops.log:
           hStack.SetMinimum(0.)
       else:
           print 'here'
	   hStack.SetMinimum(10.)
    else:
       hStack.SetMinimum(ops.ymin)

    hStack.GetXaxis().SetTitle(ops.tx)
    hStack.GetYaxis().SetTitle(ops.ty)
    #hStack.GetYaxis().SetTitleOffset(1.75)
    #hStack.GetXaxis().SetTitleOffset(1.40)
    hStack.GetYaxis().SetTitleOffset(1.6)
    hStack.GetXaxis().SetTitleOffset(1.05)
    hStack.GetXaxis().SetTitleSize(0.045)
    hStack.GetYaxis().SetTitleSize(0.045)

    print 'set maxima and minima', ops.log

    # build legend
    leg = TLegend(0.58,0.86-legsize,0.90,0.86)
    leg.AddEntry(hd,ops.ld,"lep")
    if ops.fs:
        leg.AddEntry(hs,ops.ls,"f")
    if ops.fb1:
        leg.AddEntry(hb1,ops.lb1,"f")
    if ops.fb2:
        leg.AddEntry(hb2,ops.lb2,"f")

    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.Draw() 

    print 'building legend'

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

    print 'writing text'

    # this happens only if additional text
    if len(rt)>2:
        text = '#it{#bf{' + rt[2] +'}}'
        if 'ell' in text:
           text = text.replace('#','\\')
        Text.SetTextSize(0.03) 
        Text.DrawLatex(0.30, 0.70, text)

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

    print 'canvas updating'

    pdir = os.path.dirname(ops.out)
    name = os.path.basename(ops.out)
    filename = pdir + '/' + name
    
    if not os.path.exists(pdir):
       os.makedirs(pdir)
    
    #canvas.Print('{}.png'.format(filename), 'png')
    #canvas.Print('{}.eps'.format(filename), 'eps')
    canvas.Print('{}.pdf'.format(filename), 'pdf')

#______________________________________________________________________________
if __name__ == '__main__': 
    main()

import ROOT, sys
from ROOT import TFile, TH1F, TGraphErrors, TMultiGraph, TLegend, TF1,gROOT
import math

c = ROOT.TCanvas("", "", 600, 600)
ROOT.gROOT.SetBatch(True)

font = 132

colors = []
colors.append(ROOT.kBlue);
colors.append(ROOT.kBlue);
colors.append(ROOT.kAzure+4);
colors.append(ROOT.kAzure+4);

colors.append(ROOT.kRed);
colors.append(ROOT.kRed);
colors.append(ROOT.kOrange+2);
colors.append(ROOT.kOrange+2);

styles = []
styles.append(7)
styles.append(1)
styles.append(7)
styles.append(1)
styles.append(7)
styles.append(1)
styles.append(7)
styles.append(1)

'''filename = sys.argv[1]
fs = sys.argv[2]
step = sys.argv[3]
var  = sys.argv[4]'''
#____________________________________________________
def myStyle():
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetPadBorderMode(0)

    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetPadColor(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetTitleColor(1)
    ROOT.gStyle.SetStatColor(0)

    # set the paper & margin sizes
    ROOT.gStyle.SetPaperSize(20,26)
    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadRightMargin(0.03)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.125)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetTextFont(42) #132
    ROOT.gStyle.SetTextSize(0.09)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.045,"xyz") #0.035
    ROOT.gStyle.SetTitleSize(0.045,"xyz")
    ROOT.gStyle.SetTitleOffset(1.15,"y")

    # use bold lines and markers
    ROOT.gStyle.SetMarkerStyle(8)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetLineWidth(1)
    #ROOT.gStyle.SetLineStyleString(2,"[12 12]") // postscript dashes

    # do not display any of the standard histogram decorations
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetOptStat(0) #("m")
    ROOT.gStyle.SetOptFit(0)

    #ROOT.gStyle.SetPalette(1,0)
    ROOT.gStyle.cd()
    ROOT.gROOT.ForceStyle()
#_____________________________________________________________________________________________________

def printResoHisto(histo, f, tag):
   c = ROOT.TCanvas(histo.GetName(), "", 600, 600)
   ROOT.gPad.SetLeftMargin(0.20) ;
   ROOT.gPad.SetRightMargin(0.05) ;
   ROOT.gPad.SetBottomMargin(0.20) ;
   ROOT.gStyle.SetOptStat(0000000);
   ROOT.gStyle.SetTextFont(132);
   ROOT.gStyle.SetOptStat(0000000)
   c.cd()
   histo.SetLineWidth(3)
   histo.Draw('hist')
   f.SetLineWidth(3)
   f.Draw('same')

   histo.SetMaximum(1.6*histo.GetMaximum())
   histo.SetMinimum(0.)
   #histo.GetXaxis().SetRangeUser(0., 1.5)
   histo.GetXaxis().SetRangeUser(0., 6.0)

   histo.GetYaxis().SetLabelFont(132)
   histo.GetYaxis().SetTitleFont(132)
   histo.GetXaxis().SetLabelFont(132)
   histo.GetXaxis().SetTitleFont(132)

   histo.GetXaxis().SetTitleOffset(1.2)
   histo.GetYaxis().SetTitleOffset(1.2)
   histo.GetXaxis().SetLabelOffset(0.02)
   histo.GetYaxis().SetLabelOffset(0.02)
   histo.GetXaxis().SetTitleSize(0.06)
   histo.GetYaxis().SetTitleSize(0.06)
   histo.GetXaxis().SetLabelSize(0.06)
   histo.GetYaxis().SetLabelSize(0.06)
   histo.GetXaxis().SetNdivisions(505)
   histo.GetYaxis().SetNdivisions(505)

   '''
   ptext = ROOT.TPaveText(0.21,0.55,0.52,.87)

   ptext.AddText("{} pile-up".format(pu))
   if pucorr: ptext.AddText("#rho correction")
   else: ptext.AddText("no #rho correction")
   ptext.AddText("anti-k_{{T}}, R = {}".format(r))
   ptext.AddText("p_{{T}} = {} GeV".format(pttext))

   ptext.SetTextFont(132)
   ptext.SetTextSize(0.035)
   ptext.SetFillColor(0)
   ptext.SetFillStyle(0)
   ptext.SetLineColor(0)
   ptext.SetBorderSize(1)
   ptext.Paint('NDC')
   ptext.Draw()
   '''


   ROOT.gStyle.SetOptFit()
   ps = histo.GetListOfFunctions().FindObject("stats")
   ps.SetX1NDC(0.60)
   ps.SetX2NDC(0.95)
   ps.SetY1NDC(0.70)
   ps.SetY2NDC(0.90)
   c.Modified()
   c.Update()

   histo.GetXaxis().SetTitle('m^{reco} / m^{gen}')

   name = 'plots/'+histo.GetName()+'_'+tag
   plotname = name+'.png'
   c.Print(plotname)
   #plotname = name+'.pdf'
   #c.Print(plotname)
   #plotname = name+'.eps'
   #c.Print(plotname)


#_____________________________________________________________________________________________________
def drawMultiGraphResp(mg, name, lt, rt, pdir, xmin, xmax, ymin, ymax, logx, logy, bl, fs):

    #myStyle()
    ROOT.gStyle.SetOptStat(0000000)

    canvas = ROOT.TCanvas(name, '', 600,600)

    ROOT.gPad.SetLeftMargin(0.20) ;
    ROOT.gPad.SetRightMargin(0.05) ;
    ROOT.gPad.SetBottomMargin(0.20) ;
    ROOT.gStyle.SetOptStat(0000000);
    ROOT.gStyle.SetOptFit(000000)
    #ROOT.gStyle.SetTextFont(132);

    Tright = ROOT.TLatex(0.23, 0.92, rt)
    Tright.SetNDC(ROOT.kTRUE)
    Tright.SetTextSize(0.044)
    #Tright.SetTextFont(132)

    Tleft = ROOT.TPaveText(0.23,0.75, 0.50,0.89, 'NDC')
    #for txt in lt:
    Tleft.AddText(lt)
    #Tleft.SetTextFont(132)
    #Tleft.SetTextSize(0.044)
    Tleft.SetFillColor(0)
    Tleft.SetFillStyle(0)
    Tleft.SetLineColor(0)
    Tleft.SetBorderSize(1)
    Tleft.Paint('NDC')
    Tleft.Draw()

    canvas.cd(0)

    if logx: ROOT.gPad.SetLogx()
    if logy: ROOT.gPad.SetLogy()


    leg = ROOT.TLegend(0.62,0.68,0.92,0.88)
    #leg.SetTextFont(132)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)

    # fit stuff
    textsfit = []
    if fs:
        shift = 0.10
        mg.Draw("AP")
        k = 0
        listofgraphs = mg.GetListOfGraphs()
        for f in fs:
           #if k > 0: break
           strA = '{:.2f}'.format(f.GetParameter(0))
           strB = '{:.2f}'.format(f.GetParameter(1))
           strC = '{:.2f}'.format(f.GetParameter(2))
           strD = '{:.2f}'.format(f.GetParameter(3))

           ngr = listofgraphs[k].GetTitle()
           fittext = 'R(p_{T}) = #frac{C + D p_{T}}{A + B p_{T}}, '+ ngr

           fittext = fittext.replace('A', strA)
           fittext = fittext.replace('B', strB)
           fittext = fittext.replace('C', strC)
           fittext = fittext.replace('D', strD)
           xcor = 0.50
           ycor = 0.8 - k*shift
           Tfit = ROOT.TLatex(xcor, ycor, fittext)
           Tfit.SetNDC(ROOT.kTRUE)
           Tfit.SetTextSize(0.03)
           Tfit.SetTextFont(132)
           Tfit.SetTextColor(colors[k])
           f.SetLineColor(colors[k])
           f.SetLineWidth(3)
           f.Draw('same')
           #Tfit.Draw('same')

           leg.AddEntry(f,ngr,"l");
           textsfit.append(Tfit)
           k += 1
    else:
       mg.Draw("ALP")

    '''for t in textsfit:
       t.Draw()
    '''

    leg.Draw('same')

    mg.GetYaxis().SetLabelFont(132)
    mg.GetYaxis().SetTitleFont(132)
    mg.GetYaxis().SetLabelOffset(0.015)
    mg.GetYaxis().CenterTitle()
    #mg.GetYaxis().SetNdivisions(505)
    #mg.GetXaxis().SetNdivisions(505)
    mg.GetYaxis().SetTitleOffset(1.4)

    mg.GetXaxis().SetTitleFont(132)
    mg.GetXaxis().SetLabelFont(132)
    mg.GetXaxis().SetLabelOffset(0.02)
    mg.GetXaxis().SetTitleOffset(1.5)
    mg.GetXaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetXaxis().SetLabelSize(0.06)
    mg.GetYaxis().SetLabelSize(0.06)
    mg.GetXaxis().SetRangeUser(xmin, xmax)
    mg.SetMinimum(ymin)
    mg.SetMaximum(ymax)


    '''if bl:
        leg = canvas.BuildLegend(0.62,0.68,0.92,0.88)
        leg.SetTextFont(132)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.Draw()
    '''
    Tleft.Draw()
    Tright.Draw()

    #canvas.Print('{}/{}.png'.format(pdir, name), 'png')
    canvas.Print('{}/{}.pdf'.format(pdir, name), 'pdf')
    #canvas.Print('{}/{}.eps'.format(pdir, name), 'eps')
#-----------------------------------------------------------------------------------------------------

def drawMultiGraphReso(mg, name, lt, rt, pdir, xmin, xmax, ymin, ymax, logx, logy, bl, fs):

    #myStyle()
    ROOT.gStyle.SetOptStat(0000000)

    canvas = ROOT.TCanvas(name, '', 600,600)

    ROOT.gPad.SetLeftMargin(0.20) ;
    ROOT.gPad.SetRightMargin(0.05) ;
    ROOT.gPad.SetBottomMargin(0.20) ;
    ROOT.gStyle.SetOptStat(0000000);
    ROOT.gStyle.SetOptFit(000000)
    ROOT.gStyle.SetTextFont(132);

    Tright = ROOT.TLatex(0.23, 0.92, rt)
    Tright.SetNDC(ROOT.kTRUE)
    Tright.SetTextSize(0.044)
    Tright.SetTextFont(132)

    Tleft = ROOT.TPaveText(0.23,0.75, 0.50,0.89, 'NDC')
    #for txt in lt:
    Tleft.AddText(lt)
    Tleft.SetTextFont(132)
    #Tleft.SetTextSize(0.044)
    Tleft.SetFillColor(0)
    Tleft.SetFillStyle(0)
    Tleft.SetLineColor(0)
    Tleft.SetBorderSize(1)
    Tleft.Paint('NDC')
    Tleft.Draw()

    canvas.cd(0)

    if logx: ROOT.gPad.SetLogx()
    if logy: ROOT.gPad.SetLogy()

    leg = ROOT.TLegend(0.62,0.68,0.92,0.88)
    leg.SetTextFont(132)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)



    # fit stuff
    textsfit = []
    if fs:
        shift = 0.12
        mg.Draw("AP")
        k = 0
        listofgraphs = mg.GetListOfGraphs()
        for f in fs:
           strA = '{:.0f}'.format(f.GetParameter(0))
           strB = '{:.0f}'.format(f.GetParameter(1))
           ngr = listofgraphs[k].GetTitle()

           fittext = '#frac{#sigma(p_{T})}{p_{T}} = #frac{A%}{#sqrt{p_{T}}} #oplus B%, '+ngr

           fittext = fittext.replace('A', strA)
           fittext = fittext.replace('B', strB)
           xcor = 0.55
           ycor = 0.8 - k*shift
           Tfit = ROOT.TLatex(xcor, ycor, fittext)
           Tfit.SetNDC(ROOT.kTRUE)
           Tfit.SetTextSize(0.035)
           Tfit.SetTextFont(132)
           Tfit.SetTextColor(colors[k])
           f.SetLineColor(colors[k])
           f.SetLineWidth(3)
           f.Draw('same')
           #Tfit.Draw('same')
           leg.AddEntry(f,ngr,"l");
           textsfit.append(Tfit)
           k += 1


    else:
       mg.Draw("ALP")

    '''for t in textsfit:
       t.Draw()'''

    leg.Draw('same')

    mg.GetYaxis().SetLabelFont(132)
    mg.GetYaxis().SetTitleFont(132)
    mg.GetYaxis().SetLabelOffset(0.015)
    mg.GetYaxis().CenterTitle()
    mg.GetYaxis().SetNdivisions(505)
    mg.GetXaxis().SetNdivisions(505)
    mg.GetYaxis().SetTitleOffset(1.4)

    mg.GetXaxis().SetTitleFont(132)
    mg.GetXaxis().SetLabelFont(132)
    mg.GetXaxis().SetLabelOffset(0.02)
    mg.GetXaxis().SetTitleOffset(1.5)
    mg.GetXaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetXaxis().SetLabelSize(0.06)
    mg.GetYaxis().SetLabelSize(0.06)
    mg.GetXaxis().SetRangeUser(xmin, xmax)
    mg.SetMinimum(ymin)
    mg.SetMaximum(ymax)


    if bl:
        leg = canvas.BuildLegend(0.62,0.68,0.92,0.88)
        leg.SetTextFont(132)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.Draw()

    Tleft.Draw()
    Tright.Draw()

    #canvas.Print('{}/{}.png'.format(pdir, name), 'png')
    canvas.Print('{}/{}.pdf'.format(pdir, name), 'pdf')
    #canvas.Print('{}/{}.eps'.format(pdir, name), 'eps')

#-----------------------------------------------------------------------------------------------------

def drawMultiGraph(mg, name, lt, rt, pdir, xmin, xmax, ymin, ymax, logx, logy, bl,  form):

    #myStyle()
    ROOT.gStyle.SetOptStat(0000000)

    canvas = ROOT.TCanvas(name, '', 600,600)

    ROOT.gPad.SetLeftMargin(0.20) ;
    ROOT.gPad.SetRightMargin(0.05) ;
    ROOT.gPad.SetBottomMargin(0.20) ;
    ROOT.gStyle.SetOptStat(0000000);
    ROOT.gStyle.SetOptFit(000000)
    #ROOT.gStyle.SetTextFont(132);

    Tright = ROOT.TLatex(0.23, 0.92, rt)
    Tright.SetNDC(ROOT.kTRUE)
    Tright.SetTextSize(0.044)
    #Tright.SetTextFont(132)

    Tleft = ROOT.TPaveText(0.23,0.75, 0.50,0.89, 'NDC')
    #for txt in lt:
    Tleft.AddText(lt)
    #Tleft.SetTextFont(132)
    #Tleft.SetTextSize(0.044)
    Tleft.SetFillColor(0)
    Tleft.SetFillStyle(0)
    Tleft.SetLineColor(0)
    Tleft.SetBorderSize(1)
    Tleft.Paint('NDC')
    Tleft.Draw()

    canvas.cd(0)

    if logx: ROOT.gPad.SetLogx()
    if logy: ROOT.gPad.SetLogy()

    leg = ROOT.TLegend(0.62,0.68,0.92,0.88)
    #leg.SetTextFont(132)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)

    mg.Draw("ALP")

    '''for t in textsfit:
       t.Draw()'''
    leg.Draw('same')

    #mg.GetYaxis().SetLabelFont(132)
    #mg.GetYaxis().SetTitleFont(132)
    mg.GetYaxis().SetLabelOffset(0.015)
    mg.GetYaxis().CenterTitle()
    #mg.GetYaxis().SetNdivisions(505)
    #mg.GetXaxis().SetNdivisions(505)
    mg.GetYaxis().SetTitleOffset(1.5)

    #mg.GetXaxis().SetTitleFont(132)
    #mg.GetXaxis().SetLabelFont(132)
    mg.GetXaxis().SetLabelOffset(0.02)
    mg.GetXaxis().SetTitleOffset(1.5)
    mg.GetXaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetXaxis().SetLabelSize(0.06)
    mg.GetYaxis().SetLabelSize(0.06)
    mg.GetXaxis().SetRangeUser(xmin, xmax)
    mg.SetMinimum(ymin)
    mg.SetMaximum(ymax)


    leg = canvas.BuildLegend(0.62,0.68,0.92,0.88)
    leg.SetTextFont(132)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.Draw()

    Tleft.Draw()
    Tright.Draw()

    #canvas.Print('{}/{}.png'.format(pdir, name), 'png')
    canvas.Print('{}/{}.{}'.format(pdir, name, form), '{}'.format(form))
    #canvas.Print('{}/{}.eps'.format(pdir, name), 'eps')


#_____________________________________________________________________________

def getEffSigma( theHist, wmin=0.2, wmax=1.8, step=0.001, epsilon=0.007 ):
#def getEffSigma( theHist, wmin=0.1, wmax=2.8, step=0.0002, epsilon=0.005 ):
  point = wmin
  weight = 0.
  points = [] #vector<pair<double,double> >
  thesum = theHist.Integral(0, theHist.GetNbinsX()+1)
  for i in range(theHist.GetNbinsX()):
    weight += theHist.GetBinContent(i)
    if weight > epsilon:
      points.append( [theHist.GetBinCenter(i),weight/thesum] )
  low = wmin
  high = wmax

  width = wmax-wmin
  for i in range(len(points)):

    #print i, points[i][0], points[i][1]
    for j in range(i,len(points)):

      wy = points[j][1] - points[i][1]
      if abs(wy-0.683) < epsilon:
      #if abs(wy-0.5) < epsilon:

        wx = points[j][0] - points[i][0]
        if wx < width:
          low = points[i][0]
          high = points[j][0]

          #print points[j][0], points[i][0], wy, wx

          width=wx

  return 0.5*(high-low)


#_____________________________________________________________________________

def getEfficiency( theHist, cutmin=0.2, cutmax=1.8):
  thesum = theHist.Integral()

  thefficientsum=0
  for i in range(theHist.GetNbinsX()):
    x = theHist.GetBinCenter(i)

    if x > cutmin and x < cutmax:
        thefficientsum += theHist.GetBinContent(i)

  efficiency = -1
  if thesum > 0:
     efficiency = thefficientsum/thesum

  return efficiency


#_______________________________________________________________________


filename = sys.argv[1]
tag = sys.argv[2]

gauss=False

label = 'VBF'
pu = 0
typlot = 'reso'



ptbins = [(200.,300.), (300.,500.), (500.,1000.)]
#ptbins = [(200.,300.)]

ptbins = [(200.,250.), (250.,300.), (300., 400.), (400., 500.)]

#ptbins = [ (300., 400.), (400., 500.), (500., 750.), (750., 1000.)]
ptbins = [ (300., 400.), (400., 500.), (500., 750.), (750., 1000.)]

mus = dict()
sigs = dict()

effs = dict()
effs2 = dict()

labels = dict()

names = []
masses = ['sd','reg']
processes = ['higgs_cc', 'higgs_bb', 'qcd_qq', 'qcd_cc', 'qcd_bb']
processes = ['higgs_bb', 'higgs_cc', 'higgs_qq', 'qcd_bb', 'qcd_cc', 'qcd_qq']

#processes = ['higgs_cc', 'qcd_cc']


#processes = ['higgs_qq', 'higgs_cc', 'higgs_bb', 'qcd_qq', 'qcd_cc', 'qcd_bb']
#processes = ['higgs_cc', 'higgs_bb', 'qcd_cc', 'qcd_bb']
algos=dict()
procs=dict()


bin_sig_def='m100.0_150.0'
bin_bg_def ='m0.0_1000.0'


for ptbin in ptbins:

    rebin = 50

    #ptbin='pt200.0_300.0'
    ptb='pt{}_{}'.format(ptbin[0],ptbin[1])

    bin_sig='{}_{}'.format(ptb,bin_sig_def)
    bin_bg ='{}_{}'.format(ptb,bin_bg_def)


    for process in processes:
        for m in masses:

            name='hd{}_{}_{}'.format(m,process,bin_sig)
            #name='hd{}_{}_pt300.0_500.0_m100.0_150.0'.format(m,process)
            #name='hd{}_{}_pt200.0_100000.0_m0.0_1000.0'.format(m,process)
            names.append(name)

            label=''

            if 'higgs' in name and 'cc' in name:
                label += 'H -> cc'

            elif 'higgs' in name and 'bb' in name:
                label += 'H -> bb'

            elif 'higgs' in name and 'qq' in name:
                label += 'H -> qq'

            elif 'qcd' in name and 'cc' in name:
                label += 'QCD (c)'

            elif 'qcd' in name and 'bb' in name:
                label += 'QCD (b)'

            elif 'qcd' in name and 'qq' in name:
                label += 'QCD (l)'

            if 'sd' in name:
               label += '  (soft drop)'
            elif 'reg' in name:
               label += '  (regression)'

            labels[name] = label

            procs[label]=process
            algos[label]=m

for name in names:
        hfile = ROOT.TFile(filename)

        histname = name
        hist = hfile.Get(histname)

        #histo = hist.Clone()
        histo = hist
        print histname
        histo.SetName(histname)
        fname = 'f{}'.format(histname)

        mus[name]    = (-1., -1)
        sigs[name]   = (-1., -1)
        effs[name]   = -1.
        effs2[name]  = -1.

        if histo.Integral() > 0:
          histo.Scale(1/histo.Integral())
          histo.Rebin(rebin)


          ## extract place where maximum is
          x0 = histo.GetXaxis().GetBinCenter(histo.GetMaximumBin())
          d = histo.GetRMS()

          # now perform gaussian fit in [x_max_sigm, x_max_sigp]
          f = ROOT.TF1(fname, 'gaus',0.0, 6.0)

          s = 1.0
          histo.Fit(fname, 'Q', '', x0 - s*d, x0 + s*d)
          #print histo, f
          #printResoHisto(histo, f, tag)

          mus[name]  = (f.GetParameter(1), f.GetParError(1))
          sigs[name] = (f.GetParameter(2) / f.GetParameter(1), f.GetParError(2) / f.GetParameter(1))

          sigma_fit = f.GetParameter(2) / f.GetParameter(1)

          if not gauss:
             mus[name]  = (x0, 0.)
             sigma= getEffSigma(histo , wmin=0., wmax=2.0, step=0.0002, epsilon=0.001 )
             sigs[name] = (sigma /x0,0.)
             sigma_eff = sigma

          stddev = sigs[name][0]
          mpv = mus[name][0]

          #mpv = f.GetParameter(1)
          #stddev = d

          effs[name] = getEfficiency(histo, cutmin=0.4, cutmax=999.)
          effs2[name] = getEfficiency(histo, cutmin=mpv-2.*stddev, cutmax=mpv+2.*stddev)

          if 'hdsd_higgs_cc' in name:
              print '        ', name, mpv, sigma_fit, sigma_eff, effs2[name]
          #print '        ', name, sigs[name][0], sigs[name][1]


for name in names:
    hfile = ROOT.TFile(filename)
    histname = name

    if 'qcd_cc' in name or 'qcd_bb' in name or 'qcd_qq' in name:
        histname2 = histname.replace('hd','h')
        histname2 = histname2.replace(bin_sig_def,bin_bg_def)

        hist2 = hfile.Get(histname2)
        hist2.Rebin(rebin)

        name_higgs = name.replace('qcd','higgs')

        stddev = sigs[name_higgs][0]
        mpv = mus[name_higgs][0]

        cmin=125.*(mpv - 2*stddev)
        cmax=125.*(mpv + 2*stddev)

        print name, histname2, name_higgs
        print mpv*125, stddev*125
        print cmin, cmax

        effs[name] = getEfficiency(hist2, cutmin=50. ,cutmax=9999999.)
        effs2[name] = getEfficiency(hist2, cutmin=cmin ,cutmax=cmax)

        print effs2[name]

        '''
        for algo in ['sd','reg']:
            for ptbin in ptbins:
                ptb='pt{}_{}'.format(ptbin[0],ptbin[1])

                if algo in name and ptb in name:
                    thename=''
                    for name2 in names:
                        for fs in ['cc','bb']:
                            if fs in name2 and algo in name2 and ptb in name2:
                                thename=name2
                                break

                            print histname2, thename

                            stddev = sigs[thename][0]
                            mpv = mus[thename][0]


                            cmin=125.*(mpv - 2*stddev)
                            cmax=125.*(mpv + 2*stddev)

                            #print mpv , stddev
                            #print cmin, cmax
                            effs[name] = getEfficiency(hist2, cutmin=50. ,cutmax=9999999.)
                            effs2[name] = getEfficiency(hist2, cutmin=cmin ,cutmax=cmax)
                            #print mpv , stddev
                            #print cmin, cmax
                            #print effs2[name]
         '''





### print( performance table

print( "")
print( "{0:>20s} {1:>11s} {2:>13s} {3:>25s} {4:>25s}".format("process (mass)", "mu", "sigma/mu", "eff. (mH > 50 GeV)", "eff. ( mH +/- 2 sigma)"))
print( "-----------------------------------------------------------------------------------------------------------------------------------------")

eps_sig_sd = 1.
eps_sig_reg = 1.
eps_bkg_sd = 1.
eps_bkg_reg = 1.



n=0
for name in names:

    if 'qcd_qq' in name: continue
    if n%2==0:
        #print name
        print( '')
    print( "{0:22} {1:10.2f} {2:10.2f} {3:20.2f} {4:20.2f}".format(labels[name], mus[name][0], sigs[name][0], effs[name], effs2[name]))

    '''
    effSD =

    if

    if n%2==0:
        print 'Gain: {:.2f}'.format(),

    '''

    n+=1

mg_resp_pt = ROOT.TMultiGraph()
mg_resp_pt.SetTitle(";p_{T} [GeV]; mass response")

mg_eff_pt = ROOT.TMultiGraph()
mg_eff_pt.SetTitle(";p_{T} [GeV]; efficiency (#mu +/- 2#sigma cut)")

mg_reso_pt = ROOT.TMultiGraph()
mg_reso_pt.SetTitle(";p_{T} [GeV]; #sigma_{eff}(m) / m")


i=0
for kname in names:

    name = labels[kname]

    if '(l)' in name or 'qq' in name: continue
    if i > 7: break



    reso_pt = ROOT.TGraph()
    reso_pt.SetLineColor(colors[i])
    reso_pt.SetLineStyle(styles[i])
    reso_pt.SetFillColor(0)
    reso_pt.SetLineWidth(4)
    reso_pt.SetMarkerSize(0)
    reso_pt.SetMarkerColor(colors[i])
    reso_pt.SetTitle(name)

    resp_pt = ROOT.TGraph()
    resp_pt.SetLineColor(colors[i])
    resp_pt.SetLineStyle(styles[i])
    resp_pt.SetFillColor(0)
    resp_pt.SetLineWidth(4)
    resp_pt.SetMarkerSize(0)
    resp_pt.SetMarkerColor(colors[i])
    resp_pt.SetTitle(name)

    eff_pt = ROOT.TGraph()
    eff_pt.SetLineColor(colors[i])
    eff_pt.SetLineStyle(styles[i])
    eff_pt.SetFillColor(0)
    eff_pt.SetLineWidth(4)
    eff_pt.SetMarkerSize(0)
    eff_pt.SetMarkerColor(colors[i])
    eff_pt.SetTitle(name)

    i += 1

    point = 0

    for pt in ptbins:

         ptval = 0.5*(float(pt[0])+float(pt[1]))

         #print pt[0],pt[1]
         ptbin='pt{}_{}'.format(pt[0],pt[1])
         bin_sig='{}_m100.0_150.0'.format(ptbin)

         #print algos[name]
         #print procs[name]
         #print bin_sig

         key='hd{}_{}_{}'.format(algos[name],procs[name],bin_sig)
         print name, ptval, sigs[key][0]

         reso_pt.SetPoint(point,ptval,sigs[key][0])
         resp_pt.SetPoint(point,ptval,mus[key][0])
         eff_pt.SetPoint(point,ptval,effs2[key])

         print name,ptval,sigs[key][0], effs2[key]

         point+=1

    mg_reso_pt.Add(reso_pt)
    mg_resp_pt.Add(resp_pt)
    mg_eff_pt.Add(eff_pt)

drawMultiGraph(mg_reso_pt, 'reso_pt_{}'.format(tag), '', '', 'plots', 0., 2000., 0., 0.5, False, False, False, 'png')
drawMultiGraph(mg_resp_pt, 'resp_pt_{}'.format(tag), '', '', 'plots', 0., 2000., 0.80, 1.30, False, False, False, 'png')
drawMultiGraph(mg_eff_pt, 'eff_pt_{}'.format(tag), '', '', 'plots', 0., 2000., 0.0, 1.50, False, False, False, 'png')


mg_gain_pt = ROOT.TMultiGraph()
mg_gain_pt.SetTitle(";p_{T} [GeV]; #frac{significance(reg)}{significance(SD)}")


i=0
#for fs in ['bb', 'cc', 'qq']:
for fs in ['bb', 'cc']:

    name = 'H #rightarrow {}'.format(fs)

    gain_pt = ROOT.TGraph()
    gain_pt.SetLineColor(colors[2*i])
    gain_pt.SetLineStyle(1)
    gain_pt.SetFillColor(0)
    gain_pt.SetLineWidth(4)
    gain_pt.SetMarkerSize(0)
    gain_pt.SetMarkerColor(colors[2*i])
    gain_pt.SetTitle(name)

    i += 1
    point = 0

    for pt in ptbins:

         ptval = 0.5*(float(pt[0])+float(pt[1]))
         ptbin='pt{}_{}'.format(pt[0],pt[1])
         bin_sig='{}_m100.0_150.0'.format(ptbin)


         key_sig_sd = 'hdsd_higgs_{}_{}_m100.0_150.0'.format(fs,ptbin)
         key_bkg_sd = 'hdsd_qcd_{}_{}_m100.0_150.0'.format(fs,ptbin)
         key_sig_reg = 'hdreg_higgs_{}_{}_m100.0_150.0'.format(fs,ptbin)
         key_bkg_reg = 'hdreg_qcd_{}_{}_m100.0_150.0'.format(fs,ptbin)

         print fs, ptval, effs2[key_bkg_reg] , effs2[key_sig_sd], point
         gain = math.sqrt(effs2[key_bkg_sd] / effs2[key_bkg_reg]) * effs2[key_sig_reg] / effs2[key_sig_sd]

         #print 'gain: ', fs, ptval, gain
         gain_pt.SetPoint(point,ptval,gain)
         point+=1

    mg_gain_pt.Add(gain_pt)

#drawMultiGraph(mg_gain_pt, 'gain_pt_{}'.format(tag), '', '', 'plots', 0., 500., 0.9, 1.7, False, False, False)
drawMultiGraph(mg_gain_pt, 'gain_pt_{}'.format(tag), '', '', 'plots', 0., 2000., 0.8, 1.5, False, False, False, 'png')


#____  VS PT_________________________


'''
mg_reso_pt = ROOT.TMultiGraph()
mg_reso_pt.SetTitle(";p_{T} [GeV]; jet resolution (%)")

mg_resp_pt = ROOT.TMultiGraph()
mg_resp_pt.SetTitle(";p_{T} [GeV]; response")

fresps = []
fresos = []
i = 0

for det in ['HF', 'Nose']:

    reso_pt = ROOT.TGraphErrors()
    reso_pt.SetLineColor(colors[i])
    reso_pt.SetLineStyle(styles[i])
    reso_pt.SetFillColor(0)
    reso_pt.SetLineWidth(4)
    reso_pt.SetMarkerColor(colors[i])

    resp_pt = ROOT.TGraphErrors()
    resp_pt.SetLineColor(colors[i])
    resp_pt.SetLineStyle(styles[i])
    resp_pt.SetFillColor(0)
    resp_pt.SetLineWidth(4)
    resp_pt.SetMarkerColor(colors[i])

    title = det
    if det == 'Nose':
        title = 'HF-Nose'

    #print title
    reso_pt.SetTitle(title)
    resp_pt.SetTitle(title)

    i += 1
    point = 0

    for pt in ptbins:
      key = (pt,r)
      if mus[name]  > 0. and sigs[name] > 0.:

         #print key, mus[name], sigs[name]

         #if key == ((20,50),0.4) and not pucorr: continue
         pterr = 0.5*(pt[1]-pt[0])

         pt = 0.5*(pt[0]+pt[1])

         reso_pt.SetPoint(point,pt,sigs[name][0])
         reso_pt.SetPointError(point,0.,sigs[name][1])
         #reso_pt.SetPointError(point,pterr,sigs[key][1])

         resp_pt.SetPoint(point,pt,mus[name][0])
         resp_pt.SetPointError(point,0.,mus[name][1])
         #resp_pt.SetPointError(point,pterr,mus[key][1])

         point += 1

    fresp = ROOT.TF1('reso', '([0]+[1]*x)/([2]+[3]*x)',0.0, 10000.0)
    #fresp = ROOT.TF1('reso', '1.0',0.0, 10000.0)
    fresp.SetParameter(0,0)
    fresp.SetParameter(1,1)
    fresp.SetParameter(2,0)
    fresp.SetParameter(3,1)

    if r == 0.1 and typlot == 'resp' and not pucorr:
        fresp.SetParLimits(0,-6.1,-5.9)
        fresp.SetParLimits(1,0.99,1.01)
        fresp.SetParLimits(2,-8.1,-7.9)
        fresp.SetParLimits(3,1.19,1.21)


    resp_pt.Fit(fresp, '', '', 5.0, 5000.0)

    freso = ROOT.TF1('reso', 'sqrt([1]^2/x + [2]^2)',0.0, 10000.0)
    #freso.SetParLimits(0,0,100)
    freso.SetParLimits(0,0,1000)
    freso.SetParLimits(1,0,1000)
    reso_pt.Fit(freso, '', '', 20.0, 5000.0)

    fresps.append(fresp)
    fresos.append(freso)

    mg_reso_pt.Add(reso_pt)
    mg_resp_pt.Add(resp_pt)

rt = 'anti-k_{T}'
#lt = 'QCD, #sqrt{{s}} = 14 TeV, {} PU'.format(pu)
rt = '{} jets, anti-k_{{T}} R = 0.2, #sqrt{{s}} = 14 TeV, {} PU'.format(label,pu)
lt = ''
name_reso = '{}_reso_pt_{}pu'.format(label,pu)
name_resp = '{}_resp_pt_{}pu'.format(label,pu)

if typlot == 'resp':
   if not pucorr:
       pname = 'resp_nocorr'
       print pname
       lt = 'no #rho correction'
       drawMultiGraphResp(mg_resp_pt, pname, lt, rt, 'plots_nose', 20, 5000., 0., 6., False, False, False, fresps)
   else:
       pname = 'resp_corr'
       lt = '#rho correction'
       drawMultiGraphResp(mg_resp_pt, pname, lt, rt, 'plots_nose', 20, 5000., 0., 2., False, False, False, fresps)
else:
   if not pucorr:
       pname = 'reso_nocorr'
       print pname
       lt = ''
       drawMultiGraphReso(mg_reso_pt, pname, lt, rt, 'plots_nose', 0., 150., 0., 50., False, False, False, fresos)
   else:
       pname = 'reso_corr'
       lt = '#rho correction'
       drawMultiGraphReso(mg_reso_pt, pname, lt, rt, 'plots_nose', 0., 500., 0., 40., False, False, False, fresos)

#if pucorr: drawMultiGraphResp(mg_resp_pt, name_resp, lt, rt, 'plots_nose', 20, 5000., 0., 2., True, False, False, fresps)
#else : drawMultiGraphResp(mg_resp_pt, name_resp, lt, rt, 'plots_nose', 20, 5000., 0., 6., True, False, False, fresps)
#drawMultiGraphReso(mg_rtyplot == 'resp'eso_pt, name_reso, lt, rt, 'plots_nose', 0., 500., 0., 40., False, False, False, fresos)
'''

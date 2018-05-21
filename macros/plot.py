from ROOT import *
import optparse
import os

#python macros/plot.py -d scankl_hmaa_mhh_resg_2.9_effg_95_fake_1_btag_1_bkg_1_syst_1HHttH

eospath='/eos/experiment/fcc/hh/analyses/hhbbaa_combine/'
#eospath='/afs/cern.ch/user/g/gortona/public/4Michele/lotsOfStuff_v0/'
eospath='/afs/cern.ch/user/g/gortona/public/4Michele/lotsOfStuff/'

#define function for parsing options
def parseOptions():

    nominal='scankl_hmaa_mhh_resg_1.3_effg_95_fake_1_btag_1_bkg_1_syst_1HH'
    #default_file1=os.path.join(eospath,nominal)

    usage = ('usage: %prog [options] datasetList\n'+ '%prog -h for help')
    parser = optparse.OptionParser(usage)
    #parser.add_option('-v', '--var', dest='var', type='string', default="kl", help='variable (kl, r)')
    #parser.add_option('-w', '--which', dest='what', type='int', default=3, help='which plot 1D/2D and vars')
    parser.add_option('-s', '--stop', dest='stop', type='int', default=1, help='stop at the end to see the plot')
    parser.add_option('-u', '--first', dest='fileuno', type='string', default=nominal)
    parser.add_option('-d', '--second', dest='filedue', type='string', default="")
    parser.add_option('-t', '--third', dest='filetre', type='string', default="")
    parser.add_option('-q', '--quattro', dest='filequattro', type='string', default="")
    parser.add_option('--ymax', dest='ymax', type=float, default=-1)

#    parser.add_option('-n', '--nuis', dest='nuis', type='int', default=1, help='use nuisances')
#    parser.add_option('-p', '--suffixoptions', dest='options', type='string', default="_", help='options used to run (p,k)')
    global opt, args
    (opt, args) = parser.parse_args()

def goodName(which,number):
	if which == "syst" :
		if number == "noSyst" : return "stat. only"
		elif "1HHttH" in number : return "#delta_{S}/S = #delta_{ttH}/ttH = 1%"
		elif "2HHttH" in number : return "#delta_{S}/S = #delta_{ttH}/ttH = 2%"
		elif "1HH" in number : return "#delta_{S}/S = 1%"
	elif which == "bkg" : return "all bkg #times "+number
	elif which == "btag" :
		if number == "1" : return "85% b-tag eff."
		else : return "75% b-tag eff."
	elif which == "fake" : return "fake rate #times "+number
	elif which == "effg" : return "#varepsilon_{#gamma} = "+number+"%"
	elif which == "resg" : return "#delta(m_{#gamma#gamma}) = "+number+" GeV"

def badName(which,number):
	if which == "syst" : return number
	elif which == "bkg" : return "bkgx"+number
	elif which == "btag" : 
		if number == "1" : return "btag085"
		else : return "btag075"
	elif which == "fake" : return "fakex"+number
	elif which == "effg" : return "effg0"+number
	elif which == "resg" : return "resg"+number


parseOptions()
global opt, args
if "scankl" in opt.fileuno : variable = "kl"
else : variable="r"

if opt.stop == 0:
    gROOT.SetBatch(True)

allVars = []
files = []
allVars.append(opt.fileuno.split("_"))

file1=eospath+"higgsCombine"+opt.fileuno+".MultiDimFit.mH120.root"
file2=eospath+"higgsCombine"+opt.filedue+".MultiDimFit.mH120.root"
file3=eospath+"higgsCombine"+opt.filetre+".MultiDimFit.mH120.root"
file4=eospath+"higgsCombine"+opt.filequattro+".MultiDimFit.mH120.root"


files.append(TFile.Open(file1))
if len(opt.filedue.split("_"))>2 :
	allVars.append(opt.filedue.split("_"))
	files.append(TFile.Open(file2))
	if len(opt.filetre.split("_"))>2 :
		allVars.append(opt.filetre.split("_"))
		files.append(TFile.Open(file3))
		if len(opt.filequattro.split("_"))>2 :
			allVars.append(opt.filequattro.split("_"))
			files.append(TFile.Open(file4))

print files

leg = []
out = [] 
if len(allVars) > 1:
	wordsD = allVars[1]
	wordsU = allVars[0]
	for icheck in range(len(allVars[0])) :
		if wordsD[icheck] != wordsU[icheck]:
			leg.append(goodName(wordsD[icheck-1],wordsU[icheck]))
			leg.append(goodName(wordsD[icheck-1],wordsD[icheck]))
			out.append(badName(wordsD[icheck-1],wordsU[icheck]))
			out.append(badName(wordsD[icheck-1],wordsD[icheck]))
			if len(allVars)>2 : 
				leg.append(goodName(wordsD[icheck-1],allVars[2][icheck]))
				out.append(badName(wordsD[icheck-1],allVars[2][icheck]))
				if len(allVars)>3 : 
					leg.append(goodName(wordsD[icheck-1],allVars[3][icheck]))
					out.append(badName(wordsD[icheck-1],allVars[3][icheck]))
else:
	leg.append("Stat. Only")
	out.append("StatOnly")


trees = []
for il in range(len(files)):
	trees.append(files[il].Get("limit"))	

graphs = []

for i in range(len(trees)) : 
	graphs.append(TGraph(0))
	graphs[i].SetFillStyle(0)
	
	graphs[i].SetMarkerSize(0)
	# tgraph name
	graphs[i].SetName(leg[i])
	#graphs[i].SetBorderSize(0)


	ipoint =0
	for event in trees[i] :
		if event.deltaNLL > 6 : continue
		if variable == "kl" :
#			if whichplot is not 4 and ( event.kl<0.9 or event.kl>1.1 ): continue
#			if whichplot == 4 :
#				if event.kl<0.95 and event.kl>0.9 : continue
#				if event.kl<1.15 and event.kl>1.02 : continue
			graphs[i].SetPoint(ipoint,event.kl, 2*event.deltaNLL)
		else :
#			if event.r<0.9 or event.r>1.1 : continue
			graphs[i].SetPoint(ipoint,event.r, 2*event.deltaNLL)
		ipoint+=1
	graphs[i].Sort()
	graphs[i].SetTitle("")
	if variable == "r" : graphs[i].GetXaxis().SetTitle("r = #sigma_{obs}/#sigma_{SM}")
	else : graphs[i].GetXaxis().SetTitle("k_{#lambda} = #lambda_{obs}/#lambda_{SM}")
	graphs[i].GetYaxis().SetTitle("-2#Delta ln L")
	graphs[i].SetLineWidth(3)


# actual plotting
c = TCanvas("c","c",600,600)
c.SetTicks(1,1)
c.SetLeftMargin(0.14)
c.SetRightMargin(0.08)
#c.SetGridx()
#c.SetGridy()


graphs[0].SetLineColor(kBlue)
graphs[0].SetMarkerColor(kBlue)

if len(opt.filedue.split("_"))>2 :
    graphs[1].SetLineColor(kRed+1)
    graphs[1].SetMarkerColor(kRed+1)
    
if len(opt.filetre.split("_"))>2 :
    graphs[2].SetLineColor(kGreen+2)
    graphs[2].SetMarkerColor(kGreen+2)
    
if len(opt.filequattro.split("_"))>2 :
    graphs[3].SetLineColor(kPink+2)
    graphs[2].SetMarkerColor(kGreen+2)


#graphs[0].GetXaxis().SetTitleOffset(0.8)
#graphs[0].GetYaxis().SetTitleOffset(1.1)
graphs[0].GetYaxis().SetTitleOffset(1.75)
graphs[0].GetXaxis().SetTitleOffset(1.35)
graphs[0].GetXaxis().SetTitleSize(0.035)
graphs[0].GetYaxis().SetTitleSize(0.035)

graphs[0].Draw("AL")
if len(opt.filedue.split("_"))>2 :graphs[1].Draw("LSAME")
if len(opt.filetre.split("_"))>2 :graphs[2].Draw("LSAME")
if len(opt.filequattro.split("_"))>2 :graphs[3].Draw("LSAME")


if opt.ymax != -1:
    graphs[0].SetMaximum(opt.ymax)
else:
    graphs[0].SetMaximum(graphs[0].GetYaxis().GetXmax()*1.3)

# draw legend
legsize = 0.055*float(len(trees))
legend = TLegend(0.53,0.88 - legsize,0.88,0.85)
legend.SetFillColor(0)
#legend.SetFillStyle(0)
legend.SetLineColor(0)
legend.SetShadowColor(10)
legend.SetTextSize(0.030)
legend.SetTextFont(42)

for i in range(len(trees)) : 
    legend.AddEntry(graphs[i],leg[i],"l")
legend.Draw()


# draw 1-sigma line
xmin = graphs[0].GetXaxis().GetXmin()
xmax = graphs[0].GetXaxis().GetXmax()

line = TLine(xmin,1,xmax,1)
line.SetLineColor(kBlack)
line.SetLineStyle(2)
line.SetLineWidth(4)
line.Draw("SAME")

line2 = TLine(xmin,3.82,xmax,3.82)
line2.SetLineColor(kBlack)
line2.SetLineStyle(2)
line2.SetLineWidth(4)
line2.Draw("SAME")

rangex = xmax-xmin
posx = xmax - rangex/9.0

Text = TLatex()
Text.SetTextAlign(12)
Text.SetTextSize(0.04) 
text = '1 #sigma'
Text.DrawLatex(posx,1.6, text) 

text = '2 #sigma'
Text.DrawLatex(posx,4.4, text) 



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
Text.Draw()

Text2 = TPaveText(0.18, 0.71,0.4,0.85,'brNDC')
rightText = re.split(",")#, rightText)
text = '#bf{#it{' + rightText[0] +'}}'
Text2.SetTextAlign(12);
#Text.SetNDC(True) 
Text2.SetTextSize(0.036) 
Text2.AddText(text)
text = '#bf{#it{' + rightText[1] +'}}'
Text2.AddText(text)
#Text2.SetFillStyle(0)
Text2.SetFillColor(kWhite)
Text2.SetLineStyle(0)
Text2.SetBorderSize(0)
Text2.Draw()

Text3 = TPaveText(0.37, 0.55, 0.67, 0.65,'brNDC')
text = '#bf{#it{HH#rightarrow bb#gamma#gamma}}'
if 'boosted' in opt.fileuno:
    text = '#bf{#it{HH#rightarrow bbbbj}}' 


Text3.SetTextAlign(22);
Text3.SetTextSize(0.045) 
Text3.AddText(text)
#Text2.SetFillStyle(0)
Text3.SetFillColor(kWhite)
Text3.SetLineStyle(0)
Text3.SetBorderSize(0)
Text3.Draw()



#Text.DrawLatex(0.18, 0.78, rightText[1])
c.RedrawAxis()
#c.Update()
c.GetFrame().SetBorderSize( 12 )
c.Modified()
c.Update()

#c.SaveAs(titles[whichplot]+appString+variable+opt.options+".pdf")
#c.SaveAs(titles[whichplot]+appString+variable+opt.options+".root")
outString = "plot"
for legs in out : outString += variable+legs
c.SaveAs(outString+".pdf")
#c.SaveAs(outString+".root")

if opt.stop > 0 :raw_input()

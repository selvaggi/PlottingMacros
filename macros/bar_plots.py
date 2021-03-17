import ROOT as r

mode="27"
#mode="100"
#mode="27_100"

bbaa      = ["bb#gamma#gamma",
              [5., 7.],  #  27 TeV ->   1, 15, 100 ab-1
              [15.,22.,26.]] # 100 TeV -> 2.5, 30, 100 ab-1
bbtata    = ["bb#tau#tau",
              [10.,15.],
              [36.,40.,43.]]
bb4l      = ["bbZZ(4l)",
              [12.,22.],
              [16.,23.,27.]]
bbbb    = ["bbbb",
              [32.,42.],
              [10.,18.,22.]]
bbWW       = ["bbWW(lq)",
              [40.,60.],
              [33.,43.,47.]]

database=[
bbWW,
bbbb,
bb4l,
bbtata,
bbaa,
]

nAna=len(database)
nbins = (3*nAna)
if mode=="27" or mode=="100": nbins = (2*nAna)
h_27=[]
h_27.append( r.TH1D("h_27_1", "h_27_1", nbins,0.,nbins))
h_27.append( r.TH1D("h_27_2", "h_27_2", nbins,0.,nbins))
h_27.append( r.TH1D("h_27_3", "h_27_3", nbins,0.,nbins))
h_100=[]
h_100.append(r.TH1D("h_100_1","h_100_1",nbins,0.,nbins))
h_100.append(r.TH1D("h_100_2","h_100_2",nbins,0.,nbins))
h_100.append(r.TH1D("h_100_3","h_100_3",nbins,0.,nbins))

nMax=len(h_100)-1

color  = [[r.kYellow-7, r.kAzure-9], [r.kRed+1, r.kBlue+1], [r.kGray+3, r.kGray+2]]
legend = [["1 ab^{-1}", "2.5 ab^{-1}"], ["15 ab^{-1}", "30 ab^{-1}"], ["100 ab^{-1}", "100 ab^{-1}"]]

process = [database[0][0],database[1][0],database[2][0],database[3][0],database[4][0]]
val27   = [database[0][1],database[1][1],database[2][1],database[3][1],database[4][1]]
val100  = [database[0][2],database[1][2],database[2][2],database[3][2],database[4][2]]

count = 1
count_ana = 0
for i_bin in xrange( 1, nbins+1 ):
  if count==4 : count=1
  if count==1 :
    if mode=="27" :
      for i in xrange( 0, nMax ) : h_27[i].SetBinContent(i_bin, val27[count_ana][i])
      count+=1
    elif mode=="100" :
      for i in xrange( 0, nMax+1 ) : h_100[i].SetBinContent(i_bin, val100[count_ana][i])
      count+=1
    else :
      for i in xrange( 0, nMax+1 ) : h_27[i].SetBinContent(i_bin, val27[count_ana][i])
  if count==2 :
    for i in xrange( 0, nMax+1 ) :
      h_100[i].SetBinContent(i_bin, val100[count_ana][i])
  #
  if mode=="27_100" :
    str_27   = '#scale[0.75]{#sqrt{s} = 27 TeV}'
    str_100  = '#scale[0.75]{#sqrt{s} = 100 TeV}'
    if count==1 : h_100[nMax].GetXaxis().SetBinLabel(i_bin,str_27)
    if count==2 : h_100[nMax].GetXaxis().SetBinLabel(i_bin,str_100)
    if count==3 :
      str_proc = '#scale[1.02]{#font[22]{'+process[count_ana]+'}}'
      h_100[nMax].GetXaxis().SetBinLabel(i_bin,str_proc)
      count_ana+=1
  else :
    if count==2 :
      str_proc = '#scale[1.02]{#font[22]{'+process[count_ana]+'}}'
      if mode=="27"  : h_27[nMax].GetXaxis().SetBinLabel(i_bin,str_proc)
      if mode=="100" : h_100[nMax].GetXaxis().SetBinLabel(i_bin,str_proc)
      count_ana+=1
  count+=1

for i in xrange( 0, nMax+1 ) :
  alpha=0.42
  if i==0: alpha=0.8
  if i==nMax: alpha=0.15
  #
  h_27[i].SetLineColorAlpha(color[i][0],0.)
  h_27[i].SetFillColorAlpha(color[i][0],alpha)
  h_27[i].SetMarkerColorAlpha(color[i][0],0.)
  h_100[i].SetLineColorAlpha(color[i][1],0.)
  h_100[i].SetFillColorAlpha(color[i][1],alpha)
  h_100[i].SetMarkerColorAlpha(color[i][0],0.)

canvas = r.TCanvas("test", "test", 600, 600)
canvas.SetTicks(1,1)
canvas.SetLeftMargin(0.21)
canvas.SetRightMargin(0.02)
r.gStyle.SetOptStat(0)
r.gPad.SetGridx()

leg = r.TLegend(0.73,0.52,0.98,0.70)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetShadowColor(10)
leg.SetTextSize(0.035)
leg.SetTextFont(42)

if mode=="27" :
  the_max=h_27[nMax].GetMaximum()
  h_27[nMax].SetMaximum(the_max*1.1)
  h_27[nMax].SetTitle("")
  h_27[nMax].GetYaxis().SetTitleOffset(1.30)
  h_27[nMax].GetYaxis().SetTitle("#delta#kappa_{#lambda} / #kappa_{#lambda} (%)")
  h_27[nMax].GetXaxis().SetLabelSize(0.05)
  h_27[nMax].GetXaxis().SetTickLength(0.)

  h_27[nMax].Draw("hbar")
  for i in xrange( nMax, -1, -1 ) :
    h_27[i].Draw("hbarsame")

  for i in xrange( 0, nMax+1 ) :
    leg.AddEntry(h_27[i],legend[i][0])
  leg.Draw("same")

else :
  the_max=h_100[nMax].GetMaximum()
  h_100[nMax].SetMaximum(the_max*1.1)
  h_100[nMax].SetTitle("")
  h_100[nMax].GetYaxis().SetTitleOffset(1.30)
  h_100[nMax].GetYaxis().SetTitle("Mass scale [TeV]")
  h_100[nMax].GetXaxis().SetLabelSize(0.05)
  h_100[nMax].GetXaxis().SetTickLength(0.)
  
  h_100[nMax].Draw("hbar")
  for i in xrange( nMax, -1, -1 ) :
    h_100[i].Draw("hbarsame")
    if mode=="27_100" : h_27[i].Draw("hbarsame")
  
  for i in xrange( 0, nMax+1 ) :
    if mode=="27_100" and i!=nMax : leg.AddEntry(h_27[i],legend[i][0])
    leg.AddEntry(h_100[i],legend[i][1])
  leg.Draw("same")

Text = r.TLatex()
Text.SetNDC()
Text.SetTextAlign(31);
Text.SetTextSize(0.033)
text = '5 #sigma Discovery'
Text.DrawLatex(0.95, 0.72, text)

leftText27      = "HE-LHC Simulation (Delphes), #sqrt{s} = 27 TeV"
leftText100     = "FCC-hh Simulation (Delphes), #sqrt{s} = 100 TeV"
leftText27_100  = "FCC-hh / HE-LHC Simulation (Delphes)"
Text.SetTextAlign(31);
Text.SetTextSize(0.04)
if mode=="27"    : Text.DrawLatex(0.97, 0.92, '#it{' + leftText27     +'}')
elif mode=="100" : Text.DrawLatex(0.97, 0.92, '#it{' + leftText100    +'}')
else             : Text.DrawLatex(0.97, 0.92, '#it{' + leftText27_100 +'}')

canvas.RedrawAxis()
canvas.RedrawAxis("g");
canvas.GetFrame().SetBorderSize( 12 )
canvas.Modified()
canvas.Update()

extra=""
if mode=="27"  : extra="_onlyHELHC"
if mode=="100" : extra="_onlyFCChh"
canvas.Print("summaryDisco"+extra+".pdf")


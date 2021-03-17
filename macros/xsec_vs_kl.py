import os, ROOT
import itertools
from ROOT import TGraphErrors, gROOT
import json

kls = [
       0.99,
       1.10,
      ]
kls = [
       0.00,
       0.20,
       0.40,
       0.60,
       0.70,
       0.80,
       0.85,
       0.90, 
       0.92, 
       0.94, 
       0.96, 
       0.97, 
       0.98, 
       0.99, 
       1.00, 
       1.01, 
       1.02, 
       1.03, 
       1.04, 
       1.06, 
       1.08, 
       1.10,
       1.20,
       1.30,
       1.40,
       1.45,
       1.50,
       1.55,
       1.60,
       1.70,
       1.80,
       1.90,
       2.00,
       2.20,
       2.40,
       2.60,
       2.80,
       3.00
]
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
    
    mg.Draw("a3")

    mg.GetXaxis().SetTitleSize(0.035)
    mg.GetYaxis().SetTitleSize(0.035)
    
    mg.GetXaxis().SetRangeUser(xmin, xmax)

    mg.GetYaxis().SetTitleOffset(1.75)
    mg.GetXaxis().SetTitleOffset(1.35)

    mg.SetMinimum(ymin)
    mg.SetMaximum(ymax)
    
    if log: ROOT.gPad.SetLogy()

    if bl:
        leg = canvas.BuildLegend(0.55,0.65,0.88,0.86)
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

    text = '#bf{#it{' + rt +'}}'
    
    Text.SetTextAlign(22);
    Text.SetNDC(ROOT.kTRUE) 
    Text.SetTextSize(0.04) 
    Text.DrawLatex(0.35, 0.78, text)
    
    
    canvas.RedrawAxis()
    canvas.Update()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()
 
    canvas.Print('{}.pdf'.format(fname), 'pdf')
    canvas.Print('{}.png'.format(fname), 'png')

#------------------------------------------------------------------------------------------------------------------------

def produceGraph(process, index):

     
    xs = []
    ys = []
    yerr = []

    title=process.label
    xs = list((process.xsecs).keys())
    ys = list((process.xsecs).values())

    #print x,y
   
    xs.sort() 
    gr = ROOT.TGraphErrors()
    gr.SetTitle(title)

    gr.SetLineColor(colors[index])
    gr.SetLineWidth(3)
    gr.SetMarkerSize(0.)
    gr.SetMarkerColor(colors[index])
    gr.SetFillColor(colors[index])
    i=0
    '''
    for k, xs in itertools.izip(x,y):
        print i, k, float(xs)
        gr.SetPoint(i,float(k),float(xs))

        gr.SetPointError(i,0.,0.)
        i+=1
    '''

    for x in xs:
        xsec = float(process.xsecs[x])
        abserr = process.err * xsec
        print i, x, 
        gr.SetPoint(i,float(x),xsec)
        gr.SetPointError(i,0., abserr )
        i+=1

    return gr 
#____________________________________________________________________________________________________________________________

eosdir='/eos/experiment/fcc/hh/generation/lhe/'

#________________________________________________
class process:
   def __init__(self, name, cfgname, label, kfact, err):
       self.name = name
       self.cfgname = cfgname
       self.label = label
       self.kfact = kfact
       self.err = err
       self.xsecs = dict()
       self.errs = dict()

   def fill_xsec_and_error(self,k,xsec,err):
       self.xsecs[k]=float(xsec)*self.kfact
       self.errs[k]=err

   def xsec(self):
       return self.xsecs

   def err(self):
       return self.errs
#_________________________________________________

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

#_________________________________________________

vhh   = process('mg_pp_vhh', 'VHH', 'VHH (V=W^{#pm},Z)', 1.400158, 0.078)
tthh  = process('mg_pp_tthh', 'ttHH','t#bar{t}HH', 1.378155, 0.042)
vbfhh = process('mg_pp_vbfhh', 'VBF HH (qq->jjHH)', 'VBF HH', 1.147188, 0.021)
gghh  = process('pw_pp_hh', 'gg->HH (NLO)', 'gg #rightarrow HH', 1.075363, 0.032)

processes = []
processes.append(gghh)
processes.append(vbfhh)
processes.append(tthh)
processes.append(vhh)

os.system('mkdir -p data')
os.system('mkdir -p hhxsec100TeV')

fillDicts = False
#fillDicts = True

paramString="'DUMMYPROCESS':['DUMMYNAME','inclusive','','DUMMYXSEC','DUMMYKFACT','1.0'],\n"
paramlist=''

if fillDicts:
    for proc in processes:
	#print proc.name 
	for k in kls:
	    #procdir=eosdir+
	    procname=proc.name + '_lambda{:03d}_5f'.format(int(k*100)) 
	    procdir=eosdir+procname
	    #print procdir
	    if not os.path.isdir(procdir):
		 print '{} does not exist ...'.format(procdir)
		 continue
     
	    foundLHE=False

            xsec_av = 0.
            nlhes = 0
	    for fname in os.listdir(procdir):
		if fname.endswith('.lhe.gz'):
		    #print fname
		    lhefile=procdir +'/'+fname
		    if os.stat(lhefile).st_size > 0:
			print 'found non-empty LHE file:', lhefile
			foundLHE=True
			
			# now copy file locally
			cmdcp = 'xrdcp -N -v root://eospublic.cern.ch/{} data/events.lhe.gz'.format(lhefile)
			os.system(cmdcp)
			os.system('gunzip data/events.lhe.gz')
			
			# extract cross section here
			with open ('data/events.lhe', 'rt') as myfile: 
			    contents = myfile.read()             
			    #print(contents) 
			    start='<init>'
			    end='</init>'
			    
			    init_block=contents.split(start)[1].split(end)[0]
			    #print init_block
			    init_block_params = init_block.split()
			    #print init_block_params

			    xsec = init_block_params[10]
			    err = init_block_params[11]
                            xsec_av += float(xsec)
                            nlhes+= 1
                            print 'Reading xsec = {} +/- {}'.format(xsec,err) 
			os.system('rm data/events.lhe') 
			#break

            # apparently no need since all LHE files seem to have same cross-section
            if nlhes >0:
                xsec_av=xsec_av/float(nlhes)

                paramStr = paramString 
                paramStr = paramStr.replace('DUMMYPROCESS', procname)
                paramStr = paramStr.replace('DUMMYNAME', proc.cfgname)
                paramStr = paramStr.replace('DUMMYXSEC', str(xsec_av))
                paramStr = paramStr.replace('DUMMYKFACT', str(proc.kfact))
		
                print paramStr 
                paramlist += paramStr
 
	        proc.fill_xsec_and_error(k,xsec_av,err)        
                with open('hhxsec100TeV/{}.json'.format(proc.name), 'w') as file:
	            file.write(json.dumps(proc.__dict__)) # use `json.loads` to do the reverse


print ''
print ''
print paramlist
print ''
print ''


mgContour = ROOT.TMultiGraph()
mgContour.SetTitle(";#kappa_{#lambda} = #lambda_{3} / #lambda_{3}^{SM}; #sigma_{100 TeV} (p p #rightarrow H H) [pb]")

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

index=0
for proc in processes:
    with open('hhxsec100TeV/{}.json'.format(proc.name), 'r') as file:
        proc_dict = json.load(file)
        #print proc_dict
        proc_struct = Struct(**proc_dict)
        #print proc_struct.name, proc_struct.xsecs

        if proc_struct.name == 'mg_pp_vhh': proc_struct.err = 0.078
        if proc_struct.name == 'mg_pp_tthh': proc_struct.err = 0.042
        if proc_struct.name == 'mg_pp_vbfhh': proc_struct.err = 0.021
        if proc_struct.name == 'pw_pp_hh': proc_struct.err = 0.032

        gr = produceGraph(proc_struct, index)
        mgContour.Add(gr)
        index+=1

lt='FCC-hh simulation'
rt='#sqrt{s} = 100 TeV'
fname = 'xsec_vs_klambda'

ymin = 0.001
ymax = 100.
xmax = 0.
xmin = 3.
log= True

'''
ymin = 0.0
ymax = 3.0
xmax = 3.
xmin = 0.
log= False
'''
drawMultiGraph(mgContour, 'xsec', lt, rt, fname, ymin, ymax, xmin, xmax, log, True)

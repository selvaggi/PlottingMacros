import os

pts=[500,1000, 2000, 5000, 10000]

path = '/afs/cern.ch/work/s/selvaggi/private/JetClustering/batch/'

#variables = ['reco/reco_massSD', 'reco/reco_massRec', 'reco/reco_massTrimmed', 'reco/reco_tau21']
variables = ['reco/reco_mass']


type = ['res','old']

for pt in pts:

    for var in variables:

        for t in type:
	    
	        f1= '{}/FccmZ{}_{}/out/FccmZ{}_{}.root'.format(path,pt,t,pt,t)
		f2= '{}/FccmW{}_{}/out/FccmW{}_{}.root'.format(path,pt,t,pt,t)
		f3= '{}/Fccml{}_{}/out/Fccml{}_{}.root'.format(path,pt,t,pt,t)

        	varstr = var.replace("reco/reco_","")
		cmd= "python macros/var1D.py  --f1 {} --h1 {} --l1 'Z jet'  --f2 {} --h2 {} --l2 'W jet'  --f3 {} --h3 {} --l3 'QCD jet' --ty 'normalized event rate'  --tx 'm_{{jet}} [GeV]' --cap_in 'p_{{T}}^{{jet}} > {} \;GeV , ,' --cap_upr 'FCC-hh Simulation' --out plots/{}_{}_{} --draw_opt 'hist' --norm --xmin 0.0 --xmax 200 --rebin 8".format(f1,var,f2,var,f3,var,pt,varstr, t, pt)

        	print cmd

        	os.system(cmd)
    

import os


kls = [
       0.00,
       1.00, 
       1.50,
       2.00,
       3.00
       ]


processes=[
'mgp8_pp_vhh',
'mgp8_pp_vbfhh',
'mgp8_pp_tthh',
'pwp8_pp_hh',
]


eosdir='/eos/user/s/selvaggi/heppyTrees/hhgen/'
treename ='FCChhAnalyses.FCChh.hhgen.TreeProducer.TreeProducer_1/tree.root'
outdir='hhgen_plots'

for process in processes:
    for k in kls:
         
        lambdastr='lambda{:03d}_5f'.format(int(k*100))
	cmd = 'python readTree.py {}/{}_{}_hhbbbb/{} {}/{}_{}.root'.format(eosdir,process,lambdastr,treename,outdir,process,lambdastr)
        print cmd
        os.system(cmd)

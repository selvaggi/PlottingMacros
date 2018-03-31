PlottingMacros
==============

1D Histogram plotter
--------------------

Plots two histograms in the canvas. Type ```python macros/var1D.py --help``` for more options. Example:


```
python macros/var1D.py  --f1 files/histo_h4mu_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_h4mu_13tev.root --h2 eta1 --l2 '13 TeV' --tx '\eta_{\ell}^{max}' --xmin 0. --xmax 8.0 --norm --cap_in ', , gg #to H #to 4#ell' --cap_upr 'FCC-hh Simulation' --out plots/etalep
```

```
python macros/var1D.py  --f1 files/histo_vbf_100tev.root --h1 eta1 --l1 '100 TeV'  --f2 files/histo_vbf_13tev.root --h2 eta1 --l2 '13 TeV' --tx '#eta_{j}^{max}' --xmin 0. --xmax 8 --norm --cap_in 'p_{T}^{jet} > 25 GeV, , VBF Higgs' --cap_upr 'FCC-hh Simulation' --out plots/vbfjet
```


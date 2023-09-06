import ROOT, sys
from ROOT import TFile, TH1F, TGraphErrors, TMultiGraph, TLegend, TF1, gROOT
import math
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy

from utils import *



fname = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHjjjj_v2/histos//histo.root"
#fname = "/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/histos//histo.root"
#fname = "histo.root"

processes = []

zhjjjj = {
    "filename":"/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHjjjj_v2/histos//histo.root",
    "name":"zhjjjj",
    "label":r"ZH $\rightarrow$ jjjj events",
    "xrange_s1":(70,150),
    "xrange_s2":(30,120),
    "xlabel_s1": r"$m_H$ [GeV]",
    "xlabel_s2": r"$m_Z$ [GeV]",
}
zhssss = {
    "filename":"/eos/experiment/fcc/ee/generation/DelphesStandalone/ColorSingletPythia8_ZHssss_v2/histos//histo.root",
    "name":"zhssss",
    "label":r"ZH $\rightarrow$ ssss events",
    "xrange_s1":(100,150),
    "xrange_s2":(50,110),
    "xlabel_s1": r"$m_H$ [GeV]",
    "xlabel_s2": r"$m_Z$ [GeV]",
   
}

vvWWjjjj = {
    "filename":"histo.root",
    "name":"vvWWjjjj",
    "label":r"ZH $\rightarrow$ vvWW*$\rightarrow$ jjjj events",
    "xrange_s1":(50,110),
    "xrange_s2":(0,50),
    "xlabel": r"$m_H$ [GeV]",
    "xlabel_s1": r"$m_W$ [GeV]",
    "xlabel_s2": r"$m_{W^{*}}$ [GeV]",   
}



#processes.append(zhjjjj)
processes.append(zhssss)
#processes.append(vvWWjjjj)

for proc in processes:
    s1_ideal = {
        "filename": proc["filename"],
        "histname": "hmass_S1_ideal",
        "label": "ideal",
        "color": "firebrick"
    
    }
    s1_fastjet = {
        "filename": proc["filename"],
        "histname": "hmass_S1_fjcombzh",
        "label": "N=4 jets",  
        "color": "dodgerblue", 
    }
    
    data_s1 = []
    data_s1.append(s1_ideal)
    data_s1.append(s1_fastjet)

    ### compute resolutions and generate corresponding text
    resolutions = dict()

    text = []
    text_events =  {
        "content": proc["label"],
        "location": (0.65, 0.92), 
    }

    text.append(text_events)

    ref_text = (0.6,0.5)
    ymax = -1
    for d in data_s1:
        filename = d["filename"]
        file = ROOT.TFile(filename)
        hname = d["histname"]
        hist = file.Get(hname)
        d["resolution"] = getEffSigma(hist, wmin=0., wmax=200, epsilon=0.01)
        print(d["label"], d["resolution"])

        text_sigma = {
            "content": r"$\sigma = {:.1f}$ GeV".format(d["resolution"]),
            "location": ref_text,
            "color": d["color"]
        }
        text.append(text_sigma)
        ref_text = (ref_text[0]+0.1, ref_text[1]-0.3)   

    
    plot_s1 = {
        "data": data_s1,
        "name": "{}_s1".format(proc["name"]),
        "outdir": "/eos/user/s/selvaggi/www/colorsinglet/",
        "title_x": proc["xlabel_s1"],
        "title_y": "event fraction",
        "yscale": "linear",
        "text": text,
        "leg_loc": "upper left",
        "normalize": True,
        "option": "hist",
        "ymin": 0,   
        "ymax": "auto",
        "xmin": proc["xrange_s1"][0],
        "xmax": proc["xrange_s1"][1],
        "linewidth": 2,
        #"rebin": 2,
        "grid":False
    }

    plotHistograms(plot_s1)

    data_s2 = copy.deepcopy(data_s1)
    data_s2[0]["histname"] = "hmass_S2_ideal"
    data_s2[1]["histname"] = "hmass_S2_fjcombzh"

    plot_s2 = copy.deepcopy(plot_s1)
    plot_s2["data"] = data_s2
    plot_s2["name"] = "{}_s2".format(proc["name"])
    plot_s2["title_x"] = proc["xlabel_s2"]

    text = []
    text_events =  {
        "content": proc["label"],
        "location": (0.65, 0.92), 
    }

    text.append(text_events)
    ref_text = (0.35,0.5)
    for d in data_s2:
        filename = d["filename"]
        file = ROOT.TFile(filename)
        hname = d["histname"]
        hist = file.Get(hname)
        d["resolution"] = getEffSigma(hist, wmin=0., wmax=200, epsilon=0.01)
        print(d["label"], d["resolution"])

        text_sigma = {
            "content": r"$\sigma = {:.1f}$ GeV".format(d["resolution"]),
            "location": ref_text,
            "color": d["color"]
        }
        text.append(text_sigma)
        ref_text = (ref_text[0]-0.1, ref_text[1]-0.3)

    plot_s2["text"] = text
    plot_s2["xmin"] = proc["xrange_s2"][0]
    plot_s2["xmax"] = proc["xrange_s2"][1]

    plotHistograms(plot_s2)

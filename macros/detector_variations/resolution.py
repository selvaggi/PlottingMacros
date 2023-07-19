import ROOT, sys
from ROOT import TFile, TH1F, TGraphErrors, TMultiGraph, TLegend, TF1, gROOT
import math
from collections import OrderedDict
from utils import *

from pltconfig import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# _______________________________________________________________________________
""" main """


observables = [
    {"name": "mass_norm", "label": r"$M_{vis} [GeV]$", "title": "visible mass"},
    # {"name": "evis", "label": r"$E_{vis}$ [GeV]", "title": "visible energy"},
]

variables = [
    {
        "name": "pcut",
        "histn": "p",
        "label": r"$p_{min}$ [GeV]",
    },
]


resolution_plots = []
for variable in variables:
    for observable in observables:
        for metric in metrics:
            resolution_plots.append(
                {
                    "name": "{}_{}_{}".format(
                        observable["name"], metric["name"], variable["name"]
                    ),
                    "observable": observable,
                    "variable": variable,
                    "metric": metric,
                    "title_x": variable["label"],
                    "title_y": metric["label"],
                    "yscale": "linear",
                    "leg_loc": "upper left",
                }
            )


collection = "ecal"
detector = "idea"

datasets = dict()
for sample in samples:
    for variable in variables:
        for observable in observables:
            filename = sample["filename"]
            file = ROOT.TFile(filename)

            x = []
            mu = []
            sig = []

            dataset_name = "{}_{}_{}_{}_{}".format(
                sample["name"],
                observable["name"],
                detector,
                collection,
                variable["name"],
            )
            for key in file.GetListOfKeys():
                histname_prefix = "h{}_{}_{}_{}_".format(
                    observable["name"],
                    detector,
                    collection,
                    variable["name"],
                )

                if histname_prefix in key.GetName():

                    hname = key.GetName()
                    hist = file.Get(hname)
                    hist.Rebin(2)

                    xval = float(hname.split("_")[-1])
                    x.append(xval)
                    # if x > 0: break

                    ## extract place where maximum is
                    mode = hist.GetXaxis().GetBinCenter(hist.GetMaximumBin())
                    mu.append(mode)

                    ## extract resolution
                    sigma = getEffSigma(hist, wmin=0.0, wmax=2.0, epsilon=0.01)
                    # sigma = getFWHM(hist) / 2.35

                    print(hname, mode, sigma)
                    if mode > 0:
                        sig.append(sigma / mode)
                    else:
                        print("Did not find histogram maximum ...")
                        sig.append(sigma)

            df = pd.DataFrame({variable["name"]: x, "response": mu, "resolution": sig})
            df.name = dataset_name
            print(df.name)
            print(df)
            datasets[dataset_name] = df


plt.rcParams.update({"font.size": 15})
for plot in resolution_plots:
    fig, ax = plt.subplots()
    for sample in samples:
        sample_name = sample["name"]
        observable_name = plot["observable"]["name"]
        variable_name = plot["variable"]["name"]
        dataset_name = "{}_{}_{}_{}_{}".format(
            sample["name"],
            observable["name"],
            detector,
            collection,
            variable["name"],
        )

        metric_name = plot["metric"]["name"]
        df = datasets[dataset_name]
        # print(df)
        x = df[variable_name]
        y = df[metric_name]

        ax.plot(x, y, linestyle=sample["linestyle"], label="{}".format(sample["label"]))

    ax.legend(loc=plot["leg_loc"], frameon=False)
    ax.set_xlabel(plot["title_x"])
    ax.set_ylabel(plot["title_y"])
    ax.grid(linestyle="dashed")

    # ax.set_xscale("log")
    # ax.set_yscale(plot["yscale"])
    fig.tight_layout()
    # fig.savefig("figs/{}.pdf".format(plot["name"]))
    fig.savefig("figs/{}.png".format(plot["name"]))

import numpy as np
import ROOT
from ROOT import TLorentzVector
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['legend.fontsize'] = 16


# _______________________________________________________________________________
def plotHistograms(config):
    fig, ax = plt.subplots()
    samples = config["data"]
    
    ymax = -1
    for sample in samples:
        filename = sample["filename"]
        file = ROOT.TFile(filename)
        hname = sample["histname"]
        hist = file.Get(hname)
        # print(sample, sample["histname"])
        x, y = [], []
        integral = 1.0
        
        max_bin = hist.GetMaximumBin()
        max_val = hist.GetBinContent(max_bin)

        if max_val >= ymax:
            ymax = max_val
        if "normalize" in config and config["normalize"]:
            integral = hist.Integral(0, hist.GetNbinsX() + 1)
        if "normfirstbin" in config and config["normfirstbin"]:
            integral = hist.GetBinContent(1)

        if "rebin" in config:
            hist.Rebin(config["rebin"])

        for i in range(1, hist.GetNbinsX() + 1):
            x.append(hist.GetBinCenter(i))
            y.append(hist.GetBinContent(i) / integral)

        # ax.plot(x, y, label="{}".format(sample["label"]))

        ax.hist(
            x,
            len(x),
            weights=y,
            label="{}".format(sample["label"]),
            histtype="step",
            linewidth=config["linewidth"],
            color=sample["color"]
        )

    ymax /= integral
    # Create new legend handles but use the colors from the existing ones
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
    ax.legend(
        handles=new_handles,
        labels=labels,
        frameon=False,
        loc=config["leg_loc"],
        #fontsize=10,
    )
    if "text" in config:
        for text in config["text"]:
            color = "black"
            if "color" in text:
                color = text["color"]
            ax.text(
                text["location"][0],
                text["location"][1],
                text["content"],
                verticalalignment="top",
                horizontalalignment="left",
                transform=ax.transAxes,
                weight="bold",
                color=color
            )

    ax.set_xlabel(config["title_x"])
    ax.set_ylabel(config["title_y"])
    if config["grid"]:
        ax.grid(linestyle="dashed")
        
    
    if "ymin" in config and "ymax" in config and config["ymax"] == "auto":
        if "yscale" in config and config["yscale"] == "log":
            ax.set_ylim(config["ymin"], ymax*200)
        elif "yscale" in config:
            ax.set_ylim(config["ymin"], ymax*1.5)
       
    elif "ymin" in config and "ymax" in config:
        ax.set_ylim(config["ymin"], config["ymax"])
    
    if "xmin" in config and "xmax" in config:
        ax.set_xlim(config["xmin"], config["xmax"])

    # ax.set_xscale("log")
    if "yscale" in config:
        ax.set_yscale(config["yscale"])
    fig.tight_layout()
    # fig.savefig("figs/{}.pdf".format(config["name"]))
    fig.savefig("{}/{}.png".format(config["outdir"], config["name"]))
    fig.savefig("{}/{}.pdf".format(config["outdir"], config["name"]))

    return fig, ax

# _______________________________________________________________________________
""" compute minimal interval that contains 68% area under curve """


def getEffSigma(theHist, wmin=0.2, wmax=1.8, epsilon=0.01):

    point = wmin
    weight = 0.0
    points = []
    thesum = theHist.Integral(0, theHist.GetNbinsX() + 1)

    # fill list of bin centers and the integral up to those point
    for i in range(theHist.GetNbinsX()):
        weight += theHist.GetBinContent(i)
        points.append([theHist.GetBinCenter(i), weight / thesum])

    low = wmin
    high = wmax

    width = wmax - wmin
    for i in range(len(points)):
        for j in range(i, len(points)):
            wy = points[j][1] - points[i][1]
            # print(wy)
            if abs(wy - 0.683) < epsilon:
                # print("here")
                wx = points[j][0] - points[i][0]
                if wx < width:
                    low = points[i][0]
                    high = points[j][0]
                    # print(points[j][0], points[i][0], wy, wx)
                    width = wx
    # print(low, high)
    return 0.5 * (high - low)


# _______________________________________________________________________________
""" compute fwhm """


def getFWHM(theHist):
    # mu = theHist.GetXaxis().GetBinCenter(theHist.GetMaximumBin())
    max_bin = theHist.GetMaximumBin()
    first_bin = 0
    last_bin = theHist.GetNbinsX() + 1

    max_val = theHist.GetBinContent(max_bin)

    ratio_up = 1.0
    ratio_down = 1.0

    down_bin = max_bin
    up_bin = max_bin

    # find first bin that gives half max from below
    # print(max_bin, max_val)
    for i in range(max_bin, first_bin - 1, -1):
        binc = theHist.GetBinContent(i)
        # print(i, binc, ratio_down, down_bin)
        if binc > 0 and ratio_down > 0.5:
            ratio_down = binc / max_val
            down_bin = i
        else:
            break
    down_bincenter = theHist.GetXaxis().GetBinCenter(down_bin)
    down_val = down_bincenter + 0.5 * theHist.GetXaxis().GetBinWidth(down_bin)

    # print(down_bin, down_bincenter, down_val)

    # find first bin that gives half max from below
    # print(max_bin, max_val)
    for i in range(max_bin, last_bin + 1, 1):
        binc = theHist.GetBinContent(i)
        # print(i, binc, ratio_up, up_bin)
        if binc > 0 and ratio_up > 0.5:
            ratio_up = binc / max_val
            up_bin = i
        else:
            break

    up_bincenter = theHist.GetXaxis().GetBinCenter(up_bin)
    up_val = up_bincenter - 0.5 * theHist.GetXaxis().GetBinWidth(up_bin)

    # print(up_bin, up_bincenter, up_val)

    fwhm = up_val - down_val
    # print(fwhm)

    return fwhm


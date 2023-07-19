import numpy as np
import ROOT
from ROOT import TLorentzVector
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


ROOT.gSystem.Load("libDelphes")

try:
    ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
    ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
    pass


# _______________________________________________________________________________
def find_daughters(particle, all_particles, unstables, daughters):

    d1 = particle.D1
    d2 = particle.D2

    if d1 < 0 and d2 < 0:
        if particle not in daughters:
            daughters.append(particle)
        return 0

    if particle not in unstables:

        # print d1,d2
        for i in range(d1, d2 + 1):
            daughter = all_particles[i]
            find_daughters(daughter, all_particles, unstables, daughters)

        unstables.append(particle)


# _______________________________________________________________________________
def find_genpfcols(collection, genall, gentracks, genphotons, gennhadrons):

    for gen in collection:
        if gen.Status == 1:
            if abs(gen.PID) in [12, 14, 16]:
                continue
            genall.append(gen)
            if abs(gen.Charge) > 0:
                gentracks.append(gen)
            elif abs(gen.PID) == 22:
                genphotons.append(gen)
            else:
                gennhadrons.append(gen)


# _______________________________________________________________________________
def find_particle(collection, pid, status):
    for gen in collection:
        if gen.PID == pid and gen.Status == status:
            return gen


# _______________________________________________________________________________


def print_genparticles(collection):
    print("-----------------------------------------------------------------")
    print("")
    i = -1
    for gen in collection:
        i += 1
        print(
            "N: ",
            i,
            ", St: ",
            gen.Status,
            ", PID: ",
            gen.PID,
            ", E: ",
            gen.E,
            ", PT: ",
            gen.PT,
            ", Eta: ",
            gen.Eta,
            ", M: ",
            gen.Mass,
            ", M1: ",
            gen.M1,
            ", M2: ",
            gen.M2,
            ", D1: ",
            gen.D1,
            ", D2: ",
            gen.D2,
        )


# ______________________________________________________________________________
""" fill histo according  """


def fill_p_hist(collection, hist, norm_factor=1.0):
    v = TLorentzVector()
    for p in collection:
        if isinstance(p, TLorentzVector):
            hist.Fill(p.P())
            v += p
        else:
            hist.Fill(p.P4().P())


# ______________________________________________________________________________
""" fill mass of vector sum of collection in histo """


def fill_mass_hist(collection, hist, norm_factor=1.0):
    v = TLorentzVector()
    for p in collection:
        if isinstance(p, TLorentzVector):
            v += p
        else:
            v += p.P4()
    hist.Fill(v.M() / norm_factor)


# ______________________________________________________________________________
""" fill visible energy of vector sum of collection in histo """


def fill_evis_hist(collection, hist, norm_factor=1.0):
    v = TLorentzVector()
    for p in collection:
        if isinstance(p, TLorentzVector):
            v += p
        else:
            v += p.P4()
    hist.Fill(v.E() / norm_factor)


# ______________________________________________________________________________
""" get bin size np array """


def get_bin_size(array):
    array_length = len(array)
    last_element = array[array_length - 1]
    first_element = array[0]
    return abs(float(last_element - first_element)) / (array_length - 1)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_efracleft_hist_p(collection, vals, prof):

    ## convert cuts to GeV
    pvals = 0.001 * vals

    etot = 0.0
    for p in collection:
        etot += p.E

    for cut in pvals:
        ecol = 0
        for p in collection:
            if p.P4().P() > cut:
                ecol += p.E

        if etot > 0:
            prof.Fill(cut, ecol / etot)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_eleft_hist_p(collection, vals, prof):

    ## convert cuts to GeV
    pvals = 0.001 * vals

    for cut in pvals:
        ecol = 0
        for p in collection:
            if p.P4().P() > cut:
                ecol += p.E

        prof.Fill(cut, ecol)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_nfracleft_hist_p(collection, vals, prof):

    ## convert cuts to GeV
    pvals = 0.001 * vals

    ntot = 0
    for p in collection:
        ntot += 1

    for cut in pvals:
        ncol = 0
        for p in collection:
            if p.P4().P() > cut:
                ncol += 1

        if ntot > 0:
            prof.Fill(cut, float(ncol / ntot))


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_nleft_hist_p(collection, vals, prof):

    ## convert cuts to GeV
    pvals = 0.001 * vals

    for cut in pvals:
        ncol = 0
        for p in collection:
            if p.P4().P() > cut:
                ncol += 1

        prof.Fill(cut, ncol)


# ______________________________________________________________________________
""" fill fraction  hist p plot """


def fill_frac_hist_p(collection, all, vals, prof):

    ## convert cuts to GeV
    pvals = 0.001 * vals

    for cut in pvals:
        ecol = 0
        etot = 0
        for p in collection:
            # print(p.P4().P(), cut)
            if p.P4().P() > cut:
                ecol += p.E
        for p in all:
            # print(p.P4().P(), cut)
            if p.P4().P() > cut:
                etot += p.E

        if etot > 0:
            prof.Fill(cut, ecol / etot)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_efracleft_hist_theta(collection, vals, prof):

    etot = 0.0
    for p in collection:
        etot += p.E

    for cut in vals:
        ecol = 0
        xval = eta_to_theta(cut)
        for p in collection:
            if abs(p.Eta) < cut:
                ecol += p.E

        if etot > 0:
            xval = eta_to_theta(cut)
            prof.Fill(xval, ecol / etot)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_eleft_hist_theta(collection, vals, prof):

    for cut in vals:
        ecol = 0
        xval = eta_to_theta(cut)
        for p in collection:
            if abs(p.Eta) < cut:
                ecol += p.E

        xval = eta_to_theta(cut)
        prof.Fill(xval, ecol)


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_nfracleft_hist_theta(collection, vals, prof):

    ntot = 0
    for p in collection:
        ntot += 1

    for cut in vals:
        ncol = 0
        xval = eta_to_theta(cut)
        for p in collection:
            if abs(p.Eta) < cut:
                ncol += 1

        if ntot > 0:
            xval = eta_to_theta(cut)
            prof.Fill(xval, float(ncol / ntot))


# ______________________________________________________________________________
""" fill energy cumulative hist p plot """


def fill_nleft_hist_theta(collection, vals, prof):

    for cut in vals:
        ncol = 0
        xval = eta_to_theta(cut)
        for p in collection:
            if abs(p.Eta) < cut:
                ncol += 1
        xval = eta_to_theta(cut)
        prof.Fill(xval, ncol)


# ______________________________________________________________________________
""" fill fraction cumulative hist theta plot """


def fill_frac_hist_theta(collection, all, eta_vals, prof):

    ## convert cuts to eta
    for cut in eta_vals:
        ecol = 0
        etot = 0
        for p in collection:
            # print(p.P4().P(), cut)
            if abs(p.Eta) < cut:
                ecol += p.E
        for p in all:
            # print(p.P4().P(), cut)
            if abs(p.Eta) < cut:
                etot += p.E

        if etot > 0:
            xval = eta_to_theta(cut)
            prof.Fill(xval, ecol / etot)


# ______________________________________________________________________________
""" convert angle in to eta """


def theta_to_eta(theta_deg):
    theta_rad = theta_deg / 180.0 * np.pi
    eta = -np.log(np.tan(theta_rad / 2))
    return eta
    # print(theta_deg, theta_rad, eta)


# ______________________________________________________________________________
""" convert eta to theta in deg """


def eta_to_theta(eta):
    theta_rad = 2 * np.arctan(np.exp(-eta))
    theta_deg = 180.0 * theta_rad / np.pi
    # print(eta, theta_rad, theta_deg)
    return theta_deg


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
""" compute multiplicity, sumE and sumE^2 """


def compute_moments(collection):
    n, sume, sume2 = 0, 0, 0
    for p in collection:
        n += 1
        sume += p.E
        sume2 += p.E ** 2
    return n, sume, sume2


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


# _______________________________________________________________________________
""" plot histograms by looping over different samples """


def plotRootHistograms(
    samples,
    config,
):
    fig, ax = plt.subplots()

    for sample in samples:
        filename = sample["filename"]
        file = ROOT.TFile(filename)
        hname = config["histname"]
        hist = file.Get(hname)

        x, y = [], []
        integral = 1.0
        if "normalize" in config and config["normalize"]:
            integral = hist.Integral(0, hist.GetNbinsX() + 1)
        if "rebin" in config:
            hist.Rebin(config["rebin"])
        if "normfirstbin" in config and config["normfirstbin"]:
            integral = hist.GetBinContent(1)

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
            linewidth=2,
        )

    # Create new legend handles but use the colors from the existing ones
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
    ax.legend(
        handles=new_handles,
        labels=labels,
        frameon=False,
        loc=config["leg_loc"],
        # fontsize=10,
    )
    if "text" in config:
        ax.text(
            0.20,
            0.90,
            config["text"],
            verticalalignment="top",
            horizontalalignment="left",
            transform=ax.transAxes,
        )

    ax.set_xlabel(config["title_x"])
    ax.set_ylabel(config["title_y"])
    ax.grid(linestyle="dashed")
    if "ymin" in config and "ymax" in config:
        ax.set_ylim(config["ymin"], config["ymax"])

    # ax.set_xscale("log")
    if "yscale" in config:
        ax.set_yscale(config["yscale"])
    fig.tight_layout()
    # fig.savefig("figs/{}.pdf".format(config["name"]))
    fig.savefig("figs/{}.png".format(config["name"]))


# _______________________________________________________________________________
""" plot histograms by looping over different samples """


def plotBlockHistograms(samples, config_list, name):

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = prop_cycle.by_key()["color"]
    lines = ["-", "--", ":"]

    fig, ax = plt.subplots()

    for sample in samples:
        filename = sample["filename"]
        file = ROOT.TFile(filename)

        for config in config_list:
            hname = config["histname"]
            hist = file.Get(hname)

            x, y = [], []
            for i in range(1, hist.GetNbinsX() + 1):
                x.append(hist.GetBinCenter(i))
                y.append(hist.GetBinContent(i))

            ax.plot(
                x,
                y,
                color=colors[samples.index(sample)],
                linestyle=lines[config_list.index(config)],
                label="{} ({}) ".format(sample["label"], config["label"]),
            )

    config = config_list[0]
    ax.legend(frameon=False, ncol=int(len(samples)), fontsize=8, loc="upper center")
    ax.set_xlabel(config["title_x"])
    ax.set_ylabel(config["name"])
    ax.grid(linestyle="dashed")
    ax.set_ylim(config["ymin"], config["ymax"])

    fig.tight_layout()
    fig.savefig("figs/{}.pdf".format(name))
    fig.savefig("figs/{}.png".format(name))


# _______________________________________________________________________________
class Data:
    def __init__(self, filepath, histname, label):
        self.filepath = filepath  #
        self.histname = histname  #
        self.label = label  #


# _______________________________________________________________________________
plt.rcParams.update({"font.size": 15})


def plotHistograms(config):
    fig, ax = plt.subplots()
    samples = config["data"]
    for sample in samples:
        filename = sample["filename"]
        file = ROOT.TFile(filename)
        hname = sample["histname"]
        hist = file.Get(hname)

        if not hist:
            continue
        # print(sample, sample["histname"])
        x, y = [], []
        integral = 1.0
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
            linewidth=2,
        )

    # Create new legend handles but use the colors from the existing ones
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
    fontsize = 10
    if "leg_size" in config:
        fontsize = config["leg_size"]
    ax.legend(
        handles=new_handles,
        labels=labels,
        frameon=False,
        loc=config["leg_loc"],
        fontsize=10,
    )
    if "text" in config:
        for text in config["text"]:
            weight = "normal"
            size = 12
            if "weight" in text:
                weight = text["weight"]
            if "size" in text:
                size = text["size"]
            ax.text(
                text["location"][0],
                text["location"][1],
                text["content"],
                verticalalignment="top",
                horizontalalignment="left",
                transform=ax.transAxes,
                weight=weight,
                fontsize=size,
            )

    ax.set_xlabel(config["title_x"])
    ax.set_ylabel(config["title_y"])
    ax.grid(linestyle="dashed")
    if "ymin" in config and "ymax" in config:
        ax.set_ylim(config["ymin"], config["ymax"])
    if "xmin" in config and "xmax" in config:
        ax.set_xlim(config["xmin"], config["xmax"])

    # ax.set_xscale("log")
    if "yscale" in config:
        ax.set_yscale(config["yscale"])
    fig.tight_layout()
    # fig.savefig("figs/{}.pdf".format(config["name"]))
    fig.savefig("figs/{}.png".format(config["name"]))

    return fig, ax


# _______________________________________________________________________________
def draw_multigraph(config):
    fig, ax = plt.subplots()
    graphs = config["data"]
    for graph in graphs:
        df = graph["data"]
        # print(df)
        x = df[config["varx"]]
        y = df[config["vary"]]

        linestyle = "solid"
        linewidth = 2
        if "linestyle" in graph:
            linestyle = graph["linestyle"]
        if "linewidth" in graph:
            linewidth = graph["linewidth"]

        ax.plot(
            x,
            y,
            linestyle=linestyle,
            linewidth=linewidth,
            label="{}".format(graph["label"]),
        )

    ax.legend(loc=config["leg_loc"], frameon=False)
    ax.set_xlabel(config["title_x"])
    ax.set_ylabel(config["title_y"])
    ax.grid(linestyle="dashed")

    if "ymin" in config and "ymax" in config:
        ax.set_ylim(config["ymin"], config["ymax"])
    if "xmin" in config and "xmax" in config:
        ax.set_xlim(config["xmin"], config["xmax"])

    if "yscale" in config:
        ax.set_yscale(config["yscale"])
    if "xscale" in config:
        ax.set_xscale(config["xscale"])

    # ax.set_xscale("log")
    # ax.set_yscale(plot["yscale"])
    fig.tight_layout()
    # fig.savefig("figs/{}.pdf".format(plot["name"]))
    fig.savefig("figs/{}.png".format(config["name"]))


# _______________________________________________________________________________
def produce_resolution_dataframe(input_list, use_gauss=False):

    x = []
    mu = []
    sig = []
    for data in input_list:
        filename = data["filename"]
        file = ROOT.TFile(filename)
        hist = file.Get(data["histname"])

        if not hist:
            continue
        hist.Rebin(2)

        x.append(data["val"])
        # if x > 0: break

        ## extract resolution
        sigma = getEffSigma(hist, wmin=0.0, wmax=2.0, epsilon=0.01)
        # sigma = getFWHM(hist) / 2.35

        x0 = hist.GetXaxis().GetBinCenter(hist.GetMaximumBin())
        d = sigma
        f = ROOT.TF1("gausfit", "gaus", 0.0, 6.0)
        s = 2.0
        hist.Fit("gausfit", "Q", "", x0 - s * d, x0 + s * d)

        mode = f.GetParameter(1)
        # mode = hist.GetMean()
        sigma_fit = f.GetParameter(2)

        mu.append(mode)

        if use_gauss:
            sigma = sigma_fit

        print(x0, mode, sigma, sigma_fit)
        # print(hname, mode, sigma)
        if mode > 0:
            sig.append(sigma / mode)
        else:
            print("Did not find histogram maximum ...")
            sig.append(sigma)

    df = pd.DataFrame({data["varname"]: x, "response": mu, "resolution": sig})
    print(df)
    return df

import matplotlib.pyplot as plt
import numpy as np


def rel_reso_total(e, det):

    a = det.tracker.a
    b = det.tracker.b
    x_x0 = det.tracker.x_x0
    n = det.calo.n
    s = det.calo.s
    c = det.calo.c

    e_brem = e * (1.0 - np.exp(-x_x0))
    e_tr = e - e_brem

    sigma_tr = a * e_tr ** 2 + b * e_tr
    sigma_calo = np.sqrt(n ** 2 + e_brem * s ** 2 + e_brem ** 2 * c ** 2)

    return np.sqrt(sigma_tr ** 2 + sigma_calo ** 2) / e


def rel_reso_trk(e, trk):
    return trk.a * e + trk.b


def rel_reso_calo(e, calo):
    return np.sqrt(calo.n ** 2 / e ** 2 + calo.s ** 2 / e + calo.c ** 2)


def plot_resolutions(resos, name):
    # print(reso_idea_dr)
    fig, ax = plt.subplots()
    for label, vals in resos.items():
        ax.plot(e, vals, lw=2, label=label)

    ax.legend(frameon=False)
    ax.set_xlabel(r"E [GeV]")
    ax.set_ylabel(r"$\sigma(E)/E$")
    ax.grid(linestyle="dashed")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_ylim(1e-4, 1.0)
    """
    if "ymin" in plot and "ymax" in plot:
        ax.set_ylim(plot["ymin"], plot["ymax"])
    ax.set_xscale("log")

    """
    fig.tight_layout()
    fig.savefig("{}.png".format(name))


class Tracker:
    def __init__(self, a, b, x_x0):
        self.a = a
        self.b = b
        self.x_x0 = x_x0


class Calo:
    def __init__(self, n, s, c):
        self.n = n
        self.s = s
        self.c = c


class Det:
    def __init__(self, tracker, calo):
        self.tracker = tracker
        self.calo = calo


idea_trk = Tracker(2.5e-05, 5.0e-04, 0.047)
cld_trk = Tracker(1.0e-05, 2.5e-03, 0.115)
cms_trk = Tracker(1.0e-04, 0.01, 0.50)

idea_calo = Calo(0.05, 0.11, 0.01)
cld_calo = Calo(0.05, 0.15, 0.01)
cry_calo = Calo(0.12, 0.03, 0.003)
cms_calo = Calo(0.12, 0.05, 0.01)

idea = Det(idea_trk, idea_calo)
idea_cry = Det(idea_trk, cry_calo)
cld = Det(cld_trk, cld_calo)
# cms = Det(cms_trk, cry_calo)
cms = Det(cms_trk, cms_calo)

e = np.arange(1.0, 200.1, 0.1)

reso_idea = rel_reso_total(e, idea)
reso_idea_trk = rel_reso_trk(e, idea.tracker)
reso_idea_calo = rel_reso_calo(e, idea.calo)

reso_idea_cry = rel_reso_total(e, idea_cry)
reso_idea_trk = rel_reso_trk(e, idea_cry.tracker)
reso_idea_cry_calo = rel_reso_calo(e, idea_cry.calo)

reso_cld = rel_reso_total(e, cld)
reso_cld_trk = rel_reso_trk(e, cld.tracker)
reso_cld_calo = rel_reso_calo(e, cld.calo)

reso_cms = rel_reso_total(e, cms)
reso_cms_trk = rel_reso_trk(e, cms.tracker)
reso_cms_calo = rel_reso_calo(e, cms.calo)


resolutions_idea = {
    "IDEA": reso_idea,
    "IDEA (trk only)": reso_idea_trk,
    "IDEA (calo only)": reso_idea_calo,
}

resolutions_idea_cry = {
    "IDEA - crys": reso_idea_cry,
    "IDEA (trk only)": reso_idea_trk,
    "IDEA (calo only)": reso_idea_cry_calo,
}

resolutions_cld = {
    "CLD ": reso_cld,
    "CLD (trk only)": reso_cld_trk,
    "CLD (calo only)": reso_cld_calo,
}

resolutions_cms = {
    "CMS ": reso_cms,
    "CMS (trk only)": reso_cms_trk,
    "CMS (calo only)": reso_cms_calo,
}


resolutions_all = {
    "IDEA": reso_idea,
    "IDEA - crys": reso_idea_cry,
    "CLD ": reso_cld,
    "CMS ": reso_cms,
}


plot_resolutions(resolutions_idea, "brem_idea")
plot_resolutions(resolutions_idea_cry, "brem_idea_cry")
plot_resolutions(resolutions_cld, "brem_cld")
plot_resolutions(resolutions_cms, "brem_cms")
plot_resolutions(resolutions_all, "brem_all")

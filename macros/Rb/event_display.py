import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ROOT
from utils import logtr
import numpy as np

def create_event_display(ev):
    jets_p4 = []
    jets_s = []

    bhadrons_p4 = []
    bhadrons_v = []

    gluons_p4 = []

    for i in range(ev.event_njet):
        jets_p4.append(
            ROOT.TLorentzVector(ev.jet_px[i], ev.jet_py[i], ev.jet_pz[i], ev.jet_e[i])
        )
        jets_s.append(ev.recojet_isB[i])

    for i in range(ev.n_bhadrons):
        bhadrons_p4.append(
            ROOT.TLorentzVector(
                ev.bhadron_px[i], ev.bhadron_py[i], ev.bhadron_pz[i], ev.bhadron_e[i]
            )
        )

        bhadrons_v.append(
            ROOT.TVector3(ev.bhadron_x[i], ev.bhadron_y[i], ev.bhadron_z[i])
        )

    for i in range(ev.n_partons):
        if ev.parton_pid[i] != 21:
            continue
        gluons_p4.append(
            ROOT.TLorentzVector(
                ev.parton_px[i], ev.parton_py[i], ev.parton_pz[i], ev.parton_e[i]
            )
        )

    # Function to plot a vector in Matplotlib
    def plot_vector(
        ax,
        start_point,
        end_point,
        color,
        linewidth=1,
        text="",
        vtx_scale=0.5,
        vec_scale=0.1,
    ):
        ax.quiver(
            vtx_scale * start_point[0],
            vtx_scale * start_point[1],
            vtx_scale * start_point[2],
            vec_scale * (end_point[0] - start_point[0]),
            vec_scale * (end_point[1] - start_point[1]),
            vec_scale * (end_point[2] - start_point[2]),
            color=color,
            arrow_length_ratio=0.15,
            linewidth=linewidth,
        )
        # Add text annotation
        ax.text(vec_scale*1.2*end_point[0], vec_scale*1.20*end_point[1], vec_scale*1.20*end_point[2], text, color=color)

    # Create a new figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # Hide the axes
    ax.set_axis_off()

    # Plotting
    for jet, score in zip(jets_p4, jets_s):
        plot_vector(
            ax,
            (0, 0, 0),
            (jet.Px(), jet.Py(), jet.Pz()),
            "blue",
            2,
            f"jet score = {logtr(score):.2f}"
        )

    for bhadron, vertex in zip(bhadrons_p4, bhadrons_v):
        plot_vector(
            ax,
            (vertex.X(), vertex.Y(), vertex.Z()),
            (bhadron.Px(), bhadron.Py(), bhadron.Pz()),
            "red",
            1,
            "b"
        )
    
    gluons_p4.sort(key=lambda gluon: gluon.P(), reverse=True)
    for i, gluon in enumerate(gluons_p4):
        txt = "g"
        if i > 1:
            txt = ""
        plot_vector(ax, (0, 0, 0), (gluon.Px(), gluon.Py(), gluon.Pz()), "green", 1, txt)

    # Setting the axes properties
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")

    plt.show()


import sys
inputFile = sys.argv[1]
event_number = int(sys.argv[2])

f = ROOT.TFile.Open(inputFile)
tree = f.events

iev = 0
for ev in tree:
    iev += 1
    #print(iev,event_number)
    if iev != event_number:
        continue
    
    create_event_display(ev)
    #break

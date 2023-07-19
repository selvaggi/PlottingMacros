from plot_config import *
from utils import *

multigraph_name = "occupancy"
graphs = []


detector = {
    "name": "idea",
    "label": "IDEA",
}

observable = {
    "name": "mass_pf",
    "label": r"$M_{vis}^{PF}$ [GeV]",
    "title": "visible mass (particle-flow)",
    "histname": "",
}

metric = {
    "name": "response",
    "label": "rel. response",
}


parameter = etaphirescal
for sample in samples:
    input_data = []
    for variation in parameter:
        input_data.append(
            {
                "filename": "{}/{}_{}_{}{}.root".format(
                    datadir,
                    sample["name"],
                    detector["name"],
                    variation["name"],
                    variation["value"],
                ),
                "varname": variation["name"],
                # "histname": "hNNeutralHadronPerTower",
                "histname": "hNPhotonPerTower",
                "rebin": 1,
                "val": variation["value"],
            }
        )
    ## produce dataframe for sample
    print(input_data)
    dataframe = produce_resolution_dataframe(input_data, True)
    graph_name = (
        "{}_{}_{}".format(
            sample["name"],
            detector["name"],
            variation["name"],
        ),
    )
    # produce graph object corresponding to dataframe
    graph = {
        "sample": sample["name"],
        "detector": detector["name"],
        "name": graph_name,
        "label": sample["label"],
        # "linestyle":,
        # "linecolor":,
        # "linewidth":,
        "data": dataframe,
    }
    graphs.append(graph)

# compose multi_graph object
multigraph = {
    "data": graphs,
    "name": multigraph_name,
    "varx": parameter[0]["name"],
    "vary": metric["name"],
    "title_x": r"$\Delta\eta\times\Delta\phi$ calo cell size",
    "title_y": "< N > per cell",
    "yscale": "linear",
    "xscale": "log",
    "text": [
        {
            # "content": sample["label"],
            "content": "label",
            "location": (0.65, 0.80),
        },
        {
            # "content": param[0]["title"],
            "content": "label",
            "location": (0.65, 0.70),
            "size": 10,
        },
        {
            "content": "variations",
            "location": (0.65, 0.60),
            "size": 10,
        },
        {
            # "content": detector["label"],
            "content": "label",
            "location": (0.008, 1.08),
            "weight": "bold",
        },
    ],
    "leg_loc": "upper left",
    "leg_size": 12,
    # "option": "hist",
    "ymin": 1.0,
    "ymax": 2.0,
    # "xmin": 90,
    # "xmax": 150,
}
draw_multigraph(multigraph)

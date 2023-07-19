from utils import *
from plot_config import *

datadir = "data/DetectorVariation_v5/"
parameters = detector_parameters_list

observables = [
    {
        "name": "mass_pf",
        "label": r"$M_{vis}^{PF}$ [GeV]",
        "title": "visible mass (particle-flow)",
        "histname": "hMassPFConstsNorm",
    },
    {
        "name": "evis_pf",
        "label": r"$E_{vis}^{PF}$ [GeV]",
        "title": "visible energy (particle-flow)",
        "histname": "hEvisPFConstsNorm",
    },
]


graphs = []
for metric in metrics:
    for detector in detectors:
        for observable in observables:
            for parameter in parameters:
                multigraph_name = "{}_{}_{}_{}".format(
                    metric["name"],
                    observable["name"],
                    parameter[0]["name"],
                    detector["name"],
                )
                graphs = []
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
                                "histname": observable["histname"],
                                "rebin": 2,
                                "val": variation["value"],
                            }
                        )
                    ## produce dataframe for sample
                    print(input_data)
                    dataframe = produce_resolution_dataframe(input_data, True)
                    graph_name = (
                        "{}_{}_{}_{}".format(
                            observable["name"],
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
                    "title_x": parameter[0]["plot_title"],
                    "title_y": metric["label"],
                    "yscale": "linear",
                    "xscale": "linear",
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
                    "ymin": 0.0,
                    "ymax": 0.10,
                    # "xmin": 90,
                    # "xmax": 150,
                }
                draw_multigraph(multigraph)

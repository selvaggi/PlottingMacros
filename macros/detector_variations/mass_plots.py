from utils import *
from plot_config import *


observables = [
    {
        "name": "mass_pf",
        "label": r"$M_{vis}^{PF}$ [GeV]",
        "title": "visible mass (particle-flow)",
        "histname": "hMassPFConsts",
    },
    {
        "name": "evis_pf",
        "label": r"$E_{vis}^{PF}$ [GeV]",
        "title": "visible energy (particle-flow)",
        "histname": "hEvisPFConsts",
    },
]
parameters = detector_parameters_list


spectra_plots = []
for sample in samples:
    #print(sample)
    for detector in detectors:
        #print(detector)
        for observable in observables:
            #print(observable)
            for param in parameters:
                data = []
                #print(param)
                for var in param:
                    #print(var)
                    filename = "{}/{}_{}_{}{}.root".format(datadir,sample["name"],detector["name"],var["name"],var["value"])
                    print(filename)
                    data.append(
                        {
                            # "filename": sample["filename"],
                            "filename": filename,
                            "histname": observable["histname"],
                            "label": var["label"],
                        }
                    )

                plotname = "{}_{}_{}_{}".format(
                detector["name"],
                sample["name"],
                param[0]["name"],
                observable["name"],
                )
                plot = {
                        "data": data,
                        "name": plotname,
                        "title_x": observable["label"],
                        "title_y": "event fraction",
                        "yscale": "linear",
                        "text": [
                            {
                                "content": sample["label"],
                                "location": (0.65, 0.80),
                            },
                            #{
                            #    "content": param[0]["title"],
                            #    "location": (0.65, 0.70),
                            #    "size": 10,
                            #},
                            {
                                "content": "variations",
                                "location": (0.65, 0.60),
                                "size": 10,
                            },
                            {
                                "content": detector["label"],
                                "location": (0.008, 1.08),
                                "weight": "bold"
                            },
                        ],
                        "leg_loc": "upper left",
                        "leg_size": 12,
                        "normalize": True,
                        "option": "hist",
                        "ymin": 0.,
                        "ymax": 0.075,
                        "xmin": 90,
                        "xmax": 150,
                        "rebin": 2,
                }
                plotHistograms(plot)




"""
data = []
sample = samples[3]
for detector in detectors:
    filename = "{}/vvgg_{}_hcalconst0.01.root".format(datadir,detector["name"])
    data.append(
        {
            # "filename": sample["filename"],
            "filename": filename,
            "histname": observables[0]["histname"],
            "label": detector["label"],
        }
    )


plot = {
        "data": data,
        "name": "mass_detectors",
        "title_x": observables[0]["label"],
        "title_y": "event fraction",
        "yscale": "linear",
        "text": [
            {
                "content": sample["label"],
                "location": (0.65, 0.80),
            },
            #{
            #    "content": param[0]["title"],
            #    "location": (0.65, 0.70),
            #    "size": 10,
            #},
            {
                "content": "variations",
                "location": (0.65, 0.60),
                "size": 10,
            },
            {
                "content": detector["label"],
                "location": (0.008, 1.08),
                "weight": "bold"
            },
        ],
        "leg_loc": "upper left",
        "leg_size": 12,
        "normalize": True,
        "option": "hist",
        "ymin": 0.,
        "ymax": 0.075,
        "xmin": 90,
        "xmax": 150,
        "rebin": 2,
}

plotHistograms(plot)
"""
#for plot in spectra_plots:
#    plotHistograms(plot)

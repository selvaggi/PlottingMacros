import copy

datadir = "data/DetectorVariation_v5/"

samples = []
final_states = ["qq", "ss", "cc", "bb", "gg"]
final_states = ["ss", "cc", "bb", "gg"]
# final_states = ["gg", "ss"]
for fs in final_states:
    samples.append(
        {
            "name": "vv{}".format(fs),
            "linestyle": "solid",
            "label": r"$H \rightarrow {}$".format(fs),
        },
    )

detectors = [
    {
        "name": "ideacry",
        "label": "IDEA + crystals",
    },
    {
        "name": "idea",
        "label": "IDEA",
    },
    {
        "name": "cms",
        "label": "CMS",
    },
    {
        "name": "atlas",
        "label": "ATLAS",
    },
]


observables = [
    {
        "name": "mass_pf",
        "label": r"$M_{vis}^{PF}$ [GeV]",
        "title": "visible mass (particle-flow)",
        "histname": "hMassPFConsts",
    },
]


# _______________________________________________________________________________
def produce_delphes_card(file_in, config):

    # print("producing {}".format(file_out))
    fin = open(file_in, "rt")
    fout = open(config["filename"], "wt")
    for line in fin:
        new_line = line
        for field, param in config["parameters"].items():
            key = param["dummystr"]
            val = param["value"]
            # print(key)
            new_line = new_line.replace(key, "{}".format(val))
        fout.write(new_line)

    # close input and output files
    fin.close()
    fout.close()

    print("generated {}".format(config["filename"]))


# _______________________________________________________________________________
def fill_param_list(name, dummystr, range, label, plot_title, precision):
    list = []
    # print(label)
    format_str = "{{:.{}f}}".format(precision)
    for val in range:

        new_label = label.replace("XXX", format_str.format(val))
        list.append(
            {
                "name": name,
                "dummystr": dummystr,
                "plot_title": plot_title,
                "value": val,
                "label": new_label,
            }
        )
    return list


# _______________________________________________________________________________
idea_parameters = {
    "bfield": {
        "name": "bfield",
        "dummystr": "DUMMY_BFIELD",
        "value": 2.0,
        "label": "B = 2 T",
    },
    "ptmintrk": {
        "name": "ptmintrk",
        "dummystr": "DUMMY_PTMINTRACK",
        "value": 0.1,
        "label": r"$p_{T}^{min}$(track) = 0.1 GeV",
    },
    "ecalemin": {
        "name": "ecalemin",
        "dummystr": "DUMMY_ECALEMIN",
        "value": 0.1,
        "label": r"$E_{min}(ECAL) = 0.1 GeV$",
    },
    "hcalemin": {
        "name": "hcalemin",
        "dummystr": "DUMMY_HCALEMIN",
        "value": 0.1,
        "label": r"$E_{min}(HCAL) = 0.1 GeV$",
    },
    "sigmincal": {
        "name": "sigmincal",
        "dummystr": "DUMMY_SIGMINCALO",
        "value": 3.0,
        "label": r"$\sigma_{min} = 3.0$",
    },
    "etaphirescal": {
        "name": "etaphirescal",
        "dummystr": "DUMMY_ETAPHIRESCALO",
        "value": 0.02,
        "label": r"$\Delta\eta\times\Delta\phi = 0.02$",
    },
    "ecalnoise": {
        "name": "ecalnoise",
        "dummystr": "DUMMY_ECALNOISE",
        "value": 0.05,
        "label": r"$N_{ecal} = 0.05 GeV$",
    },
    "ecalstoch": {
        "name": "ecalstoch",
        "dummystr": "DUMMY_ECALSTOCHASTIC",
        "value": 0.11,
        "label": r"$S_{ecal}=11$%",
    },
    "ecalconst": {
        "name": "ecalconst",
        "dummystr": "DUMMY_ECALCONSTANT",
        "value": 0.01,
        "label": r"$C_{ecal}=$1%",
    },
    "hcalnoise": {
        "name": "hcalnoise",
        "dummystr": "DUMMY_HCALNOISE",
        "value": 0.05,
        "label": r"$N_{hcal} = 0.05 GeV$",
    },
    "hcalstoch": {
        "name": "hcalstoch",
        "dummystr": "DUMMY_HCALSTOCHASTIC",
        "value": 0.30,
        "label": r"$S_{hcal}=30$%",
    },
    "hcalconst": {
        "name": "hcalconst",
        "dummystr": "DUMMY_HCALCONSTANT",
        "value": 0.01,
        "label": r"$C_{ecal}=$1%",
    },
}

ideacry_parameters = copy.deepcopy(idea_parameters)
atlas_parameters = copy.deepcopy(idea_parameters)
cms_parameters = copy.deepcopy(idea_parameters)

ideacry_parameters["ecalstoch"]["value"] = 0.05

cms_parameters["ecalstoch"]["value"] = 0.05
cms_parameters["hcalstoch"]["value"] = 1.00

atlas_parameters["ecalstoch"]["value"] = 0.10
atlas_parameters["hcalstoch"]["value"] = 0.50

detector_idea_baseline = {
    "name": "idea",
    "filename": "cards/generated/idea.tcl",
    "label": "IDEA",
    "parameters": idea_parameters,
}
detector_ideacry_baseline = {
    "name": "ideacry",
    "filename": "cards/generated/ideacry.tcl",
    "label": "IDEA + crystals",
    "parameters": ideacry_parameters,
}
detector_cms_baseline = {
    "name": "cms",
    "filename": "cards/generated/cms.tcl",
    "label": "CMS",
    "parameters": cms_parameters,
}
detector_atlas_baseline = {
    "name": "atlas",
    "filename": "cards/generated/atlas.tcl",
    "label": "ATLAS",
    "parameters": atlas_parameters,
}


bfield = fill_param_list(
    "bfield", "DUMMY_BFIELD", [1.0, 2.0, 3.0, 4.0], "B = XXX T", "B [T]", 0
)
ptmintrk = fill_param_list(
    "ptmintrk",
    "DUMMY_PTMINTRACK",
    [0.1, 0.2, 0.3, 0.4, 0.5, 1.0],
    r"$p_{T}^{min}$(track) = XXX GeV",
    r"$p_{T}^{min}(track)$ [GeV]",
    1,
)
ecalemin = fill_param_list(
    "ecalemin",
    "DUMMY_ECALEMIN",
    [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 1.5, 2.0],
    r"$E_{min}(ECAL) = XXX GeV$",
    r"$E_{min}(ECAL) [GeV]$",
    1,
)
hcalemin = fill_param_list(
    "hcalemin",
    "DUMMY_HCALEMIN",
    [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 1.5, 2.0],
    r"$E_{min}(HCAL) = XXX GeV$",
    r"$E_{min}(HCAL) [GeV]$",
    1,
)
sigmincal = fill_param_list(
    "sigmincal",
    "DUMMY_SIGMINCALO",
    [1.0, 2.0, 3.0, 4.0, 5.0],
    r"$\sigma_{min} = XXX$",
    r"$\sigma_{min}",
    1,
)
etaphirescal = fill_param_list(
    "etaphirescal",
    "DUMMY_ETAPHIRESCALO",
    [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0],
    r"$\Delta\eta\times\Delta\phi = XXX$",
    r"$\Delta\eta\times\Delta\phi$",
    3,
)
ecalnoise = fill_param_list(
    "ecalnoise",
    "DUMMY_ECALNOISE",
    [0.025, 0.05, 0.10, 0.20, 0.50],
    r"$N_{ecal} = XXX GeV$",
    r"$N_{ecal} [GeV]$",
    3,
)
ecalstoch = fill_param_list(
    "ecalstoch",
    "DUMMY_ECALSTOCHASTIC",
    [0.025, 0.05, 0.10, 0.15],
    r"$S_{ecal} = XXX$",
    r"$S_{ecal}$ $[GeV^{1/2}]$",
    3,
)
ecalconst = fill_param_list(
    "ecalconst",
    "DUMMY_ECALCONSTANT",
    [0.005, 0.01, 0.02],
    r"$C_{ecal}=$ XXX",
    r"$C_{ecal}$",
    3,
)
hcalnoise = fill_param_list(
    "hcalnoise",
    "DUMMY_HCALNOISE",
    [0.025, 0.05, 0.10, 0.20, 0.50, 1.00],
    r"$N_{hcal} = XXX GeV$",
    r"$N_{hcal} [GeV]$",
    3,
)
hcalstoch = fill_param_list(
    "hcalstoch",
    "DUMMY_HCALSTOCHASTIC",
    [0.30, 0.40, 0.50, 1.00],
    r"$S_{hcal} = XXX$",
    r"$S_{hcal}$ $[GeV^{1/2}]$",
    3,
)
hcalconst = fill_param_list(
    "hcalconst",
    "DUMMY_HCALCONSTANT",
    [0.005, 0.01, 0.02, 0.05],
    r"$C_{ecal}=$ XXX",
    r"$C_{ecal}$",
    3,
)

detector_parameters_list = [
    bfield,
    ptmintrk,
    ecalemin,
    hcalemin,
    sigmincal,
    etaphirescal,
    ecalnoise,
    ecalstoch,
    ecalconst,
    hcalnoise,
    hcalstoch,
    hcalconst,
]

base_detector_list = [
    detector_idea_baseline,
    detector_ideacry_baseline,
    detector_cms_baseline,
    detector_atlas_baseline,
]
var_detector_list = []

output_dir = "cards/DetectorVariation_v5/"

metrics = [
    {
        "name": "resolution",
        "label": "rel. resolution",
    },
    # {
    #    "name": "response",
    #    "label": "rel. response",
    # },
]

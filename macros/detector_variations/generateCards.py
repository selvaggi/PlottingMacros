from plot_config import *
import numpy as np

for base_det in base_detector_list:
    for parameter_list in detector_parameters_list:
        for param in parameter_list:
            det_out = copy.deepcopy(base_det)
            ##print(param)
            det_out["name"] = "{}_{}{}".format(
                base_det["name"], param["name"], param["value"]
            )
            det_out["filename"] = "{}/{}.tcl".format(output_dir, det_out["name"])
            # print(det_out["name"], det_out["filename"])
            # print(param)
            det_out["parameters"][param["name"]] = param
            # print(base_det["parameters"][param["name"]])
            # print(base_det["parameters"]["bfield"])

            var_detector_list.append(det_out)


dummy_card = "cards/dummy.tcl"

for det in var_detector_list:
    # print("")
    print(det["filename"])
    # for name, params in det_out["parameters"].items():
    # print(name, params)
    produce_delphes_card(dummy_card, det)

print("[")
for det in var_detector_list:
    # print("")
    print("  '{}',".format(det["name"]))
print("]")

print(len(var_detector_list))

import math
from collections import OrderedDict


def eta(theta):
    return -math.log(math.tan(theta / 2.0))


# _______________________________________________________________________________
class Endcap:
    def __init__(self, area, z, r_in, r_out, label, opt):

        self.label = label
        ## nose geometry
        self.area = area  # in cm2
        self.size = math.sqrt(area)  # in cm
        self.opt = opt  # 0: first, 1: middle, 2: last, 3: standalone module

        self.z = z  # z position of first layer in cm

        self.r_in = r_in  # in cm
        self.r_out = r_out  # in cm

        self.n_rings = int((self.r_out - self.r_in) / self.size)
        # print(self.n_rings)

        self.phi_str = """set PhiBins {}
        for {set i -DUMMY_NPHI} {$i <= DUMMY_NPHI} {incr i} {
            add PhiBins [expr {$i * $pi/DUMMY_NPHI}]
        }"""

        self.eta_str = "add EtaPhiBins DUMMY_ETA $PhiBins"

        self.theta_in = math.atan2(r_in, z)
        self.theta_out = math.atan2(r_out, z)

        self.eta_in = eta(self.theta_in)
        self.eta_out = eta(self.theta_out)

        self.etabins = OrderedDict()

        for i in range(self.n_rings + 1):
            r_min = r_in + i * self.size
            r_max = r_in + (i + 1) * self.size
            a_i = math.pi * (r_max ** 2 - r_min ** 2)

            n_i = int(0.5 * a_i / area)

            theta_min = math.atan2(r_min, z)
            theta_max = math.atan2(r_max, z)

            eta_max = eta(theta_min)
            eta_min = eta(theta_max)

            if i == self.n_rings:
                eta_min = self.eta_out

            self.etabins[(eta_min, eta_max)] = []

            for j in range(-n_i, n_i + 1):
                # print(n_i, (eta_min, eta_max))
                self.etabins[(eta_min, eta_max)].append(float(j) * math.pi / n_i)

    def print(self):
        print(" ")
        print("========== {} ============".format(self.label))
        print(" ")
        print("z     = {:.1f} cm".format(self.z))
        print("r_min = {:.1f} cm".format(self.r_in))
        print("r_max = {:.1f} cm".format(self.r_out))
        print("cell area = {:.1f} cm2".format(self.area))
        print(" ")
        print("eta_max = {:.2f}".format(self.eta_out))
        print("eta_min = {:.2f}".format(self.eta_in))

        print("eta bins: ")
        for etabin, phivals in self.etabins.items():
            print("  {:.2f}, {:.2f}: ".format(etabin[0], etabin[1]))
            phistr = "    "
            for phi in phivals:
                phistr += " {:.2f}".format(phi)
            print(phistr)
        print(" ")

    def print_delphes(self):

        i = 0
        for etabin, phivals in self.etabins.items():

            eta_max = etabin[1]
            eta_min = etabin[0]

            n_i = int((len(phivals) - 1.0) / 2.0)

            phi_str_i = self.phi_str.replace("DUMMY_NPHI", str(n_i))
            print(phi_str_i)

            if i == 0 and (self.opt == 0 or self.opt == 3):
                print(self.eta_str.replace("DUMMY_ETA", "{:.2f}".format(-eta_max)))

            print(self.eta_str.replace("DUMMY_ETA", "{:.2f}".format(-eta_min)))
            print(self.eta_str.replace("DUMMY_ETA", "{:.2f}".format(eta_max)))

            if i == self.n_rings and (self.opt != 1):
                print(self.eta_str.replace("DUMMY_ETA", "{:.2f}".format(eta_min)))
            i += 1


# _______________________________________________________________________________
class Barrel:
    def __init__(self, etaphi_size, etamax, label, opt):

        self.label = label
        ## nose geometry
        self.etaphi_size = etaphi_size  # in etaphi
        self.etamax = etamax  # in cm2
        self.opt = opt  # 0:last, 1: standalone module

        self.str = """
set EtaPhiRes DUMMYETAPHIRES
set EtaMax DUMMYETAMAX

set nbins_phi [expr {$pi/$EtaPhiRes} ]
set nbins_phi [expr {int($nbins_phi)} ]

set PhiBins {}
for {set i -$nbins_phi} {$i <= $nbins_phi} {incr i} {
  add PhiBins [expr {$i * $pi/$nbins_phi}]
}

set nbins_eta [expr {$EtaMax/$EtaPhiRes} ]
set nbins_eta [expr {int($nbins_eta)} ]

set nbins_eta_m [expr {int($DUMMYNBINSETA)} ]

for {set i -$nbins_eta_m} {$i <= $nbins_eta} {incr i} {
  set eta [expr {$i * $EtaPhiRes}]
  add EtaPhiBins $eta $PhiBins
}"""

    def print_delphes(self):
        self.str = self.str.replace("DUMMYETAPHIRES", str(self.etaphi_size))
        self.str = self.str.replace("DUMMYETAMAX", str(self.etamax))

        nbins = "nbins_eta"
        if self.opt == 0:
            nbins = "nbins_eta - 1"
        self.str = self.str.replace("DUMMYNBINSETA", nbins)
        print(self.str)


# _______________________________________________________________________________


def main():

    debug = False

    nose = Endcap(0.5, 1040, 31, 105, "nose", 1)
    # nose = Endcap(200, 1040, 31, 105, "nose", 1)

    if debug:
        nose.print()
    else:
        nose.print_delphes()

    hgcal_hd = Endcap(0.5, 357, 36, 80, "hgcal high density", 1)
    # hgcal_hd = Endcap(200, 357, 36, 80, "hgcal high density",  1)
    if debug:
        hgcal_hd.print()
    else:
        hgcal_hd.print_delphes()

    hgcal_ld = Endcap(1, 357, 80, 168, "hgcal low density", 1)
    # hgcal_ld = Endcap(500, 357, 80, 168, "hgcal low density",  1)
    if debug:
        hgcal_ld.print()
    else:
        hgcal_ld.print_delphes()

    central = Barrel(0.02, 1.5, "barrel", 0)
    if not debug:
        central.print_delphes()


# _______________________________________________________________________________
if __name__ == "__main__":
    main()

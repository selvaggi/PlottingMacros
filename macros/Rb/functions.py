def f1(e_b, e_c, e_uds, Rb, Rc):
    return (e_b * Rb + e_c * Rc + e_uds * (1 - Rb - Rc))


def f2(C_b, C_c, C_uds, e_b, e_c, e_uds, Rb, Rc):
    return (C_b * e_b**2 * Rb + C_c * e_c**2 * Rc + C_uds * e_uds**2 * (1 - Rb - Rc))



Nhad = 1e12
e_b = 0.9
e_c = 0.005
e_uds = 0.001
Rc = 0.1687884
Rb = 0.223144

C_b = 1
C_c = 1
C_uds = 1

fs = f1(e_b, e_c, e_uds, Rb, Rc)
fd = f2(C_b, C_c, C_uds, e_b, e_c, e_uds, Rb, Rc)

ratio = fs**2/fd


print(ratio/Rb)
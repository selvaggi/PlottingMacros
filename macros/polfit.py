
#____________________________________________________________________________________________    
    
    
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def pol(x, a, b, c):
    return a*x**2 + b*x + c

x = np.array( [0.50, 0.90, 0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.10,1.50])
y = np.array([1.92258,1.41752,1.36266,1.35191,1.34124,1.33063,1.32011,1.30965,1.29927,1.28896,1.27872,1.26856,1.25848,1.20914,0.88070])

fitting_parameters, covariance = curve_fit(pol, x, y)
a, b, c = fitting_parameters

x_min = 0  
x_max = 3                                #min/max values for x axis

x_fit = np.linspace(x_min, x_max, 100)   #range of x values used for the fit function
plt.plot(x, y, 'o', label='data')
plt.plot(x_fit, pol(x_fit, *fitting_parameters), '-', label='Fit')

plt.axis([x_min, x_max, 0, 3])
plt.legend()

#plt.show()
	

##### here predict k factor for 27 TeV based on 100 TeV ########

x = np.array( ['-1.000', '-0.500','0.000','0.500','0.750','0.800','0.850','0.875','0.900','0.925','0.950','0.975','1.000','1.025','1.050','1.075','1.100','1.125','1.150','1.200','1.250','1.500','2.000','2.500','3.000'] )

#xsec_kl100 = 0.1399* 2. * 0.58
#xsec_kl100 = 1.224 * 2. * 0.58

xsec_kl100 = 1.224 

for xval in x:

    xsec = float(pol(float(xval), *fitting_parameters) / pol(1.00, *fitting_parameters)) * xsec_kl100
    
    klstr = xval.replace('.', '')
    klstr = klstr[:-1]
    #print "'mg_pp_hh_5f_kl_{}':['HH, H->bb, H undec., kl = {}','inclusive','','{}','1.0','1.0'],".format(klstr,xval,xsec)
    
    #print "'mg_pp_hh_lambda{}_5f':['HH, H->bb, H undec., kl = {}','','','{}','1.0','1.0'],".format(klstr,xval,xsec)

    print xval,xsec

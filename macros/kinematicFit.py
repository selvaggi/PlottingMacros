import sys
import ROOT
from collections import OrderedDict
from ROOT import TMatrixD, TMath
from array import array
import numpy as np
import re
import math

debug = True
debug = False

c_light=2.99792458E8

from array import array
import sympy
from sympy import *
import numpy as np
from numpy.linalg import multi_dot, inv


def computeReplacements(variables, alpha):
    sub_list = []
    rows = alpha.shape[0]
    for i in range(rows):
        sub_list.append((variables[i],alpha[i][0]))
    return sub_list


def computeConstraintsDerivative(constraints, variables, dconstraints):
    # these are expressions
    for i in range(len(constraints)):
        dH_i = []
        for j in range(len(variables)):
            constrain_derivative = Derivative(constraints[i], variables[j]).doit()
            dH_i.append(constrain_derivative)
        dconstraints.append(dH_i)

def computeConstraintsVector(constraints, replacements):
    d = np.zeros((len(constraints),1))
    for i in range(d.shape[0]):
        Hi = constraints[i]
        d[i][0] = Hi.subs(replacements)
    return d

def computeConstraintsDerivativeMatrix(dconstraints, replacements):
    D = np.zeros((len(constraints),len(dconstraints[0])))
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            dHi_dxj = dconstraints[i][j]
            D[i][j] = dHi_dxj.subs(replacements)
    return D


def computeChiSq(matrix):
    chisqrd = 0
    for i in range(matrix.shape[0]):
        chisqrd += matrix[i][i]**2
    return chisqrd

# Make the header known to the interpreter
ROOT.gInterpreter.ProcessLine('#include "kinfitDummy.h"')


e1_0 = 94.12634072642227
e2_0 = 44.700872904171305

# expected corrected values
#e1 = 91.19000803486719
#e2 = 44.03863365342827

### various global definitions
mh = 125.
mz = 91.18800354003906
sqrt_s = 240.
s = sqrt_s**2

Eh = 0.5 * (s + mh**2 - mz**2) / sqrt_s
Ez = sqrt_s - Eh

ph = math.sqrt(Eh**2 - mh**2)
pz = math.sqrt(Ez**2 - mz**2)

# kinematic fit parameters
maxloops=100
maxDeltaChiSq = 1.e-03
weight = 1 # use weight = 1 when linear constraints

e1, e2 = symbols('e1 e2')
variables = (e1, e2)
n = len(variables)

## define constraints here
constraints = []
constraints_derivatives = []  # compute vector of dH/dxi (this is )

#cnstr1 = e1**2 + e2**3 - Eh
cnstr1 = e1 + e2 - Eh
cnstr2 = e1**2 + e2**3 - Eh
# cnstr3 = ...

constraints.append(cnstr1)
constraints.append(cnstr2)

# ...
r = len(constraints)
for i in range(r):
    print(i, "constraint expression : {}".format(constraints[i]))

constraints_derivatives = []  # compute vector of dH/dxi (this is an r x n matrix)
computeConstraintsDerivative(constraints, variables, constraints_derivatives)

for i in range(r):
    for j in range(n):
        print("dH{}/d{} = {}".format(i+1,variables[j], constraints_derivatives[i][j]))

## event loop here
for iev in range(1):
    ## fill in parameter values
    e1_0 = 94.12634072642227
    e2_0 = 44.700872904171305

    sigma1 = 0.05 * e1_0
    sigma2 = 0.05 * e2_0

    ## fill in parameters

    alpha0 = np.array([[e1_0],
                      [e2_0]])

    # and covariance matrix
    Valpha0 = np.array([[sigma1**2, 1.e-6],
                        [1.e-6, sigma2**2]])


    ## start minimisation here
    converged=False
    loops=0
    chisqrd=0.
    chisqrdlast=0.

    # initialize parameters and covariance matrix
    Valpha = Valpha0
    alpha = alpha0

    while not converged and loops < maxloops:

        print('---------------------------------- ', loops)
        # compute mapping between variables and their value
        x_to_val = computeReplacements(variables, alpha)
        #print(x_to_val)
        # returns a TMatrixD(r,1)
        d = computeConstraintsVector(constraints, x_to_val)
        #print(d)
        # returns a TMatrixD(r,n)
        D = computeConstraintsDerivativeMatrix(constraints_derivatives, x_to_val)
        #print(D)

        DT = np.transpose(D)
        #print(DT)

        VD = inv(multi_dot([D, Valpha, DT]))
        #print(VD)

        ## fix me: could be as well V * (d+D*delta_alpha)
        Lambda = VD.dot(d)
        #print(Lambda)

        LambdaT = np.transpose(Lambda)
        #print(LambdaT)

        delta_alpha = - weight * multi_dot([Valpha, DT, Lambda])

        print('Valpha',Valpha)
        print('Vd',VD)
        print('d',d)

        print('DT',DT)
        print('Lambda',Lambda)

        print('delta_alpha',delta_alpha)

        delta_alpha_T = np.transpose(delta_alpha)
        #print(delta_alpha_T)

        ## new alpha
        alpha = alpha + delta_alpha
        #print(alpha)
        print('alpha',alpha)

        # new covariance matrix
        Valpha = Valpha - Valpha * DT * VD * D * Valpha * weight
        #print(Valpha)
        print('Valpha',Valpha)

        chisqrd = computeChiSq(Valpha)
        chisqrd_v2 = multi_dot([delta_alpha_T, inv(Valpha), delta_alpha]) + 2*LambdaT.dot(d + D.dot(delta_alpha))

        #print(loops, chisqrd, chisqrdlast)
        print(loops, chisqrd,chisqrd_v2)
        #print(converged,loops,alpha[0][0],alpha[1][0])

        if loops==0: firstchisqrd = chisqrd
        loops += 1

        if abs(chisqrd - chisqrdlast) < maxDeltaChiSq:
             converged=True # good enough fit


    print('Initial values', alpha0)
    print('Final values', alpha)
    print('Initial cov.matrix', Valpha0)
    print('Final cov.matrix', Valpha)
    print('Initial chi2', firstchisqrd)
    print('Final chi2', chisqrd)

        #x_to_val = computeReplacements(variables, alpha0)
    	#D = computeConstraintsDerivativeMatrix(constraints_derivatives, x_to_val)

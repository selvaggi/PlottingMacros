import math

pt=5.
eta=2
mass=2.

# in seconds
tau=300e-9

#xmin=10.
#xmax=10.5


xmin=0.
xmax=1.

#speed of light
c=3.e+8

energy=pt*math.cosh(eta)

gamma=energy/mass

gct = gamma*c*tau

efficiency=math.exp(-xmin/gct) - math.exp(-xmax/gct) 

print 'tau           =   {:.3f} ns'.format(tau*1e9)
print 'gamma         =   {:.3f} '.format(gamma)
print 'ctau          =   {:.3f} m'.format(c*tau)
print 'gamma*c*tau   =   {:.3f} m'.format(gct)
print 'efficiency    =   {:.5f} '.format(efficiency)



#!/usr/bin/env python

import numpy as np
from matplotlib.pyplot import * 

P_mech = np.linspace(0, 100, 11)
omega = [0., 30., 60., 80., 95., 100., 105., 115., 135., 160., 200.]

cofs = np.polyfit(P_mech, omega, 4)
polynomial = np.poly1d(cofs)
P_mechs = np.arange(0, 100, 1)
omegas = polynomial(P_mechs)

print cofs
#print poly
#print omegas

plot(P_mech, omega, 'o')
plot(P_mechs, omegas)
ylabel('omega')
xlabel('Power load')
xlim(0, 110)
ylim(0, 210)
suptitle('plot thing', fontsize=20)
show()


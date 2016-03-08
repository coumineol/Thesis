import numpy as np
from scipy.special import betainc,beta
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def showColorGraph(z):

    Z = np.zeros((16, 16))

    counter = 0
    for i in range(0,16):
        for j in range(0,16):
            Z[i,j] = z[counter]
            counter += 1
    print(Z)


    im=plt.imshow(Z,extent=[4.2-(1/32),5.1+(1/32),-40-(4.5/32),50+(4.5/32)],origin='lower',alpha=1,aspect='auto')
    plt.colorbar()
    plt.xlabel(r'$\gamma$', size=20)
    plt.ylabel('c', size=20)
    plt.show()

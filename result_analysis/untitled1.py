# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:35:46 2020

@author: r0772291
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
x=np.arange(-1000,1000)*0.01
y=np.arange(-1000,1000)*0.01
f=np.multiply((1-x),(1-y))
f = np.multiply(f,(x+y))
fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(x,y,f,rstride=1,cstride=1,cmap='rainbow')
plt.show()
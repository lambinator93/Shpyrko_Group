"""
Author: Erik Lamb
Organization: Shpyrko Group, UC San Diego
Date: 01/10/2020
Description: This code plots 2D images of X-Ray Diffraction data embedded in an hdf5 file. The
number of detector images depends on the number of energies used. This creates a slider
plot to observe the 2D detector images for each energy sampled in sequential order. Could easily 
be modified for other parameters or data types.
"""

#!/usr/bin/env python
# coding: utf-8

import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


#Declare hdf5 object and extract energy and detector data
filename1 = 'scan_0229'
f1 = h5py.File(filename1+'.nxs', 'r') #must declare object here to use throughout
en1 = list(f1['/'+filename1+'/scan_data/data_15/'])
det1 = list(f1['/'+filename1+'/scan_data/data_17/'])

idx0 = 0
l = plt.imshow(det1[idx0])

#Set contrast limits
cmin = 200
cmax = 1300
l.set_clim(cmin,cmax)

#Create plot
axidx = plt.axes([0.19, 0.025, 0.65, 0.03])
slidx = Slider(axidx, 'Energy', 0, len(en1)-1, valinit=idx0, valfmt='%d')
slidx.valtext.set_text(str(en1[idx0]))
slidx.label.set_size(18)
slidx.valtext.set_size(18)

#Create Slider
def update(val):
    idx = slidx.val
    l.set_data(det1[int(idx)])
    l.set_clim(cmin,cmax)
    slidx.valtext.set_text(str(en1[int(idx)]))
#    fig.canvas.draw_idle()
slidx.on_changed(update)

plt.show()


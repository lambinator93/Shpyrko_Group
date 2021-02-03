
"""
Author: Erik Lamb
Organization: Shpyrko Group, UC San Diego
Date: 01/10/2020
Description: This code merges two corresponding sets of 3-dimensional data embedded in hdf5 files using a spatial 
correlation method and plots the result in an interactive slider plot. In this case, the data are x-ray diffraction
images at two separate, vertical positionsand  for many different energies that must be stitched together for visualization.
"""
#!/usr/bin/env python
# coding: utf-8

import h5py
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

###This section defines the functions used for correlation###
def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)

    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r


enind = 60 #This is a random energy index used for correlation. This was chosen solely based on the number of visual features to correlate.

#The two corresponding files to correlate. These could be added to a filepath by modifying f1 &f2
filename1 = 'scan_0225';
filename2 = 'scan_0229';

#Create hdf5 objects and energy and detector lists
f1 = h5py.File(filename1+'.nxs', 'r'); #must declare object here to use throughout
en1 = list(f1['/'+filename1+'/scan_data/data_15/']);
det1 = list(f1['/'+filename1+'/scan_data/data_17/']);

f2 = h5py.File(filename2+'.nxs', 'r'); #must declare object here to use throughout
en2 = list(f2['/'+filename2+'/scan_data/data_15/']);
det2 = list(f2['/'+filename2+'/scan_data/data_17/']);

###This section finds the index of highest correlation.
corr = np.zeros(len(det2[enind]));

for i in range(1,len(det2[enind])):
    #print(i)
    for j in range(0,i):
        #print(j)
        corr[i-1] = (corr2(det1[enind][len(det1[enind])-i-j,:],det2[enind][i-j,:])+corr[i-1]);
    
    corr[i-1] = corr[i-1]/(len(det2[enind])*i)

idx = np.where(corr == np.amax(corr))

###This section merges the two data sets###
det = np.zeros((len(det2[enind])*2-idx[0][0]+1,len(det2[enind])))
DET = []

for en in range(0,len(en1)):
    for i in range(0,det.shape[0]-1):
        if i<(len(det2[en])-idx[0][0]-2):
            #print(i)
            det[i,:] = det1[en][i,:];
        if (len(det2[en])-idx[0][0]-2) <= i < (len(det2[en])-1):
            #print(i)
            det[i,:] = (det1[en][i,:]+det2[en][i-(len(det2[en])-idx[0][0]-2),:])/2
        if (len(det2[en])-1) <= i:
            #print(i-len(det2[enind])+idx[0][0])
            det[i,:] = det2[en][i-len(det2[en])+idx[0][0],:]
    DET.append(det)
    det = np.zeros((len(det2[enind])*2-idx[0][0]+1,len(det2[enind])))

###This section creates the slider plot###
idx0 = 0
l = plt.imshow(DET[idx0])

cmin = 200
cmax = 1300
l.set_clim(cmin,cmax)

axidx = plt.axes([0.19, 0.025, 0.65, 0.03])
slidx = Slider(axidx, 'Energy', 0, len(en1)-1, valinit=idx0, valfmt='%d')
slidx.valtext.set_text(str(en1[idx0]))
slidx.label.set_size(18)
slidx.valtext.set_size(18)

def update(val):
    idx = slidx.val
    l.set_data(DET[int(idx)])
    l.set_clim(cmin,cmax)
    slidx.valtext.set_text(str((en1[int(idx)]+en2[int(idx)])/2))
#    fig.canvas.draw_idle()
slidx.on_changed(update)

plt.show()


     

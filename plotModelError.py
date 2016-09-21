# plotModelError.py
# Script to plot out the model forecast error figure (sea ice, ocean, atmo componeents)
# Note that I need to add in the shifts where two model setups are the same - I kinda bodged this last time..
# Alek Petty

import matplotlib
matplotlib.use("AGG")
import sys
# Numpy import
import numpy as np
from pylab import *
import pandas as pd

#FIGURE PARAMETERS
rcParams['axes.labelsize'] =8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

#2015 extent
obsExtent = 4.63
minval=-1.
maxval=1.

figpath='./Figures'

# use Pandas to read in data and put into categories..
file = pd.read_csv('./Data/SIOMODELDATA2015_PETTY.csv')

Names=file['Name'].values
OceanModel=pd.Categorical(file['OceanModel'])
OceanModelCat=OceanModel.rename_categories(np.arange(file['OceanModel'].nunique()))
OceanModelCatA=np.asarray(OceanModelCat)

SeaIceModel=pd.Categorical(file['SeaIceModel'])
SeaIceModelCat=SeaIceModel.rename_categories(np.arange(file['SeaIceModel'].nunique()))
SeaIceModelCatA=np.asarray(SeaIceModelCat)


AtmoModel=pd.Categorical(file['AtmoModel'])
AtmoModelCat=AtmoModel.rename_categories(np.arange(file['AtmoModel'].nunique()))
AtmoModelCatA=np.asarray(AtmoModelCat)

SeaIceCats=np.array(SeaIceModel.categories)
OceanCats=np.array(OceanModel.categories)
AtmoCats=np.array(AtmoModel.categories)

BiasCorrect=file['BiasCorrect'].values
IceExtent=file['IceExtent'].values

#assign model numbers
modelNum=[str(x) for x in xrange(1,size(IceExtent)+1)]

modelLabs=''
for x in xrange(size(Names)):
	modelLabs+=str(x+1)+'. '+Names[x]+'\n'

diff = [IceExtent[x]-obsExtent for x in xrange(size(IceExtent))]

fig = figure(figsize=(6,3))
#### AX1 ###
ax1 = subplot(1, 2, 1)

im1 = scatter(ma.masked_where(BiasCorrect<0.5, SeaIceModelCatA), OceanModelCatA, 
	c=diff, s=130, marker='o',cmap=cm.RdYlBu, vmin=minval-0.01, vmax=maxval+0.01,rasterized=True)
im2 = scatter(ma.masked_where(BiasCorrect>0.5, SeaIceModelCatA), OceanModelCatA, 
	c=diff, s=130, marker='s',cmap=cm.RdYlBu, vmin=minval-0.01, vmax=maxval+0.01, rasterized=True)

for x in xrange(size(modelNum)):
	im3 = text(SeaIceModelCatA[x], OceanModelCatA[x], modelNum[x],  fontsize=8, horizontalalignment='center',verticalalignment='center')

ax1.yaxis.grid(True)
ax1.xaxis.grid(True, which='major')

ax1.yaxis.set_major_locator(FixedLocator(np.arange(0, size(OceanCats))))
ax1.yaxis.set_minor_locator(FixedLocator(np.arange(-0.5, size(OceanCats)+0.5)))
ax1.set_ylim(-0.5, size(OceanCats)-0.5)
ax1.set_yticklabels(OceanCats, rotation=30, rotation_mode="anchor")
ax1.set_yticklabels([], minor=True)
ax1.yaxis.grid(True, which="minor")
ax1.yaxis.grid(False, which="major")

ax1.xaxis.set_major_locator(FixedLocator(np.arange(0, size(SeaIceCats))))
ax1.xaxis.set_minor_locator(FixedLocator(np.arange(-0.5, size(SeaIceCats)+0.5)))
ax1.set_xlim(-0.5, np.size(SeaIceCats)-0.5)
ax1.set_xticklabels(SeaIceCats, rotation=25)
ax1.set_xticklabels([], minor=True)
ax1.xaxis.grid(True, which="minor")
ax1.xaxis.grid(False, which="major")
ax1.set_ylabel( 'Ocean model', labelpad=0)


#### AX2 ###
ax2 = subplot(1, 2, 2)

im21 = scatter(ma.masked_where(BiasCorrect<0.5, SeaIceModelCatA), AtmoModelCatA, c=diff, s=130, marker='o',cmap=cm.RdYlBu, vmin=minval-0.01, vmax=maxval+0.01,rasterized=True)
im22 = scatter(ma.masked_where(BiasCorrect>0.5, SeaIceModelCatA), AtmoModelCatA, c=diff, s=130, marker='s',cmap=cm.RdYlBu, vmin=minval-0.01, vmax=maxval+0.01, rasterized=True)

for x in xrange(size(modelNum)):
	im23 = text(SeaIceModelCatA[x]-0.01, AtmoModelCatA[x], modelNum[x],  fontsize=8, horizontalalignment='center',verticalalignment='center')

ax2.yaxis.grid(True)
ax2.xaxis.grid(True, which='major')

ax2.yaxis.set_major_locator(FixedLocator(np.arange(0, size(AtmoCats))))
ax2.yaxis.set_minor_locator(FixedLocator(np.arange(-0.5, size(AtmoCats)+0.5)))
ax2.set_ylim(-0.5, size(AtmoCats)-0.5)
ax2.set_yticklabels(AtmoCats, rotation=30, rotation_mode="anchor")
ax2.set_yticklabels([], minor=True)
ax2.yaxis.grid(True, which="minor")
ax2.yaxis.grid(False, which="major")
ax2.set_ylabel( 'Atmo model/reanalysis', labelpad=0)

ax2.xaxis.set_major_locator(FixedLocator(np.arange(0, size(SeaIceCats))))
ax2.xaxis.set_minor_locator(FixedLocator(np.arange(-0.5, size(SeaIceCats)+0.5)))
ax2.set_xlim(-0.5, np.size(SeaIceCats)-0.5)
ax2.set_xticklabels(SeaIceCats, rotation=25)
ax2.set_xticklabels([], minor=True)
ax2.xaxis.grid(True, which="minor")
ax2.xaxis.grid(False, which="major")
ax2.set_ylabel( 'Atmosphere model/reanalyses', labelpad=0)


ax2.annotate(modelLabs, xy=(1.01, 0.99), xycoords='axes fraction', horizontalalignment='left', verticalalignment='top')

cax = fig.add_axes([0.71, 0.26, 0.1, 0.03])
cbar = colorbar(im21,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_ticks(np.linspace(minval, maxval, 3))
cbar.solids.set_rasterized(True)
cbar.set_label(r'Error (10$^{6}$ km)', labelpad=0)


subplots_adjust( right = 0.85, left = 0.1, top=0.99, bottom=0.13, wspace=0.45)

savefig(figpath+'/modelResults.pdf', dpi=300)

close(fig)










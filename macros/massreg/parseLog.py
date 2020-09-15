#python /afs/cern.ch/work/s/selvaggi/private/HCC/NNTools/training/logs/mass_regression_ak15_2020025_20epochs_dilution10.log plots_massreg/test.png


import os, sys
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from scipy import stats
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import BoundaryNorm
import multiprocessing as mp



inputFile = sys.argv[1]
outputFile = sys.argv[2]


log=inputFile


def produceLossArray(log ,val_str, list_loss):

    if os.path.exists(log):
        with open(log) as f:
          for line in f:
            if line.find(val_str):
              list_of_words = line.split()
              if any(val_str in s for s in list_of_words):
                 found=True
                 loss_str = list_of_words[4]

                 loss = loss_str.split("=")[1]
                 list_loss.append(float(loss))
                 #print val_str, ' : ', loss


list_mse = []
list_mae = []
list_hub = []

produceLossArray(log ,'Validation-mse', list_mse)
produceLossArray(log ,'Validation-mae', list_mae)
produceLossArray(log ,'Validation-huber_loss', list_hub)

nd = np.arange(1,len(list_mse)+1)

data_mse = np.sqrt(list_mse)
data_mae = np.array(list_mae)
data_hub = np.array(list_hub)

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(nd, data_mse, label='mse', linewidth=2)
ax.plot(nd, data_mae, label='mae', linewidth=2)
ax.plot(nd, data_hub, label='hub', linewidth=2)


ax.set_title('losses vs epoch')
ax.legend(loc='upper right')
ax.set_ylabel('losses')
ax.set_xlabel('epoch #')
ax.set_xlim(xmin=nd[0], xmax=nd[-1])

grid_x_ticks = np.arange(0, len(nd), 1)

ax.set_xticks(grid_x_ticks , minor=True)

ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
ax.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)

#ax.set_ylim(ymin=0, ymax=80.)



fig.tight_layout()
#fig.show()
fig.savefig(outputFile)

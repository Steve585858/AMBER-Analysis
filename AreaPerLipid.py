
import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MD import MD

class AreaPerLipid(MD):

    def generate(self):
        traj = pt.iterload(self.files, os.path.join(self.data_path, self.prmtop))
        areas = np.zeros(len(traj))

        for findex, f in enumerate(traj):
            x, y, z, alpha, beta, gamma = f.box
            areas[findex] = x*y/256.0
        np.savetxt(os.path.join(self.results_path, self.base+'_area_per_lipid.txt'), areas)

    def read(self):
        areas = np.loadtxt(os.path.join(self.results_path, self.base+'_area_per_lipid.txt'))
        print("{} : {}".format(self.base, areas.shape))
        return areas

    def getOriginalData(self):
        return self.read()

    def plot(self):
        areas = self.read()
        window_size = 101
        mean_ma = np.convolve(areas, np.ones(window_size), 'valid') / window_size
        df = pd.DataFrame({ 'Area Per Lipid': mean_ma })
        colNames=df.columns.values.tolist()
        print(df.info())
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        #fig.suptitle('Dihedral Angle Count', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            col.plot()
            
        plt.xlabel("Frame #") 
        plt.ylabel("Area Per Lipid (Angstrom^2/lipid)")
        plt.title("Area Per Lipid vs Frame")
        #outputFilename = os.path.join(self.images_path, self.base+"_area_per_lipid.png")
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
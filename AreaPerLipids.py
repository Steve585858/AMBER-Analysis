import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from AreaPerLipid import AreaPerLipid

class AreaPerLipids():

    def __init__(self, type, data_path_list, file_list, prmtop):
        self.type = type
        self.data_path_list = data_path_list
        self.file_list = file_list
        self.prmtop = prmtop
        self.base_list = []
        self.da_list = []
        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        for index,  data_path in enumerate(data_path_list):
            base = data_path
            self.base_list.append(base)
            da = AreaPerLipid(0, data_path, base, file_list[index], prmtop)
            self.da_list.append(da)
    
    def plot(self):
        iMethod = 0
        frameMean = np.zeros(len(self.da_list))
        temperatures = np.zeros(len(self.da_list), dtype=int)
        for index, da in enumerate(self.da_list):
            data = da.getOriginalData()
            frameMean[index] = np.mean(data)
            a, b, c = da.parseBase()
            temperatures[index] = b
        df = pd.DataFrame(frameMean, index=temperatures, columns=['1 Bar'])
        df.index.name = 'Temperature'
        base = self.base_list[0]
        outputFilename = os.path.join(self.results_path, base+"_11"+"_areaPerlipid_plot.csv")
        df.to_csv(outputFilename, sep=',', index=True)
        print(df)
        ax = df.plot(use_index=True, marker="o") 
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Average Area Per Lipid (Angstrom^2/lipid)")
        plt.title("Temperature vs Area Per Lipid")
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
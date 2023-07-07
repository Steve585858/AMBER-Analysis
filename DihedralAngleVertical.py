import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from DihedralAngle import DihedralAngle

class DihedralAngleVertical():

    def __init__(self, type, path_list, base_list, file_list, prmtop):
        self.type = type
        self.path_list = path_list
        self.base_list = base_list
        self.file_list = file_list
        self.prmtop = prmtop
        self.base_list = []
        self.da_list = []
        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        for index,  base in enumerate(base_list):
            self.base_list.append(base)
            da = DihedralAngle(0, path_list[index], base, file_list[index], prmtop)
            self.da_list.append(da)
        
    def plotCount(self):
        dfs = []
        #columnNames = ["1Bar", "300Bar", "600Bar"]
        for index, da in enumerate(self.da_list):
            a, b, c = da.parseBase()
            results = da.flatten()
            count = np.bincount(results)
            percentages = 100.0*count/len(results)
            df = pd.DataFrame({ "{}B_{}K".format(c,b): percentages })
            dfs.append(df)
        df = pd.concat(dfs, axis = 1)
        ax = df.plot() 
        ax.set_xlabel("Dihedral Angle (degree)")
        ax.set_ylabel("Percentage (%)")
        plt.title('Dihedral Angle Percentage')
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
        
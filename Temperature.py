import os
import pandas as pd
import matplotlib.pyplot as plt

class Temperature():

    def __init__(self, type, files):
        self.type = type
        self.files = files

        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        self.images_path = os.path.join(cwd, 'images')

    def parseFiles(self):
        dfs = []
        for i, f in enumerate(self.files):
            df = pd.read_csv(os.path.join(self.results_path, f), index_col = 0)
            dfs.append(df)
        df = pd.concat(dfs, axis = 1)
        self.df = df.abs()
        print(self.df)
    
    def plot(self, title, xlabel, ylabel):
        ax = self.df.plot(use_index=True, marker="o") 
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.title(title)
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
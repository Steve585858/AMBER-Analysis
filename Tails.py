import os
import pytraj as pt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Tail import Tail

class Tails():

    def __init__(self, type, data_path_list, file_list, prmtop):
        self.type = type
        self.data_path_list = data_path_list
        self.file_list = file_list
        self.prmtop = prmtop
        self.base_list = []
        self.tail_list = []
        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        for index,  data_path in enumerate(data_path_list):
            base = data_path
            self.base_list.append(base)
            tail = Tail(0, data_path, base, file_list[index], prmtop)
            self.tail_list.append(tail)
    
    def plotItem(self, itemIndex):
        item = None
        frameMean = np.zeros(len(self.tail_list))
        temperatures = np.zeros(len(self.tail_list), dtype=int)
        for index, tail in enumerate(self.tail_list):
            item = tail.items[itemIndex]
            data = tail.getDataDetails(itemIndex)
            frameMean[index] = np.mean(data)
            a, b, c = tail.parseBase()
            temperatures[index] = b
        df = pd.DataFrame(frameMean, index=temperatures, columns=['300 Bar'])
        print(df)
        ax = df.plot(use_index=True, marker="o") 
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Average {}".format(item))
        plt.title("Temperature vs {}".format(item))
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
        
    def plotItemSD(self, itemIndex):
        item = None
        frameMean = np.zeros(len(self.tail_list))
        temperatures = np.zeros(len(self.tail_list), dtype=int)
        for index, tail in enumerate(self.tail_list):
            item = tail.items[itemIndex]
            data = tail.getDataDetailsSD(itemIndex)
            frameMean[index] = np.mean(data)
            a, b, c = tail.parseBase()
            temperatures[index] = b
        df = pd.DataFrame(frameMean, index=temperatures, columns=['600B'])
        df.index.name = 'temperature'
        base = self.base_list[0]
        outputFilename = os.path.join(self.results_path, base+"_"+str(itemIndex)+"_tails_plot.csv")
        df.to_csv(outputFilename, sep=',', index=True)
        print(df)
        ax = df.plot(use_index=True, marker="o") 
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Average {}".format(item))
        plt.title("Temperature vs {}".format(item))
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
    
    def plot(self):
        itemIndexs = [6,7,8,9,10]
        frameMean = np.zeros((len(self.tail_list), len(itemIndexs)))
        temperatures = np.zeros(len(self.tail_list), dtype=int)
        
        for index, tail in enumerate(self.tail_list):
            for itemIndex in itemIndexs:
                item = tail.items[itemIndex]
                data = tail.getDataDetails(itemIndex)
                frameMean[index][itemIndex-6] = np.mean(data)
            a, b, c = tail.parseBase()
            temperatures[index] = b

        colNames = []
        for itemIndex in itemIndexs:
            colNames.append(self.tail_list[0].items[itemIndex])
        df = pd.DataFrame(data=frameMean, index=temperatures, columns=colNames)
        print(df)

        nSubPlots = len(colNames)
        fig,axes = plt.subplots(nSubPlots, 1, figsize=(7,10), sharex=True)
        #fig.suptitle('Tail vs Temperature', fontsize=14)
        for i, col in enumerate(df.columns):
            ax = axes[i]
            ax.plot(df[col], marker="o")
            ax.set_title("Temperature vs {}".format(col))
            ax.set_ylabel("Average {}".format(col))
            #ax.set_xlabel("Temperature (K)")
        axes[-1].set_xlabel("Temperature (K)")
        #plt.xlabel(df.index.name)
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
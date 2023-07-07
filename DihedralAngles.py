import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from DihedralAngle import DihedralAngle

class DihedralAngles():

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
            da = DihedralAngle(0, data_path, base, file_list[index], prmtop)
            self.da_list.append(da)

    def plotResMeanEach(self, resIndex):
        iMethod = 1
        df = pd.DataFrame()
        for index, da in enumerate(self.da_list):
            colName = "{}_res{}_mean".format(self.base_list[index], resIndex)
            data = da.getDataRes(resIndex)
            mean = np.mean(data, axis=1)
            if iMethod==0:
                df[colName] = mean
            elif iMethod==1:
                window_size = 101
                mean_ma = np.convolve(mean, np.ones(window_size), 'valid') / window_size
                df[colName] = mean_ma
            elif iMethod==2:
                countArray = np.bincount([int(i) for i in np.rint(data).flatten()])
                print("countArray={}".format(len(countArray)))
                df[colName] = countArray
        colNames = df.columns
        print(colNames)

        nSubPlots = 1
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        #fig.suptitle('Res_CC vs Frame Index', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index//20+1)
            col = pd.to_numeric(df[colName].squeeze())
            col.plot() 
            plt.legend(loc='lower right')
        plt.xlabel("Frame #")
        plt.ylabel("Dihedral Angle Mean")
        plt.title("Frame vs Dihedral Angle for Residue {}".format(resIndex))
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()

    def plotFrameMeanEach(self, frameIndex):
        iMethod = 1
        df = pd.DataFrame()
        frameMean = np.ones(len(self.da_list))
        temperatures = np.ones(len(self.da_list), np.int8)
        for index, da in enumerate(self.da_list):
            colName = "{}_f{}_count".format(self.base_list[index], frameIndex)
            data = da.getDataFrame(frameIndex)
            mean = np.mean(data, axis=1)
            if iMethod==0:
                df[colName] = mean
            elif iMethod==1:
                window_size = 101
                mean_ma = np.convolve(mean, np.ones(window_size), 'valid') / window_size
                df[colName] = mean_ma
            elif iMethod==2:
                countArray = np.bincount([int(i) for i in np.rint(data).flatten()])
                print("countArray={}".format(len(countArray)))
                df[colName] = countArray
        colNames = df.columns
        print(colNames)
        
        nSubPlots = 1
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        #fig.suptitle('Res_CC vs Frame Index', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index//20+1)
            col = pd.to_numeric(df[colName].squeeze())
            col.plot() 
            plt.legend(loc='lower right')
        plt.xlabel("Residue #")
        plt.ylabel("Dihedral Angle Mean")
        plt.title("Residue vs Dihedral Angle for Frame {}".format(frameIndex))
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
    
    def plotFrameMeanOverall(self, frameIndex):
        iMethod = 0
        frameMean = np.zeros(len(self.da_list))
        temperatures = np.zeros(len(self.da_list), dtype=int)
        for index, da in enumerate(self.da_list):
            data = None
            if frameIndex<0:
                data = da.getOriginalData()
            else:
                data = da.getDataFrame(frameIndex)
            frameMean[index] = np.nanmean(data)
            a, b, c = da.parseBase()
            temperatures[index] = b
        
        df = pd.DataFrame(frameMean, index=temperatures, columns=['600 Bar'])
        df.index.name = 'Temperature'
        base = self.base_list[0]
        outputFilename = os.path.join(self.results_path, base+"_11"+"_dihedralAngle_plot.csv")
        df.to_csv(outputFilename, sep=',', index=True)
        print(df)
        ax = df.plot(use_index=True, marker="o") 
        ax.set_xlabel("Temperature (K)")
        #ax.set_ylabel("Average Dihedral Angle for Frame_{}".format(frameIndex))
        ax.set_ylabel("Average Dihedral Angle")
        plt.title("Temperature vs Dihedral Angle")
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
        
    def plotCount(self):
        results = []
        for index, da in enumerate(self.da_list):
            results += da.flatten()
        count = np.bincount(results)
        percentages = 100.0*count/len(results)
        values = np.arange(len(count))
        print(values)
        print(percentages)
        df = pd.DataFrame({ 'Percentage': percentages })
        df = pd.read_csv(os.path.join(self.results_path, self.base+'_dihedral_percentage.csv'), sep=",", header=None, names=['dihedral_count'])
        colNames=df.columns.values.tolist()
        print(df.info())
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        fig.suptitle('Dihedral Angle Percentage', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot()
            
        plt.xlabel("Dihedral Angle") 
        #plt.legend(loc='lower right')
        #print(df.info)
        #outputFilename = os.path.join(self.images_path, self.base+"_dihedral_count.png")
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
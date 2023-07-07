
import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from SCD import SCD

class SCDS():

    def __init__(self, type, data_path_list, file_list, prmtop):
        self.type = type
        self.data_path_list = data_path_list
        self.file_list = file_list
        self.prmtop = prmtop
        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        self.base_list = []
        self.scd_list = []
        for index,  data_path in enumerate(data_path_list):
            base = data_path
            self.base_list.append(base)
            scd = SCD(0, data_path, base, file_list[index], prmtop)
            self.scd_list.append(scd)
    
    def plotFrameMeanOverall(self, frameIndex):
        frameMean = np.zeros(len(self.scd_list))
        temperatures = np.zeros(len(self.scd_list), dtype=int)
        for index, scd in enumerate(self.scd_list):
            data = None
            simplifiedData = scd.getSimplifiedData()
            if frameIndex<0:
                data = simplifiedData
            else:
                for fIndex,  sd in enumerate(simplifiedData):
                    if fIndex==frameIndex: 
                        data = sd
                        break

            frameMean[index] = np.mean(data)
            a, b, c = scd.parseBase()
            temperatures[index] = b
            print("index={} f={} t={}".format(index, frameMean[index], temperatures[index]))
        
        df = pd.DataFrame(frameMean, index=temperatures, columns=['600 Bar'])
        base = self.base_list[0]
        outputFilename = os.path.join(self.results_path, base+"_"+str(frameIndex)+"_SCD_plot.csv")
        df.to_csv(outputFilename, sep=',', index=True)
        print(df)
        ax = df.plot(use_index=True, marker="o") 
        ax.set_xlabel("Temperature (K)")
        if frameIndex<0:
            ax.set_ylabel("Average SCD for All Frames")
        else:
            ax.set_ylabel("Average SCD for Frame_{}".format(frameIndex))
        plt.title("Temperature vs SCD")
        outputFilename = ""
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()

    def plotScdVsFrame(self, resIDs, c_name):
        df_list = []
        for index, scd in enumerate(self.scd_list):
            df1 = scd.getScdData(resIDs, c_name)
            for col in df1.columns:
                new_col = "{}_{}".format(self.base_list[index], col)
                df1.rename(columns={col:new_col}, inplace=True)
            df_list.append(df1)
        df = pd.concat(df_list, axis=1)
        colNames = df.columns

        iMethod = 2

        if iMethod==0:
            nSubPlots = len(colNames)/2
            fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
            fig.suptitle('SCD vs Frame Index', fontsize=18)
            for index, colName in enumerate(colNames):
                plt.subplot(nSubPlots, 1, index//2+1)
                col = pd.to_numeric(df[colName].squeeze())
                plt.ylabel(colName+" SCD")
                col.plot() 
                plt.legend(loc='upper right')
        elif iMethod==1:
            nSubPlots = 1
            fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
            fig.suptitle('SCD vs Frame Index', fontsize=18)
            for index, colName in enumerate(colNames):
                if index%2==0:
                    continue
                plt.subplot(nSubPlots, 1, index//20+1)
                col = pd.to_numeric(df[colName].squeeze())
                plt.ylabel("SCD")
                col.plot() 
                plt.legend(loc='lower right')
        elif iMethod==2:
            column_averages = df.mean()
            df_means = pd.DataFrame({'Column_mean':column_averages})
            df = df_means.iloc[::2]
            print(df)
            temp_list = [305, 310, 315]
            df.rename(index=dict(zip(df.index,temp_list)), inplace=True)
            print(df)
            ax = df.plot(use_index=True, marker="o") 
            ax.set_xlabel("Temperature (K)")
            ax.set_ylabel("Average SCD for res_{}_c_{}".format(resIDs[0], c_name))
        plt.title("Temperature vs SCD")
        outputFilename = ""
        #outputFilename = os.path.join(self.images_path, self.base+"_scd.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()

    def plotScdGrid(self):
        xdim, ydim = (64, 64)
        cols = []
        for i in range(0, xdim):
            cols.append("c{}".format(i))
        idx = []
        for i in range(0, ydim):
            idx.append("i{}".format(i))
            
        df = pd.read_csv(os.path.join(self.results_path, self.base+'_scd_grid.txt'), sep=" ", header=None, names=cols)
        df1 = df.drop(['c0'], axis=1)
        df2 = df1.tail(-1)
        
        #sns.heatmap(df2, cmap ='RdYlGn', linewidths = 0.030, annot = True)
        #print(df2)
        plt.imshow(df2, cmap ="RdYlBu")
        plt.colorbar()
        plt.xticks(range(len(df2)), df2.columns)
        plt.yticks(range(len(df2)), df2.index)
        outputFilename = os.path.join(self.images_path, self.base+"_scd_grid.png")
        outputFilename = ''
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()


    def extract(self, xyz_scd_array, tail_index, carbon=10):
        m = len(self.CH2_carbon)
        carbon_index = -1
        try:
            carbon_index = self.CH2_carbon.index(carbon)
        except ValueError:
            carbon_index = -1
        
        resID = tail_index*m
        scd_list = []
        if carbon_index >= 0:
            resID += carbon_index
            for i, f in enumerate(xyz_scd_array):
                ch2 = f[resID]
                scd_list.append(ch2[-1])
        else :
            for i, f in enumerate(xyz_scd_array):
                sum = 0.0
                for j in range(m) :
                    sum += float(f[resID+j][-1])
                scd_list.append(sum/m)

        return scd_list
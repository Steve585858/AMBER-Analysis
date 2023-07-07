
import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MD import MD

class SCD(MD):

    def generate(self):
        traj = pt.iterload(self.files, os.path.join(self.data_path, self.prmtop))
        top = traj.top

        c_list = []
        for i in range(top.n_residues):
            res = top.residue(i)
            if top.residue(i).name == 'PA':
                for c_name_index in self.CH2_carbon:
                    c_list.append(top.select(':{}@C{}'.format(i+1, c_name_index))[0])

        m = len(traj)
        n = len(c_list)
        print("m = {}  n = {}".format(m, n))
        #xyz_scd_array = np.zeros(m, n, 10)  # #frames x #CH2 in PA x (x/y/z_c/h1/h2, SCD)
        xyz_scd_array = np.zeros((len(traj), len(top.select(':PA@/C')) - len(top.select(':PC@/P')) *2, 10))
        print("xyz_scd_array shape = {}".format(xyz_scd_array.shape))
        # retrieve coordinates of methylene carbon in PA and assocated Hs, calculate SCD
        print('generating site-specific scd')
        for i, f in enumerate(traj):
            for j, c_index in enumerate(c_list):
                xyz_scd_array[i,j,:3] = [f.xyz[c_index][0] % f.box.x, f.xyz[c_index][1] % f.box.y, f.xyz[c_index][2] % f.box.z]   # x/y/z of carbon; move atoms back into box
                v1 = f.xyz[c_index+1] - f.xyz[c_index]
                v2 = f.xyz[c_index+2] - f.xyz[c_index]  # assuming the indices of the two hydrogens in each methylene follow immediately that of the carbon, works for PA
                xyz_scd_array[i][j][3:6] = xyz_scd_array[i,j,:3] + v1   # coords of H1
                xyz_scd_array[i][j][6:9] = xyz_scd_array[i,j,:3] + v2   # coords of H2
                v1 /= np.linalg.norm(v1)
                v2 /= np.linalg.norm(v2)
                #theCos = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
                #xyz_scd_array[i][j][9] = (3*theCos**2 - 1 )/2
                xyz_scd_array[i][j][9] = ((v1[2] **2 + v2[2] **2) /2 *3 -1) /2  # SCD = <3*cos(q)**2-1>/2
        np.save(os.path.join(self.results_path, self.base+'_scd.npy'), xyz_scd_array)

        # 2d gridding
        xdim, ydim = (64, 64)
        print('mapping scd onto xy grid')
        xmin, ymin = np.min(xyz_scd_array, axis=(0,1))[:2]
        xmax, ymax = np.max(xyz_scd_array, axis=(0,1))[:2]
        xgrid = np.linspace(xmin, xmax, xdim)
        ygrid = np.linspace(ymin, ymax, ydim)
        scd_grid = np.zeros((xdim, ydim))
        bin_count = np.zeros((xdim, ydim))
        for f in xyz_scd_array:
            for ch2 in f:
                nx = np.digitize(ch2[:1], xgrid, right=True)
                ny = np.digitize(ch2[1:2], ygrid, right=True)
                scd_grid[nx,ny] += ch2[-1]
                bin_count[nx,ny] += 1
        scd_grid = np.true_divide(scd_grid, bin_count)
        np.savetxt(os.path.join(self.results_path, self.base+'_scd_grid.txt'), scd_grid)

    def read(self):
        xyz_scd_array = np.load(os.path.join(self.results_path, self.base+'_scd.npy'))
        print("{} : {}".format(self.base, xyz_scd_array.shape))
        return xyz_scd_array

    def getOriginalData(self):
        return self.read()

    def getSimplifiedData(self):
        xyz_scd_array = self.read()
        m, i, j = xyz_scd_array.shape
        k = len(self.CH2_carbon)
        n = i/k

        scd_array = np.zeros((m, n, k))
        print("scd_array shape = {}".format(scd_array.shape))
        for findex, f in enumerate(xyz_scd_array):
                for cindex, c in enumerate(f):
                    #print("j={} : {}: {}".format(cindex//k, cindex%k, c[-1]))
                    scd_array[findex][cindex//k][cindex%k] = c[-1]

        return scd_array

    def getScdData(self, resIDs, c_name):
        xyz_scd_array = self.read()
        self.num_of_frames = len(xyz_scd_array)

        df = pd.DataFrame()
        colNames = []
        for index, resID in enumerate(resIDs):
            if c_name <12:
                colNames.append("res_{}".format(resID))
            else :
                colNames.append("res_{}_c_{}".format(resID, c_name))
            scd_list = self.extract(xyz_scd_array, resID, c_name)
            #print("resID={} len={}".format(resID, len(scd_list)))
            df[colNames[index]] = scd_list
        
        for index, colName in enumerate(colNames):
            name = "{}_{}".format(colName, "MV")
            df[name]=df[colName].rolling(window=51, min_periods=1, center=True).mean()
        return df

    def getData(self, frameIndex, carbonIndex, itemIndex):
            xyz_scd_array = self.read()
            for findex, f in enumerate(xyz_scd_array):
                if findex!=frameIndex:
                    continue
                for cindex, c in enumerate(f):
                    if cindex!=carbonIndex:
                        continue
                    for item_index, item in enumerate(c):
                        if item_index==itemIndex:
                            return item


    def plotScdVsFrame(self, resIDs, c_name):
        df = self.getScdData(resIDs, c_name)
        cols = df.columns
        n = len(cols)/2
        colNames = []
        for index, col in enumerate(cols):
            if index < n:
                colNames.append(col)
        
        plotFrameBoundary = True
        nFiles = len(self.files)
        dx = self.num_of_frames/nFiles
        bxs = []
        for i in range(1, nFiles, 1):
            bxs.append(i*dx)
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        fig.suptitle('SCD vs Frame Index', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot() 
            if plotFrameBoundary:
                for x in bxs:
                    plt.plot([x,x],[col.min(),col.max()],'--r')
            name = "{}_{}".format(colName, "MV")
            col = pd.to_numeric(df[name].squeeze())
            col.plot(label=name)
            plt.legend(loc='upper right')

        plt.xlabel("Frame Index")
        #outputFilename = ""
        outputFilename = os.path.join(self.images_path, self.base+"_scd.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()
        
    def plotItemSCD(self, itemIndex):
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

import os
import math
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MD import MD

class DihedralAngle(MD):

    def generate(self):
        traj = pt.iterload(self.files, os.path.join(self.data_path, self.prmtop))
        top = traj.top

        pa_carbons = []

        # obtain indices of carbon atoms in PA residue
        for i in range(top.n_residues):
            res = top.residue(i)
            if res.name == 'PA':
                pa_carbons.append(top.select(':{}@/C'.format(i+1)))

        m = len(traj)
        n = len(pa_carbons)
        print("m = {}  n = {} pa={}".format(m, n, len(pa_carbons[0])))

        cc_vectors = np.zeros((14, 3))
        dihedrals = np.zeros((m, n, 12))

        for findex, f in enumerate(traj):
            for rindex, carbons in enumerate(pa_carbons):
                for cindex in range(len(carbons)-1):
                    cc_vectors[cindex] = f.xyz[carbons[cindex+1]] - f.xyz[carbons[cindex]]
                    cc_vectors[cindex] /= np.linalg.norm(cc_vectors[cindex])
                for dhindex in range(1, len(cc_vectors)-1):
                    v1 = cc_vectors[dhindex-1]
                    v2 = cc_vectors[dhindex]
                    v3 = cc_vectors[dhindex+1]
                    v1p = v1 - v2 * np.dot(v1, v2)
                    v1p /= np.linalg.norm(v1p)
                    v3p = v3 - v2 * np.dot(v3, v2)
                    v3p /= np.linalg.norm(v3p)
                    dihedrals[findex, rindex, dhindex-1] = np.arccos(np.dot(v1p, v3p)) / np.pi *180
        np.save(os.path.join(self.results_path, self.base+'_dihedral.npy'), dihedrals)

        #count = np.bincount([int(i) for i in np.rint(dihedrals).flatten()])
        #np.savetxt(os.path.join(self.results_path, self.base+'_dihedral_count.txt'), count)

    def read(self):
        dihedrals = np.load(os.path.join(self.results_path, self.base+'_dihedral.npy'))
        print("{} : {}".format(self.base, dihedrals.shape))
        return dihedrals

    def getOriginalData(self):
        return self.read()

    def getData(self, frameIndex, resIndex, cc_bond_index):
        dihedrals = self.read()
        for findex, f in enumerate(dihedrals):
            if findex!=frameIndex:
                continue
            for rindex, r in enumerate(f):
                if rindex!=resIndex:
                    continue
                for cindex, c in enumerate(r):
                    if cindex==cc_bond_index:
                        return c
    
    def getDataResCC(self, resIndex, cc_bond_index):
        dihedrals = self.read()
        (m,n,k) = dihedrals.shape
        data = np.zeros(m)

        for findex, f in enumerate(dihedrals):
            for rindex, r in enumerate(f):
                if rindex!=resIndex:
                    continue
                for cindex, c in enumerate(r):
                    if cindex==cc_bond_index:
                        data[findex] = c
        return data

    def getDataRes(self, resIndex):
        dihedrals = self.read()
        (m,n,k) = dihedrals.shape
        data = np.zeros((m,k))

        for findex, f in enumerate(dihedrals):
            for rindex, r in enumerate(f):
                if rindex!=resIndex:
                    continue
                data[findex] = r
        return data

    def getDataFrame(self, frameIndex):
        dihedrals = self.read()
        (m,n,k) = dihedrals.shape
        data = np.zeros((n,k))
        for findex, f in enumerate(dihedrals):
            if findex!=frameIndex:
                continue
            return f

    def flatten(self):
        dihedrals = self.read()
        dihedrals1 = np.nan_to_num(dihedrals)
        #a = np.rint(dihedrals)
        #b = a[~np.isnan(a)].flatten()
        #return b
        #dihedrals = [x for x in dihedrals if not math.isnan(x)]
        return [int(i) for i in np.rint(dihedrals1).flatten()]        

    def plotCount(self):
        result = self.flatten()
        count = np.bincount(result)
        percentages = 100.0*count/len(result)
        values = np.arange(len(count))
        print(values)
        print(percentages)
        df = pd.DataFrame({ 'dihedral_counts': percentages })
        #df = pd.read_csv(os.path.join(self.results_path, self.base+'_dihedral_count.txt'), sep=" ", header=None, names=['dihedral_count'])
        colNames=df.columns.values.tolist()
        print(df.info())
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        fig.suptitle('Dihedral Angle Count', fontsize=18)
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

    def plotFrameMean(self, frameIndex):
        data = self.getDataFrame(frameIndex)
        (n,k) = data.shape
        meanArray = np.mean(data, axis=1)
        df = pd.DataFrame({ 'dihedral_angle': meanArray })
        colNames=df.columns.values.tolist()
        print(df.info())
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        fig.suptitle('Dihedral Angle Count', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot()
            
        plt.xlabel("Chain #") 
        #plt.legend(loc='lower right')
        #print(df.info)
        outputFilename = os.path.join(self.images_path, self.base+"_dihedral_mean.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()

    def plotFrameCount(self, frameIndex):
        data = self.getDataFrame(frameIndex)
        (n,k) = data.shape
        countArray = np.bincount([int(i) for i in np.rint(data).flatten()])
        df = pd.DataFrame({ 'dihedral_angle_count': countArray })
        colNames=df.columns.values.tolist()
        print(df.info())
        nSubPlots = len(colNames)
        fig,axs = plt.subplots(nSubPlots, 1, figsize=(10,10))
        fig.suptitle('Dihedral Angle Count', fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(nSubPlots, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot()
            
        plt.xlabel("Chain #") 
        #plt.legend(loc='lower right')
        #print(df.info)
        outputFilename = os.path.join(self.images_path, self.base+"_dihedral_mean.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()


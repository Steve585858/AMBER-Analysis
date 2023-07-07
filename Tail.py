
import os
import pytraj as pt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from MD import MD

class Tail(MD):

    def generate(self):
        traj = pt.iterload(self.files, os.path.join(self.data_path, self.prmtop))
        top = traj.top
        # clist contais indices of C12 and C116 for all PAs
        clist = []
        for i in range(top.n_residues):
            res = top.residue(i)
            if res.name == 'PA':
                clist.append([top.select(':{}@C12'.format(i+1))[0], top.select(':{}@C116'.format(i+1))[0]])

        m = len(traj)
        n = len(clist)
        print("m = {}  n = {}".format(m, n))

        # xyz: coordinates of C12 and C116: dimension 1: frame, dimension 2: residue, dimension 3: x,y,z,x,y,z
        xyz_tail = np.zeros((m, n, 11))
        for i, f in enumerate(traj):
            for j, pair in enumerate(clist):
                c12, c116 = pair
                xyz_tail[i, j, :3] = f.xyz[c12]
                xyz_tail[i, j, 3:6] = f.xyz[c116]

                # membrane thickness, |z_c12 - z_c116| *2
                k = 6
                dz = abs(f.xyz[c116][2] - f.xyz[c12][2])
                thickness = dz*2
                xyz_tail[i, j, k] = thickness 

                # length, l = distance(c12-c116)
                l = np.linalg.norm(f.xyz[c12] - f.xyz[c116])
                k += 1
                xyz_tail[i, j, k] = l

                # tail order parameter, S = 1.5* <cos^2(theta)>-0.5, theta = C12-C116 angle with z
                theCos = 0.5*thickness/l
                stail = 1.5*theCos*theCos-0.5
                k += 1
                xyz_tail[i, j, k] = stail

                #tail angle
                v = f.xyz[c12] - f.xyz[c116]
                v /= np.linalg.norm(v)
                tail_theta = np.arccos(v[2]) / np.pi *180
                tail_phi = np.arccos(v[0] / np.linalg.norm(v[:2])) / np.pi * 180
                k += 1
                xyz_tail[i, j, k] = tail_theta
                k += 1
                xyz_tail[i, j, k] = tail_phi

        np.save(os.path.join(self.results_path, self.base+'_tail.npy'), xyz_tail)

    def read(self):
        xyz_tail = np.load(os.path.join(self.results_path, self.base+'_tail.npy'))
        print("{} : {}".format(self.base, xyz_tail.shape))
        return xyz_tail

    def getOriginalData(self):
        return self.read()

    def getDataDetails(self, itemIndex):
        xyz_tail = self.read()
        m, n, k = xyz_tail.shape
        data = np.zeros((m, n))
        for i, f in enumerate(xyz_tail):
            for j, item in enumerate(f):
                data[i][j] = item[itemIndex]
        return data
    
    def getDataDetailsSD(self, itemIndex):
        data = self.getDataDetails(itemIndex)
        return np.std(data, axis=0)

    def getDataMembraneThickness(self):
        return self.getDataDetails(6)
    
    def getDataTailLength(self):
        return self.getDataDetails(7)

    def getDataTailOrderParameter(self):
        return self.getDataDetails(8)

    def getDataTailTheta(self):
        return self.getDataDetails(9)

    def getDataTailPhi(self):
        return self.getDataDetails(10)
    
    def getDataTailThetaSD(self):
        return np.std(self.getDataTailTheta(), axis=0)
    
    def getDataTailPhiSD(self):
        return np.std(self.getDataTailPhi(), axis=0)

    def plot(self):
        # time plot
        outputFilename = os.path.join(images_path, base+"_tail_order_parameter_parameter.png")
        colNames1 = []
        for i in range(n):
            colNames1.append('membrane_thickness_{}'.format(i))
        df1 = pd.read_csv(os.path.join(self.results_path, self.base+'_membrane_thickness.csv'), header=None, names=colNames1)
        colNames2 = []
        for i in range(n):
            colNames2.append('tail_length_{}'.format(i))
        df2 = pd.read_csv(os.path.join(self.results_path, self.base+'_tail_length.csv'), header=None, names=colNames2)
        colNames3 = []
        for i in range(n):
            colNames3.append('tail_order_parameter_{}'.format(i))
        df3 = pd.read_csv(os.path.join(self.results_path, self.base+'_tail_order_parameter.csv'), header=None, names=colNames3)

        index = 15

        df = pd.concat([df1["membrane_thickness_{}".format(index)].copy(), 
        df2["tail_length_{}".format(index)].copy(), 
        df3["tail_order_parameter_{}".format(index)].copy()], axis=1, join="inner")

        colNames=df.columns.values.tolist()
        fig,axs = plt.subplots(3, 1, figsize=(10,10))
        fig.suptitle('membrane_thickness, tail_length, and tail_order of #{}'.format(index), fontsize=18)
        for index, colName in enumerate(colNames):
            plt.subplot(3, 1, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot()
            
        plt.xlabel("Index") 
        #plt.legend(loc='lower right')
        #print(df.info)
        outputFilename = os.path.join(self.images_path, self.base+"_tail.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()


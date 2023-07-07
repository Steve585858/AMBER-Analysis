
import os
import pytraj as pt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from MD import MD

class TiltAngle(MD):

    def generate(self):
        traj = pt.iterload(self.files, os.path.join(self.data_path, self.prmtop))
        top = traj.top

        end_carbons = []

        # obtain indices of carbon atoms in PA residue
        for i in range(top.n_residues):
            res = top.residue(i)
            if res.name == 'PA':
                end_carbons.append(list(top.select(':{}@C12'.format(i+1))) + list(top.select(':{}@C116'.format(i+1))))
        m = len(traj)
        n = len(end_carbons)
        print("m = {}  n = {}".format(m, n))


        tail_theta = np.zeros((m, n))   # tilt
        tail_phi = np.zeros((m, n))     # azimuth

        for findex, f in enumerate(traj):
            for rindex, carbons in enumerate(end_carbons):
                c12, c116 = carbons
                v = f.xyz[c12] - f.xyz[c116]
                v /= np.linalg.norm(v)
                tail_theta[findex, rindex] = np.arccos(v[2]) / np.pi *180
                tail_phi[findex, rindex] = np.arccos(v[0] / np.linalg.norm(v[:2])) / np.pi * 180
        theta_count = np.bincount([int(i) for i in np.rint(tail_theta).flatten()])
        phi_count = np.bincount([int(i) for i in np.rint(tail_phi).flatten()])
        np.savetxt(os.path.join(self.results_path, self.base+'_theta_phi.csv'), np.vstack((theta_count, phi_count)).T, delimiter=",")
        sd_theta = np.std(tail_theta, axis=0)
        sd_phi = np.std(tail_phi, axis=0)
        np.savetxt(os.path.join(self.results_path, self.base+'_theta_phi_sd.csv'), np.vstack((sd_theta, sd_phi)).T, delimiter=",")

    def plot(self):
        bin_count = pd.read_csv(os.path.join(self.results_path, self.base+'_theta_phi.csv'), header=None, names=['theta_count', 'phi_count'])
        sd = pd.read_csv(os.path.join(self.results_path, self.base+'_theta_phi_sd.csv'), header=None, names=['theta_sd', 'phi_sd'])
        df = pd.concat([bin_count, sd], axis=1, join="inner")
        colNames=df.columns.values.tolist()
        fig,axs = plt.subplots(2, 2, figsize=(10,10))
        fig.suptitle('Tilt Angles', fontsize=24)
        for index, colName in enumerate(colNames):
            plt.subplot(2, 2, index+1)
            col = pd.to_numeric(df[colName].squeeze())
            plt.ylabel(colName)
            col.plot()
            
        plt.xlabel("Index") 
        #plt.legend(loc='lower right')
        #print(df.info)
        outputFilename = os.path.join(self.images_path, self.base+"_theta_phi.png")
        if outputFilename:
            plt.savefig(outputFilename)
        plt.show()

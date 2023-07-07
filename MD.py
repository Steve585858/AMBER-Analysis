
import os

class MD():

    def __init__(self, type, data_path, base, files, prmtop):
        self.type = type
        self.data_path = data_path
        self.base = base
        self.files = files
        self.prmtop = prmtop
        self.num_of_frames = 10
        
        self.CH2_carbon = (12,13,14,15,16,17,18,19,110,111,112,113,114,115)  # this works for PA residules
        self.items = ["C12_x", "C12_y", "C12_z", "C116_x", "C116_y", "C116_z", "Membrane Thickness", "Tail Length", "Tail Order Parameter", "Tail Theta", "Tail Phi"]

        cwd = os.getcwd()
        self.results_path = os.path.join(cwd, 'results')
        self.images_path = os.path.join(cwd, 'images')

        #self.df = pd.DataFrame()
        if self.type == 1:
            self.out = None
        elif self.type == 2:
            self.out = None
        elif self.type == 3 or self.type == 4:
            self.out = None

    def parseBase(self):
        parsed_list = self.base.split('_')
        return (int(parsed_list[0]), int(parsed_list[1][:3]), int(parsed_list[2][:3]))
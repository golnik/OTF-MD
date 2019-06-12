import numpy as np

class Geometry(object):
    def __init__(self):
        self.coords = []
        self.vels = []
        self.atoms  = []
        self.atomic_numbers = []
        self.atomic_masses = []

    def read_xyz(self,fname_xyz):
        inp_xyz = open(fname_xyz,'r')

        lines_xyz = inp_xyz.readlines()
        lines_xyz = lines_xyz[2:]

        for line in lines_xyz:
            data = line.split()

            self.atoms.append(data[0])

            self.coords.append(float(data[1]))
            self.coords.append(float(data[2]))
            self.coords.append(float(data[3]))

        self.vels = np.zeros(self.get_n_coords())

        inp_xyz.close()

    def read_vel(self,fname_xyz):
        inp_xyz = open(fname_xyz,'r')

        lines_xyz = inp_xyz.readlines()
        lines_xyz = lines_xyz[2:]

        for line in lines_xyz:
            data = line.split()

            self.atoms.append(data[0])

            self.vels.append(float(data[1]))
            self.vels.append(float(data[2]))
            self.vels.append(float(data[3]))

        inp_xyz.close()

    def print_xyz(self,output):
        n_atoms = len(self.atoms)
        output.write("%s\n" % n_atoms)
        output.write("comment line\n")
        for i_atom in range(n_atoms):
            output.write("%s %s %s %s\n" %
                (self.atoms[i_atom],
                 self.coords[3*i_atom],self.coords[3*i_atom+1],self.coords[3*i_atom+2]))

    def print_vel(self,output):
        n_atoms = len(self.atoms)
        output.write("%s\n" % n_atoms)
        output.write("comment line\n")
        for i_atom in range(n_atoms):
            output.write("%s %s %s %s\n" %
                (self.atoms[i_atom],
                 self.vels[3*i_atom],self.vels[3*i_atom+1],self.vels[3*i_atom+2]))

    def read_mol(self,fname_mol):
        inp_mol = open(fname_mol,'r')

        lines_mol = inp_mol.readlines()

        line_nmb = 0
        for line in lines_mol:
            data = line.split()

            if data:
                atom = data[0]
                if atom == self.atoms[line_nmb]:
                    self.atomic_numbers.append(float(data[1]))
                    self.atomic_masses.append(float(data[2]))
                else:
                    raise Exception('Geometry read error. xyz and mol files '
                                    'contain different atomic labels')
                line_nmb += 1

        inp_mol.close()

    def get_n_atoms(self):
        return len(self.atoms)

    def get_n_coords(self):
        return len(self.coords)

    def get_i_coord(self,i):
        return self.coords[i]

    def set_i_coord(self,i,val):
        self.coords[i]=val

    def get_i_vel(self,i):
        return self.vels[i]

    def set_i_vel(self,i,val):
        self.vels[i]=val
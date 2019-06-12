import configparser
import re
import os

class InputParams:
    def __init__(self):
        self.xyz_fname = None
        self.mol_fname = None
        self.vel_fname = None

        self.run_script_fname = None
        self.run_command = None

        self.prop_method = 'VelocityVerlet'
        self.prop_dt = 1.0
        self.prop_steps = 1

        self.xyz_out_fname = 'XYZ_$TSTEP.xyz'
        self.vel_out_fname = 'VEL_$TSTEP.xyz'
        self.eg_out_fname  = 'EG_$TSTEP.out'
        self.tmp_dir       = os.getcwd()

    def subst_variables(self, string, tstep):
        res_str = string
        #run_script variable
        res_str = self.subst_string_pattern(res_str,"\$RUN_SCRIPT",self.run_script_fname)

        #output variables
        res_str = self.subst_string_pattern(res_str,"\$XYZ_OUT",   self.xyz_out_fname)
        res_str = self.subst_string_pattern(res_str,"\$VEL_OUT",   self.vel_out_fname)
        res_str = self.subst_string_pattern(res_str,"\$EG_OUT",    self.eg_out_fname)
        res_str = self.subst_string_pattern(res_str,"\$TMP_DIR",   self.tmp_dir)

        #time step variable
        res_str = self.subst_string_pattern(res_str,"\$TSTEP",     str(tstep))

        return res_str

    def subst_string_pattern(self, string, pattern, subst):
        res = re.sub(pattern,subst,string)
        return res

class Input(object):
    def __init__(self,inp_fname):
        #create config file parser
        self.config = configparser.ConfigParser()
        self.config.read(inp_fname)

        self.inp_params = InputParams()
        self.analyze_input(self.inp_params)

    def analyze_input(self, inp_params):
        #get sections
        sections = self.config.sections()

        if "input" in sections:
            section = self.config['input']

            #get xyz_file
            inp_params.xyz_fname = section.get('xyz_file')
            if inp_params.xyz_fname is None:
                raise Exception("Problem with [input] section. XYZ_FILE is not specified.")

            #get mol_file
            inp_params.mol_fname = section.get('mol_file')
            if inp_params.mol_fname is None:
                raise Exception("Problem with [input] section. MOL_FILE is not specified.")

            #get vel_file
            inp_params.vel_fname = section.get('vel_file')
        else:
            raise Exception("Problem with config file. Input section is not found.")

        if "external" in sections:
            section = self.config['external']

            #get run_script
            inp_params.run_script_fname = section.get('run_script')
            if inp_params.run_script_fname is None:
                raise Exception("Problem with [external] section. run_script is not specified.")

            #get command
            inp_params.run_command = section.get('command')
            if inp_params.run_command is None:
                raise Exception("Problem with [external] section. command is not specified.")
        else:
            raise Exception("Problem with config file. External section is not found.")

        if "propagation" in sections:
            section = self.config['propagation']

            inp_params.prop_method = section.get('method',fallback=inp_params.prop_method)
            inp_params.prop_dt = section.getfloat('dt',fallback=inp_params.prop_dt)
            inp_params.prop_steps = section.getint('steps',fallback=inp_params.prop_steps)

        if "output" in sections:
            section = self.config['output']

            inp_params.xyz_out_fname = section.get('xyz_out',fallback=inp_params.xyz_out_fname)
            inp_params.vel_out_fname = section.get('vel_out',fallback=inp_params.vel_out_fname)
            inp_params.eg_out_fname  = section.get('eg_out',fallback=inp_params.eg_out_fname)
            inp_params.tmp_dir       = section.get('tmp_dir',fallback=inp_params.tmp_dir)
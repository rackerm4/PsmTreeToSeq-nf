#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import yaml
import numpy as np


class Loader:
    def get_path(self):
        return '/src/default.yaml'

    def cfg_load(self):
        path = '/src/default.yaml'
        with open(path) as f:
            config = yaml.safe_load(f)
        return config

    # def value_check(self, tell):
    #     config = self.cfg_load()
    #     vals = {k: v for k, v in tell.items() if v}
    #     empty = {k: v for k, v in tell.items() if not v}
    #
    #     for arg in config[str(tell)]:
    #

    def get_specific_config_values(self, getting):
        return self.cfg_load()[str(getting)]

    @staticmethod
    def generate_protracted_speciation_process_values():
        vital = ['incipient_species_extinction_rate', 'speciation_initiation_from_orthospecies_rate',
                 'speciation_initiation_from_incipient_species_rate', 'speciation_completion_rate',
                 'orthospecies_extinction_rate', 'aincipient_species_extinction_rate']
        rng_values = []
        n = 2  # number of digits after the decimal point
        # todo
        # filter values = 0 of rng_values
        for i in range(len(vital)):
            rng_values.append(round(random.uniform(0, 0.5), n))
        # test values below
        #return {'incipient_species_extinction_rate': 0.2, 'speciation_initiation_from_orthospecies_rate': 0.2, 'speciation_initiation_from_incipient_species_rate': 0.2, 'speciation_completion_rate': 0.2, 'orthospecies_extinction_rate': 0.2, 'aincipient_species_extinction_rate': 0.2}
        return dict(zip(vital, rng_values))

    # old function, reads in parameters from config file 'default.yaml'
    # def generate_protracted_speciation_process_values(self):
    #     psp = self.get_specific_config_values('ProtractedSpeciationProcess')
    #     vital = ['incipient_species_extinction_rate', 'speciation_initiation_from_orthospecies_rate',
    #              'speciation_initiation_from_incipient_species_rate', 'speciation_completion_rate',
    #              'orthospecies_extinction_rate', 'aincipient_species_extinction_rate']
    #     if 'ProtractedSpeciationProcess' in self.cfg_load():
    #         for arg in vital:
    #             if arg not in psp:
    #                 print("Missing ProtractedSpeciationProcess argument: " + arg + " in file " + self.get_path())
    #                 sys.exit()
    #         values_protractedspeciationprocess = psp
    #         return values_protractedspeciationprocess
    #     else:
    #         print("Missing ProtractedSpeciationProcess in config file.")
    #         sys.exit()

    def get_generate_sample_values(self):
        return self.get_specific_config_values('generate_sample')

    def generate_seq_gen_state_freqs(self):
        sum = 0
        vals = []
        while True:
            for i in np.random.dirichlet(np.ones(4)) * 1:
                rounded = np.round(i, 1)
                if rounded == 0:
                    sum = 0
                    vals = []
                    break
                vals.append(rounded)
                sum = np.sum(vals)
            if sum == 1:
                break
            else:
                sum = 0
                vals = []
        #vals = [int(i) for i in vals] # from str list to an int list
        return vals

    def get_seq_gen_values(self):
            config = self.get_specific_config_values('seq-gen')
            empty_args = {k: v for k, v in config.items() if not v}
            for k in empty_args.keys():
                if k == 'state_freqs':
                    empty_args['state_freqs'] = self.generate_seq_gen_state_freqs()
                # else:
                #     empty_args[k] = round(random.uniform(0, 1), 2)
            return {**config, **empty_args}
            #return self.get_specific_config_values('seq-gen')

    def load_headers(self):
        return list(self.cfg_load()['ProtractedSpeciationProcess']) + list(self.cfg_load()['generate_sample']) + list(self.cfg_load()['seq-gen'])

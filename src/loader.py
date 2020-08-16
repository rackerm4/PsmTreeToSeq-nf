#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import yaml


class Loader:
    def __init__(self, load):
        self.load = load

    def get_path(self):
        return '/src/default.yaml'

    def cfg_load(self):
        path = '/src/default.yaml'
        with open(path) as f:
            config = yaml.safe_load(f)
        return config

    def get_specific_config_values(self, getting):
        return self.cfg_load()[str(getting)]

    @staticmethod
    def generate_protracted_speciation_process_values():
        vital = ['incipient_species_extinction_rate', 'speciation_initiation_from_orthospecies_rate',
                 'speciation_initiation_from_incipient_species_rate', 'speciation_completion_rate',
                 'orthospecies_extinction_rate', 'aincipient_species_extinction_rate']
        rng_values = []
        n = 1  # number of digits after the decimal point
        for i in range(len(vital)):
            rng_values.append(round(random.uniform(0, 1), n))
        # test values below
        return {'incipient_species_extinction_rate': 0.2, 'speciation_initiation_from_orthospecies_rate': 0.2, 'speciation_initiation_from_incipient_species_rate': 0.2, 'speciation_completion_rate': 0.2, 'orthospecies_extinction_rate': 0.2, 'aincipient_species_extinction_rate': 0.2}
        #return dict(zip(vital, rng_values))

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

    def get_seq_gen_values(self):
        # todo:
        # state-freqs: if no values given, they're all equal 0.25
        # generate 4 random numbers with sum of 1 for state_freqs
        # possible solution:
        # import numpy as np
        # np.random.dirichlet(np.ones(4))*1
        return self.get_specific_config_values('seq-gen')

    def load_headers(self):
        return list(self.cfg_load()['ProtractedSpeciationProcess']) + list(self.cfg_load()['generate_sample']) + list(self.cfg_load()['seq-gen'])

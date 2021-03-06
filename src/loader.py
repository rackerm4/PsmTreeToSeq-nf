#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import dendropy
import yaml
import numpy as np
import sys
import os


class Loader:
    def __init__(self, path):
        self.path = path

    def cfg_load(self):
        fpath = os.path.join(self.path, 'src', 'default.yaml')
        with open(fpath) as f:
            config = yaml.safe_load(f)
        return config

    def get_specific_config_values(self, getting):
        return self.cfg_load()[str(getting)]

    def generate_protracted_speciation_process_values(self):
        get_values = self.get_specific_config_values('ProtractedSpeciationProcess')
        config_values = {k: v for k, v in get_values.items() if v}
        empty_config_values = {k: v for k, v in get_values.items() if not v}
        n = 2  # number of digits after the decimal point
        for key in empty_config_values:
            empty_config_values[key] = round(np.random.uniform(0.001, 0.3), n)
        # test values below
        # return {'incipient_species_extinction_rate': 0.2, 'speciation_initiation_from_orthospecies_rate': 0.2, 'speciation_initiation_from_incipient_species_rate': 0.2, 'speciation_completion_rate': 0.2, 'orthospecies_extinction_rate': 0.2, 'aincipient_species_extinction_rate': 0.2}
        return {**config_values, **empty_config_values}

    def get_generate_sample_values(self):
        get_values = self.get_specific_config_values('generate_sample')
        return {k: v for k, v in get_values.items() if v}

    def generate_seq_gen_general_rates(self):
        n = 2  # number of digits after the decimal point
        return [round(np.random.uniform(0.1, 1), n) for _ in range(6)]

    def generate_seq_gen_state_freqs(self):
        """Generates 4 random numbers using dirichlet distribution. Return when sum = 1"""
        sum = 0
        vals = []
        while True:
            for i in np.random.dirichlet(np.ones(4)) * 1:
                rounded = np.round(i, 3)
                if rounded == 0:
                    sum = 0
                    vals = []
                    break
                vals.append(rounded)
                sum = np.sum(vals)
            if sum == 1:
                break
            sum = 0
            vals = []
        # vals = [int(i) for i in vals]
        return vals

    def get_seq_gen_values(self):
        """Grabs Seq-Gen parameters of config and generates random values."""
        config = self.get_specific_config_values('seq-gen')
        random_args = {k: v for k, v in config.items() if v == 1}
        for k in random_args.keys():
            if k == 'state_freqs':
                random_args['state_freqs'] = self.generate_seq_gen_state_freqs()
            elif k == 'general_rates':
                random_args['general_rates'] = self.generate_seq_gen_general_rates()
            else:
                random_args[k] = round(np.random.uniform(0.1, 1), 2)
        return {**config, **random_args}

    def load_headers(self):
        return ['id'] + list(self.cfg_load()['ProtractedSpeciationProcess']) + list(self.cfg_load()['generate_sample']) + list(
            self.cfg_load()['seq-gen'])
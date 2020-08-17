# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#

import os
import argparse
import dendropy
import loader as cl
from dendropy.interop import seqgen

"""
    author: Robin Ackermann
    version: -
"""


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('trees', metavar='N', nargs='+', help='Incoming trees')
    parser.add_argument('--output_dir')
    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader()
    s = seqgen.SeqGen()

    # generate one alignment per tree
    # as substitution model is not specified, defaults to a JC model
    # will result in a DataSet object with one DnaCharacterMatrix per input tree
    # d0 = s.generate(trees)

    # print(len(d0.char_matrices))
    # print(d0.char_matrices[0].as_string("nexus"))
    # with open("seq_align.txt", "w") as f:
    #     f.write(d0.char_matrices[0].as_string("nexus"))

    # instruct Seq-Gen to scale branch lengths by factor of 0.1
    # note that this does not modify the input trees
    s.scale_branch_lens = 0.1
    # more complex model
    s.char_model = seqgen.SeqGen.GTR
    s.seq_len = None
    s.num_partitions = None
    s.scale_branch_lens = None
    s.scale_tree_len = None
    s.codon_pos_rates = None
    s.gamma_shape = None
    s.gamma_cats = None
    s.prop_invar = None
    s.ti_tv = 0.5  # = kappa of 1.0, i.e. JC
    s.ancestral_seq_idx = None
    s.output_text_append = None
    s.write_ancestral_seqs = False
    s.write_site_rates = False
    s.state_freqs = config.generate_seq_gen_state_freqs()
    s.general_rates = [0.8, 0.4, 0.4, 0.2, 0.2, 0.1]

    def seqgen_to_file(args, config, file, schema):
        trees = dendropy.TreeList.get(path=file, schema=schema)

        d1 = s.generate(trees)
        filename = "seq_{}.txt".format(file.split('.')[0])
        with open(filename, "w") as f:
            f.write(d1.char_matrices[0].as_string(schema))
        with open('test.txt', "a") as f:
            f.write(str(config.generate_seq_gen_state_freqs()) + '\n')
    # todo:
    # lineage and ortho tree don't have same parameters.

    for file in args.trees:
        schema = file.split('.')[1]
        if 'used_parameters' not in file:
            seqgen_to_file(args, config, file, schema)

if __name__ == '__main__':
    main()

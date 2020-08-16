# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#

import os
import argparse
import dendropy
from dendropy.interop import seqgen

"""
    author: Robin Ackermann
    version: -
"""


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    # parser.add_argument('--dir', '-d', required=True, help='Input dir')
    # parser.add_argument('--profile', '-p', default="default", required=True, help='')
    parser.add_argument('trees', metavar='N', nargs='+', help='Incoming trees')
    parser.add_argument('--output_dir')
    args = parser.parse_args()
    args.parser = parser

    for file in args.trees:
        schema = file.split('.')[1]
        if 'used_parameters' not in file:
            fpath = os.path.join(args.output_dir, 'generated_trees', file)
            trees = dendropy.TreeList.get(path=file, schema=schema)
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
            s.state_freqs = [0.4, 0.4, 0.1, 0.1]
            s.general_rates = [0.8, 0.4, 0.4, 0.2, 0.2, 0.1]
            d1 = s.generate(trees)
            filename = "seq_{}.txt".format(file.split('.')[0])
            with open(filename, "w") as f:
                f.write(d1.char_matrices[0].as_string(schema))


if __name__ == '__main__':
    main()

# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import os
import argparse
import dendropy
import loader as cl
from dendropy.interop import seqgen


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('trees', metavar='N', nargs='+', help='Incoming trees')
    parser.add_argument('--output_dir')
    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader()
    s = seqgen.SeqGen()

    s.scale_branch_lens = 0.1
    # more complex model

    def seqgen_to_file(args, config, file, schema):
        trees = dendropy.Tree.get(path=file, schema=schema)
        seqgen_vals = config.get_seq_gen_values()
        for k, v in seqgen_vals.items():
            seqgen_vals[k] = seqgen.SeqGen(v)

        filename = "seq_{}.txt".format(file.split('.')[0])
        d1 = s.generate(trees)
        with open(filename, "w") as f:
            f.write(d1.char_matrices[0].as_string(schema))

        # with open('test.txt', "a") as f:
        #     f.write(str(config.generate_seq_gen_state_freqs()) + '\n')
        # todo:
        # lineage and ortho tree don't have same parameters.

    for file in args.trees:
        schema = file.split('.')[1]
        if 'used_parameters' not in file:
            seqgen_to_file(args, config, file, schema)


if __name__ == '__main__':
    main()

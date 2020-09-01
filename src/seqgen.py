# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
import json
import argparse
import dendropy
import loader as cl
from dendropy.interop import seqgen


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('--ts', metavar='N', nargs='+', help='Incoming trees')
    parser.add_argument('--output_dir')
    parser.add_argument('--params', metavar='N', nargs='+', help='Incoming parameter files')
    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader(args.output_dir)

    # get seqgen parameters
    get_seqgen_param = config.get_seq_gen_values()
    # write seqgen params to file
    for i in range(len(args.ts)):
        id = args.ts[i].split('.')[0]
        seqgen_params_with_id = {'id': id, **get_seqgen_param}
        parameters_to_json(id, seqgen_params_with_id)
    # generate seqs
    seqgen_to_file(args.ts, get_seqgen_param)


def parameters_to_json(id, seqgen_params_with_id):
    file_name = id + "_s_params.json"
    with open(file_name, 'a') as f:
        json.dump(seqgen_params_with_id, f)


def seqgen_to_file(files, seqgen_vals):
    s = seqgen.SeqGen()
    s.scale_branch_lens = 0.1
    for k, v in seqgen_vals.items():
        seqgen_vals[k] = seqgen.SeqGen(v)
    for file in files:
        schema = file.split('.')[1]
        trees = dendropy.Tree.get(path=file, schema=schema)
        filename = "seq_{}".format(file.split('.')[0] + "." + schema)
        d1 = s.generate(trees)
        with open(filename, "w") as f:
            f.write(d1.char_matrices[0].as_string(schema))


if __name__ == '__main__':
    main()

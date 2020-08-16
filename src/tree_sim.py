# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#

import argparse
import time
import tempfile
import data_to_csv as dtc
import loader as cl
from dendropy.model import protractedspeciation

"""
    author: Robin Ackermann
    version: -
"""


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('--output', '-o', required=False, help='Output dir')
    parser.add_argument('--schema', '-s', choices=['newick', 'nexus'], required=True,
                        help='Tree schema: Newick, Nexus')
    parser.add_argument('--config', '-p', default="default", required=True, help='')
    parser.add_argument('--num_runs', '-n', default=1, type=int, required=False, help='')

    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader(args.config)
    #db = data.DB(args.output)
    headers = config.load_headers()

    # start
    start = time.perf_counter()
    c = 0
    for _ in range(args.num_runs):
        # getting trees
        get_trees = call_sample_tree(args, config)
        # generating Sequences & saving trees
        file_output(get_trees, args, ["lineage", "orthospecies"])
        # saving parameters
        parameters_to_txt(config, args, headers)


def temp_file_name():
    """
    Generates random string
    :return : random string
    """
    temp_name = next(tempfile._get_candidate_names())
    return temp_name


def gen_sample_values(values):
    """
    Returns variables for psp_ini.generate_sample in call_sample_tree function. Joins args to dict and filters empty args
    :param :
    :return : args with parameters only
    """
    return {k: v for k, v in values.items() if v}


def call_sample_tree(args, config):
    """
    Calls ProtractedSpeciationProcess and generates sample trees.
    :param args, config:
    :return trees,
    generate_tree[0] lineage_tree (|Tree| instance) – A tree from the protracted speciation process, with all lineages
    (good species as well as incipient species).
    generate_tree[1] orthospecies_tree (|Tree| instance) – A tree from the protracted speciation process with only
    “good” species.:
    """
    try:
        # calling args
        values = gen_sample_values(config.get_generate_sample_values())
        # generate trees
        generated_trees = protractedspeciation.ProtractedSpeciationProcess(
            **config.generate_protracted_speciation_process_values()).generate_sample(**values)
        return generated_trees
    except BaseException as e:
        print("Maximum number of runs to execute in the event of prematurely-terminated simulations due to all "
              "lineages going extinct. Once this number or re-runs is exceed, then TreeSimTotalExtinctionException "
              "is raised. Defaults to 1000. Set to None to never quit trying.\n" + str(e))


def file_output(trees, args, tree_names):
    """Stores output files."""
    for i in range(len(trees)):
        try:
            file_name = tree_names[i] + '_' + temp_file_name() + "." + str(args.schema)
            # tmp_path = os.path.join(output_dir, file_name)
            trees[i].write_to_path(file_name, suppress_edge_lengths=True,
                                   schema=args.schema)
            # yield file_name
        except BaseException as e:
            return "Unexpected error while saving tree data:\n" + str(e)


def parameters_to_txt(config, args, headers):
    z = {**config.get_generate_sample_values(), **config.generate_protracted_speciation_process_values(),
         **config.get_seq_gen_values()}
    dtc.write_data_to_txt(z, args.output, headers)


if __name__ == '__main__':
    main()

# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#

import os
import glob
import argparse
import time
import tempfile
import data_to_csv as dtc
import loader as cl

import dendropy
from dendropy.model import protractedspeciation


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('--output', '-o')
    parser.add_argument('--schema', '-s', choices=['newick', 'nexus'], required=True,
                        help='Tree schema: Newick, Nexus')
    parser.add_argument('--config', '-c', default="default", required=True, help='')
    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader(args.output)
    headers = config.load_headers()

    # getting trees
    get_trees = call_sample_tree(config)
    # generating Sequences & saving trees
    try:
        file_output(get_trees, args, ["lineage", "orthospecies"])
    except:
        pass
    # saving parameters
    parameters_to_txt(config, headers)


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


def call_sample_tree(config):
    """
    Calls ProtractedSpeciationProcess and generates sample trees.
    :param args, config:
    :return trees,
    generate_tree[0] lineage_tree (|Tree| instance) – A tree from the protracted speciation process, with all lineages
    (good species as well as incipient species).
    generate_tree[1] orthospecies_tree (|Tree| instance) – A tree from the protracted speciation process with only
    “good” species.:
    """
    while True:
        try:
            # calling args
            values = gen_sample_values(config.get_generate_sample_values())
            # generate trees
            generated_trees = protractedspeciation.ProtractedSpeciationProcess(
                **cl.Loader.generate_protracted_speciation_process_values()).generate_sample(**values)
            return generated_trees
        except:
            continue
        # except BaseException as e:
        #     print("Maximum number of runs to execute in the event of prematurely-terminated simulations due to all "
        #           "lineages going extinct. Once this number or re-runs is exceed, then TreeSimTotalExtinctionException "
        #           "is raised. Defaults to 1000. Set to None to never quit trying.\n" + str(e))


def file_output(trees, args, tree_names):
    """Stores output files."""
    for i in range(len(trees)):
        try:
            # if schema is not nexus, trees will be stored as newick and then converted to nexus
            if args.schema != 'nexus':
                file_name = tree_names[i] + '_' + temp_file_name() + "." + str(args.schema)
                trees[i].write_to_path(file_name, suppress_rooting=True, suppress_edge_lengths=True,
                                       schema=args.schema)
                convert_newick_to_nexus(file_name)
            else:
                file_name = tree_names[i][:3] + '_' + temp_file_name() + "." + str(args.schema)
                trees[i].write_to_path(file_name, suppress_rooting=True, suppress_edge_lengths=True,
                                       schema=args.schema)
            for f in glob.glob("*.newick"):
                os.remove(f)
        except BaseException as e:
            return "Unexpected error while saving tree data:\n" + str(e)


def convert_newick_to_nexus(fname):
    """ Converts newick trees to nexus schema."""
    tree = dendropy.Tree.get(path=fname, schema='newick')
    new_file_name = fname.split('.')[0] + '.nexus'
    tree.write_to_path(new_file_name, suppress_rooting=True, suppress_edge_lengths=True,
                                                 schema="nexus")
    return new_file_name


def parameters_to_txt(config, headers):
    """Combines all parameters dicts to one dict and pass dict + headers to write_data_to_txt"""
    z = {**config.get_generate_sample_values(), **config.generate_protracted_speciation_process_values(),
         **config.get_seq_gen_values()}
    dtc.write_data_to_txt(z, headers)


if __name__ == '__main__':
    main()

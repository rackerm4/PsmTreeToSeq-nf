# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#

import os
import glob
import argparse
import time
import tempfile
import json
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

    # load run parameters
    generated_sample_parameters = gen_sample_values(config.get_generate_sample_values())
    generated_protracted_speciation_process_parameters = cl.Loader.generate_protracted_speciation_process_values()

    try:
        # getting trees
        get_trees = call_sample_tree(generated_sample_parameters, generated_protracted_speciation_process_parameters)
        # generating Sequences & saving trees, creating file names
        a = rng_file_name()
        for i in range(len(get_trees)):
            names = ["lineage", "orthospecies"]
            file_name = names[i][:3] + '_' + a + "." + str(args.schema)
            file_output(get_trees[i], args, file_name)
            parameters_to_json(generated_sample_parameters, generated_protracted_speciation_process_parameters, headers,
                              file_name)
    except:
        pass


def rng_file_name():
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


def call_sample_tree(generate_sample_parameters, generated_protracted_speciation_process_parameters):
    """
    Calls ProtractedSpeciationProcess and generates sample trees.
    :param generated_protracted_speciation_process_parameters:
    :param generate_sample_parameters
    :return trees,
    generate_tree[0] lineage_tree (|Tree| instance) – A tree from the protracted speciation process, with all lineages
    (good species as well as incipient species).
    generate_tree[1] orthospecies_tree (|Tree| instance) – A tree from the protracted speciation process with only
    “good” species.:
    """
    while True:
        try:
            # # calling args
            # values = gen_sample_values(config.get_generate_sample_values())
            # generate trees
            generated_trees = protractedspeciation.ProtractedSpeciationProcess(
                **generated_protracted_speciation_process_parameters).generate_sample(**generate_sample_parameters)
            return generated_trees
        except:
            continue
            # ignores error coming from ProtractedSpeciationProcess and keeps going instead.


def file_output(trees, args, file_name):
    """Stores output files."""
    try:
        # if schema is not nexus, trees will be stored as newick and then converted to nexus
        if args.schema != 'nexus':
            trees.write_to_path(file_name, suppress_rooting=True, suppress_edge_lengths=True,
                                schema=args.schema)
            convert_newick_to_nexus(file_name)
        else:
            trees.write_to_path(file_name, suppress_rooting=True, suppress_edge_lengths=True,
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


def parameters_to_json(generated_sample_parameters, generated_protracted_speciation_process_parameters, headers,
                      file_name):
    """Combines all parameters dicts to one dict and pass dict + headers to write_data_to_txt"""
    id_file = {'id': file_name.split('.')[0]}
    z = {**id_file, **generated_sample_parameters, **generated_protracted_speciation_process_parameters}

    json_file = "{}_t_params.json".format(file_name.split('.')[0])
    with open(json_file, "a+") as json_file:
        json.dump(z, json_file)


if __name__ == '__main__':
    main()

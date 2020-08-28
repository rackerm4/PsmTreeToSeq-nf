import csv
import os

"""
    Stores all parameters into text file
"""


def write_params_to_txt(data_dict, headers):
    """Parameter to file writer."""
    csv_columns = headers
    # if val:
    #     csv_file = "{}_tree_params.txt".format(data_dict['id'])
    # else:
    #     csv_file = "{}_seqgen_params.txt".format(data_dict['id'])
    csv_file = "params.txt"

    if os.path.isfile(csv_file):
        with open(csv_file, "a+") as csvfile:
            writer = csv.DictWriter(csvfile, lineterminator='\n', delimiter=' ', fieldnames=csv_columns)
            writer.writerow(data_dict)
    else:
        with open(csv_file, "a+") as csvfile:
            writer = csv.DictWriter(csvfile, lineterminator='\n', delimiter=' ', fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(data_dict)

    # csv_columns = ['id', 'incipient_species_extinction_rate', 'speciation_initiation_from_orthospecies_rate',
    # 'speciation_initiation_from_incipient_species_rate', 'speciation_completion_rate',
    # 'orthospecies_extinction_rate', 'aincipient_species_extinction_rate'], ['max_time', 'num_extant_orthospecies',
    # 'num_extant_lineages', 'is_retry_on_total_extinction', 'max_retries'], ['state_freqs', 'general_rates',
    # 'MODEL', 'SEQUENCE_LENGTH', 'NUMBER_OF_DATASETS', 'NUMBER_OF_PARTITIONS', '-sSCALE', '-dSCALE',
    # 'CODON_POSITION_RATES', 'ALPHA', 'NUM_CATEGORIES', 'PROPORTION_INVARIABLE', 'STATE_FREQUENCIES',
    # 'TRANSITION_TRANSVERSION_RATIO', 'RATE_MATRIX_VALUES', 'ANCESTRAL_SEQUENCE_NUMBER', 'RANDOM_NUMBER_SEED', 'op',
    # 'or', True, 'of', 'TEXT_FILE_NAME', 'wa', 'wr', 'q', 'h']

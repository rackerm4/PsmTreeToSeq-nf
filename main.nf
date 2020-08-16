#!/usr/bin/env nextflow

// User Input Parameter
params.force = true
params.output_dir = "$baseDir/"

// Path Variable
TREE_SIM_DIR = params.output_dir + "/generated_trees"
SEQGEN_DIR = params.output_dir + "/generated_seqs"
output_dir = file(params.output_dir)
/*
// Sanity checks
// If output_dir exists, check for "--force" parameter otherwise error with Exitcode 1
if (output_dir != null && output_dir.list().size() != 0) {
    println "Warning: Directory $output_dir is not empty."
    if (params.force == false){
         return 1
        }
}
*/
/*
    First Process: tree_sim.py generates n trees and stores them.container 'src'
*/
process tree_sim {
//    container 'stanni/prokka'
    publishDir TREE_SIM_DIR, mode: 'copy'
    output:
        file '*' into ch_tree_sim_output
    script:
    """
    python3 /home/student/pspsTSGen_nf/src/tree_sim.py --num_runs ${params.nums} --schema ${params.schema} --config ${params.config}
    """
}
/*
    Seq_gen process: uses simulated trees of process tree_sim and simulates sequences.
*/
process seq_gen {
    publishDir SEQGEN_DIR, mode: 'copy'
    input:
        file seqgen_input from ch_tree_sim_output
    output:
        file '*' into ch_seqgen_output
    script:
        """
        python3 /home/student/pspsTSGen_nf/src/seqgen.py $seqgen_input --output_dir ${params.output_dir}
        """
}

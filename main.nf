#!/usr/bin/env nextflow

// User Input Parameter
params.force = true
params.output_dir = "$baseDir/"

// Path Variable
TREE_SIM_DIR = params.output_dir + "generated_trees"
SEQGEN_DIR = params.output_dir + "generated_seqs"
output_dir = file(params.output_dir)

println """\
         P s m  T r e e  T o  S e q - N F  ~  version 0.1
         ===================================
         Directory of generated trees        : ${TREE_SIM_DIR}
         Directory of generated sequences    : ${SEQGEN_DIR}
         """
         .stripIndent()
/*
    First Process: tree_sim.py generates n trees and stores them.
*/
process tree_sim {
    publishDir TREE_SIM_DIR, mode: 'copy'
    input:
        each x from 1..params.nums.toInteger()
    output:
        file '*' into ch_tree_sim_output
    script:
    """
    python3 ${output_dir}/src/tree_sim.py --schema ${params.schema} --config ${params.config} --output ${output_dir}
    """
}
/*
    Seq_gen process: uses simulated trees of process tree_sim and simulates sequences.
*/
process seq_gen {
    publishDir SEQGEN_DIR,mode: 'move'
    input:
        file tree from ch_tree_sim_output
    output:
        file '*' into ch_seqgen_output
    script:
        """
        python3 ${output_dir}/src/seqgen.py ${tree} --output_dir ${params.output_dir}
        """
}

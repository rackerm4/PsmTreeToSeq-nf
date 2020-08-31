# PsmTreeToSeq-nf

Pipeline using Nextflow, DendroPy & Seq-Gen.

Simulates pyhlogentic trees with protracted speciation model, using Seq-Gen to simulate the evolution of nucleotide sequences along those phylogenies.

Status: Working. Testing...

## :thought_balloon: Background


### Installation & Docker
Install as Module:
```
$ python setup.py install
```
Install Nextflow.io
```
curl -s https://get.nextflow.io | bash
export PATH=$PATH:/your/path/
```
Install Seq-Gen
```
$ sudo apt-get install seq-gen
```

Run via Nextflow:
```sh
$ nextflow run rackerm4/PsmTreeToSeq-nf --nums N --schema nexus --config default (--profile standard (default)/cluster_sge/docker) (-with-docker docker)
```

Clone from GitHub:
```sh
$ git clone https://github.com/rackerm4/PsmTreeToSeq.git
$ cd PsmTreeToSeq
$ nextflow run main.nf --nums N --schema nexus --config default (--profile standard/cluster_sge/docker) (-with-docker docker)
```
## :wrench: Requirements

* DendroPy==4.4.0
* future==0.18.2
* numpy==1.19.1
* PyYAML==5.3.1
* Seq-Gen
* Nextflow

### :pencil2: Arguments

Arg | Notes
------- | --------
--config/-c | Choosing parameters file (config): 1 = random parameters, None = None, False = False, or specify your value
--num_runs/-n   | Enter number of trees & sequence files you want simulate
--schema/-s | Tree schema (newick, nexus..)
--output/-o | Specify output directory
--profile | Choose between different profile. Default: "standard", runs locally. 
--with-docker | runs processes in specific container

### :bulb: Sun Grid Engine

"The SGE executor allows you to run your pipeline script by using a Sun Grid Engine cluster.
Nextflow manages each process as a separate grid job that is submitted to the cluster by using the qsub command.
Being so, the pipeline must be launched from a node where the qsub command is available, that is, in a common usage scenario, the cluster head node.
To enable the SGE executor simply set to process.executor property to sge value in the nextflow.config file.
The amount of resources requested by each job submission is defined by the following process directives:"
- cpus
- queue
- memory
- penv
- time
- clusterOptions

Source & for further information: https://www.nextflow.io/docs/latest/executor.html#sge


## :construction: Work to be done
- (Dockerfile/image/container)
- Ignore parameters of failed runs -> see Known issues [Done]
- Passing Seq-Gen parameter from default config [Done]
- randomized Seq-Gen parameters [Done]
- several testing:
    - behavior with high tree counts & full size
    
## :warning: Known issues
- possible error when Docker run in SGE. SGE should be used without Docker
- Parameters not logged properly [Done]
- Newick trees raise an error when read in with Seq-Gen. Currently every newick tree is converted into a nexus tree. All newick tree will be deleted.
- When ProtractedSpeciationProcess class raises an error, most of the time it's that error below. 
It will be ignored and the next run will start, but the parameters still get saved. [Done] runs process until return
```
"_Maximum number of runs to execute in the event of prematurely-terminated simulations due to all 
lineages going extinct. Once this number or re-runs is exceed, then TreeSimTotalExtinctionException 
is raised. Defaults to 1000. Set to None to never quit trying._"
```
- Permission denied error? Execute permission for the files in /src/: chmod u+rwx *.py
- If you find yourself with an error like that: 
```
$ docker: Got permission denied while trying to connect to the Docker daemon socket 
try
$ sudo chmod 666 /var/run/docker.sock
```
## :question: Open questions
- Big data runtime
- Number of digits after the decimal point for random values
- typical DNA specific rates

### How does it work

- [`Nextflow/main.nf`](main.nf)
Defines output directories and takes several arguments listed above. Runs the tree simulation "nums" times and forwards output into specific channel to SeqGen.py 
Merges all parameters files to single "params.txt" file.
Can be run in Docker container, with Docker images/containers or in Sun Grid Engine.

- [`tree_sim.py`](src/tree_sim.py):
Runs "nums" times. Reads in parameters from config file, or loads randomized parameters. Stores used parameters in json files "TREENAME_t_params.json". 
If user used "newick" schema, all trees are converted to nexus. Returns 2 trees per run:
    - lineage_tree – A tree from the protracted speciation process, with all lineages
    (good species as well as incipient species).
    - orthospecies_tree – A tree from the protracted speciation process with only
    “good” species.
    
- [`seqgen.py`](src/seqgen.py)
Takes two trees per run. Reads in parameters from config file, or loads randomized parameters. Stores used parameters in json files "SEQFILE_s_params.json". Returns 2 nexus files with sequences.

- [`default.yaml`](src/default.yaml)
Contains arguments for ProtractedSpeciationProcess, generate_sample & SeqGen.
Parameters with "1" will be randomized. None = None, False = False


## :books: Resources
- DendroPy - Phylogenetic Computing Library:
    - https://dendropy.org/
- Seq-Gen - Program simulating the evolution of nucleotide or amino acid sequences along a phylogeny
    - http://tree.bio.ed.ac.uk/software/seqgen/
- Nextflow - Data-driven computational pipelines 
    - https://www.nextflow.io/

### Protracted speciation model-related publications
Estimating the duration of speciation from phylogenies  
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4262007/

Prolonging the past counteracts the pull of the present: protracted speciation can explain observed slowdowns in diversification 
- https://pubmed.ncbi.nlm.nih.gov/21873376/

The reconstructed tree in the lineage-based model of protracted speciation 
- https://pubmed.ncbi.nlm.nih.gov/24615006/

### Seq-gen-related publications
Seq-Gen: an application for the Monte Carlo simulation of DNA sequence evolution along phylogenetic trees 
- https://pubmed.ncbi.nlm.nih.gov/9183526/
- Full article for free: 
    - https://academic.oup.com/bioinformatics/article-pdf/13/3/235/1170463/13-3-235.pdf
    
    

##### :microscope: Biology
https://en.wikipedia.org/wiki/Phylogenetics
##### :computer: Bioinformatics
https://en.wikipedia.org/wiki/Bioinformatics



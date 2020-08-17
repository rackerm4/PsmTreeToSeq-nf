# PsmTreeToSeq-nf
Pipeline using Nextflow, DendroPy & Seq-Gen.

Simulates pyhlogentic trees with protracted speciation model, using Seq-Gen to simulate the evolution of nucleotide or amino acid sequences along those phylogenies.

Status: Currently not working.

## Background


### Installation & Docker

```sh
$ nextflow run rackerm4/PsmTreeToSeq-nf --nums N --schema nexus --config default (-with-docker docker NOT WORKING RN)
```
## Requirements

* DendroPy==4.4.0
* future==0.18.2
* numpy==1.19.1
* PyYAML==5.3.1
* Seq-Gen

(Will be installed by pip in Docker)

### Arguments
[`main.py`]

Arg | Notes
------- | --------
--config/-c    | Choosing parameters file (config): no specification of parameters will result in randomized values
--num_runs/-n   | Enter number of trees you want simulate
--schema/-s | tree schema (newick, nexus..)
--output/-o | specify output directory

## Work to be done
- only save parameters of generated tree -> see Knows issues
- Passing Seq-Gen parameter from default config 
- randomized Seq-Gen parameters
- several testing:
    - behavior with high tree counts & full size
    
## Known issues
- When ProtractedSpeciationProcess class raises an error, most of the time it's that error below. 
It will be ignored and the next run will start, **but the parameters still get saved**.
```
"_Maximum number of runs to execute in the event of prematurely-terminated simulations due to all 
lineages going extinct. Once this number or re-runs is exceed, then TreeSimTotalExtinctionException 
is raised. Defaults to 1000. Set to None to never quit trying._"
```
- Permission denied error? Execute permission for the files in /src/: chmod u+rwx *.py
- If you find yourself with an error like that: 
    
   
    $ docker: Got permission denied while trying to connect to the Docker daemon socket 
    try
    $ sudo chmod 666 /var/run/docker.sock

## Open questions
- Big data runtime?
- Works better with implementing with nextflow.io ?
    - parallelization of runs
- number of digits after the decimal point for random values

### How does it work

## Resources
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
    
    

##### Biology
https://en.wikipedia.org/wiki/Phylogenetics
##### Bioinformatics
https://en.wikipedia.org/wiki/Bioinformatics



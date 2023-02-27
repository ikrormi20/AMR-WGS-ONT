import subprocess 
from os.path import join

###Declare Global wildcards 

SAMPLES, = glob_wildcards(join(config["fastqDir"], "{sample}."+config["fastqExtension"]))

print(SAMPLES)

###Rules
rule all:
    input:
        expand(join(config["outputDir1"], "{sample}/assembly.fasta"),sample=SAMPLES),
        expand(join(config["outputDir2"],"{sample}/consensus.fasta"),sample=SAMPLES),
        expand(join(config["outputDir3"],"{sample}.csv"),sample=SAMPLES)       

rule flye:
    input:
        fastq=join(config["fastqDir"], "{sample}."+config["fastqExtension"])
    output:
        (join(config["outputDir1"],"{sample}/assembly.fasta"))
    params:
        outfly=(join(config["outputDir1"],"{sample}"))
    shell:
        """
        mkdir -p {params.outfly}
        flye --nano-hq {input.fastq} --out-dir {params.outfly} 
        """

rule medaka:
    input:
        rawreads=join(config["fastqDir"], "{sample}."+config["fastqExtension"]),
        assemblyfile=(join(config["outputDir1"],"{sample}/assembly.fasta"))
    output:
        (join(config["outputDir2"],"{sample}/consensus.fasta"))
    params:
        outMedaka=(join(config["outputDir2"],"{sample}"))
    shell:
        """
        medaka_consensus -m r941_min_sup_g507 -i {input.rawreads} -d {input.assemblyfile} -o {params.outMedaka}
        """

rule abricate:
    input:
        polishedFile=(join(config["outputDir2"],"{sample}/consensus.fasta"))
    output:
        (join(config["outputDir3"],"{sample}.csv"))
    shell:
        """
        abricate/bin/abricate -db card --csv {input.polishedFile} > {output}
        """



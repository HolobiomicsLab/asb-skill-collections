---
name: kilobase-resolution-contact-map-analysis
description: Use when you have paired-end Hi-C FASTQ files from a public repository (NCBI SRA, GEO, or ENCODE-deposited) and need to produce standardized .hic binary contact maps that conform to ENCODE reference formats and integrity standards for downstream 3D genome analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
  - Burrows-Wheeler Aligner (BWA)
  - Caper
  - Juicer Tools
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_juicer
    doi: 10.1016/j.cels.2016.07.002
    title: juicer
  dedup_kept_from: coll_juicer
schema_version: 0.2.0
---

# kilobase-resolution-contact-map-analysis

## Summary

Generate and validate Hi-C contact maps at kilobase resolution from FASTQ raw sequencing data using the Juicer pipeline and ENCODE's uniform processing workflow. This skill enables reproducible construction of three-dimensional genome contact matrices with format validation and output integrity verification.

## When to use

You have paired-end Hi-C FASTQ files from a public repository (NCBI SRA, GEO, or ENCODE-deposited) and need to produce standardized .hic binary contact maps that conform to ENCODE reference formats and integrity standards for downstream 3D genome analysis.

## When NOT to use

- Input is not raw FASTQ data but already an aligned BAM or SAM file — use the 'merge' or 'dedup' stage restart flags instead of running the full pipeline.
- You require sub-kilobase or nucleosome-resolution contact mapping — Juicer is optimized for kilobase resolution and may not provide sufficient granularity for finer scales.
- Your cluster does not support SLURM, LSF, GridEngine, or cloud execution; CPU-only mode requires >= 4 cores and >= 64 GB RAM minimum, and is not recommended for large datasets.

## Inputs

- Hi-C paired-end FASTQ files from public repository (NCBI SRA, GEO) or ENCODE accession
- Genome identifier (e.g., hg19, mm10) or reference genome file in FASTA format
- Restriction enzyme site file (e.g., HindIII, MboI)
- Chromosome sizes file (.chrom.sizes)

## Outputs

- .hic binary contact map file (Hi-C format)
- File checksum or hash for integrity verification
- Alignment statistics and deduplication metrics
- Feature-annotated Hi-C maps (via postprocessing command-line tools)

## How to apply

Clone the ENCODE Hi-C uniform processing pipeline (ENCODE-DCC/hic-pipeline) and invoke the Juicer-based encode_hic_pipeline wrapper on your FASTQ input files to align reads and construct the Hi-C contact map in .hic binary format. The pipeline performs chimeric read handling, deduplication, and final Hi-C file generation across configurable cluster environments (SLURM, CPU, or cloud via Caper/Cromwell). Validate output by computing file checksums or hashes and comparing against ENCODE reference outputs to confirm pipeline reproducibility. For cloud execution, use the dockerized ENCODE pipeline with Caper (Python wrapper for Cromwell) rather than the deprecated AWS scripts; ensure Java >= 1.8 and Python >= 3.6 are installed.

## Related tools

- **Juicer** (Core pipeline for generating Hi-C maps from FASTQ data and command-line tools for feature annotation on contact maps) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)** (Wrapper and standardized distribution of Juicer for cloud-based and reproducible Hi-C processing) — https://github.com/ENCODE-DCC/hic-pipeline
- **Burrows-Wheeler Aligner (BWA)** (Underlying read alignment tool required by Juicer pipeline) — http://bio-bwa.sourceforge.net/
- **Caper** (Python wrapper for Cromwell workflow engine to run ENCODE pipeline on local, cluster, or cloud platforms) — https://github.com/ENCODE-DCC/caper
- **Juicer Tools** (Java-based command-line utilities for post-processing, feature annotation, and analysis of .hic contact maps) — https://github.com/theaidenlab/juicer/wiki/Download

## Examples

```
caper run hic.wdl -i tests/functional/json/test_hic.json --docker
```

## Evaluation signals

- Output .hic file exists in expected binary format and can be parsed by Juicer Tools without corruption errors.
- Computed file checksum or cryptographic hash of output .hic matches ENCODE reference checksum, confirming bit-for-bit reproducibility.
- Pipeline produces alignment statistics (mapped reads, deduplicated reads, unique valid pairs) within expected ranges for the input dataset and genome.
- Hi-C map can be visualized and interrogated by downstream tools (Juicebox, HiCCUPS peak calling) without format errors.
- Post-processing feature annotation tools (TADs, loops, domain boundaries) execute successfully on the generated .hic file.

## Limitations

- Juicer 2.0 (current main repository) is under active development; for stable production runs, use Juicer 1.6 release branch to minimize unexpected behavior.
- AWS-based execution scripts in the main Juicer repository are deprecated; ENCODE's Caper-based pipeline is recommended for cloud computing.
- Pipeline requires cluster or cloud infrastructure with ≥ 4 cores and ≥ 64 GB RAM for optimal performance; CPU-only single-machine execution is supported but not recommended for large Hi-C datasets.
- GPU/CUDA support (for HiCCUPS peak calling) requires an NVIDIA GPU; CPU version of HiCCUPS is available but slower.
- No changelog is published for ongoing development versions, making version tracking difficult for reproducibility across time.

## Evidence

- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps.: "pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps"
- [readme] ENCODE's Hi-C uniform processing pipeline based on Juicer can be found here: https://github.com/ENCODE-DCC/hic-pipeline: "ENCODE's Hi-C uniform processing pipeline based on Juicer can be found [here](https://github.com/ENCODE-DCC/hic-pipeline)"
- [other] Obtain a publicly available Hi-C FASTQ dataset from a public repository (e.g., NCBI SRA, GEO) or use an ENCODE-deposited accession. Clone the ENCODE Hi-C uniform processing pipeline from the ENCODE-DCC/hic-pipeline repository. Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map.: "Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map"
- [other] Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash. Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness.: "Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash. Compare the computed checksum against the ENCODE reference output checksum"
- [readme] The main repository on Github is now focused on the Juicer 2.0 release and is under active development. The beta release for Juicer version 1.6 can be accessed via the Github Release.: "The main repository on Github is now focused on the Juicer 2.0 release and is under active development"
- [readme] We recommend ENCODE's Hi-C processing pipeline, based on Juicer, to run in the cloud; the AWS scripts are out of date.: "We recommend ENCODE's Hi-C processing pipeline, based on Juicer, to run in the cloud; the AWS scripts are out of date"
- [readme] Juicer is a pipeline optimized for parallel computation on a cluster. Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM): "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"
- [readme] Install Caper, requires java >= 1.8 and python >= 3.6, Caper >= 0.8.2.1 is required to run the pipeline. Caper is a Python wrapper for Cromwell.: "Install Caper, requires `java` >= 1.8 and `python` >= 3.6, Caper >= 0.8.2.1 is required to run the pipeline"

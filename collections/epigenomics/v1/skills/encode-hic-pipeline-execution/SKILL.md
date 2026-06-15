---
name: encode-hic-pipeline-execution
description: Use when you have raw Hi-C FASTQ files from a public repository (NCBI SRA, GEO, or ENCODE-deposited accession) and need to reproduce or validate Hi-C map generation following the ENCODE uniform processing standard, or you need to verify that your pipeline output conforms to reference format and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
  - Juicer
  - Caper
  - BWA (Burrows-Wheeler Aligner)
  - Juicer Tools
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans:
- ENCODE's Hi-C uniform processing pipeline based on Juicer can be found [here](https://github.com/ENCODE-DCC/hic-pipeline)
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

# encode-hic-pipeline-execution

## Summary

Execute the ENCODE Hi-C uniform processing pipeline (based on Juicer) to generate aligned Hi-C contact maps and .hic binary files from raw FASTQ sequencing data, with output validation against reference checksums to ensure reproducibility and format correctness.

## When to use

You have raw Hi-C FASTQ files from a public repository (NCBI SRA, GEO, or ENCODE-deposited accession) and need to reproduce or validate Hi-C map generation following the ENCODE uniform processing standard, or you need to verify that your pipeline output conforms to reference format and integrity standards expected for Hi-C maps.

## When NOT to use

- Input is already a .hic file or pre-processed Hi-C contact map (skip directly to feature annotation or downstream analysis).
- You require GPU-accelerated HiCCUPS peak calling and do not have access to an NVIDIA GPU or CPU fallback alternative.
- Your cluster does not support any of Juicer's supported resource managers (SLURM, LSF, GridEngine, OpenLava) and cloud infrastructure is not available.

## Inputs

- Hi-C FASTQ dataset (paired-end sequencing reads)
- Reference genome FASTA file
- Restriction site file (e.g., for HindIII or MboI)
- Chromosome sizes file (chrom.sizes)

## Outputs

- Aligned reads file (BAM or intermediate SAM format)
- Hi-C contact map (.hic binary format)
- Merged and deduplicated alignments (merged_nodups)
- Pipeline statistics and QC metrics
- File checksum/hash for output validation

## How to apply

Clone the ENCODE Hi-C uniform processing pipeline from ENCODE-DCC/hic-pipeline and install Caper (Python wrapper for Cromwell) with Java >= 1.8 and Python >= 3.6. Configure your Caper configuration file (~/.caper/default.conf) for your platform (local, cloud, or cluster). Run the encode_hic_pipeline wrapper via Caper on your FASTQ input files to execute the Juicer-based pipeline, which performs alignment, duplicate removal, and constructs the Hi-C contact map in .hic binary format. After pipeline completion, validate the output .hic file by computing its checksum (e.g., MD5 hash) and compare it against the ENCODE reference output checksum to confirm reproducibility and detect any corruption or deviation in the processing pipeline.

## Related tools

- **Juicer** (Core pipeline platform that generates Hi-C maps from FASTQ raw data and provides command-line tools for feature annotation on Hi-C maps) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)** (Dockerized wrapper and Cromwell workflow (WDL) for running Juicer in cloud and cluster environments with standardized ENCODE parameters) — https://github.com/ENCODE-DCC/hic-pipeline
- **Caper** (Python wrapper for Cromwell that manages workflow execution and resource allocation across local, cloud, and cluster platforms) — https://github.com/ENCODE-DCC/caper
- **BWA (Burrows-Wheeler Aligner)** (Sequence alignment tool required to map FASTQ reads to the reference genome during the Juicer pipeline) — http://bio-bwa.sourceforge.net/
- **Juicer Tools** (Java-based post-processing and analysis tools for .hic files, including HiCCUPS peak calling and feature annotation) — https://github.com/theaidenlab/juicer/wiki/Download

## Examples

```
caper run hic.wdl -i tests/functional/json/test_hic.json --docker
```

## Evaluation signals

- Output .hic file exists in the correct binary format and can be read by Juicer Tools without errors.
- Computed MD5 or SHA checksum of the output .hic file matches the ENCODE reference checksum, confirming pipeline reproducibility and data integrity.
- Pipeline completion statistics (total reads, aligned reads, duplicate rate, contact map resolution) are within expected ranges for the input dataset and restriction enzyme used.
- Intermediate files (merged_nodups, statistics) are generated and pass format validation (correct column counts, coordinate ranges, and sorting order).
- Pipeline exits with status code 0 and all major stages (alignment, merge, dedup, final, postprocessing) complete without errors or warnings.

## Limitations

- The main aidenlab/juicer repository is under active development for Juicer 2.0; for production use, access the stable Juicer 1.6 release via GitHub Releases.
- CUDA and GPU resources are required for optimal HiCCUPS peak calling performance; CPU-based HiCCUPS is available but slower.
- AWS scripts in the repository are deprecated; use the ENCODE uniform processing pipeline with cloud support via Caper for cloud deployment.
- Juicer requires a cluster or cloud environment with >= 4 cores (minimum 1 core) and >= 64 GB RAM (minimum 16 GB RAM) for efficient processing of large Hi-C datasets.
- Output reproducibility is sensitive to Java version, BWA version, and CUDA version (if using GPU); users with different environments may observe checksum mismatches.

## Evidence

- [other] Juicer includes a pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline.: "Juicer includes a pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline."
- [other] Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map.: "Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map."
- [other] Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash.: "Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash."
- [other] Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness.: "Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness."
- [readme] Install Caper, requires `java` >= 1.8 and `python` >= 3.6, Caper >= 0.8.2.1 is required to run the pipeline.: "Install Caper, requires `java` >= 1.8 and `python` >= 3.6, Caper >= 0.8.2.1 is required to run the pipeline."
- [readme] Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM): "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"
- [readme] To run locally, you must first install `docker`. Then run the following command: `caper run hic.wdl -i tests/functional/json/test_hic.json --docker`: "To run locally, you must first install `docker`. Then run the following command: `caper run hic.wdl -i tests/functional/json/test_hic.json --docker`"

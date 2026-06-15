---
name: genomic-loop-call-interpretation
description: Use when you have a pre-generated .hic contact map file and need to identify and annotate chromatin loops or topologically associating domains (TADs) at high resolution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0440
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0097
  tools:
  - Juicer
  - juicer_cli_tools
  - HiCCUPS
  - ENCODE Hi-C pipeline
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

# genomic-loop-call-interpretation

## Summary

Interpret and annotate chromatin loop features detected on pre-generated Hi-C contact maps using Juicer's command-line feature annotation tools. This skill enables systematic extraction of loop coordinates and domain boundaries from kilobase-resolution Hi-C data, yielding structured feature annotations for downstream genomic analysis.

## When to use

You have a pre-generated .hic contact map file and need to identify and annotate chromatin loops or topologically associating domains (TADs) at high resolution. Apply this skill when your research question requires extracting loop coordinates, domain boundaries, or other structural features from Hi-C maps rather than generating the contact maps themselves from raw sequencing data.

## When NOT to use

- Input is raw FASTQ sequencing reads—use the Juicer pipeline stage for Hi-C map generation first
- You need to generate Hi-C maps from sequencing data—this skill assumes maps already exist; use the Juicer processing pipeline instead
- Your .hic file is incomplete or corrupted—verify file integrity before annotation

## Inputs

- .hic contact map file (binary Hi-C matrix format)
- genome reference identifier (e.g., hg19, mm10)
- feature annotation parameters (loop resolution threshold, domain size cutoffs)

## Outputs

- loop coordinate list (anchor pair positions in genomic coordinates)
- domain boundary file (TAD edge positions)
- annotated feature file (tool-specific format: loop anchors or domain boundaries with significance scores)

## How to apply

Load the pre-generated .hic contact map file into the Juicer command-line tools suite. Select the appropriate feature annotation algorithm based on your target features—loop-calling tools (e.g., HiCCUPS) for interaction anchors or domain-detection algorithms for TAD boundaries. Execute the selected tool with appropriate parameters (cluster-size thresholds, significance cutoffs, GPU acceleration if available for HiCCUPS). The tool outputs annotated feature coordinates in a structured format (e.g., loop anchor positions, domain boundaries with genomic coordinates). Validate output by checking that coordinates fall within the expected genomic range and that feature lists are non-empty.

## Related tools

- **Juicer** (Platform hosting command-line feature annotation tools for loop calling and domain detection on .hic contact maps) — https://github.com/aidenlab/juicer
- **juicer_cli_tools** (Command-line toolkit providing loop-calling and domain-detection algorithms executed on loaded .hic files) — https://github.com/aidenlab/juicer
- **HiCCUPS** (Peak-calling algorithm for chromatin loop detection; supports GPU acceleration via CUDA for high-performance annotation) — https://github.com/aidenlab/juicer/wiki/CPU-HiCCUPS
- **ENCODE Hi-C pipeline** (Dockerized wrapper around Juicer for cloud-based Hi-C processing including feature annotation) — https://github.com/ENCODE-DCC/hic-pipeline

## Evaluation signals

- Output feature file is non-empty and contains valid genomic coordinates within the specified genome bounds
- Loop anchors or domain boundaries align with expected Hi-C matrix features (peaks, block patterns) visible in the contact map
- Coordinate format matches tool specification (e.g., tab-delimited with chromosome, start, end columns for domains; anchor-pair format for loops)
- Feature significance scores (if present) are within expected ranges and show expected distribution (e.g., peaks in HiCCUPS output have q-values < 0.1)
- No null or malformed entries in output; all coordinates map to valid genomic regions in the reference

## Limitations

- Requires pre-computed .hic file; cannot operate on raw sequencing data or other Hi-C matrix formats without conversion
- HiCCUPS peak calling requires an NVIDIA GPU and CUDA (version 7 or 7.5 native; other versions require custom JCuda libraries) for best performance; CPU version available but slower
- Feature detection quality depends on Hi-C map resolution and sequencing depth; low-coverage maps may yield incomplete or unreliable annotations
- Tool parameters (cluster size, significance thresholds) must be tuned per experiment; default settings may not suit all cell types or chromatin organizations
- Output format varies by algorithm selected; downstream analysis may require format conversion or custom parsing

## Evidence

- [other] Juicer includes command line tools designed for feature annotation on Hi-C maps, enabling users to annotate features on pre-generated Hi-C map artifacts.: "Juicer includes command line tools designed for feature annotation on Hi-C maps, enabling users to annotate features on pre-generated Hi-C map artifacts."
- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [other] 1. Load the pre-generated .hic contact map file into Juicer command-line tools. 2. Select and execute the appropriate feature annotation tool (e.g., loop-calling or domain-detection algorithm) from the Juicer CLI suite. 3. Generate and output the annotated feature file in the format specified by the chosen tool (e.g., loop coordinates, domain boundaries).: "Load the pre-generated .hic contact map file into Juicer command-line tools. Select and execute the appropriate feature annotation tool (e.g., loop-calling or domain-detection algorithm). Generate"
- [readme] You must have an NVIDIA GPU to install CUDA. Instructions for installing the latest version of CUDA can be found on the NVIDIA Developer site. The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5.: "You must have an NVIDIA GPU to install CUDA. The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5."
- [readme] If you cannot access a GPU, you can run the CPU version of HiCCUPS directly using the `.hic` file and Juicer Tools.: "If you cannot access a GPU, you can run the CPU version of HiCCUPS directly using the `.hic` file and Juicer Tools."

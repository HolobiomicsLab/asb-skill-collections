---
name: hic-contact-map-feature-annotation
description: Use when you have completed Hi-C map generation (producing .hic files from aligned reads) and need to detect and annotate topological features such as chromatin loops, topologically associating domains (TADs), or interaction peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - juicer_tools
  - Juicebox
  - ENCODE Hi-C uniform processing pipeline
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

# Annotate Features on Hi-C Contact Maps Using Juicer Command Line Tools

## Summary

This skill applies Juicer's command-line post-processing tools to annotate structural features (loops, domains, peaks) on pre-generated Hi-C contact map files (.hic format). It enables quantitative extraction of 3D genome organization features for downstream analysis and interpretation.

## When to use

You have completed Hi-C map generation (producing .hic files from aligned reads) and need to detect and annotate topological features such as chromatin loops, topologically associating domains (TADs), or interaction peaks. This is the standard post-processing step in the Juicer pipeline when the contact matrix is ready but features have not yet been called.

## When NOT to use

- Raw FASTQ reads or alignment files are your input — use the Juicer pipeline (chimeric/merge/dedup/final stages) first to generate the .hic file.
- Feature annotations already exist in another format — this skill is for *de novo* feature calling, not format conversion or merging of existing annotations.
- You require sub-kilobase resolution features — Juicer is optimized for kilobase-resolution Hi-C data; ultra-high-resolution methods (e.g., Micro-C) may require specialized tools.

## Inputs

- .hic contact map file (binary Hi-C matrix)
- genome identifier (e.g., hg19, mm10)
- optionally: restriction enzyme site file or custom reference genome

## Outputs

- annotated loop coordinates file (e.g., loop_calls.bedpe or equivalent)
- domain boundary annotations (e.g., domain list with start/end positions)
- peak-calling results (for HiCCUPS: peak coordinates and significance scores)

## How to apply

Load the .hic contact map file into Juicer's command-line tools suite, which provides specialized algorithms for feature detection (e.g., HiCCUPS for loop calling, domain detection for TAD boundaries). Select the appropriate tool based on your target feature type and resolution requirements. Execute the chosen tool with parameters tuned to your sequencing depth and resolution; for GPU-accelerated peak calling (HiCCUPS), CUDA support is required, but CPU alternatives exist. The tool outputs annotated feature coordinates (loop anchors, domain boundaries) in standard formats. Validation occurs by visual inspection in Juicebox and by checking that detected features align with expected biological patterns (e.g., loops at known CTCF sites, domain sizes in expected ranges).

## Related tools

- **Juicer** (Main platform providing the .hic file format and command-line post-processing tools (HiCCUPS, domain detection, etc.) for feature annotation) — https://github.com/aidenlab/juicer
- **juicer_tools** (Command-line toolkit bundled with Juicer for executing feature annotation algorithms on .hic files; includes HiCCUPS peak caller and domain-detection modules) — https://github.com/aidenlab/juicer
- **Juicebox** (Interactive visualization tool for validating and exploring annotated features on Hi-C maps) — https://github.com/theaidenlab/Juicebox
- **ENCODE Hi-C uniform processing pipeline** (Dockerized, cloud-ready wrapper around Juicer for end-to-end Hi-C processing including feature annotation) — https://github.com/ENCODE-DCC/hic-pipeline

## Examples

```
java -Xmx32g -jar juicer_tools hiccups -m 512 -r 5000,10000 input.hic output_loops.bedpe
```

## Evaluation signals

- Output feature files are in expected format (bedpe for loops, coordinates for domains) and are non-empty with reasonable feature counts for the input resolution and depth.
- Annotated loops cluster near known regulatory markers (CTCF, cohesin) when cross-referenced with ChIP-seq or orthogonal 3D-mapping data.
- Domain sizes fall within expected biological ranges (typically 100 kb–3 Mb for mammalian TADs); domain boundaries coincide with known insulation sites.
- Features visualize correctly in Juicebox without coordinate out-of-bounds errors; loop anchors and domain edges align with visible contact matrix features.
- Reproducibility: re-running the same .hic file with identical parameters produces identical or near-identical feature calls (allowing for stochastic variation in GPU runs).

## Limitations

- HiCCUPS peak calling requires CUDA and an NVIDIA GPU for full performance; CPU versions are available but significantly slower. Native libraries are compiled for CUDA 7/7.5; other CUDA versions require manual library downloads from JCuda.
- Feature detection quality depends critically on sequencing depth and restriction enzyme fragment distribution; shallow data or biased restriction maps can yield false negatives or spurious calls.
- Juicer is optimized for kilobase-resolution Hi-C; performance or applicability on ultra-high-resolution data (Micro-C, Pore-C) has not been validated in this documentation.
- The main repository focuses on Juicer 2.0 (under active development); Juicer 1.6 is the last stable release. Active development may introduce breaking changes; users requiring stability should pin version 1.6.

## Evidence

- [other] Juicer includes command line tools designed for feature annotation on Hi-C maps, enabling users to annotate features on pre-generated Hi-C map artifacts.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [other] The post-processing workflow selects and executes appropriate feature annotation tools from the Juicer CLI suite.: "Select and execute the appropriate feature annotation tool (e.g., loop-calling or domain-detection algorithm) from the Juicer CLI suite."
- [readme] HiCCUPS peak calling requires CUDA and GPU hardware for optimal performance.: "CUDA (for HiCCUPS peak calling) You must have an NVIDIA GPU to install CUDA."
- [readme] The native CUDA libraries bundled with Juicer support CUDA 7 and 7.5; other versions require manual library sourcing.: "The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5. Other versions of CUDA can be used, but you will need to download the respective native libraries from JCuda."
- [readme] Juicer 1.6 is the last stable release; the main GitHub repository contains the in-development Juicer 2.: "To access Juicer 1.6 (last stable release), please see the Github Release. If you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development."
- [readme] Feature annotation is a post-processing stage that runs after .hic file creation.: "-Use "postproc" when the hic files have been created and only postprocessing feature annotation remains to be completed."
- [readme] Juicer requires minimum 4 cores and 64 GB RAM for optimal performance; lower limits are 1 core and 16 GB.: "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"

---
name: hi-c-normalization-and-bias-correction
description: Use when after generating raw Hi-C contact matrices from aligned reads (post-merge, pre-analysis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - Juicer 1.6
  - Juicer 2
  - Juicer Tools
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

# Hi-C Normalization and Bias Correction

## Summary

Normalize and correct systematic biases in Hi-C contact matrices to enable accurate comparison of interaction frequencies across genomic regions and between samples. This skill is essential for removing technical artifacts (e.g., restriction enzyme cutting efficiency, GC content, mappability) that distort raw contact counts and obscure true 3D chromatin structure.

## When to use

Apply this skill after generating raw Hi-C contact matrices from aligned reads (post-merge, pre-analysis). Use it when you need to compare interaction frequencies between regions with different sequence properties, merge data across multiple replicates or experiments, or prepare matrices for downstream analysis (peak calling, domain detection, comparative genomics). Essential when raw contact counts show systematic variation correlated with genomic features rather than true interaction strength.

## When NOT to use

- Input is already a normalized or published Hi-C matrix from a repository — re-normalization may introduce artifacts or is redundant.
- Data is from a non-standard restriction enzyme or in-situ protocol where Juicer's built-in bias model has not been validated — consider custom normalization pipelines.
- Sample size or sequencing depth is extremely low (< 1M valid pairs) — normalization may amplify noise rather than reveal signal.

## Inputs

- Merged, deduplicated Hi-C alignment file (merged_nodups format or equivalent SAM/BAM)
- Reference genome sequence (FASTA)
- Restriction enzyme specification (e.g., HindIII, MboI)
- Chromosome sizes file (chrom.sizes)
- Juicer pipeline configuration (genome ID, queue parameters, computational resources)

## Outputs

- Normalized Hi-C contact matrix (.hic file format)
- Bias correction factors (per-bin weights, embedded in .hic)
- Contact matrix statistics and quality metrics

## How to apply

The Juicer platform includes normalization as part of its unified pipeline: after read alignment, deduplication, and chimera filtering, the pipeline constructs a raw contact matrix and applies normalization during .hic file creation. The normalization step removes biases by modeling how sequence-level and mappability factors affect observed contact counts. Configure the pipeline with the appropriate reference genome and restriction enzyme (e.g., HindIII, MboI) so that bias correction can account for restriction site distribution and local sequence properties. Execute the final pipeline stage to generate the normalized .hic output file. Verify that the resulting contact matrix shows biologically plausible patterns (e.g., strong diagonal, decay with genomic distance) and that inter-regional comparisons are no longer confounded by GC content or mappability differences.

## Related tools

- **Juicer** (Unified Hi-C processing pipeline that performs read alignment, deduplication, chimera filtering, and normalization to generate .hic contact matrices) — https://github.com/aidenlab/juicer
- **Juicer 1.6** (Stable release version of Juicer with mature normalization and bias correction implementation) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2** (Development version with active updates to normalization methods and bias correction algorithms) — https://github.com/aidenlab/juicer
- **Juicer Tools** (Command-line utilities for post-processing and feature annotation on normalized Hi-C maps; includes normalization visualization and diagnostic functions) — https://github.com/theaidenlab/juicer/wiki/Download
- **ENCODE Hi-C uniform processing pipeline** (Dockerized, cloud-friendly implementation of Juicer-based normalization for standardized Hi-C data processing) — https://github.com/ENCODE-DCC/hic-pipeline

## Examples

```
juicer.sh -g hg19 -d /path/to/topDir -q short -l long -s HindIII -C 30000000 -D /path/to/juicer/scripts
```

## Evaluation signals

- Output .hic file is valid and readable by Juicer Tools; file size and structure are consistent with input data depth (typically scales with valid pair count).
- Contact matrix decay with genomic distance follows expected power-law trend; no strong systematic biases remain in bins with similar GC content or mappability.
- Normalized contact counts in biologically replicate experiments show high correlation (e.g., Pearson r > 0.8–0.9 at 10–100 kb resolution); inter-sample comparisons are not confounded by sequence properties.
- Peak calling or domain detection on normalized matrices yields known topologically associating domains (TADs) or loops at expected genomic locations; results are consistent with independent chromatin conformation capture assays (e.g., 3C-qPCR, Capture-C).
- Bias correction factors (per-bin weights in .hic metadata) are smooth and reflect expected biases: lower weights for low-mappability or extreme-GC regions, higher weights for standard genomic regions.

## Limitations

- Juicer's normalization assumes standard restriction enzyme protocols (HindIII, MboI, etc.); non-standard or in-situ-specific enzymes may not be fully supported without manual parameter tuning.
- Very low-coverage samples (< 1M valid pairs) or highly fragmented assemblies may suffer from overfitting or unreliable bias estimates.
- Normalization is optimized for mammalian genomes; application to highly repetitive, polyploid, or poorly assembled genomes may require custom reference preparation and validation.
- Batch effects between library preparations or sequencing runs are not corrected by Juicer's bias model; sample-level harmonization may be needed for cross-batch comparisons.
- README notes that AWS scripts are deprecated; cloud users are directed to the ENCODE pipeline instead. Development version (Juicer 2) is under active development; stability and backward compatibility not guaranteed.

## Evidence

- [other] Juicer includes a pipeline that generates Hi-C maps from fastq raw data files as input, producing processed Hi-C map artifacts.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [other] The pipeline performs alignment, contact matrix construction, and normalization as integrated steps.: "Execute the Juicer pipeline on the raw FASTQ files to perform read alignment, contact matrix construction, and normalization."
- [other] Juicer requires genome and restriction enzyme specification for proper bias correction.: "Configure the Juicer pipeline with appropriate parameters for the reference genome, restriction enzyme, and computational resources"
- [other] The pipeline produces a .hic output file containing the processed Hi-C contact map.: "Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map."
- [readme] Juicer is optimized for parallel computation and works with multiple cluster resource managers.: "Juicer is a pipeline optimized for parallel computation on a cluster. Juicer consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools."
- [readme] SLURM and CPU scripts are the most up-to-date implementations; AWS scripts are deprecated.: "The SLURM and CPU scripts are the most up to date. For cloud computing, we recommend the ENCODE uniform processing pipeline based on Juicer"

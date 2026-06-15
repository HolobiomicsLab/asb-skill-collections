---
name: kilobase-resolution-genomics-analysis
description: Use when you have raw Hi-C FASTQ data and need to generate contact maps at kilobase resolution, or you have pre-generated .hic files and need to annotate structural features (loops, domains) for downstream 3D genome analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3169
  tools:
  - Juicer
  - Juicer 1.6
  - Juicer 2.0
  - ENCODE Hi-C uniform processing pipeline
  - BWA (Burrows-Wheeler Aligner)
  - HiCCUPS
  - Juicebox
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

# kilobase-resolution-genomics-analysis

## Summary

Apply Juicer's integrated pipeline and command-line tools to process raw Hi-C sequencing data (FASTQ) into kilobase-resolution contact maps (.hic files) and annotate structural features such as loops and topologically associating domains (TADs). This skill encompasses both the primary data processing stage (alignment, deduplication, .hic file generation) and post-processing feature annotation.

## When to use

You have raw Hi-C FASTQ data and need to generate contact maps at kilobase resolution, or you have pre-generated .hic files and need to annotate structural features (loops, domains) for downstream 3D genome analysis. This skill is appropriate when working with chromosome conformation capture (3C-based) experiments and requires parallel cluster or cloud infrastructure.

## When NOT to use

- Input data are not Hi-C or 3C-based; Juicer is specialized for chromosome conformation capture.
- You already have pre-processed, normalized contact matrices in a standard format (e.g., HDF5, sparse matrix) and only need downstream statistical analysis, not raw-read processing.
- Your cluster or compute environment does not support any of the supported job schedulers (SLURM, LSF, GridEngine, OpenLava) or cloud/local execution; Juicer requires orchestration infrastructure.

## Inputs

- FASTQ files (raw Hi-C sequencing reads)
- Genome reference (FASTA or genome ID, e.g., 'hg19')
- Restriction enzyme site file (coordinates of cut sites)
- Chromosome sizes file (.chrom.sizes)

## Outputs

- .hic contact map file (multi-resolution, indexed)
- Annotated loop coordinates (BED/BEDPE format or Juicer native)
- Topologically associating domain boundaries (domain annotation file)
- Pipeline statistics and QC logs

## How to apply

The Juicer platform operates in two sequential stages. First, invoke the main pipeline (juicer.sh) on your cluster with FASTQ files located in [topDir]/fastq, specifying the genome ID (e.g., 'hg19' or 'mm10'), restriction enzyme site (e.g., 'HindIII', 'MboI'), and resource queue parameters appropriate to your scheduler (SLURM, LSF, GridEngine, or single CPU). The pipeline performs alignment via BWA, chimera handling, deduplication, and generates a merged .hic contact map file. Second, execute post-processing feature annotation tools (accessible via Juicer command-line tools) on the resulting .hic file to call loops (using HiCCUPS, which requires CUDA/GPU for optimal performance) or detect topologically associating domains. Validate output by checking that the .hic file is properly indexed, contains multi-resolution matrix data at 5 kb and coarser scales, and that annotation outputs (loop coordinates, domain boundaries) are in standard formats (e.g., BED, BEDPE). The choice between GPU-accelerated and CPU-only HiCCUPS depends on available hardware; CPU versions are available but slower.

## Related tools

- **Juicer** (Main platform for Hi-C processing pipeline and feature annotation command-line tools) — https://github.com/aidenlab/juicer
- **Juicer 1.6** (Last stable release (recommended for production use)) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2.0** (Active development version with additional features) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline** (Dockerized Juicer-based pipeline optimized for cloud execution) — https://github.com/ENCODE-DCC/hic-pipeline
- **BWA (Burrows-Wheeler Aligner)** (Aligns Hi-C reads to reference genome)
- **HiCCUPS** (Peak-calling tool for loop annotation; GPU version requires CUDA)
- **Juicebox** (Interactive visualization and analysis of .hic contact maps) — https://github.com/theaidenlab/Juicebox

## Examples

```
juicer.sh -g hg19 -d /path/to/topDir -q short -l long -s HindIII
```

## Evaluation signals

- Verify that the output .hic file is correctly indexed and can be opened in Juicebox or queried via Juicer Tools without I/O errors.
- Check that multi-resolution matrices are present at standard resolutions (e.g., 5 kb, 10 kb, 25 kb, 50 kb) by inspecting the .hic file header or using Juicer Tools dump command.
- Confirm that pipeline statistics (total reads, duplicate rate, valid-interaction percentage) meet expected quality thresholds for your organism and enzyme (typically >10M valid interactions for mammalian genomes).
- Validate annotated features (loops, domains) by comparing to independent datasets or visual inspection in Juicebox; loop coordinates should be in valid BED/BEDPE format with non-overlapping, contiguous domain calls.
- Verify that no stage of the pipeline (alignment, deduplication, final) exited with error status and that all expected intermediate files were created and moved to final directories.

## Limitations

- Juicer requires a compute cluster or cloud infrastructure with job scheduling (SLURM, LSF, GridEngine, OpenLava) or single-CPU fallback; it is not designed for desktop execution of large datasets.
- HiCCUPS loop calling requires an NVIDIA GPU and CUDA 7.0+ for best performance; CPU-only versions are available but substantially slower.
- The README notes that AWS scripts are deprecated; cloud execution is recommended via the ENCODE dockerized pipeline.
- Juicer 2.0 is under active development and may be less stable than the 1.6 stable release; production workflows should use 1.6 unless specific Juicer 2.0 features are required.
- Feature annotation quality depends on sequencing depth and read quality; shallow or low-quality Hi-C libraries may produce unreliable loop/domain calls.

## Evidence

- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature"
- [readme] Juicer is optimized for parallel computation on a cluster and consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools.: "Juicer is a pipeline optimized for parallel computation on a cluster. Juicer consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools."
- [readme] Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM). Juicer currently works with OpenLava, LSF, SLURM, and GridEngine.: "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM). Juicer currently works with the following resource management software:"
- [readme] To access Juicer 1.6 (last stable release); if you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development.: "To access Juicer 1.6 (last stable release), please see [the Github Release]. If you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development."
- [readme] The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5. For best performance, use a dedicated GPU. If you cannot access a GPU, you can run the CPU version of HiCCUPS directly using the .hic file and Juicer Tools.: "The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5. For best performance, use a dedicated GPU. If you cannot access a GPU, you can run the CPU version of HiCCUPS"

---
name: chip-seq-read-alignment-filtering
description: 'Use when when beginning peak calling on ChIP-Seq data: you have raw single-end or paired-end BED/BEDPE alignment files for both ChIP and control samples and need to remove duplicate reads before predicting fragment length and building local bias models.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3179
  tools:
  - macs3 filterdup
  - macs3 predictd
  - macs3 callpeak
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_macs
    doi: 10.1186/gb-2008-9-9-r137
    title: macs
  dedup_kept_from: coll_macs
schema_version: 0.2.0
---

# ChIP-Seq read alignment filtering

## Summary

Filter redundant reads from ChIP-Seq alignment files and perform duplicate-aware read counting prior to peak calling. This is a critical initial step in MACS3 callpeak analysis that removes PCR artifacts and establishes the true library complexity, which affects all downstream fragment length prediction and background modeling.

## When to use

When beginning peak calling on ChIP-Seq data: you have raw single-end or paired-end BED/BEDPE alignment files for both ChIP and control samples and need to remove duplicate reads before predicting fragment length and building local bias models. This step is obligatory before macs3 predictd and macs3 pileup.

## When NOT to use

- Input is already a deduplicated or UMI-collapsed alignment file (would lose information on true duplicate complexity).
- Analysis goal is to preserve all reads for coverage visualization without statistical peak calling (use macs3 pileup directly instead).
- Data is single-cell ChIP-Seq or other ultra-sparse ChIP where aggressive duplicate filtering would remove real signal at low coverage sites.

## Inputs

- ChIP sample alignment file in BED format (e.g., CTCF_ChIP_200K.bed.gz)
- Control sample alignment file in BED format (e.g., CTCF_Control_200K.bed.gz)

## Outputs

- Filtered ChIP BED file with duplicates removed
- Filtered control BED file with duplicates removed
- Read count statistics (number of reads retained after duplicate filtering)

## How to apply

Apply macs3 filterdup separately to both ChIP and control BED files using --keep-dup=1 to retain one copy of each duplicate read cluster (or --keep-dup=all to retain all duplicates, depending on sequencing depth and library complexity expectations). The command reads genomic coordinates from the alignment file, identifies reads mapping to identical positions, and outputs filtered BED with duplicate read counts recorded. Record the final read counts for each sample (e.g., ChIP: 199,583; Control: 199,867) as these are used to compute genome-wide background (control_reads × fragment_length / genome_size) and the ChIP-to-control scaling ratio in later steps. The duplicate filtering rate and absolute read counts are quality metrics that should be assessed before proceeding to fragment length prediction.

## Related tools

- **macs3 filterdup** (Remove redundant reads from identical genomic positions in ChIP and control BED files) — https://github.com/macs3-project/MACS
- **macs3 predictd** (Predict fragment length d from filtered ChIP data (downstream consumer of this skill's output)) — https://github.com/macs3-project/MACS
- **macs3 callpeak** (End-to-end peak calling pipeline that includes filterdup as its first internal step) — https://github.com/macs3-project/MACS

## Examples

```
macs3 filterdup -i CTCF_ChIP_200K.bed.gz -o CTCF_ChIP_filtered.bed --keep-dup=1
```

## Evaluation signals

- Read count statistics are reported and logged (e.g., 'ChIP: 199,583 reads retained after filtering'; 'Control: 199,867 reads retained'); verify no reads are lost if --keep-dup=all is used.
- Filtered BED files are valid and sortable; spot-check that coordinates and strand annotations are preserved.
- Duplicate filtering rate is biologically plausible (typically 5–30% for ChIP-Seq depending on sequencing depth and PCR amplification); unusually high filtering (>50%) or no filtering (0%) should trigger investigation.
- Read counts for ChIP and control are within the same order of magnitude; extreme imbalance (e.g., >10-fold) may indicate quality issues in one sample.
- Filtered read counts are suitable inputs for genome-wide background calculation: control_reads × predicted_d / genome_size should yield a reasonable background (e.g., 0.01–0.1 for mammalian genomes with standard coverage).

## Limitations

- Duplicate filtering is position-based and does not use molecular barcodes (UMIs), so true biological duplicates from independent fragment molecules are also removed if they map to identical coordinates.
- The --keep-dup parameter assumes all reads at identical positions are PCR artifacts; in high-coverage regions or with multi-mapping reads, this may over-filter real signal.
- Paired-end BED files (.bedpe) require the pe variant of filterdup; single-end BED assumes fragments are not strand-paired, which may inflate apparent duplication rates.

## Evidence

- [methods] MACS3 does offer a range of subcommands that allow you to customize every step of your analysis: "MACS3 does offer a range of subcommands that allow you to customize every step of your analysis"
- [methods] In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location: "In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location"
- [methods] we'll explain how you can accomplish this using the `filterdup` subcommand: "we'll explain how you can accomplish this using the `filterdup` subcommand"
- [other] MACS3 callpeak performs duplicate filtering as an initial step and predicts fragment length d, which is crucial for ChIP-Seq analysis and used in subsequent peak calling steps.: "MACS3 callpeak performs duplicate filtering as an initial step and predicts fragment length d, which is crucial for ChIP-Seq analysis and used in subsequent peak calling steps"
- [other] Filter duplicate reads from both ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording final read counts (ChIP: 199,583; Control: 199,867).: "Filter duplicate reads from both ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording final read counts (ChIP: 199,583; Control: 199,867)"

---
name: duplicate-read-filtering-and-normalization
description: Use when you have raw ChIP-Seq and control BED files with potential PCR duplicates or unequal sequencing depths. Duplicate filtering is mandatory before estimating fragment length (predictd) or generating coverage pileups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 filterdup
  - macs3 bdgopt
  - macs3 pileup
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

# duplicate-read-filtering-and-normalization

## Summary

Remove redundant reads from ChIP-Seq data and normalize read counts across samples to enable unbiased statistical comparison. This skill is essential before peak calling, as duplicate reads inflate coverage at single genomic loci and violate the assumption of independent sampling required for p-value and q-value calculations.

## When to use

Apply this skill when you have raw ChIP-Seq and control BED files with potential PCR duplicates or unequal sequencing depths. Duplicate filtering is mandatory before estimating fragment length (predictd) or generating coverage pileups. Normalization is required whenever ChIP and control samples have different total read counts, so that downstream statistical tests (bdgcmp with qpois or ppois) operate on comparably scaled signal tracks.

## When NOT to use

- Input is already a deduplicated BAM or BED file (e.g., from a prior alignment pipeline); duplicate filtering would be redundant.
- Control sample is missing or the experiment is single-condition (unpaired); normalization cannot be computed without a baseline for depth correction.
- Fragment length d has not yet been estimated; scaling the lambda background requires knowledge of d to construct the pileup tracks at the correct extension length.

## Inputs

- ChIP BED file (read locations, one per line: chromosome, start, end, etc.)
- Control BED file (same format as ChIP file)

## Outputs

- Filtered ChIP BED file (duplicates removed)
- Filtered control BED file (duplicates removed)
- Final read count for ChIP sample (scalar: number of unique genomic positions after filtering)
- Final read count for control sample (scalar: number of unique genomic positions after filtering)
- Sequencing depth scaling factor (ratio: ChIP_reads / control_reads)

## How to apply

First, filter duplicate reads from both ChIP and control BED files using macs3 filterdup with --keep-dup parameter (e.g., --keep-dup=1 keeps a maximum of 1 read per genomic location); record the final read counts for each sample, as these normalization factors are needed later. Second, compute the sequencing-depth scaling ratio as (final_ChIP_reads / final_control_reads) and apply it via macs3 bdgopt multiply when scaling the local lambda background track. This ensures that when ChIP and control pileup tracks are compared in bdgcmp, both are on the same effective sequencing depth scale, preventing false enrichment calls due to differential coverage rather than true ChIP signal.

## Related tools

- **macs3 filterdup** (Removes redundant reads at each genomic locus; outputs deduplicated BED files and reports final read counts for normalization) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Applies multiplicative scaling to normalized background tracks (pileup BEDGRAPH) using the sequencing depth ratio (ChIP_reads / control_reads)) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Generates coverage BEDGRAPH tracks from deduplicated BED files; inputs are the output of filterdup) — https://github.com/macs3-project/MACS

## Examples

```
macs3 filterdup -i CTCF_ChIP_200K.bed.gz -o CTCF_ChIP_filtered.bed --keep-dup=1 && macs3 filterdup -i CTCF_Control_200K.bed.gz -o CTCF_Control_filtered.bed --keep-dup=1
```

## Evaluation signals

- Final read counts from macs3 filterdup should be ≤ input read counts (monotonic decrease after duplicate removal).
- The sequencing depth scaling ratio (ChIP_reads / control_reads) should be close to 1.0 for well-balanced experiments; large deviations (e.g., >2-fold) indicate substantial imbalance and justify the normalization step.
- After scaling the local lambda background with bdgopt multiply using the depth ratio, the scaled lambda BEDGRAPH should have signal levels comparable to the ChIP pileup BEDGRAPH (visual inspection of overlaid tracks or summary statistics of min/max/median per-base values).
- When bdgcmp is run on scaled ChIP vs. scaled lambda, the resulting p-value/q-value distribution should be reasonable (e.g., not all values ≈ 1.0 or all ≈ 0.0), indicating that samples were properly normalized before statistical comparison.
- Peaks called via bdgpeakcall on the score track should not show obvious strand bias or edge artifacts attributable to scaling errors (e.g., all peaks on one strand or clustered at read length boundaries).

## Limitations

- macs3 filterdup uses a simple position-based deduplication strategy: it keeps only a maximum number of reads (--keep-dup) at each genomic location, which may not fully account for PCR duplicates spread over a small window or for sequencing-error-induced pseudo-duplicates.
- Sequencing depth normalization assumes that the ChIP enrichment is global and unbiased; if enrichment is localized to specific chromosomes or regions, depth-based scaling may overcorrect or undercorrect in those regions.
- The scaling factor is applied uniformly across the entire genome; no per-chromosome or per-region adjustment is made, which may mask subtle biases in library construction or sequencing.
- If control sequencing depth is very low (few reads), the scaling ratio becomes unstable, and bdgopt multiply can produce artifactually large lambda values in sparse regions.

## Evidence

- [methods] In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location: "In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location"
- [methods] Filter duplicate reads from CTCF ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording the final read counts for each sample.: "Filter duplicate reads from CTCF ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording the final read counts for each sample"
- [methods] To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth: "To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth"
- [methods] Scale local lambda bias to ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts.: "Scale local lambda bias to ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts"
- [methods] we'll explain how you can accomplish this using the `filterdup` subcommand: "we'll explain how you can accomplish this using the `filterdup` subcommand"

---
name: chip-seq-signal-pileup-extension
description: Use when after duplicate filtering and fragment length prediction (d) in ChIP-Seq analysis, when you need to convert discrete read alignments into continuous coverage signal for comparison against control background.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0091
  tools:
  - macs3 pileup
  - macs3 predictd
  - macs3 filterdup
  - macs3 bdgopt
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans:
- generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand
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

# ChIP-Seq Signal Pileup Extension

## Summary

Extend aligned ChIP-Seq reads to their predicted fragment length and generate genome-wide coverage (pileup) tracks. This is a critical intermediate step in peak calling that converts single-end or paired-end reads into continuous signal intensity maps needed for subsequent statistical comparison against background.

## When to use

After duplicate filtering and fragment length prediction (d) in ChIP-Seq analysis, when you need to convert discrete read alignments into continuous coverage signal for comparison against control background. Specifically, apply this skill when preparing ChIP pileup tracks before constructing local bias models or performing statistical testing with bdgcmp.

## When NOT to use

- When input reads are already in bedgraph or BigWig format (already represent continuous signal, not discrete alignments).
- When analyzing broad histone marks without prior fragment length prediction; use bdgbroadcall instead of narrow peak calling workflow.
- When fragment length d is unknown or invalid (negative, zero, or larger than biological expectation); predictd must succeed first.

## Inputs

- Filtered ChIP-Seq BED file (duplicate-filtered reads with columns: chromosome, start, end, name, score, strand)
- Filtered control BED file (duplicate-filtered reads in BED format, optional but recommended)
- Predicted fragment length d in base pairs (integer, e.g. 254)
- Genome size (string code like 'hs' for human, or integer)

## Outputs

- ChIP pileup bedgraph file (chromosome, start, end, coverage depth)
- Control pileup bedgraph file (chromosome, start, end, coverage depth)
- d-background bedgraph (control extended to d/2 bp, used for local bias at fragment scale)
- slocal-background bedgraph (control coverage in 1 kb window, used for local bias)
- llocal-background bedgraph (control coverage in 10 kb window, used for local bias)

## How to apply

Use macs3 pileup on the filtered ChIP BED file with --extsize set to the predicted fragment length d (e.g., 254 bp for CTCF). This extends each aligned read in both directions to simulate the actual DNA fragment size, creating a bedgraph file where each genomic position is assigned a read count representing local sequencing depth. The extension parameter is critical because it normalizes for the fragment length that was determined in the predictd step, allowing proper comparison with control signal that is similarly extended. Generate separate pileup tracks for both ChIP and control samples; for control, additionally apply the -B flag to generate bidirectional background tracks at multiple scales (d/2, 1 kb, 10 kb) used in local bias calculation. The output bedgraph format preserves base-pair resolution coverage for downstream statistical testing.

## Related tools

- **macs3 pileup** (Extends filtered ChIP and control reads to fragment length d and generates base-pair resolution coverage bedgraph files; primary tool for this skill) — https://github.com/macs3-project/MACS
- **macs3 predictd** (Predicts the fragment length d from ChIP data before pileup; must be run prior to this skill) — https://github.com/macs3-project/MACS
- **macs3 filterdup** (Filters duplicate reads from BED files to remove redundant alignments; produces cleaned input for pileup) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalizes background pileup tracks by multiply operations (factors 0.254 for slocal, 0.0254 for llocal); post-processes pileup output) — https://github.com/macs3-project/MACS

## Examples

```
macs3 pileup -f BED -i CTCF_ChIP_200K.bed.gz --extsize 254 -o CTCF_ChIP_pileup.bedgraph && macs3 pileup -f BED -i CTCF_Control_200K.bed.gz -B --extsize 254 -o CTCF_Control_pileup.bedgraph
```

## Evaluation signals

- Output bedgraph files are valid BEDGRAPH format (4-column: chrom, chromStart, chromEnd, dataValue) with no negative values and monotonic or sensible coverage transitions.
- Pileup coverage values are integers ≥ 0 and do not exceed input read count (sanity bound: sum of all base-pair coverages ≥ number of input reads * (d-1), accounting for overlap).
- ChIP pileup shows enriched peaks at known binding sites (e.g., reproducible peaks in replicates); control pileup shows more uniform, lower-intensity signal.
- Fragment length d correctly extends reads: peak width in bedgraph should be approximately d bp wider than original read length (typically 50 bp), resulting in broader coverage features.
- slocal and llocal background tracks show smooth, gradually increasing coverage away from control peaks, compatible with downstream local bias model (max operation will not produce artifacts).

## Limitations

- Fragment length prediction (predictd) may fail or produce unreliable estimates if ChIP enrichment is weak, low sequencing depth, or complex peak structure; pileup extension accuracy depends entirely on correctness of d.
- Pileup extension assumes all reads represent single DNA fragments of uniform length d; paired-end reads are treated as fragments defined by insert size, not by d parameter.
- bedgraph resolution is fixed at single base-pair; very deep sequencing may produce large output files (bedgraph is uncompressed); consider compression or binning for very large genomes.
- Symmetric extension (both 5' and 3' directions) assumes strand-symmetric fragment distribution; directional bias in fragment orientation will not be captured by simple extension.

## Evidence

- [methods] generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand: "generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand"
- [methods] Now that you've estimated the fragment length, we can proceed to generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand: "Now that you've estimated the fragment length, we can proceed to generate a pileup track for the ChIP sample"
- [other] Generate ChIP pileup coverage track using macs3 pileup with --extsize 254 (the predicted fragment length): "Generate ChIP pileup coverage track using macs3 pileup with --extsize 254 (the predicted fragment length)"
- [other] Build local bias tracks from filtered control data using macs3 pileup with -B option at three scales (d/2=127 bp for d-background, 500 bp for 1 kb slocal, 5000 bp for 10 kb llocal): "Build local bias tracks from filtered control data using macs3 pileup with -B option at three scales"
- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"
- [methods] To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function: "To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function"

---
name: bedgraph-file-format-manipulation
description: Use when you have aligned ChIP-Seq reads (in BED or BEDPE format) and need to convert them into quantitative genome-wide signal tracks (coverage, p-value, or q-value scores) for downstream statistical comparison or peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - macs3 pileup
  - macs3 bdgopt
  - macs3 bdgcmp
  - macs3 bdgpeakcall
  - macs3 filterdup
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

# BEDGRAPH file format manipulation

## Summary

BEDGRAPH is a tab-delimited format for storing continuous genomic signal (coverage, p-values, q-values) across regions, with one score per base pair. This skill covers generating, transforming, and combining BEDGRAPH tracks through sequential operations (pileup, normalization, comparison, merging) to produce score landscapes suitable for peak calling.

## When to use

You have aligned ChIP-Seq reads (in BED or BEDPE format) and need to convert them into quantitative genome-wide signal tracks (coverage, p-value, or q-value scores) for downstream statistical comparison or peak detection. Specifically, apply this skill when you must: (1) generate pileup coverage tracks from reads extended to a known or predicted fragment length, (2) normalize background tracks to account for sequencing depth or local bias, (3) compute statistical scores (p-value or q-value) by comparing ChIP and control signal tracks, or (4) merge multiple background layers (fragment-length, 1kb local, 10kb local, genome-wide) into a single background estimate.

## When NOT to use

- Input reads are already in BEDGRAPH or BigWig format — skip pileup generation and proceed directly to normalization or comparison.
- You are performing broad peak calling — use `bdgbroadcall` instead of the narrow peak pathway; background layer construction differs.
- Fragment length is unknown and unpredictable (e.g., highly variable insert-size library) — prediction may fail; consider external QC or alternative peak callers.

## Inputs

- Filtered ChIP-Seq reads in BED format (from macs3 filterdup)
- Filtered control reads in BED format (from macs3 filterdup)
- Predicted fragment length d (from macs3 predictd)
- Genome size (integer, bp)

## Outputs

- ChIP pileup BEDGRAPH (coverage track, one score per base pair)
- Control pileup BEDGRAPH files (d, slocal, llocal)
- Combined local lambda (background bias) BEDGRAPH
- Score BEDGRAPH (p-value or q-value track, one score per base pair)

## How to apply

Begin by generating a pileup BEDGRAPH from filtered ChIP reads using `macs3 pileup --extsize <fragment_length>`, which extends each read to the predicted fragment length d and outputs continuous signal. For background (control) data, generate three separate pileup BEDGRAPH files with different extension sizes: d (fragment length), slocal (1 kb default), and llocal (10 kb default). Normalize the slocal and llocal backgrounds using `macs3 bdgopt --method multiply` with scaling factors (d/slocal and d/llocal ratios) to make them comparable. Combine the three background tracks by computing the maximum bias at each genomic position using sequential `macs3 bdgcmp --method max` operations, then add a genome-wide background constant (control_reads × fragment_length / genome_size). Scale the combined local lambda to ChIP sequencing depth by multiplying with the ratio of final ChIP to control read counts using `macs3 bdgopt --method multiply`. Finally, compare the ChIP pileup against the scaled local lambda using `macs3 bdgcmp --method qpois` (for q-values) or `--method ppois` (for p-values) to generate a score BEDGRAPH. Choose the statistical method (qpois vs. ppois) based on whether you need multiple-testing-corrected significance (q-value) or raw statistical significance (p-value).

## Related tools

- **macs3 pileup** (Generates pileup BEDGRAPH coverage tracks from filtered reads, extending each read to a specified fragment length (--extsize parameter); used for both ChIP and control samples.) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalizes and scales BEDGRAPH files using arithmetic operations (multiply mode); applied to slocal and llocal background tracks to adjust for fragment-length ratios and sequencing depth.) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (Compares two BEDGRAPH files element-wise using statistical methods (qpois, ppois, max); outputs score BEDGRAPH (p/q-values) or combined background tracks.) — https://github.com/macs3-project/MACS
- **macs3 bdgpeakcall** (Identifies peaks from score BEDGRAPH by filtering regions above a score cutoff; final step in the peak-calling pipeline, uses BEDGRAPH as input.) — https://github.com/macs3-project/MACS
- **macs3 filterdup** (Preprocesses input BED files by removing duplicate reads at the same genomic location; output serves as input to pileup generation.) — https://github.com/macs3-project/MACS

## Examples

```
macs3 pileup -f BED -i CTCF_ChIP_filtered.bed -o CTCF_ChIP.bdg --extsize 147 -B && macs3 pileup -f BED -i CTCF_Control_filtered.bed -o CTCF_Control_d.bdg --extsize 147 -B && macs3 bdgcmp -t CTCF_ChIP.bdg -c CTCF_Control_d.bdg -m qpois -o CTCF_ChIP_vs_control_qvalue.bdg
```

## Evaluation signals

- Pileup BEDGRAPH header and format validation: confirm three columns (chrom, start, end) with numeric coverage values and no gaps exceeding the read length.
- Signal continuity: all genomic positions covered by extended reads must have a non-zero score; absence of gaps indicates correct fragment-length extension.
- Background track relationships: verify that max(d, slocal, llocal) ≥ all individual components at each position, confirming proper merging logic.
- Sequencing-depth scaling: check that scaled local lambda = original local lambda × (ChIP_depth / control_depth); scaling ratio should be > 0 and typically between 0.5 and 2.0 for similar sequencing depths.
- Score distribution sanity: p/q-value BEDGRAPH should have scores ≥ 0; q-values should be ≤ p-values at each position due to multiple-testing correction.

## Limitations

- Fragment length prediction (macs3 predictd) may fail or return unreliable estimates for samples with very short or very long inserts, or low ChIP enrichment; manual specification of --extsize may be necessary.
- Local background calculation (combining d, slocal, llocal) assumes symmetrical fragment-length extension; asymmetric or paired-end protocols may require custom handling.
- BEDGRAPH format stores one score per base pair, resulting in large file sizes for whole-genome analysis; consider compression (bedgraph.gz) or conversion to BigWig for storage efficiency.
- The Poisson model (qpois/ppois) assumes read counts follow a Poisson distribution; violations due to zero-inflation, overdispersion, or systematic biases may affect score calibration.
- Genome-wide background is calculated as a single constant; systematic regional biases (e.g., GC-content artifacts) are not accounted for and may reduce specificity in high-bias regions.

## Evidence

- [methods] Generate ChIP pileup BEDGRAPH by extending filtered ChIP reads to the predicted fragment length d using macs3 pileup with --extsize parameter.: "Generate ChIP pileup BEDGRAPH by extending filtered ChIP reads to the predicted fragment length d using macs3 pileup with --extsize parameter."
- [methods] Build local bias track from control by creating d, slocal (1kb), and llocal (10kb) background BEDGRAPH files using macs3 pileup with -B option and different --extsize values, then normalize slocal and llocal backgrounds using macs3 bdgopt with multiply mode and d/slocal and d/llocal scaling factors.: "Build local bias track from control by creating d, slocal (1kb), and llocal (10kb) background BEDGRAPH files using macs3 pileup with -B option and different --extsize values, then normalize slocal"
- [methods] Combine background tracks by computing maximum bias across d, slocal, and llocal using sequential macs3 bdgcmp -m max operations, then add genome-wide background value using macs3 bdgopt.: "Combine background tracks by computing maximum bias across d, slocal, and llocal using sequential macs3 bdgcmp -m max operations, then add genome-wide background value using macs3 bdgopt."
- [methods] Compare ChIP pileup against scaled local lambda using macs3 bdgcmp with -m qpois or -m ppois to generate q-value or p-value score BEDGRAPH files.: "Compare ChIP pileup against scaled local lambda using macs3 bdgcmp with -m qpois or -m ppois to generate q-value or p-value score BEDGRAPH files."
- [methods] using the `bdgcmp` module, which outputs a score for each base pair in the genome: "using the `bdgcmp` module, which outputs a score for each base pair in the genome"

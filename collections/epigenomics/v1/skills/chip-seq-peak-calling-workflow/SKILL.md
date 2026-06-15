---
name: chip-seq-peak-calling-workflow
description: Use when when you have aligned ChIP-Seq reads (single-end BED or paired-end BEDPE format) and need to identify enriched genomic regions by comparing ChIP signal against control background, with the ability to customize fragment length estimation, local bias calculation, and peak score thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3673
  tools:
  - macs3 filterdup
  - macs3 predictd
  - macs3 pileup
  - macs3 bdgcmp
  - macs3 bdgopt
  - macs3 bdgpeakcall
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

# chip-seq-peak-calling-workflow

## Summary

A complete ChIP-Seq peak calling workflow that decomposes MACS3 callpeak into sequential subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) to progressively transform aligned reads into peak calls with customizable statistical scoring and filtering.

## When to use

When you have aligned ChIP-Seq reads (single-end BED or paired-end BEDPE format) and need to identify enriched genomic regions by comparing ChIP signal against control background, with the ability to customize fragment length estimation, local bias calculation, and peak score thresholds rather than using the monolithic callpeak command.

## When NOT to use

- Input reads are already in a pre-processed or normalized format (e.g., pre-computed coverage tracks, counts per genomic bin) — the workflow requires raw aligned reads in BED/BEDPE format.
- You need to call broad peaks (e.g., for histone marks covering large domains) — use macs3 bdgbroadcall instead of bdgpeakcall, or apply a different workflow designed for broad mark analysis.
- You lack a suitable control/input sample — the workflow requires both ChIP and control samples to compute local bias; single-sample peak calling requires alternative statistical approaches.

## Inputs

- Aligned ChIP-Seq reads in BED format (single-end) or BEDPE format (paired-end)
- Aligned control/input reads in BED format (single-end) or BEDPE format (paired-end)
- Genome size in base pairs (for genome-wide background calculation)
- Sequencing read length (for gap parameter in peak calling)

## Outputs

- Filtered ChIP read count (integer)
- Filtered control read count (integer)
- Estimated fragment length d in base pairs (integer)
- ChIP pileup BEDGRAPH file (bedGraph format)
- Local bias BEDGRAPH file (bedGraph format, combined maximum of d/slocal/llocal backgrounds)
- Score BEDGRAPH file (bedGraph format, q-value or p-value scores per base pair)
- narrowPeak file (BED-like format with peak coordinates, summit positions, and score)

## How to apply

Begin by filtering duplicate reads from both ChIP and control samples using macs3 filterdup with --keep-dup=1 to record final read counts. Predict fragment length d from the ChIP sample using macs3 predictd (or skip for paired-end data where fragment extent is inherent). Generate ChIP pileup coverage by extending reads to fragment length d using macs3 pileup --extsize. Build local bias track from control by creating three background BEDGRAPH files at different scales (fragment length d, 1 kb slocal window, and 10 kb llocal window) using macs3 pileup -B, then normalize slocal and llocal relative to d using macs3 bdgopt in multiply mode. Combine backgrounds into maximum bias track using sequential macs3 bdgcmp -m max operations, add genome-wide background value (control_reads × d / genome_size), and scale to ChIP sequencing depth using macs3 bdgopt multiply with the ChIP-to-control read count ratio. Compare ChIP pileup against the scaled local lambda using macs3 bdgcmp -m qpois (or -m ppois) to generate score BEDGRAPH files. Finally, call narrow peaks using macs3 bdgpeakcall with score cutoff (e.g., -c 1.301 for q-value ≤ 0.05), minimum peak length -l equal to fragment length d, and gap parameter -g set to sequencing read length.

## Related tools

- **macs3 filterdup** (Remove duplicate reads from ChIP and control samples to record final read counts for normalization) — https://github.com/macs3-project/MACS
- **macs3 predictd** (Estimate average fragment length d from ChIP-Seq data (applied only to ChIP sample; skipped for paired-end reads)) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Generate coverage tracks by extending reads to fragment length d (ChIP pileup) and create background tracks at different scales (d, slocal, llocal) from control sample) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (Compare ChIP pileup against scaled local lambda using statistical models (qpois or ppois) to generate q-value or p-value score tracks; also used to combine background tracks using max operation) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalize and scale background tracks (multiply mode) and adjust scores for sequencing depth differences between ChIP and control) — https://github.com/macs3-project/MACS
- **macs3 bdgpeakcall** (Call narrow peaks from score BEDGRAPH by filtering regions above a user-defined cutoff, enforcing minimum peak length and gap constraints) — https://github.com/macs3-project/MACS

## Examples

```
macs3 filterdup -i CTCF_ChIP.bed -o CTCF_ChIP_filtered.bed --keep-dup=1 && macs3 predictd -i CTCF_ChIP_filtered.bed -g hs -m 5 50 && macs3 pileup -i CTCF_ChIP_filtered.bed -o CTCF_pileup.bedgraph --extsize 253 && macs3 bdgpeakcall -i CTCF_score.bedgraph -o CTCF_peaks.narrowPeak -c 1.301 -l 253 -g 50
```

## Evaluation signals

- Verify filterdup output: final ChIP and control read counts are positive integers and are less than or equal to input read counts (no reads are added, only removed).
- Verify predictd output: estimated fragment length d is a positive integer in a biologically plausible range (typically 100–300 bp for mammalian ChIP-Seq); for paired-end data, d should match the observed insert size distribution median.
- Verify pileup BEDGRAPH files: all three background tracks (d, slocal, llocal) have non-negative values; slocal and llocal normalized tracks reflect d/slocal and d/llocal scaling in their magnitudes.
- Verify combined bias track: maximum bias track contains non-negative values; genome background value is positive and approximately equal to (control_reads × d) / genome_size.
- Verify score BEDGRAPH output: all values are q-values (range [0, ~10]) or p-values (range [0, 1]) depending on the statistical model chosen; regions with high ChIP signal relative to background have higher scores.
- Verify narrowPeak output: peak coordinates span consecutive non-gap regions in the score track above the chosen cutoff; minimum peak length is ≥ d base pairs; summit position is within peak boundaries and has the maximum score in that peak.

## Limitations

- Fragment length estimation (predictd) assumes single-end reads and may be inaccurate if reads are short or ChIP enrichment is weak; paired-end mode bypasses this step but requires BEDPE input.
- Local bias calculation uses fixed windows (1 kb slocal, 10 kb llocal, fragment length d) and is sensitive to the control sample quality — low-quality or non-specific control samples can inflate background estimates and reduce peak sensitivity.
- Peak calling relies on a single score cutoff parameter (e.g., q-value ≤ 0.05); the optimal threshold is experiment-dependent and requires validation (e.g., overlap with motifs, independent replication).
- The workflow assumes a single ChIP condition and single control; complex experimental designs (e.g., multiple replicates, temporal dynamics) require extension or meta-analysis of individual peak calls.

## Evidence

- [other] The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp compares ChIP and control signals to compute p/q-value scores, bdgopt applies optimization to score tracks, and bdgpeakcall identifies peaks by filtering regions above a score cutoff.: "The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp"
- [methods] In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location: "In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location"
- [methods] This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data: "Decide the fragment length d ... This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data"
- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"
- [methods] To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model: "To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model"
- [methods] The final step in peak calling is to identify regions that surpass a specific score cutoff using the `bdgpeakcall` function: "The final step in peak calling is to identify regions that surpass a specific score cutoff using the `bdgpeakcall` function"
- [methods] The whole genome background is calculated using the formula: `number_of_control_reads * fragment_length / genome_size`: "The whole genome background is calculated using the formula: `number_of_control_reads * fragment_length / genome_size`"

---
name: local-background-bias-estimation
description: Use when you have paired ChIP and control BED/BEDPE files and need to account for local sequencing bias before peak calling. Use it specifically when control signal varies across genomic regions at multiple spatial scales (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 pileup
  - macs3 bdgopt
  - macs3 bdgcmp
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

# local-background-bias-estimation

## Summary

Construct a multi-scale local background noise track from control ChIP-Seq data by computing fragment-length (d), short-local (slocal, 1kb), and long-local (llocal, 10kb) pileups, normalizing each scale relative to fragment-length baseline, and combining them via maximum operation to capture spatially varying sequencing bias. This track is then scaled to match ChIP sequencing depth and used as the null hypothesis for peak enrichment testing.

## When to use

Apply this skill when you have paired ChIP and control BED/BEDPE files and need to account for local sequencing bias before peak calling. Use it specifically when control signal varies across genomic regions at multiple spatial scales (e.g., open chromatin bias at 1kb and 10kb windows differs from global background), or when simple global normalization would mask true enrichment in high-background regions.

## When NOT to use

- Input control file is already normalized or has been processed through another bias-correction pipeline; applying local-lambda estimation a second time risks double-correction.
- Sequencing depth is extremely low (< 1M reads in control) or extremely high (> 1B reads), making multi-scale window estimates unstable or memory-prohibitive.
- Analysis goal is to call broad peaks (histone marks with diffuse enrichment); use macs3 bdgbroadcall instead, which applies its own broad-scale background model.

## Inputs

- Filtered control BED file (after duplicate removal via macs3 filterdup)
- Predicted fragment length d (from macs3 predictd on ChIP sample)
- Control read count (final count after duplicate filtering)
- ChIP read count (final count after duplicate filtering)
- Genome size (in base pairs, e.g., 2.7 billion for human haploid)

## Outputs

- Local lambda BEDGRAPH file (scaled to ChIP sequencing depth)
- Intermediate d, slocal, llocal BEDGRAPH files (if retained for inspection)
- Combined maximum background BEDGRAPH (before depth scaling)

## How to apply

Generate three background BEDGRAPH files from the filtered control sample using macs3 pileup with the -B flag and three different --extsize values: (1) fragment length d, (2) slocal (default 1kb), and (3) llocal (default 10kb). Normalize slocal and llocal tracks by dividing each by the d track using macs3 bdgopt with multiply mode and scaling factors (d/slocal and d/llocal), which corrects for read-count differences at each scale. Combine normalized tracks by computing the element-wise maximum across all three using sequential macs3 bdgcmp -m max operations. Finally, add a genome-wide constant (control_reads × d / genome_size) to the combined track using macs3 bdgopt. Scale the resulting local lambda BEDGRAPH by the ratio of final ChIP to control read counts (macs3 bdgopt multiply) to match ChIP sequencing depth before comparison.

## Related tools

- **macs3 pileup** (Generate fragment-length-extended pileup BEDGRAPH tracks from control reads; invoked separately for d, slocal, and llocal windows using -B flag) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalize slocal and llocal by dividing by d track (multiply mode with scaling factors), and add genome-wide constant to combined track) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (Compute element-wise maximum across normalized background tracks using -m max operation) — https://github.com/macs3-project/MACS
- **macs3 filterdup** (Remove duplicate reads from control file prior to background estimation (prerequisite step)) — https://github.com/macs3-project/MACS

## Examples

```
macs3 pileup -i CTCF_Control_200K.bed -o control_d.bedgraph -B --extsize 147; macs3 pileup -i CTCF_Control_200K.bed -o control_slocal.bedgraph -B --extsize 1000; macs3 bdgcmp -t control_d.bedgraph -c control_slocal.bedgraph -m max -o control_lambda.bedgraph
```

## Evaluation signals

- All three background BEDGRAPH files (d, slocal, llocal) have identical genomic coverage (same coordinates and nonzero spans), differing only in signal magnitude.
- Normalized slocal and llocal tracks (after bdgopt division by d) have values typically in the range [0.5–2.0] if local bias is modest; extreme values (>5 or <0.1) indicate regional sequencing artifacts.
- Combined maximum BEDGRAPH shows smooth spatial variation; abrupt step changes suggest an error in bdgcmp -m max ordering or intermediate file corruption.
- Final scaled local lambda BEDGRAPH has non-zero signal genome-wide (due to genome-wide constant) and spatial scale matching slocal/llocal windows (visually, peaks and valleys span 1–10kb regions).
- When compared to ChIP pileup, local lambda track should be lower than ChIP in enriched regions (allowing positive log-ratio scores) and similar or higher in background regions (allowing near-zero or negative scores).

## Limitations

- Default window sizes (1kb and 10kb) are heuristic and not tuned for all mark types; heterochromatin or repeat-rich regions may require custom window parameters.
- Multi-scale approach assumes that bias is smooth and separable across scales; sharp local artifacts (e.g., PCR duplicates in a single 100bp window) are not captured by bdgopt normalization alone.
- Genome-wide background constant assumes uniform control sequencing depth; highly non-uniform coverage (e.g., from targeted enrichment or severe batch effects) can lead to over-correction in sparse regions.
- Scaling by read count ratio (ChIP/control) is sensitive to library size differences; if ChIP and control libraries differ by >5-fold or involve different sequencing platforms, consider quantile or spike-in normalization instead.

## Evidence

- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"
- [methods] To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function: "To create the background noise track, extend the control read to both sides using the `-B` option in the `pileup` function"
- [methods] Next, you can create a background noise track for the `slocal`bps local window, or a 1kb window by default: "Next, you can create a background noise track for the `slocal`bps local window, or a 1kb window by default"
- [methods] The background noise from a larger region can be generated similarly to the previous approach for the slocal background: "The background noise from a larger region can be generated similarly to the previous approach for the slocal background"
- [methods] The whole genome background is calculated using the formula: `number_of_control_reads * fragment_length / genome_size`: "The whole genome background is calculated using the formula: `number_of_control_reads * fragment_length / genome_size`"
- [methods] To compute the maximum bias for each genomic location, you can follow the default behavior of MACS3 `callpeak` or customize your pipeline: "To compute the maximum bias for each genomic location, you can follow the default behavior of MACS3 `callpeak` or customize your pipeline"
- [methods] To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth: "To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth"

---
name: narrow-peak-calling-score-threshold
description: Use when after generating a q-value bedgraph track from ChIP-Seq pileup versus local lambda comparison, and you need to identify statistically significant narrow peaks with defined boundaries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3673
  tools:
  - macs3 bdgpeakcall
  - macs3 bdgcmp
  - macs3 predictd
  - macs3 bdgbroadcall
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

# narrow-peak-calling-score-threshold

## Summary

Call narrow peaks from a q-value bedgraph track by applying a statistical significance cutoff and enforcing minimum peak length and gap constraints. This final step converts continuous score data into discrete peak regions for ChIP-Seq analysis.

## When to use

After generating a q-value bedgraph track from ChIP-Seq pileup versus local lambda comparison, and you need to identify statistically significant narrow peaks with defined boundaries. Apply this skill when your input is a bedgraph file of q-values (or p-values) and you want discrete narrowPeak format output with regions that exceed a user-specified significance threshold.

## When NOT to use

- Input is broad histone mark data (e.g., H3K27me3, H3K4me1) — use bdgbroadcall instead of bdgpeakcall
- Input bedgraph contains p-values not converted to -log10 scale — ensure proper transformation before applying cutoff
- Fragment length d is unavailable or unreliable (e.g., bimodal or very short ChIP library) — revisit macs3 predictd output or adjust d manually based on expected mark width

## Inputs

- bedgraph file of q-value scores (output from macs3 bdgcmp with -m qpois)
- predicted fragment length d (from macs3 predictd)
- significance threshold (q-value cutoff, typically 0.05)

## Outputs

- narrowPeak format file with peak coordinates, summit, and -log10(q-value) scores

## How to apply

Use macs3 bdgpeakcall to identify contiguous regions in the q-value track that exceed a cutoff threshold (converted from q-value to -log10 scale; e.g., q-value 0.05 = cutoff 1.301). Enforce a minimum peak length equal to the predicted fragment length d (e.g., 245 bp) to filter out spurious short fragments, and set a gap parameter to the read length (typically 100 bp) to merge peaks separated by small intervals. The function outputs narrowPeak format, which includes peak coordinates, summit position, and -log10(q-value) score for each called peak. Rationale: the fragment length constraint ensures peaks are wide enough to represent true ChIP enrichment, while the gap parameter prevents artificial fragmentation of continuous enriched regions.

## Related tools

- **macs3 bdgpeakcall** (identifies regions that surpass a specific score cutoff and calls narrow peaks with defined boundaries) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (upstream tool that generates the q-value bedgraph track by comparing ChIP pileup against local lambda using Poisson model) — https://github.com/macs3-project/MACS
- **macs3 predictd** (upstream tool that predicts fragment length d, a required parameter for bdgpeakcall minimum peak length) — https://github.com/macs3-project/MACS
- **macs3 bdgbroadcall** (alternative function for calling broad peaks instead of narrow peaks) — https://github.com/macs3-project/MACS

## Examples

```
macs3 bdgpeakcall -i ChIP_qvalue.bdg -c 1.301 -l 245 -g 100 -o narrow_peaks.narrowPeak
```

## Evaluation signals

- Output narrowPeak file is valid: coordinates are ordered, start < end, and all summits fall within peak intervals
- Peak length distribution matches expected minimum (fragment length d); all peaks ≥ minimum length constraint
- Q-value scores in output are monotonically non-decreasing within peaks and exceed cutoff threshold (e.g., ≥ 1.301 for q-value 0.05)
- Peak count is reasonable relative to input library size and known biology (typically 1,000–100,000 peaks for mammalian ChIP-Seq)
- Peaks overlap with known binding sites or motif-enriched regions when cross-validated against independent datasets

## Limitations

- Peak calling quality depends critically on accurate fragment length prediction; if macs3 predictd fails or returns bimodal estimates, manual adjustment may be needed
- Cutoff threshold is arbitrary and should be tuned to match downstream validation (e.g., motif recovery, overlap with independent replicates); no universal default applies to all mark types
- Narrow peak calling is designed for point-source marks (e.g., CTCF, transcription factors); broad marks (e.g., H3K27me3) require bdgbroadcall and different gap/length parameters
- Low-complexity or highly repetitive regions may produce spurious peaks due to control bias underestimation; filtering by local signal-to-noise ratio post-hoc is recommended

## Evidence

- [methods] identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling: "identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling"
- [other] Call narrow peaks from q-value track using macs3 bdgpeakcall with cutoff 1.301 (q-value 0.05 in -log10 format), minimum peak length 245 bp (fragment length d), and gap parameter 100 bp (read length), outputting narrowPeak format.: "Call narrow peaks from q-value track using macs3 bdgpeakcall with cutoff 1.301 (q-value 0.05 in -log10 format), minimum peak length 245 bp (fragment length d), and gap parameter 100 bp (read length),"
- [methods] Compare ChIP and local lambda to get the scores in pvalue or qvalue: "Compare ChIP and local lambda to get the scores in pvalue or qvalue"
- [methods] MACS3 does offer a range of subcommands that allow you to customize every step of your analysis: "MACS3 does offer a range of subcommands that allow you to customize every step of your analysis"

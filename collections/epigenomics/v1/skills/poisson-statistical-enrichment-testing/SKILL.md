---
name: poisson-statistical-enrichment-testing
description: Use when after extending ChIP sample reads to their predicted fragment length and constructing local lambda bias tracks (incorporating d-scaled, 1 kb, 10 kb, and genome-wide backgrounds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3673
  tools:
  - macs3 bdgcmp
  - macs3 pileup
  - macs3 bdgopt
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

# poisson-statistical-enrichment-testing

## Summary

Applies Poisson statistics to identify genomic regions where ChIP-Seq signal significantly exceeds local background noise, computing q-value scores at single-base-pair resolution to rank peaks by statistical confidence. This is a critical intermediate step in narrow peak calling that converts pileup coverage and local bias estimates into statistical significance measures.

## When to use

After extending ChIP sample reads to their predicted fragment length and constructing local lambda bias tracks (incorporating d-scaled, 1 kb, 10 kb, and genome-wide backgrounds). Apply this skill when you have aligned, deduplicated ChIP and control bedGraph pileup tracks and need to identify enriched regions by computing base-pair-level q-values before calling peak boundaries.

## When NOT to use

- Input ChIP or control files have not been deduplicated — run macs3 filterdup first
- Fragment length d has not been predicted or estimated — run macs3 predictd on ChIP data
- Local bias track has not been constructed or normalized to account for multiple scales (d, slocal, llocal, genome-wide)

## Inputs

- ChIP pileup bedGraph (coverage extended by predicted fragment length d)
- local lambda bedGraph (maximum bias track scaled by ChIP/control ratio)

## Outputs

- q-value bedGraph track (one q-value score per base pair)

## How to apply

Use macs3 bdgcmp with the -m qpois mode to compare the ChIP pileup coverage track against the scaled local lambda track (representing the expected background signal). This generates a q-value score for each genomic base pair using the Poisson model: q-values are computed as -log10(p-value) where the p-value reflects the probability of observing the ChIP count given the lambda (background) expectation. The local lambda is pre-computed by taking the maximum bias across d/2, 1 kb slocal, 10 kb llocal windows, and genome-wide backgrounds, then scaled by the ChIP-to-control sequencing depth ratio (e.g., 0.99858 in the CTCF example). The resulting bedGraph contains q-value scores suitable for thresholding (e.g., -log10(0.05) ≈ 1.301) in subsequent peak calling.

## Related tools

- **macs3 bdgcmp** (Compares ChIP pileup against local lambda using Poisson model (-m qpois) to generate base-pair-level q-value scores) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Pre-processing step to generate ChIP coverage track extended by fragment length d) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Pre-processing step to normalize and scale local bias components and construct final lambda track) — https://github.com/macs3-project/MACS

## Examples

```
macs3 bdgcmp -t ChIP_pileup.bedGraph -c local_lambda.bedGraph -m qpois -o qvalue.bedGraph
```

## Evaluation signals

- Output bedGraph contains exactly one q-value score per genomic position; no missing or NaN values in regions of interest
- Q-value distribution shows expected shape: low values (high enrichment) at peak summits, increasing values away from peaks
- Q-value range is compatible with downstream peak calling threshold (e.g., -log10(0.05) ≈ 1.301); verify cutoff is within observed q-value range
- Peaks called from q-value track using macs3 bdgpeakcall match published reference narrowPeak set for the same dataset (e.g., CTCF ENCODE peaks)
- Peaks with high q-values (strong enrichment) overlap known ChIP-binding motifs or published peak annotations; low q-value peaks fail validation

## Limitations

- Poisson model assumes read counts follow Poisson distribution; violations (overdispersion) can occur with low-complexity regions or repetitive sequences
- Local lambda computation depends on accurate fragment length prediction (d); errors in d propagate to q-value scoring
- Q-values are sensitive to sequencing depth and the magnitude of the ChIP-to-control scaling ratio; imbalanced library sizes can inflate false positives or negatives
- The method requires deduplicated input; high duplicate rates artificially reduce signal and inflate q-value thresholds

## Evidence

- [methods] Compare ChIP and local lambda to get the scores in pvalue or qvalue: "To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model"
- [methods] using the `bdgcmp` module, which outputs a score for each base pair in the genome: "using the `bdgcmp` module, which outputs a score for each base pair in the genome"
- [methods] Compare ChIP pileup against local lambda using macs3 bdgcmp with -m qpois to generate q-value scores for each base pair.: "Compare ChIP pileup against local lambda using macs3 bdgcmp with -m qpois to generate q-value scores for each base pair."
- [methods] Scale combined background by ChIP-to-control ratio (0.99858) using macs3 bdgopt multiply to create local lambda track.: "Scale combined background by ChIP-to-control ratio (0.99858) using macs3 bdgopt multiply to create local lambda track."
- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"

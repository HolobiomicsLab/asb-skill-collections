---
name: poisson-test-statistical-scoring
description: Use when after generating ChIP pileup and local lambda (background) BEDGRAPH tracks with matched sequencing depth, use this skill to assign statistical significance scores to each genomic region.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3179
  tools:
  - macs3 bdgcmp
  - macs3 pileup
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

# Poisson Test Statistical Scoring

## Summary

Apply Poisson or quasi-Poisson statistical models to compare ChIP-Seq signal against local background noise, generating p-value or q-value scores for each genomic position. This skill transforms raw coverage comparisons into statistical significance estimates suitable for peak calling.

## When to use

After generating ChIP pileup and local lambda (background) BEDGRAPH tracks with matched sequencing depth, use this skill to assign statistical significance scores to each genomic region. Specifically, when you have comparable ChIP and control coverage tracks and need to identify enriched regions above baseline noise — typical in narrow peak calling workflows where a single comparison model (qpois or ppois) must be applied genome-wide.

## When NOT to use

- Input backgrounds are not normalized to the same sequencing depth as ChIP — local lambda must be scaled by the ratio (final_ChIP_reads / control_reads) before comparison.
- ChIP and control samples have vastly different library sizes without depth normalization; the statistical model assumes comparable sequencing effort.
- Local background was not properly constructed from d, slocal (1kb), and llocal (10kb) windows; misspecified background invalidates the significance test.

## Inputs

- ChIP pileup BEDGRAPH (coverage track extended to fragment length d)
- Local lambda background BEDGRAPH (scaled to ChIP sequencing depth, combining d/slocal/llocal maximum with genome background)

## Outputs

- q-value BEDGRAPH (log10-transformed quasi-Poisson scores, base-pair resolution)
- p-value BEDGRAPH (log10-transformed Poisson scores, base-pair resolution)

## How to apply

Use macs3 bdgcmp with the -m qpois flag to apply a quasi-Poisson test comparing ChIP pileup BEDGRAPH against the scaled local lambda background BEDGRAPH. The quasi-Poisson model accounts for overdispersion in read counts and outputs a q-value BEDGRAPH; alternatively, use -m ppois for p-value scoring if Poisson assumptions hold more strictly. The resulting score track contains log10-transformed statistical significance at base-pair resolution. Choose qpois (default, more robust) when read count variance exceeds the mean; choose ppois when variance equals mean. The output BEDGRAPH is then thresholded using macs3 bdgpeakcall with a cutoff (e.g., -c 1.301 for q-value ≤ 0.05) to call peaks.

## Related tools

- **macs3 bdgcmp** (Compares ChIP pileup against scaled local lambda using quasi-Poisson or Poisson models to compute p/q-value scores) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Generates ChIP and control coverage BEDGRAPH tracks that serve as input to bdgcmp) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Scales and combines background tracks before statistical comparison) — https://github.com/macs3-project/MACS
- **macs3 bdgpeakcall** (Thresholds the output score BEDGRAPH using the cutoff value derived from the q-value or p-value distribution) — https://github.com/macs3-project/MACS

## Examples

```
macs3 bdgcmp -t CTCF_ChIP.pileup.bedg -c CTCF_lambda.bedg -m qpois -o CTCF_qvalue.bedg
```

## Evaluation signals

- Output BEDGRAPH has contiguous genomic intervals with valid log10-transformed scores (positive values = enrichment above background, negative = depletion)
- Score values are monotonic with sequencing depth: doubling ChIP reads increases scores; doubling control reads decreases scores proportionally
- Peak calls derived from q-value scores at cutoff -c 1.301 (q ≤ 0.05) recover known binding sites or match expected ChIP peak count for the transcription factor
- Regions with high ChIP signal but high local background receive lower scores than regions with identical ChIP signal but lower background, confirming that statistical significance accounts for noise
- Score BEDGRAPH has no gaps or negative intervals; every genomic position has a score value (including low-signal regions scoring near 0)

## Limitations

- Quasi-Poisson and Poisson models assume reads are independently and identically distributed; violations (e.g., PCR bias, mappability bias) inflate false positives.
- The model is sensitive to the correctness of the local lambda background: miscalculation of d, slocal, or llocal components directly propagates into inflated or deflated significance scores.
- q-value cutoff (e.g., 1.301 for q ≤ 0.05) is not self-adaptive to different peak widths or signal-to-noise ratios; narrow and broad peaks may require different thresholds.
- Genome-wide background is a scalar (control_reads × fragment_length / genome_size) and does not account for regional GC content or copy-number variation.

## Evidence

- [methods] using the `bdgcmp` module, which outputs a score for each base pair in the genome: "using the `bdgcmp` module, which outputs a score for each base pair in the genome"
- [methods] Compare ChIP pileup against scaled local lambda using macs3 bdgcmp with -m qpois or -m ppois to generate q-value or p-value score BEDGRAPH files.: "Compare ChIP pileup against scaled local lambda using macs3 bdgcmp with -m qpois or -m ppois to generate q-value or p-value score BEDGRAPH files."
- [methods] To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model: "To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model"
- [methods] Scale local lambda bias to ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts.: "Scale local lambda bias to ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts."
- [methods] identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling: "identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling"

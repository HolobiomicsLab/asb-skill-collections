---
name: pearson-correlation-computation-across-tools
description: Use when you have quantification results from two or more independent implementations, versions, or variants of the same analysis tool (e.g. C++ salmon 1.11.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0080
  tools:
  - pufferfish
  - piscem-rs
  - minimap2
  - salmon
  - R or Python statistical libraries (e.g., scipy.stats.pearsonr, cor.test in R)
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- pufferfish's SSHash k-mer lookup, now fixed upstream
- The Rust port (built on piscem-rs, which derives orientation correctly)
- The Rust port (built on piscem-rs, which derives orientation correctly) was right all along
- minimap2 (full SW) on these reads gives near-identical quality profiles in both directions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_salmon
    doi: 10.1038/nmeth.4197
    title: salmon
  dedup_kept_from: coll_salmon
schema_version: 0.2.0
---

# Pearson-correlation computation across tools

## Summary

Compute Pearson correlation coefficients on quantitative outputs (e.g. transcript abundance estimates, read counts) from independent implementations or versions of the same tool to validate technical equivalence and detect algorithmic divergence. This skill is essential for validating that a port (e.g. Rust rewrite) or bug fix produces numerically equivalent results to a reference implementation.

## When to use

Apply this skill when you have quantification results from two or more independent implementations, versions, or variants of the same analysis tool (e.g. C++ salmon 1.11.4 pre-fix vs. post-fix, or C++ salmon vs. Rust salmon port) and need to assess whether they produce equivalent abundance estimates or mapping metrics. Trigger on: (1) release of a major rewrite or language port, (2) application of a known bug fix to one version, (3) need to validate equivalence before deprecating a legacy implementation, or (4) comparing outputs across different parameter configurations on the same input dataset.

## When NOT to use

- Input is quantification from different tools entirely (e.g., salmon vs. kallisto vs. RSEM), rather than versions/variants of the same tool — use inter-tool benchmark comparisons instead
- Quantification results come from different input datasets (different reads or references); Pearson correlation requires identical inputs to isolate tool differences
- The goal is to detect biological signal or differential expression, not validate tool equivalence — high correlation does not indicate correct abundance estimates, only consistency

## Inputs

- quant.sf output files (tab-delimited quantification tables with Name, Length, EffectiveLength, TPM, NumReads columns) from two or more tool implementations/versions, run on identical input reads and reference transcripts
- SAM/BAM alignment output (writeMappings from salmon quant -z) from each implementation, if read-level validation is required

## Outputs

- Pearson correlation coefficient (scalar, range [−1, 1]) for each quantitative column (e.g., NumReads Pearson, EffectiveLength Pearson)
- Per-read mapping agreement percentage (e.g., 99.83% of reads mapped to same or no transcript across implementations)
- Mapping rate comparison (e.g., 85.55% for both implementations, differing by ≤1 read)
- Cross-check table of differentially mapped reads with strand and locus agreement confirmation

## How to apply

Extract quantitative columns (e.g., NumReads, EffectiveLength) from the quant.sf output files produced by each tool/version on identical inputs (same reads, same reference, same parameters). Align the rows by transcript identifier and compute Pearson correlation coefficient for each column pair. A correlation ≥ 0.998 indicates near-perfect agreement; values <0.99 warrant investigation of per-transcript or per-read disagreement. Cross-check differentially mapped reads (e.g., those identified as mapped in one version but not the other) using SAM writeMappings output to confirm whether strand orientation or locus placement agrees. Report mapping rate (percentage of reads mapped) as a coarse-grained agreement metric; discrepancies in mapping rate combined with high Pearson correlation (0.99+) suggest systematic mapping decisions (e.g. chain pruning thresholds) rather than stochastic noise.

## Related tools

- **salmon** (Quantification tool; run as C++ (salmon 1.11.4, pre-fix and post-fix versions) and Rust port (salmon 2.0) on identical input reads and reference to generate quant.sf tables for correlation comparison) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (K-mer lookup and indexing component; bug fix (commit 5dce7f4) in SSHash streaming orientation is the algorithmic source of pre/post-fix divergence being quantified)
- **R or Python statistical libraries (e.g., scipy.stats.pearsonr, cor.test in R)** (Compute Pearson correlation coefficients on aligned quant.sf columns and generate comparison tables)

## Examples

```
# Extract NumReads and EffectiveLength from two quant.sf files, compute Pearson correlation:
Rscript -e "d1 <- read.table('salmon_cpp_post_fix/quant.sf', header=T); d2 <- read.table('salmon_rust/quant.sf', header=T); cat('NumReads Pearson:', cor(d1\$NumReads, d2\$NumReads), '\n'); cat('EffectiveLength Pearson:', cor(d1\$EffectiveLength, d2\$EffectiveLength), '\n')"
```

## Evaluation signals

- Pearson correlation coefficient ≥ 0.998 for NumReads and EffectiveLength columns indicates near-perfect quantitative agreement; values <0.99 warrant per-transcript investigation
- Mapping rate (percentage of reads mapped) matches to within 1 read across implementations (e.g., 85.55% for both C++ post-fix and Rust); discrepancies >0.1% suggest algorithmic drift
- Per-read mapping agreement ≥ 99.8% (e.g., 99.83% of reads assigned to same or no transcript); lower values indicate systematic orientation, locus, or filtering differences
- SAM/BAM cross-check confirms strand and locus agreement for reads identified as differentially mapped; mismatches indicate bugs rather than benign parameter tuning
- Reproducibility: re-running both implementations on the same reads/reference with fixed random seed should yield identical or near-identical Pearson correlations (within floating-point precision)

## Limitations

- Pearson correlation is insensitive to systematic biases (e.g., if one version consistently overestimates NumReads by 5%, Pearson may still be >0.99); examine raw differences or fold-change distributions for bias detection
- Correlation threshold (0.998 vs. 0.999) is heuristic; biological applications may tolerate lower agreement (e.g., 0.95) than validation of a bug fix (where 0.9999 is expected)
- Small transcripts or low-abundance genes have fewer reads and higher sampling variance, reducing per-transcript correlation; aggregate by abundance quartile to stabilize estimates
- Floating-point precision differences across implementations (C++ vs. Rust, different compilers, SIMD variants) can produce minor Pearson divergence (e.g., 0.999854 vs. 0.999855) even with identical algorithms; do not over-interpret sub-0.0001 differences
- The skill detects equivalence but not correctness; high correlation does not validate that either implementation produces the ground truth, only that they agree with each other

## Evidence

- [methods] Finding: After pufferfish fix, C++ salmon maps 85.55% vs Rust port 85.55%, matching within 1 read: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] Finding: NumReads Pearson correlation is 0.99854 between C++ and Rust on byte-identical index: "NumReads Pearson | 0.99854"
- [methods] Finding: Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index: "per-read mapping agreement | 99.83%"
- [methods] Workflow step: Extract mapping rates from output and compute correlation coefficients on quant.sf files: "Extract mapping rates (percentage of reads mapped) from each run's output. 7. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using"
- [methods] Validation step: Cross-check differentially mapped reads using SAM output to confirm strand and locus agreement: "Cross-check placement of reads identified as differentially mapped (e.g., ERR458493.850) using writeMappings SAM output to confirm strand and locus agreement."
- [readme] README statement on Rust rewrite equivalence: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"

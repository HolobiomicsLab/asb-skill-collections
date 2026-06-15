---
name: per-read-mapping-agreement-assessment
description: Use when comparing mapping outputs from two different salmon versions or implementations (e.g., C++ 1.12.0 vs. Rust 2.0) to determine if observed differences in total mapped read counts are due to true algorithmic bugs, parameter defaults, or index format changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - minimap2
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- minimap2 (full SW) on these reads gives near-identical quality profiles in both directions
- The Rust port (built on piscem-rs, which derives orientation correctly)
- The Rust port (built on piscem-rs, which derives orientation correctly) was right all along
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

# per-read-mapping-agreement-assessment

## Summary

Quantify read-by-read concordance between two salmon mapping implementations (or versions) by comparing which reads each mapper assigns to the transcriptome, identifying systematic differences in mapping behavior due to algorithmic or parameter choices. This skill detects whether mapping discrepancies arise from fundamental orientation/correctness bugs versus tunable pruning thresholds.

## When to use

Apply this skill when comparing mapping outputs from two different salmon versions or implementations (e.g., C++ 1.12.0 vs. Rust 2.0) to determine if observed differences in total mapped read counts are due to true algorithmic bugs, parameter defaults, or index format changes. Specifically useful when one version maps significantly more reads than another and you need to partition the gap into root causes before deciding whether to retune parameters or escalate as a correctness issue.

## When NOT to use

- Input comes from different reference transcriptomes or significantly different k-mer lengths (byte-identity requirement violated).
- You are comparing biological replicates or samples with expected natural variation; this skill targets technical/algorithmic concordance, not biological agreement.
- The two mappers were run with intentionally different parameters as a feature comparison; use this skill only when parameters are held constant to isolate algorithmic differences.

## Inputs

- FASTQ/FASTQ.gz read file (paired-end or single-end, e.g., GEUVADIS ERR188044: 36.35M 76bp paired-end reads)
- byte-identical salmon index (same reference transcriptome, k-mer length, deterministic N-replacement; e.g., 193,759 transcripts, k=31)
- quant.sf output from mapper version A (C++ salmon 1.12.0)
- quant.sf output from mapper version B (Rust salmon 2.0 or other variant)

## Outputs

- per-read agreement percentage (e.g., 99.83%)
- cross-tabulation table: reads mapped by both, mapped by A only, mapped by B only, unmapped by both (e.g., 62,812 mapped by Rust only; 154 mapped by C++ only)
- NumReads Pearson correlation coefficient (e.g., 0.99854)
- minimap2 validation classification of boundary-case reads (strong/weak/unaligned)
- quantified attribution of the mapping-count gap to root causes (e.g., ~80% attributable to orphanChainSubThresh/postMergeChainSubThresh default difference)

## How to apply

Run both implementations on a byte-identical transcriptome index with identical selective-alignment parameters (e.g., -l A, no bias correction). Extract per-read mapping decisions (mapped vs. unmapped, target assignment) from each run's output. Compute a cross-tabulation: reads mapped by both, mapped by version A only, mapped by version B only, unmapped by both. Express agreement as the percentage of reads with identical mapping status across both versions. For boundary-case reads (mapped by one version only), perform independent full-strength validation (e.g., minimap2 Smith-Waterman re-alignment) to classify whether the mapped read is likely correct, weak, or a false positive. Use Pearson correlation on abundance counts (NumReads) and per-read agreement thresholds (e.g., ≥99.8%) to assess quantitative concordance. This partitions the total gap into explainable causes: k-mer lookup bugs (should show asymmetric true/false positives), parameter defaults (should show systematic orphan/post-merge pruning effects), or index format issues.

## Related tools

- **salmon 2.0** (Rust re-implementation of salmon; one of the two mappers being compared for per-read agreement) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0** (C++ reference implementation; the baseline mapper for comparison against Rust port) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **minimap2** (Independent full Smith-Waterman aligner used to validate boundary-case reads (mapped by one version only) and classify them as true/weak/false positives)
- **piscem-rs** (Underlying Rust mapping engine used by salmon 2.0; encodes k-mer orientation logic that may differ from C++ pufferfish) — https://github.com/COMBINE-lab/salmon

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -o quant_v2 -p 16 ; compare quant_v2/quant.sf with baseline C++ 1.12.0 quant.sf via cross-tabulation and compute per-read agreement ≥99.8% and NumReads Pearson ≥0.998
```

## Evaluation signals

- Per-read mapping agreement ≥99.8% (as reported: 99.83% on byte-identical index indicates negligible algorithmic difference)
- NumReads Pearson correlation coefficient ≥0.998 (reported: 0.99854 validates abundance quantification concordance)
- Residual cross-discrepancy (reads mapped by A only + reads mapped by B only) reduces to <20,000 reads after parameter tuning from initial ~63,000 (indicates parameters, not bugs, explain most of the gap)
- Minimap2 Smith-Waterman validation of boundary-case reads shows asymmetry ratio consistent with the stated root cause (e.g., if orphan pruning is the culprit, C++-only unmapped reads should predominantly be short/weak chains)
- Mapping-count gap is attributable to a single, named parameter difference (e.g., ~80% explained by orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 in C++ vs. different defaults in Rust)

## Limitations

- Requires a byte-identical reference index; if indices differ in format, construction parameters, or N-replacement strategy, observed disagreement may conflate index vs. mapper bugs.
- Per-read agreement can be high (>99%) even when a small number of high-abundance transcripts have systematic assignment errors; use NumReads correlation and downstream abundance-level validation to catch this.
- minimap2 re-alignment on boundary reads is computationally expensive for large datasets (36M+ reads); sampling or downsampling may be necessary for triage.
- Per-read agreement alone does not reveal whether mapped reads are correct in terms of abundance; validation against ground-truth (spike-ins, qPCR, or independent methods) is needed for biological validation.

## Evidence

- [methods] per-read mapping agreement | 99.83%: "Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index"
- [methods] NumReads Pearson correlation coefficient: "On byte-identical index, NumReads Pearson correlation is 0.99854 between C++ and Rust"
- [methods] cross-tabulation of mapped reads: "Rust maps 62,812 reads C++ leaves fully unmapped; C++ maps only 154 Rust doesn't"
- [methods] orphan and post-merge chain pruning threshold defaults: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ="
- [methods] byte-identical index requirement: "Obtain byte-identical reference index built from clean.fa (193,759 transcripts) using salmon 2.0 with k=31, deterministic N-replacement"
- [methods] minimap2 validation workflow: "minimap2 (full SW) on these reads gives near-identical quality profiles in both directions"
- [methods] mapping agreement threshold for validation: "per-read mapping agreement ≥99.8%"

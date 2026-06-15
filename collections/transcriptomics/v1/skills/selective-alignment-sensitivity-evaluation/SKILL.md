---
name: selective-alignment-sensitivity-evaluation
description: Use when when comparing mapping outputs between two selective-alignment implementations (e.g., C++ vs. Rust port) on byte-identical reference indices and observing a multi-percentage-point gap in mapping rate or read assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3673
  tools:
  - minimap2
  - piscem-rs
  - salmon
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

# selective-alignment-sensitivity-evaluation

## Summary

Systematically evaluate how chain-pruning threshold parameters (orphanChainSubThresh, postMergeChainSubThresh) in selective alignment affect read mapping rates and per-read mapping agreement between implementations. This skill isolates the contribution of chain-score defaults to observed mapping discrepancies on real RNA-seq data.

## When to use

When comparing mapping outputs between two selective-alignment implementations (e.g., C++ vs. Rust port) on byte-identical reference indices and observing a multi-percentage-point gap in mapping rate or read assignments. Use this skill to determine whether the gap is attributable to differences in chain pruning thresholds rather than algorithmic correctness or index quality.

## When NOT to use

- Input implementations differ in reference index format or construction parameters—ensure byte-identical indices first
- Observed mapping gap is <1% or within acceptable tolerance for the analysis goal; sensitivity evaluation is unnecessary if implementations already agree within acceptable bounds
- One or both implementations lack explicit control over chain-pruning thresholds or do not document their default values

## Inputs

- byte-identical reference index built from transcriptome FASTA (e.g., 193,759 transcripts, k=31)
- paired-end RNA-seq reads in FASTQ or compressed format (e.g., GEUVADIS ERR188044: 76 bp, 36.35M reads)
- baseline mapping rate from reference implementation (e.g., 92.011% from C++ salmon 1.12.0)
- selective alignment parameters (default chain-pruning thresholds from reference)

## Outputs

- mapping rate (%) for test implementation with reference thresholds applied
- per-read mapping agreement (%) between reference and test implementation
- NumReads Pearson correlation coefficient between implementations
- count of reads mapped exclusively by test implementation vs. reference only
- quantification of chain-pruning contribution to mapping gap (as % of total gap)

## How to apply

Obtain or construct a byte-identical reference index (e.g., from clean.fa, 193,759 transcripts, k=31, deterministic N-replacement) using both implementations. Quantify the baseline mapping rate on real paired-end short reads (e.g., GEUVADIS ERR188044, 76 bp, 36.35M reads) using the reference implementation's default selective alignment settings. Then re-run the test implementation with the reference's chain-pruning thresholds explicitly set (e.g., --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9) and measure the resulting mapping rate, per-read mapping agreement, and NumReads Pearson correlation. Compute the reduction in per-read disagreement (reads mapped by test only vs. by reference only) and express it as a percentage of the original gap. If mapping rate improves to within the target tolerance (e.g., ≥92.03% when baseline is 92.011%) and per-read agreement exceeds a threshold (e.g., ≥99.8%), conclude that chain-sub-optimality accounts for the primary discrepancy.

## Related tools

- **salmon** (Reference and test implementation for selective-alignment quantification; both C++ 1.12.0 (baseline) and Rust 2.0 port support explicit chain-pruning threshold parameters) — https://github.com/COMBINE-lab/salmon
- **minimap2** (Full Smith-Waterman re-alignment of boundary-case reads (reads with disagreement between implementations) to classify as strong/weak/unaligned and assess whether disagreement reflects true alignment ambiguity)
- **piscem-rs** (Underlying mapper for Rust port; correct k-mer orientation enables accurate selective alignment evaluation)

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -p 16 -o test_quant
```

## Evaluation signals

- Mapping rate of test implementation with reference thresholds applied must be ≥92.03% (within 0.02% of C++ 1.12.0 baseline of 92.011%), indicating threshold adjustment eliminates most of the gap
- Per-read mapping agreement between implementations must reach ≥99.8%, confirming that the vast majority of individual read assignments are identical after threshold alignment
- Residual per-read disagreement (sum of reads mapped by test only + reads mapped by reference only) must drop from ~62,966 to <20,000, demonstrating that chain-pruning accounts for ~80% of the original discrepancy
- NumReads Pearson correlation must exceed 0.998, indicating strong agreement in transcript abundance estimates after threshold correction
- Minimap2 full Smith-Waterman re-alignment of boundary-case reads should reveal that disagreements are symmetric (test maps as many C++-only reads as C++ maps test-only reads), confirming threshold difference rather than algorithmic asymmetry

## Limitations

- This skill assumes both implementations share the same underlying k-mer lookup, MEM extraction, and alignment scoring logic; if they differ in those components, chain-pruning threshold adjustment alone will not fully explain the mapping gap
- Evaluation is specific to selective alignment mode; sketch-mode quantification (--sketch flag) uses a different pipeline and does not employ chain pruning, so this skill does not apply
- Residual disagreement after threshold adjustment may be attributed to other sources (k-mer-orientation bugs in upstream libraries, poly-A clipping differences, read-trimming policies); this skill isolates chain-pruning contribution only
- The evaluation depends on availability of reference implementation's default threshold values; if not documented, threshold discovery requires reverse-engineering or access to source code

## Evidence

- [other] C++ salmon uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 for chain pruning before alignment, accounting for approximately 80% (~49k reads) of the observed mapping count gap between C++ 1.12.0 and the Rust port: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ="
- [methods] On byte-identical index constructed from clean.fa with 193,759 transcripts using salmon 2.0 (k=31, deterministic N-replacement), per-read mapping agreement between C++ 1.12.0 and Rust is 99.83%: "per-read mapping agreement | 99.83%"
- [methods] Baseline mapping rate for C++ salmon 1.12.0 on GEUVADIS ERR188044 (36.35M 76bp paired-end reads) is 92.011% (33,446,029 mapped reads): "Rust mapping rate must be ≥92.03% (within 0.02% of C++ 1.12.0 baseline (92.011%, 33,446,029 mapped reads))"
- [other] After applying reference thresholds, residual per-read disagreement (Rust-only + C++-only) must drop from 62,966 to <20,000 reads: "residual per-read disagreement (Rust-only + C++-only) must drop from 62,966 to <20,000 reads"
- [methods] On real short reads, a k-mer-orientation bug in pufferfish's SSHash streaming lookup was identified and fixed, demonstrating that threshold evaluation must account for upstream algorithmic correctness: "That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] Minimap2 full Smith-Waterman alignment is used to classify boundary-case reads as strong/weak/unaligned and assess symmetry of disagreement: "minimap2 full Smith-Waterman re-alignment of boundary-case reads to classify as strong/weak/unaligned"

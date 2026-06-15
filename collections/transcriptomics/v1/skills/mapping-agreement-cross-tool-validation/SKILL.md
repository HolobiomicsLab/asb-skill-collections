---
name: mapping-agreement-cross-tool-validation
description: Use when when you have built a new tool implementation or major version and need to verify it produces equivalent results to a reference implementation on the same input data and index.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - piscem-rs
  - salmon 2.0 (Rust)
  - salmon 1.12.0 (C++)
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
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

# mapping-agreement-cross-tool-validation

## Summary

Quantify per-read and per-transcript agreement between two transcript-quantification tools (e.g., salmon versions or implementations) to assess consistency and expose algorithmic differences. This skill validates that a reimplementation or alternative tool produces equivalent quantification outputs within acceptable tolerance.

## When to use

When you have built a new tool implementation or major version and need to verify it produces equivalent results to a reference implementation on the same input data and index. Specifically: when two versions claim to use the same algorithm (selective alignment, chaining, MEM extraction) but differ in language/rewrite, and you need to quantify the magnitude of discrepancy and trace which algorithmic steps account for residual differences.

## When NOT to use

- Input indices are not byte-identical or were built with different parameters (k-mer length, decoy handling); index differences will confound tool-implementation differences.
- Tools are being run with different quantification parameters (e.g., one with bias correction, one without; different library-type inference); compare only under matched parameter sets.
- You are comparing tools on different datasets or read lengths; per-read and per-transcript agreement are dataset-dependent and cannot be generalized across experiments.

## Inputs

- byte-identical transcriptome index (same FASTA, same k-mer length, deterministic non-ACGT replacement)
- paired-end RNA-seq reads in FASTQ or gzip format
- quant.sf output files from both tools
- unmapped_names.txt files (per-read mapping status) from both tools

## Outputs

- Pearson correlation coefficient for NumReads per transcript
- Pearson correlation coefficient for TPM per transcript
- per-read mapping agreement percentage (% reads both tools agree are mapped or unmapped)
- total assigned NumReads difference as percentage
- breakdown of mapping discrepancies by category (fully unmapped, partially mapped)

## How to apply

Build a byte-identical reference index and run both tools on the same sequencing dataset (e.g., ERR188044, 36.35M paired-end reads) using identical parameters (e.g., selective-alignment mode, `-l A` auto-detect library type, no bias correction). Extract per-transcript quantification columns (NumReads, TPM) from both tools' quant.sf outputs and compute Pearson correlations. For per-read mapping agreement, parse unmapped_names.txt files from both runs and count reads on which both tools agree in mapping status (mapped vs. fully unmapped, coded 'u'). Report total assigned reads difference as a percentage. When residual disagreement exists (~0.15% per-read mapping disagreement), identify the source by comparing parameter defaults (e.g., orphanChainSubThresh, postMergeChainSubThresh chain-pruning thresholds) and trace whether the difference is algorithmic or parametric. Strong agreement (Pearson > 0.998, per-read agreement > 99.8%) indicates the implementations are functionally equivalent despite language differences.

## Related tools

- **salmon 2.0 (Rust)** (primary implementation to validate (generates quant.sf and unmapped_names.txt)) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (reference implementation for cross-tool comparison) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **piscem-rs** (underlying mapper in Rust port; exposes orientation behavior in k-mer lookup) — https://github.com/COMBINE-lab/salmon

## Examples

```
salmon index -t GRCh38_cDNA.fa -i idx_salmon2 -k 31 && salmon index -t GRCh38_cDNA.fa -i idx_salmon112 -k 31 && salmon quant -i idx_salmon2 -l A -1 ERR188044_R1.fastq.gz -2 ERR188044_R2.fastq.gz -o quant_rust --no-bias-seq-bias && salmon quant -i idx_salmon112 -l A -1 ERR188044_R1.fastq.gz -2 ERR188044_R2.fastq.gz -o quant_cpp112 --no-bias-seq-bias && paste <(cut -f1,4,5 quant_rust/quant.sf) <(cut -f4,5 quant_cpp112/quant.sf) | Rscript -e 'x <- read.table(stdin()); cor(x[,2],x[,4]); cor(x[,3],x[,5])'
```

## Evaluation signals

- Per-transcript Pearson correlation for NumReads ≥ 0.9985 indicates high quantitative agreement across thousands of transcripts.
- Per-transcript Pearson correlation for TPM ≥ 0.9989 (higher due to normalization reducing noise) indicates abundance ranking is consistent.
- Per-read mapping agreement ≥ 99.8% (i.e., ≤0.2% reads where tools disagree on mapped vs. unmapped status) indicates low residual algorithmic difference.
- Total assigned NumReads difference < 1% indicates tools assign nearly identical total read mass across the transcriptome.
- When disagreement exists, mapping-gap analysis (e.g., '62,812 reads Rust maps but C++ leaves unmapped') can be traced to specific parameter defaults (chain-pruning thresholds account for ~80% of the difference) rather than core algorithmic divergence.

## Limitations

- Per-read and per-transcript agreement are sensitive to minor parameter differences (orphanChainSubThresh, postMergeChainSubThresh); identical algorithm with different defaults will show measurable disagreement (up to ~0.2% per-read in this case).
- Correlation metrics alone (Pearson > 0.998) do not reveal systematic bias or directional differences; residual disagreement must be traced by inspecting specific reads and chains to distinguish algorithmic bugs from intentional parameter tuning.
- Index byte-identity is required; any mismatch in k-mer extraction, decoy handling, or bloom-filter configuration will confound the tool comparison and make it impossible to isolate implementation effects.
- This skill validates quantification consistency but does not assess downstream inference (EM, VBEM) convergence or posterior variance; abundance point estimates may agree while credible intervals diverge.

## Evidence

- [methods] Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index: "per-read mapping agreement | 99.83%"
- [methods] On byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM: "On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%."
- [methods] ~80% of mapping gap is attributable to chain-pruning-threshold defaults, not algorithmic divergence: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ="
- [methods] Workflow specifies byte-identical index construction and paired parameter control: "Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement (193,759 transcripts). 2. Run salmon 2.0 quant"
- [readme] salmon 2.0 is a Rust rewrite and must be validated against C++ reference: "This is salmon 2.0 — a from-scratch Rust rewrite of salmon. It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read, but it is a"

---
name: paired-end-read-quantification
description: Use when you have paired-end RNA-seq reads (FASTQ) and a reference transcriptome (FASTA), and you need to estimate transcript-level expression (NumReads and TPM).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0654
  tools:
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0 (C++ version)
  - pufferfish
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

# paired-end-read-quantification

## Summary

Quantify transcript abundances from paired-end RNA-seq reads using selective alignment and statistical inference over equivalence classes. This skill combines fast k-mer-based mapping with EM/VBEM to produce per-transcript NumReads and TPM estimates.

## When to use

You have paired-end RNA-seq reads (FASTQ) and a reference transcriptome (FASTA), and you need to estimate transcript-level expression (NumReads and TPM). Apply this when the goal is rapid, bias-aware quantification without building a genome BAM or when you want to leverage selective alignment's chain-based mapping and decoy-aware filtering to reduce spurious transcript assignment.

## When NOT to use

- Input is already a BAM or SAM alignment file — use `salmon quant -a/--alignments` instead.
- You need single-cell quantification — use alevin-fry or piscem with RAD output instead.
- You require posterior-sampled BAM output with per-read quantification uncertainty — this feature is not yet implemented in salmon 2.0.

## Inputs

- paired-end FASTQ reads (gzip-compressed or uncompressed)
- transcriptome FASTA file
- salmon index directory (pre-built from transcriptome)

## Outputs

- quant.sf file (per-transcript NumReads and TPM estimates)
- logs and mapping statistics
- unmapped_names.txt (fully-unmapped reads, optional)

## How to apply

First, build a reusable index from the transcriptome FASTA using salmon index with a chosen k-mer length (default k=31) and optional decoy sequences. Then run salmon quant in selective-alignment mode (the default) on paired-end reads, specifying library type (use `-l A` for auto-detection) and output directory. Selective alignment performs k-mer seeding via pufferfish SSHash lookup, extracts MEMs, chains matches, optionally clips poly-A tails (≥10 trailing As by default), and prunes low-coverage chains using orphanChainSubThresh and postMergeChainSubThresh thresholds before alignment scoring. The quantification engine (default VBEM) then infers per-transcript abundances over equivalence classes of reads and outputs quant.sf. Optionally enable decoy-aware indexing with `-d/--decoys` to absorb reads of unexpected origin and improve specificity.

## Related tools

- **salmon 2.0** (Primary quantification engine; performs selective-alignment mapping, chain pruning, and EM/VBEM inference over equivalence classes) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++ version)** (Reference implementation for validation; achieves 0.99854 Pearson correlation (NumReads) and 0.99897 (TPM) with Rust 2.0 on byte-identical indices) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (Provides SSHash k-mer index and lookup; k-mer orientation correctness is critical for mapping accuracy)
- **piscem-rs** (Rust mapper underlying salmon 2.0; handles orientation-aware k-mer lookup, MEM extraction, and chaining)

## Examples

```
salmon index -t transcripts.fa -i salmon_index -p 16 && salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant
```

## Evaluation signals

- Per-transcript NumReads and TPM are present and numeric in quant.sf; no NaN or negative values.
- Per-transcript Pearson correlation ≥0.998 when compared against a reference implementation (e.g., salmon 1.12.0 on a byte-identical index) on the same data and index.
- Assigned read counts match within <1% of the reference when summed across all transcripts.
- Per-read mapping agreement ≥99.8% when comparing unmapped_names.txt against a reference (i.e., both tools agree on which reads are fully unmapped).
- Logs show no warnings about poly-A clipping failures or chain-pruning edge cases for the read set size.

## Limitations

- Index format changed in salmon 2.0; indices built with salmon 1.x must be rebuilt.
- Chain-pruning thresholds (orphanChainSubThresh, postMergeChainSubThresh) default to 0.0 in Rust salmon 2.0 but 0.95 and 0.9 in C++ salmon 1.12.0; this accounts for ~80% of mapping discrepancies (~49k reads on 36.35M reads) and is describable but not yet harmonized.
- Posterior-sampled BAM output (--sampleOut, --sampleUnaligned, --writeQualities) is not yet implemented; acceptor flags are recognized but not functional.
- Bias correction (--seqBias, --gcBias) is available but performance is not quantified in this evaluation.
- Single-cell quantification functionality has been removed from salmon; use alevin-fry ecosystem instead.

## Evidence

- [methods] selective alignment mode (the default) on paired-end reads: "Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with `-l A` (auto-detect library type), no bias correction"
- [methods] k-mer lookup and chain pruning: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9"
- [methods] poly-A tail clipping step: "Default clips poly-A tails (≥10 trailing As → trimmed; all-A dropped), matching pufferfish FixFasta"
- [methods] output format and quantification correlation: "On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM"
- [readme] workflow definition: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
- [readme] decoy-aware indexing benefit: "Accounting for fragments of unexpected origin improves quantification. salmon can index decoy sequence (e.g. the genome) alongside the transcriptome"

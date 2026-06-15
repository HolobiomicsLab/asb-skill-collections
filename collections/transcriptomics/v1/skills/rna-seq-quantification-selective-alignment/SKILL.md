---
name: rna-seq-quantification-selective-alignment
description: Use when you have paired-end or single-end RNA-seq reads (FASTQ format) and a reference transcriptome (FASTA), and you need to estimate transcript-level abundances (NumReads and TPM per transcript) rather than gene-level counts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0080
  tools:
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0 (C++)
  - pufferfish
  - alevin-fry
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

# rna-seq-quantification-selective-alignment

## Summary

Quantify transcript abundances from RNA-seq reads using selective alignment, which combines fast k-mer-based mapping with MEM extraction and alignment scoring to assign reads to transcripts while estimating abundance via an EM/VBEM statistical model. This skill is used when you have raw sequencing reads and a transcriptome reference, and need per-transcript NumReads and TPM estimates with transcript-level isoform resolution.

## When to use

You have paired-end or single-end RNA-seq reads (FASTQ format) and a reference transcriptome (FASTA), and you need to estimate transcript-level abundances (NumReads and TPM per transcript) rather than gene-level counts. Selective alignment is appropriate when you want fast, bias-aware quantification with high read assignment accuracy (99%+ per-read mapping agreement across compatible tools). Use this instead of alignment-free sketch mode when you need maximum sensitivity and specificity on challenging datasets (e.g., short reads with substantial secondary mapping).

## When NOT to use

- If you already have BAM/SAM alignments and only need to infer abundance from existing assignments, use `salmon quant -a` (alignment mode) instead; selective alignment is not needed.
- If your input reads are extremely short (e.g. <20 bp) or highly degraded, selective alignment may struggle; consider genome-guided quantification or alignment-free sketch mode as alternatives.
- If you need single-cell quantification (e.g. barcode parsing, UMI deduplication), do not use salmon 2.0 directly; use the alevin-fry ecosystem (piscem + alevin-fry) instead, as salmon 2.0 removed the `salmon alevin` command.

## Inputs

- FASTQ reads (paired-end or single-end, gzip-compressed or uncompressed)
- Reference transcriptome FASTA (cDNA, e.g. Ensembl or RefSeq)
- Optional: pre-built salmon index (from a prior `salmon index` run)

## Outputs

- quant.sf (TSV with columns: Name, Length, EffectiveLength, TPM, NumReads)
- logs/salmon_quant.log (quantification run metadata and diagnostics)
- unmapped_names.txt (optional; list of fully-unmapped reads if --dumpUnmapped is set)

## How to apply

First, build a byte-deterministic index from your reference transcriptome using `salmon index` with a fixed k-mer length and seed; ensure non-ACGT residues are replaced deterministically to guarantee index reproducibility across runs. Next, run `salmon quant` in selective-alignment mode (the default) with your reads, specifying library type (auto-detect with `-l A` if unknown), thread count, and output directory; by default, salmon clips poly-A tails (≥10 trailing As) and applies orphan chain pruning (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0 in salmon 2.0; 0.95 and 0.9 respectively in C++ 1.12.0). The selective-alignment pipeline internally performs k-mer lookup via pufferfish's SSHash, extracts MEMs, chains seeds, and aligns via local Smith-Waterman before assigning reads to equivalence classes. Finally, extract NumReads and TPM columns from the output `quant.sf` file. For maximum reproducibility across tool versions or implementations (e.g., C++ vs. Rust), rebuild indices after upgrading, as index formats may change between major versions.

## Related tools

- **salmon 2.0** (Primary quantification tool; executes selective alignment (k-mer lookup, MEM extraction, alignment scoring) and EM/VBEM inference to estimate transcript abundances from reads) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (Legacy version for backwards compatibility; achieves 99.83% per-read mapping agreement with salmon 2.0 on byte-identical indices; differs in chain-pruning thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9)) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (Provides SSHash k-mer lookup and index structures underlying selective alignment; implements both streaming and non-streaming k-mer orientation for canonical vs. raw k-mer queries) — https://github.com/COMBINE-lab/pufferfish
- **piscem-rs** (Rust-based mapper that derives orientation correctly; foundation for the Rust port of selective alignment used in salmon 2.0)
- **alevin-fry** (Successor to salmon alevin for single-cell quantification; consumes RAD files from piscem or salmon alevin (deprecated) and performs barcode, UMI, and cell-level quantification) — https://github.com/COMBINE-lab/alevin-fry

## Examples

```
salmon index -t transcripts.fa -i salmon_index -p 16 && salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant
```

## Evaluation signals

- Pearson correlation of NumReads and TPM between independent salmon runs on the same index and reads should exceed 0.998 (0.99854 achieved on ERR188044 between C++ 1.12.0 and Rust salmon 2.0)
- Per-read mapping agreement (comparing unmapped_names.txt files for fully-unmapped reads coded 'u') should exceed 99% when comparing across compatible tool versions and settings
- Total assigned NumReads should match to within <1% between runs with identical settings and index format; differences >2% indicate upstream chain-pruning threshold mismatches or pufferfish bugs
- quant.sf NumReads column must be a non-negative integer and TPM must be non-negative and sum to approximately 1e6 across all transcripts (or be normalized to 1e6 in downstream analysis)
- Index rebuild after major version upgrade should be enforced; attempting to use a salmon 1.x index with salmon 2.0 should fail with a clear error message

## Limitations

- Index format changed between salmon 1.12.0 and salmon 2.0, requiring users to rebuild indices; byte-identical indices from different major versions are not guaranteed to exist
- Selective alignment is sensitive to chain-pruning default thresholds (orphanChainSubThresh, postMergeChainSubThresh); different settings can introduce ~2% per-read disagreement in downstream assignments, even with identical indices
- A pufferfish k-mer-orientation bug (present in older SSHash versions) caused ~2% false negatives in mapping; this was fixed upstream, but older installations may still expose the bug
- Some infrequently-used flags from salmon 1.x are not yet implemented in salmon 2.0 Rust rewrite: --minAssignedFrags, --eqclasses, --alternativeInitMode, --bootstrapReproject, --noGammaDraw, --numBiasSamples, --sampleOut, --sampleUnaligned, --writeQualities, --auxTargetFile, --writeOrphanLinks
- Rust salmon 2.0 maps ~62k reads in ERR188044 that C++ salmon leaves fully unmapped; ~80% of this gap is due to chain-sub-optimality default differences (describable, deferred); the remaining ~20% derives from genuine algorithmic improvements in the Rust port

## Evidence

- [other] On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%.: "On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%."
- [other] Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with `-l A` (auto-detect library type), no bias correction, and default chain-pruning thresholds (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0).: "Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with `-l A` (auto-detect library type), no bias correction, and default chain-pruning thresholds"
- [other] Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement (193,759 transcripts).: "Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement (193,759 transcripts)."
- [methods] Selective alignment is always on; default clips poly-A tails (≥10 trailing As → trimmed; all-A dropped), matching pufferfish FixFasta.: "Selective alignment is always on; default clips poly-A tails (≥10 trailing As → trimmed; all-A dropped), matching pufferfish FixFasta"
- [readme] Salmon keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read.: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
- [readme] The index format changed, so you must rebuild your index.: "the index format changed, so you must rebuild your index"
- [methods] C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9.: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9"
- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup.: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] ~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh =: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95"
- [readme] Single-cell quantification moved to the [alevin-fry] ecosystem (`salmon alevin` is removed).: "Single-cell quantification moved to the [alevin-fry] ecosystem (`salmon alevin` is removed)."
- [discussion] Some of the least-frequently used or niche features were removed.: "Some of the least-frequently used or niche features were removed"

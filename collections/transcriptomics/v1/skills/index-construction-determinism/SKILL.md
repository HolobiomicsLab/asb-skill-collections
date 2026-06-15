---
name: index-construction-determinism
description: Use when when comparing quantification results between two versions of a tool (e.g., salmon 2.0 Rust rewrite vs. C++ salmon 1.12.0), or when validating a new tool implementation against a reference version.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3308
  tools:
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0
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

# index-construction-determinism

## Summary

Verify that transcript indices built from the same source FASTA with identical parameters produce byte-identical outputs across different tool versions or implementations, ensuring reproducible quantification results. This skill surfaces hidden tool bugs (e.g., k-mer orientation errors) that would otherwise manifest only as small divergences in read-mapping agreement.

## When to use

When comparing quantification results between two versions of a tool (e.g., salmon 2.0 Rust rewrite vs. C++ salmon 1.12.0), or when validating a new tool implementation against a reference version. Apply this skill early in validation pipelines to establish a reproducibility baseline before running downstream inference—if indices are not byte-identical, downstream disagreement cannot be attributed solely to algorithmic differences in quantification inference.

## When NOT to use

- When comparing tools designed for different data types (e.g., salmon for bulk RNA-seq vs. piscem for single-cell), as index format and parameterization differ by design.
- When the input FASTA has not been consistently cleaned (e.g., non-ACGT characters are replaced non-deterministically), as index divergence will not be interpretable.
- When comparing versions with intentionally different default chain-pruning thresholds or other algorithmic settings, unless those settings are first harmonized; raw disagreement alone does not reveal bugs.

## Inputs

- Transcriptome FASTA (cleaned, with deterministic non-ACGT replacement)
- Index parameters (k-mer length, thread count, optional decoy sequences)
- Paired-end or single-end RNA-seq reads (FASTQ)

## Outputs

- Byte-identical (or non-identical) index files from both tool versions
- quant.sf quantification tables (NumReads and TPM columns) from both tools
- Per-transcript Pearson correlation coefficients (NumReads and TPM)
- unmapped_names.txt files from both tools
- Per-read mapping agreement percentage
- Total assigned NumReads difference as a percentage

## How to apply

Build the same transcriptome index twice using both tool versions with identical parameters (same cleaned FASTA with deterministic non-ACGT replacement, same k-mer length, same threads, same decoys if any). Compare the resulting index files byte-for-byte using checksums or binary diff tools. If indices match, run both tools on the same reads with the same selective-alignment mode parameters and library-type detection settings (e.g., `-l A` auto-detect). Extract per-transcript NumReads and TPM columns from the quant.sf outputs and compute Pearson correlations; extract unmapped read names and compute the percentage of per-read mapping agreement (focusing on fully-unmapped reads coded 'u'). Correlations ≥0.999 and per-read agreement ≥99.8% on a byte-identical index indicate the tools map and quantify equivalently; larger discrepancies signal algorithmic divergences or bugs. If indices are not byte-identical but quantification correlations remain high, investigate whether the index format changed intentionally or whether a pufferfish/lookup-table bug is present.

## Related tools

- **salmon 2.0** (Rust rewrite of salmon for index construction and quantification; primary tool being validated) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0** (C++ reference implementation for byte-identity and quantification agreement comparison) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (K-mer lookup engine underlying index construction; bugs (e.g., k-mer-orientation in SSHash streaming lookup) are revealed by index-level validation)

## Examples

```
salmon index -t transcripts.fa -i salmon_index_v2 -k 31 -p 16; salmon index -t transcripts.fa -i salmon_index_cpp -k 31 -p 16; diff <(md5sum salmon_index_v2/*) <(md5sum salmon_index_cpp/*); salmon quant -i salmon_index_v2 -l A -1 reads_1.fq.gz -2 reads_2.fq.gz -o quant_v2; salmon quant -i salmon_index_cpp -l A -1 reads_1.fq.gz -2 reads_2.fq.gz -o quant_cpp; paste quant_v2/quant.sf quant_cpp/quant.sf | awk '{print $1, $5, $10}' | Rscript -e 'data <- read.table("/dev/stdin", header=F); print(cor(data$V2, data$V3, method="pearson"))'
```

## Evaluation signals

- Byte-identity of index files (checksums match or binary diff is empty) when built from the same FASTA with identical parameters
- Per-transcript Pearson correlation ≥0.999 for both NumReads and TPM between the two tools on a byte-identical index
- Per-read mapping agreement ≥99.8% (percentage of reads where both tools agree on mapped/unmapped status)
- Total assigned NumReads difference <1% when quantifying the same dataset with the same selective-alignment mode and library-type parameters
- Reproducibility check: re-running the same commands on the same inputs yields identical quantification outputs (deterministic randomness in seeding or tie-breaking)

## Limitations

- Chain-pruning threshold differences (e.g., orphanChainSubThresh and postMergeChainSubThresh) between versions can account for ~80% of per-read mapping disagreement even on byte-identical indices; harmonize these parameters before concluding that disagreement indicates a bug.
- Index format changes (e.g., salmon 2.0 Rust uses a new format) mean byte-identity is not achievable across major versions; in such cases, correlations and per-read agreement become the primary validation metrics rather than checksums.
- Very short reads (<50 bp) or highly repetitive transcriptomes may show larger discrepancies; the validation was demonstrated on 76 bp paired-end reads from a human reference (GRCh38).
- Downstream inference divergence (VBEM vs. EM, bias-correction toggling) will mask index-level agreement, so validation must be performed with the same inference settings across tools.

## Evidence

- [other] Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement: "Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement (193,759 transcripts)."
- [other] On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%: "On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%."
- [other] After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [other] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [other] ~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh =: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh"
- [intro] salmon 2.0 maintains the same workflow (salmon index → salmon quant → quant.sf) and output formats as the previous version: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
- [readme] the index format changed, so you must rebuild your index: "the index format changed, so you must rebuild your index"

---
name: transcript-abundance-correlation-analysis
description: Use when when validating a new or reimplemented quantification tool against a reference implementation on the same dataset and index, or when investigating whether changes to seed representation, chain pruning thresholds, or other algorithmic parameters affect downstream abundance estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - piscem-rs
  - salmon 2.0
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

# Transcript Abundance Correlation Analysis

## Summary

Compare per-transcript quantification outputs (NumReads, TPM) between two RNA-seq quantification tools or implementations using Pearson correlation and per-read mapping agreement metrics to assess quantitative concordance and identify systematic differences in abundance estimation.

## When to use

When validating a new or reimplemented quantification tool against a reference implementation on the same dataset and index, or when investigating whether changes to seed representation, chain pruning thresholds, or other algorithmic parameters affect downstream abundance estimates. Apply this skill to byte-identical indices and the same read set to isolate the effect of the tool/parameter under test.

## When NOT to use

- When comparing tools run on different reference indices or different cleaned FASTA sources—differences in index content will dominate tool differences.
- When one or both quantification runs used bias correction (--seqBias, --gcBias) or non-standard chain-pruning thresholds without explicit matching—these parameters will confound the comparison.
- When datasets have very low read depth or transcript abundance ranges that limit statistical power for correlation estimation (correlation magnitude depends on abundance variability).

## Inputs

- paired-end or single-end RNA-seq reads (FASTQ format)
- byte-identical transcriptome index built identically by both tools
- quant.sf quantification output from tool 1 (NumReads, TPM columns)
- quant.sf quantification output from tool 2 (NumReads, TPM columns)
- unmapped_names.txt read-level mapping status files from both runs

## Outputs

- Pearson correlation coefficient (r) for NumReads between tools
- Pearson correlation coefficient (r) for TPM between tools
- per-read mapping agreement percentage
- mapping rate (%) for each tool
- count and percentage of discordant reads (mapped by one tool, unmapped by the other)
- total assigned NumReads difference (percentage or absolute count)

## How to apply

Run both quantification pipelines (e.g., salmon 2.0 Rust and salmon 1.12.0 C++) on identical input reads using the same library-type specification (-l A for auto-detect), no bias correction, and matching selective-alignment settings. Extract the NumReads and TPM columns from the quant.sf output files for all transcripts. Compute Pearson correlation coefficient (r) for NumReads and TPM across the two runs—values ≥0.998 indicate high quantitative agreement. Separately, compare per-read mapping outcomes by analyzing unmapped_names.txt files to compute the percentage of reads on which both tools agree on mapping status (fully unmapped='u', or mapped). Calculate total assigned NumReads difference as a percentage to identify any global assignment bias. Report mapping rate as a percentage and quantify the magnitude of discordant reads (e.g., Rust maps X reads C++ leaves fully unmapped). This analysis exposes algorithm-level differences masked by coarse-grain output statistics.

## Related tools

- **salmon 2.0** (Rust reimplementation of transcript quantification with selective alignment; primary tool for generating quant.sf output and unmapped read records for comparison) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (Reference C++ implementation of transcript quantification; second tool to compare against Rust rewrite on identical inputs) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **piscem-rs** (Rust-based read mapper underlying salmon 2.0 selective alignment; responsible for per-read mapping decisions and chain pruning) — https://github.com/COMBINE-lab/salmon

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant && paste <(cut -f1,4 sample_quant/quant.sf | tail -n +2) <(cut -f4 reference_salmon_output/quant.sf | tail -n +2) | awk '{print $1, $2, $3}' | R --slave -e 'data <- read.table("stdin"); cat("Pearson r (NumReads):", cor(data[,2], data[,3]), "\n")'
```

## Evaluation signals

- Pearson r ≥ 0.9985 for NumReads and r ≥ 0.9989 for TPM indicates tool implementations are quantitatively concordant on a byte-identical index.
- Per-read mapping agreement ≥ 99.8% shows that both tools agree on the vast majority of individual read assignments.
- Total assigned NumReads difference < 1% of total reads quantified indicates no large-scale global assignment bias between tools.
- Discordant read counts (e.g., ~62k reads mapped by Rust but unmapped by C++) are attributable to documented parameter differences (e.g., chain-pruning threshold defaults) rather than random variation.
- Mapping rate values differ by ≤0.01% when chain-pruning parameters are equalized, isolating algorithmic differences from parameter choices.

## Limitations

- Correlation magnitude depends on the range of transcript abundances in the dataset; datasets with narrow abundance distributions will show lower correlation coefficients even with perfect tool agreement.
- Default chain-pruning thresholds differ between C++ salmon 1.12.0 (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) and Rust salmon 2.0 (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0); ~80% of mapping discordance may stem from these defaults rather than core algorithmic differences, requiring explicit parameter matching to isolate true implementation differences.
- The analysis requires access to per-read mapping status files (unmapped_names.txt) and raw quant.sf outputs; some quantification pipelines or older versions may not preserve these intermediate outputs.
- Very short reads (< 51 bp) or reads with high sequencing error rates may exhibit different behavior between tools due to seed-collection and alignment-scoring parameter sensitivity.

## Evidence

- [methods] On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%.: "per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%"
- [methods] Extract NumReads and TPM columns from quant.sf outputs for both runs. Compute Pearson correlations for NumReads and TPM per transcript across the two tools, and compute total assigned NumReads difference as a percentage. Count per-read mapping agreement by comparing unmapped_names.txt files (fully-unmapped reads only, coded 'u') and report the percentage of reads on which both tools agree.: "Extract NumReads and TPM columns from quant.sf outputs for both runs. Compute Pearson correlations for NumReads and TPM per transcript across the two tools, and compute total assigned NumReads"
- [methods] Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with -l A (auto-detect library type), no bias correction, and default chain-pruning thresholds (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0). Run C++ salmon 1.12.0 quant in selective-alignment mode on the same reads with -l A, no bias correction, and default thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9).: "Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with -l A, no bias correction, and default chain-pruning thresholds (orphanChainSubThresh=0.0,"
- [methods] ~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh =: "~80% (~49k): a chain-sub-optimality default difference. C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh"
- [readme] It keeps the same workflow (salmon index → salmon quant → quant.sf) and the same output formats downstream tools read: "It keeps the same workflow (salmon index → salmon quant → quant.sf) and the same output formats downstream tools read"

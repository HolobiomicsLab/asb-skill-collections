---
name: pearson-correlation-analysis-genomics
description: Use when when comparing transcript quantification outputs (NumReads counts, abundance estimates) from two mapper implementations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
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

# Pearson Correlation Analysis for Genomics Quantification

## Summary

Compute Pearson correlation coefficients (r) between quantification results (e.g., per-transcript NumReads) from two implementations or seed strategies to assess quantitative agreement and reproducibility of transcript abundance estimates. This skill validates that mapping algorithms and seed representations yield consistent transcript-level quantification despite algorithmic or implementation differences.

## When to use

When comparing transcript quantification outputs (NumReads counts, abundance estimates) from two mapper implementations (e.g., C++ vs. Rust salmon), variant seed representations (sparse fixed-k anchors, reference k-mer variants, uni-MEMs), or different selective-alignment parameter sets on the same sequencing reads and byte-identical reference index. Use this skill to isolate whether observed mapping-rate differences stem from fundamental algorithmic divergence or from implementation/representation variants.

## When NOT to use

- Comparing quantification outputs from different reference transcriptomes or differently-constructed indices; correlation will reflect reference divergence, not implementation agreement.
- Analyzing single-implementation results without a paired baseline; Pearson r requires two distributions to compare.
- Comparing mappers applied to different read sets or read subsets; technical variation in read set will confound correlation.

## Inputs

- Per-transcript NumReads output from first mapper implementation or seed strategy (e.g., quant.sf from C++ salmon 1.12.0)
- Per-transcript NumReads output from second mapper implementation or seed strategy (e.g., quant.sf from Rust salmon 2.0)
- Byte-identical reference index (GRCh38 cDNA, Ensembl R64-1-1 cDNA, or equivalent)
- Identical read set (FASTQ, paired-end or single-end) applied to both mappers

## Outputs

- Pearson correlation coefficient (r) between NumReads distributions from both implementations
- Transcript-level correlation matrix (optional: r values per transcript or per abundance quartile)
- Per-read mapping agreement percentage (optional: proportion of reads with identical mapping outcome)
- Stratified correlation metrics (e.g., r by transcript abundance, by number of mapping locations)

## How to apply

Extract per-transcript NumReads counts (or other transcript-level quantification metrics) from both mapper implementations or seed-representation variants applied to the same read set and reference index. Align the output by transcript identifier and calculate the Pearson correlation coefficient (r) across all transcripts. Verify that r ≥ 0.99 (or the project's stability threshold; the salmon article uses r ≥ 0.99854 as evidence of high quantitative agreement). If r falls below the threshold, stratify the correlation by transcript abundance quartiles or mapping ambiguity class to identify whether disagreement is systematic (affecting high-abundance or ambiguous transcripts differentially) or scattered. Document the number of transcripts with mapped reads in each implementation and any per-read mapping agreement metrics (e.g., 99.83% per-read mapping agreement in the salmon study) to distinguish read-level vs. transcript-level signal drift.

## Related tools

- **salmon 2.0 (Rust)** (Performs selective-alignment mapping and quantification of transcript abundances, outputting per-transcript NumReads counts for correlation comparison) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (Reference implementation for comparative quantification; final C++ release against which Rust port is validated for correlation agreement) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **piscem-rs** (Rust-based k-mer mapping library that corrects orientation handling in SSHash lookups, ensuring reliable seed collection for correlation validation) — https://github.com/COMBINE-lab/salmon

## Examples

```
# After running salmon quant with C++ and Rust implementations on the same reads and index, extract NumReads and compute Pearson correlation in R: reads_cpp <- read.table('cpp_quant.sf', header=T); reads_rust <- read.table('rust_quant.sf', header=T); merged <- merge(reads_cpp[,c('Name','NumReads')], reads_rust[,c('Name','NumReads')], by='Name'); r <- cor(merged$NumReads.x, merged$NumReads.y, method='pearson'); print(paste('Pearson r:', round(r, 5)))
```

## Evaluation signals

- Pearson r ≥ 0.99 (or project-specific threshold; article uses 0.99854) across all transcripts with mapped reads, indicating high quantitative agreement independent of seed representation or implementation language
- Per-read mapping agreement ≥ 99% (article reports 99.83%), confirming that disagreement is confined to transcript-level aggregation effects, not systematic read misassignment
- Mapping rate stability within ≤0.01% between implementations on byte-identical index, ruling out drift in sensitivity or specificity
- Consistent correlation magnitude when stratified by transcript abundance quartile or by single-mapped vs. multi-mapped reads, identifying whether disagreement is localized to ambiguous or low-abundance features
- Number of reads mapped uniquely by one implementation vs. the other (e.g., 'Rust maps 62,812 reads C++ leaves fully unmapped'; annotate with downstream impact on transcript abundance estimates)

## Limitations

- Pearson r measures linear association and may mask systematic biases in a subset of transcripts; stratified or robust correlation metrics (Spearman rho, Kendall tau) may be more sensitive to algorithmic divergence in edge cases.
- High correlation (r > 0.99) does not rule out implementation differences in chain pruning, orphan filtering, or alignment scoring thresholds that affect low-abundance transcripts; correlation is insensitive to small absolute differences in NumReads for rare features.
- Correlation analysis assumes transcript-level counts are normally or near-normally distributed; highly sparse or zero-inflated quantification outputs (e.g., dropout in single-cell data) may violate Pearson assumptions.
- Byte-identical index requirement limits applicability to comparing only implementations and seed representations that use the same k-mer lookup substrate; decoy handling, k-mer length, or bloom-filter size differences will confound correlation.

## Evidence

- [methods] On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies.: "On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies."
- [methods] Re-run salmon mapper with sparse fixed-k anchor representation, capturing mapping rate and NumReads correlation (Pearson r) against baseline.: "Re-run salmon mapper with sparse fixed-k anchor representation, capturing mapping rate and NumReads correlation (Pearson r) against baseline."
- [methods] Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants.: "Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants."
- [methods] per-read mapping agreement | 99.83%: "per-read mapping agreement | 99.83%"
- [methods] Rust maps 62,812 reads C++ leaves fully unmapped (u), C++ maps only 154 Rust doesn't: "Rust maps 62,812 reads C++ leaves fully unmapped (u), C++ maps only 154 Rust doesn't"

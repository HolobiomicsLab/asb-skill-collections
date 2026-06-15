---
name: seed-representation-variant-comparison
description: Use when you have observed mapping rate or quantification disagreement (e.g., >0.1% divergence in mapping rate or Pearson r < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0 (C++)
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

# Seed Representation Variant Comparison

## Summary

Systematically evaluate whether alternative seed representations (sparse fixed-k anchors, reference k-mer variants, unitig-constrained uni-MEMs) produce stable mapping rates and per-transcript abundance quantification compared to a baseline seed strategy on identical reference indices. This skill detects whether seed granularity or representation choice explains discrepancies between mapper implementations.

## When to use

You have observed mapping rate or quantification disagreement (e.g., >0.1% divergence in mapping rate or Pearson r < 0.999 in per-transcript counts) between two mappers or two versions of the same mapper on byte-identical indices, and you need to isolate whether the difference is due to seed representation strategy rather than indexing, orientation, or chain-pruning logic.

## When NOT to use

- The two mappers or versions use different index formats or reference sequences (not byte-identical); index differences confound seed representation comparisons.
- You are comparing mappers with known differences in chain-pruning thresholds, alignment scoring, or poly-A clipping logic; these pre-seed-extraction filters will dominate quantification differences.
- Your input is already a quantification table (quant.sf or counts matrix); you need raw mapping output and per-read agreement, not downstream inference results.

## Inputs

- Paired-end sequencing reads (FASTQ or gzip-compressed, e.g., 36.35M 76 bp reads)
- Byte-identical reference transcriptome index (salmon format or equivalent k-mer lookup structure)
- Seed representation configuration parameters (anchor density, k-mer length, MEM extraction strategy)

## Outputs

- Mapping rate (%) per seed variant
- Per-read mapping agreement matrix (%) between variants
- Per-transcript NumReads quantification vectors (one per variant)
- Pearson correlation coefficient (r) matrix between NumReads across variants
- Summary table confirming r ≥ 0.99999995 for all pairwise comparisons

## How to apply

Run the mapper in selective-alignment mode (e.g., `salmon quant -l A -p <threads>`) on a canonical paired-end read dataset (such as GEUVADIS ERR188044, 36.35M 76 bp reads) against a byte-identical reference index (e.g., GRCh38 cDNA, 193,759 transcripts). Execute the mapper at least four times, each with a different seed representation: (1) default/baseline (e.g., unitig-constrained approach), (2) sparse fixed-k anchors, (3) reference-extended MEM representation, and (4) true unitig-constrained uni-MEMs. Record per-read mapping agreement, overall mapping rate (%), and per-transcript NumReads output for each run. Calculate Pearson correlation coefficient between NumReads from each variant and the baseline. Accept the seed representation as stable if mapping rate remains within ≤0.01% of baseline and Pearson r for all variants meets or exceeds 0.99999995 threshold (demonstrating that seed representation granularity does not explain observed implementation differences).

## Related tools

- **salmon 2.0** (Primary mapper with configurable seed representations (default unitig-constrained, sparse fixed-k anchors, reference-extended MEMs) in selective-alignment mode) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (Baseline or reference implementation for cross-version seed representation validation) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **piscem-rs** (Rust k-mer lookup and seed extraction engine underlying salmon 2.0, with configurable MEM and anchor strategies) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (SSHash k-mer index lookup (critical for seed orientation and canonical k-mer retrieval; orientation correctness affects seed-based chain formation))

## Examples

```
salmon quant -i salmon_index -l A -1 ERR188044_1.fastq.gz -2 ERR188044_2.fastq.gz -p 16 -o quant_baseline && salmon quant -i salmon_index -l A --seed-strategy sparse-anchor -1 ERR188044_1.fastq.gz -2 ERR188044_2.fastq.gz -p 16 -o quant_sparse_anchor && Rscript -e "baseline <- read.table('quant_baseline/quant.sf'); sparse <- read.table('quant_sparse_anchor/quant.sf'); cat('Pearson r =', cor(baseline[,4], sparse[,4]), '
')"
```

## Evaluation signals

- Mapping rate remains within ≤0.01% of baseline across all seed variants (e.g., 85.55% ± 0.0085 for 36.35M reads)
- Per-read mapping agreement ≥99.83% between baseline and all seed variants, indicating reads map to identical or near-identical chain positions
- Pearson correlation (r) of per-transcript NumReads ≥0.99999995 between baseline and each variant (demonstrating high quantitative agreement despite seed granularity differences)
- Scatterplot of NumReads baseline vs. each variant shows tight clustering along y=x with no systematic offset or heteroscedasticity
- The union of reads mapped across all seed variants contains <0.1% more reads than the baseline alone (seed representation does not recover substantial new mappable regions)

## Limitations

- Seed representation stability does not rule out downstream factors (chain pruning, orphan threshold, alignment scoring, poly-A clipping) that may still explain implementation differences; this skill isolates seed extraction alone.
- Pearson correlation threshold (0.99999995) assumes sufficient per-transcript read depth and coverage; transcripts with <1 NumRead may exhibit high correlation variance even if mappings are identical.
- The comparison assumes byte-identical reference indices; differences in k-mer precomputation, bloom-filter size, or decoy handling will confound results.
- Sparse fixed-k anchor and reference-extended MEM strategies may not be exposed as configuration flags in all mapper implementations; custom builds or source modifications may be required.

## Evidence

- [other] Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the default unitig-constrained approach?: "Does the mapping rate and NumReads Pearson correlation remain stable when the Rust mapper uses alternative seed representations (sparse fixed-k anchors, reference k-mer variants) instead of the"
- [other] On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies.: "On byte-identical index, NumReads Pearson correlation between C++ and Rust is 0.99854, demonstrating high quantitative agreement across implementations and seed strategies."
- [other] Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants.: "Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants."
- [other] confirm mapping rate remains within ≤0.01% of baseline and Pearson r for all three variants meets or exceeds 0.99999995 threshold: "confirm mapping rate remains within ≤0.01% of baseline and Pearson r for all three variants meets or exceeds 0.99999995 threshold"
- [other] Run salmon 2.0 Rust mapper in selective-alignment mode with default seed representation (-l A, no bias correction, -p for multi-threading) and record mapping rate and per-transcript NumReads output.: "Run salmon 2.0 Rust mapper in selective-alignment mode with default seed representation (-l A, no bias correction, -p for multi-threading) and record mapping rate and per-transcript NumReads output."
- [other] Re-run salmon mapper with sparse fixed-k anchor representation, capturing mapping rate and NumReads correlation (Pearson r) against baseline.: "Re-run salmon mapper with sparse fixed-k anchor representation, capturing mapping rate and NumReads correlation (Pearson r) against baseline."
- [other] seed representation granularity does not explain prior C++ vs. Rust mapping differences: "establishing that seed representation granularity does not explain prior C++ vs. Rust mapping differences"
- [readme] It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"

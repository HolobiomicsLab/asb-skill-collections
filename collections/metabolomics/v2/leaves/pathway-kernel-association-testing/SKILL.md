---
name: pathway-kernel-association-testing
description: Use when you have paired genotype and phenotype data and want to test
  for association between a predefined genetic pathway (set of genes or variants)
  and a quantitative or binary trait, particularly when individual-variant tests lack
  power or when pathway-level aggregation is scientifically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3197
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3053
  tools:
  - PaIRKAT
  license_tier: restricted
derived_from:
- doi: 10.1101/2021.04.23.440821v1
  title: PaIRKAT
evidence_spans:
- github.com/CharlieCarpenter/PaIRKAT
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairkat_cq
    doi: 10.1101/2021.04.23.440821v1
    title: PaIRKAT
  dedup_kept_from: coll_pairkat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.04.23.440821v1
  all_source_dois:
  - 10.1101/2021.04.23.440821v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-kernel-association-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply the PaIRKAT (pathway-integrated kernel association test) function to genotype and phenotype data to compute pathway-level association test statistics and p-values. This skill enables detection of associations between genetic pathways and phenotypic traits by aggregating variant effects within biologically defined gene sets.

## When to use

Use this skill when you have paired genotype and phenotype data and want to test for association between a predefined genetic pathway (set of genes or variants) and a quantitative or binary trait, particularly when individual-variant tests lack power or when pathway-level aggregation is scientifically motivated.

## When NOT to use

- Input data are already aggregated at pathway level or summarized; use PaIRKAT on raw variant-level genotypes instead.
- Only individual-variant-level results are available and pathway grouping is not defined.
- Sample sizes are extremely small (n < 20) and kernel method assumptions may not hold.

## Inputs

- genotype data matrix (variants × samples)
- phenotype vector (aligned to samples)
- pathway definition (variant/gene set membership)

## Outputs

- test statistics (pathway-level kernel association test)
- p-values (unadjusted or permutation-based)
- structured results file with pathway associations

## How to apply

Load genotype and phenotype files from your data directory into memory and format them to match PaIRKAT function requirements (e.g., genotype matrix with variants as rows and samples as columns; phenotype vector aligned to samples). Clone or retrieve the PaIRKAT repository and source the core analysis scripts. Execute the PaIRKAT kernel association test function on the prepared data with your pathway definition (variant or gene grouping). Extract and format the resulting test statistics, p-values, and pathway-level association measures into a structured output file. Cross-validate results using the provided Type I error and power simulation scripts to assess false-positive rate and statistical power under your data characteristics.

## Related tools

- **PaIRKAT** (implements pathway-integrated kernel association test functions; core analysis engine for computing pathway-level test statistics and p-values) — github.com/CharlieCarpenter/PaIRKAT

## Evaluation signals

- Output p-values and test statistics are numeric, finite, and span expected ranges (p ∈ [0,1]; test statistic ≥ 0 for kernel tests).
- Type I error simulation scripts confirm false-positive rate near nominal significance level (e.g., ~5% at α=0.05).
- Power simulation scripts show increasing statistical power with increasing effect size or sample size.
- Results file contains pathway-level associations for all input pathways with no missing or NaN entries.
- Genotype and phenotype inputs match in sample count and order before test execution.

## Limitations

- No changelog available; version history and reproducibility constraints not documented.
- Pathway definition quality directly impacts power; poorly defined or heterogeneous pathways may reduce test sensitivity.
- Kernel method assumptions (kernel matrix positive semi-definiteness) must be met; validation not explicitly mentioned in documentation.

## Evidence

- [other] PaIRKAT provides scripts implementing PaIRKAT functions that can be applied to example workflow data, with supporting simulation scripts for Type I error and power assessment.: "PaIRKAT provides scripts implementing PaIRKAT functions that can be applied to example workflow data, with supporting simulation scripts for Type I error and power assessment"
- [other] Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements.: "Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements"
- [other] Execute the PaIRKAT kernel association test function on the prepared data.: "Execute the PaIRKAT kernel association test function on the prepared data"
- [other] Extract and format the test results (p-values, test statistics, pathway-level associations) into a structured output file.: "Extract and format the test results (p-values, test statistics, pathway-level associations) into a structured output file"
- [readme] Scripts for PaIRKAT functions with example work flow: "Scripts for PaIRKAT functions with example work flow"
- [readme] TypeI and Power simulation scripts: "TypeI and Power simulation scripts"

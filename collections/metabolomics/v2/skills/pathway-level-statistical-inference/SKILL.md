---
name: pathway-level-statistical-inference
description: Use when when you have genotype data (variants grouped by pathway annotation) and quantitative or binary phenotype data, and you want to test whether a pathway as a whole is associated with the phenotype, rather than testing individual variants.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_2885
  tools:
  - PaIRKAT
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
---

# pathway-level-statistical-inference

## Summary

Apply kernel association tests to detect pathway-level genetic associations by integrating genotype and phenotype data across multiple variants within a pathway. This skill uses PaIRKAT (Pathway-Integrated Rank Kernel Association Test) to test for collective pathway effects while accounting for variant correlation structure.

## When to use

When you have genotype data (variants grouped by pathway annotation) and quantitative or binary phenotype data, and you want to test whether a pathway as a whole is associated with the phenotype, rather than testing individual variants. Use this when individual variant effect sizes are small but may be collectively informative, or when you need to account for linkage disequilibrium within pathways.

## When NOT to use

- Your input is already a pre-computed p-value or summary statistic per pathway; apply this skill to raw genotype and phenotype data instead.
- You have only a single variant or very few variants per pathway; single-variant tests are more appropriate.
- Your phenotype data are already aggregated or pre-filtered by pathway; this skill requires unaggregated individual-level data.

## Inputs

- genotype matrix (samples × variants, or variants × samples)
- phenotype vector (quantitative or binary traits)
- pathway variant groupings (pathway annotations mapping variants to pathways)
- optional: covariate matrix for adjustment

## Outputs

- p-value per pathway (pathway-level association significance)
- test statistic per pathway
- pathway effect estimate or kernel score
- structured results table (pathway ID, statistic, p-value, effect size)

## How to apply

Load the PaIRKAT analysis scripts and prepare your genotype and phenotype data in the format required by the PaIRKAT functions (typically matrices with variants as rows/columns and samples as the corresponding dimension). Format the phenotype data to match function requirements (continuous or binary). Execute the PaIRKAT kernel association test function on the prepared data, specifying the pathway variant groupings. The function computes a test statistic by integrating over the pathway's variant correlation structure (kernel matrix) and produces a p-value for pathway-level association. Extract the structured output containing p-values, test statistics, and pathway-level association estimates.

## Related tools

- **PaIRKAT** (Implements pathway-integrated kernel association test functions to compute pathway-level test statistics and p-values from genotype and phenotype data) — https://github.com/CharlieCarpenter/PaIRKAT

## Evaluation signals

- Output p-values are in the valid range [0, 1] and follow expected distribution under null hypothesis (uniform for independent pathways).
- Type I error rate matches target significance level (e.g., α=0.05) when validated on simulated null data; compare against Type I error simulation script results.
- Power to detect pathway associations is consistent with simulation expectations for known effect sizes; validate using Power simulation scripts provided in the repository.
- Test statistics and p-values are reproducible when re-running on the same input data with identical parameters.
- Pathway-level results are interpretable relative to component variant effect sizes; pathways with many associated variants should have lower p-values than those with few.

## Limitations

- Method assumes variants within a pathway can be meaningfully grouped; pathway annotations must be accurate and biologically relevant.
- Performance depends on the kernel matrix specification (e.g., linear kernel, polynomial); misspecification may reduce power.
- Large numbers of pathways increase multiple-testing burden; appropriate multiple-hypothesis correction (e.g., Bonferroni, FDR) should be applied.
- Phenotype must be compatible with the test framework (quantitative or binary); mixed or censored phenotypes may require adaptation.

## Evidence

- [intro] Core PaIRKAT function definition and workflow: "PaIRKAT provides scripts implementing PaIRKAT functions that can be applied to example workflow data"
- [other] Input data preparation and execution steps: "Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements. Execute the PaIRKAT kernel association test function on the prepared data."
- [other] Output structure and extraction: "Extract and format the test results (p-values, test statistics, pathway-level associations) into a structured output file"
- [intro] Simulation and validation support: "Type I error and power simulation scripts are available"
- [readme] Repository purpose and scope: "Scripts for PaIRKAT functions with example work flow"

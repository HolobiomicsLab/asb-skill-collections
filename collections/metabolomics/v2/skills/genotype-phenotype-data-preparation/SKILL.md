---
name: genotype-phenotype-data-preparation
description: Use when when you have raw genotype and phenotype data files (e.g., from a GWAS dataset or genetic study) and need to apply PaIRKAT or similar pathway-level association tests.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3517
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

# genotype-phenotype-data-preparation

## Summary

Format and structure raw genotype and phenotype files to match the input requirements of pathway-integrated kernel association test functions. This skill ensures data compatibility and proper variable alignment before statistical testing.

## When to use

When you have raw genotype and phenotype data files (e.g., from a GWAS dataset or genetic study) and need to apply PaIRKAT or similar pathway-level association tests. The input files must be reformatted to match the specific schema expected by the kernel association test function before analysis can proceed.

## When NOT to use

- Data is already in the exact format required by the kernel association test function.
- Genotypes and phenotypes are missing critical sample identifiers or cannot be aligned.
- You are performing quality control or filtering before data preparation (apply filtering first).

## Inputs

- raw genotype file
- raw phenotype file
- example workflow data

## Outputs

- formatted genotype matrix
- formatted phenotype vector or data frame
- sample-aligned genotype-phenotype data structure

## How to apply

Load example workflow data (genotype and phenotype files) into memory. Examine the expected input schema from PaIRKAT function documentation or example scripts. Reformat genotypes and phenotypes to align sample identifiers, ensure consistent variable naming, and encode genotypes in the format expected by the kernel function (typically numeric or matrix form). Validate that all samples present in phenotype data have matching genotype records, and that phenotype variables are properly encoded (e.g., binary traits as 0/1, continuous traits as numeric). After formatting, verify data dimensions and absence of missing values in key columns before passing to the kernel association test function.

## Related tools

- **PaIRKAT** (Pathway-integrated kernel association test function that consumes prepared genotype and phenotype data to perform statistical testing) — github.com/CharlieCarpenter/PaIRKAT

## Evaluation signals

- Genotype and phenotype files share identical sample identifiers with no mismatches or unaligned records.
- Genotype data is encoded in numeric or matrix form compatible with kernel function input schema.
- Phenotype variables are properly encoded (binary as 0/1, continuous as numeric) with no missing values in key columns.
- Data dimensions are consistent (same number of samples in both genotype and phenotype) and conform to PaIRKAT function expectations.
- Example workflow data successfully loads and produces valid output when passed to the kernel association test function.

## Limitations

- Requires prior knowledge of the PaIRKAT function schema; consult example workflow scripts for exact format specifications.
- No automated data validation or error recovery is described; misaligned samples or encoding errors will cause downstream test failures.
- The README provides only high-level descriptions; detailed format specifications must be inferred from example scripts in the repository.

## Evidence

- [other] Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements.: "Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements"
- [other] Load the example workflow data (genotype and phenotype files) into memory.: "Load the example workflow data (genotype and phenotype files) into memory"
- [readme] Scripts for PaIRKAT functions with example work flow: "Scripts for PaIRKAT functions with example work flow"

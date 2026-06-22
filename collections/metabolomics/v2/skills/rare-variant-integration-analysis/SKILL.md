---
name: rare-variant-integration-analysis
description: Use when when analyzing rare-variant associations where sample sizes are modest, individual-variant tests lack power, or you need to aggregate signal across multiple rare variants within a biological pathway.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3197
  edam_topics:
  - http://edamontology.org/topic_0634
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0625
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

# rare-variant-integration-analysis

## Summary

Apply pathway-integrated kernel association testing (PaIRKAT) to detect rare-variant effects by integrating genotype and phenotype data into a kernel-based statistical framework. This skill enables pathway-level rare-variant association detection when individual-variant signals are weak or sparse.

## When to use

When analyzing rare-variant associations where sample sizes are modest, individual-variant tests lack power, or you need to aggregate signal across multiple rare variants within a biological pathway. Use this when you have genotype data (VCF, imputed, or array-based) and quantitative or binary phenotypes, and suspect pathway-level rather than single-variant effects.

## When NOT to use

- Common-variant association analysis where individual SNP effects are expected to be large and well-powered — use standard GWAS instead.
- When genotype and phenotype samples do not match or cannot be reliably aligned — data integrity is prerequisite.
- Pathway definitions are unavailable or not biologically justified for the trait of interest.

## Inputs

- Genotype matrix or file (samples × variants, e.g. dosage or binary genotypes)
- Phenotype vector or file (quantitative or binary trait, sample-matched)
- Pathway or gene set definition (SNP list, gene boundaries, or pathway annotation)
- Sample metadata (optional covariates, population structure)

## Outputs

- Pathway-level test statistic (kernel-based association score)
- P-value for pathway association
- Formatted results table (pathway name, statistic, p-value, sample size)
- Simulation assessment output (Type I error rate, power curve)

## How to apply

Retrieve the PaIRKAT repository and load the pathway kernel association test functions. Format genotype and phenotype data to match PaIRKAT function requirements (typically matrix or data.frame input with matching sample identifiers). Execute the core PaIRKAT kernel association test function on the prepared data, specifying the pathway of interest (gene set or SNP set). Extract pathway-level test statistics and p-values from the function output. Validate results using the provided Type I error and power simulation scripts to confirm control of false positive rate and assess statistical power for your sample size and effect configuration.

## Related tools

- **PaIRKAT** (Core implementation of pathway-integrated rare-variant kernel association test functions and simulation utilities for Type I error and power assessment) — https://github.com/CharlieCarpenter/PaIRKAT

## Evaluation signals

- Test p-values are in valid range [0, 1] with no NA or infinite values; pathway test statistic is numeric and non-NA.
- Type I error simulation returns false positive rate near the nominal significance level (e.g. ≈0.05 at α=0.05) across replicate simulations under the null hypothesis.
- Power simulation demonstrates monotonic increase in power with effect size, sample size, or allele frequency under alternative hypotheses.
- Output table includes all expected columns (pathway ID, test statistic, p-value, sample count) with consistent row counts matching input pathway set.
- Genotype and phenotype sample identifiers match exactly; no samples are dropped without explicit documentation of reason.

## Limitations

- Requires careful specification of pathway/gene set definitions; misaligned or irrelevant pathway annotations reduce power and interpretability.
- Performance and Type I error control depend on accurate specification of null model (e.g. covariate adjustment); model misspecification can inflate false positive rate.
- No changelog or version history is documented in the repository, making it difficult to track methodological or implementation changes between releases.

## Evidence

- [intro] PaIRKAT provides scripts implementing PaIRKAT functions that can be applied to example workflow data: "PaIRKAT provides scripts for PaIRKAT functions with example work flow"
- [intro] Type I error and power assessment are supported via dedicated simulation scripts: "TypeI and Power simulation scripts"
- [other] Workflow involves preparing input data, executing the kernel test function, and extracting pathway-level associations: "Prepare input data by formatting genotypes and phenotypes to match PaIRKAT function requirements. Execute the PaIRKAT kernel association test function on the prepared data. Extract and format the"

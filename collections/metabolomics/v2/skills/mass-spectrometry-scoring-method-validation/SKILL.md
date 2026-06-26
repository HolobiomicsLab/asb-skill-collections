---
name: mass-spectrometry-scoring-method-validation
description: Use when you have high-resolution LC-MS data processed through both XCMS
  feature detection and RAMClustR clustering, and you need to verify the reliability
  of molecular weight assignments before downstream annotation or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RAMClustR
  - InterpretMSSpectrum
  - R
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-scoring-method-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Empirically validate agreement between independent molecular weight scoring methods applied to LC-MS metabolomics data. This skill quantifies concordance between the findMain and RAMClustR scoring approaches to establish confidence in molecular weight inference and identify systematic disagreement patterns.

## When to use

Apply this skill when you have high-resolution LC-MS data processed through both XCMS feature detection and RAMClustR clustering, and you need to verify the reliability of molecular weight assignments before downstream annotation or statistical analysis. Specifically, use it when you want to establish an empirical agreement baseline between two competing scoring algorithms on the same compound clusters, or when validating a new scoring method against an established reference.

## When NOT to use

- Input data is already fully annotated with high-confidence spectral library matches; scoring method validation is unnecessary if identity is already established.
- Negative or alternative ionization modes without mode parameter revalidation; the ~90% concordance is specific to positive ionization mode.
- Feature detection and clustering have not been completed; do.findmain requires a mature RC object as input and cannot be applied to raw LC-MS data.

## Inputs

- RC object (RAMClustR cluster object from prior XCMS and RAMClustR processing)
- High-resolution LC-MS feature intensity matrix aligned across samples
- Compound cluster assignments from RAMClustR

## Outputs

- Agreement fraction (percentage) between findMain and RAMClustR scoring
- Consensus molecular weight table (using higher value when methods disagree)
- Disagreement set with both scoring results for each discordant cluster
- Validation report against ~90% expected concordance threshold

## How to apply

Load or construct an RC (RAMClustR) object from prior XCMS feature detection and RAMClustR clustering. Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10 to infer molecular weights using the findMain scoring approach. Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster, calculating the fraction of compounds where the two methods agree within acceptable tolerance (essentially identical masses). When disagreement occurs, the higher of the two molecular weights should be returned as the consensus value. Report the agreement fraction as a percentage and validate against the expected ~90% concordance benchmark to assess whether the scoring methods are performing within typical specification.

## Related tools

- **XCMS** (Upstream feature detection and alignment; required to generate the feature matrix for RC object construction)
- **RAMClustR** (Clustering algorithm that groups features from the same compound and provides internal scoring method for molecular weight inference) — https://github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Source package from which the findMain function was adapted for molecular weight scoring)
- **R** (Runtime environment for executing do.findmain and agreement calculation functions)

## Examples

```
RC <- do.findmain(RC, mode='positive', mzabs.error=0.02, ppm.error=10); agreement_frac <- sum(RC$findmain_mz == RC$ramclustr_mz) / length(RC$findmain_mz); print(paste('Agreement:', round(agreement_frac*100, 1), '%'))
```

## Evaluation signals

- Agreement fraction ≥ ~90% validates that the two scoring methods are operating within expected concordance specification for positive ionization mode LC-MS data.
- All compound clusters in the RC object receive a consensus molecular weight assignment (no missing or null values in output table).
- Disagreement set is non-empty and systematic inspection shows disagreements are typically small mass differences within ppm.error=10 tolerance, not sporadic outliers.
- When do.findmain and RAMClustR scores disagree, the higher molecular weight is consistently selected in the consensus output, confirming the tiebreaker rule is applied.
- Molecular weight values from both methods fall within chemically plausible range for organic metabolites (typically 50–2000 Da for small-molecule LC-MS) and exhibit reasonable retention time–mass relationships.

## Limitations

- The ~90% concordance benchmark is empirically established for positive ionization mode only; concordance may differ significantly in negative ionization mode or with different instrument platforms (GC-MS, high-field orbitrap, etc.).
- Agreement depends on correct upstream feature detection and clustering; errors in XCMS feature picking or RAMClustR cluster assignment will propagate into scoring disagreements that do not reflect method differences.
- The mzabs.error=0.02 and ppm.error=10 parameters are context-specific; different mass accuracy specifications (e.g., lower-resolution instruments) may require parameter adjustment and alter concordance rates.
- No version control or changelog is documented for RAMClustR, so reproducibility across code versions is not guaranteed; pinning specific package versions is recommended for validation workflows.
- The skill only quantifies agreement; it does not determine which method is 'correct' when disagreement occurs. Validation against an orthogonal standard (e.g., authentic standards or high-confidence library matches) is needed to establish ground truth.

## Evidence

- [other] What is the empirical rate of agreement between findMain and RAMClustR scoring methods when inferring molecular weights from high-resolution LC-MS data in positive ionization mode?: "What is the empirical rate of agreement between findMain and RAMClustR scoring methods when inferring molecular weights from high-resolution LC-MS data in positive ionization mode?"
- [other] The findMain and RAMClustR scoring methods agree approximately 90% of the time when inferring molecular weight; when they disagree, the higher of the two molecular weights is returned.: "The findMain and RAMClustR scoring methods agree approximately 90% of the time when inferring molecular weight; when they disagree, the higher of the two molecular weights is returned."
- [other] Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10 to infer molecular weights: "Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10 to infer molecular weights using the findMain scoring approach."
- [other] Extract and compare molecular weight predictions from do.findmain against RAMClustR internal scoring results for each compound cluster: "Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster."
- [intro] In practice we find that the two scoring methods agree about 90% of the time.: "In practice we find that the two scoring methods agree about 90% of the time."
- [intro] RAMClustR was designed to group features designed from the same compound using an approach which is unsupervised, platform-agnosic, and devoid of curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [intro] We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package: "We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package"
- [readme] ramclustObj <- do.findmain(ramclustObj = ramclustObj): "ramclustObj <- do.findmain(ramclustObj = ramclustObj)"

---
name: molecular-weight-inference-comparison
description: Use when after RAMClustR clustering of XCMS-detected features and prior
  to final compound annotation, when you need to verify the robustness of molecular
  weight inference or when findMain and RAMClustR predictions are available for the
  same compound clusters and you want to assess concordance or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
  license_tier: restricted
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

# molecular-weight-inference-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate and reconcile molecular weight predictions from two independent scoring methods (findMain and RAMClustR) applied to high-resolution LC-MS metabolomics data in positive ionization mode. This skill quantifies agreement rate and resolves discordant predictions using a decision rule.

## When to use

After RAMClustR clustering of XCMS-detected features and prior to final compound annotation, when you need to verify the robustness of molecular weight inference or when findMain and RAMClustR predictions are available for the same compound clusters and you want to assess concordance or select the most conservative estimate.

## When NOT to use

- Input data is in negative ionization mode (do.findmain parameters are mode-specific; mode='negative' would be required instead)
- RC object has not yet been clustered by ramclustR function (molecular weight inference requires valid cluster assignments)
- Only one scoring method is available (comparison requires both findMain and RAMClustR predictions)

## Inputs

- RC object (RAMClustR cluster object from prior XCMS feature detection and ramclustR clustering)
- high-resolution LC-MS data in positive ionization mode with m/z and retention time features

## Outputs

- Reconciled molecular weight predictions (one per compound cluster)
- Agreement fraction (percentage of clusters where findMain and RAMClustR agree)
- Updated RC object with do.findmain molecular weight field populated

## How to apply

Execute the do.findmain function on an RC (RAMClustR) object with parameters mode='positive', mzabs.error=0.02 (absolute mass tolerance), and ppm.error=10 (parts-per-million tolerance) to generate findMain-derived molecular weights. Extract and compare findMain predictions against the internal RAMClustR scoring molecular weights for each compound cluster. Calculate the fraction of cluster centroids where the two methods agree (masses identical or within acceptable tolerance). For discordant predictions, apply the decision rule: return the higher of the two molecular weights. Report the agreement fraction as a percentage; validated benchmarks expect approximately 90% concordance. Use this comparison to flag anomalous clusters or build confidence in molecular weight assignments for downstream identification.

## Related tools

- **RAMClustR** (Feature clustering and internal molecular weight scoring; provides RC object and baseline predictions for comparison) — https://github.com/cbroeckl/RAMClustR
- **XCMS** (Upstream feature detection and alignment; produces the aligned feature matrix consumed by ramclustR)
- **InterpretMSSpectrum** (Source package from which do.findmain function was adapted; implements findMain scoring algorithm)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10); agreement_frac <- sum(RC$inchikey != "") / length(RC$inchikey)
```

## Evaluation signals

- Agreement fraction equals or approaches the ~90% benchmark reported in the literature
- No missing or null values in either the findMain or RAMClustR molecular weight fields for assigned clusters
- When methods disagree, the selected (higher) molecular weight is plausible within the m/z range of the detected features (m/z ≤ inferred MW + 2×proton mass for [M+H]+ ions)
- Reconciled molecular weights are consistent across multiple samples (low variance in assigned MW for the same compound cluster)
- Distribution of disagreement cases is unbiased across mass range (no systematic over- or under-prediction in high vs. low mass regions)

## Limitations

- Agreement rate of ~90% implies systematic disagreement in ~10% of cases; no method to distinguish which is correct without orthogonal reference (e.g. authentic standards or HR-MS/MS fragmentation rules)
- Parameters mzabs.error=0.02 and ppm.error=10 are empirically derived for high-resolution LC-MS in positive mode; tolerance must be recalibrated for different mass analyzers, ionization modes, or mass ranges
- Decision rule (return higher MW) is a pragmatic tiebreaker but may not always be correct; users should review high-confidence annotations independently for critical applications
- Performance depends on upstream XCMS feature detection quality and RAMClustR clustering success; poor clustering or missed isotopic features will degrade molecular weight inference before this comparison step occurs

## Evidence

- [intro] ~90% agreement benchmark and disagreement rule: "In practice we find that the two scoring methods agree about 90% of the time."
- [intro] findMain parameter specification for positive ionization: "RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)"
- [intro] Method of comparison workflow: "Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster."
- [intro] findMain source and integration: "We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package"
- [readme] Installation and stepwise workflow context from README: "ramclustObj <- do.findmain(ramclustObj = ramclustObj)"

---
name: positive-mode-ionization-analysis
description: Use when you have LC-MS metabolomics data in positive ionization mode
  and have already performed XCMS feature detection and RAMClustR clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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

# positive-mode-ionization-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply molecular weight inference on high-resolution LC-MS data acquired in positive ionization mode by executing the findMain scoring method within RAMClustR, then validate agreement with RAMClustR's internal scoring to ensure robust compound identification. This skill is critical for non-targeted metabolomics workflows where accurate mass assignment directly affects downstream annotation and biological interpretation.

## When to use

You have LC-MS metabolomics data in positive ionization mode and have already performed XCMS feature detection and RAMClustR clustering. You need to infer the most likely molecular weight for each compound cluster and want to benchmark the findMain scoring method (from InterpretMSSpectrum) against RAMClustR's internal scoring to identify cases of disagreement that may indicate ambiguous or poorly-resolved isotopic patterns.

## When NOT to use

- Input data were acquired in negative ionization mode (use mode='negative' parameter instead)
- Raw data have not yet been processed through XCMS feature detection and alignment
- RAMClustR clustering has not been executed on the XCMS object (do.findmain requires a populated RC object)

## Inputs

- RC object (RAMClustR object from prior clustering)
- High-resolution LC-MS feature table (positive ionization mode)
- XCMS xcmsSet or xcmsExperiment object

## Outputs

- RC object with populated findMain molecular weight assignments
- Comparison table of findMain vs. RAMClustR molecular weight scores
- Agreement fraction (percentage of concordant predictions)
- List of discordant cluster predictions for manual curation

## How to apply

Load or construct an RC (RAMClustR) object from prior XCMS feature detection and RAMClustR clustering. Execute the do.findmain function on the RC object with mode='positive', mzabs.error=0.02 (20 ppm absolute tolerance), and ppm.error=10 (10 ppm relative tolerance) to infer molecular weights using the findMain scoring approach. Extract and compare the molecular weight predictions from do.findmain against the RAMClustR internal scoring results for each compound cluster. Calculate the fraction of clusters where the two methods agree (essentially identical masses within tolerance). The expected agreement rate is approximately 90%; when methods disagree, return the higher of the two molecular weights as the more conservative estimate. Document any clusters with discordant predictions for manual review, as these may represent complex isotopic or adduction scenarios.

## Related tools

- **XCMS** (Feature detection and alignment from raw LC-MS chromatographic data; provides input feature table to RAMClustR)
- **RAMClustR** (Clusters XCMS features from the same compound using retention time and correlational similarity; holds internal molecular weight scoring used for comparison) — https://github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Source package for the findMain function, adapted for molecular weight inference within RAMClustR)
- **R** (Runtime environment for executing do.findmain and RC object manipulation)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10); agreement_rate <- mean(RC$findmain_mw == RC$ramclustr_mw, na.rm = TRUE); print(paste("Agreement:", round(agreement_rate * 100, 1), "%"))
```

## Evaluation signals

- Agreement fraction between findMain and RAMClustR scoring is approximately 90% (within ±5–10% tolerance); significantly lower agreement may indicate parameter miscalibration or poor cluster quality
- All compound clusters (RC$nfeat values) have been assigned a molecular weight; no NA or missing values in the findMain output column
- Discordant predictions cluster in specific m/z or retention time regions (suggesting systematic issues with isotopic or adduction patterns), not random across the dataset
- When disagreement occurs, the higher molecular weight is consistently selected and documented, and the difference is typically ≤ 0.02 Da (within the mzabs.error tolerance)
- RC object structure is preserved and all prior cluster annotations and sample abundance data remain intact after do.findmain execution

## Limitations

- The findMain and RAMClustR scoring methods agree ~90% of the time; 10% of predictions will show discordance, requiring manual inspection or orthogonal validation
- Performance depends on high mass accuracy (suitable for Orbitrap, Q-TOF, or equivalent instruments); low-resolution data may yield unreliable agreement rates
- findMain scoring assumes well-resolved isotopic patterns; overlapping or poorly-resolved clusters may not be correctly scored by either method
- No changelog is available for RAMClustR; version-to-version changes or breaking changes are undocumented, which may affect reproducibility across package updates

## Evidence

- [intro] XCMS is a commonly used tool to detect all the signals from a metabolomics dataset, generating aligned features: "XCMS is a commonly used tool to detect all the signals from a metabolomics dataset, generating aligned features"
- [intro] We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package: "We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package"
- [intro] In practice we find that the two scoring methods agree about 90% of the time.: "In practice we find that the two scoring methods agree about 90% of the time."
- [other] Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10: "Execute do.findmain function on the RC object with mode='positive', mzabs.error=0.02, and ppm.error=10 to infer molecular weights using the findMain scoring approach."
- [other] when they disagree, the higher of the two molecular weights is returned: "when they disagree, the higher of the two molecular weights is returned"
- [readme] ramclustObj <- do.findmain(ramclustObj = ramclustObj): "ramclustObj <- do.findmain(ramclustObj = ramclustObj)"
- [discussion] No changelog found.: "No changelog found — version history and breaking changes undocumented"

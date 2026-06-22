---
name: feature-quality-assessment-by-rsd-within-class
description: Use when after blank subtraction and background drift removal in an MS-DIAL peak list, when you need to exclude features with high within-class measurement variability. Apply this when you have replicate samples assigned to distinct classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-quality-assess-by-RSD-within-class

## Summary

Filter metabolomic features by calculating relative standard deviation (RSD) within each sample class and removing features that exceed a user-defined RSD threshold for their respective class. This step identifies and removes features with poor reproducibility in their assigned sample groupings before downstream clustering and annotation.

## When to use

After blank subtraction and background drift removal in an MS-DIAL peak list, when you need to exclude features with high within-class measurement variability. Apply this when you have replicate samples assigned to distinct classes (e.g., disease vs. control, treatment groups) and want to retain only reproducible features within each class.

## When NOT to use

- Input data contain fewer than 3 replicates per sample class — RSD calculation becomes unstable with very small sample sizes.
- Sample classes are not clearly defined or assigned in the MS-DIAL metadata — the filter cannot group intensities meaningfully.
- Data are from MS1-only acquisitions without MS/MS spectra — MS-CleanR discards all features without MS/MS in the first step.

## Inputs

- MS-DIAL peak list (feature table with m/z, retention time, intensity values, and sample class assignments)
- User-defined RSD threshold (percentage, e.g., 30%)
- Sample class labels (from MS-DIAL sample metadata)

## Outputs

- Filtered MS-DIAL peak list with features above RSD threshold removed
- Feature retention statistics (count and proportion of features removed by RSD filtering)

## How to apply

For each feature in the filtered MS-DIAL peak list, group its intensity values by the sample class assignment provided in the MS-DIAL sample metadata. Calculate the relative standard deviation (RSD = [standard deviation / mean intensity] × 100) separately for each class. Remove any feature whose RSD exceeds the user-specified threshold (e.g., RSD > 30%) in its assigned class. The rationale is that features with high within-class RSD are likely noise or highly variable background signals rather than robust metabolite signals, and their removal improves feature robustness for subsequent clustering and annotation steps.

## Related tools

- **MS-CleanR** (Primary implementation; wraps RSD-based filtering as tunable parameter within the generic filtering step applied to MS-DIAL peak lists) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Upstream tool that generates the peak list (feature table) and provides sample class metadata required for RSD grouping) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Verify that the number of features retained is less than or equal to the input count and matches the expected reduction from applying the RSD threshold.
- Confirm that all retained features have RSD values ≤ the specified threshold within their respective sample classes; spot-check a sample of removed features to confirm their RSD exceeds the threshold.
- Check that sample class labels are consistently applied across the input metadata and that no features are removed due to missing or ambiguous class assignments.
- Verify that the output feature table maintains m/z, retention time, and intensity columns intact, with only feature rows (not samples) removed.
- Compare class-wise RSD distributions (median, quartiles) before and after filtering to confirm high-variability features are preferentially removed.

## Limitations

- Requires at least 3 replicate samples per class (as stated in MS-CleanR README) for reliable RSD calculation; smaller sample groups may produce misleading estimates.
- RSD thresholds are user-defined and not automatically calibrated; threshold choice depends on instrument stability and experimental design, and no universal cutoff is provided in the article.
- Features with missing intensity values in some class members will produce biased RSD estimates; the article does not explicitly detail handling of missing data.
- RSD filtering is class-specific, so a feature may be retained in one class but filtered from another; downstream clustering may create inconsistent feature lists if classes are merged without careful harmonization.
- MS-CleanR actively discards all features without MS/MS spectra during this first generic filtering step, so MS1-only data will fail before RSD filtering is reached.

## Evidence

- [other] Calculate relative standard deviation (RSD) for each feature within each sample class and remove features exceeding the RSD threshold for their respective class.: "Calculate relative standard deviation (RSD) for each feature within each sample class and remove features exceeding the RSD threshold for their respective class."
- [readme] MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on sample class and relative mass defect (RMD) window filtering. All these options are tunable by the user.: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [readme] At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list.: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list."
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."

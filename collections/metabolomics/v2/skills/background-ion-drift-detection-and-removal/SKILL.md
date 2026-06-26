---
name: background-ion-drift-detection-and-removal
description: Use when processing MS-DIAL peak lists from untargeted LC-MS/MS experiments
  (DDA or DIA mode) where you suspect instrumental background contamination or ion
  source carry-over is generating false positive features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-ion-drift-detection-and-removal

## Summary

Detect and remove background ions that exhibit systematic signal intensity drift across an LC-MS analysis run, using retention time-based intensity profiles. This step eliminates spurious features arising from instrument contamination or carry-over that confound metabolite discovery in untargeted metabolomics.

## When to use

Apply this skill when processing MS-DIAL peak lists from untargeted LC-MS/MS experiments (DDA or DIA mode) where you suspect instrumental background contamination or ion source carry-over is generating false positive features. Specifically use it when retention time-dependent signal intensity patterns suggest non-biological feature drift across the analytical sequence.

## When NOT to use

- Input is already a fully annotated or curated metabolite set — background drift removal is a preprocessing step for raw peak lists only.
- Data consist of MS1 scans only (no MS/MS data) — MS-CleanR and this filter require data-dependent or data-independent MS/MS acquisition.
- Retention time information is missing or unreliable — drift detection depends on accurate RT ordering across the run.

## Inputs

- MS-DIAL peak list (feature table) with columns: m/z, retention time, intensity, sample identifiers
- Sample class assignments (study samples vs. blanks vs. QCs)

## Outputs

- Filtered MS-DIAL peak list with background drift features removed
- Feature intensity table ready for RSD/RMD filtering and clustering

## How to apply

After loading an MS-DIAL feature table (containing m/z, retention time, intensity, and sample assignments), examine the intensity profile of each feature across the retention time dimension of the analysis run. Identify features whose signal intensity systematically increases, decreases, or otherwise drifts over the course of the run in a manner inconsistent with true metabolites (which should have stable, sample-class-dependent intensity distributions). Remove such drifting features by filtering them from the peak list prior to downstream RSD/RMD thresholding and feature clustering. The tunable parameter is the drift detection threshold, which should be set based on your instrument's baseline contamination behavior and run length.

## Related tools

- **MS-DIAL** (Produces the initial peak list (feature table with m/z, RT, intensity) that serves as input to background drift detection) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Implements background ions drift removal as part of the generic filtering step; orchestrates the complete cleaning workflow) — https://github.com/eMetaboHUB/MS-CleanR

## Examples

```
library(mscleanr); runGUI()
```

## Evaluation signals

- Verify that removed features exhibit monotonic or strong systematic drift in intensity across retention time, while retained features show stable or sample-class-stratified intensity profiles.
- Check that the number of removed features is consistent with expected background contamination levels (typically 5–15% of raw features in clean runs).
- Confirm that downstream RSD/RMD filtering step receives a peak list with reduced spurious background noise, as reflected in fewer features failing quality thresholds.
- Validate that ion-specific drift removal does not eliminate genuine adducts or fragment ions belonging to true metabolites (cross-check with known internal standards or QC compounds).
- Ensure retention time distribution of retained features matches expected metabolite elution patterns and is not skewed toward early or late timepoints.

## Limitations

- Drift detection is sensitive to the quality and spacing of blank/QC samples throughout the run; at least 3 blanks are required for robust background characterization (per README).
- Cannot distinguish between instrumental background drift and genuine biological variability if samples are not properly randomized or if run order is confounded with sample class.
- Drift thresholds are user-tunable and not automatically optimized; poor threshold choice may retain contamination or discard real features with subtle RT-dependent intensity changes.
- The method relies on retention time-based intensity profiles and does not account for m/z-specific instrumental artifacts (e.g., space-charge effects in high-mass regions).
- Data must include MS/MS spectra (DDA or DIA mode); MS1-only data will cause the first MS-CleanR step (which includes this filter) to crash.

## Evidence

- [other] Remove background ions exhibiting systematic drift across the analysis run using retention time-based signal intensity profiles.: "Remove background ions exhibiting systematic drift across the analysis run using retention time-based signal intensity profiles."
- [readme] MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on sample class and relative mass defect (RMD) window filtering. All these options are tunable by the user.: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list.: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis."

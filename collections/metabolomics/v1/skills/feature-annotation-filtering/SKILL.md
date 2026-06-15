---
name: feature-annotation-filtering
description: Use when you have a feature list with assigned molecular formulas and m/z values from non-target HRMS analysis, and you need to identify and rank potential PFAS compounds among thousands of detected features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  - MSConvert
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
---

# MD/C-m/C prioritization filter for PFAS candidate features

## Summary

The MD/C-m/C approach filters and ranks potential per- and polyfluoroalkyl substance (PFAS) features from non-target high-resolution mass spectrometry data by normalizing mass defect to the number of carbon atoms, then applying a threshold criterion to flag PFAS candidates. This prioritization technique reduces false positives in feature lists generated from LC- or GC-HRMS raw data.

## When to use

Apply this skill when you have a feature list with assigned molecular formulas and m/z values from non-target HRMS analysis, and you need to identify and rank potential PFAS compounds among thousands of detected features. Use it as part of a multi-filter strategy alongside Kendrick mass defect analysis and MS2 fragment matching to narrow candidate space before suspect screening or MS2 spectral confirmation.

## When NOT to use

- Input feature list lacks assigned or suspect molecular formulas — the MD/C calculation requires a known elemental composition and cannot infer it from m/z alone.
- Data are from targeted screening or reference standard analysis where compound identity is already confirmed — prioritization filtering is unnecessary.
- Non-fluorinated organic compounds are the focus; MD/C filtering is optimized for fluorine-enriched PFAS and will not enrich other compound classes.

## Inputs

- Feature list (Excel .xlsx or equivalent) with columns: m/z (observed mass-to-charge), retention time, molecular formula (assigned or suspect-screened)
- Standard atomic mass table (built-in or user-supplied)

## Outputs

- Annotated feature list with MD/C scores for each feature
- Binary PFAS prioritization flags (yes/no or ranked list)
- Filtered feature list containing only features passing MD/C threshold
- Interactive HTML MD/C-m/C scatter plot (m/z vs. MD/C with highlights)

## How to apply

Load the feature list containing m/z values and corresponding molecular formulas (e.g., from pyOpenMS feature detection or an external .xlsx file). For each feature, calculate the exact mass from the assigned molecular formula using standard atomic masses, then compute mass defect as (observed m/z − exact mass). Divide the mass defect by the number of carbon atoms in the molecular formula to obtain the MD/C value. Apply a user-defined MD/C threshold criterion (typically tuned per analysis context) to flag features as potential PFAS. The rationale is that fluorine-rich PFAS compounds exhibit characteristic mass defects that normalize differently across carbon chain lengths; this ratio isolates features with the fluorine-enriched signature typical of PFAS. Output the filtered feature list with MD/C scores and binary PFAS prioritization flags, optionally ranked by MD/C value for downstream MS2 confirmation.

## Related tools

- **PFΔScreen** (GUI application that implements MD/C-m/C filtering, Kendrick mass defect analysis, and MS2 fragment matching; orchestrates feature detection via pyOpenMS and outputs annotated results tables and interactive plots) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Performs feature detection in raw HRMS data (mzML format) upstream of feature list generation and annotation)
- **MSConvert** (Converts vendor-specific raw mass spectrometry files to vendor-neutral mzML format for input to feature detection)

## Evaluation signals

- MD/C scores for known PFAS standards (e.g., PFOA, PFOS) should cluster within the threshold range; features outside the range should fail the filter.
- The filtered feature list should show a reduced cardinality (number of features) compared to the input list; the reduction ratio depends on threshold stringency and sample complexity.
- Features retained after filtering should exhibit coelution patterns in extracted ion chromatograms (EIC) and isotope patterns consistent with PFAS (e.g., fluorine-induced isotope shifts).
- Cross-validation: features passing the MD/C filter should also receive high prioritization scores from orthogonal methods (e.g., Kendrick mass defect or diagnostic MS2 fragments) to confirm the filter is not isolating false positives.
- Manual inspection of the interactive MD/C-m/C HTML plot should show expected feature distributions; suspicious outliers should be investigated for formula assignment errors or instrumental artifacts.

## Limitations

- The MD/C approach depends on accurate molecular formula assignment; errors in formula annotation will propagate to incorrect MD/C values and false prioritization.
- The optimal MD/C threshold is context-dependent (matrix, ionization mode, instrument tuning) and may require empirical calibration with standards or reference samples; no universal threshold is provided in the article.
- The method prioritizes features by fluorine-enriched mass defect but does not confirm identity; MS2 spectral data or authentic standards are required to confirm suspected PFAS hits.
- Isomeric or isobaric compounds with the same molecular formula cannot be distinguished by m/z and MD/C alone; additional retention time or spectral data is needed.
- PFAS with very few carbons or those lacking typical fluoroalkyl chains may not show characteristic MD/C values and could be missed by this filter.

## Evidence

- [other] Calculate mass defect (observed m/z minus exact mass) for each feature. Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value. Apply MD/C threshold criterion to flag features as potential PFAS.: "Calculate mass defect (observed m/z minus exact mass) for each feature. 3. Compute mass defect... 4. Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value. 5."
- [other] The MD/C-m/C approach is one of several prioritization techniques implemented in PFΔScreen for identifying potential PFAS features from non-target HRMS data, operating alongside Kendrick mass defect analysis and MS2 fragment analysis.: "The MD/C-m/C approach is one of several prioritization techniques implemented in PFΔScreen for identifying potential PFAS features from non-target HRMS data, operating alongside Kendrick mass defect"
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] To perform the PFASPrioritization, appropriate input parameters can be set, and then PFAS-specific data evaluation is performed with the 'Run PFASPrioritization' button. ... interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot: "To perform the PFASPrioritization, appropriate input parameters can be set, and then PFAS-specific data evaluation is performed with the 'Run PFASPrioritization' button... interactive HTML plots are"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."

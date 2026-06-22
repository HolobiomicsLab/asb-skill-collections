---
name: interference-profile-identification
description: Use when after running saturation repair or multidimensional smoothing on IM-MS data when you need to validate whether corrected peaks are reliable or whether overlapping coeluting/comobiling ions may have caused incorrect signal reconstruction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# interference-profile-identification

## Summary

Identify and diagnose highly convoluted elution and ion mobility profiles caused by spectral interferences in IM-MS data, which may compromise the accuracy of downstream signal reconstruction algorithms like saturation repair. This skill is essential for quality control of preprocessed IM-MS data to flag problematic ion signals before accepting computational corrections.

## When to use

Apply this skill after running saturation repair or multidimensional smoothing on IM-MS data when you need to validate whether corrected peaks are reliable or whether overlapping coeluting/comobiling ions may have caused incorrect signal reconstruction. Use it particularly when working with complex biological samples (proteomics, metabolomics) where matrix effects and structural isomer coelution are common.

## When NOT to use

- Input data is from a simple, well-separated standard or a low-complexity sample where coelution is unlikely.
- Saturation repair was not applied or is not part of the preprocessing pipeline; interference diagnosis is orthogonal to noise filtering alone.
- Data quality is already confirmed via orthogonal reference standards or prior LC-MS/MS validation of the same analytes.

## Inputs

- PNNL PreProcessor output logs (text)
- Raw Agilent MassHunter (.d) or UIMF IM-MS data file
- Preprocessed IM-MS data frame with m/z, drift time, retention time, and intensity dimensions

## Outputs

- Flagged ion list (m/z, CCS/drift time, retention time ranges with interference markers)
- Diagnostic report identifying ions with convoluted elution/mobility profiles
- Annotated region map (regions where saturation repair may have produced incorrect results)

## How to apply

Load preprocessed IM-MS output logs and examine them for warnings flagged during saturation repair execution. Search logs for signals exhibiting convoluted elution/mobility profiles — these are ions with complex, multimodal intensity distributions across retention time and drift time dimensions that may be caused by coeluting species or isomers. Cross-reference flagged m/z, mobility, and retention time ranges against the raw data using the IM-MS Browser or similar visualization tool. If an ion's signal profile shows multiple peaks or asymmetric distortion across the mobility and RT dimensions, and saturation repair was applied to that region, treat the repaired signal with caution and consider manual inspection or exclusion from quantification. The rationale is that saturation repair software assumes unimodal, well-resolved peak shapes; violations of this assumption lead to incorrect peak reconstruction.

## Related tools

- **PNNL PreProcessor** (Generates preprocessed IM-MS data and output logs containing saturation repair warnings and metadata; reads raw .d and UIMF files) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **IM-MS Browser** (Visualizes and manually inspects ion mobility, retention time, and m/z distributions to confirm convoluted peak profiles flagged by logs)
- **Agilent MassHunter** (Source instrument software; provides raw .d data files that serve as input for PNNL PreProcessor and can be opened for secondary visualization)

## Evaluation signals

- Output logs contain explicit warnings about 'convoluted elution/mobility profiles' for specific m/z and retention time windows; log entries are parsed and flagged ions match independent visual inspection in IM-MS Browser.
- Flagged ions show multimodal or heavily tailed intensity distributions across drift time and retention time dimensions in the raw data; unflagged ions exhibit symmetric, unimodal profiles.
- Saturation repair corrections for flagged regions are validated against a reference standard or orthogonal LC-MS/MS data; corrected peaks diverge from reference values (e.g., >20% intensity error, altered peak centroid).
- Reproducibility check: re-running PNNL PreProcessor on the same raw file with identical settings produces consistent interference flags; flags appear in the same m/z and retention time ranges.
- Quantification sensitivity: quantitative results (peak area, intensity) for flagged vs. unflagged ions differ significantly when saturation repair is toggled on/off; flagged ions show larger divergence, indicating unstable reconstruction.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, but the tool does not automatically distinguish between true coelution and instrumental artifacts; manual inspection is required.
- The identification depends on log output from PNNL PreProcessor; silent failures or warnings suppressed by user settings will not be captured.
- Interference profiles caused by structural isomers or isobars may be indistinguishable from true coelution without tandem MS or chemical derivatization validation.
- No quantitative threshold for 'convoluted' is defined in the literature; diagnosis relies on qualitative log inspection and visual assessment.

## Evidence

- [methods] Saturation repair software may produce incorrect results: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [other] Verify repair success by checking output logs for warnings: "Verify repair success by checking output logs for warnings about convoluted elution/mobility profiles that may have caused incorrect repairs."
- [other] Multidimensional smoothing and saturation repair algorithm: "Apply multidimensional smoothing and saturation repair algorithm to detect and reconstruct saturated peaks across the m/z, mobility, and retention time dimensions."
- [methods] Smoothing removes artifacts in jagged peaks: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions."
- [readme] IM-MS preprocessing pipeline capabilities: "multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"

---
name: md-defect-ratio-calculation
description: Use when you have a feature table from LC- or GC-HRMS data (either detected
  via pyOpenMS or imported as a custom feature list) containing m/z, retention time,
  and intensity values, and you want to rapidly filter to candidate PFAS features
  that exhibit the elevated mass defects typical of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pyOpenMS
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MD/C-m/C Ratio Calculation for PFAS Feature Prioritization

## Summary

Calculate the mass defect (MD) to molecular ion abundance ratio (C-m/C) for each detected feature to identify PFAS-like compounds with elevated mass defects characteristic of perfluorinated structures. This ratio-based filtering step prioritizes features most likely to be PFAS before more computationally intensive downstream analysis.

## When to use

Apply this skill when you have a feature table from LC- or GC-HRMS data (either detected via pyOpenMS or imported as a custom feature list) containing m/z, retention time, and intensity values, and you want to rapidly filter to candidate PFAS features that exhibit the elevated mass defects typical of perfluorinated compounds. Use this as the first prioritization gate to reduce the search space before Kendrick mass defect clustering or MS2 fragment matching.

## When NOT to use

- Input is a pre-filtered or suspect list of known PFAS compounds — this skill is a discovery/prioritization step, not a validation step.
- Raw MS data lacks centroided spectra or is not in mzML format — mass defect calculation requires accurate monoisotopic peak detection.
- Non-targeted features from non-fluorinated or weakly fluorinated analyte classes dominate — the MD/C-m/C ratio is specific to perfluorinated compounds and will misclassify other lipophilic species.

## Inputs

- Feature table (CSV, TSV, or Excel) with columns: m/z, retention time (RT), intensity
- Optional: Raw mzML file(s) for peak intensity extraction if custom feature list lacks abundance data
- User-specified MD/C-m/C threshold parameter (e.g., minimum ratio to retain feature)

## Outputs

- Filtered feature table with MD/C-m/C ratio annotations for each feature
- Subset of features passing the MD/C-m/C threshold, ranked by ratio magnitude
- MD/C-m/C scatter plot (interactive HTML) for visual inspection of feature distribution and threshold cutoff

## How to apply

For each feature in the input table, calculate the mass defect (MD) as the difference between the exact monoisotopic mass and the integer nominal mass (e.g., m/z 537.9735 has MD = 0.9735). Then compute the ratio C-m/C, where C is the intensity (abundance) of the molecular ion peak and m is the intensity of the corresponding monoisotopic peak, normalizing abundance information into the ratio. Features with elevated MD/C-m/C ratios are characteristic of PFAS and are flagged for retention; features below a user-specified threshold are deprioritized. The rationale is that perfluorinated chains accumulate mass defect from multiple fluorine atoms (each contributing negative mass defect), making this ratio a rapid chemical fingerprint for structural class filtering.

## Related tools

- **pyOpenMS** (Feature detection and intensity extraction from raw mzML data prior to MD/C-m/C calculation)
- **PFΔScreen** (Integrated platform implementing MD/C-m/C prioritization alongside KMD analysis and MS2 fragment matching; provides GUI and automated workflow for ratio calculation and filtering) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- All features in the output table have valid m/z and calculated mass defect values (non-null, within physical mass range ~–0.5 to +0.5 Da for organic compounds).
- MD/C-m/C ratio values are consistently higher for known PFAS standards or curated PFAS features compared to non-fluorinated background features (evidence of chemical selectivity).
- Threshold cutoff visually separates a dense cluster of candidate PFAS features from background noise in the MD/C-m/C distribution plot, with clear inflection point or bimodality.
- Cross-validation: features passing MD/C-m/C filter are confirmed by downstream Kendrick mass defect clustering and MS2 diagnostic fragment matching (consistency across orthogonal prioritization methods).

## Limitations

- MD/C-m/C ratio depends on accurate intensity measurements; weak or poorly resolved monoisotopic peaks in low-abundance features may yield unreliable ratios.
- The approach assumes perfluorinated structure; partially fluorinated or non-fluorinated compounds with similar molecular weight or polarity may co-elute and exhibit spuriously elevated mass defects (false positives).
- Threshold selection is user-dependent; no universal cutoff is provided in the article or README. Optimal threshold may vary by sample type, instrument, and ionization mode (ESI vs. APCI).
- Does not account for natural stable isotope composition; features with unusual isotope patterns (e.g., high bromine content) may confound mass defect calculation.

## Evidence

- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences"
- [other] Apply MD/C-m/C ratio filtering to identify PFAS-like features with elevated mass defects: "Apply MD/C-m/C ratio filtering to identify PFAS-like features with elevated mass defects."
- [intro] Optionally, custom feature lists can be included and applies prioritization techniques including MD/C-m/C approach: "Optionally, custom feature lists can be included. 2. Parse feature metadata and convert to internal PFΔScreen feature object format compatible with downstream prioritization modules. 3. Apply"
- [readme] The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
- [readme] a MD/C-m/C plot [is saved along with] several interactive HTML plots: "Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected. After executing the"

---
name: high-resolution-mass-spectrometry-interpretation
description: Use when you have centroided LC- or GC-HRMS data (in mzML format, ideally from data-dependent acquisition) and need to identify potential PFAS candidates from a large feature list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# High-Resolution Mass Spectrometry Interpretation

## Summary

Interpret LC- or GC-HRMS data to prioritize potential PFAS features using complementary mass-defect filtering, Kendrick analysis, and MS2 fragment matching. This skill combines multiple prioritization techniques to rank candidate features in non-target screening workflows, enabling efficient identification of perfluorinated and polyfluorinated compounds from vendor-neutral mzML spectral data.

## When to use

Apply this skill when you have centroided LC- or GC-HRMS data (in mzML format, ideally from data-dependent acquisition) and need to identify potential PFAS candidates from a large feature list. Use it when baseline screening requires ranking many features by likelihood of being true PFAS rather than false positives or structurally unrelated compounds. Specifically, use it when you have MS1 m/z values with assigned molecular formulas and corresponding MS2 spectra, and need to apply chemical intelligence (fluorine-rich mass patterns, known PFAS diagnostic fragments) to filter a non-target feature set.

## When NOT to use

- Data is already a curated suspect list or confirmed compound library—use targeted screening instead.
- MS data lacks MS2 spectra or was acquired in full-scan mode without data-dependent MS/MS—MD/C-m/C filtering can proceed, but fragment-based prioritization will be unavailable.
- Input format is not mzML or vendor raw format (incompatible with pyOpenMS)—convert via MSConvert first or use custom feature import path.
- The goal is quantification or peak-area integration rather than feature discovery and ranking.

## Inputs

- mzML file(s) from LC- or GC-HRMS with data-dependent MS2 acquisition (centroided spectra)
- Optional: custom feature list (Excel format) with m/z, retention time, and assigned molecular formulas
- Optional: blank control mzML file for subtraction

## Outputs

- PFASPrioritization results table (Excel format) with MD/C scores, m/C values, KMD scores, diagnostic fragment matches, and PFAS ranking flags
- Interactive HTML plots: MD/C-m/C scatter plot, m/z vs. retention time (with/without MS2 overlay), KMD vs. m/z linked plot, m/C histogram
- Annotated MS2 spectra with highlighted fragment mass differences and diagnostic fragments

## How to apply

Load mzML file(s) and optional custom feature list into PFΔScreen. Run feature detection via pyOpenMS or import pre-computed features (m/z, retention time, molecular formula assignments). Apply three complementary filters in sequence: (1) MD/C-m/C approach—calculate exact mass from molecular formula, compute mass defect (observed m/z minus theoretical), divide by carbon count, and flag features where MD/C falls within characteristic PFAS ranges; (2) Kendrick mass defect (KMD) analysis to identify repeating unit patterns typical of homologous PFAS series; (3) MS2 fragment mass differences and diagnostic fragment matching (e.g., CF3⁻, SO3⁻) against known PFAS fragmentation patterns. Apply user-specified thresholds for each filter, then combine scores into a prioritization rank. Perform optional blank correction by comparing sample/blank feature intensities. Output ranked feature table and interactive HTML visualizations (MD/C-m/C scatter plot, KMD vs. m/z, m/C histogram, m/z vs. RT map) for manual review and evidence assessment.

## Related tools

- **pyOpenMS** (Feature detection engine; Python interface to OpenMS C++ library for extracting features (m/z, RT, intensity) from raw mzML spectra) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Underlying C++ mass spectrometry data processing library providing feature finding, alignment, and MS2 spectral annotation) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Format conversion utility to generate vendor-independent mzML files from raw mass spectrometry data)
- **PFΔScreen** (Complete HRMS interpretation toolkit integrating MD/C-m/C, KMD, and MS2 fragment analysis with GUI for PFAS prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- MD/C values fall within expected ranges for fluorinated compounds (typically higher than non-fluorinated organic features); distribution should show multimodal peaks at known PFAS MD/C thresholds.
- Known PFAS reference compounds (if spiked or in control samples) are ranked in top percentile of prioritization output; negative controls show minimal or no high-priority flags.
- Kendrick mass defect plot shows clear horizontal alignments or linear chains characteristic of PFAS homolog series; RT coelution confirmed via linked m/z vs. RT visualization.
- MS2 spectra for top-ranked features contain diagnostic fragments (CF₃⁻, CF₂⁻, SO₃⁻, SO₂⁻, or characteristic loss patterns) consistent with documented PFAS fragmentation.
- Sample/blank intensity ratio >3 for flagged features (after blank subtraction), confirming features are sample-derived rather than contaminant or background.
- Output feature count and ranking distribution is consistent with expected PFAS abundance and structural diversity for the sample type (e.g., aqueous film-forming foam vs. industrial wastewater).

## Limitations

- MD/C-m/C filtering assumes correct molecular formula assignment; errors in elemental composition (charge, ionization adduct, isotope confusion) propagate through mass defect calculation and may cause true PFAS to be missed or false positives to be inflated.
- Kendrick mass defect analysis relies on detecting repeating units (typically CF₂ or CF₂SO₂); cyclic or highly substituted PFAS with irregular patterns may show weak or fragmented signals in KMD space.
- MS2 fragment diagnostic matching requires prior knowledge of PFAS fragmentation patterns; novel or degradation products without canonical diagnostic fragments may rank lower despite being PFAS-related.
- Blank correction assumes blank samples are representative of method background; matrix suppression or sample-specific contamination may not be fully removed.
- Tool is optimized for ESI or APCI ionization; compatibility with other ionization modes (MALDI, APPI) is not explicitly documented.
- Runtime performance (stated as <1 minute for 4000 spectra per sample) assumes moderate feature counts; very large feature lists (>10,000 features) may exceed usability expectations or memory constraints.

## Evidence

- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [other] The MD/C approach calculates mass defect divided by carbon atoms to yield a PFAS-diagnostic value: "Compute mass defect (observed m/z minus exact mass) for each feature. Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value."
- [readme] Feature detection uses pyOpenMS and mzML input format is required: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data. Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent"
- [readme] Data-dependent acquisition with centroided spectra and single collision energy per precursor is the recommended format: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
- [readme] Output includes interactive HTML visualizations and results table for manual review: "the PFΔScreen results table (Excel format) and several interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot, a m/z vs. RT plot"
- [readme] Short runtime enables convenient parameter adjustment: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
- [readme] Custom feature lists can be imported as an alternative to pyOpenMS feature detection: "In case another feature finding procedure (e.g., from vendor software) is desired, custom feature lists (see external_feature_list.xlsx) together with the respective mzML files can instead be"
- [readme] Blank correction is performed during feature finding: "The parameters for feature finding, MS2 alignment and blank correction can be specified and executed by pressing the "Run FeatureFinding" button."

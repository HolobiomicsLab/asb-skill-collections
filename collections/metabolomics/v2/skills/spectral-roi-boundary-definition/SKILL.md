---
name: spectral-roi-boundary-definition
description: Use when when you have identified a spectral window of interest in a
  1H NMR spectrum from a complex biological sample (serum, urine, CSF, tissue, saliva,
  or sweat) and need to systematically retrieve all metabolites from HMDB whose reference
  proton NMR chemical shifts fall within that window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - pandas
  - openpyxl
  - XlsxWriter
  - ROIAL-NMR
  - openpyxl / XlsxWriter
  - Human Metabolome Database (HMDB)
  - PyQt5
  techniques:
  - LC-MS
  - NMR
  license_tier: open
derived_from:
- doi: 10.1002/nbm.70131
  title: ROIAL-NMR
evidence_spans:
- pandas 2.2.3
- openpyxl 3.1.5
- XlsxWriter 3.2.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_roial_nmr_cq
    doi: 10.1002/nbm.70131
    title: ROIAL-NMR
  dedup_kept_from: coll_roial_nmr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/nbm.70131
  all_source_dois:
  - 10.1002/nbm.70131
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-roi-boundary-definition

## Summary

Define chemical-shift boundaries (lower and upper ppm limits) for proton NMR regions-of-interest (ROIs) to constrain metabolite candidate matching against reference spectral databases. This skill is essential for converting unstructured spectral observations into queryable interval parameters that ROIAL-NMR uses to filter and identify matching metabolites.

## When to use

When you have identified a spectral window of interest in a 1H NMR spectrum from a complex biological sample (serum, urine, CSF, tissue, saliva, or sweat) and need to systematically retrieve all metabolites from HMDB whose reference proton NMR chemical shifts fall within that window. This is typically done after visual inspection or peak-picking of the spectrum but before running metabolite identification queries.

## When NOT to use

- You already possess a pre-identified list of metabolites and do not need to query the database by spectral region.
- Your spectral data is from a non-standard 1H NMR platform (e.g., low-field benchtop NMR with poor chemical-shift resolution) where ppm calibration or reference-to-sample shift matching is unreliable.
- You do not have access to the HMDB or an equivalent reference database with assigned proton NMR chemical shifts for metabolites of interest.

## Inputs

- 1H NMR spectrum (raw FID or processed spectrum, from complex biological sample)
- Visual or algorithmic peak identification (chemical shift value in ppm)
- ROI bounds: lower_ppm and upper_ppm (floats, typically 0–12 ppm range for 1H NMR)
- Trend designation ('+' or '−')
- Significance level ('*' or '!')
- Sample type (human serum, saliva, sweat, urine, CSF, or tissue)

## Outputs

- ROI parameter record (lower_ppm, upper_ppm, trend, significance, sample_type)
- Candidate metabolite table (metabolite name, HMDB ID, matched shift values, functional group assignments)
- CSV or Excel export of matched metabolites with match ratios and concentration ranges

## How to apply

Record the lower and upper proton NMR chemical-shift limits (in ppm) that define your ROI window. These bounds are parsed by ROIAL-NMR to filter the HMDB reference database using interval matching—only metabolites whose assigned 1H NMR shifts fall within [lower_ppm, upper_ppm] are retained as candidates. The skill also requires specifying a trend annotation ('+' for increase, '−' for decrease) and significance level ('*' for Level 1, '!' for Level 2) if the ROI corresponds to a biomarker observation. Store these parameters in the analysis template following the ROIAL-NMR GUI workflow. The quality of candidate identification depends critically on the tightness and accuracy of the ROI bounds; overlapping or overly broad windows will inflate false-positive candidates, while overly narrow windows may exclude true metabolites due to reference-to-sample shift variation.

## Related tools

- **ROIAL-NMR** (Main application that executes ROI-to-HMDB candidate matching and metabolite filtering using the supplied spectral-roi-boundary parameters.) — github.com/Leo-Cheng-Lab/ROIAL-NMR
- **pandas** (Data structure and filtering library used to store and filter HMDB metabolite entries by chemical-shift interval matching.)
- **openpyxl / XlsxWriter** (Excel export libraries for writing candidate-metabolite results tables to structured spreadsheets.)
- **Human Metabolome Database (HMDB)** (Reference metabolite spectral database queried via ROI bounds to retrieve candidates with assigned 1H NMR chemical shifts.)
- **PyQt5** (GUI framework that provides the ROIAL-NMR interface for entering ROI bounds and other analysis parameters.)

## Examples

```
python main.py  # Then in GUI: input lower_ppm=1.2, upper_ppm=1.8, trend='+', significance='*', sample_type='urine' to define ROI and retrieve candidate metabolites.
```

## Evaluation signals

- ROI bounds are numeric, valid (lower_ppm < upper_ppm), and fall within the 1H NMR chemical-shift scale (typically 0–12 ppm).
- Candidate metabolite list returned contains only entries whose reference 1H NMR shifts overlap the defined ROI window; spot-check 5–10 entries to confirm shift values fall within [lower_ppm, upper_ppm].
- Match ratio and shift-assignment columns are populated for all returned metabolites, with no null or malformed entries.
- Exported CSV/Excel file can be opened and parsed without corruption; row count and column structure match the expected schema (metabolite name, HMDB ID, matched shifts, functional group context, concentration ranges).
- Rerunning the same ROI bounds on the same HMDB snapshot yields identical candidate lists (reproducibility check).

## Limitations

- ROI boundary accuracy depends on proper 1H NMR chemical-shift referencing (typically tetramethylsilane or internal standard); miscalibrated spectra will produce mismatched candidates.
- HMDB reference 1H NMR shifts are typically assigned in standardized conditions (solvent, pH, temperature); shifts in non-standard sample conditions (e.g., extreme pH, high ionic strength) may not align with reference values, inflating false negatives.
- Overlapping metabolite shifts in a crowded ROI may lead to ambiguous assignment without additional orthogonal data (e.g., 2D NMR, MS/MS integration).
- The README states 'No changelog found', indicating version stability and reproducibility guarantees are not documented; future HMDB updates may alter candidate sets for the same ROI bounds.
- Combining analyses (compare-two-groups workflow) requires both groups to have completed ROI definition and metabolite matching; incomplete or misaligned ROI windows across groups will compromise comparison validity.

## Evidence

- [other] Parse the user-supplied ROI bounds (lower and upper chemical-shift limits in ppm).: "Parse the user-supplied ROI bounds (lower and upper chemical-shift limits in ppm)."
- [other] Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching.: "Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching."
- [readme] ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum, saliva, sweat, urine, CSF, and tissues) using the Human Metabolome Database (HMDB) as a reference platform.: "ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum,"
- [readme] Follow the existing analysis template to input ROIs, trends, and significance levels: Use "+" for increase and "-" for decrease. Use "*" for Significance Level 1 and "!" for Significance Level 2.: "Follow the existing analysis template to input ROIs, trends, and significance levels: Use "+" for increase and "-" for decrease."
- [other] Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available).: "Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available)."

---
name: hmdb-metabolite-query-and-retrieval
description: Use when you have identified one or more proton NMR spectral regions-of-interest (ROIs)—defined by lower and upper chemical-shift bounds in ppm—from complex biological samples (serum, saliva, urine, tissue, CSF) and need to generate a ranked list of plausible metabolite identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - openpyxl
  - XlsxWriter
  - Human Metabolome Database (HMDB)
  - ROIAL-NMR
derived_from:
- doi: 10.1002/nbm.70131
  title: ROIAL-NMR
evidence_spans:
- pandas 2.2.3
- openpyxl 3.1.5
- XlsxWriter 3.2.2
- using the Human Metabolome Database (HMDB) as a reference platform
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
---

# HMDB-metabolite-query-and-retrieval

## Summary

Query the Human Metabolome Database (HMDB) to systematically retrieve candidate metabolites whose reference proton NMR chemical shifts fall within user-defined spectral regions-of-interest (ROIs). This skill enables annotation of NMR signals from complex biological samples by interval-matching observed chemical-shift windows against HMDB reference data.

## When to use

Apply this skill when you have identified one or more proton NMR spectral regions-of-interest (ROIs)—defined by lower and upper chemical-shift bounds in ppm—from complex biological samples (serum, saliva, urine, tissue, CSF) and need to generate a ranked list of plausible metabolite identities. Use it as the first filtering step to narrow down candidate metabolites before further MS/MS validation or quantification.

## When NOT to use

- ROI bounds are not clearly defined or span an unreasonably wide chemical-shift window (e.g., >5 ppm); interval matching will return too many false positives.
- HMDB reference data for the sample type (e.g., CSF metabolites) is incomplete or absent; candidate lists will lack coverage.
- Input spectral data is already fully annotated with metabolite identities from orthogonal methods (e.g., GC-MS, LC-MS/MS); further HMDB querying is redundant.

## Inputs

- HMDB reference database (metabolite entries with assigned proton NMR chemical shifts)
- ROI specification: tuple of (lower_ppm_bound, upper_ppm_bound) defining the spectral window
- Sample type identifier (e.g., human serum, saliva, urine, CSF, tissue)

## Outputs

- Candidate metabolite table (CSV or Excel) with columns: metabolite name, HMDB ID, matched 1H NMR shift values, functional-group assignments, concentration ranges
- Filtered metabolite dataset indexed by ROI

## How to apply

Load the HMDB reference database and extract all metabolite entries with assigned proton NMR chemical shifts. Parse the user-supplied ROI bounds (chemical-shift window in ppm). Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching. Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and functional-group context. Export the candidate-metabolite table to CSV or Excel format for downstream review and manual curation of abbreviations and match ratios.

## Related tools

- **ROIAL-NMR** (End-to-end NMR-based metabolite identification platform that encapsulates HMDB querying, ROI parameter setting, and GUI-driven result visualization and export) — github.com/Leo-Cheng-Lab/ROIAL-NMR
- **pandas** (DataFrame construction, filtering, and interval matching operations for metabolite dataset queries)
- **openpyxl** (Reading and writing Excel-format metabolite reference tables and output candidate lists)
- **XlsxWriter** (Programmatic export of filtered candidate-metabolite tables to Excel format with formatting)
- **Human Metabolome Database (HMDB)** (Reference repository of metabolite structures, chemical shifts, and biological sample context)

## Evaluation signals

- All returned metabolites have reference 1H NMR chemical shifts strictly within the ROI bounds; no shift values fall outside the specified ppm window.
- Candidate table is non-empty and contains metabolites biologically plausible for the stated sample type (e.g., serum vs. CSF).
- Matched shift values in the output table are accompanied by functional-group context (e.g., 'aromatic H', 'methyl group') that aids manual interpretation.
- Export file is valid CSV or Excel with expected column headers (metabolite name, HMDB ID, matched shifts, concentration ranges) and row count matches the number of filtered metabolites.
- User can modify or add abbreviations in the 'All Metabolites' window without data loss, confirming that results are editable and traceable back to HMDB entries.

## Limitations

- HMDB reference 1H NMR shift data may be incomplete or represent only one solvent/pH condition; observed shifts in complex samples may deviate from reference values due to pH, ionic strength, or protein binding.
- Overlapping ROIs or very narrow windows (< 0.1 ppm) can result in no candidates or excessive sensitivity to small shift perturbations; user must balance specificity against coverage.
- No changelog documented for ROIAL-NMR or HMDB version tracking, making it difficult to reproduce results if database entries are updated or deprecated.
- Interval matching alone does not account for multiplet splitting patterns, J-coupling, or 2D NMR correlation; manual validation against experimental COSY/HSQC is recommended before reporting final identifications.

## Evidence

- [other] ROIAL-NMR operates by querying the Human Metabolome Database (HMDB) as a reference platform to systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs).: "querying the Human Metabolome Database (HMDB) as a reference platform to systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs)"
- [other] Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching.: "Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching"
- [other] Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available).: "Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available)"
- [readme] After setting parameters and completing the calculation, open the 'All Metabolites' window. Here, you can view identified metabolites along with their abbreviations, match ratios, matched regions, and concentration ranges. Users can modify or add abbreviations as needed.: "you can view identified metabolites along with their abbreviations, match ratios, matched regions, and concentration ranges. Users can modify or add abbreviations as needed"
- [readme] ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum, saliva, sweat, urine, CSF, and tissues) using the Human Metabolome Database (HMDB) as a reference platform.: "ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum,"

---
name: nmr-chemical-shift-interval-matching
description: Use when you have isolated one or more regions-of-interest (ROIs) from a proton NMR spectrum (defined as lower and upper chemical-shift bounds in ppm) and need to systematically generate a list of plausible metabolite assignments from a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0634
  tools:
  - pandas
  - openpyxl
  - XlsxWriter
  - Python
  - PyQt5
  - Human Metabolome Database (HMDB)
  techniques:
  - tandem-MS
  - NMR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-chemical-shift-interval-matching

## Summary

A systematic workflow to identify candidate metabolites by matching user-defined proton NMR chemical-shift windows (ROIs, in ppm) against reference 1H NMR shifts in the Human Metabolome Database (HMDB). Outputs a ranked candidate list with metabolite names, HMDB IDs, matched shift values, and functional-group assignments to support targeted metabolite annotation in complex biological samples.

## When to use

You have isolated one or more regions-of-interest (ROIs) from a proton NMR spectrum (defined as lower and upper chemical-shift bounds in ppm) and need to systematically generate a list of plausible metabolite assignments from a reference database. Use this skill when manual spectral assignment is impractical or when you require a reproducible, queryable candidate list ranked by shift overlap with HMDB entries.

## When NOT to use

- Input is a raw NMR spectrum file or raw FID data — this skill assumes ROIs have already been manually or computationally defined; use peak-picking or ROI-extraction tools first.
- HMDB reference database is unavailable or out of date — the skill relies on complete, accurate HMDB shift annotations; local or custom metabolite databases are not supported without code modification.
- ROI bounds are not in ppm units or are not numeric — the interval-matching algorithm requires valid chemical-shift intervals; ambiguous or non-numeric inputs will fail silently or produce empty candidate lists.

## Inputs

- ROI definitions: user-supplied pairs of chemical-shift bounds (lower_ppm, upper_ppm)
- Human Metabolome Database (HMDB): reference metabolite entries with annotated 1H NMR chemical shifts
- Sample type designation (e.g., human serum, urine, CSF, tissue) — optional, for filtering HMDB subsets

## Outputs

- Candidate metabolite table (CSV or Excel): columns for metabolite name, HMDB ID, matched 1H NMR shift values, functional-group assignments, and shift match ratios
- Abbreviated metabolite names and modified abbreviations (user-editable in 'All Metabolites' window)
- Concentration ranges and biological context (extracted from HMDB)

## How to apply

Load the HMDB reference database and extract all metabolite entries annotated with proton NMR chemical shifts. Parse the user-supplied ROI bounds (ppm lower and upper limits). Filter the HMDB dataset by interval matching: retain only entries whose reference 1H NMR shifts fall within the specified ROI window. Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and functional-group context (if available in HMDB). The rationale is that metabolites with reference shifts overlapping the ROI are candidates for the observed signal; the interval-matching approach ensures reproducibility and enables batch processing of multiple ROIs. Export results to CSV or Excel format for downstream analysis (e.g., cross-validation with other modalities, concentration annotation, or disease-association lookup).

## Related tools

- **Python** (Runtime environment (≥3.9) for executing interval-matching queries and data wrangling) — https://www.anaconda.com/download/
- **pandas** (DataFrame filtering and interval matching; query HMDB entries by shift ranges)
- **openpyxl** (Read and parse Excel-based ROI input files and metabolite abbreviation annotations)
- **XlsxWriter** (Export candidate metabolite results to formatted Excel workbooks with match-ratio and shift-value columns)
- **PyQt5** (GUI components for ROI input, parameter setting, and interactive browsing of 'All Metabolites' and 'Result Show' windows)
- **Human Metabolome Database (HMDB)** (Reference platform of metabolite entries with annotated proton NMR chemical shifts, used for interval matching and candidate generation)

## Examples

```
python main.py
```

## Evaluation signals

- All matched metabolites have 1H NMR reference shifts that fall strictly within the user-supplied ROI bounds (lower_ppm ≤ matched_shift ≤ upper_ppm); no out-of-bounds entries in the results table.
- Match ratio column (percentage of metabolite's shifts or peak count overlapping the ROI) is non-empty and consistent with the number of matched shift values; enables ranking of candidates by overlap quality.
- Metabolite names and HMDB IDs are valid, non-duplicated entries from the current HMDB version; spot-check a subset against HMDB web interface.
- Output file schema matches the documented columns (metabolite name, HMDB ID, matched shifts, functional-group context, concentration range); verify column headers and row count align with input ROI count and expected candidate density.
- User-modified abbreviations in the 'All Metabolites' window persist in the final 'Result Show' table and are saved to the 'dataResult' export file; confirms end-to-end tracking of curation.

## Limitations

- HMDB shift assignments are static snapshots; real biological samples may exhibit pH-, solvent-, or temperature-dependent chemical-shift variations that diverge from the database reference. Consider applying a chemical-shift tolerance window (e.g., ±0.1 ppm) to account for instrumental and matrix effects.
- Interval matching returns all metabolites with overlapping shifts regardless of relative abundance or biological plausibility in the sample type; users must perform manual or statistical filtering to prioritize candidates (e.g., by disease association, tissue expression, or combined modalities).
- HMDB entries may be incomplete, outdated, or missing for rare or novel metabolites; the candidate list is bounded by HMDB coverage and curation quality.
- No changelog or version tracking is documented; users cannot easily assess whether HMDB updates or tool changes affect reproducibility of prior analyses.
- The skill does not integrate 2D NMR, coupling constants (J), or multiplicity; 1D proton chemical shift alone is insufficient to confirm metabolite identity in complex mixtures — combination with other modalities (COSY, HSQC, MS/MS) is recommended for validation.

## Evidence

- [other] Parse the user-supplied ROI bounds (lower and upper chemical-shift limits in ppm). 3. Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching.: "Parse the user-supplied ROI bounds (lower and upper chemical-shift limits in ppm). 3. Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI"
- [readme] ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum, saliva, sweat, urine, CSF, and tissues) using the Human Metabolome Database (HMDB) as a reference platform.: "ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum,"
- [other] Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available).: "Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available)."
- [readme] After setting parameters and completing the calculation, open the 'All Metabolites' window. Here, you can view identified metabolites along with their abbreviations, match ratios, matched regions, and concentration ranges.: "After setting parameters and completing the calculation, open the 'All Metabolites' window. Here, you can view identified metabolites along with their abbreviations, match ratios, matched regions,"
- [other] Export the candidate-metabolite table to CSV or Excel format.: "Export the candidate-metabolite table to CSV or Excel format."

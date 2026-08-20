---
name: metabolite-reference-library-filtering
description: Use when you have defined one or more proton NMR spectral regions-of-interest (ROIs) with lower and upper chemical-shift bounds (in ppm) from an experimental NMR spectrum of a biological sample, and you need to identify which metabolites in a reference database (HMDB) have published 1H NMR shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0592
  - http://edamontology.org/topic_3375
  tools:
  - pandas
  - openpyxl
  - XlsxWriter
  - XlsxWriter / openpyxl
  - PyQt5
  - Human Metabolome Database (HMDB)
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-reference-library-filtering

## Summary

This skill filters a reference metabolite database (HMDB) by proton NMR chemical-shift windows to systematically identify candidate metabolites whose reference 1H NMR shifts fall within user-defined regions-of-interest (ROIs). It is essential for annotating and interpreting NMR spectral features from complex biological samples.

## When to use

Apply this skill when you have defined one or more proton NMR spectral regions-of-interest (ROIs) with lower and upper chemical-shift bounds (in ppm) from an experimental NMR spectrum of a biological sample, and you need to identify which metabolites in a reference database (HMDB) have published 1H NMR shifts matching those regions. Typical use cases include human serum, saliva, sweat, urine, CSF, or tissue samples where spectral peaks require metabolite annotation.

## When NOT to use

- Input data lacks defined ROI bounds or chemical-shift windows — use spectral peak-picking or manual ROI definition first.
- Metabolite identity is already confirmed by independent orthogonal methods (e.g., MS/MS fragmentation, 2D NMR) — this skill is for candidate generation, not confirmation.
- Reference database is unavailable or lacks 1H NMR shift annotations for your target metabolites — filtration will return empty or incomplete results.

## Inputs

- HMDB reference database (metabolite entries with assigned proton NMR chemical shifts)
- ROI specification table (lower and upper chemical-shift bounds in ppm for each region of interest)
- Sample type designation (e.g., human serum, urine, CSF, tissue)

## Outputs

- Candidate metabolite table (CSV or Excel format with columns: metabolite name, HMDB ID, matched shift values, shift assignments/functional group context)
- Match ratio and concentration range per metabolite
- Annotated results table with abbreviations and regional assignments

## How to apply

Load the HMDB reference database and extract all metabolite entries with assigned proton NMR chemical shifts. Parse the user-supplied ROI bounds (lower and upper ppm limits) for each region of interest. Apply interval matching to filter the HMDB metabolite dataset, retaining only entries whose reference 1H NMR shifts fall within each ROI window. Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available). The filtration is deterministic: a metabolite is included if at least one of its reference shifts lies within [ROI_lower, ROI_upper]. Export the candidate-metabolite table to CSV or Excel format for downstream review and optional abbreviation annotation.

## Related tools

- **pandas** (Tabular filtering and interval matching of metabolite shift data against ROI bounds)
- **XlsxWriter / openpyxl** (Export and format candidate-metabolite results table to Excel format)
- **PyQt5** (GUI for ROI parameter input, metabolite selection, and results visualization)
- **Human Metabolome Database (HMDB)** (Reference platform and data source for metabolite entries with assigned proton NMR chemical shifts)

## Examples

```
python main.py
```

## Evaluation signals

- All returned metabolites have at least one reference 1H NMR shift value within the specified ROI bounds (no false negatives or out-of-range candidates).
- Results table schema validation: required columns (metabolite name, HMDB ID, matched shifts, shift assignments) are present and non-empty.
- Match ratio calculation is consistent: for each metabolite, (number of reference shifts within ROI) / (total number of reference shifts for that metabolite) is in range [0, 1].
- No duplicate metabolite entries in the output; each HMDB ID appears at most once per ROI.
- Export file format integrity: CSV or Excel output opens correctly and contains all candidate rows with no truncation or encoding errors.

## Limitations

- Filtration accuracy depends on the completeness and accuracy of HMDB reference 1H NMR shift annotations; missing or erroneous shifts in HMDB may cause false negatives or false positives.
- Chemical-shift overlap across metabolites (particularly for common functional groups like methyl or methylene) can lead to multiple candidates per ROI; post-hoc filtering or additional spectroscopic evidence is required for definitive assignment.
- No changelog or version history documentation provided; updates to HMDB or tool dependencies may affect reproducibility.
- ROI bounds must be manually defined by the user; automated peak detection or ROI optimization is not part of this workflow.

## Evidence

- [other] Given a defined proton NMR chemical-shift window (ROI) and the HMDB reference database, how does ROIAL-NMR systematically identify and return the list of candidate metabolites whose reference NMR shifts fall within that specified spectral region?: "Given a defined proton NMR chemical-shift window (ROI) and the HMDB reference database, how does ROIAL-NMR systematically identify and return the list of candidate metabolites whose reference NMR"
- [other] ROIAL-NMR operates by querying the Human Metabolome Database (HMDB) as a reference platform to systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs).: "ROIAL-NMR operates by querying the Human Metabolome Database (HMDB) as a reference platform to systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs)"
- [other] Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching.: "Filter the HMDB metabolite dataset to retain only entries whose reference 1H NMR shifts fall within the ROI window using interval matching"
- [other] Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available).: "Construct a results table with columns for metabolite name, HMDB ID, matched shift values, and shift assignments (functional group context if available)"
- [readme] ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum, saliva, sweat, urine, CSF, and tissues) using the Human Metabolome Database (HMDB) as a reference platform.: "ROIAL-NMR can systematically identify potential metabolites from defined proton NMR spectral regions-of-interest (ROIs), which are identified from complex biological samples (i.e., human serum,"

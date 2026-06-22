---
name: retention-time-and-mass-sorting-of-chromatographic-peaks
description: Use when you have raw GC-MS output from Agilent Unknowns Analysis (a .CSV with columns Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3307
  tools:
  - R
  - Agilent Unknowns Analysis
  - ChemmineR
  - fmcsR
  - webchem
  - PubChem
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
- The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis
- uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
---

# retention-time-and-mass-sorting-of-chromatographic-peaks

## Summary

Organizes raw GC-MS peak data from Agilent Unknowns Analysis output by retention time and exact mass, aggregating redundant peaks across samples and associating them with published chemical metadata (names, m/z fragments, exact mass, literature RT). This preprocessing prepares CSV input for downstream chemical identification and quantitation in the uafR pipeline.

## When to use

You have raw GC-MS output from Agilent Unknowns Analysis (a .CSV with columns Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) and need to convert it into a structured format for intelligent searching by retention time, exact mass, and published chemical identifiers before querying for specific analytes or applying cheminformatics filters.

## When NOT to use

- Input CSV is missing required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) — pre-processing or column renaming is needed first.
- Data is already in a structured, deduplicated format (e.g., already converted by spreadOut or another peak-matching tool) — applying again risks redundant aggregation.
- Retention time or mass information is missing or unreliable (e.g., RT values are null, Base.Peak.MZ is 0 or absent) — sorting and aggregation will fail or produce invalid rtBYmass codes.

## Inputs

- CSV file from Agilent Unknowns Analysis with mandatory columns: Component.RT (decimal, minutes), Base.Peak.MZ (decimal, m/z), Component.Area (numeric, integrated area), Compound.Name (string, tentative chemical name), Match.Factor (numeric, 0–100 spectral similarity), File.Name (string, sample identifier)

## Outputs

- List object with eight named components: Compounds (character matrix of chemical identifiers), RT (numeric matrix of retention times), MatchFactor (numeric matrix of spectral match scores), MZ (numeric matrix of observed m/z values), Mass (numeric matrix of exact masses), Area (numeric matrix of peak areas), rtBYmass (character matrix of unique RT|mass deduplication codes), webInfo (nested list of published metadata per compound)

## How to apply

Load the raw CSV into R and apply the spreadOut() function, which sorts peaks by retention time and exact mass, then aggregates sample portions describing the same chemical by pooling all published synonyms and top m/z fragments. The function constructs eight output matrices: (1) Compounds (chemical identifiers), (2) RT (retention times in minutes), (3) MatchFactor (spectral match scores from Unknowns Analysis), (4) MZ (observed base peak m/z values), (5) Mass (exact monoisotopic mass from PubChem/ChemSpider), (6) Area (raw integrated peak areas), (7) rtBYmass (unique retention-time|mass codes for deduplication), and (8) webInfo (nested lists containing all published synonyms, top m/z fragments, exact mass, and literature retention times for each compound). Validate the output by confirming all eight components are present, verifying no null or empty matrices for samples with detected peaks, checking that rtBYmass codes are unique (no duplicate RT|mass pairs), and ensuring webInfo nested lists contain non-empty metadata for each queried compound. The output list object is then ready for mzExacto() to extract user-defined query chemicals.

## Related tools

- **Agilent Unknowns Analysis** (generates raw GC-MS peak list CSV with required column schema (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name))
- **R** (environment in which spreadOut() and downstream uafR functions execute; any R-compatible mass spectrometry or cheminformatics tool can be adapted by changing column names)
- **ChemmineR** (cheminformatics package for structure-based queries and filtering of aggregated compounds)
- **fmcsR** (molecular flexible common substructure comparisons; used in exactoThese() to subset by structural features (rings, groups, atoms, charges))
- **webchem** (retrieves exact masses, synonyms, and literature retention times from PubChem and ChemSpider; populates webInfo nested lists)
- **PubChem** (source for exact monoisotopic masses, published chemical names (synonyms), and structure data)

## Examples

```
input_dat = read.csv('your/gcms/dataset.csv'); input_spread = spreadOut(input_dat)
```

## Evaluation signals

- All eight output matrix/list components (Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo) are present and non-null in the returned list object.
- rtBYmass codes are unique within each sample; no two peaks have identical retention-time|mass combinations (deduplication successful).
- For each compound in webInfo, nested lists contain non-empty entries for published synonyms, top m/z fragments, exact mass, and literature retention time values.
- Retention time ordering is monotonically non-decreasing (peaks sorted left-to-right by RT); m/z values correspond to Base.Peak.MZ from input.
- Exact masses in the Mass matrix match literature values from PubChem/ChemSpider within ±0.01 Da; no NULL or zero-values for samples with detected peaks above Match.Factor threshold.

## Limitations

- Requires strict CSV schema with exact column names; any deviation (e.g., 'Retention Time' instead of 'Component.RT') causes function failure.
- Aggregation by published names and m/z peaks assumes Agilent Unknowns Analysis tentative compound names are correct; misidentifications in the input are propagated and duplicated across rtBYmass codes.
- webInfo nested lists depend on successful queries to PubChem/ChemSpider via webchem; compounds without online matches or with obsolete/misspelled names will have incomplete or empty metadata entries.
- No changelog or version history provided in repository; reproducibility across different uafR versions is not documented.
- Peak deduplication by RT and exact mass assumes chromatographic and mass calibration are consistent across all input files; drift in retention time or m/z alignment can create false duplicates or miss true matches.

## Evidence

- [other] Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: "execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices"
- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [other] spreadOut() is designed to prepare CSV input for intelligent sorting and downstream processing by converting raw data into a format compatible with retention time and mass-based analysis.: "spreadOut() is designed to prepare CSV input for intelligent sorting and downstream processing by converting raw data into a format compatible with retention time and mass-based analysis"
- [other] webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times): "webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times)"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"

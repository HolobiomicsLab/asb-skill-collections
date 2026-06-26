---
name: spectral-library-matching-and-m-z-peak-ranking
description: Use when you have raw GC-MS output in CSV format (with Component.RT,
  Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, and File.Name columns)
  and need to systematically rank putative identifications by match quality and exact
  mass agreement.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - Agilent Unknowns Analysis
  - ChemmineR
  - fmcsR
  - webchem
  - PubChem/ChemSpider
  - uafR
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with
  simple modifications
- any software or utility that generates the necessary information can be used with
  simple modifications (e.g. changing the column names)
- The recommended software for generating the necessary data in the default format
  (i.e. with correct column names) is Unknowns Analysis
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0306202
  all_source_dois:
  - 10.1371/journal.pone.0306202
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-and-m-z-peak-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and rank chemical compounds in GC-MS data by matching observed mass spectra against published libraries and prioritizing peaks by match factor and m/z accuracy. This skill converts raw Agilent Unknowns Analysis output into a structured, ranked list of candidate identifications suitable for downstream cheminformatic filtering.

## When to use

Apply this skill when you have raw GC-MS output in CSV format (with Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, and File.Name columns) and need to systematically rank putative identifications by match quality and exact mass agreement. Use it as the first processing step in the uafR pipeline before querying specific chemicals or filtering by molecular properties.

## When NOT to use

- Input is already a pre-processed feature table or aggregated compound list — spreadOut() is designed for raw Unknowns Analysis CSV only.
- You need to subset or filter compounds before structural ranking — use spreadOut() first, then apply mzExacto() or exactoThese() on the output.
- Match factor data are missing or unreliable; the skill depends on accurate spectral matching scores from the mass spectrometer's library search.

## Inputs

- CSV file from Agilent Unknowns Analysis with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- R data.frame of raw GC-MS peak data

## Outputs

- Structured list object with eight named components: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo
- Ranked and aggregated peak identifications sorted by retention time and exact mass
- Unique retention-time|mass codes (rtBYmass) for unambiguous peak indexing

## How to apply

Load the standard Agilent Unknowns Analysis CSV into R and execute spreadOut() to sort peaks by retention time and exact mass, aggregate duplicate identifications by published chemical names and top m/z fragments, and construct eight output matrices: Compounds (chemical identifiers), RT (retention times), MatchFactor (numeric match scores), MZ (observed m/z values), Mass (exact masses from PubChem/ChemSpider), Area (peak areas), rtBYmass (unique retention-time|mass codes for peak identification), and webInfo (nested metadata including published names, top m/z fragments, exact mass, and literature retention times). Validate that all eight components are present, no matrices are null for samples with detected peaks, rtBYmass codes uniquely identify each peak, and webInfo contains non-empty published metadata. The resulting structured list is ready for downstream mzExacto() processing to extract query chemicals or for exactoThese() subsetting by Match.Factor threshold (e.g., >= 65 or > 80) to isolate high-confidence identifications.

## Related tools

- **R** (Host language for executing spreadOut() function and constructing output matrices)
- **Agilent Unknowns Analysis** (Source software generating the raw CSV input with spectral match factors and peak metadata)
- **ChemmineR** (Provides cheminformatic functions for mass and structural comparison in downstream workflows)
- **PubChem/ChemSpider** (Source databases for exact masses and published chemical names incorporated into webInfo metadata)
- **uafR** (R package containing spreadOut(), mzExacto(), categorate(), and exactoThese() functions for GC-MS processing) — https://github.com/castratton/uafR

## Examples

```
input_dat = read.csv('your/gcms/dataset.csv'); input_spread = spreadOut(input_dat); query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]; input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- All eight output matrices (Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo) are present and non-null for samples with detected peaks.
- rtBYmass codes are unique and consistently pair each retention time with its corresponding exact mass, with no duplicate codes across peaks.
- webInfo nested lists contain non-empty published metadata (chemical names, m/z fragments, exact mass, literature retention times) for all queried compounds.
- Match.Factor values are numeric and consistent with the input Match.Factor column; peaks above threshold (e.g., >= 65 or > 80) are correctly retained.
- Peak areas in the Area matrix are positive, non-zero values corresponding to the original Component.Area input; null or zero areas indicate missing or failed detections.

## Limitations

- Requires strict column name compliance (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name); non-standard CSV headers will cause function failure.
- Depends on the accuracy of the Agilent Unknowns Analysis spectral library match; low-quality matches (Match.Factor < 65) may introduce false or ambiguous identifications.
- Exact masses are retrieved from external databases (PubChem, ChemSpider); network failures or database unavailability will cause webInfo metadata to be incomplete.
- Does not resolve isomeric compounds with identical m/z and retention times; aggregation by published names and top m/z fragments may conflate structurally distinct isomers.
- No changelog found in the repository, limiting visibility into recent updates or breaking changes to the spreadOut() function.

## Evidence

- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor': "The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [other] spreadOut() prepares CSV input for intelligent sorting and downstream processing by converting raw data into a format compatible with retention time and mass-based analysis.: "spreadOut() is designed to prepare CSV input for intelligent sorting and downstream processing by converting raw data into a format compatible with retention time and mass-based analysis."
- [other] Execute spreadOut() to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: "Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: Compounds (chemical"
- [other] Validate output list structure: confirm all eight components present, verify no null matrices for samples with detected peaks, check that rtBYmass codes uniquely identify each peak, and ensure webInfo nested lists contain non-empty published metadata: "Validate output list structure: confirm all eight components present, verify no null matrices for samples with detected peaks, check that rtBYmass codes uniquely identify each peak, and ensure"
- [readme] Filter compounds by Match.Factor threshold before downstream processing: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]"
- [other] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and"

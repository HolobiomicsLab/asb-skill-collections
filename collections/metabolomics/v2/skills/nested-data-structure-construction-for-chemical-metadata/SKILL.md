---
name: nested-data-structure-construction-for-chemical-metadata
description: Use when you have loaded raw Agilent Unknowns Analysis CSV output with required columns (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0582
  - http://edamontology.org/topic_3172
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0306202
  all_source_dois:
  - 10.1371/journal.pone.0306202
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nested-data-structure-construction-for-chemical-metadata

## Summary

Construct a nested list object from GC-MS peak data that encapsulates chemical identifiers, retention times, match factors, exact masses, and literature metadata indexed by retention time and m/z. This structure bridges raw instrument output with downstream cheminformatics query and categorization workflows.

## When to use

You have loaded raw Agilent Unknowns Analysis CSV output with required columns (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) and need to prepare it for downstream functions (mzExacto, categorate) that expect data sorted and aggregated by published compound names and exact mass.

## When NOT to use

- Input CSV lacks required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) — preprocess or reformat first
- Data is already in a structured matrix/list format from a prior spreadOut() call — use directly for mzExacto() without re-processing
- You need only to filter by a single threshold (e.g., Match.Factor > 80) without full aggregation — subset the input directly instead

## Inputs

- CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- R DataFrame with GC-MS peak data loaded from Agilent Unknowns Analysis output

## Outputs

- List object with eight named components: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo
- Compounds: character matrix of chemical identifiers
- RT: numeric matrix of retention times
- MatchFactor: numeric matrix of match factors
- MZ: numeric matrix of observed m/z values
- Mass: numeric matrix of exact masses from chemical databases
- Area: numeric matrix of raw peak areas
- rtBYmass: character vector of unique RT|mass identifier codes
- webInfo: nested list of published compound names, top m/z fragments, exact mass, and literature retention times

## How to apply

Execute the spreadOut() function on your input CSV DataFrame. The function sorts peaks by retention time and exact mass, aggregates duplicates by published chemical names and top m/z peaks, and constructs eight output matrices: Compounds (chemical identifiers), RT (retention times), MatchFactor (match factors), MZ (observed m/z values), Mass (exact masses queried from PubChem/ChemSpider), Area (raw peak areas), rtBYmass (unique RT|mass codes), and webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times). The resulting list object is validated by confirming all eight components are present, verifying no null matrices exist for samples with detected peaks, checking that rtBYmass codes uniquely identify each peak, and ensuring webInfo nested lists contain non-empty published metadata for queried compounds.

## Related tools

- **R** (Programming environment for executing spreadOut() and constructing nested list objects)
- **Agilent Unknowns Analysis** (Instrument software that generates the raw CSV input in the required column format)
- **ChemmineR** (R cheminformatics package for querying exact mass and chemical structure data from PubChem/ChemSpider during webInfo construction)
- **webchem** (R package for retrieving published chemical metadata and literature retention times for webInfo nested lists)
- **PubChem** (Chemical database queried to populate exact mass (Mass) and reactive groups in webInfo)

## Examples

```
input_spread = spreadOut(read.csv('gcms_data.csv'))
```

## Evaluation signals

- All eight expected list components (Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo) are present with correct names and no NULL values for samples with detected peaks
- rtBYmass codes are unique identifiers—no duplicate RT|mass pairs exist within the same sample
- webInfo nested lists are non-empty for each queried compound and contain published names, top m/z fragments, exact mass value, and at least one literature retention time
- Matrix dimensions are consistent: all eight components have the same number of rows/compounds and columns match the number of unique input samples
- Retention time ordering within each sample is monotonically increasing (spreadOut sorts by RT), and aggregated peaks with identical compound names and m/z are merged without duplication

## Limitations

- Exact mass lookup depends on successful queries to PubChem/ChemSpider; compounds not found in these databases will have empty Mass fields or missing webInfo metadata
- Aggregation by published chemical names is sensitive to name variation and spelling; synonyms or abbreviations not recognized by the database will be treated as separate compounds
- The function assumes input CSV has strict column name requirements; any deviation in column naming or data type will cause failure unless modified
- No changelog is available for uafR, limiting visibility into past bug fixes, breaking changes, or version-specific behavior

## Evidence

- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses).: "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [other] Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, and webInfo.: "Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: Compounds (chemical"
- [other] Validate output list structure: confirm all eight components present, verify no null matrices for samples with detected peaks, check that rtBYmass codes uniquely identify each peak, and ensure webInfo nested lists contain non-empty published metadata for each queried compound.: "confirm all eight components present, verify no null matrices for samples with detected peaks, check that rtBYmass codes uniquely identify each peak, and ensure webInfo nested lists contain non-empty"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] Return structured list object ready for downstream mzExacto() processing.: "Return structured list object ready for downstream mzExacto() processing."

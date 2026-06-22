---
name: exact-mass-lookup-and-aggregation-from-chemical-databases
description: Use when after loading raw Agilent Unknowns Analysis CSV output and when you need to convert tentative compound identifications (matched only by GC-MS library cosine similarity or Match.Factor score) into searchable, curated chemical records with exact masses and multi-source confirmation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Agilent Unknowns Analysis
  - ChemmineR
  - fmcsR
  - webchem
  - PubChem
  - ChemSpider
  - uafR
  techniques:
  - GC-MS
  - tandem-MS
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

# exact-mass-lookup-and-aggregation-from-chemical-databases

## Summary

Retrieve exact masses, published chemical names, and spectroscopic metadata for compounds detected in GC-MS data by querying PubChem, ChemSpider, and literature databases, then aggregate redundant peak representations by chemical identity and dominant m/z fragments. This skill bridges raw mass spectrometry output to downstream retention time and mass-based sorting in the uafR pipeline.

## When to use

Apply this skill after loading raw Agilent Unknowns Analysis CSV output and when you need to convert tentative compound identifications (matched only by GC-MS library cosine similarity or Match.Factor score) into searchable, curated chemical records with exact masses and multi-source confirmation. Use it whenever samples contain multiple peaks from the same chemical (differing by retention time or fragmentation pattern) that should be consolidated for downstream analysis.

## When NOT to use

- Input CSV does not contain the required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) — preprocess or reformat first.
- Compound names are already resolved to exact structures with confirmed stereochemistry; this skill is for ambiguous or synonym-heavy identifications requiring database cross-reference.
- Samples contain no peaks with Match.Factor ≥ 65 or you are working with fully annotated, de novo MS/MS spectra rather than library-matched GC-MS runs.

## Inputs

- CSV file from Agilent Unknowns Analysis (with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name)
- Chemical compound names (character vector)
- PubChem/ChemSpider database connection

## Outputs

- Structured R list with eight named matrices: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass, webInfo
- webInfo nested list (published chemical names, top m/z fragments, exact monoisotopic mass, literature retention times per compound)

## How to apply

Execute the spreadOut() function on the raw CSV input to sort peaks by retention time and exact mass, then query PubChem and ChemSpider (via the webchem R package) for each unique Compound.Name to retrieve exact masses, published synonyms, and fragment ion patterns. Aggregate peaks that share the same chemical identity and top m/z value into a single record, preserving the highest Match.Factor and largest Component.Area per compound per file. Store results in eight output matrices: Compounds (chemical names), RT (retention times in minutes), MatchFactor (match quality scores), MZ (observed m/z), Mass (exact monoisotopic masses), Area (integrated peak areas), rtBYmass (unique retention time | mass codes for peak disambiguation), and webInfo (nested lists of published names, top m/z fragments, exact mass, and literature-reported retention times). Validate that rtBYmass codes uniquely identify each peak and that webInfo contains non-empty metadata for all queried compounds before passing to mzExacto() for targeted chemical search.

## Related tools

- **R** (Programming environment for executing spreadOut() and database query functions)
- **webchem** (R package for querying PubChem, ChemSpider, and retrieving exact masses and chemical metadata)
- **ChemmineR** (R cheminformatics package for structure-based chemical comparison and fragment ion analysis)
- **fmcsR** (R package for flexible maximum common substructure matching and molecular property extraction)
- **PubChem** (Public chemical database queried for exact monoisotopic masses, synonyms, and reactive group annotations)
- **ChemSpider** (Chemical structure database providing exact masses and alternative compound names)
- **uafR** (R package containing spreadOut() and mzExacto() pipeline functions) — https://github.com/castratton/uafR

## Examples

```
input_spread = spreadOut(read.csv('standard_data.csv')); query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- All eight output matrices are present in the returned list and non-null for samples with detected peaks (Match.Factor ≥ 65).
- rtBYmass codes uniquely identify each peak (no duplicate retention time | mass pairs within a sample).
- webInfo nested list contains non-empty published compound names and exact monoisotopic mass for ≥ 95% of queried compounds.
- Peaks from the same chemical (identical Compound.Name) are consolidated into a single row per file; Component.Area and Match.Factor reflect aggregation (max or sum as specified).
- Exact masses retrieved from PubChem/ChemSpider differ from observed Base.Peak.MZ by ≤ 5 ppm (drift consistent with GC-MS instrumental accuracy).

## Limitations

- Compound name matching depends on exact string concordance with PubChem/ChemSpider; synonyms and misspellings in the input CSV will fail silent or return null metadata.
- Literature retention times (stored in webInfo) are acquired from published GC methods, which may not match the user's instrument, column, or temperature program.
- Aggregation by 'top m/z peaks' requires a predefined threshold or ranking rule; the article does not specify how many fragments are retained or how ties are broken.
- No explicit validation step for false positives (high Match.Factor from NIST library match but incorrect compound identity); downstream curation by expert review is recommended.

## Evidence

- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and"
- [other] Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices: "Execute spreadOut() function to sort peaks by retention time and exact mass, aggregate by published chemical names and top m/z peaks, and construct eight output matrices"
- [methods] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times): "webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times)"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor': "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [other] Validate output list structure: confirm all eight components present, verify no null matrices for samples with detected peaks: "Validate output list structure: confirm all eight components present, verify no null matrices for samples with detected peaks"

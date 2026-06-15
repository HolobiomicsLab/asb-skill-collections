---
name: chemical-structure-similarity-matching
description: Use when when you have a set of query chemicals (e.g., ethyl hexanoate, methyl salicylate) and need to find their -matched structural analogues within a reference library (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - R
  - ChemmineR
  - fmcsR
  - webchem
  - uafR::categorate
  - uafR::exactoThese
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
- uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
---

# chemical-structure-similarity-matching

## Summary

A cheminformatics skill that uses structural fingerprinting and maximum common substructure (FMCS) algorithms to identify and rank structurally similar compounds within a chemical library. It quantifies structural similarity via match scores (typically ≥0.95 threshold) to enable compound classification and cross-library matching.

## When to use

When you have a set of query chemicals (e.g., ethyl hexanoate, methyl salicylate) and need to find their best-matched structural analogues within a reference library (e.g., restricted chemical types A–E) to support compound identification, structural classification, or validation in mass spectrometry workflows. Use this when Match.Factor filtering alone is insufficient and you need to confirm structural relationships beyond retention time and m/z matching.

## When NOT to use

- Input is a pre-computed feature matrix or a distance matrix — use this skill on raw chemical names/SMILES, not on derived numerical features.
- Query chemicals lack common names or SMILES strings recognized by PubChem/ChemmineR — structural matching requires resolvable chemical identities.
- The reference library is already a mass spectrometry match table (e.g., Agilent Unknowns Analysis output) — use mzExacto() for MS-based matching instead.

## Inputs

- query_chemicals (character vector of compound names, e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'))
- chem_library (data frame with chemical groups/types as columns, e.g., GroupA, GroupB, or Types A–E)
- input_format parameter ('wide' for column-per-group, 'long' for alternative layouts)

## Outputs

- BestChemMatch dataframe with rows per query chemical, columns for each library type, cells containing matched compound identifiers (e.g., 'CMP2'), and associated similarity/match scores
- Categorical data structure enabling downstream subsetting via exactoThese()

## How to apply

Load query chemicals (as a character vector of compound names) and a reference chemical library (as a data frame with chemical groups or types) into R. Execute categorate() with the query_chemicals and chem_library arguments, specifying input_format='wide' if the library is structured as columns per group. The function internally invokes ChemmineR, fmcsR, and webchem to compute atomic feature descriptors and FMCS overlap scores for each query chemical against each library compound. Extract the BestChemMatch dataframe from categorate() output, which ranks matches by similarity score. Filter or inspect rows where the match score is ≥0.95 to confirm structurally equivalent compounds. Verify that expected high-similarity pairs (e.g., ethyl hexanoate and isobutyl hexanoate) appear in the same type column with matching compound identifiers (e.g., 'CMP2').

## Related tools

- **ChemmineR** (Computes structural fingerprints and similarity metrics for query and library chemicals)
- **fmcsR** (Calculates maximum common substructure (FMCS) overlap and atomic feature descriptors)
- **webchem** (Resolves chemical names to structure data and integrates external database lookups (PubChem, LOTUS, KEGG, FEMA, FDA/SPL))
- **uafR::categorate** (Orchestrates structural matching across cheminformatics packages and outputs BestChemMatch results) — https://github.com/castratton/uafR
- **uafR::exactoThese** (Subsets categorate() output by database presence, FMCS properties (MW, rings, groups, atoms, charges), or library groups) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); chem_library = data.frame(cbind(Types_A = c(...), Types_B = c(...), Types_D = c('Isobutyl hexanoate', ...))); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide')
```

## Evaluation signals

- Ethyl hexanoate match score to isobutyl hexanoate is ≥0.95 and appears in the same library type column (e.g., Type D) with matching compound identifier
- BestChemMatch dataframe has one row per query chemical and one column per library type/group
- All expected high-similarity structural pairs (e.g., isomers or homologs) are ranked in the top matches for their respective queries
- No null or 'NA' values in match score columns for well-established compounds in the reference library
- Downstream exactoThese() subsetting produces non-empty chemical subsets when filtering by database presence (LOTUS, FEMA, KEGG, FDA/SPL) or FMCS thresholds (MW range, ring count, etc.)

## Limitations

- Structural matching depends on chemical name resolution by PubChem/webchem; obscure or misspelled compound names may fail to resolve or return incorrect structures.
- Match scores reflect FMCS and fingerprint overlap, which may not capture all chemically relevant structural features (e.g., stereochemistry nuances, tautomeric forms).
- Library completeness and currency affect the quality of matches; outdated or sparse reference libraries may fail to identify true structural analogues.
- The function requires internet access or cached cheminformatics databases (PubChem, LOTUS, KEGG, FEMA, FDA/SPL); offline workflows are not supported in the current uafR implementation.
- No changelog documented for categorate() or exactoThese() versions, limiting reproducibility across package updates.

## Evidence

- [other] Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a restricted chemical library?: "Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a restricted chemical"
- [other] The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds.: "The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds."
- [readme] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical.: "Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical."
- [readme] query_categorated = categorate(query_chemicals, chem_library, input_format = "wide"): "query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")"
- [other] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"

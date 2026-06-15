---
name: compound-structural-fingerprint-comparison
description: Use when you have a set of query chemicals and a reference library (organized by type or group), and you need to determine which reference compounds most closely resemble each query chemical based on structural features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0209
  tools:
  - R
  - ChemmineR
  - fmcsR
  - webchem
  - uafR
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

# compound-structural-fingerprint-comparison

## Summary

This skill uses cheminformatics packages (ChemmineR, fmcsR, webchem) to compute structural similarity scores between query chemicals and a reference library, identifying best-matched compounds based on atomic fingerprints and molecular features. It is essential when you need to assess whether structurally similar compounds are correctly distinguished or grouped during chemical categorization.

## When to use

Use this skill when you have a set of query chemicals and a reference library (organized by type or group), and you need to determine which reference compounds most closely resemble each query chemical based on structural features. This is particularly important when validating that the categorate() function correctly identifies structural matches (e.g., matching ethyl hexanoate to isobutyl hexanoate with a similarity score ≥0.95) or when filtering chemicals by Tanimoto/FMCS metrics.

## When NOT to use

- Input chemicals do not have valid chemical names or SMILES representations resolvable by PubChem/webchem.
- Reference library contains fewer than 2 compounds per type, making comparative structural matching uninformative.
- Goal is mass spectrum matching rather than structural similarity; use Match.Factor filtering on MS/GC-MS data instead.

## Inputs

- vector of query chemical names or SMILES strings
- reference chemical library (data.frame organized by type or group, wide or long format)
- input_format parameter ('wide' or 'long') specifying reference library structure

## Outputs

- categorate() output object containing BestChemMatch dataframe
- BestChemMatch dataframe with columns for each library type, rows for each query chemical, entries showing match scores and matched compound identifiers
- FMCS structural features (molecular weight, ring count, functional group count, atom count, net charge)

## How to apply

Load query chemicals and the reference library (organized by type or group) into R. Execute the categorate() function, which internally calls ChemmineR, fmcsR, and webchem to compute structural comparisons and extract atomic feature fingerprints for each compound pair. Extract the BestChemMatch dataframe from the categorate() output, which contains match scores for each query chemical against each type group. Filter or rank results by match score (typically expecting ≥0.95 for high-confidence structural similarity) to identify the best-matched compound in each reference type. Validate the results by checking that expected structural analogs (e.g., ethyl hexanoate and isobutyl hexanoate) appear in the same type group with high scores, and confirm the output table displays the correct compound identifier (e.g., 'CMP2') for each query-reference match.

## Related tools

- **ChemmineR** (computes molecular fingerprints and structural similarity metrics for query and library compounds)
- **fmcsR** (performs flexible maximum common substructure (FMCS) matching and extracts atomic features (MW, rings, groups, atoms, charges))
- **webchem** (resolves chemical names to canonical structures and retrieves molecular data from PubChem)
- **uafR** (provides categorate() wrapper function that orchestrates ChemmineR, fmcsR, and webchem for streamlined structural comparison workflows) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c("Ethyl hexanoate", "Methyl salicylate", "Octanal", "Undecane"); chem_library = data.frame(cbind(TypeA, TypeB, TypeC, TypeD, TypeE)); query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")
```

## Evaluation signals

- BestChemMatch dataframe is non-null and contains one row per query chemical and one column per library type group.
- Match scores for structurally related pairs (e.g., ethyl hexanoate vs. isobutyl hexanoate) are ≥0.95; unrelated pairs score <0.7.
- Matched compound identifiers (e.g., 'CMP2') correctly map to the expected reference library compound in each type.
- FMCS feature columns (MW, Rings, Groups, Atoms, NCharges) contain numeric values consistent with molecular composition.
- No NA or null entries appear in match score columns for valid input chemicals with resolvable structures.

## Limitations

- Structural matching depends on accurate chemical name resolution via PubChem/webchem; ambiguous or misspelled names may fail to resolve.
- Match scores reflect 2D structural similarity (fingerprints and FMCS); they do not capture 3D conformational or pharmacophoric differences.
- Very large reference libraries (>10,000 compounds) may incur long computation times due to pairwise FMCS comparisons.
- categorate() requires strict input data format (data.frame with named columns for each type group); malformed input will error before comparison runs.

## Evidence

- [other] Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a restricted chemical library?: "research_question: Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a"
- [readme] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [methods] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [other] Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical.: "Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical."
- [other] Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2) and that the output table displays 'CMP2' in the Type D column for ethyl hexanoate.: "Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2) and that the output table displays 'CMP2' in the Type D column for ethyl hexanoate."

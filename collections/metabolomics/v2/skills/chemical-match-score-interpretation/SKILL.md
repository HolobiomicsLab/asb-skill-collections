---
name: chemical-match-score-interpretation
description: Use when when you have query chemicals identified by GC-MS (with Match.Factor values) and need to verify structural similarity against a reference chemical library to confirm compound identity or detect structural analogs (e.g., isomers or homologs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
  tools:
  - R
  - ChemmineR
  - fmcsR
  - webchem
  - categorate
  - exactoThese
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
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

# chemical-match-score-interpretation

## Summary

Interpret structural similarity match scores from cheminformatics tools (ChemmineR, fmcsR) to identify and validate chemical compounds that meet structural equivalence thresholds. This skill bridges mass spectrometry identification with structural validation, enabling confident assignment of query chemicals to library compounds based on quantified atomic and molecular feature overlap.

## When to use

When you have query chemicals identified by GC-MS (with Match.Factor values) and need to verify structural similarity against a reference chemical library to confirm compound identity or detect structural analogs (e.g., isomers or homologs). Apply this skill when a compound name alone is insufficient and you require quantified structural evidence—especially when screening for specific functional groups, molecular weight ranges, or ring structures within a library.

## When NOT to use

- Input query chemicals are already validated against a curated standard with Match.Factor >95; structural re-validation is redundant.
- Chemical library contains only chemical names without SMILES/structure files; categorate() requires structure data for fmcsR/ChemmineR to compute scores.
- You need to filter results by metabolite presence or bioactivity categories; use exactoThese() subsetting instead, which operates downstream of categorate().

## Inputs

- query_chemicals (character vector of compound names)
- chemical_library (dataframe with named groups/types containing chemical names; can be 'wide' or 'long' format)
- input_format parameter ('wide' or 'long')

## Outputs

- BestChemMatch dataframe (query chemical × best-matched library compound, match scores, group/type assignment)
- categorate_full_output object (includes nested FMCS molecular feature tables: MW, Atoms, Rings, Groups, NCharges)

## How to apply

Load query chemicals (e.g., ethyl hexanoate, methyl salicylate) and a structured chemical library (organized by groups or chemical types) into categorate(). The function wraps ChemmineR, fmcsR, and webchem to compute pairwise structural match scores via flexmatch common substructure (FMCS) analysis. Extract the BestChemMatch output dataframe, which ranks library compounds by match score for each query chemical. Filter results for match scores ≥0.95 to identify high-confidence structural matches; examine the compound ID and chemical group assignment (e.g., 'Type D', 'GroupA') in the output table. Validate that ethyl hexanoate correctly matches isobutyl hexanoate at the expected score, confirming the function is correctly identifying structurally similar esters. Cross-reference retained match scores with molecular properties (MW, atomic count, ring structure) extracted by fmcsR to ensure the match reflects meaningful structural overlap, not coincidental similarity.

## Related tools

- **ChemmineR** (Cheminformatics package that enables structural comparison and atomic feature analysis for computing match scores)
- **fmcsR** (Implements flexmatch common substructure (FMCS) algorithm to quantify structural similarity and extract molecular properties (MW, Atoms, Rings, Groups, NCharges))
- **webchem** (Retrieves and validates chemical structure data from online databases for query and library compounds)
- **categorate** (Orchestrates structural matching workflow; wraps ChemmineR/fmcsR/webchem and outputs BestChemMatch dataframe with match scores and group assignments) — https://github.com/castratton/uafR
- **exactoThese** (Filters categorate() output by match scores, molecular properties (MW, Rings, Groups, Atoms), or database presence for downstream subsetting) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c("Ethyl hexanoate", "Methyl salicylate", "Octanal", "Undecane")
Types_library = data.frame(cbind(TypeA = c(...), TypeB = c(...), TypeD = c("Isobutyl hexanoate", ...)))
query_categorated = categorate(query_chemicals, Types_library, input_format = "wide")
BestChemMatch = query_categorated$BestChemMatch
```

## Evaluation signals

- BestChemMatch dataframe row for ethyl hexanoate shows match score ≥0.95 and Type/Group assignment 'Type D' or 'CMP2' (the isobutyl hexanoate compound); confirm no NULL/NA values in the match score column.
- Molecular property columns (MW, Atoms, Rings, NCharges) extracted by fmcsR for the matched compound pair differ by ≤±2 units for Atoms and ≤1 for Rings, reflecting true structural similarity.
- Match scores for non-similar query-library pairs (e.g., octanal vs. undecane) are <0.90, demonstrating discrimination; rerun on a known non-matching pair as a negative control.
- Exact compound name or SMILES string of the best match in BestChemMatch matches the reference library input (e.g., 'isobutyl hexanoate' or its chemical ID) without truncation or alias substitution.
- categorate() output structure contains expected columns: Query.Chemical, Best.Match, Match.Score, Group/Type, and all FMCS feature columns; verify via colnames() and str().

## Limitations

- Match scores depend on structure file quality and coverage in underlying databases (PubChem, LOTUS, KEGG); missing or incorrect SMILES will reduce or eliminate matches.
- FMCS algorithm may assign high scores to compounds with similar functional groups but different carbon chain length or saturation; complementary filtering by exactoThese(subsetBy='FMCS', subsetArgs='MW') is needed to enforce stricter molecular weight constraints.
- categorate() expects chemical names resolvable by webchem to PubChem/ChemSpider; ambiguous or obsolete trade names may fail to retrieve structure data, resulting in NA match scores.
- No changelog or version specification provided in README; reproducibility across uafR versions is not guaranteed.

## Evidence

- [other] Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a restricted chemical library?: "Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions"
- [other] The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds.: "The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment"
- [other] Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis against each chemical type set.: "Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis"
- [other] Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical.: "Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound"
- [other] Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2) and that the output table displays 'CMP2' in the Type D column for ethyl hexanoate.: "ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2)"
- [readme] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [methods] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [readme] these_chems = exactoThese(query_categorated, subsetBy = "FMCS", subsetArgs = "MW", subsetArgs2 = "Between", subset_input = c(50,115)): "exactoThese(query_categorated, subsetBy = "FMCS", subsetArgs = "MW", subsetArgs2 = "Between", subset_input = c(50,115))"

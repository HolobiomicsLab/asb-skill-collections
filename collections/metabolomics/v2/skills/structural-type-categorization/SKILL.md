---
name: structural-type-categorization
description: Use when when you have a set of query chemical compounds (by name or SMILES) and a reference library organized into named groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3345
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
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

# structural-type-categorization

## Summary

A cheminformatics workflow that categorizes query chemicals against a reference library by computing structural similarity scores and identifying best-matched compounds in each library group. Uses ChemmineR, fmcsR, and webchem to enable structural matching and assessment across chemical types.

## When to use

When you have a set of query chemical compounds (by name or SMILES) and a reference library organized into named groups (e.g., Types A–E, or user-defined library groups), and you need to determine which reference compound in each group is most structurally similar to each query chemical, with quantitative match scores (e.g., ≥0.95 for isomers or close analogs).

## When NOT to use

- Query chemicals lack SMILES or canonical names resolvable by PubChem/webchem (categorate() will fail to compute descriptors).
- Reference library contains fewer than 2 groups or is already organized as a tall (long-format) table rather than wide format (requires reformatting before categorate()).
- You only need binary presence/absence of compounds in groups, not quantitative structural similarity scores (simpler subsetting with exactoThese() is more efficient).

## Inputs

- vector of query chemical names (e.g., c('Linalool', 'Methyl Salicylate', 'Limonene'))
- reference library as wide-format data frame with group names as column headers and chemical compound names as cell values
- optional: Match.Factor or retention time data to pre-filter high-confidence compounds before categorization

## Outputs

- categorate() output object containing BestChemMatch dataframe
- BestChemMatch dataframe with rows for each query chemical, columns for each library group, cell values showing best-matched compound ID and match score
- structural match scores (0–1 scale or 0–100) indicating degree of similarity between query and reference compounds

## How to apply

Load query chemical names and a reference library organized as a wide-format data frame (groups as columns, compound names as rows) into R. Call categorate() with the query chemicals and library, specifying input_format='wide' to trigger cheminformatics comparison via ChemmineR, fmcsR, and webchem. Extract the BestChemMatch output dataframe, which contains structural similarity scores for each query–reference pair. Filter results by match score threshold (typically ≥0.95 for structural analogs) and identify the best-matched compound ID in each library group for each query chemical. Verify output by checking that structurally similar compounds (e.g., ethyl hexanoate and isobutyl hexanoate) show scores above the threshold and appear in the same library group.

## Related tools

- **ChemmineR** (Core cheminformatics backend for computing structural fingerprints and similarity metrics during categorate() execution)
- **fmcsR** (Flexible maximum common substructure matching for evaluating atomic feature overlap between query and reference compounds)
- **webchem** (Resolves chemical names to standard structures and retrieves descriptors from external databases (PubChem, KEGG))
- **uafR** (R package hosting categorate() and companion workflow functions (spreadOut, mzExacto, exactoThese)) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal'); library = data.frame(TypeA=c('Guaiacol','Tridecane'), TypeD=c('Compound1','Isobutyl hexanoate')); result = categorate(query_chemicals, library, input_format='wide')
```

## Evaluation signals

- BestChemMatch dataframe is returned with one row per query chemical and one column per library group; no missing values in match score column.
- Structurally similar compound pairs (e.g., ethyl hexanoate and isobutyl hexanoate) show match scores ≥0.95 and are assigned to the same library group.
- Match scores are symmetric or near-symmetric: if compound A matches compound B with score S, the reverse comparison yields similar S (validates proper molecular descriptor calculation).
- All query chemicals are present in the output; compounds with no match in a group show score 0 or NA (not dropped entirely).
- Molecular weight, ring count, and functional group composition extracted by fmcsR are consistent with known chemical structures (spot-check 2–3 outputs against PubChem).

## Limitations

- categorate() requires all chemical names to be resolvable by webchem and PubChem; misspelled or non-standard names will fail silently or return NA scores.
- Structural similarity is based on 2D atomic fingerprints (ChemmineR/fmcsR); stereoisomers and different tautomers may be incorrectly scored as identical.
- Match scores are relative to the provided library only; same query chemical may score differently against a different reference library, making absolute thresholds unreliable across studies.
- No changelog available for uafR; version-specific behavior of ChemmineR/fmcsR backends and external database APIs (PubChem) may cause reproducibility issues.

## Evidence

- [methods] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [readme] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds.: "The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds."
- [other] Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis against each chemical type set.: "Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis against each chemical type set."
- [other] Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical.: "Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical."
- [other] Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2): "Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2)"
- [readme] query_categorated = categorate(query_chemicals, chem_library, input_format = "wide"): "query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")"

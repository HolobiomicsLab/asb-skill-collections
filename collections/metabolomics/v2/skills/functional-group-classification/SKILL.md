---
name: functional-group-classification
description: Use when you have a set of query chemicals (chemical names or structures) and need to match them against a reference chemical library organized by type or category, with the goal of identifying structural similarity, functional group membership, or categorical assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_2258
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

# functional-group-classification

## Summary

Classify query chemicals into categorical groups based on structural and functional properties using cheminformatics packages that assess atomic features, ring systems, and molecular weight. This skill enables researchers to systematically organize and filter chemical inventories by structural similarity and functional characteristics.

## When to use

Apply this skill when you have a set of query chemicals (chemical names or structures) and need to match them against a reference chemical library organized by type or category, with the goal of identifying structural similarity, functional group membership, or categorical assignment. Typical triggers include: (1) need to assess whether query compounds (e.g., ethyl hexanoate, methyl salicylate) match reference library groups (e.g., Types A–E) with quantified similarity scores; (2) requirement to filter compounds by atomic features, ring counts, or molecular weight ranges; (3) goal to cross-reference query chemicals against multiple external databases (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) for regulatory or safety categorization.

## When NOT to use

- Query chemicals are already classified and no reference library is available or needed.
- Input library is unstructured or lacks clear chemical identifiers and group labels.
- Goal is only to identify exact chemical matches by name or InChI, without structural or functional similarity assessment.

## Inputs

- vector or list of query chemical names (character strings, e.g., c('Linalool', 'Methyl Salicylate'))
- reference chemical library as a data frame with named groups/types (wide format: GroupA, GroupB; or long format with Type/Compound columns)
- input_format parameter specifying library orientation ('wide' or 'long')

## Outputs

- categorate() output dataframe containing: query chemical names, matched reference compound names, BestChemMatch similarity scores, type/group assignments
- BestChemMatch dataframe (extracted from categorate() output) with match scores ≥0.95 for high-confidence structural matches
- subsetted chemical list from exactoThese() filtered by database membership, molecular weight range, or structural feature thresholds

## How to apply

Load query chemical names (e.g., 'Linalool', 'Methyl Salicylate') and a reference chemical library (organized in wide or long format with named groups, e.g., GroupA, GroupB, or Types A–E) into R. Call categorate() with the query chemicals, library, and input_format parameter to invoke cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis. The function returns a dataframe that includes: best-matched compound names, BestChemMatch scores (typically filtered at ≥0.95 for high confidence), and categorical assignments to each group. Post-process the output using exactoThese() to subset results by database presence (e.g., subsetBy='Database', subsetArgs='FEMA'), molecular weight range (e.g., subsetArgs='MW', subsetArgs2='Between', subset_input=c(125,200)), or structural features (e.g., Rings, Groups, Atoms, NCharges). Verify that the output table displays the expected compound name or code in the matched type column for each query chemical.

## Related tools

- **ChemmineR** (Performs structural comparison and similarity assessment against chemical library groups)
- **fmcsR** (Computes flexible maximum common substructure (FMCS) for structural matching and extracts atomic features (rings, groups, atoms, charges))
- **webchem** (Queries external chemical databases (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) to retrieve categorical and regulatory information)
- **uafR** (R package providing categorate() and exactoThese() functions to orchestrate functional group classification and filtering workflows) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c('Linalool', 'Methyl Salicylate'); chem_library = data.frame(cbind(c('Guaiacol', 'Tridecane'), c('2-Aminothiazole', 'Aspirin'))); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide'); these_chems = exactoThese(query_categorated, subsetBy = 'FMCS', subsetArgs = 'MW', subsetArgs2 = 'Between', subset_input = c(125, 200))
```

## Evaluation signals

- BestChemMatch similarity score for the intended reference compound is ≥0.95 (e.g., ethyl hexanoate matches isobutyl hexanoate at score ≥0.95)
- Matched compound name or code appears in the correct type/group column of the output dataframe (e.g., 'CMP2' displayed in Type D column)
- exactoThese() subsets correctly reduce the result set according to specified filter criteria (e.g., molecular weight 'Between' c(125,200) returns only compounds within that range)
- Compounds present in specified external databases (FEMA, LOTUS, KEGG) are correctly flagged or retained in the database-filtered output
- Output dataframe structure matches expected schema: query chemical names as rows, type/group columns, match scores, and database flags as columns

## Limitations

- Structural matching relies on canonical SMILES or InChI representations; poorly standardized or ambiguous chemical names may fail to match or return low confidence scores.
- External database queries (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) depend on web service availability and may be slow for large query sets.
- Match scores reflect structural/functional similarity, not chemical safety or regulatory approval; downstream validation against regulatory databases is required for safety-critical applications.
- Atomic feature extraction (ring count, group count, charge) is sensitive to protonation state and tautomerism; input structures should be pre-standardized if consistent results across batches are required.
- No changelog available in the source repository; version stability and backwards compatibility are undocumented.

## Evidence

- [methods] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [other] Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis against each chemical type set.: "Execute categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) for structural comparison and atomic feature analysis against each chemical type set."
- [other] Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical.: "Extract the BestChemMatch dataframe from categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical."
- [other] Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2) and that the output table displays 'CMP2' in the Type D column for ethyl hexanoate.: "Verify that ethyl hexanoate shows a structural match score ≥0.95 to isobutyl hexanoate (Type D compound 2) and that the output table displays 'CMP2' in the Type D column for ethyl hexanoate."
- [readme] query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene', 'alpha-Thujene'); GroupA = c('Guaiacol', 'Tridecane', 'Ethyl heptanoate', 'Caffeine'); GroupB = c('2-Aminothiazole', 'Aspirin', 'Octanoic acid', 'alpha-Pinene', 'Toluene'); chem_library = data.frame(cbind(GroupA, GroupB)); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide'): "query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")"
- [readme] example of using the info from categorate() to get a user-defined set of chemicals with exactoThese(): these_chems = exactoThese(query_categorated, subsetBy = 'FMCS', subsetArgs = 'MW', subsetArgs2 = 'Between', subset_input = c(125, 200)): "exactoThese(query_categorated, subsetBy = "FMCS", subsetArgs = "MW", subsetArgs2 = "Between", subset_input = c(125, 200))"

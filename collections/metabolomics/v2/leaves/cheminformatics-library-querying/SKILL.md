---
name: cheminformatics-library-querying
description: Use when you have a list of query chemicals (compound names or SMILES)
  and a reference library organized by chemical groups (e.g., Types A–E, GroupA/GroupB),
  and you need to assess which library compounds are structurally similar to your
  queries, retrieve their categorical annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0346
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - R
  - ChemmineR
  - fmcsR
  - webchem
  - uafR
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with
  simple modifications
- any software or utility that generates the necessary information can be used with
  simple modifications (e.g. changing the column names)
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

# cheminformatics-library-querying

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Query a structured chemical library against a set of query compounds to retrieve categorical metadata, structural similarity scores, and database presence flags using cheminformatics packages. This skill enables systematic identification of compounds matching specific structural or property criteria across multiple external databases (PubChem, LOTUS, KEGG, FEMA, FDA/SPL).

## When to use

You have a list of query chemicals (compound names or SMILES) and a reference library organized by chemical groups (e.g., Types A–E, GroupA/GroupB), and you need to assess which library compounds are structurally similar to your queries, retrieve their categorical annotations (e.g., database presence, molecular weight, ring count, functional groups), or filter the library by structural or property thresholds. This is particularly useful after mass spectrometry peak matching (Match.Factor filtering) when you want to contextualize identified compounds against curated chemical sets or assess structural diversity.

## When NOT to use

- Your query compounds are already represented as SMILES strings or molecular objects without common chemical names — categorate() expects chemical names that can be resolved by webchem/ChemmineR to structures.
- Your reference library is very large (>10,000 compounds) or consists of proprietary/in-house structures not indexed by PubChem, LOTUS, KEGG, or FEMA — external database lookups will fail or return incomplete results.
- You only need exact match retrieval (e.g., 'find all compounds in the library with name = X'), not structural similarity assessment — a simple dataframe subset or SQL join would be more efficient.

## Inputs

- query_chemicals: character vector of compound names (e.g., c('Linalool', 'Methyl Salicylate', 'Limonene'))
- chem_library: dataframe with chemical groups as columns and compound names as values (wide format) or a long format equivalent
- input_format: character string ('wide' or 'long') indicating library layout

## Outputs

- query_categorated: dataframe with rows for each query chemical and columns for each library group, containing best-matched compound name and match score for each group
- BestChemMatch dataframe (extractable from query_categorated output) with match scores, structural similarity metrics, and categorical flags (database presence, molecular weight, ring/atom/group counts, charge status)

## How to apply

Load your query chemical names and the reference library (as a wide or long dataframe) into R, then invoke categorate() with the query list and library dataframe. categorate() delegates to ChemmineR, fmcsR, and webchem packages to compute structural similarity (via maximum common substructure matching) and query multiple external databases (PubChem reactive groups, LOTUS natural products, KEGG bioactivities, FEMA flavor/odor status, FDA/SPL regulatory presence). The function returns a BestChemMatch dataframe for each query compound showing the best-matched library compound per group, along with match scores (typically ≥0.95 for high structural similarity), and categorical flags (e.g., database membership, molecular weight, atom/ring/group counts). You can then subset the categorated output using exactoThese() to further filter by database presence (e.g., retain only FEMA compounds), molecular weight range (Greater Than, Less Than, Between), or structural features (rings, atoms, charged groups). Evaluate success by confirming that structurally analogous compounds (e.g., ethyl hexanoate and isobutyl hexanoate) receive match scores ≥0.95 and are correctly identified in the output.

## Related tools

- **ChemmineR** (Provides cheminformatics infrastructure for structure comparison, similarity scoring, and compound object manipulation)
- **fmcsR** (Computes maximum common substructure (FMCS) matching and structural similarity scores between query and library compounds)
- **webchem** (Resolves chemical names to structures and queries external databases (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) for categorical metadata)
- **uafR** (R package wrapping categorate(), exactoThese(), and associated workflow functions for mass spectrometry and cheminformatics integration) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene'); chem_library = data.frame(cbind(GroupA = c('Guaiacol', 'Ethyl heptanoate'), GroupB = c('Aspirin', 'alpha-Pinene'))); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide')
```

## Evaluation signals

- Structurally analogous compounds (e.g., homologous esters) in the reference library receive match scores ≥0.95 from fmcsR when queried
- The BestChemMatch dataframe contains exactly one row per query chemical and one column per library group, with no NA values in match score columns for successful lookups
- Database presence flags (LOTUS, KEGG, FEMA, FDA/SPL, PubChem.Reactive.Groups) are populated as TRUE/FALSE or presence counts for all query compounds
- Subsequent exactoThese() subsetting (e.g., by molecular weight range c(50, 115)) returns a subset of matched compounds with all FMCS properties (MW, Rings, Groups, Atoms, NCharges) within or matching the specified bounds
- Comparison of match scores and categorical outputs to published chemical similarity databases (e.g., PubChem similarity clusters) shows consistent ranking and grouping

## Limitations

- External database queries (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) depend on internet availability and may fail silently or return incomplete metadata if a chemical name is ambiguous or not indexed.
- Chemical name resolution via webchem assumes standardized nomenclature; proprietary, colloquial, or misspelled names will not be resolved and will produce NA values.
- Structural similarity is computed via maximum common substructure (FMCS) matching, which may not capture all relevant pharmacological or sensory similarities (e.g., two compounds with high topological similarity may differ greatly in volatility or flavor).
- The function is optimized for small to moderate query sets (<100 compounds) and library sizes (<1000 compounds); performance degrades significantly for large-scale screening without parallelization.

## Evidence

- [methods] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [methods] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds.: "The categorate() function is designed to access categorical data for searched chemicals, enabling structural matching and similarity assessment across chemical compounds."
- [other] categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical: "categorate() output, filtering for match scores and identifying the best-matched compound in each type for each query chemical"
- [readme] example usage for chemical informatics: query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene', 'alpha-Thujene'); chem_library = data.frame(...); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide'): "query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene', 'alpha-Thujene'); chem_library = data.frame(cbind(GroupA, GroupB)); query_categorated = categorate(query_chemicals, chem_library,"
- [methods] Reactive Groups from PubChem, natural products occurrences from LOTUS, bioactivites and risk categories from the Kyoto Encyclopedia of Genes and Genomes (KEGG), flavors, odors, etc. from the Flavor and Extract Manufacturers Association (FEMA), whether it exists in the Food and Drug Administration's SPL data base (FDA/SPL): "Reactive Groups from PubChem; natural products occurrences from LOTUS; bioactivites and risk categories from the Kyoto Encyclopedia of Genes and Genomes (KEGG); flavors, odors, etc. from the Flavor"

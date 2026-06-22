---
name: chemical-name-normalization-and-publish-database-integration
description: Use when after spreadOut() has converted raw CSV peak data into a structured list, when you have one or more Compound.Name entries from GC-MS that may be ambiguous, non-canonical, or missing standardized properties (exact mass, published retention times, reactive groups, database presence).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - R
  - Agilent Unknowns Analysis
  - ChemmineR
  - fmcsR
  - webchem
  - PubChem
  - LOTUS
  - KEGG
  - FEMA
  - FDA/SPL
  techniques:
  - GC-MS
  - tandem-MS
  - NMR
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

# chemical-name-normalization-and-publish-database-integration

## Summary

Normalize chemical compound names from GC-MS output and enrich them with standardized metadata (exact mass, retention time, fragment patterns, literature references) from PubChem, ChemSpider, and other curated databases. This skill ensures that tentatively identified compounds from Agilent Unknowns Analysis are mapped to canonical identities and linked to physicochemical properties required for downstream chemical inference and subsetting.

## When to use

Apply this skill after spreadOut() has converted raw CSV peak data into a structured list, when you have one or more Compound.Name entries from GC-MS that may be ambiguous, non-canonical, or missing standardized properties (exact mass, published retention times, reactive groups, database presence). Use it when downstream analysis requires chemical subsetting by molecular weight, ring count, functional groups, or membership in curated databases (LOTUS, KEGG, FEMA, FDA/SPL).

## When NOT to use

- Input is a pre-filtered, curated chemical database with all properties already populated and validated against reference sources.
- Compound names are already IUPAC systematic or InChI strings with no ambiguity or alternative trivial names.
- Analysis requires only peak detection and quantification without chemical identification or structure-based filtering.

## Inputs

- vector of compound names (character) — e.g. c('Linalool', 'Methyl Salicylate', 'Limonene')
- optional: chemical library data frame for grouping and cross-reference (wide or long format)
- spreadOut() output list (if performing full integration with GC-MS data)

## Outputs

- categorated object — data frame with columns for canonical chemical name, exact mass, molecular weight, ring count, functional group count, atom count, net charge, reactive group membership, and database presence flags (LOTUS, KEGG, FEMA, FDA/SPL, reactives)
- filtered chemical subset (via exactoThese) — vector of compound names meeting user-specified molecular or database criteria

## How to apply

Pass the compound names (either directly or after Match.Factor filtering, e.g., Match.Factor ≥ 65–80) to categorate(), which queries PubChem, ChemSpider, LOTUS, KEGG, FEMA, and FDA/SPL to retrieve exact mass, molecular weight, ring count, functional group counts, atom counts, net charge, reactive groups, and literature retention times. The function returns a categorated object containing a nested data frame with canonical chemical identifiers and all retrieved properties. Use the resulting categorated object with exactoThese() to subset by database membership (e.g., subsetBy='Database', subsetArgs='LOTUS') or molecular properties (e.g., subsetBy='FMCS', subsetArgs='MW', subsetArgs2='Between', subset_input=c(50,115)). Validate that all queried compounds return non-null entries in at least one database; missing entries indicate potential misidentification or typos in the original Compound.Name field.

## Related tools

- **ChemmineR** (Cheminformatics toolkit providing structure parsing, similarity metrics, and property calculation)
- **fmcsR** (Flexible molecular core structure (FMCS) alignment and substructure comparison for grouping and filtering by structural features)
- **webchem** (R interface to PubChem, ChemSpider, and other web-based chemical databases for querying exact mass, reactive groups, and literature metadata)
- **PubChem** (Source of exact mass, reactive groups, and standardized chemical identifiers)
- **LOTUS** (Database of natural products occurrences, used to filter for biologically relevant compounds)
- **KEGG** (Kyoto Encyclopedia of Genes and Genomes — provides bioactivities and risk categories for compounds)
- **FEMA** (Flavor and Extract Manufacturers Association database — classifies compounds as flavoring or extract ingredients)
- **FDA/SPL** (FDA Structured Product Labeling database — indicates whether a compound is approved or listed in pharmaceutical or food products)

## Examples

```
query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene', 'alpha-Thujene'); query_categorated = categorate(query_chemicals); these_chems = exactoThese(query_categorated, subsetBy = 'Database', subsetArgs = c('LOTUS', 'FEMA'))
```

## Evaluation signals

- All queried compound names return non-null entries in the categorated object; missing or NA entries for a compound suggest a name mismatch or non-existent chemical in the underlying databases.
- Exact mass and molecular weight values are populated and match expected ranges (e.g., MW > 0, exact mass within ±5 ppm of nominal mass for typical organics).
- Database membership flags (LOTUS, KEGG, FEMA, FDA/SPL) are consistent with compound class; e.g., volatile esters and terpenes should frequently appear in FEMA and LOTUS.
- Subsequent exactoThese() subsetting produces a non-empty filtered set when criteria are reasonable (e.g., MW between 50–300 for typical GC-amenable compounds); empty results may indicate overly restrictive thresholds or misidentified input names.
- Molecular property counts (rings, atoms, net charges, functional groups) are non-negative integers and internally consistent (e.g., atom count ≥ ring count × 2).

## Limitations

- Compound name queries are case-sensitive and require exact or very close spelling matches in PubChem and ChemSpider; trivial or misspelled names may fail to retrieve metadata.
- Retention time literature values are sparse and may not be available for many compounds; webInfo rtLiterature fields may be empty or highly variable across different column/temperature conditions.
- Web-based database queries (PubChem, ChemSpider, KEGG, FEMA) depend on network availability and rate limits; large batches of compounds may timeout or require throttling.
- Database presence flags (LOTUS, FEMA, FDA/SPL) indicate listing but do not confirm purity, concentration, or biological activity in the user's sample; integration with MS/MS or NMR is recommended for high-confidence identification.

## Evidence

- [other] categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [methods] uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [other] construct eight output matrices: Compounds (chemical identifiers), RT (retention times), MatchFactor (match factors), MZ (observed m/z values), Mass (exact masses from PubChem/ChemSpider), Area (raw peak areas), rtBYmass (unique RT|mass codes), and webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times): "webInfo (nested list of published names, top m/z fragments, exact mass, and literature retention times)"
- [methods] Reactive Groups from PubChem; natural products occurrences from LOTUS; bioactivites and risk categories from the Kyoto Encyclopedia of Genes and Genomes (KEGG); flavors, odors, etc. from the Flavor and Extract Manufacturers Association (FEMA); whether it exists in the Food and Drug Administration's SPL data base (FDA/SPL): "Reactive Groups from PubChem; natural products occurrences from LOTUS; bioactivites and risk categories from the Kyoto Encyclopedia of Genes and Genomes (KEGG); flavors, odors, etc. from the Flavor"
- [readme] exactoThese(query_categorated, subsetBy = 'Database', subsetArgs = c('LOTUS', 'FEMA')): "exactoThese(query_categorated, subsetBy = 'Database', subsetArgs = c('LOTUS', 'FEMA'))"
- [other] exactoThese(input_categorated, subsetBy = 'FMCS', subsetArgs = 'MW', subsetArgs2 = 'Between', subset_input = c(50,115)): "exactoThese(input_categorated, subsetBy = 'FMCS', subsetArgs = 'MW', subsetArgs2 = 'Between', subset_input = c(50,115))"

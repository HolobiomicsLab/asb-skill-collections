---
name: lipid-maps-database-lookup
description: Use when when you have a parsed lipid species table (output from LipidSearch or LIQUID) containing lipid names or identifiers, and you need to annotate each entry with its standardized LIPID MAPS category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - ADViSELipidomics
  - LIPID MAPS
  - LipidSearch
  - LIQUID
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
- parsing lipid species (using LIPID MAPS classification)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-maps-database-lookup

## Summary

Map parsed lipid species names to standardized LIPID MAPS taxonomic classifications (category and subcategory) to produce an annotated species table with chemical identity metadata. This enables downstream analysis and comparison by organizing lipids into a unified classification scheme.

## When to use

When you have a parsed lipid species table (output from LipidSearch or LIQUID) containing lipid names or identifiers, and you need to annotate each entry with its standardized LIPID MAPS category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.g., Phosphatidylcholines) for comparative lipidomics analysis or reporting.

## When NOT to use

- Lipid identities are already annotated with LIPID MAPS classifications — reapplying this skill would be redundant.
- Input is raw instrument data (e.g., mzML, raw LC-MS files) — lipid identification and parsing must occur first.
- Only relative quantification is needed and standardized taxonomic organization is not required for your analysis goal.

## Inputs

- Parsed lipid species table (from LipidSearch or LIQUID output)
- Lipid names or identifiers (column)
- Quantitative data per lipid and sample

## Outputs

- Annotated lipid species table with LIPID MAPS classification fields
- Classification category assignments (e.g., Glycerophospholipids)
- Classification subcategory assignments (e.g., Phosphatidylcholines)

## How to apply

Load the parsed lipid species table containing lipid names or identifiers from upstream lipid identification tools. For each lipid species entry, query the LIPID MAPS database or API to retrieve the corresponding classification hierarchy, extracting both the primary category and subcategory level. Append these classification fields as new columns to the species table, preserving the original lipid names and quantitative data (e.g., abundance values per sample). Validate that all queried lipid names returned valid LIPID MAPS classifications; flag or handle unmatched entries (e.g., novel lipids or annotation ambiguities). Save the enriched table with standardized columns for lipid identifier, classification category, subcategory, and quantitative data.

## Related tools

- **ADViSELipidomics** (Shiny application that orchestrates LIPID MAPS classification lookup and annotation within an integrated lipidomics preprocessing and analysis workflow) — https://github.com/ShinyFabio/ADViSELipidomics
- **LIPID MAPS** (Reference database and API providing standardized lipid classification hierarchy (category and subcategory))
- **LipidSearch** (Upstream lipid identification tool producing parsed species names that serve as input to LIPID MAPS lookup)
- **LIQUID** (Upstream lipid identification tool producing parsed species names that serve as input to LIPID MAPS lookup)

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()
```

## Evaluation signals

- All lipid species names in the input table match to valid LIPID MAPS classifications with no missing values in category and subcategory columns.
- Classification assignments are chemically consistent (e.g., all Phosphatidylcholines are assigned to Glycerophospholipids category, not Sphingolipids).
- The output table retains all original lipid names and quantitative columns; no data loss or reordering occurs during annotation.
- Unmatched or ambiguous lipid names are flagged or logged separately, allowing review of coverage and potential edge cases.
- The annotated table can be used downstream for filtering, grouping, or statistical analysis by lipid class without reimporting or reformatting.

## Limitations

- Novel or non-standard lipid nomenclature may not map to LIPID MAPS classifications, requiring manual curation or fallback handling.
- LIPID MAPS database coverage and version may affect mapping success; older or very recently discovered lipids may have incomplete or absent annotations.
- Query performance scales with table size; large-scale lookups may require batch processing or caching strategies.
- Different lipid naming conventions (e.g., shorthand notation, vendor-specific formats) may require normalization before LIPID MAPS lookup to ensure reliable matching.

## Evidence

- [intro] Parse lipid species using LIPID MAPS classification: "ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification)"
- [other] Map parsed lipid species to classifications: "Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory"
- [other] Append classification fields and save annotated table: "Append the classification fields to the parsed species table. 4. Save the annotated table with lipid names, original quantitative data, and classification fields."
- [readme] Input from LipidSearch or LIQUID: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"

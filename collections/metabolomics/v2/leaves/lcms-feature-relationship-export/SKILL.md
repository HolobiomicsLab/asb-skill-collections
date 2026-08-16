---
name: lcms-feature-relationship-export
description: Use when after ISFrag has completed identification of in-source fragment
  features (Part 4 output), when you need to serialize and inspect the hierarchical
  fragmentation relationships among identified ISF features, or when preparing data
  for visualization or external analysis of fragment lineage and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ISFrag
  - R
  - RStudio
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS
  metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
- we recommend using RStudio to complete the installation and usage of ISFrag
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-feature-relationship-export

## Summary

Export the hierarchical relationship tree of identified in-source fragment (ISF) features from an LCMS feature table, representing structural fragmentation relationships among parent ions and their daughter fragments. This skill captures the parent–child topology of ISF features for downstream interpretation and visualization.

## When to use

After ISFrag has completed identification of in-source fragment features (Part 4 output), when you need to serialize and inspect the hierarchical fragmentation relationships among identified ISF features, or when preparing data for visualization or external analysis of fragment lineage and parent–daughter relationships.

## When NOT to use

- Input feature table has not yet been processed through ISFrag Part 4 (ISF identification); raw LCMS feature tables without ISF feature assignments cannot be used.
- You only need the individual ISF feature annotations and not the structural relationships among fragments.
- Feature table format does not contain parent–daughter ion relationship metadata required by the export function.

## Inputs

- ISF feature table (output from ISFrag Part 4: Identification of ISF Features)
- R environment with ISFrag package loaded

## Outputs

- ISF Relationship Tree artifact (exported in specified format, e.g., text file, CSV, or structured data frame)

## How to apply

Load the ISFrag R package and the feature table output from Part 4 (ISF identification results). The ISFrag relationship tree export function (Part 5.2) organizes ISF features and their parent ions hierarchically according to fragmentation relationships detected during the identification step. Call the dedicated export function to serialize the tree structure into the specified output format (typically a text or data-frame representation). The function constructs the relationship tree by traversing parent–daughter ion associations stored in the ISF feature table and exporting them in a format that preserves the hierarchical topology.

## Related tools

- **ISFrag** (R package providing the dedicated export function (Part 5.2) for serializing ISF Relationship Tree structures) — https://github.com/HuanLab/ISFrag.git
- **R** (Language runtime for executing ISFrag package and export functions (version 4.0.0 or above required))
- **RStudio** (Recommended IDE for running ISFrag package, loading feature tables, and executing export workflow)

## Examples

```
# Load ISFrag and the ISF feature table from Part 4
library(ISFrag)
isfFT <- readRDS('Part4_ISF_features.rds')
# Export the ISF Relationship Tree using ISFrag's export function
export.ISF.relationship.tree(isfFT, output_format='csv', output_file='ISF_relationship_tree.csv')
```

## Evaluation signals

- Exported relationship tree file is generated without errors and contains entries for all identified ISF features from Part 4 output.
- Parent–daughter ion relationships are correctly represented in the tree structure (verify by spot-checking parent m/z values match expected fragmentation patterns).
- Tree structure preserves hierarchical topology: each fragment feature links to its parent ion, and no circular references exist.
- Output file format matches the expected schema (row/column structure for CSV exports, or object schema for data-frame exports).
- Exported tree can be successfully re-imported or parsed by downstream analysis tools without truncation or schema violations.

## Limitations

- Export function output format is dependent on ISFrag version and may require parsing into alternative formats for external tools.
- Relationship tree reflects only fragmentation relationships identified during Part 4; relationships not detected by ISFrag's algorithms will not appear in the export.
- Export does not include quantitative intensity or annotation metadata beyond the structural relationships; integration with Part 5.1 (ISF Result Feature Table export) may be needed for complete feature annotation.

## Evidence

- [other] ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree: "ISFrag includes a dedicated export function (Part 5.2) for exporting the ISF Relationship Tree, which represents the structural relationships among identified in-source fragment features."
- [other] Construct the relationship tree by organizing ISF features hierarchically: "Construct the relationship tree by organizing ISF features and their parent ions hierarchically according to fragmentation relationships."
- [other] Export function to produce a relationship tree artifact: "Export the relationship tree structure using ISFrag's export function to produce a relationship tree artifact in the specified output format."
- [readme] Part 5: Results Export section includes Part 5.2 for ISF Relationship Tree: "Part 5: Results Export
    - [5.1 Export ISF Result Feature
        Table](#51-export-isf-result-feature-table)
    - [5.2 Export ISF Relationship
        Tree](#52-export-isf-relationship-tree)"

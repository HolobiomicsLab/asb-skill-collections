---
name: lcms-result-table-structure
description: Use when after completing Part 4 (Identification of ISF Features) in the ISFrag workflow, when you have an analysis results object containing identified ISF features and need to generate a shareable, tabular export that documents feature annotations, hierarchical parent–fragment relationships, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - ISFrag
  - R
  - RStudio
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table
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
---

# Reconstruct the ISF Result Feature Table export

## Summary

Export identified in-source fragment (ISF) features from ISFrag analysis into a structured result feature table file (CSV/TSF format) with feature identifiers, ISF annotations, parent–fragment relationships, and confidence scores for downstream analysis and reporting.

## When to use

After completing Part 4 (Identification of ISF Features) in the ISFrag workflow, when you have an analysis results object containing identified ISF features and need to generate a shareable, tabular export that documents feature annotations, hierarchical parent–fragment relationships, and detection confidence for publication, archival, or integration with external metabolomics databases.

## When NOT to use

- ISF identification has not yet been completed (Part 4 has not been run); export Part 2 or Part 3 output instead.
- The goal is to export the ISF Relationship Tree structure; use Part 5.2 export function instead.
- Input feature table does not contain ISF annotations; run ISF identification first.

## Inputs

- ISFrag analysis results object (from Part 4 containing identified ISF features)
- Feature identifiers and m/z, retention time coordinates
- ISF annotations (fragment type, neutral loss information)
- Parent–fragment relationship pairs
- Confidence scores for each identified ISF

## Outputs

- ISF Result Feature Table (CSV or TSV file)
- Structured tabular export with columns: feature ID, m/z, retention time, ISF annotation, parent feature ID, confidence score

## How to apply

Load the ISFrag analysis results object (from Part 4) containing identified ISF features into the R environment. Format the identified ISF features into a tabular result structure with columns for feature identifiers, ISF annotations (e.g., fragment type, neutral loss mass), parent–fragment relationships (indicating which features are fragments of which parent ions), and confidence scores. Apply ISFrag's Part 5.1 export function to serialize the formatted result feature table to a standard delimited file format (CSV or TSF). Verify that all identified ISF features are represented, that parent–fragment links are bidirectionally consistent, and that confidence scores fall within the expected range used during identification.

## Related tools

- **ISFrag** (R package providing Part 5.1 export function to output ISF Result Feature Table from identified ISF features) — https://github.com/HuanLab/ISFrag.git
- **R** (Language runtime for executing ISFrag export functions; version 4.0.0 or above required)
- **RStudio** (Recommended IDE for executing ISFrag export workflow and inspecting exported result tables)

## Examples

```
# After loading ISFrag and completing Part 4 identification:
library(ISFrag)
# isf_results is the output object from Part 4
# export.ISF.result.featuretable(isf_results, output_dir="./results", file_format="csv")
```

## Evaluation signals

- Exported file is readable as CSV/TSV and parses without delimiter or encoding errors
- All identified ISF features from Part 4 results object are represented as rows in the export
- Parent–fragment relationship pairs are bidirectionally consistent: if feature F_A lists F_B as parent, then F_B's record shows F_A in its fragment list or parent–fragment edge
- Confidence scores for all ISF features are present and numeric, within the range [0, 1] or the scale specified by ISFrag's identification thresholds
- Feature identifiers, m/z, and retention time values are populated and match source analysis results object

## Limitations

- Export only captures features identified as ISF in Part 4; non-ISF features or features with low confidence below the identification threshold are excluded.
- The export does not include MS2 annotation details or adduct/isotope information from Part 3; those require separate export or custom post-processing.
- CAMERA adduct and isotope annotation are available only for XCMS-extracted features; custom feature tables do not support this annotation layer in export.

## Evidence

- [other] Part 5.1 export function to output ISF Result Feature Table: "ISFrag provides a Part 5.1 export function to output ISF Result Feature Table from identified ISF features as a structured result file."
- [other] Tabular structure with feature identifiers, ISF annotations, parent–fragment relationships, and confidence scores: "Format the identified ISF features into a tabular result structure with appropriate columns (feature identifiers, ISF annotations, parent–fragment relationships, confidence scores)."
- [other] Export to CSV or TSV format using ISFrag's export functionality: "Export the formatted result feature table to a standard file format (CSV or TSV) using ISFrag's export functionality."
- [readme] Workflow step: load ISFrag analysis results from Part 4: "Load the ISFrag analysis results object containing identified ISF features from Part 4 (Identification of ISF Features)."
- [readme] Part 5: Results Export with subsection 5.1 and 5.2: "Part 5: Results Export
    - [5.1 Export ISF Result Feature
        Table](#51-export-isf-result-feature-table)
    - [5.2 Export ISF Relationship
        Tree](#52-export-isf-relationship-tree)"

---
name: parent-fragment-relationship-mapping
description: Use when after ISF features have been identified in Part 4 of the ISFrag workflow and you need to export or visualize the hierarchical structure of detected in-source fragments relative to their parent ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ISFrag
  - R
  - RStudio
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# parent-fragment-relationship-mapping

## Summary

A method to establish and represent hierarchical relationships between parent metabolite features and their identified in-source fragments (ISF) within LCMS metabolite feature tables. This skill is essential for disambiguating false-positive features that arise from in-source fragmentation and organizing results into parent–fragment dependency structures.

## When to use

Apply this skill after ISF features have been identified in Part 4 of the ISFrag workflow and you need to export or visualize the hierarchical structure of detected in-source fragments relative to their parent ions. Use it when preparing results for downstream interpretation or when the analysis must distinguish true metabolite features from fragmentation artifacts.

## When NOT to use

- MS1 feature extraction has not yet been completed or no ISF identification has been performed in Part 4.
- Input data lacks MS2 annotation or retention time alignment information required to infer valid parent–fragment pairs.
- The analysis is focused only on feature detection without the need to distinguish in-source fragments from true metabolite features.

## Inputs

- ISFrag analysis results object containing identified ISF features (output from Part 4: Identification of ISF Features)
- MS1 feature table with m/z, retention time, and intensity columns
- MS2 annotation data linked to features

## Outputs

- ISF Result Feature Table with parent–fragment relationships, feature identifiers, ISF annotations, and confidence scores (CSV or TSV format)
- ISF Relationship Tree showing hierarchical parent–fragment dependency structure

## How to apply

Load the ISFrag analysis results object containing identified ISF features from Part 4. The ISFrag package internally computes parent–fragment mass differences and retention time co-elution patterns to infer dependency relationships. Format these relationships into a structured representation that captures feature identifiers, parent–fragment annotations, confidence scores, and hierarchical parent–child links. The relationship mapping leverages the MS1 m/z, retention time, and MS2 annotation alignment to establish valid parent–fragment pairs; features with mass deficits consistent with common neutral losses and co-eluting retention times are linked as fragments of a parent ion. Export the mapped relationships as part of the ISF Result Feature Table or as a dedicated ISF Relationship Tree file (Part 5.1 or 5.2) in CSV, TSV, or tree format for downstream use.

## Related tools

- **ISFrag** (R package that performs ISF identification and provides functions to map parent–fragment relationships and export results as structured tables or trees) — https://github.com/HuanLab/ISFrag.git
- **R** (Runtime environment for executing ISFrag and manipulating the relationship data structures)
- **RStudio** (Recommended IDE for completing ISFrag installation and running the parent–fragment relationship mapping workflow)

## Examples

```
library(ISFrag); isfrag_results <- ISFrag(featuretable = xcmsFT, ms2data = ms2_annotated); export_isf_result(isfrag_results, output_format = "csv", file = "ISF_result_feature_table.csv")
```

## Evaluation signals

- Verify that all identified ISF features in the results object are assigned to a parent feature with a valid mass difference corresponding to known neutral losses.
- Check that parent–fragment pairs share similar retention times (co-elution constraint) with differences within expected chromatographic peak width.
- Confirm that the exported relationship table contains non-null parent identifiers, fragment identifiers, mass differences, confidence scores, and ISF annotations for all records.
- Validate that the ISF Relationship Tree output shows a coherent hierarchical structure with no orphaned fragments or circular parent–fragment links.
- Cross-check that mapped relationships are consistent with MS2 fragmentation patterns observed in the annotation data.

## Limitations

- Parent–fragment relationship mapping relies on accurate MS1 feature extraction and MS2 annotation; errors or gaps in earlier workflow stages (Part 2–3) propagate into incorrect relationship assignments.
- CAMERA adduct and isotope annotation features are available only for XCMS-based analysis; custom feature tables cannot leverage these annotations to refine parent–fragment inference.
- Relationship mapping may fail or be ambiguous for features with overlapping retention times or mass values close to common neutral loss thresholds, potentially leading to false or missing parent–fragment links.
- The ISFrag package does not account for in-source fragmentation patterns specific to non-standard ionization modes or unusual sample matrices; results are calibrated primarily for standard DDA/DIA LCMS data.

## Evidence

- [other] ISFrag provides a Part 5.1 export function to output ISF Result Feature Table from identified ISF features as a structured result file.: "ISFrag provides a Part 5.1 export function to output ISF Result Feature Table from identified ISF features as a structured result file."
- [other] Format the identified ISF features into a tabular result structure with appropriate columns (feature identifiers, ISF annotations, parent–fragment relationships, confidence scores).: "Format the identified ISF features into a tabular result structure with appropriate columns (feature identifiers, ISF annotations, parent–fragment relationships, confidence scores)."
- [other] Load the ISFrag analysis results object containing identified ISF features from Part 4 (Identification of ISF Features).: "Load the ISFrag analysis results object containing identified ISF features from Part 4 (Identification of ISF Features)."
- [readme] ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.: "ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table."
- [readme] Part 5: Results Export — 5.1 Export ISF Result Feature Table — 5.2 Export ISF Relationship Tree: "Part 5: Results Export — 5.1 Export ISF Result Feature Table — 5.2 Export ISF Relationship Tree"

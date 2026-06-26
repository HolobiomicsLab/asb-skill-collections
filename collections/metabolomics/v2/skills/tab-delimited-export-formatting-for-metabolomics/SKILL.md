---
name: tab-delimited-export-formatting-for-metabolomics
description: Use when after completing batch normalization and quality control filtering
  on a Metaboprep object, when you need to share processed metabolomics data with
  collaborators, import into other statistical packages, or archive results in a platform-independent
  format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - rmarkdown
  - knitr
  - ggplot2
  - metaboprep
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
- '%\VignetteEngine{knitr::rmarkdown}'
- library(ggplot2)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac059/6522114
  all_source_dois:
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tab-delimited-export-formatting-for-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Export processed metabolite data, sample metadata, and feature metadata from a Metaboprep object into tab-delimited text files (.txt/.tsv) for downstream analysis in external tools. This skill enables interoperability by converting in-memory R objects into portable, standard tabular formats.

## When to use

After completing batch normalization and quality control filtering on a Metaboprep object, when you need to share processed metabolomics data with collaborators, import into other statistical packages, or archive results in a platform-independent format. Trigger: you have a post-QC Metaboprep object and require tab-delimited outputs.

## When NOT to use

- Input is already in tab-delimited format and requires no further conversion
- You need to preserve intermediate QC layers (use export with format='all' or other multi-layer options instead)
- Downstream analysis requires native R Metaboprep object methods (e.g. feature_summary, sample_summary with tree_cut_height)

## Inputs

- Metaboprep object (post-quality_control)
- Output directory path (string)

## Outputs

- Tab-delimited processed data matrix (.txt or .tsv)
- Tab-delimited sample metadata (.txt or .tsv)
- Tab-delimited feature metadata (.txt or .tsv)

## How to apply

Load a quality-controlled Metaboprep object (post-batch_normalise and post-quality_control). Call the export() function with format='metaboprep' and specify an output directory; this writes three tab-delimited files: the processed data matrix, sample metadata (with exclusion flags and annotations), and feature metadata (with biochemical identifiers and exclusion codes). Verify file creation and check that row/column counts match expected sample and feature counts post-filtering. The export captures the final 'qc' data layer and all associated metadata, making it suitable for external validation, visualization, or statistical modeling.

## Related tools

- **metaboprep** (R package containing export() function and Metaboprep class definition) — https://github.com/MRCIEU/metaboprep
- **R** (Host language for Metaboprep object manipulation and export execution)

## Examples

```
export(mydata, directory = output_dir, format = "metaboprep")
```

## Evaluation signals

- Three tab-delimited files are created in the specified output directory with expected naming convention
- File row counts match number of retained samples (post-exclusion) and feature counts (post-exclusion)
- Sample metadata includes exclusion-related columns (reason_excluded, excluded flag)
- Feature metadata includes biochemical annotation columns (metabolite_id, pathway, kegg, group_hmdb) and exclusion codes
- Tab-delimited format can be successfully read into external tools (e.g., pandas, base R read.table, spreadsheet software) without parsing errors

## Limitations

- Export does not include visualization outputs (dendrogram trees, PCA plots); generate_report() should be used for HTML report and plots
- Floating-point precision may be affected by tab-delimited serialization; verify precision matches original data layer if needed for very strict comparisons
- No built-in version tracking or provenance metadata in the exported files; document Metaboprep version and QC parameters separately

## Evidence

- [methods] Call export() with format='metaboprep' to write processed data, sample metadata, and feature metadata as tab-delimited text files: "Call export() with format='metaboprep' to write processed data, sample metadata, and feature metadata as tab-delimited text files to the specified output directory."
- [readme] metaboprep generates tab-delimited text file outputs suitable for use elsewhere: "Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere"
- [methods] Verify that tab-delimited exports exist after export function call: "Verify that the HTML report file (project_name_metaboprep_qc_report.html) and associated tab-delimited exports (.txt/.tsv) exist in the output directory."
- [readme] metaboprep provides tab-delimited text file and HTML report as summary outputs: "Provide useful summary data in the form of tab-delimited text file and a html report"

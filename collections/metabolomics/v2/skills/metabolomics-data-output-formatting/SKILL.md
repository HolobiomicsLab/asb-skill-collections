---
name: metabolomics-data-output-formatting
description: Use when after completing feature annotation with the annotateRC function on LC–MS All-ion fragmentation (AIF) datasets, when you need to persist ranked metabolite candidates, matched ion spectra, and global summary tables to disk for archival, manual review, or integration into downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-output-formatting

## Summary

Export annotated LC–MS metabolomics features and their ranked candidate matches to a multi-format output directory, including global results tables, ranked results per feature, ranked spectra PDFs, and pseudo-MS/MS MGF files. This skill ensures reproducible, auditable dissemination of annotation outputs suitable for downstream curation and publication.

## When to use

After completing feature annotation with the annotateRC function on LC–MS All-ion fragmentation (AIF) datasets, when you need to persist ranked metabolite candidates, matched ion spectra, and global summary tables to disk for archival, manual review, or integration into downstream metabolomics pipelines.

## When NOT to use

- You have not yet run annotateRC on your feature set — saveAnnotations requires a populated annotations object as input.
- Your output directory is read-only or has insufficient disk space for the full output set (global table + per-feature PDFs + MGF file).
- You only need the ranked candidate list and do not require spectra visualizations or pseudo-MS/MS export for downstream tools.

## Inputs

- MetaboAnnotatoR annotations object (from annotateRC function)
- Output directory path (user-specified, writable)

## Outputs

- Global results table (CSV/TSV format)
- Ranked results file (CSV/TSV, one row per feature with candidate metadata)
- Ranked spectra PDF files (one PDF per annotated feature, showing matched ions)
- Pseudo-MS/MS MGF file (all pseudo-MS/MS spectra in MGF format)

## How to apply

Call the saveAnnotations function with a MetaboAnnotatoR annotations object (output from annotateRC) and a target directory path, enabling all save flags to write the full output set: global results table, ranked results file (one row per feature with top-ranked candidates), individual ranked spectra PDF files (one per feature showing ion matches), and a pseudo-MS/MS MGF file for all spectra. The function writes outputs in standard formats (CSV/TSV tables, PDF visualizations, MGF spectral format) to facilitate review and reuse. Verify completion by enumerating all generated files, checking that each is non-empty (file size > 0 bytes), and confirming the presence of expected file types matching the number of annotated features and candidate matches.

## Related tools

- **MetaboAnnotatoR** (Core R package providing saveAnnotations function and annotations object structure; handles multi-format export of ranked metabolite matches, spectra visualizations, and pseudo-MS/MS data.) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher required) for executing saveAnnotations and managing annotations objects.)

## Examples

```
saveAnnotations(annotations = annotated_features, output_dir = './results/', write_global = TRUE, write_ranked = TRUE, write_spectra_pdf = TRUE, write_msp = TRUE)
```

## Evaluation signals

- Global results file exists and is non-empty (size > 0 bytes), containing annotated features and summary match statistics.
- Ranked results file exists and is non-empty, with one row per feature and columns for candidate metabolite name, database match score, and ion match count.
- Number of ranked spectra PDF files equals the number of annotated features; each PDF is non-empty and contains visualization of pseudo-MS/MS spectrum with matched ions highlighted.
- Pseudo-MS/MS MGF file exists and is non-empty, with proper MGF header fields (BEGIN IONS / END IONS blocks) and at least one spectrum per annotated feature.
- All output files are written to the specified directory without errors; file enumeration and size checks confirm no truncation or write failures.

## Limitations

- Output format is tied to MetaboAnnotatoR's internal structure; custom export schemas or filtering of ranked candidates before export is not documented.
- No changelog or version history is available for MetaboAnnotatoR, limiting reproducibility tracking across package updates.
- PDF and MGF file generation performance and scalability for large feature sets (>1000 features) is not discussed in the article.
- The function does not support selective export of output file types; all flags must be individually specified to control which outputs are written.

## Evidence

- [intro] saveAnnotations function writes output files: "Call saveAnnotations with the annotations object and a temporary directory path as output destination."
- [intro] Multi-format output types produced by saveAnnotations: "Verify presence of global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file."
- [intro] Full output set from saveAnnotations includes tables, PDFs, and MGF files: "The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files to a temporary directory, with all"
- [intro] Save outputs to user-specified directory: "It is possible to save the annotation results to a user-specified directory"
- [intro] Non-empty file validation: "Check that each file is non-empty (file size > 0 bytes)."

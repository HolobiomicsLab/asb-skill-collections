---
name: annotation-object-manipulation
description: Use when after completing metabolite annotation of LC-MS AIF features
  using the annotateRC function, when you need to persist ranked candidate matches,
  inspect multiple candidate annotations per feature, visualize matched ions in ranked
  spectra, or export pseudo-MS/MS spectra for external analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnnotatoR
  - R
  - RamClustR
  - xcms
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS
  All-ion fragmentation (AIF) datasets
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotation-object-manipulation

## Summary

Manipulate and export MetaboAnnotatoR annotation objects (output from annotateRC) to produce structured results files, ranked candidate lists, annotated spectra visualizations, and pseudo-MS/MS data in standard formats. This skill bridges metabolite annotation workflows and downstream analysis by persisting and organizing ranked candidate matches with their spectral evidence.

## When to use

After completing metabolite annotation of LC-MS AIF features using the annotateRC function, when you need to persist ranked candidate matches, inspect multiple candidate annotations per feature, visualize matched ions in ranked spectra, or export pseudo-MS/MS spectra for external analysis platforms. Specifically apply this skill when the annotation run has produced an annotations object containing ranked candidates and you require outputs in multiple formats (global results table, ranked results, PDF visualizations, MGF pseudo-MS/MS).

## When NOT to use

- Input is not a completed MetaboAnnotatoR annotations object (e.g., raw peak table or unprocessed xcms/RamClustR objects without annotation results)
- Output directory does not exist or is not writable by the R process
- Annotation run failed or annotateRC did not complete successfully, leaving annotations object incomplete or corrupted

## Inputs

- MetaboAnnotatoR annotations object (output from annotateRC function containing ranked candidate matches)
- Output directory path (character string, must be writable)

## Outputs

- Global results table file (CSV or tabular format, all features and top-ranked candidates)
- Ranked results file (CSV or tabular format, all candidates per feature with ranking scores)
- Ranked spectra PDF files (one PDF per annotated feature, showing matched ions for each ranked candidate)
- Pseudo-MS/MS MGF file (standard MGF format containing pseudo-MS/MS spectra derived from AIF data)

## How to apply

Load the annotations object returned by annotateRC, which contains feature IDs, ranked candidate metabolites, and matched fragment ions. Call saveAnnotations with the annotations object and specify an output directory path; enable all save flags to write the complete set of outputs: global results file (summary across all features), ranked results file (per-feature candidate lists), ranked spectra PDFs (one per feature showing matched ions), and pseudo-MS/MS MGF file (spectral data in standard format). The function writes all expected output file types to disk without errors. Enumerate the output files to verify presence of global results table, ranked results file, ranked spectra PDF files (one per annotated feature), and the pseudo-MS/MS MGF file. Check that each file is non-empty (file size > 0 bytes) to confirm successful serialization.

## Related tools

- **MetaboAnnotatoR** (Core R package providing annotateRC and saveAnnotations functions for metabolite annotation and result export) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher required) for executing MetaboAnnotatoR functions)
- **RamClustR** (Upstream tool that generates pseudo-MS/MS spectra from AIF chromatograms, whose output is annotated by MetaboAnnotatoR)
- **xcms** (Upstream tool for LC-MS peak-picking and feature detection, whose output is processed alongside RamClustR spectra by MetaboAnnotatoR)

## Examples

```
saveAnnotations(annotations_object, output_dir = './annotation_results', save_global_results = TRUE, save_ranked_results = TRUE, save_ranked_spectra_pdfs = TRUE, save_pseudo_ms_mgf = TRUE)
```

## Evaluation signals

- All expected output files are present in the specified directory: global results table, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file
- Each output file has file size > 0 bytes (non-empty files indicating successful write)
- Ranked spectra PDF files contain matched ion annotations and visualizations for each ranked candidate per feature
- Global results table and ranked results file contain consistent feature IDs, candidate metabolite names, and match scores across outputs
- Pseudo-MS/MS MGF file conforms to standard MGF format (parseable by external tools) with pseudo-MS/MS spectra derived from AIF data

## Limitations

- No changelog found in the repository — version history and updates are not documented, limiting reproducibility tracking
- saveAnnotations requires all input parameters (annotations object and output directory) to be correctly specified; no automatic error recovery or fallback defaults
- PDF generation for ranked spectra depends on successful prior annotation; if annotateRC fails or produces incomplete results, PDF outputs may be missing or malformed
- MGF pseudo-MS/MS export depends on valid RamClustR pseudo-spectra in the annotations object; incompatible or corrupted spectra will not serialize correctly

## Evidence

- [other] saveAnnotations function successfully writes all expected output file types: "The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files to a temporary directory, with all"
- [intro] Workflow steps for annotations object manipulation after annotateRC: "annotations can be performed using the *annotateRC* function"
- [intro] Inspection and visualization of ranked candidates from annotations object: "It is also possible to inspect if there were other candidate annotations for a given feature"
- [intro] Spectral visualization with matched ions in ranked candidates: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [intro] Export of annotation results to specified directory: "It is possible to save the annotation results to a user-specified directory"
- [readme] Core function purpose and input requirements: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases."

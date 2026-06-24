---
name: metabolite-annotation-result-export
description: Use when after running the annotateRC function on LC-MS All-ion fragmentation
  (AIF) features and obtaining a populated annotations object with ranked candidate
  matches, use this skill when you need to persist results to disk for archival, sharing,
  or downstream interpretation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnnotatoR
  - R
  techniques:
  - LC-MS
  license_tier: restricted
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

# metabolite-annotation-result-export

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Export completed metabolite annotations from a MetaboAnnotatoR annotations object to a user-specified directory as a suite of structured output files (global results table, ranked results per feature, ranked spectra PDFs, and pseudo-MS/MS MGF). This skill ensures all annotation results are serialized in standardized, reusable formats for downstream analysis and reporting.

## When to use

After running the annotateRC function on LC-MS All-ion fragmentation (AIF) features and obtaining a populated annotations object with ranked candidate matches, use this skill when you need to persist results to disk for archival, sharing, or downstream interpretation (e.g., manual curation of top-ranked candidates, integration with other metabolomics pipelines, or generation of publication-quality spectra visualizations).

## When NOT to use

- If the annotations object is empty or contains no annotated features
- If the output directory path is read-only or does not exist and cannot be created
- If you only need to inspect top-ranked candidates interactively and do not require persistent file export

## Inputs

- MetaboAnnotatoR annotations object (from annotateRC output)
- Output directory path (must be writable)

## Outputs

- Global results table (consolidated annotation summary)
- Ranked results file (per-feature candidate rankings)
- Ranked spectra PDFs (one per feature, showing matched ions)
- Pseudo-MS/MS MGF file (combined fragmentation spectra)

## How to apply

Invoke the saveAnnotations function with the annotations object (output from annotateRC) and a valid output directory path. Enable all save flags (save global results, ranked results, ranked spectra PDFs, and pseudo-MS/MS MGF) to write the complete annotation output set. The function will automatically enumerate all annotated features and generate one ranked results file per feature, one PDF per ranked spectrum visualization, and a single combined MGF file containing all pseudo-MS/MS spectra. Verify that all expected file types are present in the output directory and that each file is non-empty (file size > 0 bytes) before downstream use.

## Related tools

- **MetaboAnnotatoR** (Provides saveAnnotations function and manages annotation object serialization) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Execution environment (version 4.5.0 or higher required))

## Examples

```
saveAnnotations(annotations_obj, output_dir = "/path/to/results", saveGlobal = TRUE, saveRanked = TRUE, savePDF = TRUE, saveMGF = TRUE)
```

## Evaluation signals

- All expected output files are present in the specified directory (global results, ranked results, ranked spectra PDFs for each feature, MGF file)
- Each output file has size > 0 bytes (non-empty validation)
- Ranked results files contain valid tabular data with candidate metabolite names, match scores, and feature identifiers
- Ranked spectra PDFs render without errors and display ion-matched spectra with peak annotations
- MGF file parses without errors and contains valid MS1/MS2 spectrum entries in standard MGF format

## Limitations

- Requires a fully annotated annotations object from annotateRC; will fail or produce empty outputs if no features were successfully matched to fragment libraries
- PDF generation depends on system graphics libraries; some headless/containerized environments may require additional X11 or graphics device configuration
- MGF file combines all spectra into a single file; very large annotation runs may produce large MGF files that require memory-efficient parsing downstream
- No built-in versioning or overwrite protection; re-running saveAnnotations to the same directory will overwrite existing files without warning

## Evidence

- [other] The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files to a temporary directory, with all save flags enabled to write the full set of annotation outputs.: "Call saveAnnotations with the annotations object and a temporary directory path as output destination... Verify presence of global results file, ranked results file, ranked spectra PDF files (one per"
- [intro] It is possible to save the annotation results to a user-specified directory: "It is possible to save the annotation results to a user-specified directory"
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [other] Check that each file is non-empty (file size > 0 bytes).: "Check that each file is non-empty (file size > 0 bytes)."
- [intro] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode.: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."

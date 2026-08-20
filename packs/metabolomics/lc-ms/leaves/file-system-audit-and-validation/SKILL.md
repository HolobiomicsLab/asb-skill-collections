---
name: file-system-audit-and-validation
description: Use when after invoking the saveAnnotations function on a MetaboAnnotatoR annotations object to confirm that all four expected output file types (global results file, ranked results file, per-feature ranked spectra PDFs, and pseudo-MS/MS MGF file) have been written to the output directory without.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-system-audit-and-validation

## Summary

Verify that a metabolomics annotation pipeline has successfully written all expected output file types to a specified directory, and that each file is non-empty and complete. This skill ensures data integrity and traceability by enumerating and validating the presence, format, and size of annotation results including global results tables, ranked candidate matches, ranked spectra PDFs, and pseudo-MS/MS MGF files.

## When to use

Apply this skill after invoking the saveAnnotations function on a MetaboAnnotatoR annotations object to confirm that all four expected output file types (global results file, ranked results file, per-feature ranked spectra PDFs, and pseudo-MS/MS MGF file) have been written to the output directory without truncation or loss. Use it as a validation checkpoint when automating metabolite annotation workflows or when output directory permissions or disk space may be uncertain.

## When NOT to use

- saveAnnotations has not yet been called — use this skill only after annotation results have been explicitly written to disk.
- Output directory path is unknown or variable — resolve the exact destination path before applying this skill.
- Annotation object is empty or contains no annotated features — audit will succeed vacuously but provide no meaningful validation.

## Inputs

- MetaboAnnotatoR annotations object (output from annotateRC function)
- output directory path (specified to saveAnnotations)

## Outputs

- Audit report documenting file names, formats, sizes, and completion status
- Enumeration of all files in output directory
- Validation summary (all expected file types present and non-empty)

## How to apply

After calling saveAnnotations with all save flags enabled (global results, ranked results, ranked spectra PDFs, and MGF output), enumerate all files in the specified output directory. Verify the presence of: (1) a single global results table (e.g., CSV format summarizing all features and top-ranked annotations); (2) a ranked results file (detailed per-feature candidate lists); (3) one PDF file per annotated feature containing ranked spectra with matched ions; and (4) a single pseudo-MS/MS MGF file. For each file, confirm file size > 0 bytes to ensure the file was not truncated or created empty. Document file names, formats, sizes, and completion status in an audit report. This validation guards against silent failures where files may be created but remain empty due to permission issues, disk space exhaustion, or function errors.

## Related tools

- **MetaboAnnotatoR** (Generates annotation results object and provides saveAnnotations function for writing outputs; this skill validates the completeness of its file system operations.) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment for executing file enumeration, size checking, and audit report generation logic.)

## Examples

```
files <- list.files(output_dir, full.names=TRUE); file_info <- data.frame(name=basename(files), size=file.size(files)); print(file_info[file_info$size > 0,])
```

## Evaluation signals

- Global results file is present and file size > 0 bytes
- Ranked results file is present and file size > 0 bytes
- At least one ranked spectra PDF file exists for each annotated feature
- Pseudo-MS/MS MGF file is present and file size > 0 bytes
- Audit report can be successfully generated with no file I/O errors or permission warnings

## Limitations

- This skill validates only file presence and size; it does not verify file content correctness, internal structure, or data consistency.
- Silent corruption or partial writes that produce non-zero file size may not be detected — consider adding downstream schema or checksum validation.
- File permissions and disk space issues are detected only indirectly through missing or empty files; pre-flight checks on directory access and available space are not included.
- No changelog or version history is documented for MetaboAnnotatoR, limiting traceability of changes to saveAnnotations behavior across releases.

## Evidence

- [other] The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files to a temporary directory, with all save flags enabled to write the full set of annotation outputs.: "The saveAnnotations function is invoked with parameters to save global annotations, ranked results, ranked spectra as PDFs, and pseudo-MS/MS spectra as MGF files"
- [other] Verify presence of global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file. Check that each file is non-empty (file size > 0 bytes).: "Verify presence of global results file, ranked results file, ranked spectra PDF files (one per feature), and pseudo-MS/MS MGF file. Check that each file is non-empty (file size > 0 bytes)"
- [other] Produce an audit report documenting file names, formats, sizes, and completion status.: "Produce an audit report documenting file names, formats, sizes, and completion status"
- [intro] It is possible to save the annotation results to a user-specified directory: "It is possible to save the annotation results to a user-specified directory"

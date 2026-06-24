---
name: ms-dial-output-parsing
description: Use when you have completed peak picking in MS-DIAL (generating files
  like Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) and need to load the resulting
  feature table into R for quality control, feature filtering, normalization, or metabolite
  annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - margheRita
  - R
  - MS-Dial
  - notame
  - MS-DIAL
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
- margheRita is intended to be used after having done a number of data acquisition
  steps through MS-Dial
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS-DIAL output parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and load MS-DIAL peak tables (feature tables with m/z, retention time, and intensity values) into a structured metabolomics data object for downstream preprocessing and analysis. This is the critical entry point for untargeted LC-MS/MS workflows, converting vendor-independent MS-DIAL output into a format compatible with quality control, filtering, and statistical analysis pipelines.

## When to use

You have completed peak picking in MS-DIAL (generating files like Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) and need to load the resulting feature table into R for quality control, feature filtering, normalization, or metabolite annotation. The input is an MS-DIAL text export containing feature identifiers, m/z values, retention times, and sample intensity columns.

## When NOT to use

- The input is already a processed feature table (normalized, imputed, or filtered); use this skill only on raw MS-DIAL exports.
- You are working with targeted metabolomics data (e.g., multiple reaction monitoring, MRM); this skill is designed for untargeted data-independent or data-dependent acquisition.
- The MS-DIAL file has been manually edited or reformatted outside MS-DIAL; verify column headers and data integrity before parsing.

## Inputs

- MS-DIAL feature table (text export, e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt)
- Sample metadata spreadsheet (optional, e.g., group labels, batch assignments, quality flags)

## Outputs

- Structured metabolomics data object (margheRita object or compatible SummarizedExperiment/metaboset)
- Feature metadata matrix (m/z, retention time, adduct, feature identifier)
- Sample annotation table (sample names, group, batch, QC status)

## How to apply

Load the MS-DIAL output file (typically .txt format with tab or space delimiters containing feature metadata and a sample-by-feature abundance matrix) into a structured data object that preserves feature annotations (m/z, RT, adduct information) and sample metadata simultaneously. The margheRita package provides loading functions that convert MS-DIAL exports into an internal S3 or S4 object that tracks features, samples, and metadata together, enabling downstream operations like mass defect filtering, CV-based filtering, and missing value imputation to reference both feature and sample dimensions without separate matrix juggling. The parsing must preserve floating-point m/z precision (typically 4–8 decimal places) and handle optional columns for quality metrics (e.g., QC flags, blank/sample annotations) if present in the MS-DIAL export.

## Related tools

- **margheRita** (Provides the primary loading and data structure functions for MS-DIAL output; encapsulates feature and sample metadata in a unified object for downstream filtering and annotation) — https://github.com/emosca-cnr/margheRita
- **notame** (Alternative R package for reading MS-DIAL Excel spreadsheets and creating a custom metabolomics object; supports drift correction, QC flagging, and batch effect correction post-parsing) — https://github.com/hanhineva-lab/notame
- **MS-DIAL** (Peak picking and feature detection software that generates the input feature tables parsed by this skill) — http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/
- **Biobase** (Provides SummarizedExperiment or ExpressionSet classes compatible with margheRita export functions)

## Evaluation signals

- The parsed object retains the full feature count and sample count from the MS-DIAL export without row/column loss; spot-check by comparing dim() of the object to the input file row/column counts.
- Feature metadata (m/z, retention time, adduct information) are preserved with full floating-point precision and are accessible via dedicated accessors (e.g., features(), featureData(), or equivalent).
- Sample annotations (group, batch, QC status if present) are correctly mapped to columns and accessible; verify by comparing sample names in the object to the MS-DIAL file header.
- The object structure is compatible with downstream margheRita functions (e.g., filtering(), normalization(), mR_pca()) — test by applying at least one downstream operation without error.
- No NA or missing values are artificially introduced during parsing; confirm that the parsed intensity matrix matches the input file exactly before filtering or imputation steps.

## Limitations

- MS-DIAL exports must be in text (tab/space-delimited) or Excel format; other formats (binary, mzXML) require separate conversion.
- The parser relies on specific column header names and order conventions expected by margheRita or notame; non-standard MS-DIAL exports may require manual reformatting.
- Floating-point precision in m/z values depends on MS-DIAL export settings; loss of precision (e.g., rounding to 2 decimals) will degrade downstream mass defect filtering accuracy.
- Large feature tables (>10,000 features, >1,000 samples) may incur memory overhead during parsing, depending on R environment.
- Sample metadata (group, batch, QC flags) must be provided separately or manually added post-parsing if not embedded in the MS-DIAL export; the parser does not infer metadata from file names or sample IDs.

## Evidence

- [other] Load the MS-Dial output feature table: "Load the MS-Dial output feature table (Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) into margheRita as a data structure."
- [readme] MS-DIAL peak picking entry point: "The first step is to take raw data files created by the LC-MS instrument and create a peak table using a peak picking software (we use MS-DIAL)."
- [readme] margheRita complete workflow coverage: "The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)."
- [readme] Data structure encapsulation: "Data is stored in a custom object that holds all the information about the features and samples along with the feature abundance matrix."
- [intro] Untargeted LC-MS/MS scope: "margheRita is intended to be used after having done a number of data acquisition steps through MS-Dial"

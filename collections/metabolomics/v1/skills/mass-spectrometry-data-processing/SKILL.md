---
name: mass-spectrometry-data-processing
description: Use when you have raw mass spectrometry outputs (peak areas/heights across samples and fragmentation spectra) that need to be formatted and validated before running the tima taxonomically informed annotation workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - tima R package
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
---

# mass-spectrometry-data-processing

## Summary

Prepare and validate raw mass spectrometry data (feature quantification tables and MS/MS spectra) for taxonomically informed metabolite annotation by converting to standardized formats (CSV/TSV and MGF) and verifying structural integrity before downstream analysis.

## When to use

You have raw mass spectrometry outputs (peak areas/heights across samples and fragmentation spectra) that need to be formatted and validated before running the tima taxonomically informed annotation workflow. Apply this skill when starting a new metabolomics annotation project or when integrating external MS datasets.

## When NOT to use

- Input is already a processed feature table with pre-computed annotations from another tool (SIRIUS or GNPS-FBMN results are optional additions, not replacements for this step)
- You are only analyzing a single organism and do not have sample metadata (tima allows this, making metadata optional in such cases)
- Raw instrument files (mzML, mzXML, raw) have already been converted to feature tables by prior processing pipelines

## Inputs

- Feature quantification table (CSV or TSV format with feature ID, retention time, m/z, sample intensities)
- MS/MS spectra file in MGF format
- Sample metadata file (CSV or TSV) linking samples to organisms

## Outputs

- Validated feature table confirmed to contain required columns
- Validated spectra count and MGF structure
- Validated metadata structure with organism assignments
- Early error report identifying format or consistency issues

## How to apply

First, prepare your feature quantification table as a CSV or TSV file containing at minimum: feature ID, retention time, m/z value, and sample intensity columns (column names are customizable). In parallel, export or convert your MS/MS spectral data to MGF (Mascot Generic Format) format, ensuring each feature has an associated spectrum when available. Before proceeding to annotation, use the tima validation function to count features, verify required columns are present, check metadata consistency (mapping samples to organisms), and report any structural issues immediately. This early validation catch mismatches and data format problems that would otherwise propagate through the entire annotation pipeline.

## Related tools

- **tima R package** (Provides validate_inputs() function to inspect feature tables, spectra, and metadata structure; orchestrates the full annotation workflow) — https://github.com/taxonomicallyinformedannotation/tima
- **R** (Programming environment for running tima validation and annotation functions)

## Examples

```
validate_inputs(features = "data/source/example_features.csv", spectra = "data/source/example_spectra.mgf", metadata = "data/source/example_metadata.tsv", feature_col = "row ID", filename_col = "filename", organism_col = "ATTRIBUTE_species")
```

## Evaluation signals

- Feature table row count matches expected number of features; all required columns (feature ID, retention time, m/z, sample intensities) are present and accessible via customizable column names
- MGF file parses without syntax errors; spectrum count aligns with expected features or feature subset
- Metadata file contains all samples referenced in the feature table and organism assignments are non-empty for each sample
- validate_inputs() function completes without reporting missing or inconsistent fields; no warnings about mismatched sample-organism mappings
- No structural issues are flagged by the validation output; the README examples confirm expected output format

## Limitations

- Column name mappings are required input parameters; the tool does not auto-detect column identity from generic names like 'feature' or 'intensity'
- Metadata is optional only for single-organism analysis; multi-sample studies require properly linked organism assignments or annotation will fail downstream
- MGF format is rigid; spectra must follow standard Mascot Generic Format syntax or parsing will fail silently or with cryptic errors

## Evidence

- [readme] Feature quantification table requirements: "**Feature quantification table** (.csv/.tsv) - Peak areas/heights across samples - Must contain: feature ID, retention time, m/z, and sample intensity columns"
- [readme] MS/MS spectra file requirement: "**MS/MS spectra file** (.mgf) - Fragment spectra for each or some features"
- [readme] Sample metadata requirement: "**Sample metadata** (.csv/.tsv) - Links samples to organisms - Optional if analyzing only a single organism"
- [readme] Validation function purpose and scope: "**Start by validating your input files** to catch issues early and save debugging time: Check if your data is matches expectations before processing"
- [readme] Validation function checks performed: "This will: Count spectra in MGF files; Count features and check required columns; Check metadata file consistency; Report eventual issues immediately"
- [readme] Customizable column names: "**Tip**: All column names and file paths are customizable through the Shiny app interface or YAML/CLI parameters"

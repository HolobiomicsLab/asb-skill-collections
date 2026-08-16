---
name: data-interchange-format-conversion
description: Use when you have deconvoluted or processed MS/MS spectra from SWATH-MS
  data that need to be (1) ingested into tools requiring open formats (e.g., spectral
  library matching, metabolite identification pipelines), (2) archived in public repositories,
  or (3) shared across different analysis platforms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DecoMetDIA
  techniques:
  - LC-MS
  license_tier: noncommercial
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-ND-4.0
    url: ZhuMSLab/DecoMetDIA
derived_from:
- doi: 10.1021/acs.analchem.9b02655
  title: DecoMetDIA
evidence_spans:
- DecoMetDIA was developed to process SWATH-MS based data for metabolomics.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_decometdia_cq
    doi: 10.1021/acs.analchem.9b02655
    title: DecoMetDIA
  dedup_kept_from: coll_decometdia_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02655
  all_source_dois:
  - 10.1021/acs.analchem.9b02655
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Data Interchange Format Conversion

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Convert mass spectrometry raw data and processed spectra between vendor-native formats and open interchange standards (mzML, MGF, mzTab) to enable downstream analysis, deposition, and interoperability. This skill is essential in untargeted metabolomics pipelines where spectral deconvolution output must be exported in formats compatible with spectral databases and identification tools.

## When to use

Apply this skill when you have deconvoluted or processed MS/MS spectra from SWATH-MS data that need to be (1) ingested into tools requiring open formats (e.g., spectral library matching, metabolite identification pipelines), (2) archived in public repositories, or (3) shared across different analysis platforms. Trigger: output from spectral decomposition algorithms exists in tool-native or intermediate formats and downstream steps require standardized inputs.

## When NOT to use

- Input spectra are already in MGF or mzTab format and do not require re-export or re-annotation.
- Downstream analysis tool natively accepts the current format (e.g., tool-specific binary output); format conversion adds no analytical value.
- Data is targeted proteomics or targeted metabolomics where proprietary vendor formats are locked into a single-vendor pipeline and no interoperability is required.

## Inputs

- Deconvoluted MS/MS spectra (tool-native or intermediate binary/text format)
- Precursor ion m/z and retention time annotations
- Fragment peak lists with intensities
- Raw SWATH-MS data files (mzML or vendor-native format, if re-exporting)

## Outputs

- MGF (Mascot Generic Format) files with deconvoluted spectra
- mzTab format files with quantitative and metadata annotations
- Validated spectral interchange files ready for database matching or repository submission

## How to apply

After spectral deconvolution in DecoMetDIA, export deconvoluted spectra with associated precursor m/z, retention time, and intensity annotations into MGF (Mascot Generic Format) or mzTab format. MGF format is suitable for spectral library matching and MS/MS database queries; mzTab format preserves quantitative metadata and is preferred for open-access data deposition. Validate exported files by (1) confirming all deconvoluted spectra are represented, (2) checking that precursor m/z and retention time values fall within expected analytical ranges, (3) verifying peak count and intensity distributions match pre-export summaries, and (4) spot-checking mass accuracy against known standards or the original raw data.

## Related tools

- **DecoMetDIA** (Spectral deconvolution engine that generates deconvoluted spectra requiring format conversion for export and downstream use) — https://github.com/ZhuMSLab/DecoMetDIA

## Examples

```
devtools::install_github("ZhuMSLab/DecoMetDIA"); library(DecoMetDIA); deconvoluted_spectra <- decoMetDIA(swath_data); exportSpectra(deconvoluted_spectra, format="MGF", output="deconvoluted_spectra.mgf")
```

## Evaluation signals

- All deconvoluted spectra from the deconvolution module are represented in the exported file (record count matches or is reconcilable with pre-export totals).
- Precursor m/z values in the export fall within the expected isolation window range (typically 5–20 ppm relative to raw data).
- Retention time annotations are preserved and monotonically increase or match the original acquisition times (no loss or scrambling).
- Peak count per spectrum is consistent with pre-export validation summaries (e.g., min 5–10 fragments per spectrum for metabolomics).
- File parses without errors in downstream tools (e.g., spectral library search engine or metabolite identification software) and produces expected search results on validation compounds.

## Limitations

- MGF and mzTab formats do not capture all metadata from vendor-native files (e.g., instrument configuration, calibration coefficients); critical metadata must be preserved separately or documented in supplementary files.
- Format conversion may introduce rounding or precision loss in m/z, intensity, or retention time values depending on export precision settings; users should verify mass accuracy post-conversion.
- Large-scale deconvoluted datasets (>100,000 spectra) can produce very large MGF/mzTab files; practical handling may require compression or segmentation into manageable chunks.

## Evidence

- [other] Export deconvoluted spectra with associated precursor m/z, retention time, and intensity annotations in MGF or mzTab format.: "Export deconvoluted spectra with associated precursor m/z, retention time, and intensity annotations in MGF or mzTab format."
- [other] Validate deconvoluted spectra quality by checking for appropriate peak counts, intensity distributions, and mass accuracy.: "Validate deconvoluted spectra quality by checking for appropriate peak counts, intensity distributions, and mass accuracy."
- [readme] DecoMetDIA was developed to process SWATH-MS based data for metabolomics.: "DecoMetDIA was developed to process SWATH-MS based data for metabolomics."

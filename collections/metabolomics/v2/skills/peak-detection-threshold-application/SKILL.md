---
name: peak-detection-threshold-application
description: Use when converting raw MS/MS spectra from library files (e.g., .msp
  format) into structured library entries, or when annotating experimental LC–MS features
  against fragment databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
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

# peak-detection-threshold-application

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Application of noise and marker peak thresholds to filter MS/MS spectral peaks during library conversion or feature annotation in LC–MS metabolomics workflows. This skill ensures that only peaks meeting signal-to-noise and abundance criteria are retained, reducing noise-driven false matches and improving annotation specificity.

## When to use

Apply this skill when converting raw MS/MS spectra from library files (e.g., .msp format) into structured library entries, or when annotating experimental LC–MS features against fragment databases. The skill is necessary whenever you need to distinguish true spectral peaks from baseline noise or low-abundance artifacts before matching against reference spectra in metabolite annotation pipelines.

## When NOT to use

- Input spectra have already been noise-corrected or pre-filtered by the instrument or upstream processing software — applying additional thresholds may over-filter and lose low-abundance diagnostic peaks.
- Analysis requires retention of all observed peaks for spectral visualization or comparative analysis across conditions — thresholds will remove data needed for such comparisons.
- Custom threshold values have been experimentally optimized for your specific instrument and metabolite class — do not apply default parameters without validation.

## Inputs

- .msp library files (MS/MS spectra in MassBank or NIST format)
- Centroid-mode LC–MS AIF raw chromatogram data
- RAMClustR object containing pseudo-MS/MS spectra
- XCMS object containing peak-picked feature data

## Outputs

- CSV library entries with filtered spectral peaks and ionization mode suffixes (positive/negative)
- Annotated feature table with ranked candidate metabolite matches
- Peak occurrence scores for retained peaks above both thresholds

## How to apply

Set two complementary thresholds during peak-picking: a noise floor threshold (default 0.005, expressed as a relative intensity fraction) that removes peaks below the baseline signal, and a marker peaks threshold (default 0.1) that further filters peaks to retain only those with sufficient abundance. Apply these thresholds sequentially during spectral processing: first remove all peaks below the noise threshold, then assign occurrence scores to remaining peaks above the marker peaks threshold using the marker peaks score parameter (default 0.9). The rationale is that noise-level peaks introduce spurious fragment matches, while the marker peaks threshold focuses annotation on the most informative, abundant peaks that are more likely to represent true molecular fragmentations. Document the threshold values used so that results are reproducible and comparable.

## Related tools

- **MetaboAnnotatoR** (Primary tool that implements peak-detection thresholds via the mspToLib function and annotateRC function for LC–MS AIF metabolite annotation) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream peak-picking and feature detection tool that produces peak-picked data consumed by threshold-based filtering in annotation workflows)
- **RamClustR** (Generates pseudo-MS/MS spectra from AIF data that are subsequently filtered using noise and marker peak thresholds)

## Examples

```
mspToLib(msp_file = 'MassBank_example.msp', output_dir = './lib_output', noise = 0.005, mpeaksThres = 0.1, mpeaksScore = 0.9)
```

## Evaluation signals

- Verify that all peaks in output CSV library entries have intensity ≥ noise threshold (0.005 by default) and that peaks above marker peaks threshold (0.1) carry non-zero occurrence scores.
- Check that the number of peaks per spectrum decreases monotonically as threshold values increase, and that peak count is reasonable (typically 5–50 diagnostic fragments per compound).
- Confirm that annotation sensitivity (proportion of features matched to a metabolite) and specificity (proportion of top-ranked matches that are correct) improve or remain stable relative to unfiltered annotation, indicating that thresholds reduce false positives without losing true signals.
- Validate that output CSV files contain all required columns (m/z, intensity, occurrence score) and that ionization mode suffixes (positive/negative) are correctly appended to file names.
- Spot-check 5–10 annotated features by visual inspection of matched fragment peaks overlaid on the experimental spectrum to confirm that retained peaks correspond to chemically plausible molecular fragmentations.

## Limitations

- Default threshold values (noise=0.005, mpeaksThres=0.1) are instrument- and metabolite-class-dependent; they may require optimization for high-resolution or time-of-flight instruments and for specific compound families (lipids, peptides, natural products).
- Thresholds are applied uniformly across all spectra; dynamic or data-driven threshold selection based on signal-to-noise ratio per spectrum is not described in the paper.
- No changelog or version history is available for the mspToLib function, so it is unclear whether threshold implementations or default values have changed across releases.
- The marker peaks score parameter (default 0.9) is mentioned but its exact computational definition and sensitivity to threshold changes are not detailed in the article.

## Evidence

- [other] occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1): "occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)"
- [intro] Peak-picking above noise level threshold (default: 0.005) and Peak-picking above marker peak threshold (default: 0.1): "Peak-picking above noise level threshold (default: 0.005) [and] Peak-picking above marker peak threshold (default: 0.1)"
- [other] the mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file name: "the mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"

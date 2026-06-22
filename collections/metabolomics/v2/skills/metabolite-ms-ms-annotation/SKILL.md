---
name: metabolite-ms-ms-annotation
description: Use when when you have SWATH-MS raw data (mzML or vendor format) containing multiplexed MS/MS spectra from multiple co-eluting precursor ions and need to separate these spectra into individual, annotatable component spectra for metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - DecoMetDIA
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
---

# metabolite-ms-ms-annotation

## Summary

Deconvolute multiplexed MS/MS spectra from SWATH-MS data to resolve overlapping fragment ion patterns into individual component spectra, enabling accurate metabolite identification in untargeted metabolomics. This skill recovers hidden metabolite signals obscured by precursor co-isolation in data-independent acquisition (DIA) experiments.

## When to use

When you have SWATH-MS raw data (mzML or vendor format) containing multiplexed MS/MS spectra from multiple co-eluting precursor ions and need to separate these spectra into individual, annotatable component spectra for metabolite identification. Apply this skill when standard targeted or simple library matching fails due to overlapping fragment patterns masking true metabolite signals.

## When NOT to use

- Input is already a feature table or quantified metabolite matrix — use this skill only on raw or minimally processed MS data.
- Data was acquired in targeted MS/MS or single-precursor isolation mode (non-DIA) — deconvolution is unnecessary and will not improve signal.
- Precursor isolation windows are very wide (>50 m/z) or retention time windows are poorly defined — the decomposition algorithm requires reasonable co-elution windows to succeed.

## Inputs

- SWATH-MS raw data files (mzML format or vendor-specific format)
- Precursor ion mass list with isolation windows
- Retention time window definitions (typically 1–2 min windows per isolation)

## Outputs

- Deconvoluted MS/MS spectra (MGF or mzTab format)
- Precursor m/z annotations per spectrum
- Retention time and intensity annotations
- Quality metrics per deconvoluted spectrum (peak count, intensity distribution summary)

## How to apply

Load SWATH-MS raw data into DecoMetDIA and apply precursor ion isolation combined with retention time windowing to group co-eluting fragment spectra. Execute DecoMetDIA's multiplexed spectrum decomposition algorithm, which separates overlapping MS/MS spectra into individual component spectra by resolving their overlaid peak patterns. Export deconvoluted spectra in MGF or mzTab format with precursor m/z, retention time, and intensity annotations. Validate output quality by checking for appropriate peak counts (typically 5–30 fragments per spectrum), realistic intensity distributions (monotonic or multi-modal within chemical constraints), and mass accuracy (typically <5 ppm for Orbitrap or equivalent). Spectra with fragmented peak distributions or extreme intensity ratios may indicate incomplete deconvolution or noise and should be inspected or filtered.

## Related tools

- **DecoMetDIA** (R package implementing multiplexed MS/MS spectrum decomposition algorithm for SWATH-MS data; performs deconvolution of overlapping spectra and exports annotated component spectra) — https://github.com/ZhuMSLab/DecoMetDIA

## Examples

```
devtools::install_github("ZhuMSLab/DecoMetDIA")
library(DecoMetDIA)
# Load mzML and apply deconvolution with precursor m/z ± 25 ppm and RT ± 1 min windows; export as MGF
```

## Evaluation signals

- Deconvoluted spectra contain 5–30 major fragment peaks with realistic intensity hierarchies consistent with fragmentation rules (not all peaks of equal height or randomly distributed).
- Mass accuracy of all fragment ions is within 5 ppm of theoretical values, validated against known metabolite fragmentation patterns or spectral library matches.
- Precursor m/z and retention time annotations are preserved and match input isolation windows; no spectra have missing or out-of-range annotations.
- Post-deconvolution spectral library matching (e.g., cosine similarity or dot product) yields higher match scores and metabolite annotations compared to raw (non-deconvoluted) spectra from the same experiment.
- Peak count distribution across deconvoluted spectra is unimodal or bimodal within expected range (5–50 peaks); extreme outliers (< 3 or > 100 peaks) indicate potential decomposition failures.

## Limitations

- DecoMetDIA requires R and Rcpp compilation; Windows users must install RTools before building the package.
- Performance and accuracy depend on quality of input precursor isolation windows and retention time windowing; poorly defined windows may reduce deconvolution efficacy.
- The algorithm assumes linear or near-linear intensity relationships between overlapping spectra; highly non-linear or extremely weak co-eluting signals may be lost or misattributed.
- Licensed under CC BY-NC-ND 4.0: non-commercial use only; no derivative works or redistribution permitted.

## Evidence

- [readme] DecoMetDIA was developed to process SWATH-MS based data for metabolomics.: "DecoMetDIA was developed to process SWATH-MS based data for metabolomics."
- [intro] Deconvolution of multiplexed MS/MS spectra from SWATH-MS data enables metabolite identification.: "DecoMetDIA is a tool developed to process SWATH-MS based data for metabolomics applications, performing deconvolution of multiplexed MS/MS spectra."
- [other] Workflow includes loading data, applying precursor ion isolation and retention time windowing, performing spectral decomposition, and exporting with annotations.: "Load SWATH-MS raw data files (mzML or vendor format) into DecoMetDIA. 2. Apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra. 3. Perform spectral"
- [other] Quality validation includes checking peak counts, intensity distributions, and mass accuracy.: "Validate deconvoluted spectra quality by checking for appropriate peak counts, intensity distributions, and mass accuracy."
- [other] Output formats include MGF and mzTab with precursor m/z, retention time, and intensity annotations.: "Export deconvoluted spectra with associated precursor m/z, retention time, and intensity annotations in MGF or mzTab format."
- [readme] Installation via devtools on Windows requires RTools.: "DecoMetDIA was developed as an R package with Rcpp code. Compiling is needed when installing. On Windows OS, RTools should be installed first."

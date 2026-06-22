---
name: spectral-signal-detection
description: Use when you have mzML mass spectrometry data and a list of predicted candidate metabolites (with known mass-to-charge ratios and retention times) for a drug of interest, and you need to determine which candidates actually appear in the observed spectra rather than treating all predictions as.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3697
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MetIDfyR
  - MSnbase
  - Rdisop
  - MetApp
derived_from:
- doi: 10.1021/acs.analchem.0c02281
  title: MetIDfyR
evidence_spans:
- open-source, cross-platform and versatile R script
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metidfyr_cq
    doi: 10.1021/acs.analchem.0c02281
    title: MetIDfyR
  dedup_kept_from: coll_metidfyr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02281
  all_source_dois:
  - 10.1021/acs.analchem.0c02281
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-signal-detection

## Summary

Match predicted candidate metabolites against mass spectrometry spectral features using mass accuracy and intensity thresholds to identify which metabolites are present in mzML data. This skill detects actual chemical signals corresponding to in silico predictions.

## When to use

You have mzML mass spectrometry data and a list of predicted candidate metabolites (with known mass-to-charge ratios and retention times) for a drug of interest, and you need to determine which candidates actually appear in the observed spectra rather than treating all predictions as equally likely.

## When NOT to use

- Input is already a curated list of identified metabolites (detection has already been performed)
- mzML data is unprocessed and contains significant noise without prior peak-picking or baseline correction
- Predicted candidates lack chemical formula or theoretical m/z values needed for mass matching

## Inputs

- mzML mass spectrometry data file (raw or peak-picked)
- TSV or configuration file containing predicted candidate metabolites with chemical formulas and theoretical m/z values
- Configuration parameters specifying mass accuracy tolerance, intensity thresholds, and retention time windows

## Outputs

- Detection report (TSV format) listing matched metabolites with observed m/z, theoretical m/z, mass error, intensity, and retention time
- Feature extraction matrix (spectral features detected in the mzML data)
- Visualization-ready data for metabolite figures (via MetApp or similar)

## How to apply

Load the mzML file into R and extract observed spectral features (m/z values, intensities, retention times). For each predicted candidate metabolite, calculate or retrieve its theoretical mass-to-charge ratio. Compare observed m/z values against predicted candidates using a mass accuracy threshold (typically parts-per-million tolerance) and minimum intensity thresholds to filter noise. Retain only candidates whose theoretical m/z and expected retention time (if available) align with detected features above the intensity cutoff. Generate a detection report listing matched candidates and their correspondence to observed signals, filtering out candidates that lack supporting spectral evidence.

## Related tools

- **MetIDfyR** (R script that implements spectral-signal-detection by parsing mzML files, calculating theoretical m/z values from drug formulas, and matching predicted candidates against observed spectral features) — https://github.com/agnesbrnb/MetIDfyR
- **MSnbase** (R package dependency used to read and parse mzML mass spectrometry data files)
- **Rdisop** (R package dependency used to compute molecular mass and elemental composition from chemical formulas)
- **MetApp** (Shiny application for visualizing and validating detected metabolites, generating PDF reports of matched signals) — https://github.com/GIELCH/MetApp

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- All matched candidates have observed m/z within the specified mass accuracy tolerance (parts-per-million) of their theoretical m/z
- Matched candidates' signal intensities exceed the configured intensity threshold, filtering genuine signals from noise
- Detection report contains no candidates whose theoretical properties cannot be explained by the input chemical formulas or configuration
- When re-running with stricter mass accuracy or intensity thresholds, the number of matched candidates decreases monotonically
- Visual inspection of matched candidate spectra via MetApp shows clear peaks corresponding to reported m/z values and intensities

## Limitations

- Requires peak-picked mzML data; raw, unprocessed spectra may yield false negatives due to noise and baseline drift
- Mass accuracy threshold must be tuned for the instrument's resolution; inappropriate tolerances cause false positives or missed detections
- Retention time matching is optional and depends on availability of chromatographic data in the mzML file or external standards
- Does not distinguish between isomeric candidates or confirm structural identity; matching relies on mass and intensity alone
- Performance depends on the quality and completeness of the predicted candidate list; true metabolites not in the prediction set will not be detected

## Evidence

- [other] Match candidate metabolites against detected features using mass accuracy and intensity thresholds.: "Match candidate metabolites against detected features using mass accuracy and intensity thresholds."
- [other] MetIDfyR is an R script that detects metabolites in mass spectrometry data (mzML format) by operating on the raw chemical formula of the drug of interest as input.: "MetIDfyR is an R script that detects metabolites in mass spectrometry data (mzML format) by operating on the raw chemical formula of the drug of interest as input."
- [readme] predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest: "predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [other] Parse predicted candidate metabolites and their chemical properties (mass-to-charge ratios, retention times if available).: "Parse predicted candidate metabolites and their chemical properties (mass-to-charge ratios, retention times if available)."
- [other] Extract spectral features from the mzML data.: "Extract spectral features from the mzML data."

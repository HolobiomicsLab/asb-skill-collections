---
name: mass-spectrometry-feature-extraction
description: Use when you have raw mzML mass spectrometry data and need to detect which predicted candidate metabolites are present in the sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0769
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

# mass-spectrometry-feature-extraction

## Summary

Extract spectral features (m/z ratios, intensities, retention times) from raw mass spectrometry data in mzML format to enable metabolite candidate matching and detection. This skill transforms unprocessed MS data into a structured feature set suitable for comparative analysis against predicted metabolite properties.

## When to use

Apply this skill when you have raw mzML mass spectrometry data and need to detect which predicted candidate metabolites are present in the sample. Specifically, use it when you have: (1) a mzML file containing sample mass spectrometry signals, (2) a list of predicted candidate metabolites with known chemical properties (m/z, retention times), and (3) a goal to identify which candidates match observed spectral features within defined mass accuracy and intensity thresholds.

## When NOT to use

- Input is already a feature table or consensus spectrum — feature extraction has already been performed.
- mzML file is not peak-picked and no peak detection / centroiding step precedes this skill.
- You lack a priori knowledge of predicted candidate metabolites or their chemical properties (m/z, formula); this skill requires a candidate list to match against, not de novo feature discovery.

## Inputs

- mzML mass spectrometry file (raw or peak-picked)
- TSV file with parent drug formula and metadata (TEMPLATE_start_mlc.tsv format)
- Configuration file with matching parameters (mass accuracy threshold, intensity cutoffs, retention time windows)

## Outputs

- Detected spectral features (m/z values, intensities, retention times)
- Detection report (TSV) listing matched candidate metabolites and their corresponding observed signals
- Feature matrix suitable for visualization and downstream metabolite identification

## How to apply

Load the mzML mass spectrometry file into R using MSnbase or equivalent parsing tools. Parse the candidate metabolite list to extract mass-to-charge ratios, retention times, and other chemical properties from a TSV configuration file. Extract spectral features from the mzML data, including m/z values, intensities, and retention time windows. Match candidate metabolites against detected features by comparing m/z values within a mass accuracy threshold (typically specified in the configuration) and filtering by intensity thresholds. The matching logic compares each candidate's predicted m/z and retention time to observed signals; candidates whose properties fall within the tolerances are marked as detected. Generate a detection report listing which candidates matched observed signals in the data, with supporting evidence (matched m/z, intensity, retention time).

## Related tools

- **MetIDfyR** (R script that orchestrates mzML parsing, spectral feature extraction, and metabolite candidate matching; implements the complete workflow) — https://github.com/agnesbrnb/MetIDfyR
- **MSnbase** (R package for loading and parsing mzML mass spectrometry data; used internally by MetIDfyR for file I/O and spectral object handling)
- **Rdisop** (R package for chemical formula manipulation and m/z calculation from molecular formulas)
- **MetApp** (Shiny application for visualizing and interpreting detected metabolite features and generating PDF reports) — https://github.com/GIELCH/MetApp

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- Output TSV report contains rows for each detected candidate with non-empty m/z match, intensity, and retention time values; no candidates with null feature matches.
- Matched m/z values are within the configured mass accuracy threshold (e.g., ±5 ppm) of the predicted m/z from the candidate formula.
- Matched intensities exceed the configured intensity threshold, indicating signal is above noise floor.
- The number and identity of detected metabolites are consistent when re-run on the same input with identical configuration parameters (reproducibility check).
- Visual inspection via MetApp confirms that matched peaks are visually present in the spectra at the reported m/z and retention time coordinates.

## Limitations

- Feature extraction depends on mzML file quality; peak-picking artifacts or poor signal-to-noise ratio will reduce detection sensitivity.
- Mass accuracy thresholds and intensity cutoffs must be tuned per instrument and sample type; overly strict thresholds may miss true metabolites (false negatives), while lenient thresholds introduce false positives.
- Retention time matching requires that mzML file contains valid retention time data; if absent or corrupted, retention time filtering cannot be applied.
- The method is designed for targeted metabolite detection (candidate-driven) and cannot discover novel, unpredicted metabolites de novo.
- No changelog is available in the repository, limiting visibility into feature changes and bug fixes across versions.

## Evidence

- [other] Extract spectral features from the mzML data. Match candidate metabolites against detected features using mass accuracy and intensity thresholds.: "Extract spectral features from the mzML data. 4. Match candidate metabolites against detected features using mass accuracy and intensity thresholds."
- [readme] MetIDfyR is an open-source, cross-platform and versatile R script to predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest.: "MetIDfyR is an open-source, cross-platform and versatile R script to predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest."
- [readme] a mzML file containing the sample informations; a tsv file containing the parent drug informations: "a mzML file containing the sample informations; a tsv file containing the parent drug informations"
- [readme] MSnbase; Rdisop; readr; tibble: "MSnbase; Rdisop; readr; tibble"
- [other] Generate a detection report listing which candidates matched observed signals in the data.: "Generate a detection report listing which candidates matched observed signals in the data."

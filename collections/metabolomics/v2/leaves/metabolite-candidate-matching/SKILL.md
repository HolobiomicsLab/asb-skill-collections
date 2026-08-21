---
name: metabolite-candidate-matching
description: 'Use when you have: (1) a set of predicted candidate metabolites with
  known mass-to-charge ratios and chemical properties derived from a parent drug formula;
  (2) raw mass spectrometry data in mzML format from a sample suspected to contain
  those metabolites;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetIDfyR
  - MSnbase
  - Rdisop
  - MetApp
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-candidate-matching

## Summary

Match predicted candidate metabolites against observed mass spectrometry features in mzML data using mass accuracy and intensity thresholds to determine which candidates are present in a sample. This skill bridges in silico metabolite prediction with experimental MS detection.

## When to use

Apply this skill when you have: (1) a set of predicted candidate metabolites with known mass-to-charge ratios and chemical properties derived from a parent drug formula; (2) raw mass spectrometry data in mzML format from a sample suspected to contain those metabolites; and (3) a need to determine which predicted candidates actually correspond to detected spectral features rather than false positives or noise.

## When NOT to use

- Input is already a peak-picked feature table or aligned feature matrix — use this skill on raw or minimally processed mzML data.
- Metabolite candidates lack reliable mass-to-charge ratios or chemical formulas — the skill requires precise m/z values for matching.
- Mass spectrometry data is in NetCDF or other binary formats without mzML conversion — the workflow expects mzML format specifically.

## Inputs

- mzML mass spectrometry data file (raw or peak-picked)
- TSV file containing parent drug information and predicted candidate metabolites with chemical formulas
- Configuration file (R script) specifying mass accuracy tolerance, intensity thresholds, and matching parameters

## Outputs

- TSV detection report listing matched candidate metabolites and unmatched candidates
- Match quality metrics (mass error, intensity, confidence score) for each candidate
- Optional: visualization-ready data structures for MetApp (Shiny application) display and PDF report generation

## How to apply

Load the mzML mass spectrometry file and extract observed spectral features (m/z values, intensities, and optional retention times). Parse the predicted candidate metabolites with their calculated mass-to-charge ratios. Match each candidate against observed features by computing mass error and comparing against a user-defined mass accuracy threshold (specified in a configuration file). Apply intensity thresholds to filter low-signal matches. Aggregate matches and assign confidence levels based on how many isotopic or fragmentation patterns align. Generate a detection report listing which candidates matched observed signals, with match quality metrics suitable for downstream interpretation or visualization.

## Related tools

- **MetIDfyR** (Core R script that implements metabolite prediction, feature extraction from mzML, and candidate-feature matching via mass accuracy and intensity filtering) — https://github.com/agnesbrnb/MetIDfyR
- **MSnbase** (R/Bioconductor package for parsing and manipulating mzML mass spectrometry data and extracting spectral features)
- **Rdisop** (R package for computing molecular formulas and mass-to-charge ratios from chemical formulas)
- **MetApp** (Shiny application for interactive visualization and validation of matched metabolites and generation of PDF reports) — https://github.com/GIELCH/MetApp

## Examples

```
Rscript MetIDfyR.R -i input/lgd_DIA_peak-picked.tsv -o LGD4033_results -c input/config_LGD.R
```

## Evaluation signals

- All predicted candidate metabolites are assigned either a match status (matched with m/z error, intensity, and quality score) or an explicit 'unmatched' label in the output TSV.
- Matched candidates have mass error values within the configured mass accuracy tolerance (e.g., typical pharmaceutical workflows use ±5 ppm or ±10 ppm); inspect the error distribution to verify no systematic bias.
- Matched candidates have intensity values above the configured threshold; verify that weak or noise-level matches are filtered and documented.
- Isotopic or retention-time patterns (if available) for top-ranked matches align with theoretical predictions; cross-check with MetApp visualizations or generated PDF reports.
- Output file schema matches the expected format (TSV columns include: candidate name, theoretical m/z, observed m/z, mass error, intensity, match score, retention time if applicable); validate against TEMPLATE output structure.

## Limitations

- Matching relies on mass accuracy and intensity thresholds; if the instrument's mass resolution is poor (>10 ppm error) or sample concentration is very low, true metabolites may be missed or mismatched.
- mzML files must be peak-picked or processed to extract features; matching on raw, centroided spectra may inflate false positives.
- No changelog is maintained in the repository, limiting reproducibility across versions and clarity on algorithm updates or bug fixes.
- The skill does not perform automated retention-time prediction; retention-time matching is optional and relies on external standards or prior knowledge.
- MetIDfyR was developed and tested on R versions 3.6.1–4.0; compatibility with R versions >4.0 is not formally documented.

## Evidence

- [readme] MetIDfyR predicts and detects metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest: "an open-source, cross-platform and versatile R script to predict and detect metabolites in mass spectrometry data (mzML) based on the raw formula of the drug of interest"
- [other] Workflow includes parsing candidates, extracting spectral features, matching with mass and intensity thresholds, and generating a detection report: "1. Load the mzML mass spectrometry file using R. 2. Parse predicted candidate metabolites and their chemical properties (mass-to-charge ratios, retention times if available). 3. Extract spectral"
- [readme] Configuration file and template inputs are required to specify matching parameters: "Need - a configuration file with the parameter (see TEMPLATE_config.R). - a mzML file containing the sample informations - a tsv file containing the parent drug informations"
- [readme] Command-line invocation specifies input, output directory, and configuration file: "Rscript MetIDfyR.R -i path-to-input-file -o output-directory -c config-file"

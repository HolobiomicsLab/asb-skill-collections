---
name: biochemical-annotation-mapping
description: Use when you have loaded MSI data into napari, defined one or more ROIs
  of biological interest (e.g., tumor margin, specific tissue layer), extracted mean
  or summed intensity spectra from those regions, and need to identify the putative
  biochemical compounds corresponding to detected m/z peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical
  annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biochemical-annotation-mapping

## Summary

Map mass spectrometry imaging (MSI) spectra extracted from annotated regions of interest (ROIs) to biochemical identities by matching against reference databases using m/z tolerance and spectral similarity scoring. This skill enables targeted metabolite discovery and localization within tissue samples.

## When to use

Apply this skill when you have loaded MSI data into napari, defined one or more ROIs of biological interest (e.g., tumor margin, specific tissue layer), extracted mean or summed intensity spectra from those regions, and need to identify the putative biochemical compounds corresponding to detected m/z peaks. Use it to move from raw spectral features to annotated metabolite hypotheses with confidence metrics.

## When NOT to use

- Input MSI data has not yet been loaded or preprocessed; complete data import and visualization first.
- No discrete ROI has been defined; use whole-tissue or global profiling workflows instead.
- Match database is not formatted correctly (missing exact mass, molecule name, or formula columns) or is empty.
- You seek to discover novel compounds de novo; this skill requires a reference database and is designed for targeted annotation.

## Inputs

- imzML file (mass spectrometry imaging dataset in profile or centroid mode)
- Napari image layer with MSI data loaded
- ROI annotation layer (drawn using napari interactive brush/selection tools)
- Reference biochemical database (file with columns: exact mass, molecule name, molecular formula)

## Outputs

- Annotated ROI mean/summed spectrum (CSV export)
- Database match table (m/z, putative identity, match score, confidence)
- Overlaid visualization (ROI boundaries + matched annotations on MSI image)
- Spectrum plot image file (PNG/image export)

## How to apply

After defining and extracting spectra from an annotated ROI using napari's interactive drawing tools, calculate the mean or summed intensity profile for all spectra within the ROI boundary. Select a reference database (built-in Metabolite_database_ver2, LIPID MAPS, HMDB, or custom library formatted with exact mass, molecule name, and molecular formula) and configure search parameters: charge state (neutral, positive, or negative), appropriate adduct (e.g., [M+H]+, [M-H]−), and m/z tolerance window. Execute mass-to-charge ratio matching and spectral similarity scoring to generate a ranked table of matched annotations with m/z values, putative identities, match scores, and confidence metrics. Visualize ROI boundaries overlaid on the original MSI image with matched annotations linked to detected m/z features to confirm spatial coherence and biological plausibility.

## Related tools

- **napari** (Interactive image viewer and ROI annotation platform; enables load of imzML data, interactive drawing of ROI boundaries, and overlay of annotations on MSI images.) — https://github.com/napari/napari
- **MSI-Explorer** (Napari plugin that implements the complete workflow: data import, visualization, ROI selection, mean spectrum calculation, database search, and annotation export.) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Runtime environment for MSI-Explorer plugin and spectral matching algorithms.)

## Evaluation signals

- Returned annotation table contains at least one match with m/z and putative identity; m/z values in table fall within defined tolerance window of extracted ROI spectrum peaks.
- Match scores and confidence metrics are computed and present in output; lower match scores correspond to greater m/z deviation or lower spectral similarity.
- ROI boundaries are visibly overlaid on the original MSI image in the visualization layer; matched annotations are spatially linked to the ROI region.
- Exported CSV spectrum data and annotation table are non-empty, well-formed, and sortable by m/z or match score.
- Database search successfully ingests custom database files that follow the specified format (exact mass | molecule name | molecular formula); built-in Metabolite_database_ver2 loads without error.

## Limitations

- Annotation accuracy depends critically on reference database completeness and quality; compounds absent from the database will not be detected.
- m/z matching is sensitive to mass spectrometer calibration and defined tolerance window; miscalibration or overly strict tolerance can cause false negatives.
- Spectral similarity scoring assumes that extracted ROI spectra are sufficiently clean; high noise levels or strong background signals degrade match confidence.
- Profile mode data must be converted to centroid mode before annotation; this conversion introduces potential artifacts or peak loss if parameters are suboptimal.
- Single ROI mean spectrum may mask chemical heterogeneity within the annotated region; multiple ROI replicates or spatial segmentation may be necessary for complex tissues.

## Evidence

- [other] MSI-Explorer implements a workflow that includes region of interest (ROI) analysis and annotation with selected databases as core components for targeted biochemical analysis of MSI data.: "region of interest (ROI) analysis and annotation with selected databases as core components for targeted biochemical analysis"
- [other] Extract all mass spectra contained within the annotated ROI boundary. Calculate mean or summed intensity profile for the ROI spectra. Match extracted ROI spectrum(s) against a selected reference database using mass-to-charge ratio tolerance and spectral similarity scoring.: "Extract all mass spectra contained within the annotated ROI boundary. Calculate mean or summed intensity profile for the ROI spectra. Match extracted ROI spectrum(s) against a selected reference"
- [other] Generate a table of matched biochemical annotations with m/z values, putative identities, match scores, and confidence metrics. Visualize ROI boundaries overlaid on the original MSI image and display matched annotations linked to detected m/z features.: "Generate a table of matched biochemical annotations with m/z values, putative identities, match scores, and confidence metrics. Visualize ROI boundaries overlaid on the original MSI image"
- [readme] The features of the database function are 1. Charge (neutral, positive or negative) 2. Adduct (based on the charge chosen) 3. Range of the m/z value for the image display: "Charge (neutral, positive or negative) 2. Adduct (based on the charge chosen) 3. Range of the m/z value for the image display"
- [readme] Users can customize the database with exact mass, molecule name, or molecular formula. The format should be as shown in the table and the headers are not needed in the database.: "Users can customize the database with exact mass, molecule name, or molecular formula. The format should be as shown in the table"
- [readme] To select the ROI, click on Select ROI for mean spectrum. Adjust the brush size and label color. You can fill the area by using paint icon. Then click on the Calculate ROI mean spectrum.: "To select the ROI, click on Select ROI for mean spectrum. Adjust the brush size and label color. Then click on the Calculate ROI mean spectrum."
- [readme] Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting Yes converts the data, while No keeps it in its original profile format.: "Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode."

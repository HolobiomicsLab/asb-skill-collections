---
name: spectral-library-matching-and-scoring
description: Use when when you have extracted a mean or ROI spectrum from MSI data (via centroid or profile mode conversion) and need to identify the biochemical composition by comparing against curated reference libraries such as LIPID MAPS, HMDB, or a custom metabolite database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - napari
  - Python
  - MSI-Explorer
  - R
  - LOTUS
  - ISDB
  - MassBank
  - SIRIUS
  - GNPS-FBMN
  - tima R package
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
- doi: 10.3389/fpls.2019.01329
  title: ''
- doi: 10.5281/zenodo.3378723
  title: ''
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  - 10.3389/fpls.2019.01329
  - 10.5281/zenodo.3378723
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-and-scoring

## Summary

Match mass spectra extracted from regions of interest (ROI) or mean intensity profiles against reference biochemical databases using m/z tolerance and spectral similarity scoring to generate ranked lists of putative metabolite identities. This skill enables targeted annotation of MSI data by linking detected m/z features to known molecules with confidence metrics.

## When to use

When you have extracted a mean or ROI spectrum from MSI data (via centroid or profile mode conversion) and need to identify the biochemical composition by comparing against curated reference libraries such as LIPID MAPS, HMDB, or a custom metabolite database. Apply this skill after ROI definition and mean intensity calculation to obtain annotated metabolite assignments with m/z values and match scores.

## When NOT to use

- Input spectrum has not been preprocessed (noise reduction, normalization, or hotspot removal may be necessary first to avoid spurious matches)
- Reference database is not appropriate for the sample type or ionization mode (e.g., using a lipid-only database for protein analysis)
- No reference database is available or the database is missing entries for the expected metabolite class in your sample

## Inputs

- Mean intensity spectrum (vector of m/z and intensity pairs)
- ROI-extracted spectrum (summed or averaged intensities within annotated region)
- Reference biochemical database (with exact mass, molecule name, molecular formula)
- Centroid or profile mode MSI data (imzML format)

## Outputs

- Ranked annotation table (m/z values, putative identities, match scores, confidence metrics)
- Matched annotations linked to detected m/z features
- ROI boundaries overlaid on MSI image with annotations
- Exportable CSV of annotated spectrum data

## How to apply

Load a preprocessed MSI dataset and extract a mean spectrum or ROI-specific spectrum (e.g., via napari drawing tools). Select a reference database (built-in 'Metabolite_database_ver2' or custom library formatted with exact mass, molecule name, and molecular formula columns). Configure matching parameters: set m/z tolerance (typically 5–50 ppm depending on instrument resolution), specify charge state (neutral, positive, or negative), and select adduct type. Execute the matching algorithm to compute mass-to-charge ratio similarity and spectral similarity scoring. The output is a ranked table of matched annotations with m/z values, putative identities, match scores, and confidence metrics, which can be visualized overlaid on the original MSI image.

## Related tools

- **napari** (Interactive visualization and ROI drawing/annotation platform for MSI data and matched feature overlay) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that implements the complete workflow including ROI selection, database search, and spectral matching with built-in Metabolite_database_ver2) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Runtime environment for executing matching algorithms and database queries)

## Evaluation signals

- All extracted m/z features are assigned to entries in the reference database with scores above the configured similarity threshold (e.g., cosine similarity or match score ≥ 0.7 or configured confidence level)
- Match table contains no missing or NaN values in m/z, putative identity, or match score columns
- Matched m/z values fall within the specified m/z tolerance window (e.g., ±5 ppm) of reference database entries
- Visualization overlay shows ROI boundaries correctly registered to the original MSI image with annotations positioned at matched m/z feature locations
- Exported CSV includes expected headers and row counts consistent with the number of detected peaks submitted for matching

## Limitations

- Matching accuracy depends critically on database completeness and quality; rare or novel metabolites absent from the reference library will not be detected
- Profile-mode data must be converted to centroid mode before matching; the conversion introduces potential artifacts or peak loss if thresholds are misconfigured
- m/z tolerance and adduct settings are user-configurable and may require empirical tuning for different instruments or sample types; incorrect settings will yield false positives or false negatives
- Spectral similarity scoring does not account for isomeric or isobaric compounds; multiple database entries with identical or near-identical m/z values cannot be disambiguated without additional MS/MS or mobility data

## Evidence

- [other] Match extracted ROI spectrum(s) against a selected reference database (e.g., LIPID MAPS, HMDB, or custom library) using mass-to-charge ratio tolerance and spectral similarity scoring.: "Match extracted ROI spectrum(s) against a selected reference database (e.g., LIPID MAPS, HMDB, or custom library) using mass-to-charge ratio tolerance and spectral similarity scoring."
- [other] Generate a table of matched biochemical annotations with m/z values, putative identities, match scores, and confidence metrics.: "Generate a table of matched biochemical annotations with m/z values, putative identities, match scores, and confidence metrics."
- [readme] select `Metabolite_database_ver2`, which is a built-in database, and click `Confirm`: "select `Metabolite_database_ver2`, which is a built-in database, and click `Confirm`"
- [readme] The features of the database function are 1. Charge (neutral, positive or negative) 2. Adduct (based on the charge chosen) 3. Range of the m/z value for the image display: "The features of the database function are 1. Charge (neutral, positive or negative) 2. Adduct (based on the charge chosen) 3. Range of the m/z value for the image display"
- [readme] Users can customize the database with exact mass, molecule name, or molecular formula.: "Users can customize the database with exact mass, molecule name, or molecular formula."

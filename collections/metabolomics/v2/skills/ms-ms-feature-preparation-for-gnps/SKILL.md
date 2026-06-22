---
name: ms-ms-feature-preparation-for-gnps
description: Use when you have completed LC-MS/MS data processing and feature alignment in MZmine2 or Optimus, generated a feature quantification matrix and MGF file, and now need to format these outputs for submission to GNPS to compute spectral similarity networks and retrieve node/edge tables.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - GNPS
  - Optimus
  - OpenMS
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- the GNPS web-platform (http://gnps.ucsd.edu)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS feature preparation for GNPS

## Summary

Prepare aligned LC-MS feature tables and MS/MS spectral data in formats compatible with GNPS molecular networking submission. This skill bridges feature detection and quantification (via MZmine2 or Optimus) with GNPS web-platform ingestion, enabling downstream spectral similarity graph computation and bioactive molecular network generation.

## When to use

You have completed LC-MS/MS data processing and feature alignment in MZmine2 or Optimus, generated a feature quantification matrix and MGF file, and now need to format these outputs for submission to GNPS to compute spectral similarity networks and retrieve node/edge tables.

## When NOT to use

- Input is already a pre-computed spectral similarity network or edge list—skip GNPS submission.
- Feature table lacks MS/MS spectral data for most features; GNPS molecular networking requires MS/MS spectra.
- Data is targeted/MRM-based rather than untargeted LC-MS/MS discovery; GNPS is designed for discovery-scale spectral networking.

## Inputs

- feature quantification table (CSV) with aligned feature intensities across fractions
- MGF file with MS/MS spectral summaries and precursor m/z, retention time metadata
- GNPS web-platform access credentials

## Outputs

- GNPS node table (detected compounds/spectra with metadata)
- GNPS edge table (spectral similarity links between features)
- spectral similarity graph for molecular network visualization

## How to apply

Export a feature quantification table (CSV format containing aligned list of features and their intensities across samples) and an MGF file containing MS/MS spectral summaries from your feature detection tool. Ensure the MGF includes precursor m/z, retention time, and MS/MS spectra for each feature with MS/MS data. Access the GNPS web-platform at http://gnps.ucsd.edu and upload both files. Configure molecular networking parameters including spectral similarity scoring thresholds and edge filtering criteria (e.g., cosine similarity cutoff, minimum matched peaks). Submit the job and retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output for downstream analysis or visualization in Cytoscape.

## Related tools

- **MZmine2** (Feature detection, alignment, quantification, and MGF export prior to GNPS submission) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS feature detection and quantification pipeline using OpenMS; outputs feature table and MGF for GNPS) — https://github.com/MolecularCartography/Optimus
- **GNPS** (Web-platform for molecular networking: accepts feature tables and MGF files, computes spectral similarity graphs, outputs node and edge tables) — http://gnps.ucsd.edu
- **OpenMS** (Underlying algorithms for LC-MS feature detection and quantification used by Optimus) — http://www.openms.de
- **Cytoscape** (Visualization and analysis of GNPS-generated molecular network graphs (node/edge tables)) — http://www.cytoscape.org/

## Evaluation signals

- Feature quantification table contains expected number of aligned features across all analyzed fractions with non-zero intensities.
- MGF file validates against GNPS schema: contains precursor m/z, retention time, MS/MS peak lists, and spectrum identifiers for each feature.
- GNPS job submission succeeds without format or schema errors and returns a valid job ID.
- Retrieved node table contains ≥1 spectral entries with assigned compound metadata; edge table contains spectral similarity scores within expected range (typically 0–1 or cosine similarity).
- Node/edge tables can be imported into Cytoscape without parsing errors and render a connected or weakly connected graph.

## Limitations

- GNPS molecular networking requires MS/MS spectra; features without MS/MS data are excluded from networking but remain in the feature table.
- Spectral similarity thresholds and edge filtering parameters significantly impact network density and interpretability; empirical optimization is often needed.
- GNPS does not provide MS/MS validation of putative molecular annotations; additional tools such as Sirius or MS-FINDER are needed for in-silico structure elucidation.
- Large datasets (hundreds of LC-MS runs) may require extended processing time and memory on the GNPS server.
- No changelog is available for GNPS version updates, so reproducibility may be affected by undocumented platform changes over time.

## Evidence

- [intro] feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra): "Prepare feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra)."
- [intro] Access the GNPS web-platform and configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds: "Access the GNPS web-platform at http://gnps.ucsd.edu and upload the processed data. 3. Configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds."
- [intro] Retrieve node and edge tables from GNPS output: "Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output."
- [readme] Feature quantification table (features_quantification_matrix.csv) and MGF file from MZmine2 or Optimus: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS; a .MGF file containing"
- [readme] The workflow relies on open bioinformatic tools (MZmine2 or Optimus using OpenMS) and GNPS web-platform: "The workflow relies on open bioinformatic tools, such [MZmine2](http://mzmine.github.io/) or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS), a Jupyter notebook, and the"

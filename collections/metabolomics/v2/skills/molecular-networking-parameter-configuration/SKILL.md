---
name: molecular-networking-parameter-configuration
description: Use when after preparing a feature table and MS/MS spectral data (mzML or MGF format with precursor m/z, retention time, and MS/MS spectra) and before submitting to GNPS for molecular network generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MZmine2
  - GNPS
  - Optimus
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
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

# molecular-networking-parameter-configuration

## Summary

Configure spectral similarity scoring and edge filtering thresholds on the GNPS web-platform prior to submitting MS/MS molecular networking jobs. Proper parameter tuning directly affects network topology, node connectivity, and the biological interpretability of detected molecular relationships.

## When to use

After preparing a feature table and MS/MS spectral data (mzML or MGF format with precursor m/z, retention time, and MS/MS spectra) and before submitting to GNPS for molecular network generation. Use this skill when you need to decide on spectral similarity cutoffs and edge filtering to balance network density against false-positive spectral associations.

## When NOT to use

- Input spectra have poor quality or low signal-to-noise ratio—network parameters cannot compensate for weak MS/MS data.
- You are working with targeted metabolomics data where all features are known a priori—molecular networking is designed for untargeted discovery.
- The MS/MS data lack consistent fragmentation patterns (e.g., very small molecules with minimal MS/MS peaks)—network similarity metrics will have low discriminatory power.

## Inputs

- feature table (quantification matrix CSV format with aligned features across samples)
- MS/MS spectral data (mzML or MGF file containing precursor m/z, retention time, and fragmentation spectra)

## Outputs

- node table (list of compounds/spectra with annotations)
- edge table (spectral similarity links with similarity scores and metadata)

## How to apply

Access the GNPS web-platform at http://gnps.ucsd.edu and upload your processed feature table and MS/MS data. On the molecular networking job submission form, configure two critical parameters: (1) spectral similarity scoring threshold—typically cosine similarity or related scoring metrics used to determine whether two spectra are similar enough to form an edge in the network graph; and (2) edge filtering thresholds—minimum score, minimum matched peaks, and/or maximum precursor m/z difference to exclude weak or unreliable spectral pairs. The rationale is that more stringent thresholds (higher similarity scores, tighter m/z windows) reduce spurious clusters and improve precision, while relaxed thresholds increase recall and may reveal co-eluting or structurally related compounds. Submit the configured job to GNPS to compute the spectral similarity graph, then retrieve node and edge tables from the output for downstream analysis in tools like Cytoscape.

## Related tools

- **GNPS** (web-platform for molecular networking job submission, parameter configuration, and spectral similarity graph computation) — http://gnps.ucsd.edu
- **MZmine2** (open bioinformatic tool for feature detection and MS/MS data preparation prior to GNPS submission) — http://mzmine.github.io/
- **Optimus** (open bioinformatic workflow for LC-MS feature detection and quantification using OpenMS, with output compatible with GNPS) — https://github.com/MolecularCartography/Optimus
- **Cytoscape** (network visualization and analysis tool for interpreting GNPS-generated molecular network nodes and edges) — http://www.cytoscape.org/

## Evaluation signals

- Node and edge tables are successfully retrieved from GNPS output with non-empty rows matching the input feature count.
- Edge table contains numerical similarity scores (cosine similarity or equivalent) within expected range (typically 0–1); verify no missing or out-of-range values.
- Network density (edges per node) is reasonable relative to parameter stringency—very relaxed parameters should yield higher edge counts than stringent thresholds applied to the same data.
- Manual inspection of representative edges in Cytoscape shows spectral pairs with high similarity scores correspond to structurally related or co-eluting compounds as expected from the experimental design.
- Node and edge tables are reproducible across re-runs with identical parameter configurations, confirming deterministic GNPS processing.

## Limitations

- GNPS parameter configuration requires empirical tuning; no automated method is provided in the workflow to optimize thresholds for a given dataset or biological context.
- Spectral similarity metrics (e.g., cosine similarity) assume MS/MS fragmentation patterns are comparable across ionization methods and instrument types; heterogeneous data may require separate network analyses.
- Edge filtering thresholds are global and apply uniformly to all spectral pairs; local variations in MS/MS quality or compound class-specific fragmentation patterns are not accommodated.
- The workflow does not validate parameter choices against independent standards or reference spectral libraries; downstream manual curation of network clusters is often necessary.

## Evidence

- [intro] Configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds.: "Configure molecular networking parameters including spectral similarity scoring and edge filtering thresholds."
- [intro] Prepare feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra).: "Prepare feature table and MS/MS data in the format required by GNPS (typically mzML or MGF with precursor m/z, retention time, and MS/MS spectra)."
- [intro] Submit the job to the GNPS platform to compute the spectral similarity graph.: "Submit the job to the GNPS platform to compute the spectral similarity graph."
- [intro] Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output.: "Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output."
- [readme] The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform (http://gnps.ucsd.edu).: "The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform"

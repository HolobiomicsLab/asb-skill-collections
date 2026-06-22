---
name: mass-spectrometry-feature-mapping
description: Use when you have (1) aligned LC-MS/MS feature quantification matrix (features × fractions with m/z and RT for each feature), (2) bioassay activity measurements across the same fractions, and (3) need to assign bioactivity values to individual molecular network nodes to identify bioactive compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - Jupyter notebook
  - Optimus
  - GNPS
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- a Jupyter notebook, and the GNPS web-platform
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-mapping

## Summary

Maps LC-MS/MS detected molecular features to bioassay-guided fractionation activity measurements by matching retention time and mass-to-charge ratio, enabling per-feature bioactivity score calculation and network annotation. Essential for integrating untargeted metabolomics with phenotypic bioassay data.

## When to use

You have (1) aligned LC-MS/MS feature quantification matrix (features × fractions with m/z and RT for each feature), (2) bioassay activity measurements across the same fractions, and (3) need to assign bioactivity values to individual molecular network nodes to identify bioactive compounds in natural product extracts or complex mixtures.

## When NOT to use

- Feature quantification matrix has not been aligned across fractions (i.e., features are not yet matched across LC-MS runs).
- Bioassay data is missing or incomplete for a majority of fractions; mapping will produce uninformative or sparse scores.
- MS/MS spectra were not acquired for features of interest; molecular network construction and annotation cannot proceed.

## Inputs

- feature quantification matrix (CSV: aligned LC-MS/MS features with m/z, retention time, and intensity per fraction)
- bioassay activity matrix (CSV: fractions × bioactivity measurement columns)
- molecular network graph structure (edges and node identifiers from GNPS, e.g., GraphML or JSON)
- feature metadata (m/z tolerance specification, retention time window)

## Outputs

- bioactivity-annotated molecular network (GraphML or JSON with bioactivity scores as node attributes)
- feature-to-bioactivity mapping table (CSV: feature identifier, m/z, RT, aggregated bioactivity score, fractions contributing to score)
- network visualization file (Cytoscape-compatible)

## How to apply

Load the feature quantification table (CSV with m/z, retention time, and intensity columns per fraction) and the bioassay activity matrix (fractions × assay measurements) into Python/R. For each detected feature, use m/z and retention time as keys to identify which fractions contain that feature above a noise threshold. Aggregate bioactivity measurements (sum, mean, or max) across all fractions containing each feature to compute a single per-feature bioactivity score. Validate that m/z matching tolerances are appropriate for your instrument resolution (typically ±5 ppm for high-resolution MS). Annotate the molecular network graph (from GNPS or other source) by adding bioactivity scores as node attributes. Export the annotated network in GraphML or JSON format compatible with Cytoscape for interactive visualization and downstream validation.

## Related tools

- **MZmine2** (LC-MS feature detection, alignment, and quantification matrix generation) — http://mzmine.github.io/
- **Optimus** (LC-MS feature detection and alignment workflow using OpenMS algorithms) — https://github.com/MolecularCartography/Optimus
- **GNPS** (Molecular network construction from MS/MS spectra and spectral library matching) — http://gnps.ucsd.edu
- **Jupyter notebook** (Interactive Python/R environment for implementing bioactivity score aggregation and network annotation) — https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks
- **Cytoscape** (Network visualization and interactive exploration of bioactivity-annotated nodes) — http://www.cytoscape.org/

## Evaluation signals

- Feature-to-fraction mapping produces non-null bioactivity scores for ≥80% of input features (indicates successful m/z and RT matching).
- Bioactivity scores are reproducible when re-aggregated from the same input data (validates aggregation logic).
- Annotated network in Cytoscape displays bioactivity scores as visible node colors/sizes without schema errors.
- Visual inspection confirms that features with high bioactivity scores co-localize in the network to known bioactive molecular families (validates biological coherence).
- Mass-activity correlation (Pearson or Spearman) between bioactivity score and feature intensity in active fractions is positive and significant (p < 0.05), indicating alignment with expected bioassay signal.

## Limitations

- M/z and retention time matching may produce ambiguous assignments when multiple features have similar mass and RT in crowded regions; m/z tolerance must be carefully tuned to instrument resolution.
- Bioactivity aggregation (sum, mean, max) is heuristic; choice depends on fractionation scheme and assay properties and may obscure features present in inactive fractions by chance.
- MS/MS spectra must have been acquired during LC-MS/MS runs for network node identification; features lacking MS/MS data cannot be robustly matched to the network.
- Bioassay reproducibility and plate-effect artifacts are not corrected by the mapping step; quality control and normalization should be applied upstream.
- No changelog or versioning documentation available for the workflow; reproducibility may be hindered if tool versions or dependencies are not explicitly tracked.

## Evidence

- [other] Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching.: "Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching."
- [other] Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature).: "Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature)."
- [other] Annotate the molecular network with bioactivity scores as node attributes.: "Annotate the molecular network with bioactivity scores as node attributes."
- [other] Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON).: "Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON)."
- [readme] The code is released as a Jupyter notebook for easiness and reproducibility.: "The code is released as a Jupyter notebook for easiness and reproducibility."
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS"

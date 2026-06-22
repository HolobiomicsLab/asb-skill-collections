---
name: bioactivity-score-aggregation
description: Use when when you have both (1) a molecular network graph from GNPS with aligned MS/MS features (nodes and edges) and (2) a bioassay-guided fractionation activity matrix (fractions × bioactivity measurements), and you need to determine which molecular features are responsible for observed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3371
  - http://edamontology.org/topic_0602
  tools:
  - MZmine2
  - Jupyter notebook
  - GNPS
  - Optimus
  - Cytoscape
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bioactivity-score-aggregation

## Summary

Compute per-feature bioactivity scores by aggregating bioassay measurements across fractions and mapping them to molecular network nodes. This skill integrates LC-MS/MS feature detection with bioassay-guided fractionation data to annotate molecular networks with quantitative bioactivity potentials.

## When to use

When you have both (1) a molecular network graph from GNPS with aligned MS/MS features (nodes and edges) and (2) a bioassay-guided fractionation activity matrix (fractions × bioactivity measurements), and you need to determine which molecular features are responsible for observed bioactivity to prioritize downstream compound isolation and structural elucidation.

## When NOT to use

- Input is already a feature quantification table without network topology — use this skill to enrich existing networks, not to create them from raw LC-MS data.
- Bioassay data lacks clear fraction-to-sample mapping or has inconsistent retention time / m/z coordinates — alignment will fail or produce spurious matches.
- Goal is structure elucidation or spectral library matching only, without bioactivity prioritization — use MS/MS spectral networking tools (GNPS) directly instead.

## Inputs

- GNPS molecular network graph (node table with feature identifiers, retention time, m/z; edge table with network connections)
- bioassay-guided fractionation activity matrix (rows=fractions, columns=bioactivity measurements; may include replicates or multiple assay endpoints)
- feature quantification table with RT and m/z for each detected feature (e.g., from MZmine2 or Optimus)

## Outputs

- Annotated molecular network with bioactivity scores as node attributes (GraphML, JSON, or CSV format)
- Summary table mapping each feature to its aggregated bioactivity score and associated metadata (RT, m/z, number of active fractions)

## How to apply

Load the GNPS molecular network structure (edges, node identifiers, retention time and m/z for each feature) and the bioassay activity matrix into Python. Match fractionation samples to molecular network features using retention time (RT) and mass-to-charge ratio (m/z) as unique identifiers, typically within a defined tolerance window. For each feature, aggregate bioactivity measurements across all fractions in which that feature was detected, using a summary statistic (sum, mean, or max of activity values). Annotate the molecular network graph with the computed bioactivity score as a node attribute. Export the annotated network in a machine-readable format (GraphML, JSON, or tabular format) compatible with Cytoscape or downstream visualization and filtering tools.

## Related tools

- **GNPS** (Host platform for MS/MS molecular networking; provides the molecular network graph structure (edges, nodes, feature identifiers) that serves as the scaffold for bioactivity annotation.) — http://gnps.ucsd.edu
- **MZmine2** (LC-MS/MS feature detection and alignment; produces the feature quantification table with RT, m/z, and intensities across all fractions, which is used for feature-to-fraction mapping.) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS/MS feature detection and alignment workflow using OpenMS; produces feature quantification matrix compatible with bioactivity aggregation.) — https://github.com/MolecularCartography/Optimus
- **Jupyter notebook** (Execution environment for the bioactivity score aggregation workflow; provides reproducible, documented integration of data loading, RT/m/z matching, aggregation, and export.) — https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks
- **Cytoscape** (Network visualization and interactive exploration tool; receives the annotated molecular network (GraphML or JSON) for visual assessment of bioactivity distribution and community structure.) — http://www.cytoscape.org/

## Evaluation signals

- Feature-to-fraction mapping completeness: verify that ≥80% of features with bioactivity signal are matched to network nodes (check for RT/m/z alignment artifacts or coordinate mismatches).
- Bioactivity score distribution: inspect the aggregated scores for expected range (e.g., non-negative for sum/mean, maximum ≤ max(raw assay values)); flag negative or missing values as alignment failures.
- Network annotation schema validation: confirm that every node in the exported network carries a bioactivity score attribute (no null values for detected features) and that the GraphML/JSON is parseable by Cytoscape.
- Reproducibility audit: re-run the Jupyter notebook on the same inputs and verify that bioactivity scores are identical (deterministic aggregation); compare against manually computed scores for a subset of features.
- Downstream enrichment: validate that high-bioactivity features co-occur in network clusters or match known bioactive compound signatures (if reference data available), and that the ranking is consistent with biological/chemical expectations.

## Limitations

- RT and m/z matching is sensitive to instrumental calibration drift and alignment errors; features detected in only one fraction may be assigned spurious bioactivity if background noise is high.
- Aggregation strategy (sum, mean, max) can bias results: sum favors features in many fractions (high noise), mean may downweight rare bioactive metabolites, max ignores dose–response dynamics; choice must be justified per bioassay context.
- Bioassay data structure assumed: the notebook requires a consistent fraction labeling and column naming scheme; non-standard formats (e.g., nested replicates, multi-plate layouts) require manual preprocessing.
- No statistical significance testing: bioactivity scores are descriptive aggregates; no p-values or confidence intervals are computed, so thresholds for 'active' vs. 'inactive' features must be set post-hoc or externally.
- MS/MS validation not included: MS/MS spectral library matching and structure confirmation are required separately (via GNPS or Sirius); bioactivity alone does not annotate chemical identity.

## Evidence

- [intro] The workflow integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking.: "integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking"
- [other] Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching.: "Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching"
- [other] Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature).: "Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature)"
- [other] Annotate the molecular network with bioactivity scores as node attributes.: "Annotate the molecular network with bioactivity scores as node attributes"
- [other] Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON).: "Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON)"
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS"
- [readme] The code is released as a Jupyter notebook for easiness and reproducibility.: "The code is released as a Jupyter notebook for easiness and reproducibility"

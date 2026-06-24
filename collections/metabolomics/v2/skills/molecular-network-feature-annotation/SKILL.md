---
name: molecular-network-feature-annotation
description: Use when when you have both (1) a molecular network graph from GNPS with
  MS/MS feature nodes and edges, and (2) a quantitative bioassay matrix (fractions
  × bioactivity measurements) from parallel LC-MS/MS fractionation of the same sample
  extract.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - Jupyter notebook
  - GNPS
  - Optimus
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
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

# molecular-network-feature-annotation

## Summary

Integrate MS/MS molecular networking topology with bioassay-guided fractionation activity data to assign bioactivity scores to individual molecular features, enabling the discovery of bioactive compounds in natural product extracts. This skill combines GNPS network structure with per-fraction bioactivity measurements to annotate and rank features by their biological relevance.

## When to use

When you have both (1) a molecular network graph from GNPS with MS/MS feature nodes and edges, and (2) a quantitative bioassay matrix (fractions × bioactivity measurements) from parallel LC-MS/MS fractionation of the same sample extract. Use this skill to identify which molecular features co-localize with bioactive fractions and to score features by their observed bioactivity across all fractions.

## When NOT to use

- Input bioassay data is qualitative (present/absent) rather than quantitative; the aggregation step requires numeric activity values to compute meaningful per-feature scores.
- Molecular features lack retention time and m/z metadata; feature-to-fraction mapping cannot proceed without accurate mass and temporal alignment.
- MS/MS molecular network is incomplete or lacks node identifiers that can be matched to the quantification table; the linking step will fail silently or produce false mappings.

## Inputs

- GNPS molecular network graph (edges, node identifiers, retention time and m/z per node)
- bioassay-guided fractionation activity matrix (fractions × bioactivity measurement columns)
- LC-MS/MS feature quantification table (features × fractions, with retention time and m/z)

## Outputs

- Annotated molecular network with bioactivity scores as node attributes (GraphML or JSON)
- Per-feature bioactivity score table (feature ID, m/z, retention time, bioactivity score)
- Cytoscape-compatible network file for interactive visualization and filtering

## How to apply

Load the GNPS molecular network structure (node identifiers, edges, and retention time/m/z for each feature) and the bioassay-guided fractionation activity matrix into a Jupyter notebook. Map each molecular feature to the fractions in which it was detected using retention time and m/z matching tolerances. For each feature, aggregate bioactivity measurements (sum, mean, or max) across all fractions containing that feature to compute a per-feature bioactivity score. Annotate the molecular network graph by adding bioactivity scores as node attributes. Export the annotated network in a format compatible with Cytoscape (e.g., GraphML or JSON) for interactive visualization and downstream filtering by activity threshold.

## Related tools

- **GNPS** (Source of MS/MS molecular network structure, edges, and feature node definitions) — http://gnps.ucsd.edu
- **MZmine2** (LC-MS/MS feature detection, alignment, and quantification table generation) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS feature detection and quantification using OpenMS algorithms) — https://github.com/MolecularCartography/Optimus
- **Jupyter notebook** (Execution environment for bioactivity score computation and network annotation) — https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks
- **Cytoscape** (Interactive visualization, filtering, and exploration of annotated molecular networks) — http://www.cytoscape.org/

## Evaluation signals

- Bioactivity scores are numeric, non-null, and within the expected range (e.g., 0 to max activity value or normalized 0–1) for all features present in at least one bioactive fraction.
- Feature-to-fraction mapping is complete and deterministic: each feature maps to the same set of fractions on re-execution; no features are lost or duplicated.
- Annotated network file is syntactically valid GraphML or JSON and can be opened without error in Cytoscape; node attributes include feature ID, m/z, retention time, and bioactivity score.
- Bioactivity scores correlate positively with MS/MS spectral abundance (or intensity) in bioactive fractions: high-scoring features should appear with higher peak areas in fractions assigned high activity values.
- Top N features by bioactivity score match known bioactive compounds (if reference standards or literature values are available) or cluster together in the network, suggesting that co-networked features share chemical and biological properties.

## Limitations

- Aggregation method (sum, mean, max) is arbitrary and can bias results; sum may favor widely-distributed features, while max may bias toward rare high-activity fractions. The article does not specify which method is optimal for drug discovery.
- Feature-to-fraction matching relies on retention time and m/z tolerance thresholds; mismatched or overlapping features can lead to incorrect bioactivity assignment, especially in complex extracts with many co-eluting compounds.
- Bioactivity scoring assumes that fractionation samples are independent and that activity values are directly proportional to bioactive compound concentration; non-linear dose–response curves or synergistic multi-component activity will not be captured.
- MS/MS validation of putative annotations is not provided in the workflow; annotated network nodes lack compound identities, limiting biological interpretation without manual curation or external spectral library matching.
- Network and bioassay data must be collected from the same biological sample; misalignment or batch effects between LC-MS/MS run and bioassay plate can introduce systematic errors.

## Evidence

- [intro] integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking: "integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking"
- [other] Load the molecular network graph structure (e.g., network edges and node identifiers from GNPS) and the bioassay-guided fractionation activity matrix (fractions × bioactivity measurements) into Python. 2. Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching. 3. Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature). 4. Annotate the molecular network with bioactivity scores as node attributes. 5. Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON).: "Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching. 3. Aggregate bioactivity measurements across fractions for each feature, computing a"
- [readme] The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform: "The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform"
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS"

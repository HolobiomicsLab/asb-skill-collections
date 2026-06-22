---
name: bioassay-activity-data-integration
description: Use when when you have (1) a molecular network graph from GNPS with node identifiers and edges, (2) LC-MS/MS features quantified across fractions in a feature table, and (3) bioassay measurements (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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
---

# bioassay-activity-data-integration

## Summary

Integration of bioassay-guided fractionation activity measurements with MS/MS molecular network features to annotate network nodes with per-feature bioactivity scores. This skill bridges untargeted metabolomics feature detection with functional bioassay phenotyping to identify active molecular entities in natural product fractionation workflows.

## When to use

When you have (1) a molecular network graph from GNPS with node identifiers and edges, (2) LC-MS/MS features quantified across fractions in a feature table, and (3) bioassay measurements (e.g., antimicrobial, antiviral, or cytotoxic activity) scored per fraction, and your goal is to map activity back to individual molecular features to prioritize lead compounds for isolation or characterization.

## When NOT to use

- Input feature table is not aligned across fractions or lacks m/z and RT metadata — feature-to-bioassay matching will fail.
- Bioassay data are qualitative (present/absent) or cannot be quantitatively aggregated — the skill relies on numerical activity values for scoring.
- Molecular network is not from MS/MS spectral matching (e.g., from NMR or predicted spectra) — the skill depends on GNPS feature-based networking.

## Inputs

- GNPS molecular network graph (GraphML or JSON format with node IDs and edges)
- Feature quantification matrix (features × fractions, from MZmine2 or Optimus)
- Bioassay activity matrix (fractions × bioactivity measurements, e.g., inhibition %, IC50, or zone diameter)
- Retention time and m/z values for feature-to-fraction mapping

## Outputs

- Annotated molecular network with bioactivity scores as node attributes (GraphML or JSON)
- Feature-bioactivity score table (feature ID, m/z, RT, bioactivity score, fractions contributing to score)
- Visualization-ready network file importable into Cytoscape

## How to apply

Load the molecular network structure (nodes and edges from GNPS GraphML or JSON export) and the bioassay-guided fractionation activity matrix (fractions × bioactivity measurements) into Python. Match fractionation samples to molecular network features using retention time and m/z alignment tolerances. Aggregate bioactivity measurements across fractions for each feature by computing a summary statistic (sum, mean, or max of activity values in fractions containing that feature). Annotate the molecular network graph with per-feature bioactivity scores as node attributes. Export the annotated network in Cytoscape-compatible format (GraphML or JSON) for visualization and manual curation of active clusters.

## Related tools

- **GNPS** (Constructs MS/MS molecular network graph and provides node/edge export formats) — http://gnps.ucsd.edu
- **MZmine2** (Detects and aligns LC-MS features across fractions; exports feature quantification table and MS/MS spectra) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS feature detection, alignment, and quantification using OpenMS; supports feature filtering and export) — https://github.com/MolecularCartography/Optimus
- **Jupyter notebook** (Executes bioactivity scoring and network annotation workflow; integrates feature table, bioassay data, and GNPS network) — https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks
- **Cytoscape** (Visualizes and manually curates the annotated molecular network with bioactivity scores) — http://www.cytoscape.org/

## Evaluation signals

- Feature-to-fraction mapping is one-to-one (each feature matched to exactly one m/z and RT) or many-to-one (multiple features per fraction); no unmatched features.
- Bioactivity scores for each feature are numeric and within the expected activity range (e.g., 0–100% inhibition); scores are computed from ≥1 fraction containing that feature.
- Annotated network node attributes include bioactivity_score, fractions_contributing, and aggregation_method (sum/mean/max); schema validation against GraphML or JSON schema.
- Network export is importable without error into Cytoscape; network topology (edges, node counts) unchanged from input GNPS network.
- High-activity features cluster together in the molecular network (cosine similarity > 0.7 within high-bioactivity regions), suggesting co-occurrence of active metabolites in fractions.

## Limitations

- Bioactivity scoring is only as sensitive as the bioassay resolution — coarse activity measurements (e.g., binary active/inactive) reduce the signal-to-noise ratio for individual features.
- Feature-to-fraction matching relies on m/z and RT tolerance windows; misalignment due to retention time drift or mass calibration errors will introduce spurious activity assignments.
- Aggregation method (sum, mean, max) is arbitrary and not optimized; different methods may yield conflicting activity rankings for features present in multiple fractions.
- Network annotation does not resolve isomeric or isobaric features; features with identical m/z and similar RT within instrument resolution will be collapsed into a single node.
- Bioassay-guided fractionation assumes activity is proportional to compound abundance and does not account for synergistic or antagonistic interactions between co-eluting compounds.

## Evidence

- [readme] integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking: "integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking"
- [other] Load the molecular network graph structure (e.g., network edges and node identifiers from GNPS) and the bioassay-guided fractionation activity matrix: "Load the molecular network graph structure (e.g., network edges and node identifiers from GNPS) and the bioassay-guided fractionation activity matrix (fractions × bioactivity measurements)"
- [other] Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching: "Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching"
- [other] Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values): "Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature)"
- [other] Annotate the molecular network with bioactivity scores as node attributes. Export the integrated network with bioactivity annotations in a format compatible with Cytoscape: "Annotate the molecular network with bioactivity scores as node attributes. Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization"
- [readme] The code is released as a Jupyter notebook for easiness and reproducibility: "The code is released as a Jupyter notebook for easiness and reproducibility. The jupyter notebook has been prepared by Dr. Ricardo Silva"

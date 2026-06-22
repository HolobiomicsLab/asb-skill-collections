---
name: background-distribution-significance-thresholding
description: Use when use when the workflow requires background-distribution-significance-thresholding.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-distribution-significance-thresholding

## When to use

Use when the workflow requires background-distribution-significance-thresholding.

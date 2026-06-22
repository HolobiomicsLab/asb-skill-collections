---
name: graph-network-construction
description: Use when you have trained ML models that predict pairwise relationships (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - ML_function.ipynb
  - recon_mapping (MATLAB and Python scripts)
  - Recon3D
derived_from:
- doi: 10.1101/2024.08.17.608400v2
  title: Recon8D
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_recon8d_cq
    doi: 10.1101/2024.08.17.608400v2
    title: Recon8D
  dedup_kept_from: coll_recon8d_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.08.17.608400v2
  all_source_dois:
  - 10.1101/2024.08.17.608400v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-network-construction

## Summary

Construct a regulatory network graph by integrating machine learning predictions with known metabolic pathway topology, then validate edges against curated databases. This skill bridges model outputs to interpretable network representations suitable for systems-level biological inference.

## When to use

You have trained ML models that predict pairwise relationships (e.g., feature→metabolite associations with confidence scores) across multiple omics feature sets, and you need to organize these predictions into a unified network structure that can be queried, visualized, and compared against existing pathway knowledge. Use this skill when your ML outputs are feature importance scores or ranked predictions that need topological context and confidence validation.

## When NOT to use

- Your ML predictions are already embedded in a validated, published pathway database with no novel relationships to integrate.
- Feature importance scores are unavailable or cannot be reliably compared across replicates or control experiments.
- The input metabolites or features are not mappable to a reference metabolic model or genome annotation (i.e., no topological context available).

## Inputs

- Machine learning model outputs (feature importance rankings and predictions for each metabolite model)
- Multiomics feature sets (transcriptomics, proteomics, metabolomics, CNV, methylation, histone PTMs, miRNA, lncRNA)
- Metabolic network topology (e.g., Recon3D reactions and gene-metabolite associations)
- Curated interaction databases (e.g., KEGG, MetaCyc pathways)
- Cross-validation or replication control results (counts of feature appearances across experiments)

## Outputs

- Regulatory network graph in structured format (JSON, GML, or TSV edge list)
- Node and edge annotations (metabolites, regulatory features, confidence scores)
- Validated edge set with known pathway associations
- Confidence score matrix (feature × metabolite with numerical confidence 0–8 scale)

## How to apply

Collect the ranked feature importance outputs from all trained ML models (one per metabolite, one per feature set). For each predicted relationship, assign a confidence score derived from how consistently that feature appears across replicates or cross-validation folds (e.g., counting in how many of 8 control experiments the feature ranked in the top 20). Map features to genes and genes to metabolic reactions using genome-scale metabolic model annotations (e.g., Recon3D). Filter edges to retain only those with confidence above a threshold (e.g., confidence ≥ 2 out of 8 controls). Construct a directed graph where nodes are metabolites and features, and edges represent predicted regulatory relationships with confidence scores as edge weights. Validate by checking that high-confidence edges align with known metabolic pathways and curated interaction databases. Export the final network in a structured format (JSON, GML, or TSV edge list) with confidence scores and regulatory annotations for downstream analysis or visualization.

## Related tools

- **ML_function.ipynb** (Trains random forest, XGBoost, ridge, and lasso models and extracts feature importance scores for each metabolite model across nine feature sets) — https://github.com/sriram-lab/Metab8D
- **recon_mapping (MATLAB and Python scripts)** (Maps genes from metabolic reactions to top feature lists and translates gene names to BiggIDs for network integration) — https://github.com/sriram-lab/Metab8D
- **Recon3D** (Provides metabolic network topology, reactions, and gene-metabolite associations for graph construction and validation) — https://github.com/sriram-lab/Recon8D

## Evaluation signals

- Confidence scores are consistently calculated as counts (0–8) reflecting feature appearance across control experiments; verify that all edges in the output have confidence values in this expected range.
- High-confidence edges (confidence ≥ threshold) show statistically significant overlap with known metabolic pathways from Recon3D or curated databases (e.g., KEGG); validate by checking precision against independent pathway annotations.
- Network graph schema validation: nodes represent metabolites or omics features, directed edges point from features to metabolites with confidence and importance annotations; verify structure in exported file (JSON, GML, TSV).
- Feature-to-gene mappings resolve to valid NCBI gene symbols or BiggIDs; spot-check mappings using recon_mapping output.
- No duplicate edges in the final graph; all edge confidence scores are monotonically consistent with model cross-validation fold counts.

## Limitations

- Genomic mutations were excluded from random forest models due to their binary structure, limiting detection of mutational effects on metabolism.
- Network validation is constrained to features with previously identified mechanistic relationships in curated databases; novel regulatory relationships may be flagged but require independent experimental validation.
- Confidence scoring is tied to the number of control experiments (8 in the Metab8D study); studies with fewer replicates will have lower maximum confidence scores, reducing discriminatory power.
- The CCLE cell line panel may not represent all cell types or metabolic contexts; generalization to other tissues or conditions requires independent validation.
- Imputation method (KNN for missing values) may introduce bias if missingness is not random across omics layers.

## Evidence

- [other] Integrate model predictions with metabolic network topology to construct a regulome network graph.: "Integrate model predictions with metabolic network topology to construct a regulome network graph."
- [other] Validate predicted regulatory edges against known metabolic pathways and curated interaction databases.: "Validate predicted regulatory edges against known metabolic pathways and curated interaction databases."
- [other] Export the final regulome network in a structured format (e.g., JSON, GML, or TSV edge list) with confidence scores and regulatory annotations.: "Export the final regulome network in a structured format (e.g., JSON, GML, or TSV edge list) with confidence scores and regulatory annotations."
- [readme] The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found.: "The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along"
- [readme] confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features.: "confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features."
- [readme] ML script for random forests, XGBoost, ridge regression, and lasso regression, as well as feature importance generation.: "ML script for random forests, XGBoost, ridge regression, and lasso regression, as well as feature importance generation."
- [readme] MATLAB and Python scripts for extracting genes from reactions involving metabolites of interest and matching them with top feature lists: "MATLAB and Python scripts for extracting genes from reactions involving metabolites of interest and matching them with top feature lists"

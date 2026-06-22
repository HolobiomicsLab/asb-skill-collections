---
name: mass-spectrometry-feature-representation
description: Use when after LC-MS feature clustering based on MS-DIAL peak character estimation, when you have grouped features that share similar chromatographic or spectral properties and need to select a single representative feature per cluster to reduce false positives and redundant annotations before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2928
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL v4.00 or higher
  - MS-FINDER 3.30 or higher
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-representation

## Summary

Extract representative parental signals from clustered LC-MS features using multi-level modularity optimization. This skill identifies and ranks the most informative feature from each cluster to reduce redundancy while preserving biological signal for downstream annotation.

## When to use

After LC-MS feature clustering based on MS-DIAL peak character estimation, when you have grouped features that share similar chromatographic or spectral properties and need to select a single representative feature per cluster to reduce false positives and redundant annotations before MS-FINDER database querying.

## When NOT to use

- Input features have not been clustered; apply feature clustering step first.
- Single features or unclustered feature sets — this skill requires cluster group structure to meaningfully rank modularity.
- Data acquired in MS1-only mode without MS/MS spectra — MS-CleanR workflow requires all features to have MS/MS data and will discard MS1-only features.

## Inputs

- Pre-clustered LC-MS feature set from MS-DIAL peak character estimation
- Feature cluster assignments with MS-DIAL metadata (m/z, retention time, peak shape metrics)

## Outputs

- Extracted parental feature list with cluster identifiers and modularity scores
- Structured output file compatible with MS-FINDER annotation input format

## How to apply

Apply a multi-level optimization of modularity algorithm to each pre-clustered feature group (output from MS-DIAL peak character estimation clustering). Score each feature in the cluster by modularity, then select the highest-modularity feature as the parental signal representative. Modularity scoring ranks features based on their connectivity and influence within the cluster structure. Compile all selected parental features into a structured output file, preserving cluster membership annotations. This approach balances feature reduction with biological signal retention by choosing the most network-central feature per cluster rather than arbitrarily selecting the first or most intense feature.

## Related tools

- **MS-CleanR** (Executes multi-level optimization of modularity algorithm on feature clusters and exports parental signals) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL v4.00 or higher** (Produces initial peak character estimation and feature clustering input) — http://prime.psc.riken.jp/compms/index.html
- **MS-FINDER 3.30 or higher** (Accepts exported parental features for in silico annotation via hydrogen rearrangement rules scoring) — http://prime.psc.riken.jp/compms/index.html

## Examples

```
After MS-DIAL feature clustering, MS-CleanR applies modularity optimization via: runGUI() → [select clustered feature set] → [run parental signal extraction step] → export_parental_features_to_msfinder(output_file='parental_signals.csv')
```

## Evaluation signals

- Each cluster has exactly one parental feature selected (no multi-selection or orphaned clusters).
- Modularity scores are ranked within each cluster and highest-scoring feature is consistently selected.
- Output file schema matches MS-FINDER input requirements (m/z, retention time, cluster ID, intensity preserved).
- Parental feature count equals number of input clusters; cluster membership is traceable.
- Downstream MS-FINDER annotation succeeds without input format errors on exported parental features.

## Limitations

- At least 3 blank and 3 quality control (QC) samples must be identified in the MS-DIAL sample list; Blank ratio analysis fails with fewer replicates.
- All features without MS/MS spectra are discarded during prior filtering steps; MS1-only datasets will cause the workflow to crash.
- Modularity-based ranking is sensitive to cluster architecture; poorly resolved or overlapping clusters may not yield biologically meaningful representatives.
- The tool is no longer actively maintained as MSDial 5.x has integrated parts of MS-CleanR functionality; reproducibility with future MSDial versions is uncertain.

## Evidence

- [other] Apply the multi-level optimization of modularity algorithm to each cluster to identify and rank representative parental features by modularity score.: "Apply the multi-level optimization of modularity algorithm to each cluster to identify and rank representative parental features by modularity score."
- [readme] feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [other] Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation.: "Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation."
- [readme] All these options are tunable by the user. The second step involves a feature clustering method based on MS-DIAL peak character estimation algorithm: "The second step involves a feature clustering method based on MS-DIAL peak character estimation algorithm"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis.: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis."
- [readme] Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained.: "Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained."

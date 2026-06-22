---
name: parental-signal-selection-from-clusters
description: Use when after feature clustering has grouped LC-MS peaks by MS-DIAL peak character estimation, you need to reduce the cluster to a single representative feature per biological entity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MS-CleanR
  - MS-DIAL v4.00 or higher
  - MS-FINDER 3.30 or higher
  techniques:
  - LC-MS
  - tandem-MS
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

# parental-signal-selection-from-clusters

## Summary

Extract representative parental features from LC-MS clustered data using multi-level optimization of modularity scoring. This skill ranks and selects the highest-modularity feature from each cluster to reduce redundancy and enable focused downstream annotation.

## When to use

After feature clustering has grouped LC-MS peaks by MS-DIAL peak character estimation, you need to reduce the cluster to a single representative feature per biological entity. Apply this skill when you have redundant or adduct-related features grouped together and require one canonical parental signal per cluster for MS-FINDER annotation.

## When NOT to use

- Input data lacks MS/MS spectra — MS-CleanR will discard MS1-only features and crash on the first step
- Features have not been pre-clustered by MS-DIAL peak character estimation — this skill assumes clustering is already complete
- You need to retain all fragment ions and isotope variants — parental signal selection discards redundant features by design

## Inputs

- Pre-clustered LC-MS feature set (grouped by MS-DIAL peak character estimation)
- Feature cluster assignments with MS/MS spectral data
- MS-DIAL peak list in DDA or DIA mode (positive, negative, or both ionization modes)

## Outputs

- Parental feature set (one representative per cluster)
- Structured output file compatible with MS-FINDER annotation
- Modularity scores per feature (for ranking and QC)

## How to apply

Load the pre-clustered feature set output from the MS-DIAL peak character estimation clustering step. Apply the multi-level optimization of modularity algorithm to each cluster to compute modularity scores for all features within that cluster. The modularity score ranks features by their connectivity and representativeness within the cluster structure. Select the feature with the highest modularity score from each cluster as the parental signal representative. Compile the selected parental features into a structured output file (compatible with MS-FINDER input format) for downstream in silico annotation using hydrogen rearrangement rules scoring.

## Related tools

- **MS-CleanR** (Executes multi-level modularity optimization and parental feature selection on clustered features) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL v4.00 or higher** (Generates peak character estimation and initial feature clustering prior to parental signal extraction) — http://prime.psc.riken.jp/compms/index.html
- **MS-FINDER 3.30 or higher** (Accepts exported parental features for in silico annotation using hydrogen rearrangement rules scoring) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Each cluster yields exactly one output parental feature (cardinality check)
- Parental feature modularity scores are ≥ all other features in the same cluster (monotonicity)
- Output file format is compatible with MS-FINDER input requirements (schema validation)
- Exported features retain MS/MS spectral data and precursor m/z values from the original peak list
- No features from the original clustered set are lost; only one per cluster is selected (completeness)

## Limitations

- Requires at least 3 blank and 3 quality-control (QC) samples pre-labeled in the MS-DIAL sample list for blank ratio analysis
- All input features must have MS/MS data; features with MS1 only will be discarded or cause the workflow to crash
- Sample and class names must avoid spaces, hyphens, and single-letter class names to prevent parsing errors
- R version > 4.2 may encounter 'Error: the condition has length > 1' during downstream database annotation merging
- MS-CleanR is no longer actively maintained; development has shifted to MS-DIAL 5.x integration

## Evidence

- [other] MS-CleanR performs parental signal extraction from clustered features using a multi-level optimization of modularity algorithm, following an initial feature clustering step based on MS-DIAL peak character estimation.: "MS-CleanR performs parental signal extraction from clustered features using a multi-level optimization of modularity algorithm, following an initial feature clustering step based on MS-DIAL peak"
- [other] Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation. Apply the multi-level optimization of modularity algorithm to each cluster to identify and rank representative parental features by modularity score. Select the highest-modularity feature from each cluster as the parental signal representative.: "Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation. Apply the multi-level optimization of modularity"
- [readme] feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."

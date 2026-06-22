---
name: qiime2-artifact-inspection
description: Use when you need to verify that a QIIME 2 artifact (e.g., a Chemical Feature Tree from q2-qemistree, a FeatureTable[Frequency], or a Phylogeny[Rooted] object) has been correctly produced, before using it as input to downstream analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3489
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - q2-qemistree
  - QIIME 2
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qemistree
    doi: 10.1038/s41589-020-00677-3
    title: qemistree
  dedup_kept_from: coll_qemistree
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00677-3
  all_source_dois:
  - 10.1038/s41589-020-00677-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QIIME 2 Artifact Inspection

## Summary

Load, validate, and parse QIIME 2 serialized artifacts (.qza files) to inspect their structure, format, and metadata. This skill is essential for understanding the composition and properties of intermediate and final analysis outputs, particularly phylogenetic trees and feature tables produced by metabolomic pipelines.

## When to use

Apply this skill when you need to verify that a QIIME 2 artifact (e.g., a Chemical Feature Tree from q2-qemistree, a FeatureTable[Frequency], or a Phylogeny[Rooted] object) has been correctly produced, before using it as input to downstream analyses. Use it to diagnose malformed artifacts, validate tree connectivity, count nodes, or extract node labels and structural metadata.

## When NOT to use

- Input artifact is already extracted and in plain-text format (e.g., already exported to Newick or CSV); use standard file inspection tools instead.
- Goal is to modify or filter the artifact contents; use qiime2-specific filtering or pruning commands (e.g., `qiime qemistree prune-hierarchy`) instead.
- Artifact path or format is unknown and needs to be discovered; use QIIME 2's `qiime tools list-plugins` or `qiime tools import` help first.

## Inputs

- QIIME 2 artifact file (.qza) in serialized format
- Tree artifact in Newick format or QIIME 2 Phylogeny[Rooted] object
- Feature table artifact (FeatureTable[Frequency])
- Feature data artifact (FeatureData[Molecules])

## Outputs

- Inspection report with artifact format and type
- Node count (leaves and internal nodes for trees)
- Tree depth and branching statistics
- Node labels and metadata extracted from tree
- Validation status (connectivity verified, no malformed branches)

## How to apply

First, load the .qza artifact file using QIIME 2 artifact inspection tools (e.g., `qiime tools inspect-metadata` or direct deserialization). Validate the file format by checking whether it is a valid QIIME 2 serialized object or, for tree artifacts, whether it is in Newick format. Parse the artifact's internal structure—for trees, count total nodes (leaves + internal nodes), verify tree connectivity, and check for malformed branches. Extract structural properties including tree depth, branching statistics, and node labels. Compare the artifact's node count and connectivity against expected values from the pipeline parameters (e.g., number of MS1 features input to make-hierarchy, expected filtering from SIRIUS fingerprint prediction success rates). Report any deviations from expected structure.

## Related tools

- **QIIME 2** (Artifact serialization framework and inspection toolkit) — https://docs.qiime2.org/
- **q2-qemistree** (Source of Chemical Feature Tree artifacts to be inspected) — https://github.com/biocore/q2-qemistree

## Evaluation signals

- Artifact successfully loads without deserialization errors and metadata is readable.
- Reported node count matches expected count from pipeline input (number of MS1 features with predicted fingerprints by SIRIUS, typically 70–90% of input features).
- Tree is fully connected with no orphaned branches, and all leaf nodes correspond to MS1 features in the input feature table.
- Tree depth and branching statistics are consistent with hierarchical clustering of molecular substructures (expected branching factor and depth scale with number of unique substructure patterns).
- Node labels are present and match feature identifiers in the corresponding feature data file (FeatureData[Molecules]).

## Limitations

- SIRIUS predicts molecular substructures for only a subset of MS1 features (typically 70–90% depending on sample type, MS2 spectrum quality, and user-defined tolerances such as ppm-max and zodiac-threshold); features without fingerprints are filtered out before tree construction and will not appear as nodes.
- Tree structure and node count depend critically on SIRIUS version compatibility; the README notes that q2-qemistree was initially developed for Sirius 4.0.1 and has been adapted for versions > 4.4.29, so older Sirius versions may produce incompatible artifact structures.
- If MGF file has formatting errors (e.g., missing MS1 entries, MS1 entries without corresponding MS2 entries), the upstream artifact generation fails and inspection will reveal a malformed or incomplete artifact.
- Artifact inspection alone does not validate the chemical correctness of the molecular substructure predictions or the biological relevance of the hierarchy; it only confirms structural integrity.

## Evidence

- [other] q2-qemistree is designed to build a tree of mass-spectrometry features for chemically-informed metabolomic profile comparison: "q2-qemistree is designed to build a tree of mass-spectrometry features for chemically-informed metabolomic profile comparison."
- [other] Validate file format as either Newick or QIIME 2 serialized object. Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches.: "Validate file format as either Newick or QIIME 2 serialized object. Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches."
- [readme] A combined feature data file that contains unique identifiers of each feature, their corresponding original feature identifier (row ID from Mzmine2), parent mass (`parent_mass`), retention time (`retention_time`), CSI:FingerID structure predictions (`csi_smiles`), MS2 match structure predictions (`ms2_smiles`), and the table(s) (`table_number`) that each feature was detected in.: "A combined feature data file that contains unique identifiers of each feature, their corresponding original feature identifier, parent mass, retention time, CSI:FingerID structure predictions, and"
- [readme] SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment (based on factors such as sample type, the quality MS2 spectra, and user-defined tolerances such as `--p-ppm-max`, `--p-zodiac-threshold`): "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment based on factors such as sample type, the quality MS2 spectra, and"
- [readme] If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot this step before proceeding forward.: "If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot"

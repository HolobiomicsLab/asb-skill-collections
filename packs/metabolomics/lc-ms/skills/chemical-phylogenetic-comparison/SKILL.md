---
name: chemical-phylogenetic-comparison
description: Use when you have LC-MS/MS data preprocessed with MZmine2 into an MGF file (containing MS1 and MS2 spectra) and a feature table (peak areas per sample), and you want to relate MS1 features to each other based on predicted molecular substructures and chemical properties rather than arbitrary.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3324
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - q2-qemistree
  - SIRIUS
  - MZmine2
  - GNPS FBMN
  - Classyfire
  techniques:
  - LC-MS
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

# chemical-phylogenetic-comparison

## Summary

Build a phylogenetic tree of mass-spectrometry features based on predicted molecular substructures to enable chemically-informed, tree-based comparison of untargeted metabolomic profiles across samples and datasets. This skill bridges mass-spectrometry feature detection with chemical taxonomy to support alpha- and beta-diversity analyses rooted in molecular similarity rather than sequence homology.

## When to use

You have LC-MS/MS data preprocessed with MZmine2 into an MGF file (containing MS1 and MS2 spectra) and a feature table (peak areas per sample), and you want to relate MS1 features to each other based on predicted molecular substructures and chemical properties rather than arbitrary clustering. Use this skill when comparing metabolomic profiles across multiple samples or datasets and you need a phylogenetic framework that accounts for chemical structure similarity—especially when 70–90% of features have sufficient MS2 spectral quality for SIRIUS to predict molecular formulas and substructures.

## When NOT to use

- Input data is already processed into a phylogenetic tree (avoid re-running make-hierarchy on downstream trees)
- MS2 spectral quality is poor or sparse; SIRIUS will predict formulas and fingerprints for <70% of features, limiting tree informativeness
- You require targeted metabolite identification rather than relative chemical comparison; Qemistree predicts structure properties but does not perform confident compound annotation

## Inputs

- MGF file (MS1 and MS2 spectra) imported as QIIME 2 MassSpectrometryFeatures artifact
- Feature table (peak areas) imported as QIIME 2 FeatureTable[Frequency] artifact
- Optionally: MS/MS spectral library matches (FeatureData[Molecules]) from FBMN or similar

## Outputs

- Phylogeny[Rooted] tree relating MS1 features based on molecular substructure similarity
- FeatureTable[Frequency] merged and filtered to retain only features with fingerprints
- FeatureData[Molecules] containing unique feature IDs, parent mass, retention time, CSI:FingerID SMILES, MS2 match SMILES, and original table assignments
- Optionally: FeatureData[Molecules] with Classyfire taxonomy (kingdom, superclass, class, subclass, direct_parent)

## How to apply

Import the MGF file and feature table into QIIME 2 artifact format (.qza). Run q2-qemistree's compute-fragmentation-trees to generate candidate molecular formulas using SIRIUS (requires SIRIUS binary and Java; typical parameters: ppm-max 15, profile orbitrap, ions-considered '[M+H]+', and sufficient heap memory). Rerank molecular formulas using SIRIUS ZODIAC (zodiac-threshold 0.95). Predict molecular fingerprints (2936 properties) via CSI:FingerID. Finally, invoke make-hierarchy to construct a rooted phylogenetic tree using the predicted molecular substructures as the basis for hierarchical clustering; this tree can optionally incorporate MS/MS library spectral matches. The resulting tree and feature table are filtered to retain only features with fingerprint predictions, and optional Classyfire taxonomy classification can be applied. Use the tree with standard QIIME 2 alpha- and beta-diversity methods.

## Related tools

- **q2-qemistree** (QIIME 2 plugin implementing the full chemical-phylogenetic workflow: compute-fragmentation-trees, rerank-molecular-formulas, predict-fingerprints, make-hierarchy, get-classyfire-taxonomy, prune-hierarchy) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (De-novo identification and molecular formula prediction; generates fragmentation trees and predicts molecular substructures via CSI:FingerID) — https://bio.informatik.uni-jena.de/sirius/
- **MZmine2** (Upstream peak detection and MS1/MS2 feature extraction producing MGF and feature table inputs) — http://mzmine.github.io
- **GNPS FBMN** (Optional source of MS2 spectral library matches (clusterinfo_summary results) for inclusion in make-hierarchy) — https://gnps.ucsd.edu/
- **Classyfire** (Chemical taxonomy assignment (kingdom, superclass, class, subclass, direct_parent) applied post-hoc via qiime qemistree get-classyfire-taxonomy)

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Tree topology is valid Newick format; rooted tree has no cycles and all tips correspond to features in the feature table
- Feature table and FeatureData[Molecules] have matching row IDs and consistent sample counts; no features appear in the tree without corresponding rows in the filtered feature table
- CSI:FingerID SMILES predictions are non-empty for 70–90% of features (expected SIRIUS success rate); fingerprint positions retained match either all 2936 properties (default) or 489 PubChem properties (if --p-qc-properties was set)
- Parent mass, retention time, and original feature identifiers (from MZmine2) are correctly populated in FeatureData[Molecules]
- If Classyfire taxonomy was applied, all features have non-null assignments for 'kingdom' and 'superclass' (mandatory levels); 'structure_source' column correctly records whether assignments derive from ms2_smiles or csi_smiles

## Limitations

- SIRIUS predicts molecular substructures for only 70–90% of MS1 features, depending on sample type, MS2 spectral quality, and user-defined ppm and zodiac thresholds; features without predictions are filtered from downstream analysis
- Molecular formula and fingerprint predictions are probabilistic and may not represent true structures, especially for rare or novel compounds not well-represented in SIRIUS training data
- Tree construction assumes molecular substructure similarity correlates with biological relevance; compounds with similar fingerprints may have different biological functions
- Requires external SIRIUS binary installation and substantial Java memory (minimum -Xms16G -Xmx64G recommended); computationally expensive for large datasets (thousands of features)
- Latest SIRIUS PubChem fingerprints are frozen at August 13, 2017; newer chemical databases are not reflected

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset."
- [readme] These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses.: "These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses."
- [readme] MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment"
- [readme] To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1. An MGF file with both MS1 and MS2 information... 2. A feature table with peak areas of MS1 ions per sample.: "To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data using MZmine2 and produce MGF file with both MS1 and MS2 information and a feature"
- [readme] A combined feature data file that contains unique identifiers of each feature, their corresponding original feature identifier, parent mass, retention time, CSI:FingerID structure predictions, MS2 match structure predictions, and the table(s) that each feature was detected in.: "A combined feature data file that contains unique identifiers of each feature, parent mass, retention time, CSI:FingerID structure predictions, MS2 match structure predictions"

---
name: ms-feature-tree-construction
description: Use when you have untargeted LC-MS/MS metabolomic data (peak-detected
  .mzXML/.mzML/.mzDATA files processed through MZmine2) and need to relate MS1 features
  by chemical similarity rather than sequence homology.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - q2-qemistree
  - SIRIUS
  - MZmine2
  - Classyfire
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed
  comparison of untargeted metabolomic profiles.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qemistree_cq
    doi: 10.1038/s41589-020-00677-3
    title: qemistree
  dedup_kept_from: coll_qemistree_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00677-3
  all_source_dois:
  - 10.1038/s41589-020-00677-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-feature-tree-construction

## Summary

Build a phylogenetic tree relating mass-spectrometry (LC-MS/MS) features based on predicted molecular substructures to enable chemically-informed comparative metabolomic analysis. This skill integrates fragmentation tree generation, molecular formula ranking, fingerprint prediction, and hierarchical clustering into a unified workflow for untargeted metabolomic profiling.

## When to use

Apply this skill when you have untargeted LC-MS/MS metabolomic data (peak-detected .mzXML/.mzML/.mzDATA files processed through MZmine2) and need to relate MS1 features by chemical similarity rather than sequence homology. Use it specifically when you aim to perform phylogeny-informed alpha- or beta-diversity analysis, conduct meta-analyses across multiple metabolomic datasets, or integrate chemical taxonomy (Classyfire) classifications into your comparative analysis.

## When NOT to use

- Input data are already in feature-tree format or pre-constructed phylogenetic trees; skip directly to diversity analysis.
- Raw mass-spectrometry files have not been peak-detected or lack MS2 fragmentation spectra; preprocessing through MZmine2 is mandatory.
- Dataset contains fewer than ~50 MS1 features with high-quality MS2 spectra; SIRIUS fingerprint prediction success rate typically covers only 70–90% of detected features depending on sample type and spectral quality.

## Inputs

- MGF file with MS1 and MS2 spectra (imported as MassSpectrometryFeatures QIIME 2 artifact)
- Feature table in BIOM format with peak areas per sample (imported as FeatureTable[Frequency])
- SIRIUS binary (version ≥4.4.29; path specified via --p-sirius-path)

## Outputs

- Rooted phylogenetic tree relating MS1 features (Phylogeny[Rooted] QIIME 2 artifact)
- Merged feature table with MS1 features lacking fingerprints filtered out (FeatureTable[Frequency])
- Feature metadata table containing parent mass, retention time, CSI:FingerID SMILES predictions, MS2 library match SMILES, and table-of-origin identifiers (FeatureData[Molecules])
- Optional: Classyfire-classified feature data with chemical kingdom, superclass, class, subclass, and direct_parent assignments (FeatureData[Molecules])

## How to apply

Begin by preprocessing raw mass-spectrometry data through MZmine2 to generate an MGF file (containing both MS1 and MS2 information) and a feature table (BIOM format with peak areas per sample). Import both into QIIME 2 artifact format. Execute compute-fragmentation-trees (with parameters like --p-ppm-max 15, --p-profile orbitrap, and appropriate adducts such as [M+H]+) to generate SIRIUS fragmentation trees and candidate molecular formulas. Rerank molecular formulas using ZODIAC (--p-zodiac-threshold 0.95 recommended) to select top-scoring formulas. Predict molecular fingerprints via CSI:FingerID (--p-ppm-max 20), which outputs probabilities for 2936 molecular substructures. Finally, call make-hierarchy to cluster features based on predicted fingerprints and generate a rooted phylogenetic tree. Optionally filter to PubChem fingerprint positions (489 properties) using --p-qc-properties, include MS/MS spectral library matches (--i-ms2-matches), or merge multiple datasets for meta-analysis by providing multiple CSI-results and feature-table pairs in the same order.

## Related tools

- **q2-qemistree** (Orchestrates the full feature-tree construction pipeline, including fragmentation-tree generation, molecular-formula ranking, fingerprint prediction, and hierarchy generation from SIRIUS output) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (Generates fragmentation trees and de-novo molecular substructure predictions via CSI:FingerID; provides candidate molecular formulas ranked by ZODIAC) — https://bio.informatik.uni-jena.de/sirius/
- **MZmine2** (Upstream peak detection and feature extraction; produces MGF and feature-table inputs required by q2-qemistree) — http://mzmine.github.io
- **Classyfire** (Assigns chemical taxonomy (kingdom, superclass, class, subclass, direct_parent) to MS1 features based on predicted or library-matched structures)

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Output tree file (Newick or .tree format) is valid Phylogeny[Rooted] artifact with all MS1 features having fingerprints represented as internal and leaf nodes.
- Merged feature table contains only features with non-null CSI:FingerID predictions; row count reflects ~70–90% retention relative to input feature count depending on dataset quality.
- Feature metadata includes non-null parent_mass, retention_time, and csi_smiles (or ms2_smiles when library matches are provided) for all features in output tree.
- Tree branch lengths reflect Tanimoto or Euclidean distances computed from the 2936-property (or 489 PubChem-filtered) fingerprint contingency table; tree should group chemically similar features (validated via structure homology of cluster members).
- Classyfire taxonomy assignments correctly map SMILES structures to chemical ontology terms; structure_source column correctly records whether prediction came from CSI:FingerID or MS2 library matches.

## Limitations

- SIRIUS fingerprint prediction covers only 70–90% of detected MS1 features; features without predictions are filtered from the output tree and cannot be included in downstream diversity analyses.
- Molecular formula ranking accuracy depends on high-quality MS2 spectra and appropriate selection of adduct parameters (e.g., [M+H]+, [M+Na]+); incorrect adduct specification will produce invalid molecular formulas.
- CSI:FingerID was trained on SIRIUS v4.0.1 and later adapted to Sirius ≥4.4.29; older or future SIRIUS versions may not be compatible.
- Meta-analysis requires strict one-to-one correspondence between CSI results, feature tables, and MS2 match tables; misalignment in input order will cause erroneous feature associations across datasets.
- PubChem fingerprint filtering (--p-qc-properties) uses PubChem version downloaded 13 August 2017; updates to PubChem structure database may affect reproducibility.
- Computational requirements are substantial: Java heap size recommendations range from -Xms16G to -Xmx64G; users must provide adequate temporary directory storage and write permissions.

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] The workflow requires preprocessing with MZmine2 to generate MGF and feature table inputs before importing into QIIME 2.: "To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1."
- [readme] SIRIUS fragmentation trees and molecular formula generation is the first computational step after data import.: "First, we generate fragmentation trees for molecular peaks detected using MZmine2: qiime qemistree compute-fragmentation-trees --p-sirius-path 'sirius.app/Contents/MacOS' --i-features sirius.mgf.qza"
- [readme] ZODIAC reranks molecular formulas with recommended threshold of 0.95.: "Next, we select top scoring molecular formula as follows: qiime qemistree rerank-molecular-formulas --p-zodiac-threshold 0.95"
- [readme] CSI:FingerID predicts 2936 molecular properties; filtering to PubChem positions reduces to 489 properties.: "This gives us a QIIME 2 artifact of type CSIFolder that contains probabilities of molecular substructures (total 2936 molecular properties) within in each feature. By default, we retain all"
- [readme] Feature retention and filtering depend on SIRIUS fingerprint prediction success, typically 70–90% of features.: "MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1"
- [readme] Output tree and feature table enable downstream phylogeny-based alpha and beta diversity analyses.: "These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses."
- [readme] Meta-analysis requires datasets provided in matching order with one-to-one correspondence.: "The input CSI results, feature tables and MS2 match tables should have a one-to-one correspondence i.e CSI results, feature tables and MS2 match tables from all datasets should be provided in the"

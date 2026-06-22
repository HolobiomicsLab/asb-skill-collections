---
name: chemical-similarity-clustering
description: Use when you have untargeted LC-MS/MS metabolomic data (MS1 features with MS2 fragmentation spectra) preprocessed by MZmine2 into a feature table (BIOM format) and MGF file, and you want to construct a chemically-informed hierarchy of features for alpha/beta-diversity analysis or to group features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - q2-qemistree
  - SIRIUS
  - MZmine2
  - GNPS FBMN
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

# chemical-similarity-clustering

## Summary

Build a tree of mass-spectrometry features based on predicted molecular substructures to cluster and compare untargeted metabolomic LC-MS/MS profiles by chemical similarity. This enables phylogeny-aware diversity analysis of metabolites within and across samples.

## When to use

You have untargeted LC-MS/MS metabolomic data (MS1 features with MS2 fragmentation spectra) preprocessed by MZmine2 into a feature table (BIOM format) and MGF file, and you want to construct a chemically-informed hierarchy of features for alpha/beta-diversity analysis or to group features by predicted molecular substructures rather than by mass or retention time alone.

## When NOT to use

- Input is already a phylogenetic tree or feature abundance table without raw MS data; tree construction requires fragmentation spectra and molecular structure prediction.
- MS1 features lack MS2 spectra or have poor-quality fragmentation data; SIRIUS cannot reliably predict molecular formulas/substructures without sufficient spectral signal.
- You need exact molecular identities rather than chemically-informed clustering; q2-qemistree predicts substructure probabilities and performs de-novo annotation, not targeted compound matching.

## Inputs

- MGF file (MS1 and MS2 spectra; imported as QIIME 2 MassSpectrometryFeatures artifact)
- Feature abundance table in BIOM format (imported as QIIME 2 FeatureTable[Frequency] artifact)
- SIRIUS installation (>=4.4.29) with path to executable
- Optional: MS2 spectral library matches (FBMN output; FeatureData[Molecules] artifact)

## Outputs

- Rooted phylogeny tree (Phylogeny[Rooted]; Newick format)
- Filtered feature abundance table (FeatureTable[Frequency]) with only fingerprint-bearing features
- Feature metadata table (FeatureData[Molecules]) including parent mass, retention time, CSI SMILES, MS2 SMILES, and table origin
- Optional: ClassyFire chemical taxonomy annotations (kingdom, superclass, class, subclass, direct_parent)

## How to apply

Preprocess MS data using MZmine2 to generate an MGF file (with both MS1 and MS2 spectra) and a feature abundance table (BIOM format). Import both into QIIME 2 artifact format. Execute the q2-qemistree pipeline: (1) compute fragmentation trees using SIRIUS with user-defined adducts (e.g., [M+H]+) and mass tolerance (typically 15 ppm); (2) rerank molecular formulas using ZODIAC with a confidence threshold (e.g., 0.95); (3) predict molecular substructures (fingerprints) via CSI:FingerID with ppm-max typically set to 20; (4) call make-hierarchy to construct the feature tree from predicted fingerprints, merging feature tables and outputting a rooted phylogeny, hashed feature table, and feature metadata. The tree is built by hierarchical clustering of the 2936 (or 489 if PubChem-filtered) binary molecular properties across all features, with optional filtering to remove features lacking fingerprints. Optionally integrate MS2 spectral library matches (e.g., from GNPS FBMN) to annotate nodes with known structures.

## Related tools

- **q2-qemistree** (orchestrates the complete pipeline: compute-fragmentation-trees, rerank-molecular-formulas, predict-fingerprints, make-hierarchy, and get-classyfire-taxonomy commands) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (de-novo identification of molecular formulas from fragmentation trees and prediction of molecular substructures via CSI:FingerID) — https://bio.informatik.uni-jena.de/sirius/
- **MZmine2** (peak detection and feature extraction from LC-MS/MS raw data; outputs MGF and feature table required as q2-qemistree inputs) — http://mzmine.github.io
- **GNPS FBMN** (optional: generates MS2 spectral library matches for structural annotation; output can be integrated into make-hierarchy via --i-ms2-matches) — https://gnps.ucsd.edu/ProteoSAFe/index.jsp?params=%7B%22workflow%22:%22FEATURE-BASED-MOLECULAR-NETWORKING%22%7D

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Output tree is a valid rooted Newick phylogeny with branch lengths reflecting Tanimoto distance between feature fingerprints; can be visualized in phylogenetic software.
- Filtered feature table contains only features with non-null fingerprints; row count typically 70–90% of input features depending on MS2 spectral quality and SIRIUS success rate.
- Feature metadata table has one row per feature with valid parent_mass, retention_time, and csi_smiles (and ms2_smiles if MS2 matches provided); no missing critical fields.
- Downstream alpha/beta-diversity metrics (Faith PD, Bray-Curtis) computed on the tree and filtered table are consistent with expected metabolomic variability; tree exhibits meaningful chemical groupings visually inspectable via QIIME 2 Emperor or iTol.
- ClassyFire taxonomy output shows >70% of features classified to at least 'class' level; structure_source column indicates source of SMILES (CSI vs. MS2).

## Limitations

- SIRIUS predicts molecular substructures for only a subset of features (typically 70–90%), dependent on MS2 spectral quality, sample type, and user-defined tolerances (ppm-max, zodiac-threshold); features without fingerprints are filtered out before tree construction.
- De-novo molecular formula and substructure prediction are probabilistic; predicted structures may not match true chemistry, especially for novel or low-abundance compounds; integration of MS2 spectral library matches (via --i-ms2-matches) improves confidence.
- Requires SIRIUS ≥4.4.29 (older versions incompatible); CSI:FingerID uses PubChem fingerprint database downloaded on 13 August 2017, so newly reported substructures are not recognized.
- Tree construction merges input feature tables; non-unique feature identifiers across datasets may cause collisions; features are automatically hashed to prevent overlap.
- Computationally intensive: fragmentation tree generation and CSI:FingerID prediction require significant Java heap memory (>16 GB recommended) and storage for temporary files; user must provide writable tmpdir with sufficient space.

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] q2-qemistree uses SIRIUS, a software-framework developed for de-novo identification of metabolites. We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset."
- [readme] These input files can be obtained following peak detection in MZmine2. To begin this demonstration, create a separate folder to store all the inputs and outputs.: "These input files can be obtained following peak detection in MZmine2."
- [readme] A combined feature table by merging all the input feature tables; MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment.: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment (based on factors such as sample type, the quality MS2 spectra, and"
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`. By default, we retain all fingerprint positions i.e. 2936 molecular properties).: "A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`. By default, we retain all fingerprint positions i.e."
- [readme] These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses.: "These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses."
- [readme] Qemistree will use `ms2_smiles` to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, `csi_smiles` will be used.: "Qemistree will use `ms2_smiles` to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, `csi_smiles` will be used."

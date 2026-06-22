---
name: metabolomic-feature-tree-construction
description: Use when when you have preprocessed LC-MS/MS data (MGF file with MS1 and MS2 spectra and a feature abundance table from MZmine2 or similar peak detection tool) and need to perform chemical phylogeny-based diversity analyses or meta-analyses comparing metabolomic profiles across multiple samples or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3934
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2275
  tools:
  - q2-qemistree
  - SIRIUS
  - MZmine2
  - GNPS (Feature-Based Molecular Networking)
  techniques:
  - LC-MS
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

# metabolomic-feature-tree-construction

## Summary

Build a tree of LC-MS/MS features that relates mass-spectrometry peaks according to predicted molecular substructures, enabling chemically-informed comparison of untargeted metabolomic profiles across samples and datasets. The tree is constructed by predicting molecular substructures using fragmentation trees and molecular formula rankings, then hierarchically organizing features based on shared chemical properties.

## When to use

When you have preprocessed LC-MS/MS data (MGF file with MS1 and MS2 spectra and a feature abundance table from MZmine2 or similar peak detection tool) and need to perform chemical phylogeny-based diversity analyses or meta-analyses comparing metabolomic profiles across multiple samples or experiments. Use this skill specifically when you want to leverage predicted molecular substructures rather than spectral similarity alone to group related compounds.

## When NOT to use

- Input feature table already contains only 70–90% of original MS1 features (expected loss from SIRIUS prediction; do not re-filter)
- You only have MS1 mass-to-charge data without MS2 fragmentation spectra (fragmentation trees require both MS1 and MS2)
- Your MGF file lacks proper formatting, missing MS1 entries, or MS1 entries without corresponding MS2 entries (pre-validate MGF in MZmine2)

## Inputs

- FeatureTable[Frequency] (QIIME 2 artifact: feature abundance table from peak detection)
- MassSpectrometryFeatures (QIIME 2 artifact: MGF file with MS1 and MS2 spectra)
- CSIFolder (optional: pre-computed molecular fingerprints from predict-fingerprints)
- FeatureData[Molecules] (optional: MS/MS spectral library matches from FBMN workflow)

## Outputs

- Phylogeny[Rooted] (tree relating MS1 features based on molecular substructures)
- FeatureTable[Frequency] (filtered feature table, MS1 features without fingerprints removed)
- FeatureData[Molecules] (feature metadata including parent mass, retention time, CSI:FingerID SMILES, MS2 SMILES, table_number)

## How to apply

First, import the MGF file and feature table into QIIME 2 artifacts (FeatureTable[Frequency] and MassSpectrometryFeatures types). Then execute a sequential pipeline: (1) compute fragmentation trees using SIRIUS with specified adduct types (e.g., [M+H]+) and ppm tolerance (typically 15 ppm for high-resolution Orbitrap data); (2) rerank molecular formulas using ZODIAC with a threshold (typically 0.95) to select top-scoring candidates; (3) predict molecular fingerprints (2936 molecular properties via CSI:FingerID); (4) invoke make-hierarchy to generate the tree by clustering features based on predicted substructures. Set Java heap flags appropriately (-Xms16G -Xmx64G) and provide sufficient temporary disk space. For meta-analyses, pair CSI results and feature tables in corresponding order.

## Related tools

- **q2-qemistree** (Core QIIME 2 plugin implementing the complete workflow (compute-fragmentation-trees, rerank-molecular-formulas, predict-fingerprints, make-hierarchy commands)) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (Dependency used to compute fragmentation trees and predict molecular formulas and substructures (CSI:FingerID)) — https://bio.informatik.uni-jena.de/sirius/
- **MZmine2** (Preprocessing tool to detect peaks and generate MGF and feature table inputs from raw LC-MS/MS data) — http://mzmine.github.io
- **GNPS (Feature-Based Molecular Networking)** (Optional external workflow to generate MS/MS spectral library matches (--i-ms2-matches input)) — https://gnps.ucsd.edu/

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Output tree file (Phylogeny[Rooted] artifact) is non-empty and valid Newick format; can be exported and visualized in phylogenetic software
- Feature abundance in output FeatureTable[Frequency] matches input table except for features without CSI fingerprints (typically 70–90% retention reported in README)
- FeatureData[Molecules] contains non-null csi_smiles or ms2_smiles for every feature; parent_mass and retention_time fields are populated and within expected ranges for LC-MS/MS
- Tree contains expected structural relationships: features sharing molecular substructures (fingerprints) cluster together; validated against known chemical families in the experiment if reference standards available
- No errors in SIRIUS Java output; ppm mass error for matched molecular formulas remains below specified --p-ppm-max threshold (e.g., ≤15 ppm for Orbitrap)

## Limitations

- SIRIUS predicts molecular substructures for only a subset of MS1 features (typically 70–90%), determined by MS2 spectral quality, sample type, and ppm/zodiac-threshold tolerances; low-abundance or fragmentation-poor features are excluded
- Molecular formula ranking (ZODIAC) is probabilistic; --p-zodiac-threshold (default 0.95) filters candidates but may exclude true formulas in complex matrices
- Tree topology depends entirely on CSI:FingerID predictions and PubChem reference database (version 13 August 2017 in latest SIRIUS); novel or off-database compounds may be misclassified or grouped incorrectly
- Classyfire taxonomy classification (get-classyfire-taxonomy) prioritizes ms2_smiles over csi_smiles but requires internet connectivity to external Classyfire server; may fail if SMILES are malformed
- Meta-analyses require strict one-to-one correspondence between CSI results, feature tables, and (optionally) MS2 match tables; misalignment produces cryptic errors

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] q2-qemistree uses SIRIUS, a software-framework developed for de-novo identification of metabolites. We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset."
- [readme] An MGF file with both MS1 and MS2 information. This file will be imported into QIIME 2 as a MassSpectrometryFeatures artifact. A feature table with peak areas of MS1 ions per sample.: "An MGF file with both MS1 and MS2 information. This file will be imported into QIIME 2 as a `MassSpectrometryFeatures` artifact."
- [readme] This method generates the following: A combined feature table by merging all the input feature tables; MS1 features without fingerprints are filtered out of this feature table.: "MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1"
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type Phylogeny[Rooted].: "A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`."
- [readme] The input CSI results, feature tables and MS2 match tables should have a one-to-one correspondence i.e CSI results, feature tables and MS2 match tables from all datasets should be provided in the same order.: "The input CSI results, feature tables and MS2 match tables should have a one-to-one correspondence i.e CSI results, feature tables and MS2 match tables from all datasets should be provided in the"
- [readme] Qemistree will use ms2_smiles to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, csi_smiles will be used.: "Qemistree will use `ms2_smiles` to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, `csi_smiles` will be used."
- [readme] Note: Qemistree was initially developed under Sirius 4.0.1 version. Since Sirius 4.0.1 got to its end of life, Qemistree was recently adapted to work with the new Sirius versions (>4.4.29).: "Qemistree was recently adapted to work with the new Sirius versions (>4.4.29)."

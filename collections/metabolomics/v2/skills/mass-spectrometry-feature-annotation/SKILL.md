---
name: mass-spectrometry-feature-annotation
description: Use when when you have peak-detected LC-MS/MS data (MGF files with MS1 and MS2 spectra, plus a feature abundance table from MZmine2) and need to assign chemical structures and molecular properties to individual MS1 features rather than relying on mass-to-charge alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - q2-qemistree
  - SIRIUS
  - MZmine2
  - GNPS FBMN
  - Classyfire
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-annotation

## Summary

Annotate untargeted LC-MS/MS features with predicted molecular substructures and chemical taxonomy using fragmentation tree analysis, molecular formula ranking, and fingerprint prediction. This enables chemically-informed metabolomic profiling by assigning structural properties to detected mass-spectrometry features.

## When to use

When you have peak-detected LC-MS/MS data (MGF files with MS1 and MS2 spectra, plus a feature abundance table from MZmine2) and need to assign chemical structures and molecular properties to individual MS1 features rather than relying on mass-to-charge alone. Apply this when pursuing comparative or diversity-based metabolomic analysis that requires chemical context.

## When NOT to use

- Input MGF lacks MS2 spectra or does not pair each MS1 entry with corresponding MS2 fragmentation data.
- Feature table is already annotated with reliable structure identifications from targeted or reference-matched methods (fingerprint prediction adds computational cost for marginal benefit).
- Dataset contains only low-resolution MS or intact mass measurements without tandem MS/MS fragmentation data (SIRIUS requires MS2 for tree construction).

## Inputs

- MGF file (MS1 and MS2 spectra) imported as MassSpectrometryFeatures artifact
- Feature abundance table (BIOM format) imported as FeatureTable[Frequency]
- Optional: MS/MS spectral library matches as FeatureData[Molecules] (from GNPS FBMN workflow)

## Outputs

- Phylogeny[Rooted] tree relating MS1 features by predicted molecular substructures
- FeatureTable[Frequency] (merged, with features lacking fingerprints filtered out)
- FeatureData[Molecules] containing original IDs, parent mass, retention time, CSI:FingerID SMILES, MS2 SMILES, and source table assignments
- FeatureData[Molecules] with Classyfire chemical taxonomy annotations (optional)

## How to apply

Execute a five-step annotation pipeline: (1) compute fragmentation trees for all detected MS1 features using SIRIUS (set ppm-max typically to 15, profile to 'orbitrap' or your instrument type, and adduct ion type such as [M+H]+ based on ionization mode); (2) rerank candidate molecular formulas using ZODIAC with a confidence threshold (e.g., 0.95) to select the top-scoring formula per feature; (3) predict molecular fingerprints (2936 substructure properties) via CSI:FingerID from the ranked formulas (ppm-max typically 20); (4) construct a hierarchy tree from fingerprints using make-hierarchy, which also filters out features lacking fingerprint predictions (typically 70–90% of features succeed); (5) optionally classify tree nodes into Classyfire chemical taxonomy (kingdom, superclass, class, subclass, direct_parent) using CSI:FingerID SMILES predictions or MS/MS spectral library matches when available. Java heap size and temporary directory must be explicitly configured (e.g., -Xms16G -Xmx64G) for large datasets.

## Related tools

- **q2-qemistree** (Orchestrates fragmentation tree, molecular formula ranking, fingerprint prediction, hierarchy construction, and Classyfire taxonomy assignment for LC-MS/MS feature annotation) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (De-novo identification of molecular formulas from fragmentation trees and prediction of molecular substructures via CSI:FingerID) — https://bio.informatik.uni-jena.de/sirius/
- **MZmine2** (Upstream peak detection and feature extraction to produce MGF and feature table inputs) — http://mzmine.github.io
- **GNPS FBMN** (Optional external source for MS/MS spectral library matches to augment CSI:FingerID structure predictions) — https://gnps.ucsd.edu/ProteoSAFe/index.jsp?params=%7B%22workflow%22:%22FEATURE-BASED-MOLECULAR-NETWORKING%22,%22library_on_server%22:%22d.speclibs;%22%7D
- **Classyfire** (Chemical taxonomy classification of predicted molecular structures into kingdom, superclass, class, subclass, and direct_parent)

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Fragmentation trees are successfully generated for ≥70% of input MS1 features; features with poor-quality MS2 or no matching formula are reported.
- Molecular formulas are ranked and filtered; ZODIAC confidence threshold is met and top candidate formula per feature is selected.
- Fingerprints are predicted for ranked formulas; output contains 2936 (or 489 if --p-qc-properties is set) molecular properties per feature.
- Feature tree is rooted and in phylogenetic format (Newick); parent mass, retention time, and SMILES predictions are present in feature metadata.
- Classyfire annotations (when run) match expected chemical taxonomy depth (5 levels: kingdom through direct_parent); structure_source column correctly records CSI vs. MS2 origin of predictions.

## Limitations

- SIRIUS predicts fingerprints for only 70–90% of input features, depending on sample type, MS2 spectrum quality, and tolerance settings (ppm-max, zodiac-threshold); features without fingerprints are excluded from the final tree and feature table.
- Adduct type must be correctly specified (e.g., [M+H]+, [M+Na]+, [M-H]−) before SIRIUS run; mismatch leads to incorrect molecular formula ranking and invalid substructure predictions.
- CSI:FingerID predictions are probabilities of 2936 molecular substructures, not definitive structures; confidence and database version (PubChem dated 13 August 2017) should be consulted for validation.
- Classyfire taxonomy assignment uses online service; requires internet connectivity and may fail silently if remote server is unavailable.
- SIRIUS version compatibility: qemistree was adapted to work with SIRIUS ≥4.4.29 after initial development on 4.0.1; older versions may produce incompatible output.

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] q2-qemistree uses SIRIUS, a software-framework developed for de-novo identification of metabolites. We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "q2-qemistree uses SIRIUS, a software-framework developed for de-novo identification of metabolites. We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a"
- [readme] To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1. An MGF file with both MS1 and MS2 information. This file will be imported into QIIME 2 as a MassSpectrometryFeatures artifact. 2. A feature table with peak areas of MS1 ions per sample.: "An MGF file with both MS1 and MS2 information and a feature table with peak areas of MS1 ions per sample are required as inputs"
- [readme] This method generates the following: ... A combined feature data file that contains unique identifiers of each feature, their corresponding original feature identifier (row ID from Mzmine2), parent mass (parent_mass), retention time (retention_time), CSI:FingerID structure predictions (csi_smiles), MS2 match structure predictions (ms2_smiles), and the table(s) (table_number) that each feature was detected in.: "A combined feature data file containing unique identifiers, parent mass, retention time, CSI:FingerID structure predictions (csi_smiles), and MS2 match structure predictions (ms2_smiles)"
- [readme] SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment (based on factors such as sample type, the quality MS2 spectra, and user-defined tolerances such as --p-ppm-max, --p-zodiac-threshold).: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) based on sample type, MS2 spectra quality, and user-defined tolerances"
- [readme] Qemistree will use ms2_smiles to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, csi_smiles will be used. The column structure_source in classified-merged-feature-data.qza records whether taxonomic assignment was done using CSI:FingerID predictions or MS/MS library matches.: "Qemistree will use ms2_smiles for taxonomy assignments when available, otherwise csi_smiles; structure_source records the assignment method"
- [readme] Note: Qemistree was initially developed under Sirius 4.0.1 version. Since Sirius 4.0.1 got to its end of life, Qemistree was recently adapted to work with the new Sirius versions (>4.4.29).: "Qemistree was recently adapted to work with Sirius versions >4.4.29 after initial development on 4.0.1"

---
name: spectral-similarity-network-building
description: Use when when you have detected LC-MS/MS features (MS1 peaks with MS2 fragmentation spectra) from untargeted metabolomics experiments and seek to organize them into a chemical hierarchy for comparative metabolomic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - q2-qemistree
  - SIRIUS
  - CSI:FingerID
  - ZODIAC
  - MZmine2
  - GNPS FBMN
  - ClassyFire
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-network-building

## Summary

Build a tree of mass-spectrometry (LC-MS/MS) features by leveraging predicted molecular substructures and spectral similarity relationships to enable chemically-informed comparison of untargeted metabolomic profiles across samples.

## When to use

When you have detected LC-MS/MS features (MS1 peaks with MS2 fragmentation spectra) from untargeted metabolomics experiments and seek to organize them into a chemical hierarchy for comparative metabolomic analysis. Use this skill when you want to move beyond abundance-based feature tables and incorporate chemical structure information—either from CSI:FingerID predictions or MS/MS spectral library matches—to build a phylogenetically-oriented tree suitable for downstream alpha and beta diversity analyses.

## When NOT to use

- Input feature table already contains structural annotations and does not require de-novo molecular characterization.
- MS/MS spectra are absent or of poor quality (low intensity, few fragment ions), rendering fragmentation tree construction and fingerprint prediction unreliable.
- Analysis goal is purely abundance-based or phylogenetic (using 16S rRNA or whole-genome sequencing); chemical hierarchy is not needed.

## Inputs

- FeatureTable[Frequency] — peak areas of MS1 ions per sample (BIOM format, imported into QIIME 2)
- MassSpectrometryFeatures — MGF file with MS1 and MS2 spectra for all detected features
- SiriusFolder — fragmentation trees with candidate molecular formulas (output of compute-fragmentation-trees)
- CSIFolder — predicted molecular fingerprints (output of predict-fingerprints)
- FeatureData[Molecules] — optional MS/MS spectral library matches from GNPS FBMN

## Outputs

- Phylogeny[Rooted] — tree relating MS1 features based on predicted molecular substructure similarity
- FeatureTable[Frequency] — merged and filtered feature table (MS1 features without fingerprints removed)
- FeatureData[Molecules] — feature metadata including unique IDs, parent mass, retention time, CSI:FingerID SMILES, MS2 SMILES, and source table assignment

## How to apply

First, preprocess mass-spectrometry data (.mzXML, .mzML, .mzDATA) using MZmine2 to produce an MGF file containing both MS1 and MS2 spectra and a feature abundance table (CSV → BIOM format). Import these into QIIME 2 as MassSpectrometryFeatures and FeatureTable[Frequency] artifacts. Run q2-qemistree's compute-fragmentation-trees command via SIRIUS to generate fragmentation trees and candidate molecular formulas for each MS1 feature (specifying ppm-max, instrument profile, and adduct type); rerank formulas using ZODIAC (typically with threshold 0.95). Predict molecular fingerprints (2936 molecular properties by default, or 489 PubChem properties with --p-qc-properties) using CSI:FingerID. Finally, invoke make-hierarchy to construct the chemical feature tree, which clusters MS1 features based on Tanimoto similarity of their predicted (or library-matched) molecular substructures. Optionally include MS/MS spectral library matches (--i-ms2-matches) from GNPS FBMN to prioritize structure assignments. The resulting Phylogeny[Rooted] artifact relates features by chemical similarity, enabling phylogeny-aware diversity metrics.

## Related tools

- **q2-qemistree** (QIIME 2 plugin that orchestrates the entire chemical feature tree construction pipeline, including fragmentation tree computation, molecular formula ranking, fingerprint prediction, and hierarchy building.) — https://github.com/biocore/q2-qemistree
- **SIRIUS** (De novo metabolite identification framework used by q2-qemistree to compute fragmentation trees and predict molecular formulas and molecular substructures (fingerprints) via CSI:FingerID.) — https://bio.informatik.uni-jena.de/sirius/
- **CSI:FingerID** (Structure prediction algorithm bundled within SIRIUS; predicts 2936 molecular properties (fingerprints) for each MS1 feature to enable chemical similarity clustering.)
- **ZODIAC** (Molecular formula ranking method used by q2-qemistree (rerank-molecular-formulas command) to select top-scoring candidate molecular formulas before fingerprint prediction.)
- **MZmine2** (Upstream preprocessing tool for peak detection and feature extraction from raw LC-MS/MS data files (.mzXML, .mzML, .mzDATA); produces MGF and feature table inputs required by q2-qemistree.) — http://mzmine.github.io
- **GNPS FBMN** (Optional upstream workflow to generate MS/MS spectral library matches that can be incorporated into q2-qemistree via the --i-ms2-matches parameter for improved structure annotation.) — https://gnps.ucsd.edu/ProteoSAFe/index.jsp?params=%7B%22workflow%22:%22FEATURE-BASED-MOLECULAR-NETWORKING%22,%22library_on_server%22:%22d.speclibs;%22%7D
- **ClassyFire** (Optional post-processing step (get-classyfire-taxonomy command) to assign chemical taxonomy (kingdom, superclass, class, subclass, direct_parent) to features based on predicted or library-matched SMILES.)

## Examples

```
qiime qemistree make-hierarchy --i-csi-results fingerprints.qza --i-feature-tables feature-table.qza --o-tree qemistree.qza --o-feature-table feature-table-hashed.qza --o-feature-data feature-data.qza
```

## Evaluation signals

- Fragmentation tree construction completes without errors, with candidate molecular formulas assigned to ≥70–90% of MS1 features (expected coverage varies by sample type and MS2 spectrum quality).
- Fingerprint prediction produces CSIFolder artifact with Tanimoto-based molecular substructure similarity scores; verify that feature pairs with high chemical similarity (by structure) cluster together in the resulting tree.
- Final Phylogeny[Rooted] artifact is properly formatted and can be visualized in QIIME 2 and used as input to phylogenetic diversity metrics (alpha_phylogenetic, beta_phylogenetic).
- Output FeatureTable[Frequency] contains only features with predicted fingerprints; rows absent from CSI output are successfully filtered out with no orphaned features.
- FeatureData[Molecules] metadata correctly maps original MZmine2 feature IDs, parent masses, and retention times; CSI:FingerID and MS2 SMILES columns are populated according to structure availability and match priority (MS2 > CSI).

## Limitations

- SIRIUS predicts molecular substructures for only 70–90% of MS1 features, depending on sample type, MS/MS spectrum quality, and user-defined tolerances (ppm-max, zodiac-threshold). Features without predictions are filtered from the output tree and feature table.
- The pipeline requires careful tuning of parameters (ppm-max typically 15–20, zodiac-threshold typically 0.95, ions-considered for adducts) and substantial computational resources (recommended Java heap size -Xms16G -Xmx64G); incorrect settings can degrade molecular formula and fingerprint accuracy.
- PubChem fingerprint database used by SIRIUS was downloaded on 13 August 2017; newer chemical structures may not be fully represented.
- Fragmentation tree construction is computationally intensive and requires a local installation of SIRIUS binary; network-based approaches are not supported.
- MS/MS spectral library matches from GNPS FBMN are optional but, when provided, must have one-to-one correspondence with input CSI results and feature tables; mismatches can lead to incomplete or incorrect structure assignment.
- Tree construction is deterministic given molecular fingerprints but is sensitive to errors in MS1 parent mass accuracy and MS/MS fragmentation pattern quality.

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1. An MGF file with both MS1 and MS2 information. 2. A feature table with peak areas of MS1 ions per sample.: "To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce an MGF file with both MS1"
- [readme] We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset."
- [readme] This method generates the following: 1. A combined feature table by merging all the input feature tables; MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment.: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment."
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type Phylogeny[Rooted].: "A tree relating the MS1 features based on molecular substructures predicted for MS1 features. This is of type Phylogeny[Rooted]."
- [readme] These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses.: "These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses."
- [readme] Qemistree will use ms2_smiles to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, csi_smiles will be used.: "Qemistree will use ms2_smiles to make chemical taxonomy assignments, when MS2 matches are available for a feature. Otherwise, csi_smiles will be used."

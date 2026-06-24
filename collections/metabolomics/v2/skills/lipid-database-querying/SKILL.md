---
name: lipid-database-querying
description: Use when you have acquired full-scan mass spectrometry imaging data (e.g.,
  from a mouse bladder or tissue section) with detected m/z features and want to assign
  chemical identities to those features by querying a structured lipid database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3814
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpaMTP
  - R
  - Seurat
  - Cardinal
  - Lipidmaps_db
  - RefineLipids
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-database-querying

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match observed mass-to-charge ratios (m/z) from spatial metabolomics datasets against curated lipid structural databases (e.g., LipidMaps) using mass accuracy tolerance and adduct type constraints. This skill enables systematic identification of lipid species in untargeted MS imaging experiments.

## When to use

You have acquired full-scan mass spectrometry imaging data (e.g., from a mouse bladder or tissue section) with detected m/z features and want to assign chemical identities to those features by querying a structured lipid database. Specifically, use this skill when you know the expected adduct form (e.g., M+K for positive ion mode) and can specify a mass error tolerance (ppm) appropriate to your instrument's accuracy.

## When NOT to use

- Input dataset contains only pre-annotated metabolite names or already-resolved chemical identities (annotation step is redundant).
- Mass spectrometry data were acquired in low-resolution mode (e.g., Orbitrap resolution <30k) or instrument calibration is poor (ppm error >50), making unambiguous matching to a curated database unreliable.
- You are working with non-lipid metabolite classes (e.g., carbohydrates, amino acids, nucleotides); use a broader metabolite database (e.g., HMDB) instead, or a database specific to your metabolite class.

## Inputs

- SpaMTP Seurat object with m/z features in assay
- Lipid structure database (e.g., Lipidmaps_db)
- Mass accuracy specification (ppm_error, typically 5–20)
- Adduct type string (e.g., 'M+K', 'M+H', 'M+Na')
- Ionization polarity ('positive' or 'negative')

## Outputs

- SpaMTP Seurat object with annotations in feature metadata (m/z, metabolite name, lipid class, structure)
- Summary table of matched m/z values and corresponding LipidMaps annotations
- Count of successfully annotated features

## How to apply

Load your spatial metabolomics dataset as a SpaMTP Seurat object, then invoke the AnnotateSM function with parameters: db (e.g., Lipidmaps_db), ppm_error (typically 15 for high-resolution MS), adducts (e.g., 'M+K'), and polarity ('positive' or 'negative'). The function performs a mass-difference search, matching each observed m/z against the database, accounting for the specified adduct mass offset and mass tolerance window. Extracted annotations (chemical name, class, structure) are stored in the feature metadata slot of the returned SpaMTP object. Optionally, apply RefineLipids to simplify lipid nomenclature into common categories for downstream interpretation.

## Related tools

- **SpaMTP** (R package that wraps AnnotateSM function for m/z annotation against lipid databases and stores results in Seurat object structure) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Provides the S4 object class (Seurat) used by SpaMTP to store m/z features, metadata, and annotations)
- **Cardinal** (Mass spectrometry imaging data import and preprocessing; SpaMTP inherits MSImageSet capabilities for raw m/z feature extraction) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **Lipidmaps_db** (Curated lipid structure and mass database queried by AnnotateSM to resolve m/z to chemical identity)
- **RefineLipids** (Post-annotation function to simplify complex lipid nomenclature into common lipid categories and classes for interpretation) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = 'M+K', polarity = 'positive')
```

## Evaluation signals

- Verify that the returned SpaMTP object contains non-empty feature metadata columns for metabolite name, lipid class, and structure; count of annotated features > 0.
- Cross-check a subset of high-confidence annotations (e.g., m/z mass difference ≤ ppm_error threshold) against external lipid databases or reference spectra to confirm chemical plausibility.
- Examine the distribution of assigned lipid classes and m/z values to ensure consistency with expected tissue/sample lipidome (e.g., phosphatidylcholines and fatty acids dominant in bladder tissue).
- Confirm that all matched m/z values fall within the specified ppm_error window when the adduct mass is subtracted from the database lipid mass.
- Verify that annotations are reproducible: re-running AnnotateSM with identical parameters and the same database version produces identical results.

## Limitations

- Annotation accuracy depends on the completeness and correctness of the reference database; lipid structures missing from LipidMaps will not be detected.
- High ppm_error tolerance (e.g., >20 ppm) increases false positive matches, especially in crowded m/z regions; low tolerance may miss genuine lipids if instrument calibration drifts.
- Isotopologs and in-source fragments may be misassigned if they happen to match database entries at the specified ppm_error; downstream filtering or confirmation (e.g., MS/MS) is advisable.
- The article notes that 'Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data' sections are marked 'To come!', indicating that orthogonal validation workflows are not yet integrated.
- Requires a priori knowledge of the expected adduct type (e.g., M+K vs. M+H); incorrect adduct specification leads to systematic mass offset and missed or mismatched annotations.

## Evidence

- [other] How many m/z masses from the mouse urinary bladder dataset can be successfully annotated when using AnnotateSM with the LipidMaps database, ppm=15, and M+K positive adduct?: "AnnotateSM with the LipidMaps database, ppm=15, and M+K positive adduct"
- [other] Run AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive'.: "Run AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive'"
- [other] Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot.: "Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot"
- [other] Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db.: "Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db"
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis... mass-to-charge ratio (m/z) metabolite annotation: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat)... mass-to-charge ratio (m/z) metabolite annotation"
- [methods] Runs lipid nomenclature simplification on annotations... RefineLipids(spotted@assays$[redacted-email]: "Runs lipid nomenclature simplification on annotations... RefineLipids"

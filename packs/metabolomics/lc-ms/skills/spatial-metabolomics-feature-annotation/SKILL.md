---
name: spatial-metabolomics-feature-annotation
description: Use when your spatial metabolomics dataset contains raw m/z features (e.g., from MALDI-MS imaging or LC-MS/MS) without metabolite annotations, and you have selected a reference database and adduct type appropriate for your ionization mode and biological sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3755
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - SpaMTP
  - R
  - Seurat
  - Cardinal
  techniques:
  - LC-MS
  - MS-imaging
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spatial Metabolomics Feature Annotation

## Summary

Assign metabolite identities to mass-to-charge (m/z) features in spatial metabolomics datasets by matching observed m/z values against a reference database (e.g., LipidMaps, HMDB) within a specified mass error tolerance and adduct assumption. This skill enables interpretation of spatial MS imaging data by linking ion signals to known chemical structures.

## When to use

Your spatial metabolomics dataset contains raw m/z features (e.g., from MALDI-MS imaging or LC-MS/MS) without metabolite annotations, and you have selected a reference database and adduct type appropriate for your ionization mode and biological sample. Apply this skill when you need to convert m/z-only feature matrices into interpretable metabolite annotations for downstream statistical analysis, visualization, or pathway inference.

## When NOT to use

- Your reference database is incomplete or poorly curated for your sample type (e.g., plant metabolites when only animal lipids are in the database).
- You have not validated mass calibration on your MS instrument; systematic calibration drift will cause ppm-based matches to fail.
- You are working with small-molecule metabolites but only have lipid-focused databases available.

## Inputs

- SpaMTP Seurat object with spatial metabolomics intensity matrix
- Reference metabolite database (LipidMaps_db or HMDB_db in RDS format)
- m/z feature list from spatial MS imaging experiment
- Mass calibration and ionization polarity metadata

## Outputs

- Annotated SpaMTP Seurat object with metabolite identities in feature metadata
- Annotation summary table (m/z, metabolite name, chemical formula, adduct type)
- Count and proportion of successfully annotated features
- ppm error distribution for matched annotations

## How to apply

Load your spatial metabolomics dataset (e.g., as a SpaMTP Seurat object from a CSV intensity matrix) and invoke the AnnotateSM function with three key parameters: the reference database (db = Lipidmaps_db or HMDB_db), the mass error tolerance in parts per million (ppm_error, typically 15 ppm for high-resolution MS), and the expected adduct type (adducts = 'M+K' for positive potassium adducts, or 'M+H' for protons). The function matches each observed m/z to the nearest database entry within the specified ppm window, returning a Seurat object with annotations stored in the feature metadata slot. Verify success by extracting the count of successfully annotated features and inspecting a summary table of m/z values and their corresponding metabolite identities; low annotation rates may indicate insufficient database coverage, incorrect adduct selection, or mass calibration issues.

## Related tools

- **SpaMTP** (R package providing AnnotateSM function for m/z-to-metabolite matching in spatial metabolomics Seurat objects) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Data container class (Seurat object) that stores intensity matrix, feature metadata, and annotation results)
- **Cardinal** (Underlying spatial mass spectrometry analysis framework inherited by SpaMTP for m/z feature handling) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **R** (Execution environment for AnnotateSM function calls and downstream metadata manipulation)

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = "M+K", polarity = "positive")
```

## Evaluation signals

- Non-zero count of annotated features; typical thresholds depend on database coverage but >50% annotation success is expected for well-matched lipidomes.
- ppm error distribution is centered near zero and falls within specified tolerance window (e.g., 68–95% of matches within ±7.5 ppm for ppm_error=15).
- Annotated metabolites match known composition of the biological sample (e.g., lipid classes appropriate to bladder urine, liver tissue).
- Feature metadata slot contains non-NA metabolite names, chemical formulas, and adduct annotations for all matched m/z values.
- Reproducibility check: re-running AnnotateSM on the same object with identical parameters yields identical annotation results.

## Limitations

- Annotation accuracy depends critically on reference database completeness and curation; underrepresented metabolite classes will show low match rates.
- Assumes a single dominant adduct per m/z feature; multiply charged or mixed-adduct ions may be misannotated or missed.
- ppm error tolerance is fixed globally across all m/z features; low m/z values and high m/z values have different absolute mass error ranges, which may cause over- or under-matching.
- No built-in filtering for biological plausibility; chemically valid matches that are absent in the sample will still be reported.
- The article indicates two planned refinement methods—'Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data'—are marked 'To come!', implying current annotation lacks MS/MS confirmation and cannot yet be validated against targeted metabolomics.

## Evidence

- [methods] Run AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive': "Run AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive'"
- [methods] Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot: "Extract the count of successfully annotated m/z features from the returned SpaMTP object and verify that annotations are stored in the feature metadata slot"
- [methods] Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db: "Generate a summary table showing the m/z values and their corresponding metabolite annotations from the Lipidmaps_db"
- [readme] m/z metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression and pathway analysis: "(1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis"
- [methods] ## 3) Pseudo MS/MS-Based Refinement

To come!
  - Refinement with Paired Targeted Metabolic Data section marked as 'To come!': "## 3) Pseudo MS/MS-Based Refinement

To come!"

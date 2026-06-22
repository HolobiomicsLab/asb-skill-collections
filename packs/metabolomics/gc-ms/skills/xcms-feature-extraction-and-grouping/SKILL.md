---
name: xcms-feature-extraction-and-grouping
description: Use when you have raw mzXML LC/MS files from replicated metabolomics experiments (e.g., 12 samples across labeled/unlabeled conditions) and need to extract, align, and group peaks before downstream feature filtering (e.g., fold-change or isotope enrichment analysis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - geoRge
  - R
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.5b03628
  title: geoRge
evidence_spans:
- library(geoRge)
- hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
- This is an R Markdown document
- Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
  dedup_kept_from: coll_george_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5b03628
  all_source_dois:
  - 10.1021/acs.analchem.5b03628
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xcms-feature-extraction-and-grouping

## Summary

Peak picking, alignment, and grouping of LC/MS data using the XCMS package to generate a feature matrix suitable for stable isotope labeling detection. This is a prerequisite preprocessing step that transforms raw mzXML files into an XCMSet object with aligned, grouped features across sample replicates.

## When to use

You have raw mzXML LC/MS files from replicated metabolomics experiments (e.g., 12 samples across labeled/unlabeled conditions) and need to extract, align, and group peaks before downstream feature filtering (e.g., fold-change or isotope enrichment analysis). Apply this when starting with vendor instrument output or when you need reproducible, unified feature detection across a cohort.

## When NOT to use

- Input is already a processed feature table (e.g., CSV with m/z, RT, intensity columns); XCMS is redundant.
- Data is not from LC/MS or is in a non-standard format (e.g., GC/MS, NMR); XCMS is LC/MS-specific.
- Peaks have already been manually or externally picked and grouped; XCMS is for automated discovery, not validation of pre-existing peak sets.

## Inputs

- mzXML files (raw LC/MS data from instrument vendor or converted)
- Sample metadata or annotations (e.g., replicate count, condition labels)

## Outputs

- XCMSet object (R S4 class containing peak picking, alignment, and grouping results)
- Feature matrix (m/z, retention time, intensity per feature per sample)

## How to apply

Load raw mzXML files into XCMS via the xcms package in R. Execute peak picking to detect individual features in each sample, alignment to correct for retention time drift across replicates, and grouping to aggregate detected peaks into unified features across the sample set. The output is an XCMSet object containing a feature matrix with m/z, retention time, and intensity values for each feature in each sample. This preprocessed XCMSet becomes the input for downstream tools like geoRge's PuInc_seeker function. XCMS parameters (e.g., ppm tolerance, minimum peak width) should be tuned to your instrument's resolution and mass accuracy; defaults are conservative starting points.

## Related tools

- **XCMS** (Peak picking, retention time alignment, and feature grouping for LC/MS preprocessing) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Scripting environment for executing XCMS workflows)

## Examples

```
library(xcms); xcms_obj <- xcmsSet(files=dir(pattern='mzXML$'), method='centWave'); xcms_aligned <- group(xcms_obj); xcms_grouped <- retcor(xcms_aligned, method='obiwarp')
```

## Evaluation signals

- XCMSet object is successfully created with no NA or empty feature matrices; inspect nrow(featureDefinitions(XCMSet)) to confirm features are detected.
- Feature retention times are consistent across replicates within expected tolerance (e.g., ±0.5 min for typical LC/MS); verify via boxplot of RT per feature.
- Feature intensities are non-negative and follow expected distribution (e.g., log-normal); check mean/median intensity ratios between replicate groups.
- Number of grouped features is comparable to prior literature on the same organism/matrix or known metabolite count; unexpectedly low counts suggest alignment or grouping failure.
- Downstream isotope enrichment detection (e.g., geoRge PuInc_seeker) recovers expected labeled/unlabeled fold-changes; if fold-changes are near 1.0 across all features, grouping may have over-collapsed features.

## Limitations

- XCMS performance and parameter sensitivity depend heavily on instrument mass accuracy (ppm), peak width, and alignment drift; suboptimal parameters can lead to missed or spurious features.
- Large sample cohorts (>100 samples) or high data density can increase runtime and memory requirements; computational scaling is not addressed in the article.
- Retention time drift correction assumes systematic, continuous drift; abrupt instrument recalibration or batch effects may not be fully corrected and could inflate feature count.
- No changelog documentation is available for the geoRge package version referenced, limiting reproducibility across software updates.

## Evidence

- [methods] Use XCMS for peak picking, alignment, and grouping is prerequisite: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"
- [intro] XCMSet is input to downstream isotope detection: "s1 <- PuInc_seeker(XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13", sep.pos.front=TRUE ,fc.threshold=1.5,p.value.threshold=.05,PuInc.int.lim = 4000)"
- [methods] geoRge workflow depends on XCMS preprocessing: "This is an R Markdown document"

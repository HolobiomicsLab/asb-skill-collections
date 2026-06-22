---
name: metabolite-fold-change-statistical-testing
description: Use when you have XCMS-processed LC/MS peak data from dual-labeled (e.g., 13C) and unlabeled (12C) metabolomics samples and need to distinguish features genuinely enriched by stable isotope incorporation from noise or background variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - geoRge
  - R
  - XCMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5b03628
  title: geoRge
evidence_spans:
- library(geoRge)
- hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
- This is an R Markdown document
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-fold-change-statistical-testing

## Summary

Identify metabolic features with statistically significant abundance differences between stable isotope-labeled and unlabeled conditions by applying fold-change and p-value thresholds to XCMS-processed LC/MS feature matrices. This skill filters putatively incorporated metabolites in untargeted metabolomics experiments.

## When to use

Apply this skill when you have XCMS-processed LC/MS peak data from dual-labeled (e.g., 13C) and unlabeled (12C) metabolomics samples and need to distinguish features genuinely enriched by stable isotope incorporation from noise or background variation. Use it after peak picking, alignment, and grouping but before metabolite annotation.

## When NOT to use

- Input is already a curated list of known metabolites or a database match table — use this skill on raw feature-level data, not on annotated identities.
- Samples do not have replicate structure or lack distinct labeled/unlabeled group assignments — the skill requires well-defined sample classes and adequate replication for p-value computation.
- Peak picking, alignment, and grouping have not been completed — XCMS preprocessing is mandatory; this skill assumes a valid feature-by-sample intensity matrix.

## Inputs

- XCMS object (XCMSet) with peak-picked, aligned, and grouped LC/MS features from dual-condition experiment
- Sample class annotations mapping replicates to unlabeled and labeled treatment tags
- Feature abundance matrix (intensity values per feature per sample)

## Outputs

- Filtered feature list with fold-change and p-value statistics
- Binary classification of features as putatively incorporated or not
- Numeric vector or table of features passing all three thresholds

## How to apply

Load an XCMS object and invoke the geoRge PuInc_seeker function with sample class tags distinguishing unlabeled (e.g., CELL_Glc12) from labeled (e.g., CELL_Glc13) replicates. Specify three filtering thresholds: a fold-change cutoff (default 1.5, comparing labeled to unlabeled abundance), a p-value threshold (default 0.05 from statistical test), and a putative incorporation intensity limit (default 4000, minimum feature intensity in labeled samples). The function computes fold-change ratios and p-values for each feature across the two groups, retaining only features that meet all three criteria simultaneously. The rationale is that true isotope-labeled incorporations exhibit both statistical significance and meaningful abundance elevation, while filtering by minimum intensity reduces spurious weak signals.

## Related tools

- **geoRge** (Primary framework providing PuInc_seeker function for fold-change and p-value filtering of isotope-labeled features) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Upstream peak picking, alignment, and grouping to generate the feature matrix input to PuInc_seeker) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Execution environment for geoRge library and PuInc_seeker function calls)

## Examples

```
s1 <- PuInc_seeker(XCMSet=mtbls213, ULtag="CELL_Glc12", Ltag="CELL_Glc13", sep.pos.front=TRUE, fc.threshold=1.5, p.value.threshold=.05, PuInc.int.lim=4000)
```

## Evaluation signals

- Output feature count is lower than input feature count, confirming filtering occurred.
- All retained features have fold-change ≥ 1.5 (or user-specified threshold) and p-value ≤ 0.05 (or threshold).
- Retained features have mean or median intensity in labeled samples ≥ 4000 (or specified PuInc.int.lim), confirming intensity filter applied.
- Fold-change values and p-values are present for all output features; no NA or missing values in filtering statistics.
- Reproducibility check: re-running PuInc_seeker with identical parameters and same XCMS input yields identical feature list and statistics.

## Limitations

- Threshold values (fold-change 1.5, p-value 0.05, intensity 4000) are dataset- and instrument-specific; no universal defaults are provided in the literature. Thresholds must be validated or justified per experiment.
- Statistical power depends on replicate number; fewer replicates reduce ability to detect true incorporations and increase false negatives.
- Assumes normally distributed or approximately normal feature abundances; extreme skew or outliers may violate p-value calculation assumptions.
- Does not account for multiple-hypothesis correction (e.g., Bonferroni, FDR) across the feature set; reported p-values are unadjusted, risking false positives when filtering many features.

## Evidence

- [intro] Describes the core filtering logic and thresholds.: "PuInc_seeker operates by taking an XCMS-processed set, specifying unlabeled (CELL_Glc12) and labeled (CELL_Glc13) sample tags, and applying three filtering thresholds: a fold-change threshold of 1.5,"
- [intro] Specifies the concrete workflow steps and parameter usage.: "s1 <- PuInc_seeker(XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13", sep.pos.front=TRUE ,fc.threshold=1.5,p.value.threshold=.05,PuInc.int.lim = 4000)"
- [methods] Confirms XCMS preprocessing requirement and the dual-condition experimental design.: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"
- [other] Describes the sample annotation strategy for distinguishing labeled and unlabeled groups.: "Set sample class annotations to distinguish CELL_Glc12_05mM_Normo (unlabelled, 6 replicates) from CELL_Glc13_05mM_Normo (labelled, 6 replicates)."
- [readme] Confirms the software framework and installation method for reproducibility.: "install.packages("devtools", dependencies=TRUE)
library(devtools)
install_github("jcapelladesto/geoRge")
library(geoRge)"

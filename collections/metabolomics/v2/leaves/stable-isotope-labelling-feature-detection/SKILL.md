---
name: stable-isotope-labelling-feature-detection
description: Use when you have XCMS-processed LC/MS peak tables from paired unlabeled
  (12C) and labeled (13C) metabolic samples with replicate measurements, and you want
  to systematically detect which features show significant enrichment in the labeled
  condition relative to the unlabeled control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - geoRge
  - R
  - XCMS
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# stable-isotope-labelling-feature-detection

## Summary

Identify metabolic features that have incorporated stable isotope labels (e.g., 13C) by comparing fold-change and statistical significance between labeled and unlabeled LC/MS sample groups. This skill detects putative isotope incorporations in untargeted metabolomics using the geoRge PuInc_seeker function on XCMS-preprocessed peak data.

## When to use

Apply this skill when you have XCMS-processed LC/MS peak tables from paired unlabeled (12C) and labeled (13C) metabolic samples with replicate measurements, and you want to systematically detect which features show significant enrichment in the labeled condition relative to the unlabeled control. Use this before isotopologue base-peak assignment or metabolite identification.

## When NOT to use

- Input is already a curated metabolite identity table or library spectrum matches — use this skill on raw peak tables from XCMS grouping, not on annotated results.
- Your experiment has only single replicates per condition or <3 replicates per group — statistical comparison requires adequate degrees of freedom.
- You lack paired unlabeled and labeled sample cohorts — the skill requires both conditions to compute fold-change and significance.

## Inputs

- XCMS processed peak set (XCMSet object in R)
- Sample class annotations distinguishing unlabeled and labeled condition tags
- Replicate LC/MS measurements (typically ≥6 replicates per condition)

## Outputs

- geoRge PuInc_seeker result object with ranked putative incorporations
- Feature m/z, retention time, fold-change, p-value, and intensity annotations
- Sample-tag and position-matching metadata for downstream basepeak_finder use

## How to apply

Load your XCMS object and geoRge library in R, then annotate sample class labels to distinguish unlabeled (e.g., CELL_Glc12) from labeled (e.g., CELL_Glc13) groups. Execute PuInc_seeker with three key filtering thresholds: fold-change threshold (typically 1.5), p-value threshold (typically 0.05), and putative incorporation intensity minimum (typically 4000) to filter features showing statistically significant abundance differences between groups. The function compares mean intensities between labeled and unlabeled sample sets, ranks by fold-change and p-value, and outputs enriched features tagged with isotope-incorporation metadata. Rationale: these thresholds balance signal detection against false-positive incorporations from noise or natural isotope variation; the intensity limit removes low-signal artifacts.

## Related tools

- **geoRge** (Primary R package implementing PuInc_seeker function for isotope-incorporation detection) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Upstream peak picking, alignment, and grouping to generate input XCMSet object) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Runtime environment for geoRge functions and statistical comparisons)

## Examples

```
s1 <- PuInc_seeker(XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13",sep.pos.front=TRUE,fc.threshold=1.5,p.value.threshold=.05,PuInc.int.lim=4000)
```

## Evaluation signals

- Output object contains features with non-null fold-change values and p-values ≤ specified threshold (e.g., 0.05) for all returned features.
- Mean intensity of labeled-group features is ≥ fold-change threshold (e.g., 1.5×) above unlabeled-group mean for each returned feature.
- Putative incorporation intensities all exceed the specified minimum (e.g., 4000); no features below threshold are retained.
- Feature count and ranking order remain consistent across re-runs with identical parameters and input XCMSet.
- Returned features include proper sample-tag annotations (ULtag/Ltag) and position metadata compatible with downstream basepeak_finder input.

## Limitations

- Performance depends critically on upstream XCMS peak picking, alignment, and grouping quality; poor alignment or mis-grouping will propagate false incorporations.
- Fold-change and p-value thresholds are user-specified and require domain knowledge or pilot data to justify; no data-driven automatic threshold selection is provided.
- The skill detects abundance enrichment but cannot distinguish genuine isotope incorporation from confounding factors (e.g., ion suppression, adduct variation, or natural 13C presence in controls).
- Statistical power is limited by replicate count; experiments with <6 replicates per condition may have high false-discovery rates at typical p-value thresholds.
- No changelog documented in the repository, limiting version-specific reproducibility.

## Evidence

- [intro] PuInc_seeker with fold-change and p-value thresholds for putative incorporation detection: "s1 <- PuInc_seeker(XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13", sep.pos.front=TRUE ,fc.threshold=1.5,p.value.threshold=.05,PuInc.int.lim = 4000)"
- [methods] Sample annotation and tag-based comparison logic: "Set sample class annotations to distinguish CELL_Glc12_05mM_Normo (unlabelled, 6 replicates) from CELL_Glc13_05mM_Normo (labelled, 6 replicates)"
- [intro] Fold-change, p-value, and intensity filtering thresholds used in geoRge: "PuInc_seeker operates by taking an XCMS-processed set, specifying unlabeled (CELL_Glc12) and labeled (CELL_Glc13) sample tags, and applying three filtering thresholds: a fold-change threshold of 1.5,"
- [methods] XCMS upstream preprocessing requirement: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"
- [intro] Output compatibility with basepeak_finder for isotopologue linkage: "basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds  [section=intro; evidence='s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213,"

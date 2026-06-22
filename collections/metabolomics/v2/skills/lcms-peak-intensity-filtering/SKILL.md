---
name: lcms-peak-intensity-filtering
description: Use when after XCMS peak picking, alignment, and grouping when you have identified putative incorporations (via PuInc_seeker) or base-peak isotopologue candidates and need to exclude low-intensity peaks that are likely noise or instrument artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - geoRge
  - R
  - XCMS
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

# lcms-peak-intensity-filtering

## Summary

Filter LC/MS-detected peaks by minimum intensity threshold to enrich signal-to-noise ratio and reduce false positives in stable isotope labelling detection workflows. This skill applies absolute intensity cutoffs to putative incorporations and base-peak isotopologue candidates downstream of peak picking and alignment.

## When to use

Apply this skill after XCMS peak picking, alignment, and grouping when you have identified putative incorporations (via PuInc_seeker) or base-peak isotopologue candidates and need to exclude low-intensity peaks that are likely noise or instrument artifacts. Use it when your LC/MS dataset exhibits variable background signal and you want to focus on metabolites with robust signal strength relative to your instrument's detection limit.

## When NOT to use

- Input is already a curated metabolite reference database or in silico spectral library (peaks are not from your experimental LC/MS run)
- You are performing untargeted discovery on samples with extremely low metabolite abundance where even weak peaks may represent true biology
- Intensity values are already normalized (e.g., by total ion current or internal standard) and do not reflect absolute detector signal

## Inputs

- XCMS feature table (XCMSet object) after peak picking, alignment, and grouping
- PuInc_seeker output object (putative incorporations with fold-change and p-value annotations)
- m/z values, retention times, and intensity measurements from aligned LC/MS runs

## Outputs

- Filtered PuInc_seeker result object with low-intensity putative incorporations excluded
- basepeak_finder result object (geoRge object) containing base-peak isotopologue pairs meeting intensity thresholds
- Subset of features with m/z, intensity, and isotope-pair annotations above threshold

## How to apply

Establish two intensity thresholds tuned to your LC/MS platform and sample preparation: (1) a putative incorporation intensity limit (e.g., 4000 counts) applied during PuInc_seeker to filter candidate labeled/unlabeled isotopologues, and (2) a base-peak minimum intensity threshold (e.g., 2000 counts) applied during basepeak_finder to validate that identified base peaks meet minimum signal abundance. Both thresholds should be derived from your instrument's noise floor and blank samples; set them conservatively to retain true metabolite signal while eliminating instrumental noise. The rationale is that low-intensity peaks are prone to mass accuracy drift and unstable isotope-pair detection, making them unreliable for downstream identification and quantification.

## Related tools

- **geoRge** (Container package providing PuInc_seeker and basepeak_finder functions that apply intensity filtering as integral workflow steps) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Upstream peak picking, alignment, and grouping to generate the feature table on which intensity filtering is applied) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Execution environment for geoRge intensity filtering functions)

## Examples

```
s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- Filtered output contains no peaks with intensity below the specified threshold (e.g., no base peaks < 2000 counts)
- Number of retained features is reduced by a reasonable proportion (typically 30–60%) relative to unfiltered input, indicating effective noise suppression without over-filtering
- Retained base-peak isotopologue pairs maintain consistent mass accuracy (within 6.5 ppm tolerance) and intensity ratios expected for labeled/unlabeled carbon-13 pairs
- Downstream database_query hits and metabolite identifications show improved specificity (fewer false positives) compared to unfiltered runs
- m/z and intensity distributions of filtered peaks align with expected metabolite mass ranges and instrument sensitivity

## Limitations

- Intensity thresholds are dataset and instrument-specific; thresholds derived from mtbls213 may not transfer to different LC/MS platforms, ionization modes, or sample matrices without reoptimization
- Filtering by absolute intensity assumes uniform detector response across m/z range; non-linear or m/z-dependent sensitivity bias may cause systematic loss of low-abundance metabolites in certain mass windows
- Threshold selection requires prior knowledge of noise floor; if blank/negative control intensities are not characterized beforehand, threshold setting may be arbitrary or too stringent/permissive
- geoRge 1.0 reduced function arguments for usability; verify that your version's default or user-specified intensity parameters match your experimental design

## Evidence

- [intro] basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds: "basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds"
- [methods] unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000: "unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000"
- [intro] Base peak minimum intensity of 2000: "Base peak minimum intensity of 2000"
- [intro] Putative incorporation intensity limit of 4000: "Putative incorporation intensity limit of 4000"
- [methods] s2 <- basepeak_finder(PuIncR=s1,XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13",sep.pos="f",UL.atomM=12.0,L.atomM=13.003355,ppm.s=6.5,Basepeak.minInt=2000): "s2 <- basepeak_finder(PuIncR=s1,XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13",sep.pos="f",UL.atomM=12.0,L.atomM=13.003355,ppm.s=6.5,Basepeak.minInt=2000)"
- [readme] Same functions, less arguments. I have updated the functions so they are less tiring to use.: "Same functions, less arguments. I have updated the functions so they are less tiring to use."

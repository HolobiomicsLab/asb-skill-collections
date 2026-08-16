---
name: isotopologue-grouping-by-mass-accuracy
description: Use when after PuInc_seeker has identified putative incorporations in a stable-isotope-labeled LC/MS dataset (e.g., CELL_Glc12 unlabeled vs. CELL_Glc13 labeled samples).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopologue-grouping-by-mass-accuracy

## Summary

Identify base-peak isotopologue groupings from putative stable-isotope incorporations by matching m/z pairs within specified mass accuracy tolerance and intensity thresholds. This skill links enriched features to their unlabeled and labeled isotope counterparts in LC/MS untargeted metabolomics.

## When to use

Apply this skill after PuInc_seeker has identified putative incorporations in a stable-isotope-labeled LC/MS dataset (e.g., CELL_Glc12 unlabeled vs. CELL_Glc13 labeled samples). Use it when you need to resolve base-peak isotopologue pairs from feature clusters, accounting for instrumental mass accuracy limits and signal intensity.

## When NOT to use

- Input has not been processed through PuInc_seeker; basepeak_finder requires putative incorporation annotations as input.
- XCMS peak picking, alignment, and grouping have not been completed; the XCMSet must be a fully processed feature matrix.
- Mass accuracy of the instrument is >6.5 ppm or unknown; the 6.5 ppm threshold is specific to the mtbls213 dataset and may require recalibration for other instruments or datasets.

## Inputs

- PuInc_seeker output (putative incorporation result object)
- XCMS peak group object (XCMSet)
- sample class labels (ULtag for unlabeled, Ltag for labeled)

## Outputs

- geoRge object with identified base-peak isotopologue groupings
- m/z-intensity pairs annotated with isotope assignment and sample origin

## How to apply

Execute the basepeak_finder function on PuInc_seeker output, specifying unlabeled atom mass (12.0 for carbon-12), labeled atom mass (13.003355 for carbon-13), mass accuracy tolerance (6.5 ppm for the mtbls213 dataset), and base-peak minimum intensity threshold (2000). The function matches m/z values between the two sample groups (ULtag and Ltag) using front-position logic to group isotopologue pairs. The algorithm filters out low-intensity noise and resolves ambiguous mass assignments by enforcing the ppm tolerance window. Validate output by confirming the geoRge object contains isotope-pair annotations with m/z, intensity, and sample-group tags intact.

## Related tools

- **geoRge** (Host R package providing basepeak_finder and related isotope-detection functions) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Prerequisite peak picking, alignment, and grouping to produce the XCMSet input) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Execution environment for basepeak_finder function)

## Examples

```
s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- Output geoRge object contains non-empty isotope-pair annotations with both m/z and intensity fields populated.
- All paired isotopologues fall within the specified mass accuracy tolerance (6.5 ppm) for the labeled–unlabeled mass difference.
- Base-peak intensities in the output are ≥2000, confirming the minimum intensity threshold was applied.
- Sample group tags (ULtag, Ltag) are correctly assigned to paired features, with no cross-contamination.
- Number of identified base peaks is consistent with the putative incorporation count from PuInc_seeker, accounting for p-value and fold-change filtering.

## Limitations

- Mass accuracy tolerance (6.5 ppm) is calibrated to the mtbls213 dataset; different instruments or chromatographic conditions may require recalibration.
- Minimum intensity threshold (2000) is dataset-specific and may suppress weak labeling signals in low-abundance metabolites.
- Requires preceding execution of PuInc_seeker; cannot operate on raw XCMS output without fold-change and p-value filtering.
- Front-position matching logic (sep.pos.front=TRUE) assumes stable retention-time alignment; misaligned peaks across samples may produce spurious or missed pairings.
- No changelog documented; version compatibility with recent XCMS and R versions unclear.

## Evidence

- [other] The basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold (2000) to identify base-peak isotopologue groupings: "The basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold"
- [other] Validate that the resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations.: "Validate that the resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations."
- [intro] basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds: "basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds"
- [readme] s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000): "s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000)"
- [methods] Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"

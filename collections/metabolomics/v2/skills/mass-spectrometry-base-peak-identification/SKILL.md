---
name: mass-spectrometry-base-peak-identification
description: Use when after PuInc_seeker has identified putative incorporations in XCMS-processed LC/MS data, when you have paired unlabeled and labeled sample groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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
---

# mass-spectrometry-base-peak-identification

## Summary

Identifies base-peak isotopologue groupings from putative stable-isotope incorporations in LC/MS data using atomic mass differences and mass accuracy thresholds. This skill links enriched feature detection to isotope-pair annotation, enabling downstream metabolite identification in stable isotope labeling (SIL) experiments.

## When to use

Apply this skill after PuInc_seeker has identified putative incorporations in XCMS-processed LC/MS data, when you have paired unlabeled and labeled sample groups (e.g., CELL_Glc12 vs. CELL_Glc13) and need to resolve which m/z peaks represent genuine isotope pairs by filtering on mass accuracy (ppm tolerance), intensity thresholds, and expected mass shifts (e.g., 13C vs. 12C = 1.003355 Da).

## When NOT to use

- Input is raw mzXML or mzML data — first run XCMS peak picking, alignment, and grouping.
- Putative incorporations have not yet been identified — run PuInc_seeker first with appropriate fold-change and p-value thresholds.
- Single-sample or non-labeled experiments — basepeak_finder requires paired unlabeled and labeled sample groups.

## Inputs

- geoRge object (PuInc_seeker output with putative incorporations)
- XCMS object (XCMSet from peak picking, alignment, and grouping)
- sample class labels (unlabeled tag, e.g. CELL_Glc12; labeled tag, e.g. CELL_Glc13)

## Outputs

- geoRge object with identified base peaks
- m/z values for base peaks and isotope pairs
- intensity values and isotope-pair annotations

## How to apply

Execute basepeak_finder on the geoRge object output from PuInc_seeker, specifying: (1) unlabeled atomic mass (typically 12.0 for carbon), (2) labeled atomic mass (13.003355 for 13C), (3) mass accuracy tolerance in ppm (6.5 ppm in the mtbls213 example), and (4) minimum intensity threshold for base peaks (2000 in the reference workflow). The function matches m/z values between unlabeled and labeled sample tags using front-position logic, retains only pairs within the specified ppm window and above the intensity cutoff, and annotates each base peak with its isotope partner. Validate output by confirming the resulting geoRge object contains m/z, intensity, and isotope-pair annotations for each identified base peak.

## Related tools

- **geoRge** (Core package providing basepeak_finder function and geoRge object model for stable isotope labeling detection) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Prerequisite: performs peak picking, alignment, and grouping to produce XCMSet input) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **R** (Execution environment for geoRge package and analysis pipeline)

## Examples

```
s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- Output geoRge object is non-empty and contains valid m/z, intensity, and isotope-pair annotations.
- All identified base peaks satisfy mass accuracy constraint: observed m/z difference ≤ 6.5 ppm of theoretical mass shift (1.003355 Da for 13C–12C).
- All base peaks exceed minimum intensity threshold (2000 in reference example).
- Isotope-pair counts align with known labeling pattern (e.g., one 13C incorporation produces m/z +1.003355 shift).
- No base peaks are duplicated across unlabeled and labeled groups; each pair is bidirectional.

## Limitations

- Mass accuracy tolerance (ppm.s) must be empirically tuned for instrument type; 6.5 ppm is example-specific and may not transfer to different LC/MS platforms.
- Minimum intensity threshold (Basepeak.minInt=2000) filters out low-abundance isotopologues; lowering it risks false positives from noise, raising it may miss genuine minor isotope peaks.
- Requires pre-existing putative incorporation annotations from PuInc_seeker; cannot recover incorporations missed at earlier filtering stages (fold-change, p-value, intensity limits).
- geoRge 1.0 changed function arguments; older invocations may fail — consult `help(basepeak_finder)` in the installed version.

## Evidence

- [intro] The basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold (2000) to identify base-peak isotopologue groupings.: "basepeak_finder function operates on PuInc_seeker output and uses unlabeled atom mass (12.0), labeled atom mass (13.003355), mass accuracy tolerance (6.5 ppm), and minimum intensity threshold (2000)"
- [intro] Apply basepeak_finder to the PuInc_seeker output with unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000, matching the same sample tags and position logic.: "Apply basepeak_finder to the PuInc_seeker output with unlabelled atomic mass 12.0, labelled atomic mass 13.003355, mass accuracy tolerance 6.5 ppm, and base-peak minimum intensity threshold 2000"
- [intro] Validate that the resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations.: "resulting geoRge object contains identified base peaks with m/z, intensity, and isotope-pair annotations"
- [readme] s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000): "basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000)"
- [intro] geoRge is a computational tool designed for detecting stable isotope labelling in LC/MS-based untargeted metabolomics: "geoRge is a computational tool designed for detecting stable isotope labelling in LC/MS-based untargeted metabolomics"

---
name: lcms-peak-alignment-and-annotation
description: Use when you have an XCMS-processed feature set (XCMSet object) from replicate LC/MS runs comparing labeled (e.g., 13C-glucose) and unlabeled (e.g., 12C-glucose) conditions, and need to identify which features show isotope incorporation (fold-change ≥1.5, p-value <0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - geoRge
  - R
  - XCMS
  - devtools
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

# LC/MS Peak Alignment and Annotation

## Summary

Align LC/MS peaks across replicate samples and annotate them with putative metabolite identities by matching observed m/z and retention time features against reference databases. This skill enables detection of stable isotope-labeled metabolic features in untargeted metabolomics experiments.

## When to use

You have an XCMS-processed feature set (XCMSet object) from replicate LC/MS runs comparing labeled (e.g., 13C-glucose) and unlabeled (e.g., 12C-glucose) conditions, and need to identify which features show isotope incorporation (fold-change ≥1.5, p-value <0.05) and map them to known or putative metabolites using accurate mass matching (ppm tolerance ~6.5) and intensity filtering.

## When NOT to use

- Input is raw mzXML or mzML files that have not yet undergone XCMS peak picking, alignment, and grouping — preprocess with XCMS first.
- Experiment lacks replicate samples or does not compare labeled versus unlabeled conditions — the fold-change and p-value thresholds require multi-replicate group structure.
- Mass spectrometry data has poor peak resolution or alignment quality — geoRge's isotope detection relies on accurate peak grouping and m/z fidelity.

## Inputs

- XCMSet object (XCMS-processed LC/MS peak set from replicate samples)
- Sample class annotations distinguishing unlabeled and labeled groups
- Reference metabolite database (e.g., in-house or public library formatted for geoRge)
- XCMS object from mtbls213 dataset or equivalent preprocessed mass spectrometry data

## Outputs

- PuIncR object (list of putatively incorporated features with fold-change, p-value, and intensity metadata)
- basepeak_finder result (base peak annotations with m/z matches and isotope assignments)
- Annotated feature table with putative metabolite identities, adduct types, and confidence scores

## How to apply

First, execute the PuInc_seeker function on your XCMS object, specifying unlabeled and labeled sample class tags (e.g., ULtag='CELL_Glc12', Ltag='CELL_Glc13'), and apply fold-change threshold of 1.5, p-value threshold of 0.05, and putative incorporation intensity limit of 4000 to isolate isotope-enriched features. Second, use basepeak_finder to refine the isotope peaks by matching observed m/z values to expected labeled and unlabeled atom masses (UL.atomM=12.0, L.atomM=13.003355) with 6.5 ppm mass accuracy tolerance and minimum base peak intensity of 2000. Finally, run database_query to annotate the filtered features against a reference metabolite database (e.g., negative-mode adducts) to assign putative compound identities. The workflow assumes XCMS has already completed peak picking, alignment, and grouping across all samples.

## Related tools

- **XCMS** (Prerequisite peak picking, retention time alignment, and feature grouping; processes raw mzXML into XCMSet object required by geoRge) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **geoRge** (Core isotope labeling detection tool; houses PuInc_seeker, basepeak_finder, and database_query functions for feature filtering, base peak identification, and metabolite annotation) — https://github.com/jcapelladesto/geoRge
- **R** (Execution environment and programming language for running geoRge functions and parameter configuration)
- **devtools** (R package manager used to install geoRge from GitHub repository)

## Examples

```
s1 <- PuInc_seeker(XCMSet=mtbls213, ULtag="CELL_Glc12", Ltag="CELL_Glc13", sep.pos.front=TRUE, fc.threshold=1.5, p.value.threshold=.05, PuInc.int.lim=4000); s2 <- basepeak_finder(PuIncR=s1, XCMSet=mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- PuInc_seeker output contains features with fold-change ≥1.5 and p-value ≤0.05 between unlabeled and labeled groups; no features fall below the 4000 intensity threshold.
- basepeak_finder successfully matches base peak m/z values to expected labeled (13C, +1.003355 Da) and unlabeled (12C) isotopologue masses within 6.5 ppm tolerance; matched peaks exceed 2000 intensity minimum.
- database_query returns non-empty hit list with assigned adduct types (e.g., [M-H]−) and putative metabolite names; no ambiguous or null annotations for high-confidence features.
- Output feature count is substantially reduced after filtering (e.g., >90% of raw features removed), confirming stringent thresholds eliminated noise while retaining true isotope incorporations.
- Fold-change distribution shows expected bimodal or right-skewed pattern with a clear separation between labeled-enriched and non-enriched features; labeled group intensities are consistently higher than unlabeled for putatively incorporated features.

## Limitations

- geoRge 1.0 has updated function signatures with fewer arguments; users upgrading from earlier versions must consult help(function) to verify parameter names and defaults.
- Database annotation accuracy depends on completeness and curation quality of the reference metabolite library; novel or rare compounds may return no hits or low-confidence matches.
- Mass accuracy tolerance (ppm.s) is fixed at 6.5 ppm; instruments with lower mass resolution or calibration drift may produce false negatives or multiple ambiguous matches per feature.
- The skill assumes well-separated labeled and unlabeled sample classes; poor experimental design (e.g., high cross-contamination or incomplete labeling) will confound fold-change estimates.
- No changelog was found in the repository documentation, limiting visibility into bug fixes or breaking changes in recent versions.

## Evidence

- [intro] fold-change threshold of 1.5, p-value threshold of 0.05, and putative incorporation intensity limit of 4000: "PuInc_seeker with XCMSet=mtbls213, ULtag='CELL_Glc12', Ltag='CELL_Glc13', and sep.pos='f' to identify features with significant abundance differences between unlabelled and labelled groups. 4. Apply"
- [methods] XCMS processing for peak picking, alignment, and grouping prerequisite: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"
- [intro] basepeak_finder mass accuracy and intensity filtering parameters: "basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds  [section=intro; evidence='s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213,"
- [readme] geoRge 1.0 function argument simplification: "Same functions, less arguments I have updated the functions so they are less tiring to use. Check `help(function)` to see the new arguments and function usage"
- [methods] database_query for metabolite annotation: "database_query  [section=methods; evidence='hits <- database_query(geoRgeR = s2, adducts = negative, db = db)']"

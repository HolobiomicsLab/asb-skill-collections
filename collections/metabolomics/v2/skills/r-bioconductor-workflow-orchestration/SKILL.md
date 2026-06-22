---
name: r-bioconductor-workflow-orchestration
description: Use when you have untargeted LC/MS metabolomics data from stable isotope labeling experiments (e.g., 13C-glucose vs. 12C-glucose) already converted to mzXML format, and you need to systematically identify putatively incorporated metabolic features by comparing unlabeled and labeled sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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

# r-bioconductor-workflow-orchestration

## Summary

Orchestrate multi-step LC/MS metabolomics pipelines in R by chaining Bioconductor packages (XCMS, geoRge) with explicit sample class annotations and parameter passing to detect stable isotope-labeled metabolic features. This skill chains peak detection, alignment, and isotope-enrichment inference into a reproducible workflow.

## When to use

You have untargeted LC/MS metabolomics data from stable isotope labeling experiments (e.g., 13C-glucose vs. 12C-glucose) already converted to mzXML format, and you need to systematically identify putatively incorporated metabolic features by comparing unlabeled and labeled sample groups. Use this when you have replicate sample cohorts (e.g., 6 unlabeled, 6 labeled) that require coordinated XCMS preprocessing followed by isotope-aware feature detection.

## When NOT to use

- Input is already a processed feature abundance table or pre-filtered peak list — XCMS preprocessing (peak picking, alignment, grouping) is required upstream
- Sample metadata lacks clear unlabeled–labeled class distinction or replicates are unpaired/unbalanced — the workflow assumes replicated cohorts for valid statistical testing
- LC/MS data originates from targeted (SRM/MRM) or data-dependent acquisition (DDA) methods rather than untargeted full-scan — geoRge is designed for untargeted metabolomics mass traces

## Inputs

- XCMS peak detection object (XCMSet) with aligned and grouped features from mzXML LC/MS data
- Sample metadata mapping sample names to unlabeled or labeled class labels (string tags, e.g. 'CELL_Glc12', 'CELL_Glc13')
- Replicate cohort structure (minimum 2 groups with ≥2 replicates each for statistical comparison)

## Outputs

- PuIncR data structure: ranked list of features with fold-change, p-value, and putative incorporation flags
- Basepeak results: isotope-annotated features mapped to monoisotopic peaks with mass error (ppm) and confidence metrics
- Database query hits (optional downstream): matched metabolite identities from spectral/structural databases

## How to apply

Begin by loading XCMS-processed peak data (via the `data(mtbls213)` pattern or custom XCMS object) into R. Set sample class annotations to distinguish unlabeled (e.g., CELL_Glc12_05mM_Normo) from labeled (e.g., CELL_Glc13_05mM_Normo) replicates using the metadata slot. Then execute PuInc_seeker with matched XCMSet, ULtag, and Ltag parameters, applying fold-change (default 1.5), p-value (default 0.05), and intensity thresholds (e.g., PuInc.int.lim=4000) to filter features with statistically significant and biologically meaningful differences between groups. Chain the output to basepeak_finder to resolve putative incorporations to their likely base peaks using atomic mass (UL.atomM=12.0, L.atomM=13.003355) and mass accuracy (ppm.s=6.5). This ordered chaining ensures coherent parameter propagation and avoids re-reading raw data.

## Related tools

- **XCMS** (Peak picking, alignment, and grouping of LC/MS features from raw mzXML; produces the XCMSet input object) — https://bioconductor.org/packages/release/bioc/html/xcms.html
- **geoRge** (Stable isotope labeling detection; provides PuInc_seeker, basepeak_finder, and database_query functions for isotope-enrichment workflow) — https://github.com/jcapelladesto/geoRge
- **devtools** (R package installation from GitHub repositories)
- **R** (Statistical computation and workflow orchestration environment)

## Examples

```
library(geoRge); data(mtbls213); s1 <- PuInc_seeker(XCMSet=mtbls213, ULtag="CELL_Glc12", Ltag="CELL_Glc13", sep.pos.front=TRUE, fc.threshold=1.5, p.value.threshold=0.05, PuInc.int.lim=4000); s2 <- basepeak_finder(PuIncR=s1, XCMSet=mtbls213, UL.atomM=12.0, L.atomM=13.003355, ppm.s=6.5, Basepeak.minInt=2000)
```

## Evaluation signals

- PuIncR output contains non-empty ranked feature table with fold-change ≥ 1.5 and p-value ≤ 0.05, confirming statistical filtering was applied
- Basepeak_finder mass error (ppm) values fall within specified tolerance (e.g., ≤ 6.5 ppm for input ppm.s=6.5), validating isotope-to-monoisotopic mapping precision
- Putative incorporation intensity for flagged features exceeds the specified intensity limit (e.g., ≥ 4000 for PuInc.int.lim=4000), confirming intensity thresholding
- Number of output features is substantially smaller than input XCMSet features, reflecting expected filtering stringency for stable isotope signals
- Replicate fold-change consistency: compare PuIncR fold-changes across replicates or cross-validation splits to ensure robustness of isotope detection

## Limitations

- Requires clear, replicated sample cohort structure — unpaired or single-replicate designs cannot be statistically validated by the p-value threshold
- Fixed threshold parameters (fold-change=1.5, p-value=0.05, intensity=4000) may be suboptimal for datasets with different dynamic ranges or noise profiles; user customization needed
- Assumes XCMS preprocessing has already been completed with appropriate retention-time alignment and peak grouping; misalignment upstream invalidates downstream isotope detection
- No built-in handling of confounding natural isotope distributions (e.g., 13C background in unlabeled samples) beyond mass accuracy filtering — high natural abundance isotopes may inflate false positives
- geoRge 1.0 reduced function arguments ('less tiring to use') but may introduce breaking changes if older scripts use deprecated parameter names; see help(function) documentation

## Evidence

- [intro] Workflow overview and chaining rationale: "s1 <- PuInc_seeker(XCMSet=mtbls213,ULtag="CELL_Glc12",Ltag="CELL_Glc13", sep.pos.front=TRUE ,fc.threshold=1.5,p.value.threshold=.05,PuInc.int.lim = 4000)"
- [methods] XCMS preprocessing requirement: "Use XCMS package (https://bioconductor.org/packages/release/bioc/html/xcms.html) for peak picking, alignment and grouping"
- [intro] Basepeak_finder chaining and mass accuracy parameters: "s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000)"
- [readme] Installation and library loading in R: "install_github("jcapelladesto/geoRge")
library(geoRge)"
- [readme] geoRge 1.0 documentation and parameter simplification: "I have updated the functions so they are less tiring to use. Check `help(function)` to see the new arguments and function usage"
- [methods] Core skill application: isotope-enriched feature detection rationale: "Set sample class annotations to distinguish CELL_Glc12_05mM_Normo (unlabelled, 6 replicates) from CELL_Glc13_05mM_Normo (labelled, 6 replicates)"

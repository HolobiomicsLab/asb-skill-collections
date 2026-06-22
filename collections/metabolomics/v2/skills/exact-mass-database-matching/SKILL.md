---
name: exact-mass-database-matching
description: Use when after feature detection and alignment on raw MS data, when you have a list of unknown feature m/z values and need to assign them to known xenobiotic metabolites or their predicted biotransformation products.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  tools:
  - tidyverse
  - CluMSID
  - CluMSIDdata
  - grid
  - OrgMassSpecR
  - pheatmap
  - reshape2
  - MSMSsim
  - msentropy
  - readxl
  - MSDial
  - Biotransformer
derived_from:
- doi: 10.1021/acs.est.5c08558
  title: CMDN
evidence_spans:
- tidyverse
- CluMSID
- CluMSIDdata
- grid
- OrgMassSpecR
- pheatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmdn_cq
    doi: 10.1021/acs.est.5c08558
    title: CMDN
  dedup_kept_from: coll_cmdn_cq
schema_version: 0.2.0
---

# exact-mass-database-matching

## Summary

Match detected metabolite features to xenobiotic reaction databases by computing exact monoisotopic mass and comparing against reference metabolite masses. This skill enables high-throughput annotation of reaction-derived metabolites in untargeted MS data by reducing candidate space through mass accuracy.

## When to use

After feature detection and alignment on raw MS data, when you have a list of unknown feature m/z values and need to assign them to known xenobiotic metabolites or their predicted biotransformation products. Apply this skill when mass spectrometry accuracy is sufficient (typically <5 ppm for high-resolution instruments) and you have access to a curated xenobiotic reaction database (e.g., one derived from Biotransformer predictions).

## When NOT to use

- Input is already a fully annotated metabolite table with confirmed identities — skip to pathway analysis.
- Mass spectrometer accuracy is poor (>10 ppm or unit-resolution only) and no orthogonal confirmation method (MS/MS, RT standards) is available.
- Xenobiotic database is unavailable or does not cover the metabolites of interest (e.g., studying endogenous lipids instead of drug metabolites).

## Inputs

- aligned feature table with m/z values and retention time
- raw MS/MS fragmentation spectra (NetCDF or mzML format)
- xenobiotic reaction database or biotransformation predictions from Biotransformer
- chemical formula reference table or structure library

## Outputs

- annotated feature table with matched metabolite identities
- reaction pathway assignments and biotransformation metadata
- mass match quality scores (e.g., ppm error, entropy, similarity rank)

## How to apply

Calculate exact monoisotopic mass for each detected feature using OrgMassSpecR, which computes theoretical m/z from chemical formulas or from empirical peak m/z. Compare each feature mass against the xenobiotic reaction database with a mass tolerance appropriate to your instrument accuracy (the CMDN pipeline is compatible with MSDial ver. 4.80 for feature input). Use CluMSID's cluster-based annotation propagation to assign metabolite identities to features that fall within the mass tolerance window. Validate matches by cross-referencing with fragmentation pattern similarity (via MSMSsim) and spectral entropy (via msentropy) to increase confidence in annotations before export. The workflow assumes features are pre-aligned and represent distinct metabolic entities.

## Related tools

- **OrgMassSpecR** (Calculates exact monoisotopic mass and performs database mass matching for annotated features)
- **CluMSID** (Clusters features and propagates metabolite annotations across aligned features with similar mass and fragmentation patterns)
- **MSMSsim** (Computes fragmentation pattern similarity scores between unknown features and reference spectra to validate mass-based matches)
- **msentropy** (Calculates spectral entropy to assess fragment complexity and confidence in match assignments)
- **MSDial** (Performs feature detection and alignment prior to exact mass matching; compatible version 4.80)
- **Biotransformer** (Generates predicted xenobiotic biotransformation products and reaction database for mass matching reference)

## Evaluation signals

- Mass error between observed and annotated feature m/z is within instrument accuracy (typically <5 ppm for high-resolution MS).
- Annotated features show coherent cluster assignments with similar fragmentation patterns (MSMSsim score and spectral entropy consistent across matched features).
- Reaction pathway metadata assigned to features is chemically plausible (e.g., Phase I oxidation, Phase II conjugation) and traceable to Biotransformer or literature predictions.
- Manual inspection of top-ranked matches confirms that highest-scoring annotations correspond to expected metabolites of known xenobiotics in the experiment.
- Proportion of annotated features is consistent with expected xenobiotic metabolism complexity (typically 5–20 metabolites per parent compound in controlled studies).

## Limitations

- Exact mass matching alone cannot distinguish isomers or isobars with identical m/z; MS/MS fragmentation pattern similarity is required for disambiguation.
- Annotation accuracy depends on database completeness; if predicted metabolites from Biotransformer are absent or incorrect, matches will fail or be spurious.
- Mass tolerance is critical and instrument-dependent; poorly calibrated instruments or drifting mass accuracy will increase false negatives and false positives.
- The CMDN pipeline requires ten R packages; compatibility issues or version mismatches can prevent reproducible execution across computing environments.

## Evidence

- [other] Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation.: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation"
- [other] CMDN pipeline requires installation of ten R packages and is compatible with MSDial (ver. 4.80) and Biotransformer 3.0.: "The CMDN pipeline requires installation of ten R packages (tidyverse, CluMSID, CluMSIDdata, grid, OrgMassSpecR, pheatmap, reshape2, MSMSsim, msentropy, readxl) and is compatible with MSDial (ver."
- [readme] CMDN is a top-down untargeted metabolomics-based MS data processing framework for high-throughput and automated annotation of reaction-derived xenobiotic metabolites.: "Compound metabolite discovery network (CMDN) is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived"
- [other] Apply MSMSsim to compute fragmentation pattern similarity scores and msentropy to assess fragment complexity and confidence for match validation.: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra. Calculate spectral entropy using msentropy to assess fragment complexity and confidence"

---
name: mass-tolerance-optimization-hrms
description: Use when you have experimental peak lists (m/z, retention time, intensity)
  from peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer) and need
  to match them against a simulated lipid fragment library (500,000+ lipid species).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values
  with simulated library m/z values
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS,
  MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-optimization-hrms

## Summary

Optimize mass tolerance thresholds for matching experimental fragment m/z values to in-silico lipid library m/z values in high-resolution tandem mass spectrometry (HRMS/MS) workflows. Correct mass tolerance selection balances specificity (fewer false positives) against sensitivity (capturing true lipid identifications) across different instrument platforms and fragmentation methods.

## When to use

You have experimental peak lists (m/z, retention time, intensity) from peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer) and need to match them against a simulated lipid fragment library (500,000+ lipid species). Mass tolerance optimization is critical when: (1) you are transitioning between instrument platforms (Q-Exactive, Q-TOF, Bruker, SCIEX, Agilent); (2) you are switching fragmentation methods (targeted, ddMS2-topN, AIF); or (3) you observe either too many candidate identifications per peak (low specificity, high false positive rate) or too few matches (low sensitivity, missed identifications).

## When NOT to use

- Input is already a validated, manually curated lipid identifications table — re-optimization risks introducing error without benefit.
- Data were acquired on Waters instruments — LipidMatch does not currently support Waters files.
- Fragment library is empty, missing, or incompatible with your lipid class of interest.

## Inputs

- Experimental peak list (m/z, retention time, intensity) from peak-picking software output
- In-silico fragmentation library (500,000+ lipid species across 60+ lipid types)
- Parent ion m/z values for candidate lipids

## Outputs

- Annotated feature table with assigned lipid identifications
- Matching scores per candidate (number of matched fragments, intensity correlation)
- Confidence levels per lipid identification
- Ranked candidate list per peak

## How to apply

Load your experimental peak list and in-silico fragmentation library into LipidMatch. For each experimental peak, retrieve candidate lipid species from the library based on parent ion m/z with an initial mass tolerance threshold (start with typical instrument resolution specifications, e.g., 5 ppm for Orbitrap, 10 ppm for Q-TOF). Match experimental fragment m/z values against simulated library fragment m/z values for each candidate using the same mass tolerance. Calculate a matching score (number of matched fragments, intensity correlation, or similar metric) for each candidate. Rank candidates by matching score and assign confidence levels. Validate the tolerance choice by examining the distribution of matched fragments per peak and the false discovery rate against known standards or replicates. Adjust the tolerance iteratively: tighten it if too many candidates remain per peak, or relax it if too few fragments match true identifications. The optimal tolerance reflects the mass accuracy capabilities of your specific instrument and fragmentation method.

## Related tools

- **LipidMatch** (Performs fragment m/z matching and lipid identification; user configures mass tolerance threshold for fragment matching) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak-picking software; generates experimental peak lists (m/z, retention time, intensity) that feed into LipidMatch)
- **XCMS** (Peak-picking software; generates experimental peak lists for LipidMatch processing)
- **MS-DIAL** (Peak-picking software; generates experimental peak lists for LipidMatch processing)
- **Compound Discoverer** (Peak-picking software; generates experimental peak lists for LipidMatch processing)
- **Q-Exactive** (High-resolution Orbitrap UHPLC-HRMS/MS instrument; reference platform for mass tolerance validation across targeted, ddMS2-topN, and AIF methods)

## Evaluation signals

- Distribution of matched fragment counts per peak is unimodal and centered on true identifications (not bimodal with one mode at zero or one).
- Sensitivity (recall) for known lipid standards is ≥90%, indicating that true identifications are not filtered out by excessive tolerance tightness.
- Specificity (precision) is ≥85%, measured as (true identifications) / (all candidates ranked #1), indicating that tolerance is not so loose that false positives rank first.
- Number of candidates per peak has median ≤5 for the top-ranked hit, indicating reasonable specificity; median >10 suggests tolerance is too loose.
- Mass accuracy of matched fragments across replicates and samples is consistent with the instrument's nominal resolution (e.g., ≤5 ppm for Orbitrap, ≤10 ppm for Q-TOF), and matches do not cluster at the tolerance boundary (suggesting tolerance is not arbitrary).

## Limitations

- LipidMatch does not currently support Waters instrument files; users with Waters data must convert to mzML or equivalent before use.
- Mass tolerance optimization is instrument-platform specific; a tolerance optimized for Q-Exactive may not transfer directly to Q-TOF or Bruker platforms without revalidation.
- Optimization is fragmentation-method specific; tolerances for targeted MS/MS may differ from ddMS2-topN or AIF, requiring separate validation for each method.
- In-silico fragmentation library comprehensiveness and accuracy directly affect the number and quality of candidate matches; missing or incorrect library entries will reduce sensitivity regardless of tolerance choice.
- The matching score metric (fragment count, intensity correlation, or other) must be chosen and validated carefully; different metrics may favor different tolerances and produce different confidence rankings.

## Evidence

- [readme] Fragment m/z matching in LipidMatch: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [intro] Mass tolerance as a parameter in matching workflow: "For each experimental peak, retrieve candidate lipid species from the library based on parent ion m/z with specified mass tolerance"
- [intro] Matching score calculation: "Calculate matching score (number of matched fragments, intensity correlation, or similar metric) for each candidate"
- [readme] Instrument-specific validation: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHRLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] In-silico library scale and diversity: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] Waters file incompatibility: "The software does not currently support Waters files"

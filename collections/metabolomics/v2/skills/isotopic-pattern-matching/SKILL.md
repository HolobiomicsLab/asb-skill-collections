---
name: isotopic-pattern-matching
description: Use when after feature detection has produced candidate formula–adduct
  pairs and their corresponding m/z values, but before final compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - MetaboShiny
  - R
  - Scannotation
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
- doi: 10.1021/acs.est.3c04764
  title: ''
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
- Scannotation is an automated and user-friendly suspect screening tool for the rapid
  pre-annotation of LC-HRMS datasets.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  - build: coll_scannotation_cq
    doi: 10.1021/acs.est.3c04764
    title: Scannotation
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  - 10.1021/acs.est.3c04764
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Isotopic Pattern Matching

## Summary

Ranks and filters candidate molecular formula and adduct annotations by computing similarity between observed isotopic patterns from mass spectrometry data and theoretical patterns predicted from molecular formulas. This skill is essential for disambiguating among multiple formula–adduct candidates with identical or near-identical monoisotopic m/z values.

## When to use

Apply this skill after feature detection has produced candidate formula–adduct pairs and their corresponding m/z values, but before final compound identification. Use it when multiple candidates share the same or very similar monoisotopic mass and you need to leverage isotopic fine structure (13C, 2H, 18O, 34S abundances) to discriminate among them. The skill is triggered by the availability of observed isotopic patterns in the feature detection output and a need to rank candidates by isotopic fit.

## When NOT to use

- Input contains only monoisotopic m/z values with no isotopic pattern information (isotope scoring requires fine structure data).
- Candidate pool is already filtered to a single formula–adduct pair (no ranking or discrimination is needed).
- Mass spectrometry data was acquired at resolving power insufficient to resolve isotope peaks (e.g., low-resolution TOF or Orbitrap below ~30k resolution at m/z 400).

## Inputs

- candidate molecular formula and adduct pairs
- observed m/z isotopic intensity patterns from feature detection
- feature detection output (e.g., XCMS or MetaboAnalyst export)
- isotope scoring configuration (method, intensity imprecision threshold)

## Outputs

- ranked annotation table with isotope scores
- filtered candidate list (above isotope score threshold)
- isotope score per candidate

## How to apply

Load candidate formula–adduct pairs alongside their observed isotopic intensity patterns from feature detection. For each candidate, calculate the theoretical isotopic pattern by enumerating all isotopologues of the molecular formula in the specified adduct state and computing their theoretical abundances. Compute an isotope score by measuring pattern similarity using cosine similarity or intensity correlation between observed and theoretical distributions. Apply the isotope scoring threshold configured in MetaboShiny's Isotope scoring settings (which includes method selection—currently M-score—and intensity imprecision tolerance, defaulting to 2%). Rank all candidates in descending order by isotope score and output the ranked annotation table. The rationale is that true formula–adduct assignments will exhibit high isotopic pattern fidelity, while incorrect assignments will show poor pattern matching.

## Related tools

- **MetaboShiny** (Interactive environment for configuring isotope scoring method, intensity imprecision threshold, and applying scores to rank candidate annotations) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Statistical and computational language for implementing isotope pattern calculation, similarity metrics, and ranking workflows)

## Evaluation signals

- Isotope scores are in range [0, 1] or according to the M-score specification; no NaN or infinite values.
- True-positive candidate (verified by independent means, e.g., MS/MS or reference standard) ranks first or within top 3 when multiple candidates are present.
- Candidates with isotope scores below the configured threshold are successfully filtered and excluded from output.
- Observed and theoretical isotopic pattern distributions show visual alignment (plot overlay or correlation coefficient > 0.8) for high-scoring candidates.
- Ranking is monotonic (descending isotope scores); ties are handled consistently (e.g., tie-break by m/z error or formula complexity).

## Limitations

- Isotope scoring assumes accurate theoretical prediction of isotopic patterns; errors in isotopologue abundance calculations or adduct modeling degrade discriminative power.
- Method is sensitive to instrument calibration and resolving power; poor mass accuracy or low peak resolution can blur isotope peaks and reduce scoring sensitivity.
- Intensity imprecision threshold (default 2%) is a global parameter; optimal threshold may vary by formula mass range, instrument, or ionization mode, requiring manual tuning.
- Rare isotope patterns (e.g., for sulfur or chlorine) require sufficient intensity signal and dynamic range; low-abundance features may not yield reliable isotopic data.
- Currently MetaboShiny only offers M-score as the isotope scoring method; no alternative algorithms (e.g., Kullback–Leibler divergence or cross-correlation) are documented as available.

## Evidence

- [other] MetaboShiny includes an Isotope scoring configuration setting as part of its pre-analysis workflow, located within the Settings section alongside Global, Project, Search, Adducts, and Formula prediction parameters.: "MetaboShiny includes an Isotope scoring configuration setting as part of its pre-analysis workflow, located within the Settings section alongside Global, Project, Search, Adducts, and Formula"
- [other] For each candidate, calculate the theoretical isotopic pattern using the molecular formula and specified adduct. Compute isotope score by measuring the similarity between observed and theoretical patterns (e.g., cosine similarity or intensity correlation). Apply isotope scoring threshold filters as configured in the Isotope scoring settings. Rank all candidates by isotope score in descending order and output the ranked annotation table with scores.: "For each candidate, calculate the theoretical isotopic pattern using the molecular formula and specified adduct. Compute isotope score by measuring the similarity between observed and theoretical"
- [readme] Select the method to use to score compounds that have the same weight (currently only M-score available). Set the intensity imprecision (default: 2%).: "Select the method to use to score compounds that have the same weight (currently only M-score available). Set the intensity imprecision (default: 2%)."

---
name: spectral-feature-scrambling-permutation
description: Use when when performing large-scale untargeted metabolomics annotations
  where you need to assess the false discovery rate of metabolite identifications
  but lack sufficient negative control samples or decoy compound databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - commons-math3
  - jfreechart
  - jopt-simple
  - trove4j
  - Passatutto
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- commons-math3-3.4.1
- jfreechart-1.0.17-experimental
- jopt-simple-4.3
- trove4j-3.0.3
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_matching_significance_estimatio_cq
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectral_matching_significance_estimatio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12020173
  all_source_dois:
  - 10.3390/metabo12020173
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-feature-scrambling-permutation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A decoy generation method that creates synthetic scrambled or permuted spectral features while preserving key statistical properties, enabling false discovery rate estimation in untargeted metabolomics annotation without requiring experimental negative controls.

## When to use

When performing large-scale untargeted metabolomics annotations where you need to assess the false discovery rate of metabolite identifications but lack sufficient negative control samples or decoy compound databases. Apply this when you want to control annotation significance across thousands of candidate matches to a reference spectral library.

## When NOT to use

- The input spectra are already known to be high-quality validated identifications — decoy generation is for assessing confidence in novel or uncertain annotations, not for re-scoring confirmed matches.
- You have access to experimentally validated negative control samples or a mature decoy spectral library already embedded in your search engine — this skill replaces the need for such external decoys, not supplements them.
- Your annotation pipeline is targeted (e.g., applying MRM or known-compound lists) rather than untargeted — decoy scrambling is designed for large-scale open searches where the FDR is unknown a priori.

## Inputs

- metabolomics spectral dataset (MS/MS spectra with m/z and intensity values)
- reference compound database with annotated spectra
- spectral similarity scoring function or annotation algorithm

## Outputs

- decoy spectral database (synthetic scrambled spectra parallel to reference)
- combined reference + decoy search space
- per-match FDR estimates and significance thresholds
- FDR-annotated metabolite identifications with q-values or posterior error probabilities

## How to apply

Load the reference metabolomics spectral dataset and compound database. Apply the Passatutto decoy generation algorithm to systematically scramble or permute spectral feature intensities and m/z values while preserving the overall statistical distribution and number of peaks per spectrum. Construct a parallel decoy compound database using these synthetic spectra. Combine reference and decoy databases into a unified search space and score candidate annotations against both. Compute FDR statistics by comparing reference annotation scores to decoy scores, retaining only matches whose reference score significantly exceeds the distribution of decoy scores. The rationale is that true annotations will score higher against reference spectra than against randomly scrambled decoys, whereas false positives will match both equally well.

## Related tools

- **commons-math3** (statistical distribution and permutation computations for decoy feature generation and FDR threshold calculation)
- **jfreechart** (visualization of score distributions (reference vs. decoy) to validate FDR calibration)
- **jopt-simple** (command-line argument parsing for configuring decoy generation parameters and output options)
- **trove4j** (efficient in-memory data structures for large spectral and decoy database indexing)
- **Passatutto** (reference implementation of the complete decoy generation and FDR estimation workflow) — https://github.com/boecker-lab/passatuto

## Evaluation signals

- Decoy spectra preserve the empirical distribution of peak counts, mass ranges, and intensity magnitudes as the reference spectra — verify by comparing histograms or statistical moments.
- Score distributions of reference and decoy matches are well-separated (reference scores >> decoy scores for true metabolites); visual inspection via score-scatter plots or ROC analysis.
- FDR estimates are calibrated: when computed q-values are thresholded at α (e.g., 0.01), the empirical false discovery rate among retained annotations should be ≤ α.
- Decoy-based FDR estimates are conservative (i.e., fewer identifications retained) compared to unadjusted or permissive scoring — confirms the method is not over-calling.
- Reproducibility: running the same algorithm on the same input spectra and database produces identical decoy databases and FDR tables (or probabilistically equivalent distributions if randomness is seeded).

## Limitations

- Decoy generation assumes that scrambling preserves the null distribution of random matches; this may fail if spectral features have strong non-random correlations or if the reference database is biased toward particular mass ranges or chemical classes.
- The method does not account for library bias — if the reference database is enriched for certain metabolite classes, decoy FDR estimates may not generalize to underrepresented classes.
- Computational cost scales with database size; generating and scoring against a combined reference+decoy database can double or more the runtime of annotation.
- No changelog or version history provided in the repository, limiting reproducibility and tracking of algorithm refinements across versions.

## Evidence

- [other] Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties.: "Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties"
- [other] Construct a decoy compound database parallel to the reference database using the generated decoy spectra.: "Construct a decoy compound database parallel to the reference database using the generated decoy spectra"
- [other] Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics.: "Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics"
- [other] Significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control in this domain.: "Significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control"

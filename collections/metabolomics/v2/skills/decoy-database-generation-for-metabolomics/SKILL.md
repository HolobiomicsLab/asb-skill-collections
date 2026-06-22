---
name: decoy-database-generation-for-metabolomics
description: Use when performing large-scale untargeted metabolomics annotation where you need to estimate the false discovery rate of metabolite identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - commons-math3
  - jfreechart
  - jopt-simple
  - trove4j
  - Passatutto
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# decoy-database-generation-for-metabolomics

## Summary

Generate synthetic decoy spectral databases in parallel with reference compound databases to enable false discovery rate estimation in untargeted metabolomics annotation. This skill addresses the critical need for significance control when annotating large numbers of metabolite matches against spectral databases.

## When to use

Apply this skill when performing large-scale untargeted metabolomics annotation where you need to estimate the false discovery rate of metabolite identifications. Use it when you have a metabolomics spectral dataset and a reference compound database, and you need to distinguish true metabolite matches from random coincidences by scoring candidates against both reference and decoy entries.

## When NOT to use

- When you already have pre-computed FDR values or significance scores from a prior annotation run—decoy generation is redundant.
- When performing targeted metabolomics with a small, manually curated set of known compounds—the statistical framework is designed for large-scale untargeted contexts.
- When your reference database is extremely small (< 100 compounds) or lacks sufficient spectral diversity—decoy generation may not yield representative background statistics.

## Inputs

- metabolomics spectral dataset (mass spectrometry data with m/z and intensity values)
- reference compound database (annotated metabolite entries with spectral signatures)

## Outputs

- decoy spectral database (synthetic spectra with scrambled/permuted features)
- unified search database (reference + decoy entries combined)
- FDR-annotated metabolite annotations (matches with computed significance estimates)

## How to apply

Load your metabolomics spectral dataset and reference compound database. Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties (e.g., mass distributions, peak intensities). Construct a parallel decoy compound database from these generated decoy spectra. Combine the reference and decoy databases into a unified search space. Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics. Output FDR-annotated results with significance estimates for each metabolite match, allowing downstream filtering by user-defined FDR thresholds.

## Related tools

- **commons-math3** (Statistical computation and random number generation for decoy spectrum scrambling)
- **jfreechart** (Visualization of FDR distributions and annotation scores)
- **jopt-simple** (Command-line parameter parsing for Passatutto configuration)
- **trove4j** (Efficient collection handling for large spectral databases and decoy storage)
- **Passatutto** (Complete decoy generation and FDR estimation framework) — https://github.com/boecker-lab/passatuto

## Evaluation signals

- Decoy database size and spectral count match reference database dimensions (1:1 ratio expected).
- FDR values increase monotonically or remain stable across ranked annotation scores (no inverted or chaotic FDR curves).
- Decoy-to-reference score distribution shows clear separation with minimal overlap at high-confidence regions, indicating effective background model.
- FDR-filtered annotation results show expected proportion of matches below user-specified threshold (e.g., 5% FDR = ≤5% estimated false matches).
- Preserved statistical properties in decoy spectra (e.g., mass range, peak count, intensity distributions similar to reference spectra).

## Limitations

- Decoy generation quality depends on the reference database composition and diversity; biased or incomplete reference databases yield unrepresentative decoy statistics.
- The method assumes that scrambling/permuting spectral features preserves appropriate null-hypothesis background statistics; this assumption may fail for highly structured spectral patterns.
- Computational cost scales with database size and number of spectra; very large databases may require substantial memory and processing time.
- FDR estimates are probabilistic and rely on sufficient numbers of decoy matches; sparse annotation scenarios may yield unstable significance estimates.

## Evidence

- [other] The paper describes a significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control in this domain.: "The paper describes a significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control"
- [other] Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties.: "Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties."
- [other] Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics.: "Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics."
- [other] Construct a decoy compound database parallel to the reference database using the generated decoy spectra.: "Construct a decoy compound database parallel to the reference database using the generated decoy spectra."
- [other] Output the FDR-annotated results with significance estimates for each metabolite match.: "Output the FDR-annotated results with significance estimates for each metabolite match."

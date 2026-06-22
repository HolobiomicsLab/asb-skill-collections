---
name: annotation-scoring-and-ranking
description: Use when you have experimental mass spectra from untargeted metabolomics and need to assign compound identities with confidence estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - commons-math3
  - jfreechart
  - jopt-simple
  - trove4j
  - Passatutto
  techniques:
  - LC-MS
  - NMR
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

# annotation-scoring-and-ranking

## Summary

Score and rank metabolite annotations by comparing experimental spectra against both reference and decoy compound databases, computing false discovery rates to assign statistical significance to each match. This skill enables large-scale untargeted metabolomics annotation with controlled error rates.

## When to use

You have experimental mass spectra from untargeted metabolomics and need to assign compound identities with confidence estimates. Use this skill when you want to rank candidate annotations by quality while controlling false discovery rate—particularly in large-scale experiments where spurious matches are likely due to high search space.

## When NOT to use

- Input spectra are already annotated with high confidence from orthogonal methods (e.g., reference standards, NMR validation)—ranking and FDR control adds no value.
- Reference database is very small or highly curated such that decoy generation does not yield meaningful null statistics.
- Analysis requires targetted metabolomics with predefined compound lists rather than open-ended untargeted search and ranking.

## Inputs

- experimental metabolomics spectral dataset (MS/MS spectra with m/z and intensity values)
- reference compound database (structures, molecular formulas, fragmentation patterns)

## Outputs

- ranked annotation list with scores for each spectrum–compound pair
- false discovery rate statistics per annotation
- filtered high-confidence metabolite assignments with significance estimates

## How to apply

Load experimental spectra and a reference compound database, then construct a parallel decoy database by scrambling or permuting spectral features while preserving statistical properties. Score each experimental spectrum against both reference and decoy entries using a consistent scoring function (e.g., cosine similarity or spectral matching metric). Compute the false discovery rate as the ratio of decoy matches to reference matches at each score threshold. Rank annotations by score and filter to a user-defined FDR cutoff (e.g., FDR < 0.05) to output high-confidence metabolite assignments with associated significance estimates.

## Related tools

- **commons-math3** (Statistical computation for FDR threshold estimation and score distribution analysis)
- **jfreechart** (Visualization of score distributions and FDR curves)
- **jopt-simple** (Command-line argument parsing for scoring parameters and FDR cutoff configuration)
- **trove4j** (Efficient data structures for large-scale score storage and ranking operations)
- **Passatutto** (Integrated pipeline for decoy generation, spectral scoring, and FDR-controlled annotation ranking) — https://github.com/boecker-lab/passatuto

## Evaluation signals

- FDR statistics are monotonically increasing with decreasing score threshold (lower scores = higher FDR).
- Number of reference matches exceeds decoy matches at all score thresholds, confirming decoy database is not enriched.
- Annotations retained at target FDR (e.g., FDR < 0.05) show higher validation rate (e.g., match to reference standards) than annotations filtered at permissive FDR.
- Score distributions for reference and decoy entries are distinct, with reference entries concentrated at higher scores.
- Rank order is consistent across repeated runs with the same parameters and input data.

## Limitations

- Decoy generation by feature scrambling assumes that preserved statistical properties sufficiently model the null distribution; systematic bias in spectral databases may violate this assumption.
- FDR control is conservative and sample-level rather than experiment-wide; multiple testing correction may reduce sensitivity in small datasets.
- Performance depends on reference database completeness and quality; sparse or biased databases yield unreliable null statistics.

## Evidence

- [other] Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics.: "Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics."
- [other] Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties.: "Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties."
- [intro] Significance estimation enabling large scale untargeted metabolomics annotations: "Significance estimation enabling large scale untargeted metabolomics annotations"
- [other] The paper describes a significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control in this domain.: "The paper describes a significance estimation method called Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control"
- [other] Output the FDR-annotated results with significance estimates for each metabolite match.: "Output the FDR-annotated results with significance estimates for each metabolite match."

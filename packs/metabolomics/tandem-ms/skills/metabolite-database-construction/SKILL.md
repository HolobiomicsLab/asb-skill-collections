---
name: metabolite-database-construction
description: Use when when performing untargeted metabolomics annotation at scale and you need to estimate false discovery rates for candidate metabolite identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
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
  - tandem-MS
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

# metabolite-database-construction

## Summary

Construct reference and decoy compound databases for untargeted metabolomics annotation by applying spectral feature permutation and statistical property preservation. This enables false discovery rate estimation and significance control in large-scale metabolite matching workflows.

## When to use

When performing untargeted metabolomics annotation at scale and you need to estimate false discovery rates for candidate metabolite identifications. Apply this skill when you have a reference spectral dataset and compound database but lack calibrated significance thresholds for matching quality.

## When NOT to use

- When your spectral dataset is already scored with empirical FDR or p-values from independent validation experiments
- When the reference database is too small (<100 compounds) to support reliable statistical estimation of decoy match distributions
- When input spectra lack sufficient feature resolution or statistical variance to preserve meaningful properties during permutation

## Inputs

- Metabolomics spectral dataset (e.g., MS/MS spectra in standard format)
- Reference compound database with spectral features and chemical metadata

## Outputs

- Reference compound database
- Decoy compound database (parallel structure with permuted spectra)
- Unified search space (reference + decoy combined)
- FDR-annotated annotation results with per-match significance estimates

## How to apply

Load the metabolomics spectral dataset and reference compound database as parallel inputs. Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties (e.g., feature distribution moments). Construct a parallel decoy compound database mirroring the reference database structure. Combine reference and decoy databases into a unified search space. Score candidate annotations against both reference and decoy entries using the same matching metric. Compute false discovery rate statistics as the ratio of decoy matches to reference matches at each score threshold. Output FDR-annotated results with significance estimates for each metabolite match.

## Related tools

- **commons-math3** (Statistical distributions and permutation algorithms for decoy generation)
- **jfreechart** (Visualization of FDR distributions and significance thresholds)
- **jopt-simple** (Command-line argument parsing for workflow configuration)
- **trove4j** (Efficient in-memory data structures for large compound databases)
- **Passatutto** (Reference implementation of decoy spectrum generation and FDR estimation) — https://github.com/boecker-lab/passatuto

## Evaluation signals

- Decoy database has identical size and structure to reference database, with feature distributions statistically equivalent to reference (checked via moment preservation)
- FDR values are monotonically non-decreasing as matching score threshold increases
- At high matching scores (top 1–5% of candidates), decoy match rate is substantially lower than reference match rate, indicating discrimination power
- FDR estimates stabilize (plateau) at high thresholds, confirming sufficient decoy sampling
- Unified search space score distributions show separation between reference and decoy peaks when visualized

## Limitations

- Decoy generation assumes that permuting spectral features while preserving statistical moments does not eliminate biologically meaningful patterns; extreme fragmentation patterns or rare neutral losses may be artificially regenerated in decoys and inflate false discovery estimates
- FDR estimation accuracy depends on having a representative reference database; systematic bias or incompleteness in the reference will propagate to decoy expectations
- Computational cost scales with database size and number of spectral features; very large datasets may require memory optimization or batch processing

## Evidence

- [other] Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties.: "Apply the Passatutto decoy generation algorithm to create synthetic decoy spectra by scrambling or permuting spectral features while preserving key statistical properties."
- [other] Combine the reference and decoy databases into a unified search space.: "Combine the reference and decoy databases into a unified search space."
- [other] Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics.: "Score candidate annotations against both reference and decoy entries to compute false discovery rate statistics."
- [other] Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control in this domain.: "Passatutto that is designed to enable large-scale untargeted metabolomics annotations, addressing the need for false discovery rate control in this domain."
- [readme] Dependencies:
 - commons-math3-3.4.1
 - jfreechart-1.0.17-experimental
 - jopt-simple-4.3
 - trove4j-3.0.3: "commons-math3-3.4.1, jfreechart-1.0.17-experimental, jopt-simple-4.3, trove4j-3.0.3"

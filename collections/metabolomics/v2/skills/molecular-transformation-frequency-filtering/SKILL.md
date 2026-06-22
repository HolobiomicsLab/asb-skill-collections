---
name: molecular-transformation-frequency-filtering
description: Use when after clustering pairwise mass differences into transformation groups from FT-ICR MS formula-assigned datasets, apply this skill when you have a catalog of transformation pairs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MoleTrans
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moletrans_cq
    doi: 10.1021/acs.estlett.5c00284
    title: MoleTrans
  dedup_kept_from: coll_moletrans_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.estlett.5c00284
  all_source_dois:
  - 10.1021/acs.estlett.5c00284
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-transformation-frequency-filtering

## Summary

Filter spurious mass-difference transformations from formula-assigned DOM datasets by applying occurrence-frequency thresholds to retain only recurring transformation pairs. This step removes noise and focuses the reactomics network on biologically or chemically meaningful molecular modifications.

## When to use

After clustering pairwise mass differences into transformation groups from FT-ICR MS formula-assigned datasets, apply this skill when you have a catalog of transformation pairs (e.g., mass shifts with associated formula pairs and co-occurrence counts) and need to distinguish real metabolic or chemical transformations from random or one-off mass differences introduced by measurement error or data artifacts.

## When NOT to use

- Input is already a validated transformation network with known biological transitions (e.g., KEGG or pathway-curated transformations); filtering by frequency alone may remove rare but genuine modifications.
- Dataset contains inherently sparse transformations (e.g., single-sample or small pilot studies with few replicates); arbitrary frequency cutoffs will eliminate signal before sufficient replication can establish recurrence.
- Transformation pairs are already pre-filtered by expert annotation or orthogonal validation (e.g., verified by NMR or stable isotope experiments); additional frequency filtering risks redundant loss of information.

## Inputs

- transformation pair table (mass difference, formula pair, co-occurrence count, transformation type label)
- occurrence frequency vector for each transformation pair
- minimum frequency threshold parameter

## Outputs

- filtered transformation network (mass differences, formula pairs, transformation types, frequency counts)
- transformation pairs passing frequency filter
- removal log (mass differences below threshold)

## How to apply

Compute occurrence frequency for each transformation pair (mass difference + pair of formulas) across all samples or replicates in the dataset. Set a minimum occurrence threshold (e.g., observed in ≥2 samples, or frequency count ≥ cutoff value) based on your experimental design and noise profile. Retain only transformation pairs that meet or exceed this threshold. The rationale is that genuine transformations (functional group modifications, metabolic intermediates) will recur consistently, whereas spurious mass differences are typically one-time noise artifacts. Export the filtered transformation network containing only high-confidence pairs, their mass differences, formula assignments, transformation type labels, and final frequency counts.

## Related tools

- **MoleTrans** (browser-based webtool implementing post-analysis and frequency-based filtering on formula-assigned FT-ICR MS datasets; provides source code for transformation pair calculation and filtering algorithms) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Retained transformation pairs exhibit recurrence frequency ≥ the specified minimum threshold; no pair passes that violates the cutoff.
- Filtered network size is consistent with expected biological complexity (e.g., 10–100s of high-confidence transformations in typical DOM reactomics studies); extreme retention or loss suggests threshold miscalibration.
- Mass differences in retained pairs match known metabolic or environmental transformations (e.g., +15 for CH₃, +45 for CHO₂, −18 for H₂O loss) or are laboratory-specific functional group modifications; novel mass shifts should be manually verified.
- Removal of low-frequency pairs reduces measurement noise without eliminating rare genuine transformations; compare filtered vs. unfiltered network topology (e.g., connectivity, clustering) for interpretability gain.
- Frequency distribution of retained transformations is inspected for biological plausibility: genuine transformations typically show unimodal or clustered frequency patterns, not uniform random distribution.

## Limitations

- Frequency threshold choice is data-dependent and not universally optimal; threshold must be tailored to replication depth, sample size, and expected transformation rarity in the specific environmental system.
- Single occurrence cutoff may fail to capture rare but mechanistically important transformations in heterogeneous or time-series datasets; consider conditional thresholds based on sample type or time point.
- Filtering is blind to chemical or biological context; mass differences that happen to recur may be artifacts (e.g., systematic calibration shifts or adducts) rather than true molecular transformations.
- No built-in recovery mechanism for filtered pairs; if threshold is too stringent, valuable signal is lost irretrievably. Recommend archiving unfiltered intermediate tables and documenting threshold rationale.

## Evidence

- [other] Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences.: "Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences."
- [other] Count frequency and co-occurrence of each transformation pair within the sample.: "Count frequency and co-occurrence of each transformation pair within the sample."
- [other] MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS: "MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS"
- [other] Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts.: "Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts."

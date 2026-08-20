---
name: unannotated-feature-characterization
description: Use when you have aligned feature tables from LC–MS/MS, corresponding
  in silico annotations (from GNPS/ISDB or SIRIUS), and metadata describing sample
  origin. Use it to rank extracts by the proportion of sample-specific, unannotated
  features—a proxy for structural novelty.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - MZmine2/MZmine3
  - SIRIUS
  - Ion Identity
  - Inventa
  techniques:
  - LC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Unannotated Feature Characterization

## Summary

Quantify and prioritize unannotated metabolomic features within natural extracts by computing specificity-based ratios and filtering annotations against curated thresholds. This skill identifies novel chemical signals that lack structural database matches, enabling prioritization of samples with high novelty potential.

## When to use

Apply this skill when you have aligned feature tables from LC–MS/MS, corresponding in silico annotations (from GNPS/ISDB or SIRIUS), and metadata describing sample origin. Use it to rank extracts by the proportion of sample-specific, unannotated features—a proxy for structural novelty. Typical triggers: (1) screening natural product libraries for bioactive leads; (2) identifying extracts enriched in rare metabolites; (3) computing a Feature Component score as part of a composite novelty index (Inventa Priority Score).

## When NOT to use

- Input is already a pre-computed novelty or FC score — skip re-computation to avoid redundancy.
- Annotation results are unavailable or highly incomplete (>70% unaligned features) — FC becomes uninformative as it collapses to near-universal high values.
- Extract set contains <3 samples — feature specificity thresholds (e.g., 90%) become unrepresentative; consider lowering min_specificity or using absolute occurrence counts instead.

## Inputs

- Quantitative feature table (MZmine2 or MZmine3 format: peak area, row m/z, row retention time columns)
- Metadata table (GNPS format with ATTRIBUTE_Species, ATTRIBUTE_Organe, sample identifiers)
- Annotation results (timaR ISDB output and/or SIRIUS compound_identification.tsv)
- Ion Identity grouping results (optional, to collapse redundant features)

## Outputs

- Per-sample Feature Component (FC) ratio (0–1 scale)
- Feature annotation status table (annotated vs. unannotated, per-feature specificity scores)
- Feature-level breakdown (m/z, retention time, count in samples, specificity, annotation status)
- Ranked sample list by FC and optional Priority Score (if LC, CC, SC components included)

## How to apply

Load quantitative feature tables (peak area, m/z, retention time from MZmine2/3) and filter annotations by quality thresholds: ppm_error ≤5 ppm (ISDB), cosine score ≥0.7, shared_peaks ≥10, min_score_final ≥0.0 (ISDB); min_ZodiacScore ≥0.9, min_ConfidenceScore ≥0.0 (SIRIUS). For each feature, compute specificity as the proportion of samples in the extract set where it is present; retain only features exceeding min_specificity (e.g., 90%). Mark features as annotated or unannotated based on filtered annotation results, optionally applying Ion Identity grouping to collapse redundant adducts/isotopologues. For each sample, calculate the Feature Component (FC) as: (count of specific, unannotated features) / (total features in sample). Output per-sample FC ratio (range 0–1), component breakdown, and ranked sample list. Rationale: high FC indicates extracts enriched in sample-unique metabolites lacking database coverage, suggesting higher chemical novelty potential.

## Related tools

- **MZmine2/MZmine3** (Feature detection, alignment, and quantification; exports peak area, m/z, and retention time tables required as input)
- **timaR** (Taxonomically informed annotation weighting; filters ISDB annotations by ppm_error, shared_peaks, cosine score, and final score thresholds) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **SIRIUS** (In silico metabolite annotation; generates compound_identification.tsv with ZodiacScore and ConfidenceScore for filtering) — https://bio.informatik.uni-jena.de/software/sirius/
- **Ion Identity** (Optional feature grouping to collapse redundant adducts and isotopologues, reducing total feature count before specificity computation) — https://github.com/luigiquiros/inventa
- **Inventa** (Complete workflow implementation: loads filtered annotations, computes per-feature specificity, calculates FC per sample, and optionally combines with LC, CC, SC into Priority Score) — https://github.com/luigiquiros/inventa

## Examples

```
From the inventa README/workflow: Set min_specificity=90, ppm_error=5, shared_peaks=10, cosine=0.7, min_ZodiacScore=0.9, then run the Inventa Jupyter notebook after loading MZmine quantitative table, metadata (GNPS format), and ISDB/SIRIUS annotation files. Output includes per-sample FC values and ranked extract list by novelty potential.
```

## Evaluation signals

- FC values for all samples fall in the valid range [0, 1] and sum of component counts matches total feature count per sample.
- Features marked 'unannotated' have zero matches in filtered ISDB/SIRIUS results; annotated features have at least one match passing all cutoffs (ppm_error, shared_peaks, cosine, ZodiacScore, ConfidenceScore).
- Specificity scores match expected proportions: a feature present in N out of M samples has specificity = 100×N/M; features below min_specificity threshold are excluded from FC computation.
- FC rank correlates with expected novelty: samples with highest FC contain rare, extract-specific, unannotated metabolites; low-FC samples are dominated by shared, annotated features.
- Reproducibility check: rerunning the workflow with identical parameters and annotation cutoffs produces identical FC values and sample rankings.

## Limitations

- FC is sensitive to annotation quality and threshold choice (ppm_error, cosine, min_score_final, ZodiacScore, min_ConfidenceScore). Overly strict thresholds inflate unannotated counts and FC; lenient thresholds reduce both. Practitioners must validate thresholds against their instrument, library, and chemical context.
- Feature specificity (min_specificity = 90%) may be unachievable in very small extract sets (<3–5 samples) or in highly diverse libraries; consider absolute feature occurrence counts or lower thresholds in such cases.
- FC does not account for the biological/chemical plausibility of unannotated features (e.g., noise, adducts, fragments). Ion Identity grouping partially mitigates this but may not eliminate all redundancy.
- Sample-level confounders (extraction method, sample mass, storage, instrument settings) can inflate or deflate feature counts independently of chemical diversity, biasing FC rankings.
- High FC does not guarantee novel chemistry: unannotated features may represent known metabolites absent from the annotation library rather than truly novel compounds. Orthogonal validation (NMR, isolation, bioassay) is required.

## Evidence

- [other] The Feature Component is computed as the ratio of the number of specific non-annotated features to the total number of features for each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."
- [other] Load quantitative feature table from MZmine2 or MZmine3 with peak area, m/z, and retention time columns.: "MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2 or MZmine 3"
- [other] Filter ISDB annotations by ppm_error (5 ppm), shared_peaks (10), cosine score (0.7), and min_score_final threshold; filter SIRIUS by min_ZodiacScore (0.9) and min_ConfidenceScore (0.0).: "For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks"
- [other] Compute feature specificity as the proportion of samples where a feature is present; retain features exceeding min_specificity threshold (90%).: "Feature_component min_specificity = 90 # minimun feature specificity to consider"
- [other] Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
- [methods] For each sample, calculate FC as (count of specific non-annotated features) / (total features in sample).: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."

---
name: metabolite-annotation-integration-across-databases
description: Use when you have MZmine-aligned features with m/z and retention time, and you have generated spectral annotations from two or more database sources (e.g., GNPS/ISDB spectral matching and SIRIUS in silico structure elucidation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - SIRIUS
  - CANOPUS
  - MZmine2/MZmine3
  - Inventa
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
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
---

# metabolite-annotation-integration-across-databases

## Summary

Integrate and filter metabolite annotations from multiple in silico sources (ISDB via timaR, SIRIUS/CANOPUS) using quality thresholds and Ion Identity grouping to reduce redundancy and assign confidence-ranked structural annotations to mass spectrometry features. This skill underpins novelty scoring and chemical class discovery in natural product metabolomics.

## When to use

You have MZmine-aligned features with m/z and retention time, and you have generated spectral annotations from two or more database sources (e.g., GNPS/ISDB spectral matching and SIRIUS in silico structure elucidation). You need a unified, high-confidence annotation table that harmonizes conflicting assignments, applies source-specific quality cutoffs, and optionally collapses redundant ion forms before downstream feature-level or sample-level metrics (e.g., Feature Component, chemical class assignment) are computed.

## When NOT to use

- Input features have not yet been aligned or feature-grouped by MZmine; integrate alignment first.
- You have only a single annotation source; this skill is designed for multi-source reconciliation and is overkill if only ISDB or only SIRIUS is available.
- Your analysis goal does not require novelty ranking or chemical class discovery; simple feature annotation without downstream priority scoring may not justify parameter tuning overhead.

## Inputs

- Quantitative feature table (MZmine2/MZmine3 format: peak area, row m/z, row retention time)
- timaR reponderated output (ISDB spectral library matches with ppm_error, shared_peaks, cosine, score fields)
- SIRIUS compound_identification.tsv (structure predictions with ZodiacScore, ConfidenceScore)
- Ion Identity grouping file (optional; MZmine output mapping redundant m/z to consensus features)
- CANOPUS NPC summary (for optional class-level validation post-integration)

## Outputs

- Unified annotation table (feature ID, m/z, retention time, annotation status, source, score, compound name)
- Annotation filtering summary (pass/fail counts per filter per source)
- Ion Identity consensus map (if grouping applied; redundant m/z → consensus feature)
- Annotated vs. unannotated feature list (for Feature Component and class novelty assessment)

## How to apply

Load filtered timaR output (ISDB spectral library matches) and SIRIUS compound_identification.tsv in parallel. For ISDB annotations, apply ppm_error (typically 5 ppm), shared_peaks count (e.g., ≥10), cosine similarity (e.g., ≥0.7), and min_score_final thresholds according to user confidence requirements. For SIRIUS annotations, filter by min_ZodiacScore (e.g., ≥0.9) and min_ConfidenceScore thresholds. Optionally apply Ion Identity grouping from MZmine output to collapse redundant m/z features (e.g., adducts, isotopes) into single consensus features before annotation, reducing false positives in downstream specificity and novelty calculations. Merge the filtered annotation sets and flag each feature as annotated or unannotated. Output a per-feature annotation table with source, score, and annotation status for use in Feature Component, Class Component (via CANOPUS), and Literature Component calculations.

## Related tools

- **timaR** (Perform taxonomically-informed spectral library matching (ISDB) and generate reponderated annotation scores for Feature Component filtering.) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **SIRIUS** (Generate in silico structure predictions and confidence scores; produce compound_identification.tsv for integration with ISDB results.) — https://bio.informatik.uni-jena.de/software/sirius/
- **CANOPUS** (Assign chemical taxonomy (NPC classes) to features post-annotation for Class Component computation.) — https://bio.informatik.uni-jena.de/software/sirius/
- **MZmine2/MZmine3** (Perform feature alignment and export Ion Identity grouping; provide quantitative feature table and m/z alignment for annotation mapping.)
- **Inventa** (Orchestrate annotation integration and compute Feature Component, Literature Component, Class Component, and Similarity Component using integrated annotation results.) — https://github.com/luigiquiros/inventa

## Examples

```
# Load and integrate ISDB (timaR) and SIRIUS annotations in Inventa notebook
ppm_error = 5
shared_peaks = 10
cosine = 0.7
min_score_final = 0.0
min_ZodiacScore = 0.9
min_ConfidenceScore = 0.0
# Then call Inventa's annotation integration function:
from inventa import integrate_annotations
annotation_table = integrate_annotations(
    isdb_file='tima_results.tsv',
    sirius_file='sirius_compound_identification.tsv',
    ion_identity_file='ion_identity_grouping.txt',
    ppm_error=ppm_error, shared_peaks=shared_peaks, cosine=cosine,
    min_score_final=min_score_final, min_ZodiacScore=min_ZodiacScore,
    min_ConfidenceScore=min_ConfidenceScore
)
```

## Evaluation signals

- Verify that all features in the input quantitative table are mapped to annotation table rows (feature ID match); check for missing or unmapped features.
- Confirm filter step counts: e.g., 'ISDB: 1500 candidates → 800 pass ppm_error → 600 pass shared_peaks → 450 pass cosine → 380 pass min_score_final' (or similar decreasing counts); if counts are flat, review parameter settings.
- If Ion Identity grouping applied, verify that all redundant m/z within each group carry the same consensus annotation; conflicting annotations within a group signal inconsistent data or parameter tuning needed.
- Compare per-feature annotation source distribution (e.g., 40% ISDB-only, 25% SIRIUS-only, 20% both, 15% unannotated) against expected biological diversity and instrument accuracy; skewed distributions may indicate overly strict or lax thresholds.
- Spot-check 10–20 randomly selected annotated features: manually verify that m/z error, shared peak count, and cosine score values fall within expected ranges for the set thresholds (e.g., cosine 0.7–1.0, ppm_error < 5).

## Limitations

- Integration accuracy depends critically on ppm_error and shared_peaks thresholds; no universal defaults exist across different instrument types and acquisition modes. Threshold tuning requires domain knowledge and may need pilot validation against reference standards.
- SIRIUS in silico predictions scale computationally with number of features and may fail or time out on very large datasets; pre-filtering by abundance or specificity is recommended before running SIRIUS.
- Ion Identity grouping assumes correct m/z calibration and feature detection; systematic calibration drift or peak-picking artifacts will propagate through grouping and produce spurious consensus annotations.
- Multi-source agreement is not enforced; conflicts between ISDB and SIRIUS predictions are not flagged or resolved, leaving ambiguous features for downstream interpretation.
- Taxonomic and chemical ontology alignment (Lotus Database NPClassifyre vs. SIRIUS Classifyre) requires manual validation; reported incompatibilities may lead to misclassified chemical classes in downstream components.

## Evidence

- [other] For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks between the MS2 experimental and MS2 fro, the database, to consider an annotation valable cosine = 0.7 # min cosine score to consider an annotation valable: "Filter ISDB annotations by ppm_error (e.g., 5 ppm), shared_peaks (e.g., 10), cosine score (e.g., 0.7), and min_score_final threshold"
- [other] filter SIRIUS annotations by min_ZodiacScore (e.g., 0.9) and min_ConfidenceScore (e.g., 0.0) according to user preference: "filter SIRIUS annotations by min_ZodiacScore (e.g., 0.9) and min_ConfidenceScore (e.g., 0.0) according to user preference"
- [other] Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features.: "Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features"
- [other] tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.: "timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation."
- [other] Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "Lotus Database uses the NPClassifyre ontology and Sirius uses the Classifyre ontology"

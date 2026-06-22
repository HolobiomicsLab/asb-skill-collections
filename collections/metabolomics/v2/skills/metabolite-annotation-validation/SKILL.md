---
name: metabolite-annotation-validation
description: Use when after running in silico annotation tools (SIRIUS, ISDB) or spectral library matching on your feature table, when you need to retain only annotations meeting a minimum confidence threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - SIRIUS
  - ISDB
  - timaR
  - Inventa
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans: []
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-validation

## Summary

Apply confidence score filtering to retain only high-quality metabolite annotations from spectral databases (SIRIUS, ISDB) and library matching, using tool-specific thresholds (e.g., ZodiacScore ≥0.9, cosine similarity ≥0.7) to remove low-confidence rows from annotation tables before downstream analysis.

## When to use

After running in silico annotation tools (SIRIUS, ISDB) or spectral library matching on your feature table, when you need to retain only annotations meeting a minimum confidence threshold. Apply this skill before calculating annotation-dependent metrics (Feature Component, Class Component) or before exporting annotations for biological interpretation, to prevent false positives from inflating novel compound counts or misleading chemical class assignments.

## When NOT to use

- Do not apply if annotation tables have already been pre-filtered by the source tool and you lack parameter metadata; re-filtering risks creating a compound filter that is opaque to downstream users.
- Do not use if your downstream analysis requires uncertain or low-confidence annotations as negative controls or for sensitivity analysis; filtering removes this ground truth.
- Do not apply if you are performing a method comparison study where consistent treatment of all annotation qualities (high and low confidence) is required.

## Inputs

- SIRIUS compound_identification.tsv (containing Zodiac score, Cosmic score, and ConfidenceScore columns)
- ISDB/spectral library annotation table (containing cosine score, shared peaks count, ppm error, and final score columns)
- Configuration parameters: min_ZodiacScore, min_ConfidenceScore, min_score_final, cosine threshold, shared_peaks threshold, ppm_error tolerance

## Outputs

- Filtered annotation table (TSV format, same schema as input, subset of rows passing all threshold criteria)
- Row count statistics (original vs. retained rows per annotation source)

## How to apply

Load the annotation table (TSV format, e.g., compound_identification.tsv from SIRIUS or ISDB output) and configure tool-specific filters: for SIRIUS annotations apply min_ZodiacScore threshold (default 0.9) to retain only rows where Zodiac score ≥0.9; optionally layer min_ConfidenceScore (default 0.0). For ISDB/spectral library annotations, apply min_score_final (default 0.0), cosine score ≥0.7, shared_peaks ≥10, and ppm_error ≤5 ppm to filter low-quality matches. Apply filters sequentially in order (ppm → shared_peaks → cosine → score thresholds) to avoid redundant computation. Write the filtered output to a new TSV, retaining all original columns for passing rows. Validate by verifying output row count is ≤ input row count and spot-checking that all retained rows meet specified thresholds.

## Related tools

- **SIRIUS** (Generates in silico molecular formula and structure annotations with Zodiac and Cosmic confidence scores; output is filtered by min_ZodiacScore threshold to retain only high-confidence identifications) — https://bio.informatik.uni-jena.de/software/sirius/
- **ISDB** (Provides spectral library matching annotations with cosine similarity scores, shared peak counts, and ppm error estimates; annotations are filtered by cosine, shared_peaks, ppm_error, and min_score_final thresholds)
- **timaR** (Performs weighted in silico annotation and taxonomically informed reponderation of ISDB results; output is filtered downstream using the same filter parameters applied to ISDB annotations) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **Inventa** (Consumes filtered annotation tables as input to Feature Component and Class Component calculations; filtering ensures only validated annotations contribute to originality scoring) — https://github.com/luigiquiros/inventa

## Examples

```
# Load SIRIUS annotations and filter by min_ZodiacScore
df = pd.read_csv('compound_identification.tsv', sep='\t')
df_filtered = df[df['ZodiacScore'] >= 0.9]
df_filtered.to_csv('compound_identification_filtered.tsv', sep='\t', index=False)
# OR in Inventa: min_ZodiacScore = 0.9; min_ConfidenceScore = 0.0; cosine = 0.7; shared_peaks = 10; ppm_error = 5
```

## Evaluation signals

- Output file contains only rows where min_ZodiacScore (SIRIUS) or all of {cosine, shared_peaks, ppm_error, min_score_final} (ISDB) criteria are met; spot-check 5–10 rows to confirm
- Output row count is strictly less than or equal to input row count; equality is acceptable only if all input rows already met thresholds
- All original annotation columns are present in output; no columns were dropped or reordered
- Filtering produces ≥1 passing rows (non-empty output table); empty output signals over-aggressive thresholding and should trigger parameter review
- When applied to same input multiple times with identical parameters, output is byte-identical (deterministic filtering)

## Limitations

- Threshold choices (e.g., min_ZodiacScore=0.9, cosine=0.7) are heuristic and may require optimization for your specific instrument, ionization mode, or organism type; no principled derivation is provided in the article.
- Sequential filtering (ppm → shared_peaks → cosine → score) may create rank-dependent artifacts if thresholds are poorly calibrated; tight coupling between parameters can amplify filtering stringency unpredictably.
- No adjustment for multiple hypothesis testing or false discovery rate control across annotation sources; filtering operates independently on SIRIUS vs. ISDB, so combined annotation sets may retain systematic biases.
- Low-abundance or rare metabolites with marginal spectral quality may fail thresholds despite biological relevance, leading to false negatives in downstream discovery workflows.

## Evidence

- [other] min_ZodiacScore filtering: "The min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score, removing lower-scoring rows from the"
- [methods] SIRIUS annotation parameters: "Parse the Zodiac score column and apply a minimum threshold filter (min_ZodiacScore = 0.9) to retain only rows where Zodiac score is ≥0.9."
- [other] ISDB/spectral library filters: "ppm_error = 5 # min error in ppm to consider an annotation valable; shared_peaks = 10 # min number of shared peaks; cosine = 0.7 # min cosine score to consider an annotation valable"
- [other] Filter application workflow: "Set annotation cleaning parameters (ppm_error, shared_peaks, cosine, ionisation_mode) For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable"
- [methods] Output format and validation: "Write the filtered annotation table to a new TSV file, retaining all original columns for retained rows. Validation: verify the output file contains only rows with Zodiac score ≥0.9 and row count is"
- [other] timaR integration: "tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation."
- [methods] Downstream use in Inventa: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."

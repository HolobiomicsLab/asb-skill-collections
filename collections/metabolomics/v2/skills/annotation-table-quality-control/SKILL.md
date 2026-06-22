---
name: annotation-table-quality-control
description: Use when after obtaining in silico annotations from SIRIUS (Zodiac/Cosmic scores) or ISDB (cosine/shared peaks metrics), before using the annotation table for Feature Component calculation, chemical class assignment, or metabolite discovery prioritization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SIRIUS
  - CANOPUS
  - Inventa
  - GNPS
  techniques:
  - LC-MS
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

# annotation-table-quality-control

## Summary

Apply confidence-based filtering to annotation tables (SIRIUS/ISDB) to retain only high-confidence molecular identifications meeting specified threshold criteria. This ensures downstream analyses operate on reliable, validated compound annotations by removing low-scoring rows.

## When to use

After obtaining in silico annotations from SIRIUS (Zodiac/Cosmic scores) or ISDB (cosine/shared peaks metrics), before using the annotation table for Feature Component calculation, chemical class assignment, or metabolite discovery prioritization. Apply when annotation scores vary widely and you need to enforce minimum quality standards (e.g., min_ZodiacScore ≥ 0.9 for SIRIUS or cosine ≥ 0.7 for ISDB).

## When NOT to use

- Annotations are already pre-filtered by the annotation tool itself and you have no domain reason to apply stricter thresholds.
- The annotation table contains predominantly high-confidence hits and applying aggressive thresholds would remove too many valid identifications.
- You require all candidate annotations (including low-confidence ones) for comparative or exploratory analysis of annotation uncertainty.

## Inputs

- SIRIUS compound_identification.tsv file with Zodiac, Cosmic, and ConfidenceScore columns
- ISDB annotation table with cosine, shared_peaks, ppm_error, and final_score columns
- Tabular annotation file (TSV/CSV format) from spectral database matching workflow

## Outputs

- Filtered annotation table (TSV format) retaining all original columns for high-confidence rows only
- Row count and filtering statistics (rows retained vs. removed per filter criterion)

## How to apply

Load the annotation table (TSV format with score columns: Zodiac, Cosmic, cosine, shared_peaks, or confidence metrics). Parse and apply multiple filter criteria in sequence: (1) ppm_error ≤ 5 ppm tolerance; (2) shared_peaks ≥ 10 minimum spectral matches; (3) cosine ≥ 0.7 similarity threshold; (4) min_ZodiacScore ≥ 0.9 for SIRIUS annotations; (5) min_ConfidenceScore ≥ 0.0 (or user-defined); (6) min_score_final ≥ 0.0 for ISDB. Retain all original columns for rows passing all thresholds. Validate output by verifying row count ≤ input row count and spot-checking that all retained rows meet the specified thresholds.

## Related tools

- **SIRIUS** (Generates in silico molecular structure predictions with Zodiac and Cosmic confidence scores that are filtered by this skill) — https://bio.informatik.uni-jena.de/software/sirius/
- **CANOPUS** (Produces chemical class predictions downstream of SIRIUS; quality-controlled annotations feed into Class Component calculation)
- **Inventa** (Consumes quality-controlled annotation tables to compute Feature Component and downstream novelty scoring) — https://github.com/luigiquiros/inventa
- **GNPS** (Provides ISDB spectral matching results (cosine, shared_peaks, ppm_error) that are filtered by this skill)

## Examples

```
# Load SIRIUS annotations and apply min_ZodiacScore threshold
import pandas as pd
df = pd.read_csv('compound_identification.tsv', sep='\t')
df_filtered = df[df['ZodiacScore'] >= 0.9]
df_filtered.to_csv('compound_identification_filtered.tsv', sep='\t', index=False)
print(f'Retained {len(df_filtered)} of {len(df)} rows (ZodiacScore >= 0.9)')
```

## Evaluation signals

- Output row count is ≤ input row count; no rows are added, only removed.
- All retained rows in output have Zodiac score ≥ 0.9 (or other specified threshold) with no exceptions.
- All retained rows have shared_peaks ≥ 10 AND cosine ≥ 0.7 AND ppm_error ≤ 5 ppm (if ISDB annotations).
- Output TSV retains all original columns (e.g., compound_name, inchikey, Zodiac, Cosmic, ConfidenceScore); no columns are dropped.
- Filtering statistics report (e.g., '1,247 rows input; 892 rows retained; 355 rows removed by min_ZodiacScore filter') is consistent with manual spot-check of marginal rows.

## Limitations

- Hard thresholds (e.g., min_ZodiacScore = 0.9) may be overly restrictive for samples with naturally low annotation confidence or for rare metabolites with few library matches.
- Threshold values are dataset- and ionization-mode dependent; no universal cutoffs are specified in the article; users must empirically validate thresholds for their specific LC-MS method and sample type.
- Filtering is applied independently to each criterion without accounting for correlations among scores; a row may pass one threshold but fail another unrelated one.
- No changelog or versioning mechanism is documented, making it difficult to track changes in filtering logic or threshold definitions over time across projects.

## Evidence

- [other] min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score, removing lower-scoring rows from the annotation table.: "The min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score, removing lower-scoring rows from the"
- [other] Load SIRIUS annotations file and parse Zodiac score column; apply minimum threshold filter (min_ZodiacScore = 0.9) and optional ConfidenceScore cut-off; write filtered table to TSV retaining all original columns.: "Parse the Zodiac score column and apply a minimum threshold filter (min_ZodiacScore = 0.9) to retain only rows where Zodiac score is ≥ 0.9. 3. Optionally apply the ConfidenceScore cut-off"
- [other] Multiple filter criteria for ISDB annotations: ppm_error = 5 ppm, shared_peaks = 10, cosine = 0.7, min_score_final = 0.0: "ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks cosine = 0.7 # min cosine score to consider an annotation valable min_score_final ="
- [other] Validation step verifies output contains only rows meeting threshold criteria and row count ≤ input.: "Validation: verify the output file contains only rows with Zodiac score ≥ 0.9 and row count is less than or equal to the input row count."
- [other] Configure annotation cleaning parameters including ppm_error, shared_peaks, cosine, and ionisation_mode for cleaning GNPS annotations.: "Set annotation cleaning parameters (ppm_error, shared_peaks, cosine, ionisation_mode) [section=other; evidence='For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an"

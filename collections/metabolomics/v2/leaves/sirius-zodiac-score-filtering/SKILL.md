---
name: sirius-zodiac-score-filtering
description: Use when after running SIRIUS on a mass spectrometry feature set and
  obtaining compound_identification.tsv output containing Zodiac and Cosmic confidence
  scores, apply this filter to eliminate low-confidence SIRIUS annotations before
  downstream prioritization or chemical class analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  tools:
  - SIRIUS
  - INVENTA
  - CANOPUS
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- install Sirius and run it in your set.
- install Sirius and run it in your set
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

# SIRIUS Zodiac Score Filtering

## Summary

Apply a minimum ZodiacScore threshold (default 0.9) to SIRIUS compound annotations to retain only high-confidence structural identifications in metabolomics annotation tables. This confidence-based filtering removes low-scoring rows while preserving all original columns for retained annotations.

## When to use

After running SIRIUS on a mass spectrometry feature set and obtaining compound_identification.tsv output containing Zodiac and Cosmic confidence scores, apply this filter to eliminate low-confidence SIRIUS annotations before downstream prioritization or chemical class analysis. Use when your annotation workflow requires high-stringency structural predictions or when preparing data for the INVENTA prioritization pipeline.

## When NOT to use

- Input annotations are not from SIRIUS (e.g., ISDB or other in silico tools use different confidence metrics)
- Analysis goal requires exploratory examination of all SIRIUS predictions including low-confidence ones
- Zodiac scores are unavailable or missing from the annotation table

## Inputs

- SIRIUS compound_identification.tsv file (tabular format with Zodiac and Cosmic score columns)
- min_ZodiacScore threshold parameter (numeric, default 0.9)
- min_ConfidenceScore threshold parameter (numeric, optional, default 0.0)

## Outputs

- Filtered annotation table (TSV format)
- High-confidence SIRIUS annotations (rows with Zodiac score ≥ min_ZodiacScore)
- Annotation row count (reduced relative to input)

## How to apply

Load the SIRIUS annotations file (compound_identification.tsv format) into a tabular parser and extract the Zodiac score column. Apply a minimum threshold filter (min_ZodiacScore = 0.9 by default) to retain only rows where the Zodiac score is ≥ 0.9. Optionally apply an additional ConfidenceScore cut-off (min_ConfidenceScore = 0.0 by default) as a secondary filter criterion. Write the filtered annotation table to a new TSV file, retaining all original columns for the retained rows. The rationale is that ZodiacScore reflects SIRIUS's molecular formula and structure ranking confidence; a threshold of 0.9 operationalizes a conservative confidence cutoff standard in natural products metabolomics.

## Related tools

- **SIRIUS** (Generates compound_identification.tsv with Zodiac scores for structural confidence ranking) — https://bio.informatik.uni-jena.de/software/sirius/
- **INVENTA** (Downstream prioritization pipeline that accepts filtered SIRIUS annotations as optional input for Feature Component calculation) — https://github.com/luigiquiros/inventa
- **CANOPUS** (Complementary SIRIUS output (chemical taxonomy) that may be used in tandem with Zodiac-filtered annotations for class-level analysis) — https://github.com/kaibioinfo/canopus_treemap

## Examples

```
# In INVENTA notebook: min_ZodiacScore = 0.9; then load compound_identification.tsv and filter df = df[df['Zodiac_score'] >= min_ZodiacScore]; df.to_csv('filtered_sirius_annotations.tsv', sep='\t')
```

## Evaluation signals

- Output file contains only rows where Zodiac score ≥ min_ZodiacScore (inspect min value in output Zodiac column)
- Output row count is less than or equal to input row count (no rows added, only removed)
- All original columns retained in output TSV (schema validation: same header as input)
- No NULL or NaN values introduced in retained rows
- Filtered annotation table successfully integrates into INVENTA or downstream chemical class analysis without schema errors

## Limitations

- ZodiacScore threshold is heuristic; optimal cutoff may vary by organism, ionization mode, or MS instrument
- Filtering alone does not validate spectral-to-structure match; relies on SIRIUS's underlying Zodiac ranking algorithm
- If min_ZodiacScore is set too high (e.g., > 0.95), may exclude valid annotations for lower-abundance or ambiguous features
- SIRIUS annotations must have been recomputed or obtained from a version supporting Zodiac scoring; older project spaces may lack this metric

## Evidence

- [other] The min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score, removing lower-scoring rows from the annotation table.: "min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score"
- [other] Load the SIRIUS annotations file (compound_identification.tsv format) containing Zodiac and Cosmic scores using a tabular file reader. Parse the Zodiac score column and apply a minimum threshold filter (min_ZodiacScore = 0.9) to retain only rows where Zodiac score is ≥ 0.9. Optionally apply the ConfidenceScore cut-off (min_ConfidenceScore = 0.0 by default) as an additional filter criterion if present. Write the filtered annotation table to a new TSV file, retaining all original columns for retained rows.: "Load the SIRIUS annotations file (compound_identification.tsv format) containing Zodiac and Cosmic scores using a tabular file reader. Parse the Zodiac score column and apply a minimum threshold"
- [other] Verify the output file contains only rows with Zodiac score ≥ 0.9 and row count is less than or equal to the input row count.: "Validation: verify the output file contains only rows with Zodiac score ≥ 0.9 and row count is less than or equal to the input row count"
- [other] min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable: "min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable"
- [readme] Recompute your project space from Sirius using the following code: "Recompute your project space from Sirius using the following code"

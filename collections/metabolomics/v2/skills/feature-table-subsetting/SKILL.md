---
name: feature-table-subsetting
description: 'Use when after loading an MS-DIAL feature table when you need to separate features into two disjoint groups: one meeting a quantitative threshold (e.g., m/z decimal values outside [4, 8], coefficient of variation below a cutoff, or mass defects within acceptable bounds) and one not meeting it.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - margheRita
  - MS-Dial
  - OUKS
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
- doi: 10.1021/acs.jproteome.1c00392
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-subsetting

## Summary

Partition a feature table into two complementary subsets based on a filtering criterion (e.g., m/z decimal values, mass defects, or coefficient of variation), retaining both the filtered-out and retained features for separate downstream analysis. This skill is essential in untargeted metabolomics to isolate features meeting quality or chemical criteria while preserving rejected features for audit trails and alternative interpretations.

## When to use

Apply this skill after loading an MS-DIAL feature table when you need to separate features into two disjoint groups: one meeting a quantitative threshold (e.g., m/z decimal values outside [4, 8], coefficient of variation below a cutoff, or mass defects within acceptable bounds) and one not meeting it. Use it when your downstream analysis depends on feature quality flags and you want to preserve both subsets for reporting, validation, or downstream decision-making.

## When NOT to use

- Input is already a pre-filtered feature table with no rejected features retained.
- You require features to be ranked or continuously scored rather than partitioned into discrete groups.
- The filtering criterion is unstable or depends on iterative re-estimation (e.g., adaptive thresholding); use model-based selection instead.

## Inputs

- Feature table from MS-DIAL (with m/z values, retention times, and intensities)
- Feature metadata (e.g., mass-to-charge ratios, decimal parts, or quality metrics)
- Filtering criterion (logical threshold or range definition)

## Outputs

- Subset of features meeting the filter criterion (e.g., 548 appropriate features)
- Subset of features failing the filter criterion (e.g., 56 inappropriate features)
- Summary report (count, percentage, feature identifiers for each subset)

## How to apply

Load the feature table (including m/z values, intensities, or metadata) from MS-DIAL output into R. Extract or compute the filtering attribute for each feature (e.g., m/z decimal part via modulo operation, CV from QC replicates, or mass defect). Define the classification criterion as a logical condition (e.g., decimal m/z in [4, 8] = inappropriate). Partition the feature table into two subsets: one where the condition is TRUE (inappropriate/rejected features) and one where it is FALSE (appropriate/retained features). Return both subsets as separate data structures and a summary report (counts, percentages, feature lists) documenting the split. The rationale is to enable traceability and allow users to review rejected features without data loss.

## Related tools

- **margheRita** (R package providing m_z_filtering() and related subset/partition functions for MS-DIAL feature tables) — https://github.com/emosca-cnr/margheRita
- **R** (Scripting language for implementing feature table subsetting logic and modulo operations)
- **MS-Dial** (Source instrument-agnostic peak-picking and feature detection software; outputs the feature table to be subsetted) — http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/

## Examples

```
# In R using margheRita: result <- m_z_filtering(feature_table, decimal_range = c(4, 8)); appropriate_features <- result$retained; inappropriate_features <- result$excluded; summary(result)
```

## Evaluation signals

- Sum of feature counts in both subsets equals the total input feature count (no features lost or duplicated).
- Each feature appears in exactly one subset (subsets are disjoint and exhaustive).
- Features in the 'inappropriate' subset all satisfy the filter criterion (e.g., m/z decimal in [4, 8]); features in the 'appropriate' subset do not.
- Summary report counts and percentages are internally consistent (e.g., 56 + 548 = 604 total; 56/604 ≈ 9.3%).
- No features are missing from the output (feature identifiers in both subsets account for all input feature IDs).

## Limitations

- Subsetting is deterministic and threshold-based; if the threshold is misspecified or dataset-dependent, the split may be inappropriate for downstream analysis.
- The skill does not validate whether the filtering criterion is biologically meaningful or statistically justified—it only mechanically partitions based on the given rule.
- If features have missing or malformed metadata (e.g., null m/z values), the classification may fail or require imputation; the article does not specify how to handle missing data in subsetting.

## Evidence

- [other] Step 4 of workflow: 'Separate the feature set into two subsets: 548 features with appropriate m/z values and 56 features with inappropriate m/z values.': "Separate the feature set into two subsets: 548 features with appropriate m/z values and 56 features with inappropriate m/z values."
- [other] Filter description: 'The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default. When applied to the dataset, this filter excluded 56 features with inappropriate m/z values while retaining 548 features with appropriate m/z values.': "The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default. When applied to the dataset, this filter excluded 56 features with inappropriate m/z"
- [other] Workflow step 3: 'Classify features as inappropriate if the decimal part lies within [4,8]; otherwise mark as appropriate.': "Classify features as inappropriate if the decimal part lies within [4,8]; otherwise mark as appropriate."
- [readme] README introduction: 'runs filters to exclude features/sample with many missing values, features with wrong m/z values': "runs filters to exclude features/sample with many missing values, features with wrong m/z values"
- [readme] README feature list: 'filtering by mass defects, filtering by coefficient of variation (samples vs QCs)': "filtering by mass defects, filtering by coefficient of variation (samples vs QCs)"

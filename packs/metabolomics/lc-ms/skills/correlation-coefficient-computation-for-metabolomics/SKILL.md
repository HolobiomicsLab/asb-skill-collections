---
name: correlation-coefficient-computation-for-metabolomics
description: Use when you have an aligned LCMS feature table (output from Eclipse or equivalent alignment tool) and need to identify candidate redundant features for clustering. It is most useful when features are suspected to originate from the same metabolite (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Eclipse
  - Gravity
  - bmxp (Python package)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- pip install bmxp
- They are written in Python and C
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compute pairwise Pearson correlation coefficients for LCMS feature intensity profiles

## Summary

Quantify co-variation between LCMS features by computing pairwise Pearson correlation coefficients across their intensity profiles in a sample cohort. This metric serves as a primary criterion for identifying redundant or related features in nontargeted metabolomics workflows.

## When to use

Apply this skill when you have an aligned LCMS feature table (output from Eclipse or equivalent alignment tool) and need to identify candidate redundant features for clustering. It is most useful when features are suspected to originate from the same metabolite (e.g., isotopologs, adducts, in-source fragments, or artifacts) and exhibit similar intensity patterns across samples.

## When NOT to use

- Input feature table is not aligned or contains missing values without imputation — Pearson correlation requires complete intensity vectors.
- Samples have extreme batch effects or drift not corrected by upstream tools — correlation will be inflated by technical variation rather than biological co-abundance.
- Feature intensities are not on comparable scales across samples — normalization must be applied before correlation computation.

## Inputs

- Aligned LCMS feature table (Eclipse output or equivalent) containing retention times (RT) and feature intensities across injections
- Feature intensity matrix (Compound_ID × injection_id pivot table)
- Correlation threshold parameter (default or user-specified cutoff, e.g., 0.7)

## Outputs

- Pairwise Pearson correlation coefficient matrix (Feature × Feature)
- Feature pairs exceeding correlation threshold, annotated with correlation values
- Candidate redundant feature pairs (input to Gravity clustering step)

## How to apply

Load the aligned LCMS feature table containing feature intensities normalized across all injections (samples). For each pair of features, extract their intensity vectors and compute the Pearson correlation coefficient using the full sample cohort. Features with correlation values exceeding a user-defined threshold (typically > 0.7 or higher, depending on stringency) are marked as candidate pairs for downstream clustering. The correlation matrix serves as input to the Gravity module's retention-time proximity and correlation-based merging logic, where both retention time proximity and correlation thresholds must be satisfied to cluster features into a single group.

## Related tools

- **Eclipse** (Upstream alignment module that produces the aligned LCMS feature table required as input to correlation computation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Downstream clustering module that uses correlation coefficients alongside retention time proximity to group redundant features into clusters) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **bmxp (Python package)** (Parent metabolomics processing platform providing shared schema (bmxp.FMDATA, bmxp.IMDATA) and standalone correlation computation routines) — https://github.com/broadinstitute/bmxp

## Evaluation signals

- Correlation matrix is symmetric and has diagonal values equal to 1.0 (self-correlation).
- All correlation values fall within the range [-1, 1].
- Feature pairs identified as highly correlated (above threshold) exhibit overlapping retention times within the Gravity RT window, supporting biological plausibility.
- Redundant feature pairs (e.g., confirmed isotopologs or known adducts) are present in the high-correlation candidate set.
- Correlation values are reproducible across repeated runs with the same input feature table and threshold.

## Limitations

- Pearson correlation assumes linear relationships; co-abundant features with nonlinear intensity patterns may be missed.
- Correlation is computed across the entire sample cohort; subgroup-specific co-abundance patterns are not detected.
- Low-abundance features with sparse or noisy intensity profiles may yield unreliable correlation estimates.
- Correlation alone cannot distinguish true redundancy from biological co-abundance; retention time proximity (used in Gravity) is essential for disambiguation.
- Future versions of Gravity may incorporate XIC (extracted ion chromatogram) shape similarity as a complementary metric, potentially reducing reliance on intensity correlation alone.

## Evidence

- [other] Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples.: "Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples."
- [other] Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria: "Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria, with potential future incorporation of XIC shape"
- [other] Group features into clusters by applying retention-time proximity filtering and correlation threshold filtering (only feature pairs exceeding a correlation cutoff are merged).: "Group features into clusters by applying retention-time proximity filtering (features within a defined RT window are candidates for clustering) and correlation threshold filtering (only feature pairs"
- [other] Load aligned LCMS feature table (from Eclipse output or equivalent input) containing retention times and feature intensities across samples.: "Load aligned LCMS feature table (from Eclipse output or equivalent input) containing retention times and feature intensities across samples."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."

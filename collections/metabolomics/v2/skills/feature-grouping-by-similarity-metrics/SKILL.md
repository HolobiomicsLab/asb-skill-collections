---
name: feature-grouping-by-similarity-metrics
description: Use when after LCMS feature alignment (e.g., Eclipse output) when you have a feature table with retention times and intensity profiles across multiple injections, and you need to collapse redundant features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - bmxp
  - Python
  - Eclipse
  - Gravity
  - Blueshift
  - bmxp (Python package)
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

# feature-grouping-by-similarity-metrics

## Summary

Group redundant LCMS features into clusters using retention time (RT) proximity and Pearson correlation of intensity profiles across samples. This skill reduces feature redundancy in nontargeted metabolomics by identifying and aggregating features that represent the same compound.

## When to use

Apply this skill after LCMS feature alignment (e.g., Eclipse output) when you have a feature table with retention times and intensity profiles across multiple injections, and you need to collapse redundant features (e.g., different ion adducts, in-source fragments, or peak-picking artifacts of the same metabolite) into non-redundant clusters for downstream annotation and quantification.

## When NOT to use

- Input features are already from targeted methods or have been manually deduplicated; Gravity is designed for nontargeted feature tables.
- RT information is missing or unreliable; clustering requires valid retention time values for the RT window filter.
- Feature intensity profiles are too sparse or noisy to compute meaningful Pearson correlations (e.g., features present in <2 samples).

## Inputs

- Aligned LCMS feature table (from Eclipse or equivalent) with columns: Compound_ID (feature index), RT (retention time), MZ (mass-to-charge), and intensity columns for each injection_id
- Feature Metadata (bmxp.FMDATA) containing Compound_ID, RT, MZ, Intensity, and Method
- Feature Abundances (Compound_ID × injection_id pivot table)

## Outputs

- Feature Metadata table with added columns: Cluster_Num (cluster assignment) and Cluster_Size (members per cluster)
- Feature-to-cluster mapping (Compound_ID → Cluster_Num, Cluster_Size)

## How to apply

Load an aligned LCMS feature table containing retention times (RT) and feature intensities across all samples. Compute pairwise Pearson correlation coefficients between all features using their intensity profiles. Apply two-stage filtering: first, restrict candidate feature pairs to those within a defined RT window (retention time proximity criterion), then merge only pairs exceeding a correlation threshold (default behavior inferred from module design). Assign each feature a unique cluster identifier and generate an output table mapping features to cluster numbers and cluster sizes. The correlation-based grouping reflects shared intensity co-variation across samples, while RT windowing ensures features are biochemically plausible co-elutes.

## Related tools

- **Eclipse** (Upstream alignment tool that produces the input feature table with RT and intensity data across samples) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Performs the clustering using RT and correlation; standalone Gravity module) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **Blueshift** (Downstream drift-correction module that uses Gravity-clustered features) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **bmxp (Python package)** (Core framework providing shared schema (FMDATA, IMDATA, SMDATA) and cluster function) — https://github.com/broadinstitute/bmxp

## Examples

```
from bmxp.gravity import cluster; import bmxp; result = cluster(feature_table, rt_window=0.5, correlation_threshold=0.8)
```

## Evaluation signals

- All features in the input table are assigned to exactly one cluster (complete coverage, no orphans).
- Cluster_Num and Cluster_Size columns are populated and consistent: Cluster_Size matches the count of features with that Cluster_Num.
- Features within the same cluster have RT values within the defined RT window and Pearson correlation above the correlation threshold.
- Features in different clusters either differ in RT (beyond window) or have correlation below threshold, confirming clusters are non-overlapping.
- Cluster assignments are stable and reproducible under identical input and parameter settings.

## Limitations

- Gravity does not yet incorporate XIC (extracted ion chromatogram) shape analysis; future versions may refine clustering using peak morphology.
- Clustering relies on intensity co-variation across samples; sparse or low-abundance features may not correlate well, leading to under-clustering.
- RT window and correlation thresholds are user-defined; inappropriate choices can lead to over-clustering (too strict) or under-clustering (too lenient).
- Method assumes aligned features have comparable RT and intensity scales; pre-alignment quality (e.g., Eclipse output) directly affects clustering performance.

## Evidence

- [other] Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria: "Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria, with potential future incorporation of XIC shape"
- [other] Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples: "Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples."
- [other] Group features into clusters by applying retention-time proximity filtering and correlation threshold filtering: "Group features into clusters by applying retention-time proximity filtering (features within a defined RT window are candidates for clustering) and correlation threshold filtering (only feature pairs"
- [readme] Gravity - Cluster redundant LCMS features based on RT and Correlation: "Gravity - Cluster redundant LCMS features based on RT and Correlation (And someday, XIC shape)"
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."

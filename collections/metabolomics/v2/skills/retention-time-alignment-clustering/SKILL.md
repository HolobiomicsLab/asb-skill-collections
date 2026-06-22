---
name: retention-time-alignment-clustering
description: Use when you have two or more nontargeted LCMS feature tables from the same analytical method and need to establish matched feature correspondences across datasets, then consolidate redundant features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - bmxp
  - Python
  - Eclipse
  - Gravity
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

# retention-time-alignment-clustering

## Summary

Align and cluster redundant LCMS features across datasets by combining m/z-based matching with retention-time proximity and correlation filtering. This two-stage approach (Eclipse → Gravity) reduces feature redundancy while preserving distinct chemical entities within co-eluting windows.

## When to use

You have two or more nontargeted LCMS feature tables from the same analytical method and need to establish matched feature correspondences across datasets, then consolidate redundant features. Use this skill when raw feature tables contain duplicate or near-duplicate entries representing the same metabolite, and you need a single unified feature set with cluster membership assigned.

## When NOT to use

- Input datasets are from different LCMS analytical methods or instruments (Eclipse requires same-method inputs)
- Feature tables are already unified and deduplicated (clustering is unnecessary overhead)
- You need to preserve all original features without any merging or deduplication for downstream targeted analysis

## Inputs

- Two or more nontargeted LCMS feature tables (same analytical method) in tabular format with m/z, retention time, and intensity values
- Feature metadata table (Compound_ID, RT, MZ, Intensity columns per bmxp.FMDATA schema)
- Feature abundances pivot table (Compound_ID × injection_id with intensity values)

## Outputs

- Matched feature correspondence table linking features across datasets with alignment confidence scores (Eclipse output)
- Cluster assignment table with unique cluster identifiers and feature-to-cluster mapping (Gravity output)
- Updated feature metadata with Cluster_Num and Cluster_Size columns

## How to apply

First, load aligned feature tables (m/z, retention time, intensity values) into the Eclipse module to perform m/z-based matching with a defined tolerance threshold, then refine candidate matches using retention-time-based clustering within co-eluting windows to produce matched feature correspondence with alignment confidence scores. Next, supply the Eclipse output (or equivalent aligned table) to the Gravity module: compute pairwise Pearson correlation coefficients across samples for all features, then apply retention-time proximity filtering (features within a defined RT window are clustering candidates) and correlation threshold filtering (only feature pairs exceeding a correlation cutoff are merged) to assign each feature a unique cluster identifier. The rationale is that true redundant features should be co-eluting (RT proximity) AND show correlated abundance patterns (Pearson correlation); combining these criteria reduces false positive merges while respecting the retention-time dimension where chromatographic resolution is meaningful.

## Related tools

- **Eclipse** (Align two or more same-method nontargeted LCMS datasets using m/z and retention-time-based matching to establish feature correspondences across datasets with confidence scores) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Cluster redundant LCMS features by applying retention-time proximity and Pearson correlation filtering to assign cluster membership and produce feature-to-cluster mapping) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **bmxp** (Standalone Python and C metabolomics processing platform providing shared schema (FMDATA, IMDATA, SMDATA) and unified column headers across all modules) — https://github.com/broadinstitute/bmxp

## Examples

```
from bmxp.eclipse import MSAligner
from bmxp.gravity import cluster
aligner = MSAligner(mz_tol=0.01, rt_tol=0.5)
matched = aligner.align(feature_table_1, feature_table_2)
clustered = cluster(matched, rt_window=0.3, corr_threshold=0.8)
```

## Evaluation signals

- Output feature correspondence table from Eclipse contains non-null alignment confidence scores for all matched feature pairs, with no orphaned features
- Gravity cluster assignments are consistent: all features within a cluster have pairwise Pearson correlation ≥ the specified threshold and retention times within the defined RT window
- Feature metadata output includes populated Cluster_Num and Cluster_Size columns; no feature is assigned to multiple clusters
- Total feature count after clustering is less than or equal to the pre-clustering count; redundancy has been reduced without feature loss
- RT-based clusters do not artificially merge features that elute in different chromatographic windows (cross-validation: plot cluster members' intensities across injections and verify co-variation)

## Limitations

- Eclipse requires that input datasets originate from the same analytical method; cross-method dataset alignment will produce spurious matches
- Gravity clustering relies on Pearson correlation across sample abundances; features with sparse or constant intensity profiles may not cluster correctly
- Retention-time windows and correlation thresholds are user-defined parameters; inappropriate values (e.g., overly permissive RT windows) can cause false merges or conversely miss true redundancy
- Gravity clustering does not yet incorporate XIC (extracted ion chromatogram) shape analysis, which could improve discrimination of co-eluting isomers
- The workflow assumes all input feature tables conform to the shared bmxp schema (FMDATA, IMDATA); non-compliant column headers or metadata structures will cause failures or require schema remapping

## Evidence

- [other] Eclipse is a standalone module designed to align two or more same-method nontargeted LCMS datasets: "Eclipse is a standalone module designed to align two or more same-method nontargeted LCMS datasets, functioning as a step in the BMXP processing pipeline written in Python and C for cloud-compatible"
- [other] Apply m/z-based matching with tolerance threshold, then retention-time-based clustering to refine matches: "Apply m/z-based matching with tolerance threshold to identify candidate feature pairs across datasets. 4. Apply retention-time-based clustering to refine candidate matches within co-eluting windows."
- [other] Gravity clusters redundant LCMS features using retention time and correlation as primary criteria: "Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria, with potential future incorporation of XIC shape"
- [other] Compute pairwise Pearson correlation and apply RT proximity and correlation threshold filtering: "Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples. 3. Group features into clusters by applying retention-time proximity filtering"
- [readme] Shared schema with preferred column headers used by all BMXP modules: "All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): * Feature Metadata `bmxp.FMDATA` - Describes the feature. Index"
- [readme] Schema customization via bmxp module configuration: "These can be changed globally so that all packages will use the same terminology. To update the schema, modify the dictionary objects in the module directly prior to running code."

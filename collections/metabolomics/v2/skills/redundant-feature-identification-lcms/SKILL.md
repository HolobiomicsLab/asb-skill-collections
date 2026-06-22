---
name: redundant-feature-identification-lcms
description: Use when after alignment of two or more same-method nontargeted LCMS datasets (e.g., via Eclipse) when you have a feature table containing retention times and feature intensities across samples. Use it when redundancy is expected—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - bmxp
  - Python
  - Eclipse
  - bmxp (Python package)
  - Blueshift
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
---

# Cluster redundant LCMS features by retention time and correlation

## Summary

Gravity identifies and groups redundant LCMS features—those arising from the same compound but detected as distinct entries—by applying retention-time proximity and intensity-correlation filtering. This step reduces false positives in nontargeted metabolomics datasets before annotation and statistical analysis.

## When to use

Apply this skill after alignment of two or more same-method nontargeted LCMS datasets (e.g., via Eclipse) when you have a feature table containing retention times and feature intensities across samples. Use it when redundancy is expected—e.g., multiple ionization adducts, in-source fragments, or instrumental artifacts creating duplicate feature entries for the same metabolite.

## When NOT to use

- Input is already a deduplicated or manually curated feature table with redundancy resolved.
- Features are from different LCMS methods or ionization modes where RT and correlation assumptions do not hold across the cohort.
- Sample cohort is very small (<5 injections) such that Pearson correlation is unstable or not meaningful.

## Inputs

- Feature Metadata table (bmxp.FMDATA): Compound_ID, RT, MZ, Intensity columns
- Feature Abundances table: pivot of Compound_ID × injection_id with abundances
- Retention time tolerance parameter (user-defined; e.g., ±0.05–0.2 min)
- Pearson correlation threshold parameter (e.g., 0.8–0.95)

## Outputs

- Feature Metadata table with appended Cluster_Num column (cluster assignment per feature)
- Feature Metadata table with appended Cluster_Size column (cluster membership count)
- Feature-to-cluster mapping table

## How to apply

Load an aligned LCMS feature table (Feature Metadata + Feature Abundances, indexed by Compound_ID × injection_id) with RT and intensity columns. Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples. Apply two-stage filtering: (1) retention-time proximity—flag features whose RTs fall within a defined window (e.g., ±0.1 min or project-specific tolerance); (2) correlation threshold—merge only feature pairs exceeding a correlation cutoff (typically >0.8–0.9 for high redundancy confidence). Assign each merged group a unique Cluster_Num and record Cluster_Size. The rationale: correlated intensity patterns across samples + close RT values strongly indicate the same underlying compound; clustering reduces statistical noise and improves downstream annotation specificity.

## Related tools

- **Eclipse** (Upstream alignment tool that produces the aligned LCMS feature table consumed by Gravity) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **bmxp (Python package)** (Parent package containing Gravity as a standalone module; provides shared schema (FMDATA, IMDATA, SMDATA) and file I/O) — https://github.com/broadinstitute/bmxp
- **Blueshift** (Downstream drift-correction tool that can operate on Gravity-clustered features) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md

## Examples

```
from bmxp.gravity import cluster; import bmxp; cluster(feature_metadata, feature_abundances, rt_tolerance=0.1, correlation_threshold=0.85)
```

## Evaluation signals

- Cluster_Num is assigned to every feature; no missing or null values in the output table.
- Cluster_Size values are consistent—each feature in a cluster of size N has Cluster_Size = N.
- Features within a cluster differ by ≤ the specified RT tolerance and have Pearson r ≥ the correlation threshold; features assigned to different clusters do not meet both criteria.
- Cluster assignments are deterministic (repeated runs on the same input yield identical results).
- Number of output feature rows equals the number of input feature rows (1:1 mapping; clustering does not remove features, only labels them).

## Limitations

- Pearson correlation assumes linear intensity co-variation and can fail when sample cohort is small (<5 injections) or when true redundancy involves non-linear adduct ionization patterns.
- RT tolerance is user-defined and method-dependent; no automatic or adaptive algorithm is described for selecting it.
- The README notes potential future incorporation of XIC (extracted ion chromatogram) shape analysis, implying current version does not account for peak morphology.
- Assumes Feature Metadata and Feature Abundances tables are already aligned; garbage-in, garbage-out if upstream alignment is poor.

## Evidence

- [readme] Gravity - Cluster redundant LCMS features based on RT and Correlation (And someday, XIC shape): "Gravity - Cluster redundant LCMS features based on RT and Correlation (And someday, XIC shape)"
- [other] Group features into clusters by applying retention-time proximity filtering (features within a defined RT window are candidates for clustering) and correlation threshold filtering (only feature pairs exceeding a correlation cutoff are merged).: "Group features into clusters by applying retention-time proximity filtering (features within a defined RT window are candidates for clustering) and correlation threshold filtering (only feature pairs"
- [other] Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples.: "Compute pairwise Pearson correlation coefficients between all features using their intensity profiles across samples."
- [other] Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria: "Gravity is a standalone module that clusters redundant LCMS features using retention time (RT) and correlation as the primary clustering criteria"
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers.: "All BMXP modules use a shared schema and file formats with our prefered columns headers."

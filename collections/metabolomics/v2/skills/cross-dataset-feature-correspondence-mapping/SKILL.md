---
name: cross-dataset-feature-correspondence-mapping
description: Use when you have two or more nontargeted LCMS feature tables from the
  same analytical method (same column, ionization mode, and acquisition parameters)
  and need to identify which features in one dataset correspond to features in another.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Eclipse
  - Gravity
  - Blueshift
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-dataset-feature-correspondence-mapping

## Summary

Eclipse aligns two or more nontargeted LCMS datasets acquired using the same analytical method to produce matched feature correspondences across datasets. This is a foundational step in the BMXP metabolomics pipeline that enables pooled feature analysis and drift correction across multiple injections or batches.

## When to use

You have two or more nontargeted LCMS feature tables from the same analytical method (same column, ionization mode, and acquisition parameters) and need to identify which features in one dataset correspond to features in another. This is required before performing cross-dataset operations like redundancy clustering (Gravity) or drift correction (Blueshift). Do not use if datasets come from different analytical methods or if you need targeted feature matching.

## When NOT to use

- Input datasets were acquired using different LCMS methods, column types, or ionization modes — Eclipse requires same-method inputs to avoid false correspondences
- Feature tables are already merged or deduplicated — correspondence mapping assumes independent input datasets
- You need targeted feature annotation or database matching rather than cross-dataset alignment

## Inputs

- Two or more nontargeted LCMS feature metadata tables (bmxp.FMDATA schema: Compound_ID, MZ, RT, Intensity, Method)
- Feature abundance pivot tables (Compound_ID × injection_id) if intensity-weighted matching is used
- Injection metadata (bmxp.IMDATA) describing the source dataset for each table

## Outputs

- Matched feature correspondence table linking features across datasets with alignment confidence scores
- Feature pairs indexed by dataset identifiers and original Compound_ID values

## How to apply

Load feature tables containing m/z, retention time (RT), and intensity values in the shared BMXP schema format (index: Compound_ID; columns: MZ, RT, Intensity, Method). Parse and normalize feature metadata distributions across datasets. Apply m/z-based matching with a predefined tolerance threshold to identify candidate feature pairs across datasets. Refine these candidates by applying retention-time-based clustering to retain only co-eluting feature matches within defined RT windows. Output a correspondence table linking features across datasets with alignment confidence scores. The alignment assumes isobaric features are distinguished primarily by retention time, so RT precision is critical.

## Related tools

- **bmxp** (Parent metabolomics processing platform providing Eclipse module and shared schema (FMDATA, IMDATA) for feature metadata normalization and alignment) — https://github.com/broadinstitute/bmxp
- **Eclipse** (Standalone module implementing m/z-based matching and RT-based clustering to align same-method nontargeted LCMS datasets) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Downstream BMXP module that clusters redundant LCMS features based on RT and correlation; operates on post-Eclipse aligned features) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **Blueshift** (Downstream BMXP module for drift correction via pooled technical replicates and internal standards; requires cross-dataset correspondence to identify technical replicates) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md

## Evaluation signals

- Correspondence table contains no orphaned features — every feature in input datasets appears in at least one correspondence pair or is marked unmatched
- Matched feature pairs satisfy both m/z tolerance (typically ≤5 ppm for high-resolution LCMS) and RT co-elution window constraints
- Alignment confidence scores are populated and rank-ordered; high-confidence matches have lower m/z error and overlap with replicate intensities
- No cross-method contamination — verify that all matched features originated from datasets with identical 'Method' column values
- Downstream Gravity clustering and Blueshift drift correction consume the correspondence output without schema errors or missing Compound_ID references

## Limitations

- Eclipse requires same-method inputs; it cannot align datasets from different LCMS methods, columns, or ionization modes without prior harmonization
- Alignment relies on m/z and RT precision; features with poor RT reproducibility (e.g., early or late eluting features) may fail to match even if genuinely identical
- Isobaric features (identical m/z, different RT) are distinguished by retention time alone; without orthogonal metrics (e.g., XIC shape, correlation), alignment may be ambiguous
- The shared BMXP schema requires explicit index and column naming (Compound_ID, MZ, RT, Intensity, Method); users must rename or remap input tables prior to Eclipse execution

## Evidence

- [other] Eclipse is a standalone module designed to align two or more same-method nontargeted LCMS datasets, functioning as a step in the BMXP processing pipeline written in Python and C for cloud-compatible operation.: "Eclipse is a standalone module designed to align two or more same-method nontargeted LCMS datasets, functioning as a step in the BMXP processing pipeline"
- [other] Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values. Parse and normalize feature metadata (m/z, RT, intensity distributions) across datasets. Apply m/z-based matching with tolerance threshold to identify candidate feature pairs across datasets. Apply retention-time-based clustering to refine candidate matches within co-eluting windows. Output matched feature correspondence table linking features across datasets with alignment confidence scores.: "Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values. Parse and normalize feature metadata (m/z, RT,"
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA` - Describes the feature. Index default is `Compound_ID`: "All BMXP modules use a shared schema and file formats with our prefered columns headers. Feature Metadata `bmxp.FMDATA` - Describes the feature. Index default is `Compound_ID`"
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [readme] Eclipse - Align two or more same-method nontargeted LCMS datasets: "Eclipse - Align two or more same-method nontargeted LCMS datasets"
- [readme] While the tools are and always will be standalone, we are working on linking them closer together with a shared schema, and eventually may have a pipeline ability to run all steps, given a set of parameters.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline"

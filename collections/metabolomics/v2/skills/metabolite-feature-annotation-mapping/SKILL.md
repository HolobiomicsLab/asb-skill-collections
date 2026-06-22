---
name: metabolite-feature-annotation-mapping
description: Use when after importing raw metabolomics data (e.g., from Metabolon, Nightingale, SomaLogic, or Olink platforms) into a Metaboprep object, but before quality control or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - R
  - metaboprep
  - read_metabolon
  - read_nightingale, read_olink, read_somalogic
  - batch_normalise
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
---

# metabolite-feature-annotation-mapping

## Summary

Map and annotate metabolite features from untargeted or targeted metabolomics data by associating raw mass spectrometry signals with metabolite identities, biochemical pathways, and external reference databases (KEGG, HMDB). This skill enables downstream biological interpretation by enriching feature tables with structured metadata.

## When to use

After importing raw metabolomics data (e.g., from Metabolon, Nightingale, SomaLogic, or Olink platforms) into a Metaboprep object, but before quality control or statistical analysis. Use this skill when you have a features table with identifiers but need to link them to metabolite names, biochemical pathways, KEGG IDs, HMDB groups, or platform-specific annotations (e.g., 'pos' vs 'neg' ionization mode).

## When NOT to use

- If the features frame is already fully annotated and validated (i.e., has been through QC and you are resuming a previous analysis) — reload the saved Metaboprep object instead.
- If your input is a pre-processed feature table with already-aggregated abundances by metabolite (e.g., pathway summaries) — this skill operates at the individual feature level, not aggregated level.
- If you lack any platform or ionization mode information and cannot infer biochemical context — annotation will be incomplete and batch_normalise() may fail or produce spurious results.

## Inputs

- raw metabolomics data matrix (samples × features, numeric values)
- features metadata frame with at minimum: feature_id, metabolite_id columns; optionally: platform, pathway, kegg, group_hmdb, reason_excluded, excluded
- samples metadata frame (one row per sample with sample_id and phenotype/batch covariates)

## Outputs

- Metaboprep S4 object with annotated features slot
- feature_summary data frame (from feature_summary() function) containing hierarchical clustering and metadata relationships
- tab-delimited features table (exported via export(..., format='metaboprep')) with all annotations preserved

## How to apply

Extract or construct a features metadata frame containing at minimum feature_id and metabolite_id columns; map additional annotations such as platform (ionization mode), pathway assignment, KEGG identifier, and HMDB group membership from the source data provider's annotation sheet or external reference files. Pass this enriched features frame to the Metaboprep object constructor alongside the data matrix and samples metadata. Verify annotation coverage by inspecting the feature_summary output, which returns a data frame with hierarchical clustering of features based on their metadata relationships (controlled by tree_cut_height parameter). Rationale: standardized feature annotation enables batch effect correction by platform, biological interpretation via pathway enrichment, and systematic exclusion of features with poor or ambiguous annotations during quality control.

## Related tools

- **metaboprep** (Constructs Metaboprep S4 object from data, samples, and features frames; provides feature_summary() to visualize and validate feature annotations via hierarchical clustering) — https://github.com/MRCIEU/metaboprep
- **read_metabolon** (Imports Metabolon Excel workbooks and parses platform and pathway annotations from the OrigScale sheet into a features metadata frame) — https://github.com/MRCIEU/metaboprep
- **read_nightingale, read_olink, read_somalogic** (Platform-specific import functions that extract and standardize feature annotations (platform, metabolite identifiers) from Nightingale, Olink, and SomaLogic data formats) — https://github.com/MRCIEU/metaboprep
- **batch_normalise** (Uses platform annotation (run_mode_col, run_mode_colmap) to perform batch correction stratified by ionization mode or instrument) — https://github.com/MRCIEU/metaboprep

## Examples

```
mydata <- Metaboprep(data = data, samples = samples, features = features); tree <- attr(feature_summary(mydata, source_layer='input', tree_cut_height=0.5), 'qc_tree'); plot(tree, main='Feature Annotation Tree')
```

## Evaluation signals

- feature_summary() output returns non-null hierarchical clustering tree (attr(mydata@feature_summary, 'qc_tree')) with all features represented in dendrogram
- All rows in the features frame have non-missing feature_id and metabolite_id; missing values in pathway, kegg, or group_hmdb are documented and justified
- summary(mydata) confirms Feature Annotation columns are present and contain expected metadata fields (platform, pathway, kegg, group_hmdb)
- Batch normalisation runs without error and stratification by run_mode_col correctly groups samples by ionization mode or platform
- Export to tab-delimited format produces a features file with identical column count and non-null entries for mapped annotations

## Limitations

- Annotation completeness depends on source data provider (Metabolon, Nightingale, etc.); some platforms may not provide KEGG or HMDB IDs, limiting pathway-level interpretation.
- The metaboprep package currently does not perform de novo feature matching against external databases (e.g., mass-to-formula conversion); it relies on pre-computed identifications from the instrument vendor.
- Feature tree construction (feature_summary with tree_cut_height parameter) is sensitive to the choice of tree_cut_height; no guidance is provided in the README for selecting this threshold for novel datasets.
- No changelog found for the package; unclear which annotation fields or metadata schemas are stable across versions v1.1 → v1.2.

## Evidence

- [methods] Extract the data matrix, samples metadata frame, and features metadata frame from the returned list.: "Extract the data matrix, samples metadata frame, and features metadata frame from the returned list."
- [readme] Feature Annotation contains metabolite_id, platform, pathway, kegg, group_hmdb columns.: "Feature Annotation (metadata):
   Columns: 8
   Names  : feature_id, metabolite_id, platform, pathway, kegg, group_hmdb, reason_excluded, excluded"
- [methods] Construct a Metaboprep S4 object by calling Metaboprep(data=data, samples=samples, features=features).: "Construct a Metaboprep S4 object by calling Metaboprep(data=data, samples=samples, features=features)."
- [readme] Batch normalisation is performed stratified by platform and ionization mode.: "batch_normalise(run_mode_col = "platform", run_mode_colmap = c(pos="pos", neg="neg"))"
- [readme] feature_summary() returns a hierarchical clustering tree of features based on their metadata relationships.: "feature_summary(metaboprep = mydata, source_layer = "input", outlier_udist = 1.0, tree_cut_height = 0.5, output = "data.frame")"

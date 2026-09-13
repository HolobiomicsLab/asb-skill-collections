---
name: retention-time-peak-matching
description: Use when after drift correction and quality flagging, when you have a
  feature abundance matrix with associated metadata (Feature_ID, m/z, retention time)
  and need to identify which features likely represent the same underlying metabolite
  or adduct series before statistical analysis or metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - notame
  - R
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Retention-time-peak-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify correlated metabolic features within a retention-time window by matching m/z values and temporal proximity, forming the basis for downstream feature clustering in LC-MS metabolomics. This skill groups isotopologues, adducts, and in-source fragments that co-elute but have different mass signatures.

## When to use

After drift correction and quality flagging, when you have a feature abundance matrix with associated metadata (Feature_ID, m/z, retention time) and need to identify which features likely represent the same underlying metabolite or adduct series before statistical analysis or metabolite identification.

## When NOT to use

- Data has not yet undergone drift correction—systematic intensity shifts will inflate or deflate correlations spuriously.
- Retention-time information is missing or unreliable (e.g., from different LC methods or poor chromatographic resolution).
- Input is already a manually curated feature grouping or metabolite-level table—peak-matching is a preprocessing step, not a post-hoc validation tool.

## Inputs

- MetaboSet object (or equivalent: feature abundance matrix + feature metadata table)
- Feature metadata: Feature_ID (character), Mass (numeric m/z), RetentionTime (numeric, seconds)

## Outputs

- Connection graph (edge list): pairs of correlated Feature_IDs with correlation and retention-time proximity scores
- Connection metadata: correlation coefficient, retention-time delta for each edge

## How to apply

Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the MetaboSet object using combined_data() and fData(). Execute find_connections() with a Pearson correlation threshold (typically 0.9) and a retention-time window (e.g., ±1 s) while specifying column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime'). This function identifies all feature pairs whose peak intensities correlate above threshold AND whose retention times fall within the window, returning a graph of connections. The rationale is that true co-eluting adducts/isotopologues show both high intensity correlation across samples and temporal co-occurrence, distinguishing them from spurious correlations.

## Related tools

- **notame** (Implements find_connections() function and MetaboSet data structure for storing and managing feature metadata and abundances during retention-time-based feature matching) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class upon which MetaboSet is built, enabling structured storage of feature abundance data and metadata)
- **R** (Execution environment for correlation calculations and graph construction)

## Examples

```
find_connections(metaboset_obj, name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime', corr_threshold=0.9, rt_window=1)
```

## Evaluation signals

- Verify that all returned connections have Pearson correlation ≥ threshold (0.9 or user-specified) by spot-checking a random sample.
- Confirm that all edge retention times satisfy |rt_feature_i − rt_feature_j| ≤ window (e.g., ±1 s); no violations should appear in output.
- Inspect the connection graph degree distribution: isolated nodes (degree=0) should be features uncorrelated with others; high-degree hubs should correspond to known adduct series or isotope patterns.
- Cross-validate: manually verify that a subset of strong connections (e.g., top 10% by correlation) represent biologically plausible adduct/isotope relationships (e.g., [M+H]⁺ and [M+Na]⁺ pairs).
- Check that the number of connections scales reasonably with feature count and correlation threshold—a sharp drop in edges when threshold increases from 0.85 to 0.95 suggests threshold sensitivity is working as intended.

## Limitations

- Correlation-based matching assumes sample-to-sample abundance co-variation; features present in only a few samples may have unstable correlations despite true co-elution.
- Retention-time window (±1 s) must be calibrated to instrument resolution; poorly resolved LC methods or variable retention-time shift (e.g., column aging) will cause true co-eluting features to fall outside the window.
- The method does not distinguish between true adducts/isotopologues and coincidental co-correlation (e.g., two unrelated metabolites that happen to co-vary across the sample cohort).
- Requires sufficient sample diversity: if sample set is homogeneous (e.g., all from same tissue/treatment), even unrelated features may correlate poorly, reducing true-positive connection detection.
- The notame package API is still quite experimental, and breaking changes are possible.

## Evidence

- [other] 1. Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the toy MetaboSet object using combined_data() and fData().: "Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the toy MetaboSet object using combined_data() and fData()"
- [other] 2. Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated feature pairs within the RT window.: "Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated"
- [intro] The notame package bundles preprocessing methods with visualizations for non-targeted LC-MS metabolomics data analysis.: "The notame package bundles together preprocessing methods from other packages along with visualizations developed by the authors for non-targeted LC-MS metabolomics data analysis"
- [readme] A novel method for clustering similar molecular features: "A novel method for clustering similar molecular features"
- [readme] The package API is still quite experimental, and breaking changes are possible: "The package API is still quite experimental, and breaking changes are possible"

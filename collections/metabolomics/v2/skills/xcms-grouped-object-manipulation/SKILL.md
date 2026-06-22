---
name: xcms-grouped-object-manipulation
description: Use when you have preprocessed LC-MS data with detected chromatographic peaks that need to be consolidated into feature groups representing putative compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3370
  tools:
  - xcms
  - MsFeatures
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.
- 'Package: xcms'
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xcms-grouped-object-manipulation

## Summary

Manipulate and refine feature groupings in XcmsExperiment objects by applying sequential grouping strategies (retention time, abundance correlation, EIC similarity) to reduce feature complexity and consolidate ions from the same compound. This skill is essential for LC-MS metabolomics workflows where multiple ions per compound must be grouped before annotation.

## When to use

Apply this skill when you have preprocessed LC-MS data with detected chromatographic peaks that need to be consolidated into feature groups representing putative compounds. Use it if your goal is to reduce data complexity by clustering features with similar retention time, correlated abundance patterns, and/or similar extracted ion chromatogram (EIC) peak shapes. Typical trigger: output from findChromPeaks() contains hundreds to thousands of individual features that require consolidation before annotation or statistical analysis.

## When NOT to use

- Input data has not yet undergone chromatographic peak detection (findChromPeaks).
- Feature grouping has already been completed and you only need to extract or visualize existing groups.
- Your analysis requires preservation of all individual peak detections without consolidation (e.g., when peak multiplicity per compound is itself a variable of interest).

## Inputs

- XcmsExperiment object (xmse) with detected chromatographic peaks from findChromPeaks()
- SimilarRtimeParam, AbundanceSimilarityParam, or EicSimilarityParam parameter object

## Outputs

- Grouped XcmsExperiment object with reduced feature group count
- Integer count of final distinct feature groups from featureGroups()

## How to apply

Begin with a pre-processed XcmsExperiment object containing detected chromatographic peaks. Apply groupFeatures() sequentially with parameter objects tailored to your data: first use SimilarRtimeParam(window_seconds) to cluster features within a retention-time window (e.g., 20 seconds), then refine with AbundanceSimilarityParam(threshold, transform) to group features whose abundances are correlated across samples (e.g., threshold=0.7, log2 transform), and optionally further refine with EicSimilarityParam(threshold, n) to group by similarity of extracted ion chromatogram peak shapes using the top n samples per group (e.g., threshold=0.7, n=2). After each groupFeatures() call, extract the final group count using featureGroups() to verify consolidation. The rationale is that features of the same compound should co-elute, show correlated abundance patterns, and display similar peak shapes; successive refinement progressively enforces these properties.

## Related tools

- **xcms** (Provides groupFeatures() function, SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam classes, and featureGroups() extraction method.) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes used by xcms.)

## Examples

```
groupFeatures(xmse, param = EicSimilarityParam(threshold = 0.7, n = 2)); featureGroups(xmse)
```

## Evaluation signals

- Final feature group count from featureGroups() is reduced compared to initial peak count (e.g., 2289 features grouped into 589 feature groups as in task_003).
- Each feature is assigned to exactly one feature group (no duplicates or unassigned features).
- Features within each group have retention times within the specified SimilarRtimeParam window.
- When AbundanceSimilarityParam is applied, abundance correlation between grouped features meets or exceeds the threshold (e.g., ≥0.7).
- When EicSimilarityParam is applied, EIC peak shapes of grouped features show visual or quantitative similarity as computed by the parameter object.

## Limitations

- Sequential grouping is order-dependent; the order of applying SimilarRtimeParam, AbundanceSimilarityParam, and EicSimilarityParam can affect final group counts and membership.
- Parameter threshold selection (e.g., SimilarRtimeParam window, AbundanceSimilarityParam threshold, EicSimilarityParam threshold) requires domain knowledge and may benefit from exploratory analysis; no single universal threshold is provided.
- EicSimilarityParam(n=2) uses only the top n samples per group for peak shape comparison, which may underutilize samples with lower abundance or miss subtle peak shape differences in low-abundance samples.
- The method assumes that features of the same compound have correlated abundances; compounds with sample-dependent ion suppression or ionization efficiency changes may yield spurious groupings or false negatives.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time, similar abundance patterns across samples, and similar peak shapes of extracted ion chromatograms: "Features (ions) of the same compound should have similar retention time, similar abundance patterns across samples, and similar peak shapes of extracted ion chromatograms"
- [intro] Compounding aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity: "Compounding aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity"
- [intro] groupFeatures() with EicSimilarityParam(threshold = 0.7, n = 2) to group features by similarity of extracted ion chromatogram peak shapes: "groupFeatures(xmse, EicSimilarityParam(threshold = 0.7, n = 2)) to group features by similarity of extracted ion chromatogram peak shapes"
- [other] Call groupFeatures() with EicSimilarityParam(threshold = 0.7, n = 2) to group features by similarity of extracted ion chromatogram peak shapes.: "Call groupFeatures() with EicSimilarityParam(threshold = 0.7, n = 2) to group features by similarity of extracted ion chromatogram peak shapes."
- [other] the 2289 features being grouped into 589 distinct feature groups: "The grouping based on EIC correlation resulted in the 2289 features being grouped into 589 distinct feature groups."

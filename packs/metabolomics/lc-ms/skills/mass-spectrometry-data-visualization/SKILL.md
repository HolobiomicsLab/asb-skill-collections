---
name: mass-spectrometry-data-visualization
description: Use when after applying retention time, abundance correlation, or EIC similarity-based feature grouping (e.g., via SimilarRtimeParam, AbundanceSimilarityParam, or EicSimilarityParam). Use when you need to visually confirm that grouped features belong to the same compound—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MsFeatures
  - Spectra
  - MsBackendMgf
  - MetaboCoreUtils
  - xcms
  - pheatmap
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(Spectra)
- library(MsBackendMgf)
- '%\VignetteDepends{xcms,MsDataHub,BiocStyle,pander,Spectra,MsBackendMgf,MetaboCoreUtils}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
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

# mass-spectrometry-data-visualization

## Summary

Visualization of LC-MS feature groups and extracted ion chromatograms (EICs) to inspect peak shape similarity, retention time alignment, and abundance patterns across samples. Used to validate feature grouping decisions and identify anomalies (e.g., co-eluting features with shifted retention times) that distinguish sub-groups.

## When to use

After applying retention time, abundance correlation, or EIC similarity-based feature grouping (e.g., via SimilarRtimeParam, AbundanceSimilarityParam, or EicSimilarityParam). Use when you need to visually confirm that grouped features belong to the same compound—i.e., have aligned retention times, similar EIC peak shapes, and correlated abundance patterns across samples—or when you suspect sub-groups within a feature group based on EIC morphology shifts.

## When NOT to use

- Input is a pre-validated, published feature quantification table (e.g., normalized abundance matrix); visualization is not needed to confirm grouping integrity.
- No feature grouping has yet been performed; first apply retention time, abundance, or EIC similarity grouping.
- Data are single-sample or single-run experiments where cross-sample abundance correlation and consistency checks are not meaningful.

## Inputs

- XcmsExperiment or comparable grouped feature object (output from groupFeatures() with one or more refinement parameters)
- Raw LC-MS spectral data (Spectra object or xcms OnDiskMSnExp) for EIC extraction
- Feature grouping metadata (group IDs, feature m/z, retention time, feature indices)

## Outputs

- plotFeatureGroups(): scatter plot in m/z–retention time space with grouped features connected by lines
- plotEICs(): overlay chromatogram plots showing intensity vs. retention time for selected feature groups, with one trace per feature
- Visual inspection report documenting peak shape consistency, retention time alignment, and sub-grouping anomalies within feature groups

## How to apply

Load the grouped feature object (XcmsExperiment or comparable) into R. Use plotFeatureGroups() to display all features in m/z–retention time space with grouped features connected by lines; this reveals gross grouping structure and potential outliers. For fine-grained inspection, generate overlay EIC plots using plotEICs() or equivalent visualization, filtering to specific feature groups of interest (e.g., FG.013.001, FG.045.001). Examine EIC traces for visual alignment of peak maxima, peak shape similarity, and consistency of retention time across all features within a group. Shifted retention times or divergent peak shapes within a nominal group signal that sub-grouping refinement (via EicSimilarityParam with appropriate threshold, e.g., 0.7) or manual curation may be needed. Document visual anomalies and map them to quantitative similarity metrics (e.g., EIC correlation scores) to establish evidence-based sub-group boundaries.

## Related tools

- **xcms** (Provides groupFeatures(), plotFeatureGroups(), filterRt(), filterMz(), and raw spectral data access (Spectra, XcmsExperiment containers) for feature grouping and EIC extraction) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines grouping parameter classes (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam) and grouping workflows that feed into visualization) — https://github.com/RforMassSpectrometry/MsFeatures
- **Spectra** (Manages raw LC-MS spectral data and provides access to m/z, retention time, and intensity for EIC construction) — https://github.com/RforMassSpectrometry/Spectra
- **pheatmap** (Optional tool for heatmap visualization of abundance patterns across samples to support feature correlation inspection)

## Examples

```
plotFeatureGroups(xe, mzlim=c(304, 305), rtlim=c(230, 610)); plotEICs(xe, features=c('FG.013.001', 'FG.045.001'), main='EIC Overlay by Feature Group')
```

## Evaluation signals

- plotFeatureGroups() output shows all features in groups as co-localized clusters in m/z–retention time space with visually tight grouping (no outliers far from group centroid)
- EIC overlay plots show aligned peak maxima (retention time agreement within group tolerance, typically seconds) and similar peak shapes for all features within a group
- Sub-groups within a larger feature group (e.g., FG.013.001 split into two sub-groups) are visually distinct in EIC plots: one sub-group shows a shifted retention time or markedly different peak morphology (e.g., broader, multi-modal, or earlier/later elution)
- EIC correlation scores (used by EicSimilarityParam) quantitatively match visual grouping decisions: features clustered together in plots have correlation > threshold (e.g., > 0.7), and features in separate sub-groups have correlation < threshold
- No unexpected outliers appear in plotFeatureGroups(): all grouped features should occupy the same nominal m/z–retention time region without isolated points at distant m/z or time

## Limitations

- Visualization alone does not distinguish true co-eluting isomers or isobars from genuine feature groups; quantitative similarity metrics (abundance correlation, EIC correlation, MS2 spectroscopy) are needed for definitive assignments.
- EIC plots can be crowded or difficult to interpret if a feature group contains many features (> ~10) or if features have very low intensity; filtering by m/z or intensity range may be necessary.
- Retention time alignment across runs can introduce artifacts if inter-run retention time drift is not corrected (e.g., using retention time correction algorithms); visualization may show spurious sub-groups if RT correction is inadequate.
- EIC similarity threshold (e.g., 0.7) is data-dependent and method-dependent; no universal threshold applies across all LC-MS platforms, sample types, or peak detection parameter sets; thresholds must be tuned empirically.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of [extracted ion chromatograms] of the same compound should be similar: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [other] one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features: "one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features"
- [intro] plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line: "plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line"
- [other] Generate overlay EIC plots for feature groups FG.013.001 and FG.045.001 using the plotEICs() or comparable visualization function to display peak shape similarity: "Generate overlay EIC plots for feature groups FG.013.001 and FG.045.001 using the plotEICs() or comparable visualization function to display peak shape similarity"
- [intro] Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [readme] Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects: "Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects"

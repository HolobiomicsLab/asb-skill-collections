---
name: preprocessing-pipeline-parameter-optimization
description: Use when you have raw TOF-MS or IM-MS data in Agilent MassHunter (.d) or UIMF format with jagged peaks and low-abundance ions that require signal enhancement, but you need to decide whether to apply smoothing, and at what strength, to avoid over-smoothing real signals or under-removing artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Preprocessing Pipeline Parameter Optimization

## Summary

Optimize multidimensional smoothing, noise filtering, and saturation repair parameters in IM-MS preprocessing to enhance signal quality while preserving real peaks and removing artifacts. This skill involves selecting and tuning algorithm parameters within the PNNL PreProcessor to balance noise removal against signal integrity across jagged, low-abundance ion regions.

## When to use

Apply this skill when you have raw TOF-MS or IM-MS data in Agilent MassHunter (.d) or UIMF format with jagged peaks and low-abundance ions that require signal enhancement, but you need to decide whether to apply smoothing, and at what strength, to avoid over-smoothing real signals or under-removing artifacts. Use it when visual inspection of preprocessed output shows either residual spikes/noise or degraded peak fidelity, indicating parameter tuning is needed.

## When NOT to use

- Input is already a denoised feature table or a processed peak list — preprocessing operates on raw instrument data, not derived matrices.
- Data quality is already high (signal-to-noise ratio > 100) and visual inspection shows minimal artifacts — optimization will provide marginal benefit and risk introducing smoothing artifacts.
- Ions exhibit highly convoluted elution/mobility profiles caused by interferences — saturation repair and smoothing may produce incorrect results in these regions, making parameter optimization unreliable.

## Inputs

- Raw IM-MS data file in Agilent MassHunter (.d) format or UIMF format
- Reference peak annotations or signal-to-noise ground truth (optional but recommended)
- Retention time range filter specifications (if retention time filtering is desired)

## Outputs

- Preprocessed MS file in native Agilent MassHunter format (.d) or UIMF with enhanced signal quality
- Preprocessing output log documenting applied parameters and artifact removal statistics
- Metadata export containing parameter set and processing version information

## How to apply

Load raw IM-MS data (.d or UIMF format) into PNNL PreProcessor and execute the preprocessing pipeline with initial default parameters for multidimensional smoothing, noise filtering by low intensity threshold, and spike removal. Examine the output log and peak quality metrics to assess whether artifacts (jagged peaks in low-abundance ions) have been adequately removed without degrading real signals. If artifacts persist, increase smoothing intensity or lower the spike-removal threshold; if real peaks are flattened, reduce smoothing or raise the intensity threshold. Validate the optimized parameters by comparing preprocessed peaks against input reference data and verifying that high-confidence peaks are preserved while noise is suppressed. Export metadata to document the chosen parameter set for reproducibility and future batch processing.

## Related tools

- **PNNL PreProcessor** (Primary preprocessing environment; hosts multidimensional smoothing, noise filtering, spike removal, saturation repair, and data compression algorithms whose parameters are optimized by this skill) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Native data format (.d) reader and writer; supplies raw IM-MS data and accepts preprocessed output in its native format for downstream analysis) — https://www.agilent.com
- **IM-MS Browser** (Optional tool for batch extraction of polygon regions; used for method definition (.m file) in Step 4a of polygon extraction workflow)

## Evaluation signals

- Output log confirms successful artifact removal and absence of error flags in multidimensional smoothing and spike removal steps.
- Visual comparison of input and preprocessed peaks shows jagged artifacts in low-abundance ion regions smoothed while high-confidence peaks remain distinct and unsuppressed.
- Signal-to-noise ratio of known reference peaks improves by at least 10–20% after optimization without peak shift or width distortion.
- Metadata export correctly documents all applied parameters (smoothing intensity, intensity threshold, spike removal tolerance) enabling reproducible re-processing.
- No saturation-repair artifacts are introduced; peaks with highly convoluted elution profiles are either avoided or flagged in the output log as potentially unreliable.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences; parameter optimization cannot overcome this fundamental ambiguity — affected regions should be identified and excluded or manually reviewed.
- No changelog or version tracking is documented; reproducibility and parameter traceability across tool versions are not guaranteed without manual metadata curation.
- Optimization is data-specific and instrument-dependent; parameters tuned for one MassHunter method or sample type may not transfer to other experiments without re-validation.

## Evidence

- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [intro] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [intro] Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power and ability to differentiate structural isomers: "Ion mobility-mass spectrometry (IM-MS) provides an increasingly popular platform for analyzing complex samples due to its separation power"
- [readme] we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files: "we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files"

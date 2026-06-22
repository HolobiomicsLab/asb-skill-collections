---
name: spike-artifact-detection-and-removal
description: Use when processing raw IM-MS data (Agilent MassHunter .d or UIMF format) that exhibits isolated high-intensity noise artifacts or instrumental artifacts that appear as discrete, non-continuous signals in the retention time, ion mobility, or m/z dimensions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  techniques:
  - ion-mobility-MS
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

# spike-artifact-detection-and-removal

## Summary

Detects and eliminates isolated high-intensity noise artifacts (spikes) that do not represent true ion signals in IM-MS data, improving signal quality without removing low-abundance genuine peaks. This is a critical preprocessing step applied after low-intensity threshold filtering to refine multidimensional ion mobility–mass spectrometry datasets.

## When to use

Apply this skill when processing raw IM-MS data (Agilent MassHunter .d or UIMF format) that exhibits isolated high-intensity noise artifacts or instrumental artifacts that appear as discrete, non-continuous signals in the retention time, ion mobility, or m/z dimensions. Spike removal should be performed after low-intensity threshold filtering to target residual noise that threshold-based filtering alone does not eliminate, especially in drift tube (DT) or SLIM IM-MS instruments.

## When NOT to use

- When the input data has already undergone aggressive spike removal or denoising by another tool; double-processing risks removing weak but genuine signals.
- When analyzing samples with expected sparse, isolated true signals (e.g., single-point calibration standards or ultra-low-abundance analytes); the algorithm may incorrectly classify coherence-lacking genuine ions as artifacts.
- If the study requires retention of all detected peaks (including artifacts) for later statistical assessment or artifact quantification.

## Inputs

- Raw IM-MS data file (Agilent MassHunter .d format or UIMF format)
- Low-intensity threshold-filtered dataset (intermediate product from noise filtering pipeline)

## Outputs

- Spike-removed IM-MS data file (MassHunter .d or UIMF format)
- Preprocessed dataset with improved signal quality and reduced artifact peaks

## How to apply

Within PNNL PreProcessor, apply the spike removal algorithm after loading the raw IM-MS data file and applying low-intensity threshold filtering. The algorithm detects isolated high-intensity peaks that lack continuity across adjacent frames or mobility bins—characteristics distinguishing noise spikes from genuine ion signals with coherent elution or mobility profiles. The spike removal operates in multidimensional space (retention time, ion mobility, m/z) to identify and flag isolated points. Configure the tool to preserve low-abundance genuine ions (which typically show some spatial coherence even at low intensity) while eliminating discontinuous high-intensity artifacts. The filtered data is exported to a new MS-file in the same instrument format with enhanced signal-to-noise ratio and reduced false positive peaks.

## Related tools

- **PNNL PreProcessor** (Primary software tool that implements the spike removal algorithm integrated into the multidimensional preprocessing pipeline for IM-MS data) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Source data format provider; raw IM-MS data acquired in MassHunter .d format is loaded into PNNL PreProcessor for spike removal)

## Evaluation signals

- Verify that spike-removed data exhibits fewer isolated high-intensity peaks not present in adjacent frames or mobility bins compared to the low-intensity-threshold-filtered input.
- Confirm that low-abundance, spatially coherent ion signals (genuine peaks with continuous elution or mobility profiles) are preserved post-removal by comparing peak intensities and counts before/after spike removal for known analytes.
- Check that the output file maintains valid IM-MS structure (consistent frame count, mobility bins, and m/z arrays) and can be loaded successfully in downstream tools (e.g., IM-MS Browser or IMFE for further analysis or visualization).
- Visually inspect 2D or 3D reconstructed ion maps (retention time vs. ion mobility, or m/z vs. mobility) to confirm elimination of isolated high-intensity pixels while preserving coherent peak shapes.
- Compare total signal intensity and number of detected features before and after spike removal; expect a reduction in peak count with minimal loss of total signal from known analytes.

## Limitations

- Spike removal may produce suboptimal results for ions with highly convoluted elution/mobility profiles caused by interferences, as these can be misclassified as isolated artifacts rather than genuine signal.
- The algorithm's effectiveness depends on proper tuning of spike detection criteria (spatial coherence thresholds); overly aggressive settings risk removing weak but genuine signals, while lenient settings may fail to eliminate all instrumental artifacts.
- No changelog or version-specific documentation is available, limiting reproducibility and tracking of algorithmic changes or bug fixes across PNNL PreProcessor releases.

## Evidence

- [methods] An algorithm to remove noise in the form of 'spikes' from IM-MS data: "An algorithm to remove noise in form of 'spikes'"
- [other] Spike removal eliminates isolated high-intensity artifacts that do not represent true ion signals: "Apply spike removal algorithm to detect and eliminate isolated high-intensity artifacts that do not represent true ion signals"
- [intro] PNNL-PreProcessor includes spike removal as part of its noise filtering functionality: "noise filtering by low intensity threshold and spike removal"
- [other] The software exports filtered data to the same instrument format (MassHunter .d or UIMF) after preprocessing: "Export the filtered data to a new MS-file in the same instrument format (MassHunter .d or UIMF) with enhanced signal quality and reduced noise"
- [methods] Saturation repair software may fail for ions with highly convoluted profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [readme] PNNL-PreProcessor supports Agilent MassHunter .d and UIMF file formats: "Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM)"

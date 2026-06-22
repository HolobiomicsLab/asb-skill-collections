---
name: mass-spectrometry-instrument-format-compatibility
description: Use when you have raw mass spectrometry data from an instrument not yet validated in your pipeline (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
---

# mass-spectrometry-instrument-format-compatibility

## Summary

Extend mass spectrometry data processing pipelines to ingest and standardize spectral data from multiple ionization platforms (DI-MS, ASAP-MS, LDI-MS, AI-MS) by parsing vendor-native and open formats (mzML, mzXML) into a unified pre-processing workflow. This skill ensures that instrument-agnostic analysis, peak detection, and database search can proceed uniformly across heterogeneous MS methodologies.

## When to use

You have raw mass spectrometry data from an instrument not yet validated in your pipeline (e.g., LDI-MS, ambient ionization MS, or a new vendor platform), and you need to confirm that the data can be imported, pre-processed (noise filtering, baseline correction, peak detection), and scored using the same downstream algorithms as established reference instruments (DI-MS, ASAP-MS). Use this skill when the research question requires species discrimination or unknown sample authentication across multiple MS platforms with comparable accuracy.

## When NOT to use

- Input data is already in a pre-processed, normalized feature table or peak list—parser extension and baseline correction are not needed.
- The new instrument's spectral format is proprietary and cannot be reverse-engineered or documented without vendor support.
- No ground-truth reference labels or validation cohort is available; comparative evaluation against baseline performance cannot be performed.

## Inputs

- Raw spectral data in vendor-native format or open formats (mzML, mzXML)
- Mass spectrometry data from new or unvalidated instruments (LDI-MS, AI-MS, etc.)
- Reference database with known species or sample labels
- Baseline accuracy metrics from validated instruments (DI-MS, ASAP-MS)

## Outputs

- Parsed spectral data in unified internal format
- Pre-processed spectra (noise-filtered, baseline-corrected, peaks detected)
- Species authentication results with confidence scores
- Visual outputs (e.g., plots, heatmaps) comparable to reference instrument output
- Comparative accuracy metrics and performance evaluation report

## How to apply

First, extend the file parser to recognize and load spectral formats from the new instrument—prioritize open formats (mzML, mzXML) or native vendor formats. Second, route imported data through the standard pre-processing pipeline (noise filtering, baseline correction, peak detection) without instrument-specific branching. Third, apply the same peak detection algorithm and database search methodology used for validated instruments. Fourth, generate visual outputs and authentication results in the same format as reference data. Finally, evaluate accuracy metrics (e.g., discrimination rate, confidence scores) against the established baseline performance from DI-MS/ASAP-MS validation cohorts. Success is demonstrated when accuracy is comparable to or exceeds the reference instrument performance on the same species or sample classes.

## Related tools

- **RapidMass** (Graphical data processing platform that integrates file parsing, pre-processing (noise filtering, baseline correction, peak detection), database search algorithms, and visual output generation for multi-instrument MS data.) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Reference validated instrument; provides baseline accuracy and performance metrics for comparative evaluation of new instrument compatibility.)
- **ASAP-MS** (Reference validated instrument; provides baseline accuracy and performance metrics for comparative evaluation of new instrument compatibility.)

## Evaluation signals

- New instrument data successfully imports and parses without format errors or data loss in spectral m/z and intensity arrays.
- Pre-processed spectra from new instrument show consistent noise filtering, baseline correction, and peak detection quality (visually comparable to reference instrument output).
- Database search scores and species discrimination results from new instrument match or exceed baseline accuracy (sensitivity, specificity, or overall classification rate) on a validation cohort with ground-truth labels.
- Visual outputs (plots, heatmaps, authentication reports) for new instrument samples are produced in the same format and information density as reference instrument samples.
- Comparative performance report documents accuracy metrics side-by-side between new and validated instruments; no systematic bias or degradation in authentication confidence scores is observed.

## Limitations

- Requires that spectral data from the new instrument can be exported or accessed in open formats (mzML, mzXML) or documented vendor formats; proprietary closed formats may prevent implementation.
- Validation depends on availability of ground-truth reference labels and easily confused or challenging sample cohorts; weak or non-representative validation datasets may obscure compatibility issues.
- Performance parity with established instruments is not guaranteed; some MS methodologies (e.g., different ionization regimes or mass accuracy) may yield inherently different spectral signatures that require method re-optimization rather than simple format bridging.
- No changelog or versioning documentation is maintained in the RapidMass repository, so compatibility across software updates is not tracked.

## Evidence

- [other] Integrate LDI-MS data import capability into RapidMass by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats).: "Integrate LDI-MS data import capability into RapidMass by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats)."
- [other] Pre-process LDI-MS spectra through RapidMass's standard data pre-processing pipeline (noise filtering, baseline correction, peak detection).: "Pre-process LDI-MS spectra through RapidMass's standard data pre-processing pipeline (noise filtering, baseline correction, peak detection)."
- [other] Evaluate LDI-MS authentication performance against a reference dataset or ground-truth species labels and compare accuracy metrics to the established DI-MS/ASAP-MS validation baseline.: "Evaluate LDI-MS authentication performance against a reference dataset or ground-truth species labels and compare accuracy metrics to the established DI-MS/ASAP-MS validation baseline."
- [intro] supports data from multiple instruments, including DI-MS and ASAP-MS: "supports data from multiple instruments, including DI-MS and ASAP-MS"
- [readme] Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be tried with this software.: "Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be"

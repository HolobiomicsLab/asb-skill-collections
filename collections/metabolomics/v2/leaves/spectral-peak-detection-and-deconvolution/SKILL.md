---
name: spectral-peak-detection-and-deconvolution
description: Use when you have raw LC-MS data in mzML or mzXML format and need to
  extract reproducible, high-quality metabolite features (m/z, retention time, intensity)
  for global metabolomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - MetaboAnalystR
  - MetaboAnalyst web server
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-48009-6
  all_source_dois:
  - 10.1038/s41467-024-48009-6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-detection-and-deconvolution

## Summary

Automated feature detection and intensity quantification from raw LC-MS1 and MS/MS spectra using optimized parameter selection and deconvolution algorithms. This skill bridges raw mass spectrometry data to a quantitative feature table suitable for downstream metabolomic analysis.

## When to use

Apply this skill when you have raw LC-MS data in mzML or mzXML format and need to extract reproducible, high-quality metabolite features (m/z, retention time, intensity) for global metabolomics. Use it especially when aiming to maximize detection sensitivity and minimize false identifications across DDA or DIA acquisition modes.

## When NOT to use

- Input is already a processed feature table or intensity matrix—skip directly to normalization or statistical analysis.
- Spectral data are in formats not supported by mzML/mzXML conversion or vendor-specific APIs are unavailable.
- Analysis requires targeted quantitation of known metabolites with predefined inclusion lists; use targeted peak extraction instead of global feature detection.

## Inputs

- raw LC-MS spectra (mzML or mzXML format)
- MS1 spectral data (full-scan or targeted)
- MS/MS spectral data (DDA or DIA mode)

## Outputs

- quantitative feature table with m/z, retention time, and intensity values
- deconvolved MS/MS spectra with peak assignments
- feature quality metrics and completeness report
- compound annotations linked to MS/MS features

## How to apply

Load raw LC-MS1 spectra (mzML/mzXML) into MetaboAnalystR and apply auto-optimized peak detection using the built-in feature detection module. The algorithm automatically selects parameters to improve quantification accuracy and detection of high-quality MS features. For MS/MS spectra, apply the streamlined deconvolution module designed for both data-dependent acquisition (DDA) and data-independent acquisition (DIA) to resolve overlapping peaks and assign compound annotations. Validate the resulting feature table for completeness and quality metrics using MetaboAnalystR's quality assessment module. According to benchmark studies, the optimized workflow detects >10% more high-quality features and increases chemical identification true positive rate by >40% without increasing false identifications.

## Related tools

- **MetaboAnalystR** (Executes auto-optimized peak detection on raw LC-MS spectra and performs MS/MS deconvolution for DDA and DIA data; integrates large spectra databases (~1.5 million MS2 spectra) for compound annotation) — https://github.com/xia-lab/MetaboAnalystR
- **MetaboAnalyst web server** (Cloud-based version of the same pipeline; R code and results are synchronized with the web platform for reproducibility)

## Examples

```
devtools::install_github("xia-lab/MetaboAnalystR"); library(MetaboAnalystR); mSet <- InitDataObjects("mass_spec", "norm_dmwU", FALSE); mSet <- Read.MSdata(mSet, "raw_spectra.mzML"); mSet <- PerformPeakDetection(mSet); mSet <- PerformPeakAlignment(mSet); mSet <- ValidateFeatureTable(mSet)
```

## Evaluation signals

- Feature table is non-empty with m/z values in expected range (50–1200 m/z for typical metabolomics), retention times in observed chromatographic window, and intensity values across all samples with expected missing-value patterns.
- Number of detected features is consistent with biological expectation and benchmarks; comparison to known spike-in standards or QC replicates shows >90% reproducibility of peak intensity.
- Quality metrics (signal-to-noise ratio, peak shape, alignment accuracy) meet MetaboAnalystR's thresholds; no systematic batch effects or instrumental drift visible in feature intensity distributions.
- Deconvolved MS/MS spectra show resolved fragment peaks with chemical plausibility (mass difference consistent with neutral loss or characteristic fragmentation); compound annotations have high cosine similarity (>0.7) to spectral library entries.
- Validation against known metabolites or internal standards shows >10% improvement in detection coverage and >40% increase in true positive identification rate versus legacy methods.

## Limitations

- Performance depends on raw spectra quality and instrument calibration; poorly calibrated or degraded samples may yield low peak counts or misaligned features.
- Auto-optimization of peak detection parameters assumes sufficient spectral complexity and signal; very simple or very noisy data may require manual parameter tuning.
- MS/MS compound annotation relies on spectral library matching; unknown metabolites or compounds absent from the ~1.5 million-entry database will remain unidentified.
- The pipeline is optimized for global (untargeted) metabolomics; targeted or highly selective methods may perform suboptimally.
- Large-scale batch processing may require API service or local high-performance computing setup; desktop installation has practical limits on dataset size.

## Evidence

- [other] MetaboAnalystR 4.0 implements a unified LC-MS workflow for global metabolomics, as indicated by the software title.: "MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics"
- [other] The workflow explicitly loads raw LC-MS spectral data (mzML or mzXML format) and executes peak detection on raw spectra using configured algorithm parameters.: "load raw LC-MS spectral data (mzML or mzXML format) into the MetaboAnalystR environment. 2. Execute peak detection on raw spectra using the configured algorithm parameters"
- [readme] MetaboAnalystR 4.0 features an auto-optimized module for LC-MS1 spectra processing.: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] The package includes a streamlined MS/MS deconvolution and annotation module supporting both DDA and DIA acquisition modes.: "a streamlined MS/MS spectra deconvolution and compound annotation module for both data-dependent acquisition (DDA) or data-independent acquisition (DIA)"
- [readme] Benchmark studies demonstrate significant improvement in feature detection and identification accuracy.: "MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features. For both DDA and DIA datasets, MetaboAnalystR 4.0 can increase the true positive rate of chemical"
- [readme] The package is synchronized with the MetaboAnalyst web server and comes with large knowledge bases for local processing.: "The package is synchronized with the MetaboAnalyst web server. MetaboAnalystR 4.0 comes with a large collection of knowledgebases (~500,000 entries of metabolite sets) and spectra databases (~1.5"
- [other] The workflow consolidates aligned peaks into a quantitative feature table with m/z, retention time, and intensity values.: "Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples"

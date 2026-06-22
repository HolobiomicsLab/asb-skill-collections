---
name: lipid-fingerprint-regeneration-neural-networks
description: Use when you have MS/MS spectra with initial lipid annotations from spectral library matching (e.g., from XCMS + CAMERA or LipidIN's Expeditious Querying module) and seek to improve recall, precision, and annotation coverage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - XCMS
  - CAMERA
  - LipidIN Expeditious Querying (EQ) Module
  - WMYn (Wide-spectrum Modeling Yield network)
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-fingerprint-regeneration-neural-networks

## Summary

Applies a Wide-spectrum Modeling Yield (WMY) neural network to regenerate MS/MS lipid fingerprints from annotated spectral data, improving lipid annotation recall and coverage by ~20% over baseline spectral library matching. This skill enhances accuracy of lipid identification in high-throughput lipidomics workflows.

## When to use

Apply this skill when you have MS/MS spectra with initial lipid annotations from spectral library matching (e.g., from XCMS + CAMERA or LipidIN's Expeditious Querying module) and seek to improve recall, precision, and annotation coverage. Specifically use it after baseline spectral matching returns candidate lipid annotations but coverage or accuracy remains limited—the WMY network generates enhanced fingerprint predictions with confidence scores to boost detection of true lipids that baseline matching may have missed.

## When NOT to use

- Input spectra lack any baseline annotation from spectral library matching—the WMY network is a post-processing refinement step, not a de novo annotation tool.
- Spectral data are already from a different modality (e.g., direct infusion MS, ion mobility MS) for which the network has not been trained or evaluated.
- Pre-trained weights are unavailable and training data (annotated matrix + ground-truth labels) are insufficient (the README recommends 'at least' a matrix and vector pair; single-sample datasets will not train effectively).

## Inputs

- MS/MS spectra in mzML or .rda format
- Annotated lipid candidate list from baseline spectral library matching
- Initial annotations with m/z values and MS/MS fragment peaks
- Pre-trained WMY neural network weights (or training data: matrix .csv + ground-truth vector .csv)

## Outputs

- Regenerated lipid fingerprint spectrograms with confidence scores
- Enhanced lipid annotations with improved coverage and recall
- Recall, precision, and coverage metrics comparing WMY vs. baseline
- Estimated recall boost percentage (target ~20%)

## How to apply

First, load preprocessed MS/MS spectral data in mzML or .rda format and extract annotated lipid candidates from baseline spectral library matching (from the EQ module or equivalent). Input these annotated candidates into the WMY neural network model (which is inspired by Kolmogorov-Arnold Networks and multi-head attention mechanisms). Execute the network to regenerate lipid fingerprints, producing enhanced predictions with associated confidence scores. Finally, compare regenerated fingerprints against baseline spectral-matching-only annotations by computing recall, precision, and coverage metrics; calculate estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of the ~20% improvement threshold. The method is matrix- and instrument-independent.

## Related tools

- **XCMS** (Preprocesses and aligns MS/MS spectral data (nonlinear peak alignment, matching, and initial feature detection) to prepare input for LipidIN annotation workflow)
- **CAMERA** (Performs initial spectral annotation and compound spectra extraction from LC-MS/MS data; outputs candidate annotations that serve as baseline input to the WMY regeneration network)
- **LipidIN Expeditious Querying (EQ) Module** (Generates baseline spectral library matching annotations against the 168.6 million lipid fragmentation hierarchical library; these high-confidence matches are fed into the WMY network for fingerprint regeneration) — https://github.com/LinShuhaiLAB/LipidIN
- **WMYn (Wide-spectrum Modeling Yield network)** (Neural network model (inspired by KAN and multi-head attention) that regenerates lipid fingerprint spectrograms and produces enhanced predictions with confidence scores to improve recall) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source('./predict.py'); predict(data_path='path/to/annotations.csv', project_folder='path/to/pretrained_weights', mode='neg'); # or for training: batch_process(data_folder='path/to/training_data', output_folder='path/to/output')
```

## Evaluation signals

- Estimated recall boost is ≥20% as calculated from (recall_wmy − recall_baseline) / recall_baseline × 100%
- Precision metric remains stable or improves relative to baseline spectral matching (avoid false positive inflation)
- Coverage metric increases: total number of annotated lipid features grows compared to baseline-only results
- Confidence scores output by the WMY network are calibrated and correlate with annotation correctness (higher scores → higher match quality)
- Regenerated fingerprints are reproducible across replicate runs and independent of sample matrix and instrument type (matrix- and instrument-invariance)

## Limitations

- Performance depends critically on quality and quantity of baseline annotations; weak baseline spectral matches cannot be meaningfully regenerated.
- Pre-trained weights are specific to positive and negative ionization modes (pos/neg) and ESI source type ([M+CH3COO]−, [M+COOH]−, etc.); transferability to alternative ionization modes is not documented.
- Training WMY weights requires paired training data: annotated matrix .csv and ground-truth label vector .csv; insufficient or imbalanced training data will degrade model performance.
- The 20% recall boost estimate is reported on specific benchmarks (methodology and datasets not detailed in README); real-world performance on novel samples may vary.
- No discussion section or changelog provided; failure modes, edge cases, and known issues are not comprehensively documented.

## Evidence

- [intro] Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with a 20% estimated recall boost.: "Wide-spectrum Modeling Yield network regenerates lipid fingerprints to improve coverage and accuracy with a 20% estimated recall boost"
- [methods] Input annotated lipid candidates from the LipidIN spectral querying module into the WMY network, then execute to regenerate lipid fingerprints with confidence scores and compare against baseline to compute recall, precision, and coverage metrics.: "Input annotated lipid candidates from the LipidIN spectral querying module into the WMY network. 3. Execute the WMY network to regenerate lipid fingerprints, producing enhanced predictions with"
- [readme] The system employs greedy secondary matching algorithms and spectrum enhancement algorithms; the model generates reverse lipid fingerprint spectrograms independent of sample matrices and instruments.: "Using the model to generate reverse lipid fingerprint spectrograms, independent of sample matrices, instruments."
- [readme] WMYn predict lipid fingerprint spectrogram using the model we designed inspired by KAN and Muit-head attention.: "WMYn predict lipid fingerprint spectrogram using the model we designed inspired by KAN and Muit-head attention"
- [readme] Training requires input data including a matrix and a vector; batch processing supports multiple paired files (e.g., aaa.csv with aaa_GT.csv).: "The input data include a matrix and a vector for training at least. For example AAA.csv(matrix) and AAA_GT.csv(vector)"

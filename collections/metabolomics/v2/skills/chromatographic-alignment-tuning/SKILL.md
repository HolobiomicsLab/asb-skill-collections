---
name: chromatographic-alignment-tuning
description: Use when when processing a cohort of centroided mzML LC-MS files with high sample-to-sample retention time and m/z drift, and you need reproducible alignment of detected peaks across all samples before gap-filling and feature consolidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
---

# chromatographic-alignment-tuning

## Summary

Automated optimization of retention time and m/z alignment parameters across LC-MS samples to establish consensus feature coordinates for untargeted metabolomics. This skill tunes alignment module parameters by iterating candidate combinations against quality metrics (feature reproducibility, detection counts, signal-to-noise) to select the parameter set that maximizes cross-sample peak alignment fidelity.

## When to use

When processing a cohort of centroided mzML LC-MS files with high sample-to-sample retention time and m/z drift, and you need reproducible alignment of detected peaks across all samples before gap-filling and feature consolidation. Apply this skill after peak picking has been executed on individual samples but before grouping isotopologues and gap-filling.

## When NOT to use

- Input samples are from a single injection or replicate only; alignment requires multiple samples to evaluate reproducibility.
- Retention time drift is negligible (e.g., short runs with stable instrumental conditions) or already corrected by external standards; automated tuning adds overhead with minimal benefit.
- Input data are already aligned or feature tables are already consolidated; re-alignment is redundant and will corrupt existing cross-sample coordinates.

## Inputs

- Peak picking results (one per sample) in mzML/mzXML format or intermediate peak table format
- QC sample identifiers (from samples.csv) to serve as alignment references
- Alignment parameter search space definition (retention time tolerance range, m/z tolerance range, intensity ratio criteria)

## Outputs

- Optimized alignment parameters (retention time tolerance, m/z tolerance, intensity ratio thresholds)
- Aligned feature table with consensus retention time and m/z coordinates across all samples
- Alignment quality score and metadata (reproducibility metrics, number of aligned features)

## How to apply

Within the SLAW automated parameter optimization loop: (1) initialize a search space over alignment parameters (e.g., retention time tolerance window, m/z tolerance, intensity ratio thresholds for grouping); (2) for each candidate parameter combination, perform full sample alignment across all QC and study samples to establish consensus retention time and m/z coordinates; (3) evaluate alignment quality using a metric such as feature reproducibility across replicates, total number of aligned features detected, or signal-to-noise ratio of aligned peaks; (4) track the parameter combination with the highest quality score; (5) return the optimized alignment parameters as input to the final processing run. The rationale is that alignment is data-dependent—optimal parameters vary across LC-MS experiments and sample cohorts—so automated search avoids manual tuning and improves reproducibility of feature detection and quantification.

## Related tools

- **Centwave** (Peak picking algorithm used upstream; alignment parameters are optimized conditioned on Centwave peak picking results) — https://github.com/sneumann/xcms
- **FeatureFinderMetabo** (Alternative peak picking algorithm; alignment parameters are optimized conditioned on FeatureFinderMetabo peak picking results)
- **ADAP** (Alternative peak picking algorithm; alignment parameters are optimized conditioned on ADAP peak picking results)
- **SLAW** (Containerized workflow that wraps alignment parameter optimization as part of automated parameter optimization module) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest  # After editing parameters.txt to set optimization/need_optimization to True
```

## Evaluation signals

- Alignment quality metric (feature reproducibility, detected feature count, or signal-to-noise ratio) reaches a local maximum or plateau, indicating convergence to optimal parameters.
- Aligned feature table exhibits consistent m/z and retention time coordinates across samples with low inter-sample variance in consensus positions.
- Number of features successfully grouped and aligned is maximized relative to the pre-alignment peak count, indicating efficient grouping without over-merging.
- Downstream gap-filling step completes without errors and produces a consolidated feature matrix with minimal missing values.
- Optimized alignment parameters are consistent with instrumental and chemical properties (e.g., m/z tolerance ≤ 5 ppm for accurate-mass instruments; retention time tolerance reflects column equilibration time).

## Limitations

- Alignment optimization requires QC samples or random sample selection if samples.csv is missing; sparse or poorly representative samples may yield suboptimal parameters.
- Parameter search space is discrete and finite; optimal parameters may lie outside the predefined search bounds, necessitating manual expansion of ranges.
- Optimization is computationally intensive for large cohorts (thousands of samples); processing time scales with number of samples and parameter combinations tested.
- SLAW is restricted to DDA (data-dependent acquisition) LC-MS; DIA-MS2 spectra are not supported and will be skipped.
- All input data must be centroided and of uniform polarity; profile mode or mixed-polarity data will cause failure or incorrect alignment.

## Evidence

- [other] Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling.: "Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling."
- [other] Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome.: "Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome."
- [other] Perform sample alignment across all samples to establish consensus retention time and m/z coordinates.: "Perform sample alignment across all samples to establish consensus retention time and m/z coordinates."
- [other] SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data.: "SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data."
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."

---
name: lc-ms-feature-quality-assessment
description: Use when you have generated feature tables from LC-MS data using different parameter combinations (e.g., varying Centwave, FeatureFinderMetabo, or ADAP peak picking settings) and need to objectively compare their outputs to select the -performing configuration for your dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS Feature Quality Assessment

## Summary

Evaluate LC-MS feature detection outcomes using quality metrics such as feature reproducibility, total feature count, and signal-to-noise ratio to determine whether parameter combinations produce acceptable peak picking, alignment, and gap-filling results. This skill is essential for automating the selection of optimal processing parameters in untargeted metabolomics workflows.

## When to use

Apply this skill when you have generated feature tables from LC-MS data using different parameter combinations (e.g., varying Centwave, FeatureFinderMetabo, or ADAP peak picking settings) and need to objectively compare their outputs to select the best-performing configuration for your dataset. Typical triggers include: running parameter optimization loops, deciding whether to accept automated parameter suggestions, or validating reproducibility across replicate QC samples.

## When NOT to use

- Input data are already processed and feature-extracted; quality assessment applies only to parameter selection, not post-hoc validation of finished tables.
- You lack replicate QC samples; reproducibility-based metrics cannot be reliably computed without repeated injections of the same pooled reference material.
- LC-MS data are profile-mode (non-centroided); SLAW and its quality assessment assume centroided mzML input only.

## Inputs

- Centroided mzML files (LC-MS data, MS1 and optionally DDA-MS2)
- Parameter search space (ranges for peak picking, alignment, gap-filling parameters)
- QC sample replicates (for reproducibility assessment)

## Outputs

- Quality score per parameter combination
- Ranked parameter sets
- Optimized parameter set (highest quality score)
- Feature table(s) from best-performing parameters

## How to apply

For each candidate parameter combination applied to peak picking, alignment, and gap-filling, compute a quality metric that captures the reliability and completeness of feature detection. The SLAW workflow evaluates each combination using metrics such as feature reproducibility across QC replicates, absolute number of features detected, or signal-to-noise ratio of detected peaks. Score each parameter set using these metrics; higher reproducibility and feature count with acceptable SNR indicate better parameter choices. Select the parameter combination with the highest overall quality score and use it as the optimized parameter set for full dataset processing. This iterative approach requires executing the complete peak picking → alignment → gap-filling pipeline for each candidate, then comparing results to identify the configuration that balances sensitivity (number of features) with precision (reproducibility and signal quality).

## Related tools

- **Centwave** (Peak picking algorithm; candidate for parameter optimization and quality assessment) — https://github.com/zamboni-lab/SLAW
- **FeatureFinderMetabo** (Peak picking algorithm; candidate for parameter optimization and quality assessment) — https://github.com/zamboni-lab/SLAW
- **ADAP** (Peak picking algorithm; candidate for parameter optimization and quality assessment) — https://github.com/zamboni-lab/SLAW
- **SLAW** (Automated parameter optimization framework implementing iterative feature quality assessment across peak picking, alignment, and gap-filling modules) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
# Then edit parameters.txt to set optimization/need_optimization=True and re-run the same command
```

## Evaluation signals

- Quality scores increase monotonically or plateau as parameter search progresses, indicating convergence toward optimal settings.
- The selected parameter combination produces higher feature counts in QC replicates compared to non-optimized defaults, demonstrating sensitivity gain.
- Feature reproducibility across replicate QC injections exceeds a domain-relevant threshold (e.g., >70% of features detected in all replicates) after optimization.
- Signal-to-noise ratio of detected peaks in the optimized feature table is higher than in suboptimal parameter combinations, confirming precision improvement.
- Gap-filling recovers expected metabolite features in downstream sample analysis when using optimized parameters versus arbitrary defaults.

## Limitations

- Quality assessment relies on the choice of metric (reproducibility, feature count, SNR); different metrics may rank parameter sets differently, and the 'best' metric is context-dependent.
- QC sample composition and representativeness directly affect reproducibility scores; if QC samples do not reflect the chemical diversity of study samples, optimized parameters may not generalize well.
- Computational cost scales with the size of the parameter search space; exhaustive grid search over many parameters across thousands of samples may be prohibitively slow without careful bounds on the search space.
- SLAW supports only centroided, DDA-mode LC-MS data in a single polarity per run; DIA-MS data and mixed-polarity experiments are not supported and cannot be assessed with this workflow.

## Evidence

- [other] Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome.: "Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio)"
- [other] Select the parameter combination with the highest quality score and return as the optimized parameter set.: "Select the parameter combination with the highest quality score and return as the optimized parameter set."
- [other] SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data.: "SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data."
- [other] Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling.: "Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling."
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."

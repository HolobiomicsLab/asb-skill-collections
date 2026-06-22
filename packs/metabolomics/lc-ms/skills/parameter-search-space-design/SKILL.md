---
name: parameter-search-space-design
description: Use when when beginning an untargeted LC-MS analysis and either (1) the dataset characteristics (sample complexity, instrument platform, or polarity) differ from previously optimized cohorts, (2) multiple peak-picking algorithms (Centwave, FeatureFinderMetabo, ADAP) are available and their relative.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Parameter Search Space Design

## Summary

Defines the bounded ranges and candidate combinations of peak picking, alignment, and gap-filling parameters for automated optimization in untargeted LC-MS workflows. This skill establishes the feasible region within which parameter optimization algorithms will search to yield optimal LC-MS processing outcomes.

## When to use

When beginning an untargeted LC-MS analysis and either (1) the dataset characteristics (sample complexity, instrument platform, or polarity) differ from previously optimized cohorts, (2) multiple peak-picking algorithms (Centwave, FeatureFinderMetabo, ADAP) are available and their relative performance on your data is unknown, or (3) you need to generate an optimized parameter set tailored to a specific LC-MS dataset rather than apply generic defaults.

## When NOT to use

- Your organization has a validated, instrument-specific parameter set from prior large-scale studies and requires consistency across cohorts rather than per-dataset optimization.
- Raw LC-MS data is profile-mode (not centroided); parameter optimization requires centroided input.
- Analysis is targeted (selected reaction monitoring or data-independent acquisition); SLAW and this skill support DDA only.

## Inputs

- centroided mzML files (raw LC-MS data)
- parameter range specifications (lower and upper bounds for peak picking, alignment, gap-filling)
- QC sample definitions or representative sample subset

## Outputs

- initialized parameter search space (candidate parameter combinations)
- optimized parameter set (single best-scoring combination from search space)

## How to apply

Initialize the parameter search space by defining ranges for peak picking parameters (ppm tolerance, minimum intensity thresholds, peak shape constraints), alignment parameters (retention-time deviation windows, mass-to-charge deviation tolerance), and gap-filling parameters (intensity thresholds for feature recovery). The search space bounds should reflect the expected variability in your LC-MS data and the capabilities of your instruments. SLAW then iterates through candidate parameter combinations drawn from this space, applying each combination to representative QC samples and evaluating the resulting feature tables using reproducibility or signal-to-noise metrics. The parameter combination achieving the highest quality score becomes the optimized set. The rationale is that defining this space upfront ensures the optimization loop explores parameter regions likely to yield valid peaks while avoiding combinations that would degrade feature detection or introduce noise.

## Related tools

- **Centwave** (Peak picking algorithm; one of three selectable peak-picking methods whose parameters are optimized within the search space)
- **FeatureFinderMetabo** (Peak picking algorithm; one of three selectable peak-picking methods whose parameters are optimized within the search space)
- **ADAP** (Peak picking algorithm; one of three selectable peak-picking methods whose parameters are optimized within the search space)
- **SLAW** (Automated LC-MS processing workflow that wraps parameter search space design and executes the optimization loop across the defined space) — https://github.com/zamboni-lab/SLAW

## Evaluation signals

- Search space bounds are explicitly logged or reported; verify ranges span expected instrumental variability without being so loose they include physically implausible combinations (e.g., ppm tolerance > 100).
- Optimized parameter set is distinct from default/prior parameters, indicating the search space exploration was non-trivial.
- Feature count, reproducibility score, or signal-to-noise ratio of the optimized parameter set exceeds those of baseline or random parameters by a measurable margin (e.g., ≥10% improvement in feature recovery).
- Quality metric used to score parameter combinations is reported and is consistent with LC-MS data characteristics (e.g., feature reproducibility across QC replicates, number of features detected with adequate peak shape).
- Parameter combinations at the boundary of the search space are not selected; if they are, search space expansion is warranted.

## Limitations

- Parameter search space design is computationally expensive; optimization scales with the number of candidate combinations and number of samples evaluated per combination.
- The choice of quality metric for evaluating parameter combinations is subjective; different metrics (e.g., feature count vs. reproducibility) may favor different parameter sets, and no universal metric exists across all metabolomics workflows.
- Search space optimization is specific to the dataset and instrument used for optimization; transfer of optimized parameters to different instruments or sample matrices may degrade performance.
- SLAW does not support profile-mode mzML or data-independent acquisition (DIA); centroided, DDA-only data are required for parameter space exploration to be valid.

## Evidence

- [other] Load raw LC-MS data files and initialize parameter search space for peak picking (Centwave, FeatureFinderMetabo, or ADAP), alignment, and gap-filling modules.: "Load raw LC-MS data files and initialize parameter search space for peak picking (Centwave, FeatureFinderMetabo, or ADAP), alignment, and gap-filling modules."
- [other] Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling.: "Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling."
- [other] Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome.: "Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome."
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
- [readme] Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP: "Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP"
- [other] SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data.: "SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data."
- [readme] Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported.: "Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported."

---
name: mz-retention-time-tolerance-parameter-configuration
description: Use when when invoking Asari to process centroid mzML files for the first
  time in a PCPFM experiment, or when RT and m/z accuracy characteristics of your
  LC-MS instrument differ from the pipeline defaults (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Asari
  - Python
  - PCPFM
  techniques:
  - LC-MS
  - GC-MS
  - direct-infusion-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pcpfm asari -i ./my_experiment
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mz-retention-time-tolerance-parameter-configuration

## Summary

Configuration of mass-to-charge (m/z) and retention time (RT) tolerance parameters for feature grouping in Asari LC-MS feature extraction. These parameters define the maximum acceptable deviations when clustering detected ions into putative metabolite features across a sample cohort.

## When to use

When invoking Asari to process centroid mzML files for the first time in a PCPFM experiment, or when RT and m/z accuracy characteristics of your LC-MS instrument differ from the pipeline defaults (e.g., instruments with lower mass resolution, longer RT drift, or non-standard chromatography). Parameter tuning is warranted if you observe either excessive feature fragmentation (same metabolite split across multiple feature rows) or over-merging (unrelated ions grouped into a single feature).

## When NOT to use

- Input data are already in feature table format (i.e., features have already been grouped and aligned). These parameters apply only during the initial mzML-to-feature-table conversion step.
- Working with non-LC-MS data (e.g., GC-MS, direct infusion MS) where retention time is not a meaningful dimension or where different grouping logic applies.
- Instrument specifications are unknown and cannot be estimated from prior calibration data or manufacturer documentation; in such cases, rely on default values and validate results post-hoc rather than attempting blind parameter optimization.

## Inputs

- centroid mzML files (in converted_acquisitions subdirectory)
- PCPFM experiment object with inferred ionization mode (positive or negative)
- LC-MS instrument specifications (mass accuracy, chromatographic reproducibility)

## Outputs

- feature grouping configuration (m/z and RT tolerance parameters passed to Asari)
- full feature table with all detected features grouped according to specified tolerances
- preferred feature table with quality-filtered features grouped according to specified tolerances

## How to apply

Asari accepts two key tolerance parameters during invocation: (1) m/z tolerance, specified in parts-per-million (ppm), which controls the maximum mass deviation allowed when grouping ions of the same putative feature across samples; (2) retention time tolerance, specified in seconds, which defines the maximum RT shift permitted for an ion to be assigned to an existing feature group. The default values are 5 ppm m/z tolerance and 2 second RT tolerance for feature grouping. These defaults are optimized for typical high-resolution LC-MS platforms. Adjustment should be made based on your instrument's demonstrated mass accuracy and chromatographic reproducibility: stricter tolerances (e.g., 3 ppm, 1 second) reduce false merging but may fragment true features; looser tolerances (e.g., 10 ppm, 5 seconds) increase feature recovery but risk grouping unrelated ions. Rationale: m/z tolerance must accommodate instrument mass error, which typically ranges from 1–5 ppm on modern Orbitraps but can be 10+ ppm on lower-resolution platforms; RT tolerance must account for inter-sample chromatographic drift and column performance degradation over a batch run.

## Related tools

- **Asari** (feature extraction and grouping engine that accepts m/z and RT tolerance parameters to align and cluster detected ions into metabolite features) — https://github.com/shuzhao-li/asari
- **PCPFM** (metabolomics pipeline that wraps Asari invocation and manages parameter passing to the feature extraction workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- Feature table row count and feature density (median features per sample) are stable across re-runs with identical parameters and should increase or remain stable when tolerances are relaxed, decrease when tightened.
- Manual inspection of a representative set of feature peak shapes using Asari's visual dashboard confirms that grouped ions share consistent m/z and RT coordinates within the specified tolerances and are not artefactually merged.
- Replicate sample correlation improves (e.g., Pearson r > 0.9 for technical replicates) when parameters are optimized, indicating reduced feature fragmentation and spurious merging.
- Quality metrics reported in the preferred feature table (e.g., signal-to-noise, feature completeness across samples) do not degrade when parameters are adjusted within a reasonable range (±50% of defaults).
- Downstream annotation results (number of matched MS1 or MS2 identifications per feature) do not decrease, suggesting features remain biologically coherent after grouping.

## Limitations

- Default 5 ppm m/z and 2 second RT tolerances are optimized for high-resolution Orbitrap and similar modern instruments; lower-resolution or time-of-flight instruments may require significantly larger m/z tolerances (e.g., 10–20 ppm) to achieve adequate feature grouping, risking over-merging.
- RT tolerance is sensitive to chromatographic drift and batch effects; a global fixed value may be inadequate for very long sample runs or instruments with significant inter-batch RT shifts. Internal spike-in standards for QC support is to be implemented but currently unavailable.
- No automated method for deriving optimal tolerances from instrument QC data is provided; practitioners must rely on instrument specifications, prior validation studies, or manual tuning based on biological replicability.
- Parameter optimization requires iterative trial-and-error or access to ground-truth spike-in or reference standards, which may not be available for all compound classes or experimental contexts.

## Evidence

- [other] Invoke Asari with the inferred ionization mode on the converted_acquisitions subdirectory containing centroid .mzML files, using default parameters (5 ppm m/z tolerance, 2 second retention time tolerance for feature grouping).: "using default parameters (5 ppm m/z tolerance, 2 second retention time tolerance for feature grouping)"
- [other] Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory.: "Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features"
- [readme] process mzML data to feature tables (Asari): "process mzML data to feature tables (Asari)"

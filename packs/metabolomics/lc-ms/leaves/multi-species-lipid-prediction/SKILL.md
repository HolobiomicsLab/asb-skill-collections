---
name: multi-species-lipid-prediction
description: Use when you have candidate lipid annotations from high-throughput spectral
  matching (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - XCMS
  - CAMERA
  - LipidIN EQ module
  - LipidIN LCI module
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-species-lipid-prediction

## Summary

Apply the Lipid Categories Intelligence (LCI) model's three relative retention time rules to filter spectral library matches and predict unannotated lipids across multiple species cohorts, achieving a 5.7% false discovery rate while expanding lipid coverage. This skill reduces false positive annotations by leveraging retention time patterns as a secondary filter on hierarchical fragmentation library query results.

## When to use

You have candidate lipid annotations from high-throughput spectral matching (e.g., from XCMS + hierarchical fragmentation library querying) across samples from multiple species or cohorts, and you need to validate candidates and predict unannotated lipids while controlling false discovery rate. Apply this when spectral similarity scores alone produce unacceptable false positive rates and you have retention time measurements available for cohort-level pattern analysis.

## When NOT to use

- Your input lacks retention time or chromatographic ordering information — the LCI model requires relative retention time intervals as the primary filtering signal.
- You have only single-species or single-cohort samples — the method depends on computing retention time distributions across multiple species or sample groups to establish meaningful RRT rules.
- Your spectral library query results already have very low false positive rates (<2%) from orthogonal validation — additional LCI filtering may be redundant.

## Inputs

- Spectral query result file (CSV or binary format) containing candidate lipid annotations from hierarchical fragmentation library matching
- Mass spectrometry data in .rda or .mzML format with extracted MS1 and MS2 peaks and retention time measurements
- Per-candidate MS/MS match scores and m/z values

## Outputs

- Filtered lipid prediction table (CSV) with validated true positive identifications and FDR-controlled annotations
- False discovery rate metric (estimated percentage, e.g., 5.7%)
- Lipid coverage count (total number of unique lipid identifications, e.g., 8923 lipids)

## How to apply

Load spectral query results (candidate lipid annotations with their MS/MS match scores) and extract relative retention time (RRT) values for each candidate lipid. Compute retention time intervals across your species or sample cohorts to establish RRT distributions. Apply the three RRT-based heuristic rules from the LCI model to re-evaluate high-scoring matches: use retention time relationships among candidate lipids and prior MS/MS score information to classify candidates as true or false positives. Aggregate predictions across all species, calculate the false discovery rate (FDR) as the proportion of filtered candidates that fail validation, and count total unique lipid identifications. The LCI module reassesses high-confidence matches using the relative position of primary information (retention time patterns) as a heuristic search filter on secondary matching scores, rather than accepting matches on spectral similarity alone.

## Related tools

- **XCMS** (Peak alignment, matching, and initial preprocessing of mass spectrometry data before spectral querying)
- **CAMERA** (Compound spectra extraction and initial annotation from LC/MS data to prepare candidate feature list)
- **LipidIN EQ module** (Expeditious querying module that performs secondary matching with lipid fragmentation hierarchical library and normalizes matching results before LCI filtering) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN LCI module** (Core implementation of the three relative retention time rules and heuristic re-evaluation of high-scoring matches using prior MS/MS scores) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source('LCI.r'); LCI('demo_pos/QC_POS1.rda')
```

## Evaluation signals

- FDR metric is reported and matches the expected range (5.7% estimated FDR as demonstrated in the original paper); compare your computed FDR against known-truth lipid identifications or orthogonal validation cohorts.
- Lipid coverage count increases or remains stable after LCI filtering compared to raw spectral matches — verify that the number of unique lipid identifications is reasonable (8923+ lipids in the reference demonstrates feasibility).
- Retention time interval ranges are computed and documented for each species/cohort; inspect that RRT rules correctly separate candidates into true and false positives by visual inspection of retention time plots.
- No retention time-independent false positives remain in the final output — review the filtered annotation table to confirm that eliminated candidates were indeed outliers in retention time space relative to their cohort.
- Reproducibility: re-run the LCI module on the same input data and confirm identical FDR and coverage metrics.

## Limitations

- The method requires sufficient multi-species or multi-cohort samples to compute stable retention time distributions; single-species studies may not generate reliable RRT rules.
- Retention time retention time is instrument- and chromatography-dependent; RRT intervals computed on one LC/MS system may not transfer to different instrument platforms or gradient methods.
- The three RRT rules are heuristic and require tuning for different lipid classes or ionization modes; the 5.7% FDR is specific to the hierarchical library used and may vary with different spectral databases.
- High-throughput prediction of unannotated lipids is limited to the chemical space covered by the 168.6 million lipid fragmentation hierarchical library; lipids with unusual chain compositions or modifications may not be predicted.

## Evidence

- [other] Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives.: "Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence"
- [readme] The Lipid Categories Intelligence (LCI) Module: Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches.: "Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches."
- [intro] Three relative retention time rules develop lipid categories intelligence model for reducing false positive annotations with 5.7% estimated false discovery rate covering 8923 lipids: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [other] Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications).: "Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications)."
- [readme] LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations: "168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"

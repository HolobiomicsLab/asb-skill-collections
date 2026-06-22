---
name: mass-accuracy-tolerance-application
description: Use when when you have generated in silico annotations (from GNPS ISDB, SIRIUS, or timaR) and need to distinguish true matches from false positives by enforcing a mass accuracy constraint. Apply this skill before computing novelty metrics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - GNPS / ISDB
  - SIRIUS
  - Inventa
  - meRgeION2
  - GNPS
  - MassBank
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
- doi: 10.1021/acs.analchem.2c04343
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-tolerance-application

## Summary

Application of mass accuracy (ppm error) thresholds to filter and validate in silico annotations from spectral databases and structure prediction tools in metabolomics workflows. This skill is essential for ensuring that only high-confidence feature–compound matches are retained during annotation refinement.

## When to use

When you have generated in silico annotations (from GNPS ISDB, SIRIUS, or timaR) and need to distinguish true matches from false positives by enforcing a mass accuracy constraint. Apply this skill before computing novelty metrics (e.g., Feature Component) or when building annotated feature tables for downstream comparative metabolomics analysis.

## When NOT to use

- When the input annotations have already been manually validated or curated by expert review; adding automated ppm filtering may introduce false negatives.
- When working with low-resolution data (e.g., nominal mass, <50 ppm uncertainty inherent to the instrument) where a 5 ppm tolerance is too stringent and would reject all candidates; adjust threshold upward or omit this step.
- When annotations come from untargeted searches where m/z uncertainty is already encompassed in the database match score; ppm filtering may be redundant with the scoring scheme.

## Inputs

- Quantitative feature table (MZmine2/MZmine3 format: peak area, m/z, retention time)
- Annotation results table (ISDB or SIRIUS format with observed m/z, theoretical m/z, and match scores)
- Instrument metadata or specifications (to justify ppm_error choice)

## Outputs

- Filtered annotation table (subset of candidates meeting ppm_error and other criteria)
- Per-feature annotation status (annotated vs. non-annotated after filtering)
- Annotation quality report (optionally: counts of candidates retained/rejected by criterion)

## How to apply

Set a ppm_error (parts-per-million) threshold that reflects your instrument's mass accuracy capability and your analytical tolerance for systematic shift. Common thresholds range from 5 ppm (high-resolution Orbitrap/Q-ToF instruments) to 10–20 ppm (lower-resolution systems). For each annotation candidate, compute the mass error as (observed_m_z − theoretical_m_z) / theoretical_m_z × 10^6. Retain only annotations where |mass_error| ≤ ppm_error threshold. This filtering is typically applied in conjunction with complementary filters (shared_peaks ≥ 10, cosine score ≥ 0.7, min_score_final ≥ 0.0) to form a multi-criterion acceptance logic. The ppm threshold should be configured before computing per-sample metrics that depend on annotation status (e.g., counts of annotated vs. non-annotated features).

## Related tools

- **MZmine2** (Source of quantitative feature table (m/z and peak area columns used as input to annotation filtering))
- **MZmine3** (Alternative source of quantitative feature table (direct input format for Inventa annotation workflow))
- **GNPS / ISDB** (Spectral library database; provides theoretical m/z and match scores that are filtered by ppm_error threshold) — https://gnps.ucsd.edu
- **SIRIUS** (Structure prediction tool; outputs candidate compounds with theoretical m/z values subject to ppm_error filtering) — https://bio.informatik.uni-jena.de/software/sirius/
- **timaR** (Taxonomically informed annotation tool; delivers weighted annotation results that are refined by ppm_error cutoff) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **Inventa** (End-to-end novelty prioritization pipeline that applies ppm_error filtering (and other annotation criteria) before computing Feature Component and other metrics) — https://github.com/luigiquiros/inventa

## Evaluation signals

- Verify that the number of retained annotations is plausible relative to input feature count (typically <10–30% of features remain annotated after ppm + other filters).
- Check distribution of mass errors in the filtered set: all values should satisfy |error| ≤ ppm_error threshold; no outliers should be present.
- Confirm that Feature Component (FC) and annotated feature counts are reproducible when re-running the filtering step with the same ppm_error parameter.
- Validate that downstream components (LC, CC, SC) use only the filtered annotation set; spot-check 3–5 samples to confirm non-annotated feature lists exclude filtered-out candidates.
- Compare ppm_error=5 vs. ppm_error=10 results on the same dataset; annotation counts and FC values should increase monotonically with looser tolerance (expect ~20–50% more candidates retained per step).

## Limitations

- Mass accuracy is instrument-dependent; a 5 ppm threshold is only valid for high-resolution instruments (Orbitrap, Q-ToF). Low-resolution instruments (e.g., triple quadrupole with <100 ppm accuracy) will reject almost all matches at 5 ppm and require looser thresholds (20–50 ppm).
- ppm_error filtering alone is insufficient to prevent false positive annotations; cosine score, shared_peaks, and other spectral match criteria must be applied jointly to maintain specificity.
- Systematic mass shifts (e.g., calibration drift across a run) can cause even true matches to exceed the ppm_error threshold; data should be recalibrated or the threshold should be adjusted for affected mass ranges.
- No guidance is provided in the source materials on how to choose ppm_error when instrument specs are unavailable; practitioner must rely on literature or prior knowledge of their instrument.

## Evidence

- [other] ppm_error = 5 # min error in ppm to consider an annotation valable: "ppm_error = 5 # min error in ppm to consider an annotation valable"
- [methods] Filter ISDB annotations by ppm_error (e.g., 5 ppm), shared_peaks (e.g., 10), cosine score (e.g., 0.7), and min_score_final threshold: "Filter ISDB annotations by ppm_error (e.g., 5 ppm), shared_peaks (e.g., 10), cosine score (e.g., 0.7), and min_score_final threshold"
- [other] For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks: "For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10"
- [methods] The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features"
- [methods] Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features.: "Mark features as annotated or unannotated based on filtered annotation results"

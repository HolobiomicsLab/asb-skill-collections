---
name: retention-time-alignment-validation
description: Use when after sample alignment step in untargeted LC-MS workflows, particularly when processing multi-sample cohorts with QC samples interspersed throughout the sequence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW alignment module
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# Retention-Time Alignment Validation

## Summary

Validation of LC-MS retention time (RT) alignment across samples by comparing aligned RT coordinates against reference peaks detected in QC samples. This skill ensures that RT correction has been accurately applied before downstream feature grouping and gap-filling.

## When to use

After sample alignment step in untargeted LC-MS workflows, particularly when processing multi-sample cohorts with QC samples interspersed throughout the sequence. Use this skill when you need to verify that RT drift correction has preserved the integrity of feature clustering before isotopologue/adduct grouping or when optimization of alignment parameters is enabled.

## When NOT to use

- Input is a single-sample LC-MS analysis with no cross-sample alignment requirement.
- No QC samples are available or defined; validation will fall back to random sample selection and cannot assess systematic RT drift.
- Sample alignment step has not yet been performed; validate only after alignment coordinates are computed.

## Inputs

- Aligned feature table (m/z and retention time coordinates per sample)
- QC sample designations (from samples.csv)
- Raw or centroided mzML files (for reference RT extraction)

## Outputs

- Validated RT alignment report (RT deviation statistics by sample)
- Flagged samples with anomalous RT drift
- QC-derived RT reference values and tolerance bounds

## How to apply

Extract reference peaks from QC samples (pooled study samples scattered throughout the injection sequence) and verify that aligned features across all samples cluster around these RT anchors with acceptable deviation. Validate that the RT alignment algorithm has correctly adjusted features in non-QC samples to match the QC reference RT values. SLAW uses QC samples as the primary basis for RT alignment; compare the distribution of aligned RTs in study samples against the QC-derived reference to detect systematic drift or local misalignment. If optimization is enabled, validate that the automated parameter tuning (adjusting alignment window width and smoothing parameters) has minimized RT deviation without collapsing co-eluting species. Check for outlier samples showing large RT shifts relative to the QC median—these indicate potential quality issues (e.g., column degradation or temperature instability).

## Related tools

- **SLAW alignment module** (Performs sample RT alignment and provides QC-based reference RT values for validation) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm that precedes alignment; output features are input to RT alignment validation)

## Evaluation signals

- RT deviation distribution (median and IQR) across all samples clusters around zero or within expected instrumental variation (typically <0.2–0.5 min for modern HPLC).
- QC sample RT values are internally consistent (low inter-QC RT variation), indicating stable reference.
- No systematic RT shift relative to injection order (i.e., early vs. late samples do not show directional drift).
- Study samples align to QC reference RTs within the specified alignment window tolerance without systematic over- or under-correction.
- Samples flagged as outliers (e.g., >3× median absolute deviation from QC median RT) are identifiable for manual inspection or exclusion.

## Limitations

- If no QC samples are defined, SLAW will select random samples as reference, reducing ability to detect systematic drift across the injection sequence.
- Validation cannot directly assess whether co-eluting isobars have been incorrectly merged or resolved; check alignment quality by post-hoc feature clustering (isotopologue/adduct grouping).
- RT alignment is polarity-specific; workflows mixing positive and negative ionization must validate alignment independently for each polarity.
- Automated parameter optimization may mask underlying alignment failures if the optimization metric (e.g., feature count or peak reproducibility) does not directly penalize RT deviation.

## Evidence

- [readme] QC samples used as reference during parameter optimization, to extract reference peaks for RT alignment, to detect isotopes/adducts, etc.: "QC samples used as reference during parameter optimization, to extract reference peaks for RT alignment"
- [intro] Sample alignment step is part of the complete untargeted LC-MS workflow, which operates before isotopologue/adduct grouping.: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts"
- [intro] SLAW includes automated parameter optimization for alignment, adjusting parameters to improve feature alignment across samples.: "Automated parameter optimization for picking, alignment, gap-filling"
- [readme] Ideally, QC samples are pooled study samples that are scattered (intercalated) through the whole sequences.: "Ideally, QC samples are pooled study samples that are scattered (intercalated) through the whole sequences"

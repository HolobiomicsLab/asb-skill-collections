---
name: retention-time-correction
description: Use when metabolomics retention time correction is needed across LC–HRMS runs using XCMS's orbiwarp algorithm with IPO-optimized parameters to ensure consistent feature matching and metabolite identification across multiple samples and replicates.
when_to_use_negative:
- Input xcmsSet already contains grouped features; retention time correction must occur before grouping, not after.
- Single run or single-replicate analysis where no cross-run drift exists; correction is redundant and may introduce noise.
- Data from instruments with very high retention time stability (±0.1 min or better); the correction gain may not justify computational cost.
edam_operation: http://edamontology.org/operation_3629
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3370
tools:
- name: XCMS
  role: Applies orbiwarp retention time correction method with IPO-optimized parameters (distFunc, profStep, gapInit, factorDiag, factorGap) to align peaks across replicates before grouping
  repo: https://github.com/chufz/incubatoR
- name: IPO
  role: Optimizes XCMS parameters including retention time correction settings (orbiwarp configuration) to maximize feature detection and alignment for the specific dataset
- name: ProteoWizard
  role: Converts raw vendor mass spectrometry data to centroided mzML format prior to XCMS retention time correction
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/retention-time-correction/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/retention-time-correction/skill.md
    merged_at: '2026-05-25T07:33:56.481825+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/retention-time-correction@sha256:4c979b18e42d638a84917cfcf41b9c57355ea8d1a378b0a532aa2aa87b87eb37
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# retention-time-correction

## Summary

Align and correct retention times across LC–HRMS runs using XCMS's orbiwarp algorithm with IPO-optimized parameters to ensure consistent feature matching and metabolite identification across multiple samples and replicates.

## When to use

Apply this skill after centroided mzML files have been loaded into XCMS and initial peak detection (centwave) has been completed, but before feature grouping and statistical comparison. Specifically use it when processing replicate LC–HRMS injections of the same compounds across multiple samples, where systematic retention time drift between runs could confound metabolite feature alignment.

## When NOT to use

- Input xcmsSet already contains grouped features; retention time correction must occur before grouping, not after.
- Single run or single-replicate analysis where no cross-run drift exists; correction is redundant and may introduce noise.
- Data from instruments with very high retention time stability (±0.1 min or better); the correction gain may not justify computational cost.

## Inputs

- xcmsSet object post-centwave peak detection (in-memory R object)
- centroided mzML files (stored on disk, referenced by xcmsSet filepaths)
- sample metadata including run order and replicate grouping

## Outputs

- xcmsSet object with corrected retention times (xcms.rds RData file)
- aligned retention time values per feature and sample for downstream grouping

## How to apply

Within XCMS v3.8, invoke the orbiwarp retention time correction method following centwave peak detection. Use IPO-optimized parameters specific to your ionization mode: for positive mode, set distFunc='cor', opt=orbiwarp, profStep=0.91, center=1, response=1, gapInit=0.352, factorDiag=2, factorGap=1; for negative mode, adjust gapInit=0.64 and center=2. The orbiwarp algorithm performs local alignment by correlation of extracted ion chromatograms (EICs) to a reference sample, warping retention times so that peaks with similar m/z and intensity patterns align across the run set. After correction, verify by inspecting a subset of EICs from known metabolite features across replicates—corrected peaks should cluster tightly around a single retention time rather than drifting. The corrected retention times are then passed to the grouping step (density-based grouping in XCMS) where features with m/z within mzwid tolerance and retention time within bw bandwidth are grouped into single metabolite features.

## Related tools

- **XCMS** (Applies orbiwarp retention time correction method with IPO-optimized parameters (distFunc, profStep, gapInit, factorDiag, factorGap) to align peaks across replicates before grouping) — https://github.com/chufz/incubatoR
- **IPO** (Optimizes XCMS parameters including retention time correction settings (orbiwarp configuration) to maximize feature detection and alignment for the specific dataset)
- **ProteoWizard** (Converts raw vendor mass spectrometry data to centroided mzML format prior to XCMS retention time correction)

## Evaluation signals

- Extracted ion chromatograms (EICs) for known metabolites align within ±0.1–0.2 min across replicate samples after correction, compared to ±0.5+ min before
- The number of features detected in the subsequent grouping step increases or remains stable compared to uncorrected data, indicating improved alignment without spurious fragmentation
- Retention time values in the final feature table (peaklist.tsv output) show low variance across biological replicates of the same compound (coefficient of variation <2%)
- Comparison of orbiwarp-corrected grouping to grouping without correction shows consistent assignment of metabolite features to the same peakID (mass@rt identifier) across replicates

## Limitations

- Orbiwarp assumes sufficient similarity in peak intensity patterns across the run set; if one run contains very different metabolite abundances or missing compounds, reference selection and alignment quality may degrade.
- Retention time correction does not account for genuine metabolite shifts due to column degradation or temperature drift; verification with external standards is recommended.
- The algorithm is sensitive to the choice of profStep granularity (0.91 in this study); suboptimal profStep values can lead to undercorrection or overcorrection.
- Some predicted metabolites may not be detected post-correction if they co-elute with background noise or have low ionization efficiency; correction cannot recover signals below detection threshold.

## Evidence

- [methods] Feature detection, alignment, and retention time correction
- [supplementary] IPO-optimized orbiwarp parameters for retention time correction
- [methods] Integration of retention time correction in automated workflow
- [methods] Retention time correction enables assignment of 91 molecular formulas
- [readme] Retention time values used as filtering input
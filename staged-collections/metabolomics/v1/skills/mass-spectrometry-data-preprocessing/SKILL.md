---
name: mass-spectrometry-data-preprocessing
description: Converts raw LC–HRMS data to centroided mzML format and applies feature detection, alignment, and retention-time correction to generate a normalized feature table with m/z values, retention times, and per-sample intensities. This is the foundation for downstream metabolite discovery and annotation in high-throughput screening workflows.
when_to_use_negative:
- Input is already a feature table or normalized intensity matrix (skip directly to statistical filtering or annotation).
- Raw data are already in mzML and do not require centroiding (use XCMS + CAMERA only, bypass ProteoWizard).
- Data come from a spectral library or reference database rather than raw samples (this skill targets discovery of unknown features, not library matching).
edam_operation: http://edamontology.org/operation_3215
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: ProteoWizard
  role: Converts raw vendor LC–HRMS spectra to centroided mzML format for downstream XCMS processing
- name: XCMS
  role: Detects peaks, aligns retention times (orbiwarp), and groups features across samples using IPO-optimized parameters (centwave, density grouping)
- name: IPO
  role: Optimizes XCMS parameters (peakwidth, ppm, gapInit, etc.) separately for positive and negative ionization modes
- name: CAMERA
  role: Annotates and groups adducts and isotopes (findIsotopes, findAdducts, groupCorr); removes redundant peaks to reduce feature count by ~60%
- name: incubatoR
  role: Wrapper and automation layer for the complete preprocessing pipeline (XCMS, CAMERA, statistics, metabolite filtering) on HPC clusters; provides R and bash scripts for reproducible job submission
  repo: https://github.com/chufz/incubatoR
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
    - outputs/pesticide_full_2026-05-10_v2/skills/mass-spectrometry-data-preprocessing/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/mass-spectrometry-data-preprocessing/skill.md
    merged_at: '2026-05-25T07:15:31.008662+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/mass-spectrometry-data-preprocessing@sha256:3e34c7ce5f4eeeb510d2a9fff1c516e95dff2429e2b513f58e5c947efee0c25a
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# mass-spectrometry-data-preprocessing

## Summary

Converts raw LC–HRMS data to centroided mzML format and applies feature detection, alignment, and retention-time correction to generate a normalized feature table with m/z values, retention times, and per-sample intensities. This is the foundation for downstream metabolite discovery and annotation in high-throughput screening workflows.

## When to use

When you have raw vendor LC–HRMS files from a metabolomic or xenobiotic screening experiment and need to detect, align, and quantify features (potential metabolites) across multiple samples and replicates. Specifically, apply this skill when you have incubated replicate samples, reference standards, negative controls, and blank injections that require unified feature space construction before statistical filtering or annotation.

## When NOT to use

- Input is already a feature table or normalized intensity matrix (skip directly to statistical filtering or annotation).
- Raw data are already in mzML and do not require centroiding (use XCMS + CAMERA only, bypass ProteoWizard).
- Data come from a spectral library or reference database rather than raw samples (this skill targets discovery of unknown features, not library matching).

## Inputs

- Raw vendor mass spectrometry files (raw, .d, .raw formats)
- XCMS parameter settings (settings_xcms.yaml with IPO-optimized values per ionization mode)
- CAMERA parameter settings (settings_camera.yaml)
- Sample class file (class.csv with sample group assignments: incubated, reference, control, blank)
- Centroided mzML files (post-ProteoWizard conversion)

## Outputs

- xcms.rds (xcmsSet R object with detected peaks, aligned retention times, and grouped features)
- camera.rds (CAMERA output with adduct and isotope annotations)
- metadata.tsv (CAMERA metadata for features: componentID, m/z, retention time, adduct type)
- peaklist.tsv (normalized intensity matrix: rows = features [mass@RT], columns = samples)

## How to apply

First, convert raw mass spectra to centroided mzML format using ProteoWizard (v3.0.18265 or equivalent). Load the resulting mzML files into XCMS (v3.8) with IPO-optimized parameters: for positive mode use peakwidth 12.32–40, ppm 11.75, and for negative mode peakwidth 25.3–76, ppm 7; apply centwave peak detection, orbiwarp retention-time correction, and density-based grouping. Export the xcmsSet and pass it to CAMERA (v1.40) with groupFWHM perfwwhm 0.6, findIsotopes mzabs 0.001, and groupCorr cor eic th 0.75 to componentize features and remove isotope/adduct clusters. The resulting peaklist.tsv contains normalized intensities per sample; verify that blank subtraction reduced feature count by ~60%, and confirm that fold-change > 4 in at least 2 of 3 replicates is met before downstream filtering. Adapt parameters based on ionization mode (positive/negative stored in separate folders) and sample structure (incubated_R[1-3], reference_clean, NC, blank patterns).

## Related tools

- **ProteoWizard** (Converts raw vendor LC–HRMS spectra to centroided mzML format for downstream XCMS processing)
- **XCMS** (Detects peaks, aligns retention times (orbiwarp), and groups features across samples using IPO-optimized parameters (centwave, density grouping))
- **IPO** (Optimizes XCMS parameters (peakwidth, ppm, gapInit, etc.) separately for positive and negative ionization modes)
- **CAMERA** (Annotates and groups adducts and isotopes (findIsotopes, findAdducts, groupCorr); removes redundant peaks to reduce feature count by ~60%)
- **incubatoR** (Wrapper and automation layer for the complete preprocessing pipeline (XCMS, CAMERA, statistics, metabolite filtering) on HPC clusters; provides R and bash scripts for reproducible job submission) — https://github.com/chufz/incubatoR

## Evaluation signals

- Feature count reduced by ~60% after blank subtraction and isotope/adduct removal, indicating effective denoising.
- peaklist.tsv contains only features with fold-change > 4 detected in at least 2 of 3 replicates, confirming reproducibility filter applied.
- metadata.tsv includes m/z values within expected ranges, retention times sorted and non-overlapping for same m/z, and adduct/isotope annotations assigned by CAMERA.
- xcms.rds xcmsSet object shows uniform retention-time alignment (orbiwarp distFunc cor) with consistent gap-fill parameters across all samples.
- No features with mass defect shift < −100 mmu or > +50 mmu remain in output (mass defect filter thresholds applied downstream, but signal should be present pre-filter for validation).

## Limitations

- IPO parameter optimization requires representative pilot data; suboptimal parameters will degrade feature detection across the full dataset.
- Centwave peak detection may fail for low-intensity features (< 100 intensity units) or unresolved peaks; prefilter value (3, 100) may need adjustment for different ionization efficiencies.
- Retention-time correction assumes sufficient overlap of features across samples; sparse or highly variable data may yield misaligned peaks.
- CAMERA isotope/adduct grouping may fail for compounds with unusual ionization patterns (e.g., multi-charged ions, exotic adducts); manual curation may be required.
- Low ionization efficiencies or losses during sample extraction can result in missed features even if metabolites are present; abundance filtering (fold-change > 4) may exclude genuine minor metabolites.
- Different pesticide standards or xenobiotic compounds may require compound-specific adjustment of mass defect thresholds (−100 to +50 mmu) and abundance cutoffs.

## Evidence

- [methods] Raw mass spectra were converted to the mzML format and centroided using ProteoWizard26 v3.0.18265 with the vendor library.: "Raw mass spectra were converted to the mzML format and centroided using ProteoWizard26 v3.0.18265 with the vendor library."
- [methods] Feature detection, alignment, and retention time correction were performed using XCMS version 3.8.27: "Feature detection, alignment, and retention time correction were performed using XCMS version 3.8.27"
- [methods] The parameters of XCMS were optimized by the IPO approach.28: "The parameters of XCMS were optimized by the IPO approach.28"
- [methods] All features were componentized using CAMERA.29: "All features were componentized using CAMERA.29"
- [methods] The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−.: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [methods] We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [supplementary] peakwidth 12.32,40 ppm 11.75 [positive mode]; peakwidth 25.3, 76 ppm 7 [negative mode]: "peakwidth 12.32,40 25.3, 76 ppm 11.75 7"
- [readme] XCMS [1] and CAMERA [2]) by `Rscripts/xcms.R` and `Rscripts/camera.R` outputting `xcms.rds`, `camera.rds`, `metadata.tsv`, `peaklist.tsv`: "Peaklist generation (XCMS [1] and CAMERA [2]) by `Rscripts/xcms.R` and `Rscripts/camera.R` outputting `xcms.rds`, `camera.rds`, `metadata.tsv`, `peaklist.tsv`"
- [readme] The sample set should contain measurements of incubated replicates of each compound, a reference standard solution, negative controls and injection/ sample peparation blanks.: "The sample set should contain measurements of incubated replicates of each compound, a reference standard solution, negative controls and injection/ sample peparation blanks."
- [discussion] Some might have been formed but could not have been detected due to low ionization efficiencies...Also, losses during the sample extraction and cleanup procedure are possible: "Some might have been formed but could not have been detected due to low ionization efficiencies...Also, losses during the sample extraction and cleanup procedure are possible"

---
name: lc-ms-feature-detection-and-alignment
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics requires automated detection, alignment, and retention-time correction of LC–HRMS features from centroided mzML files using XCMS with IPO-optimized parameters, followed by isotope/adduct deconvolution via CAMERA to generate a feature table.
when_to_use_negative:
- Input files are already in profile (non-centroided) mode; use ProteoWizard centroiding first.
- Sample set lacks replicate structure or contains only single measurements; retention-time alignment and quality filtering depend on cross-sample consistency.
- Data originate from targeted or scheduled LC–MS/MS with pre-defined inclusion lists; use targeted feature extraction (e.g., XICs) instead of discovery-mode peak detection.
edam_operation: http://edamontology.org/operation_3634
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3172
tools:
- name: XCMS
  role: Peak detection (centwave), retention-time correction (orbiwarp), and peak grouping (density method) on centroided mzML spectra
- name: IPO
  role: Optimization of XCMS parameters (peakwidth, ppm, snthresh, prefilter, bw, mzwid) to maximize feature detection and minimize false positives
- name: CAMERA
  role: Post-hoc deconvolution and grouping of XCMS features into isotope and adduct clusters; assignment of adduct type and mass annotation
- name: ProteoWizard
  role: Conversion of vendor-specific raw mass spectrometry data to centroided mzML format prior to XCMS processing
- name: incubatoR
  role: Integrated R/bash workflow wrapper combining XCMS, CAMERA, statistical filtering (Rvolcano), and downstream metabolite prioritization via mass-defect and abundance filtering
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
    - outputs/pesticide_full_2026-05-10_v2/skills/lc-ms-feature-detection-and-alignment/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/lc-ms-feature-detection-and-alignment/skill.md
    merged_at: '2026-05-25T06:57:01.629120+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/lc-ms-feature-detection-and-alignment@sha256:0c97c344868541ff7a3c4aa5d79e94ec427fad9ceba651342ecaf8fc7e3202c2
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# lc-ms-feature-detection-and-alignment

## Summary

Automated detection, alignment, and retention-time correction of LC–HRMS features from centroided mzML files using XCMS with IPO-optimized parameters, followed by isotope/adduct deconvolution via CAMERA to generate a feature table (m/z, retention time, per-sample intensity) suitable for metabolite screening.

## When to use

You have centroided mzML files from LC–HRMS experiments (ESI+ or ESI− ionization) and need to discover all metabolite features across a cohort of samples in a data-dependent or data-independent acquisition. Apply this skill when raw spectral data require unbiased feature extraction and inter-sample alignment before filtering, annotation, or quantification. Specifically, use it when you have replicated incubations or biomonitoring samples and wish to identify potential metabolites via mass-defect or abundance-based prioritization.

## When NOT to use

- Input files are already in profile (non-centroided) mode; use ProteoWizard centroiding first.
- Sample set lacks replicate structure or contains only single measurements; retention-time alignment and quality filtering depend on cross-sample consistency.
- Data originate from targeted or scheduled LC–MS/MS with pre-defined inclusion lists; use targeted feature extraction (e.g., XICs) instead of discovery-mode peak detection.

## Inputs

- centroided mzML files (from ProteoWizard or equivalent)
- class.csv (sample phenotype/group assignments)
- settings_xcms.yaml (XCMS configuration with IPO-optimized parameters)
- settings_camera.yaml (CAMERA configuration)

## Outputs

- xcms.rds (xcmsSet object with detected and aligned features)
- camera.rds (CAMERA deconvolution result)
- peaklist.tsv (feature table: m/z, retention time, intensities per sample)
- metadata.tsv (CAMERA annotations: isotope, adduct, correlation groups)

## How to apply

Load centroided mzML files using XCMS v3.8 with IPO-optimized parameters (e.g., centwave peak-width 12.32–40 ppm for positive mode, 11.75 ppm tolerance, snthresh 10, orbiwarp retention-time correction with cor distance function). Apply density-based grouping (bw=0.879 positive, 12.4 negative; mzwid=0.01198 positive, 0.003 negative) to align peaks across samples. Next, deconvolute features using CAMERA v1.40 (groupFWHM perfwwhm=0.6, findIsotopes mzabs=0.001, groupCorr cor/eic threshold=0.75, findAdducts for positive/negative polarity) to assign isotope and adduct clusters. The output is an xcmsSet (xcms.rds) and CAMERA-annotated peaklist (peaklist.tsv, metadata.tsv) with m/z, retention time, and normalized intensities per sample and group. Verify by inspecting the number of detected features before and after blank subtraction (~60% reduction expected) and checking that replicate samples show consistent retention times and intensity ranks.

## Related tools

- **XCMS** (Peak detection (centwave), retention-time correction (orbiwarp), and peak grouping (density method) on centroided mzML spectra)
- **IPO** (Optimization of XCMS parameters (peakwidth, ppm, snthresh, prefilter, bw, mzwid) to maximize feature detection and minimize false positives)
- **CAMERA** (Post-hoc deconvolution and grouping of XCMS features into isotope and adduct clusters; assignment of adduct type and mass annotation)
- **ProteoWizard** (Conversion of vendor-specific raw mass spectrometry data to centroided mzML format prior to XCMS processing)
- **incubatoR** (Integrated R/bash workflow wrapper combining XCMS, CAMERA, statistical filtering (Rvolcano), and downstream metabolite prioritization via mass-defect and abundance filtering) — https://github.com/chufz/incubatoR

## Evaluation signals

- Check that detected features span a plausible m/z and retention-time range for the parent compound and expected metabolites; verify no obvious clustering artifacts or extreme outliers in the feature table.
- Confirm that replicate samples show reproducible retention times (intra-sample RT alignment); drift >±30 s may indicate failed orbiwarp correction.
- Verify that isotope and adduct deconvolution reduced the peak count by ~60% (as reported for blank subtraction + isotope/adduct removal); large deviations suggest CAMERA parameters may be misaligned or data quality is poor.
- Cross-check that features assigned to the same CAMERA group (isotope/adduct cluster) have m/z differences consistent with expected patterns (e.g., 13C isotope ~1.003 Da, common adducts [M+H]+, [M+Na]+, [M+NH4]+).
- Inspect volcano plots (fold-change vs. p-value) and mass-defect plots from downstream filtering steps to ensure feature distributions are rational; absence of outliers or extreme values suggests XCMS parameters are well-tuned for the dataset.

## Limitations

- XCMS and CAMERA performance depend critically on IPO parameter optimization; suboptimal parameters may cause missed features (false negatives) or over-detection of noise and adducts (false positives).
- Retention-time alignment (orbiwarp) assumes sufficient overlap in feature patterns across samples; if samples are very different (e.g., distinct metabolite profiles), alignment may fail or produce spurious RT shifts.
- Low-abundance metabolites or those with poor ionization efficiency will be missed; this skill detects features above the snthresh noise threshold but cannot recover signals inherently absent from the raw data.
- Isotope and adduct deconvolution (CAMERA) can conflate true metabolite features if they have similar m/z and retention time; manual verification or additional orthogonal data (e.g., MS/MS fragmentation) may be needed.
- The workflow does not account for in-source fragmentation, unusual adducts (e.g., [M+2Na]2+, [M+K]+), or salt/matrix artifacts; additional filtering steps (mass-defect, abundance fold-change, blank subtraction) are necessary to prioritize true metabolites.

## Evidence

- [methods] Feature detection, alignment, and retention time correction were performed using XCMS version 3.8.: "Feature detection, alignment, and retention time correction were performed using XCMS version 3.8."
- [methods] The parameters of XCMS were optimized by the IPO approach.: "The parameters of XCMS were optimized by the IPO approach."
- [methods] All features were componentized using CAMERA.: "All features were componentized using CAMERA."
- [methods] Raw mass spectra were converted to the mzML format and centroided using ProteoWizard v3.0.18265 with the vendor library.: "Raw mass spectra were converted to the mzML format and centroided using ProteoWizard v3.0.18265 with the vendor library."
- [methods] We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates, which reduced the number of features: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI−: "we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI−"
- [readme] Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering"
- [readme] Peaklist generation (XCMS and CAMERA) by Rscripts/xcms.R and Rscripts/camera.R. INPUT: settings_xcms.yaml, class.csv, globalvar.sh. OUTPUT: xcms.rds. INPUT: settings_camera.yaml, xcms.rds, globalvar.sh. OUTPUT: camera.rds, metadata.tsv, peaklist.tsv: "Peaklist generation (XCMS [1] and CAMERA [2]) by `Rscripts/xcms.R` and `Rscripts/camera.R`. OUTPUT: `xcms.rds`. OUTPUT: `camera.rds`, `metadata.tsv`, `peaklist.tsv`"

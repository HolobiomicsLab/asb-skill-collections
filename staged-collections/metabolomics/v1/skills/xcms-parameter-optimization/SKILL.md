---
name: xcms-parameter-optimization
description: Optimize XCMS feature detection, alignment, and retention time correction parameters using the IPO algorithm to maximize sensitivity and specificity in LC–HRMS metabolomics workflows. This skill applies data-driven parameter tuning to centroided mzML files before peak picking, ensuring robust detection of low-abundance metabolite features across replicate samples.
when_to_use_negative:
- Input mzML files are already profile-mode (not centroided); XCMS requires centroided spectra—use ProteoWizard to centroid first.
- Your sample set lacks replicate structure or quality controls (e.g., reference standards, blanks); IPO requires examples of true peaks to optimize against.
- Feature table is already generated; parameter optimization is a preprocessing step that must occur before peak detection, not after.
edam_operation: http://edamontology.org/operation_3629
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: XCMS
  role: Core feature detection, peak alignment, and retention time correction engine; processes centroided mzML and outputs xcmsSet with optimized parameters
  repo: https://bioconductor.org/packages/xcms/
- name: IPO
  role: Parameter optimization package; systematically searches XCMS parameter space to maximize feature detection accuracy using known reference compounds
  repo: https://bioconductor.org/packages/IPO/
- name: ProteoWizard
  role: Converts raw vendor mass spectra formats to centroided mzML before XCMS processing
- name: CAMERA
  role: Post-XCMS componentization of features; groups adducts, isotopes, and in-source fragments for downstream filtering
  repo: https://bioconductor.org/packages/CAMERA/
- name: R
  role: Language environment for running XCMS, IPO, and CAMERA workflows; version 3.6.1 used in this study
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
    - outputs/pesticide_full_2026-05-10_v2/skills/xcms-parameter-optimization/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/xcms-parameter-optimization/skill.md
    merged_at: '2026-05-25T07:15:30.999189+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/xcms-parameter-optimization@sha256:30957d372b9de96545a8157fc77c3e9e82f72931ff773cbdcf45c3a2361937b0
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# xcms-parameter-optimization

## Summary

Optimize XCMS feature detection, alignment, and retention time correction parameters using the IPO algorithm to maximize sensitivity and specificity in LC–HRMS metabolomics workflows. This skill applies data-driven parameter tuning to centroided mzML files before peak picking, ensuring robust detection of low-abundance metabolite features across replicate samples.

## When to use

Apply this skill when you have centroided mzML files from LC–HRMS experiments (e.g., ESI+ and ESI− modes) and need to detect metabolite features across multiple replicates with high confidence. Use IPO-optimized parameters when the XCMS default settings are insufficient to resolve low-intensity metabolite signals or when you have reference compounds with known m/z and retention time values to validate parameter performance. This is especially important in biomonitoring studies where metabolite feature detection must balance sensitivity (recovering true metabolites) and specificity (minimizing noise and artifacts).

## When NOT to use

- Input mzML files are already profile-mode (not centroided); XCMS requires centroided spectra—use ProteoWizard to centroid first.
- Your sample set lacks replicate structure or quality controls (e.g., reference standards, blanks); IPO requires examples of true peaks to optimize against.
- Feature table is already generated; parameter optimization is a preprocessing step that must occur before peak detection, not after.

## Inputs

- Centroided mzML files (from LC–HRMS; ESI+ and ESI− stored in separate folders)
- Class file (CSV) defining sample type (incubated_replicate, reference_standard, blank, negative_control)
- Parent compound m/z and retention time values (for validation)
- XCMS settings template (YAML) with initial parameter bounds

## Outputs

- Optimized XCMS parameter set (documented in YAML or parameter table)
- xcmsSet object (RData) containing detected features with m/z, retention time, and per-sample intensities
- Feature metadata table (m/z, retention time, mean intensity, SD, RSD, fold-change)
- Peaklist TSV with m/z@retention time identifiers and normalized feature intensities

## How to apply

Load centroided mzML files and a class file defining sample groups (incubated replicates, reference standards, blanks) into XCMS v3.8. Use the IPO package to systematically search parameter space for centwave peak picking (e.g., peakwidth, ppm, noise, snthresh), orbiwarp retention time correction (distFunc, profStep, center, response, gapInit, factorDiag, factorGap), and density-based grouping (bw, mzwid, minfrac, minsamp). IPO optimizes these parameters by maximizing the number of features that match known standards while minimizing false positives. Once optimal parameters are identified (documented in a YAML configuration file), apply them uniformly across all samples in your dataset. The resulting xcmsSet object should contain m/z values, retention times, and per-sample intensity matrices ready for downstream filtering. Validate parameter success by confirming that known reference compound peaks are detected with expected retention times and that replicate samples show high correlation in feature intensity profiles.

## Related tools

- **XCMS** (Core feature detection, peak alignment, and retention time correction engine; processes centroided mzML and outputs xcmsSet with optimized parameters) — https://bioconductor.org/packages/xcms/
- **IPO** (Parameter optimization package; systematically searches XCMS parameter space to maximize feature detection accuracy using known reference compounds) — https://bioconductor.org/packages/IPO/
- **ProteoWizard** (Converts raw vendor mass spectra formats to centroided mzML before XCMS processing)
- **CAMERA** (Post-XCMS componentization of features; groups adducts, isotopes, and in-source fragments for downstream filtering) — https://bioconductor.org/packages/CAMERA/
- **R** (Language environment for running XCMS, IPO, and CAMERA workflows; version 3.6.1 used in this study)

## Evaluation signals

- Reference compound peaks (parent pesticides) are detected at expected m/z values (within ±8 ppm mass accuracy) and expected retention times across all replicates; no false positives in blank samples.
- Replicate feature intensity profiles show high correlation (Pearson r > 0.75) across incubated samples, indicating reproducible peak detection.
- Feature intensity distribution shows expected fold-change pattern: incubated samples have >4-fold higher mean intensity than blanks and reference standards (signal-to-noise > 10, as per snthresh parameter).
- Mass defect shift of detected features clusters around expected values (e.g., oxidized metabolites within −100 to +50 mmu relative to parent); outliers suggest parameter overfitting or artefacts.
- Total feature count after IPO optimization and subsequent blank subtraction + isotope/adduct removal reduces raw peak list by ~60%, consistent with the study's reported filtering efficiency.

## Limitations

- IPO parameter optimization is computationally expensive and requires known reference compounds with high confidence; optimization may fail or overfit if reference data are contaminated or poorly annotated.
- Optimized parameters are data-set-specific; parameters derived from one instrument or ionization mode may not transfer to different LC–HRMS platforms or ESI polarities without re-optimization.
- XCMS feature detection is sensitive to baseline noise and chromatographic variation; poor sample preparation, instrument calibration drift, or uncontrolled pH/temperature can cause parameter-optimized settings to miss features or produce false positives.
- Some predicted metabolites (e.g., from BioTransformer) may not be detected despite parameter optimization due to low ionization efficiency, neutral loss during extraction, or metabolite instability—parameter tuning cannot compensate for biological/chemical factors.
- For compounds with complex metabolite pools or highly variable retention times (e.g., polymorphic lipids), a single parameter set may not optimally resolve all features; variable strictness filtering in downstream steps may be needed.

## Evidence

- [methods] Feature detection, alignment, and retention time correction were performed using XCMS version 3.8.: "Feature detection, alignment, and retention time correction were performed using XCMS version 3.8."
- [methods] The parameters of XCMS were optimized by the IPO approach.: "The parameters of XCMS were optimized by the IPO approach."
- [methods] Raw mass spectra were converted to the mzML format and centroided using ProteoWizard v3.0.18265: "Raw mass spectra were converted to the mzML format and centroided using ProteoWizard26 v3.0.18265 with the vendor library."
- [other] XCMS version 3.8 with IPO-optimized parameters successfully processed the deposited mzML files and generated feature data that enabled assignment of 91 unambiguous molecular formulas to 82 prioritized features in ESI+ and 39 in ESI− across 22 pesticides.: "XCMS version 3.8 with IPO-optimized parameters successfully processed the deposited mzML files and generated feature data that enabled assignment of 91 unambiguous molecular formulas to 82"
- [readme] Peaklist generation (XCMS and CAMERA) with INPUT settings_xcms.yaml and OUTPUT xcms.rds: "Peaklist generation (XCMS [1] and CAMERA [2]) by `Rscripts/xcms.R` and `Rscripts/camera.R` INPUT: `settings_xcms.yaml`, `class.csv`, `globalvar.sh` OUTPUT: `xcms.rds`"
- [supplementary] XCMS parameters documented in Table S3 include centwave method with specific peakwidth, ppm, noise, snthresh, mzdiff, and prefilter values optimized for positive and negative modes.: "xcms[v3.8] peakpicking method centwave peakwidth 12.32,40 25.3, 76 ppm 11.75 7"

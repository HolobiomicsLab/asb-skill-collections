---
name: feature-table-reduction-and-quality-control
description: Use when working in the metabolomics domain to reduce dimensionality and noise in LC-MS and GC-MS untargeted lipidomics feature tables by applying sequential statistical and chemical filters such as blank subtraction and isotope/adduct removal.
when_to_use_negative:
- Do not apply this skill if the input feature table is already a curated target list of known metabolites; this skill is for exploratory discovery, not targeted confirmation.
- Do not use if you lack biological replicates or negative control samples; the replication and fold-change criteria require comparison groups.
- Do not apply if the sample set contains structurally related compounds (e.g. atrazine, terbuthylazine, terbutryn) without first removing shared metabolites to avoid false exclusions in the control group.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0629
- http://edamontology.org/topic_2258
- http://edamontology.org/topic_3172
tools:
- name: XCMS
  role: Feature detection, alignment, and retention-time correction prior to filtering and componentization
- name: CAMERA
  role: Componentization of features to identify and annotate isotope and adduct peaks for removal
- name: ProteoWizard
  role: mzML format conversion and centroiding of raw mass spectra before XCMS processing
- name: R v3.6.1
  role: Statistical computation environment for automated fold-change calculation, filtering, and visualization
  repo: https://github.com/chufz/incubatoR
- name: incubatoR
  role: Complete automated workflow pipeline implementing blank subtraction, abundance filtering, mass defect/difference filtering, and output generation
  repo: https://github.com/chufz/incubatoR
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-table-reduction-and-quality-control/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/feature-table-reduction-and-quality-control/skill.md
    merged_at: '2026-05-25T07:33:56.485831+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/feature-table-reduction-and-quality-control@sha256:e1969da7ba75484c919f4cfa64c3b2c996bb38bd579323d1f7ec1c8e8d83a498
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# feature-table-reduction-and-quality-control

## Summary

This skill reduces the dimensionality and noise of LC–HRMS feature tables by applying sequential statistical and chemical filters (blank subtraction, isotope/adduct removal, fold-change thresholding, replication criteria, mass defect and mass difference boundaries) to prioritize putative metabolite features for downstream structure elucidation. It is essential for distinguishing true metabolic transformation products from background noise, matrix effects, and instrumental artifacts in high-throughput in vitro incubation studies.

## When to use

Apply this skill after XCMS/CAMERA feature detection and componentization when you have a feature table from pesticide or xenobiotic incubation samples measured against negative controls (S9 + NADPH), and you need to reduce false positives and retain only high-confidence metabolite candidates for MS/MS extraction and molecular formula annotation. Use it specifically when you have biological replicates (≥2) of incubated samples and corresponding blank/control measurements, and when you aim to identify transformation products with fold-change enrichment in incubated groups.

## When NOT to use

- Do not apply this skill if the input feature table is already a curated target list of known metabolites; this skill is for exploratory discovery, not targeted confirmation.
- Do not use if you lack biological replicates or negative control samples; the replication and fold-change criteria require comparison groups.
- Do not apply if the sample set contains structurally related compounds (e.g. atrazine, terbuthylazine, terbutryn) without first removing shared metabolites to avoid false exclusions in the control group.

## Inputs

- mzML-formatted LC–HRMS raw spectra files (in separate Pos/Neg folders for ionization modes)
- XCMS peaklist (peaklist.tsv with m/z, retention time, intensity per sample)
- CAMERA componentized features (camera.rds or metadata.tsv with isotope/adduct annotations)
- Sample classification file (class.csv mapping file names to sample groups: incubated replicates, negative controls, blanks, reference standards)
- Parent pesticide m/z value and retention time
- Mass defect thresholds (−100 to +50 mmu)
- Fold-change cutoff (e.g. FC > 4) and replication criteria (≥2 of 3 replicates)

## Outputs

- Reduced feature table (Metabolites.txt) containing only features meeting FC > 4, replication, mass defect, and mass difference criteria
- Visualization plots: volcano plot (p-value vs. log2 fold-change), mass defect plot (mmu shift vs. m/z), feature retention-time/m/z scatter
- List of removed features and removal reasons (isotope, adduct, blank contamination, low FC, mass defect/difference violation)
- Prioritized peak identifiers (mass@retention_time) for downstream EIC and MS/MS extraction

## How to apply

Begin by blank subtraction: compare mean intensity of each feature in incubated samples to injection and sample blanks, removing features with higher mean intensity in blanks. Next, remove isotope and adduct peaks using CAMERA's findIsotopes, groupCorr (correlation threshold 0.75), and findAdducts functions. Then apply the abundance filter by calculating fold-change (FC) for each feature as FC = (mean intensity of incubated replicates) / (mean intensity of negative control S9 + NADPH), retaining only features with FC > 4 that are detected in at least two of three biological replicates. Apply mass defect filtering (retain features with mass defect shift between −100 and +50 mmu relative to parent compound) to exclude unlikely chemical transformations. Remove features with m/z difference > +50 u from the parent pesticide, as these suggest conjugation rather than core metabolism. Finally, subtract standard impurities by comparing incubated sample intensities to intensities in pure pesticide standard at the same concentration. The workflow outputs a reduced feature table typically containing 40% of the original features, prioritized for MS/MS acquisition and molecular formula assignment.

## Related tools

- **XCMS** (Feature detection, alignment, and retention-time correction prior to filtering and componentization)
- **CAMERA** (Componentization of features to identify and annotate isotope and adduct peaks for removal)
- **ProteoWizard** (mzML format conversion and centroiding of raw mass spectra before XCMS processing)
- **R v3.6.1** (Statistical computation environment for automated fold-change calculation, filtering, and visualization) — https://github.com/chufz/incubatoR
- **incubatoR** (Complete automated workflow pipeline implementing blank subtraction, abundance filtering, mass defect/difference filtering, and output generation) — https://github.com/chufz/incubatoR

## Evaluation signals

- Check that the reduced feature table retains only features with fold-change ≥ 4 and presence in ≥ 2 of 3 replicates (verify via peaklist comparison before/after filtering).
- Verify isotope and adduct peaks are absent from the output by cross-referencing CAMERA componentization annotations and checking that all features in Metabolites.txt have unique m/z and retention times (no redundant isotope/adduct clusters).
- Confirm that features with mass defect shifts outside the −100 to +50 mmu window are not included, and all remaining features fall within the acceptable mass difference range (Δm/z ≤ +50 u to parent).
- Validate that blank-subtracted features show mean intensity in incubated samples significantly higher than in injection/sample blanks and negative controls (visualize in volcano and diffplot outputs).
- Confirm that approximately 40% of the original feature count remains post-filtering (typical reduction from ~120–150 features down to ~50–60 prioritized metabolites), consistent with the article's ~60% reduction from blank subtraction and filtering steps.

## Limitations

- Some predicted metabolites cannot be detected due to low ionization efficiencies or losses during sample extraction/cleanup; the skill can only filter and prioritize observable features.
- The workflow does not detect metabolites formed by reduction reactions (dehydrogenation), consecutive hydroxylations, or weak bond breaking if these modifications fall outside the mass defect and mass difference thresholds; thresholds may need adjustment for specific compound classes.
- Features from structurally similar pesticides that share metabolites may be incorrectly excluded from controls if the shared metabolite is also a true product of the incubated pesticide; manual curation or per-compound filtering may be required.
- Incubation time (3 hours) may not be sufficient to capture slow or multi-step metabolic transformations observed in vivo or reported in mammalian registration dossiers; only features detectable within the assay timeframe are prioritized.
- The generic fold-change cutoff (FC > 4) and replication criteria (≥2 of 3) may need adaptation for low-abundance metabolites or compounds with high inter-replicate variability; the workflow documentation notes that filtering strictness can be adjusted.

## Evidence

- [methods] blank_subtraction
- [methods] isotope_adduct_removal
- [methods] abundance_filter_definition
- [methods] mass_defect_filter_definition
- [methods] mass_difference_filter_definition
- [methods] fold_change_reduction_magnitude
- [readme] workflow_overview_from_readme
- [methods] standard_impurity_removal
- [supplementary] camera_parameters
- [discussion] filtering_adaptability
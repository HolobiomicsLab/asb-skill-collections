---
name: lcms-target-visibility-screening
description: Use when after loading centroided .mzML LC–MS runs and before executing full peak detection and integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - TARDIS
  - Spectra
  - xcms
  - R
  - MsExperiment
  - knitr
  - ProteoWizard
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- R package for *TArgeted Raw Data Integration In Spectrometry*
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms` package
- Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object
- knitr::include_graphics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-target-visibility-screening

## Summary

A diagnostic preprocessing step in targeted LC–MS metabolomics that uses TARDIS screening mode to verify that all intended target compounds (internal standards and endogenous metabolites) are detectable within their expected m/z and retention time windows before launching full peak detection and integration. This step ensures data quality and prevents wasted computational effort on targets absent from the sample.

## When to use

After loading centroided .mzML LC–MS runs and before executing full peak detection and integration. Use this skill when you have a defined target list (compound ID, theoretical m/z, expected retention time, ionization polarity) and need to confirm that all 10+ target analytes produce ion signals in the expected mass and chromatographic windows across your sample batch. Particularly important for multi-batch QC workflows where target visibility may vary by instrument state or sample matrix.

## When NOT to use

- Input files are already in profile (non-centroided) mode — centroiding must be applied first via ProteoWizard MSConvert or equivalent
- Target list lacks expected retention time values or ionization polarity annotations — screening mode requires these parameters to define search windows
- You are reprocessing a batch where target visibility has already been validated in a prior screening step; skip to full peak detection mode (screening_mode=FALSE) to save time

## Inputs

- centroided .mzML LC–MS run files (14+ runs per batch)
- target list data.frame with columns: compound ID, compound name, theoretical m/z, expected retention time (minutes), ionization polarity
- Spectra object or MsExperiment object loaded from .mzML files

## Outputs

- extracted ion chromatogram (EIC) PNG plots for each target (one plot per target per run or summary)
- diagnostic QC output folder (e.g., output/screening/Diagnostic_QCs_Batch_1/) containing visualizations
- preliminary assessment of target visibility across the batch (pass/fail or adjusted window parameters)

## How to apply

Load centroided .mzML LC–MS runs as Spectra objects (or via MsExperiment) along with a data.frame target list containing compound ID, name, theoretical m/z, expected RT in minutes, and ionization polarity. Execute tardisPeaks() with screening_mode=TRUE; the function automatically applies polarity filtering and screens for target visibility within defined m/z and retention time windows without performing peak detection. Inspect the resulting extracted ion chromatogram (EIC) PNG plots saved to the diagnostic output folder for each target to visually confirm peak presence, shape, and signal-to-noise. If any target shows absent or ambiguous signal, adjust m/z or RT window tolerances and re-screen before proceeding to full peak detection (screening_mode=FALSE). The rationale is that this rapid visual triage prevents integration of noise or false positives and validates that your target list parameters are fit for the current batch.

## Related tools

- **TARDIS** (Main package; implements tardisPeaks() function with screening_mode parameter for target visibility assessment and EIC generation) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads MS data as Spectra objects for easy integration with TARDIS and retention time correction workflows)
- **xcms** (Provides established retention time correction algorithm used internally by TARDIS)
- **MsExperiment** (Alternative input format to file paths; allows passing structured experiment object to TARDIS)
- **ProteoWizard** (File conversion tool (MSConvert) to convert raw instrument files to centroided .mzML format before TARDIS input)

## Examples

```
library(TARDIS); targets <- data.frame(compound_id=1:10, name=c('IS1','IS2','IS3','IS4','IS5','met1','met2','met3','met4','met5'), mz=c(250.1,300.2,350.3,400.4,450.5,500.6,550.7,600.8,650.9,701.0), rt=c(2.5,3.1,4.2,5.0,6.1,7.3,8.5,9.2,10.1,11.0), polarity=rep('positive',10)); result <- tardisPeaks(file_list, targets, screening_mode=TRUE, output_folder='output/screening/')
```

## Evaluation signals

- All 10 target EIC plots are generated and saved to the output folder without errors or missing targets
- Visual inspection of EIC plots confirms peak presence (non-zero intensity) within the expected retention time window for each target in at least 80% of QC runs
- Peak annotation in EIC plots shows correct m/z assignment (within theoretical m/z ± defined tolerance) and clean ion signal with baseline separation
- No targets show ambiguous, split, or noise-contaminated signals that would preclude reliable integration in the next peak detection step
- Diagnostic folder structure and file naming convention (e.g., target_compound_name_run_ID.png) are consistent and complete

## Limitations

- Screening mode is a visual/qualitative step; it does not calculate quantitative metrics (area under peak, max intensity, SNR) — these are reserved for full peak detection mode
- Success depends on accurate target list parameters (m/z, RT, polarity); systematic errors in these inputs will cause false negatives (targets marked invisible when they are present)
- EIC visualization quality may be reduced for low-abundance targets or samples with high matrix background; manual inspection is required to interpret ambiguous signals
- No changelog is provided in the repository, so version-to-version parameter or output format changes must be inferred from vignettes or GitHub commit history

## Evidence

- [intro] perform a screening step to check if our targets are visible within our m/z and RT windows: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [other] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected: "tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected"
- [intro] Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] compound ID, a unique identifier; A compound Name; Theoretical or measured m/z; Expected RT (in minutes); A column that indicates the polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"

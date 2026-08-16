---
name: chromatographic-peak-annotation-visualization
description: Use when after running tardisPeaks() with screening_mode=TRUE on centroided .mzML LC-MS data, when you need to visually inspect whether the 10 target compounds (internal standards and endogenous metabolites) were correctly detected within their expected m/z and retention time windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - TARDIS
  - Spectra
  - xcms
  - R
  - MsExperiment
  - knitr
  - ProteoWizard (MSConvert)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Chromatographic Peak Annotation and Visualization

## Summary

Generate and inspect extracted ion chromatogram (EIC) plots with annotated peaks for targeted LC-MS compounds, enabling visual quality control of peak detection, integration, and retention time alignment across sample batches. This skill bridges automated peak detection with human-interpretable diagnostic plots for targeted metabolomics and lipidomics workflows.

## When to use

After running tardisPeaks() with screening_mode=TRUE on centroided .mzML LC-MS data, when you need to visually inspect whether the 10 target compounds (internal standards and endogenous metabolites) were correctly detected within their expected m/z and retention time windows. Use this skill to generate diagnostic QC plots before proceeding to quantitative integration in non-screening mode, especially when validating a new target list or batch of samples.

## When NOT to use

- Your input data is already in profile (non-centroided) mode; TARDIS requires centroided .mzML files.
- You are performing untargeted or discovery-mode metabolomics without a predefined target list; this skill is designed for targeted screening only.
- You have already obtained quantitative integration results and need statistical comparison; use this skill earlier in the workflow, during the screening phase.

## Inputs

- centroided .mzML LC-MS runs (14+ runs typical)
- target list data.frame with columns: compound ID, compound name, theoretical m/z, expected retention time (minutes), ionization polarity
- Spectra objects or file paths to .mzML files loaded into TARDIS environment

## Outputs

- PNG files containing extracted ion chromatogram (EIC) plots with annotated peaks for each target compound
- plots saved to output/screening/Diagnostic_QCs_Batch_N/ folder
- visual quality control diagnostic plots suitable for inspection and reporting

## How to apply

Execute tardisPeaks() with screening_mode=TRUE on your loaded Spectra objects and target list data.frame (containing compound ID, name, theoretical m/z, expected RT in minutes, and ionization polarity). The function automatically applies polarity filtering and generates EIC plots for each of the target compounds, saving individual PNG files to the output/screening/Diagnostic_QCs_Batch_N/ folder. Inspect the resulting plots to verify (1) peak visibility within the defined m/z and RT windows, (2) peak annotation accuracy and integration boundaries, and (3) consistency of peak shape and retention time across replicates. The visualization step is essential for detecting method failures (missing signals, interfering peaks, retention time drift) before committing to full quantitative analysis.

## Related tools

- **TARDIS** (R package that executes tardisPeaks() function with screening_mode=TRUE to detect peaks and generate EIC plots for all target compounds) — https://github.com/pablovgd/TARDIS
- **Spectra** (Bioconductor package for loading and representing MS data as Spectra objects, the native input format for TARDIS)
- **xcms** (Provides retention time correction algorithms used internally by TARDIS for RT alignment)
- **MsExperiment** (Alternative input container for MS data to TARDIS; can be used instead of file paths)
- **ProteoWizard (MSConvert)** (Converts vendor-specific LC-MS raw files to .mzML format and applies centroiding prior to TARDIS input)

## Examples

```
library(TARDIS); results <- tardisPeaks(mzml_files = list.files(path='./data', pattern='\.mzML$', full.names=TRUE), target_list = targets_df, screening_mode = TRUE, output_folder = './output/screening')
```

## Evaluation signals

- All 10 target compounds (5 internal standards + 5 endogenous metabolites) have corresponding PNG files in the output/screening/Diagnostic_QCs_Batch_N/ folder.
- Each EIC plot shows a clearly annotated peak within the expected m/z ± tolerance and retention time ± tolerance window defined in the target list.
- Peak annotation includes visible integration boundaries and does not overlap with unexpected peaks in the chromatographic background.
- Retention time consistency across replicates is visually confirmed; peaks for the same compound cluster within a narrow RT range (typically < 0.5 min drift across a batch).
- Diagnostic plots are suitable for inclusion in QC reports and enable rapid identification of compounds with missing or degraded signals before proceeding to quantitative integration.

## Limitations

- Screening-mode visualization does not provide quantitative metrics (AUC, max intensity, SNR, peak correlation); these require a separate non-screening-mode run with tardisPeaks(screening_mode=FALSE).
- EIC plot quality and interpretability depend on the quality of centroiding and the accuracy of the input target list (m/z, RT, polarity); incorrect target parameters will produce uninformative or misleading plots.
- Visual inspection of PNG files is a manual, subjective step; no automated quality scoring is performed at the visualization stage. Formal acceptance criteria must be defined by the analyst.
- The package requires R ≥ 4.4.0 and BiocManager 3.20 with specific dependency versions; installation can be prone to timeout issues on slow connections.

## Evidence

- [other] Generate extracted ion chromatogram (EIC) plots for each of the 10 targets with peak annotation and save as individual PNG files to the output/screening/Diagnostic_QCs_Batch_1/ folder for visual inspection of target detection.: "Generate extracted ion chromatogram (EIC) plots for each of the 10 targets with peak annotation and save as individual PNG files to the output/screening/Diagnostic_QCs_Batch_1/ folder for visual"
- [other] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and integration for each component.: "tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs"
- [other] Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows across all runs, automatically applying polarity filtering.: "Execute tardisPeaks() function with screening_mode=TRUE to detect peaks and screen for target compound visibility within defined m/z and retention time windows"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"

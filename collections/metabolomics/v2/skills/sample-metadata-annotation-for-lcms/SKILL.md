---
name: sample-metadata-annotation-for-lcms
description: Use when when you have loaded centroided .mzML files into a Spectra object and plan to use TARDIS (tardisPeaks) with an MsExperiment object rather than file paths, and you need TARDIS to distinguish QC runs from sample runs for separate quality metric calculation, polarity filtering, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - xcms
  - Spectra
  - MsExperiment
  - TARDIS
  - R
  - knitr
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms` package
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object
- R package for *TArgeted Raw Data Integration In Spectrometry*
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

# sample-metadata-annotation-for-lcms

## Summary

Annotate LC–MS sample metadata (particularly sample type classification as QC vs. sample) within an MsExperiment object to enable TARDIS to perform polarity filtering, QC-stratified quality metrics, and screening-mode target visibility assessment without manual file subsetting.

## When to use

When you have loaded centroided .mzML files into a Spectra object and plan to use TARDIS (tardisPeaks) with an MsExperiment object rather than file paths, and you need TARDIS to distinguish QC runs from sample runs for separate quality metric calculation, polarity filtering, and screening-mode diagnostic output.

## When NOT to use

- You are invoking tardisPeaks() with file paths directly (file-path-based input does not require MsExperiment object construction or sampleData annotation).
- Your LC–MS runs are not stratified into QC and sample cohorts, or you do not need separate quality metrics per cohort.
- The sampleData 'type' column is not populated or is incomplete; TARDIS requires this metadata to function correctly with MsExperiment objects.

## Inputs

- Spectra object loaded from centroided .mzML files
- sampleData data frame with 'type' column (values: 'QC', 'sample', or equivalent run classification)

## Outputs

- MsExperiment object (Spectra + sampleData combination)
- Passed to tardisPeaks() for polarity-filtered, QC-stratified peak integration and screening-mode diagnostics

## How to apply

Create a sampleData data frame with one row per mzML file, including a 'type' column that labels each run as either 'QC' or 'sample' (or other run classifications relevant to your study design). Pass this sampleData data frame when constructing the MsExperiment object together with the Spectra object. TARDIS will use this metadata to automatically filter polarity within tardisPeaks(), compute separate average quality metrics (Max. Int., SNR, peak_cor, points over peak) for QC and sample runs, and generate stratified screening-mode EIC diagnostic plots. The key rationale is that polarity filtering and QC-stratified quality assessment occur internally within TARDIS, requiring the type annotation to be pre-populated in sampleData rather than applied manually to the raw file set.

## Related tools

- **Spectra** (Load and represent MS data from .mzML files as Spectra objects for integration into MsExperiment)
- **MsExperiment** (Container class that combines Spectra object with sampleData metadata for TARDIS input)
- **TARDIS** (Accept annotated MsExperiment object as input to perform polarity filtering, QC-stratified metric calculation, and screening-mode diagnostics) — https://github.com/pablovgd/TARDIS
- **xcms** (Provide retention time correction algorithm used internally by TARDIS)

## Examples

```
library(Spectra); library(MsExperiment); library(TARDIS); spec <- Spectra(c('sample1.mzML','sample2.mzML','qc1.mzML')); sampleData <- data.frame(type=c('sample','sample','QC')); experiment <- MsExperiment(spectra=spec, sampleData=sampleData); tardisPeaks(experiment, targetList=targets, screening_mode=TRUE, outputFolder='./results')
```

## Evaluation signals

- The constructed MsExperiment object successfully passes to tardisPeaks() without errors when screening_mode=TRUE is specified.
- EIC PNG diagnostic plots are generated and saved to the output folder, with content visually matching reference EIC files produced from equivalent file-path-based invocation.
- The results object includes separate tibbles with average quality metrics (Max. Int., SNR, peak_cor, points over peak) for QC and sample cohorts, confirming stratification by sampleData$type.
- Polarity filtering is applied automatically within TARDIS output; inspect the generated EICs and metrics to confirm that only targets matching the polarity annotation are included.
- The output feature table (AUC data frame) contains rows for all targets across all annotated runs, with no missing or incorrectly filtered entries.

## Limitations

- The 'type' column in sampleData must be manually curated or pre-populated before MsExperiment construction; TARDIS does not infer run type from file names or metadata.
- If sampleData$type is incomplete or contains unexpected values, TARDIS may fail to stratify QC and sample metrics correctly.
- No automatic validation of type annotations is documented; users must ensure consistency (e.g., case sensitivity) with TARDIS's internal expectations.

## Evidence

- [other] MsExperiment approach requiring sampleData$type to be populated to distinguish QC from sample runs: "the MsExperiment approach requiring sampleData$type to be populated to distinguish QC from sample runs"
- [other] Create sampleData with type labels (QC, sample) for each mzML file: "Create a sampleData data frame with type labels (e.g., QC, sample) for each mzML file"
- [intro] Polarity filtering is done within TARDIS: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an MsExperiment object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [results] Results include a tibble with average metrics for each target in QC runs: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"

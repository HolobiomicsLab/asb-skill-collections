---
name: targeted-peak-detection-screening-and-validation
description: Use when you have centroided mzML LC–MS data, a curated list of target compounds (with theoretical m/z, expected retention time, and polarity), and you need to confirm target presence and extract quantitative metrics (area under curve, max intensity, signal-to-noise ratio, peak correlation, point.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - xcms
  - Spectra
  - MsExperiment
  - TARDIS
  - R
  - knitr
  - ProteoWizard MSConvert
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Targeted Peak Detection Screening and Validation

## Summary

A two-stage workflow that first screens LC–MS data to confirm visibility of targeted compounds within defined m/z and retention-time windows, then performs automated peak detection, integration, and quality assessment on confirmed targets. This skill validates that targets are detectable before committing to full quantitative analysis.

## When to use

Apply this skill when you have centroided mzML LC–MS data, a curated list of target compounds (with theoretical m/z, expected retention time, and polarity), and you need to confirm target presence and extract quantitative metrics (area under curve, max intensity, signal-to-noise ratio, peak correlation, point count) for each target across multiple runs. Use it when QC and sample runs are annotated in sampleData$type and you need to stratify quality assessment by sample type.

## When NOT to use

- Input files are not centroided or not in mzML format—convert and centroid first.
- Target list lacks polarity annotation or expected retention times—TARDIS requires these to filter and window correctly.
- You are working with untargeted/discovery metabolomics and have not pre-defined a compound list—use untargeted peak detection (e.g., xcms) instead.
- Sample metadata does not distinguish QC from sample runs—QC stratification will not work.

## Inputs

- centroided mzML files (or Spectra object loaded from mzML)
- MsExperiment object (Spectra + sampleData with type annotation)
- target list data frame (columns: compound ID, name, m/z, RT in minutes, polarity)

## Outputs

- data.frame: AUC of each target in each run
- tibble: average metrics for each target in QC runs
- results tables: Max. Int., SNR, peak_cor, points over the peak
- extracted ion chromatogram (EIC) PNG files saved to output folder

## How to apply

Load mzML data as a Spectra object and combine it with annotated sampleData (including type labels: QC vs. sample) into an MsExperiment object. Construct a target list data frame with columns for compound ID, name, theoretical m/z, expected RT (in minutes), and polarity. Execute tardisPeaks() with screening_mode=TRUE to perform a fast visibility check—polarity filtering is applied within TARDIS—generating diagnostic extracted ion chromatograms (EICs) as PNG files. After confirming target visibility in screening plots, re-run tardisPeaks() with screening_mode=FALSE on all runs to trigger full peak detection, integration, and metric calculation. The function automatically outputs results tables (AUC per target per run, average QC metrics, max intensity, SNR, peak correlation, point counts) and EIC visualizations to the specified output folder. Compare screening-mode EIC outputs between MsExperiment and file-path invocations to verify functional equivalence if switching input modality.

## Related tools

- **TARDIS** (main R package that orchestrates screening-mode validation and peak detection; performs polarity filtering, EIC extraction, and metric calculation) — https://github.com/pablovgd/TARDIS
- **Spectra** (loads mzML files as Spectra objects for integration with MsExperiment)
- **MsExperiment** (wraps Spectra object and sampleData (with type annotation) into unified input for tardisPeaks())
- **xcms** (provides retention-time correction algorithm used within TARDIS)
- **ProteoWizard MSConvert** (file format conversion to mzML and centroiding (preprocessing step before TARDIS))

## Examples

```
library(TARDIS); library(Spectra); library(MsExperiment)
spectra_obj <- readMsExperiment('path/to/mzML/files/')
sampleData(spectra_obj)$type <- c('QC','sample','QC','sample')
target_list <- data.frame(ID=1:5, name=c('Compound1','Compound2',...), mz=c(200.1,250.3,...), rt=c(5.2,7.8,...), polarity=rep('positive',5))
results <- tardisPeaks(lcmsData=spectra_obj, targetList=target_list, screening_mode=TRUE, outputPath='./screening_output/')
```

## Evaluation signals

- Screening-mode EIC PNG files are generated and visually confirm target compound presence within expected m/z and RT windows.
- EIC outputs from MsExperiment-based invocation match (identical file set and visual content) reference EICs from equivalent file-path-based tardisPeaks() call.
- Results data.frame contains AUC values for all targets in all runs with no missing entries where targets were visible in screening.
- QC tibble contains average metrics (Max. Int., SNR, peak_cor, points) stratified by target, with SNR and peak_cor values within expected ranges for your instrument/method.
- Peak detection and integration succeed without errors when screening_mode=FALSE after successful screening; no spurious or zero-intensity peaks in results.

## Limitations

- Input files must be centroided mzML; non-centroided or other formats require preprocessing.
- Polarity filtering is automatic within TARDIS and cannot be disabled—ensure target polarity annotations are correct.
- Screening mode provides only visibility confirmation, not quantitative metrics; full peak detection requires a second run with screening_mode=FALSE.
- EIC and results quality depend on correct specification of m/z windows and RT windows; too-narrow windows may cause targets to be missed.
- No changelog available in the public repository documentation to track breaking changes between versions.

## Evidence

- [other] Do MsExperiment objects with annotated sampleData$type produce identical screening-mode EIC diagnostic outputs compared to file-path-based invocation?: "The tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated to distinguish"
- [intro] Screening mode workflow and target list requirements.: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Peak detection occurs after screening validation.: "perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [intro] Polarity filtering is automatic within TARDIS.: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Target list data frame structure requirements.: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [results] Output metrics and visualization.: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
- [results] QC stratification output.: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
- [results] Complete metric suite and EIC output.: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] Input file format requirement.: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] MsExperiment integration with Spectra and sample data.: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"

---
name: spectral-data-object-construction-and-integration
description: Use when you have centroided mzML files from LC–MS experiments and need
  to perform targeted metabolomics or lipidomics analysis. Specifically, use it when
  you require polarity filtering, QC-sample stratification, or batch-aware peak detection—all
  of which depend on sampleData$type annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3209
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - xcms
  - Spectra
  - MsExperiment
  - TARDIS
  - R
  - knitr
  - ProteoWizard (MSConvert)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- Alternatively, instead of using file paths as input for TARDIS, the user can also
  use an `MsExperiment` object
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

# Spectral Data Object Construction and Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill encapsulates the process of loading LC–MS raw data (mzML files) into in-memory Spectra objects, annotating them with sample metadata (sampleData), and integrating them into MsExperiment containers for downstream targeted analysis. It bridges raw chromatographic data with structured experimental metadata required by TARDIS and related peak-detection workflows.

## When to use

Apply this skill when you have centroided mzML files from LC–MS experiments and need to perform targeted metabolomics or lipidomics analysis. Specifically, use it when you require polarity filtering, QC-sample stratification, or batch-aware peak detection—all of which depend on sampleData$type annotations (e.g., QC vs. sample run labels) to be embedded in the spectral object before TARDIS invocation.

## When NOT to use

- Input files are not yet centroided or are in profile mode—they must be converted to centroided mzML first.
- sampleData does not include a type column or QC/sample stratification is not needed; in that case, file-path-based TARDIS invocation may be simpler.
- You already have pre-constructed MsExperiment objects from another workflow—no need to rebuild from raw mzML files.

## Inputs

- Centroided mzML files (one per LC–MS run)
- Sample metadata table with run identifiers, type labels (QC/sample), and polarity annotations

## Outputs

- Spectra object containing all loaded MS data
- sampleData data frame with type and metadata columns
- MsExperiment object integrating Spectra and sampleData

## How to apply

Load all centroided mzML files as a single Spectra object using the Spectra package. Construct a parallel sampleData data frame with one row per mzML file, including a mandatory type column (e.g., 'QC' or 'sample') and any other relevant annotations (batch, replicate ID, sample name). Bind the Spectra and sampleData into an MsExperiment object, ensuring row order alignment. Verify that sampleData$type is populated to enable polarity filtering and QC–sample stratification within TARDIS. Pass the MsExperiment object directly to tardisPeaks() in downstream screening or peak-detection steps.

## Related tools

- **Spectra** (Loads mzML files into in-memory spectral objects with lazy evaluation and efficient m/z–intensity indexing)
- **MsExperiment** (Wraps Spectra objects and sampleData metadata into a single container for downstream TARDIS and xcms analysis)
- **xcms** (Provides retention-time correction and peak-detection algorithms that operate on MsExperiment inputs)
- **ProteoWizard (MSConvert)** (Pre-processes raw vendor formats into centroided mzML before Spectra loading)
- **TARDIS** (Consumes MsExperiment objects for targeted peak integration and quality assessment) — https://github.com/pablovgd/TARDIS

## Examples

```
library(Spectra); library(MsExperiment); spectra <- Spectra(c('file1.mzML', 'file2.mzML', 'file3.mzML')); sampleData <- data.frame(type=c('QC','sample','sample')); ms_exp <- MsExperiment(Spectra=spectra, sampleData=sampleData); results <- tardisPeaks(lcmsData=ms_exp, screening_mode=TRUE, targets=target_list, output_folder='./output');
```

## Evaluation signals

- Spectra object is non-empty and contains ms_level, mz, intensity, and rtime columns; length(Spectra) == nrow(sampleData).
- sampleData data frame has one row per mzML file, includes a type column with QC and/or sample labels, and row order matches Spectra file order.
- MsExperiment object is constructible without error: MsExperiment(Spectra = spectra_obj, sampleData = sample_meta).
- tardisPeaks(lcmsData = ms_exp, screening_mode = TRUE, ...) executes without polarity or sample-type errors; EIC PNG outputs are generated for all targets.
- EIC PNG outputs from MsExperiment-based invocation are visually identical to reference EICs from equivalent file-path-based tardisPeaks() invocation.

## Limitations

- Input mzML files must be centroided; profile-mode data will cause incorrect m/z and intensity representation.
- sampleData$type is mandatory for polarity filtering and QC–sample stratification to work correctly; missing type values will bypass filtering logic.
- Row order of sampleData must exactly match the order in which mzML files are loaded into Spectra; misalignment causes incorrect sample-type assignment.
- The Spectra object is lazily evaluated; memory usage scales with file count and spectral density, not file size, so very large experiments may require chunking.
- No changelog documented for TARDIS; version compatibility between Spectra, MsExperiment, xcms, and TARDIS is not formally tracked.

## Evidence

- [intro] loads MS data as `Spectra` objects so it's easily integrated with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [intro] Create sampleData data frame with type labels (e.g., QC, sample) for each mzML file: "Create a sampleData data frame with type labels (e.g., QC, sample) for each mzML file"
- [intro] Construct an MsExperiment object combining the Spectra object and sampleData: "Construct an MsExperiment object combining the Spectra object and sampleData"
- [intro] sampleData$type to be populated to distinguish QC from sample runs: "sampleData$type to be populated to distinguish QC from sample runs"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object: "Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"

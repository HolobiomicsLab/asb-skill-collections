---
name: extracted-ion-electropherogram-generation
description: Use when you have CE-MS raw data (mzML or netCDF format) containing a
  target compound of known m/z ratio and you need to resolve it as a distinct peak
  on the effective mobility scale rather than migration time scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MobilityTransformR
  - Spectra
  - xcms
  - MetaboCoreUtils
  - MSnbase
  - R
  techniques:
  - CE-MS
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("Spectra")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
- The MT of the peak will be determined by `findChromPeaks` from `xcms`.
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# extracted-ion-electropherogram-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate extracted ion electropherograms (EIE) from CE-MS data by transforming migration times to effective mobility scale and isolating specific m/z signals within defined mobility windows. This skill enables reproducible peak visualization and quantification by converting raw electrophoretic separation data into a mobility-normalized coordinate system that accounts for electroosmotic flow variations.

## When to use

Apply this skill when you have CE-MS raw data (mzML or netCDF format) containing a target compound of known m/z ratio and you need to resolve it as a distinct peak on the effective mobility scale rather than migration time scale. This is particularly important when electroosmotic flow variations cause peak drift in migration time, making direct time-based peak comparison unreliable across runs. Use this skill if you are analyzing amino acids, metabolites, or other small ions where effective mobility remains stable within the same electrophoretic system.

## When NOT to use

- Input is already a feature table or peak matrix — this skill is for raw CE-MS signal extraction, not post-processing.
- You only have migration time data and cannot or do not want to apply effective mobility transformation — use direct migration time-based peak detection instead.
- Your CE-MS data is in CE-UV (capillary electrophoresis–UV) format; effective mobility transformation for CE-UV is more straightforward and does not require this specialized approach.

## Inputs

- CE-MS raw data file (mzML or netCDF format)
- Target m/z value (numeric, e.g., 147.112806)
- m/z tolerance window (numeric, in ppm or Da)
- Desired effective mobility range (numeric tuple, mm²/(kV·min))

## Outputs

- Extracted ion electropherogram (chromatogram on µeff axis)
- Peak record table (effective mobility position, peak intensity, peak area)
- Single output file containing both positive and negative effective mobilities

## How to apply

Load CE-MS raw data using Spectra or MSnbase packages, then apply effective mobility transformation using MobilityTransformR to convert migration time coordinates to the µeff scale, accounting for electroosmotic flow variations inherent to the CE system. Extract the ion trace for your target m/z (e.g., m/z 147.112806 for Lysine) with specified mass tolerance and filter the extracted trace to your desired mobility window (e.g., 1000–2500 mm²/(kV·min)) using xcms or MetaboCoreUtils. Generate the extracted ion electropherogram by identifying peak boundaries on the µeff axis, then export peak properties (effective mobility position, peak intensity, peak area) as a data table. The key rationale is that effective mobility transformation produces highly reproducible peaks across runs by normalizing away migration time drift, enabling more reliable quantification and peak alignment than raw migration time alone.

## Related tools

- **MobilityTransformR** (Performs effective mobility transformation of CE-MS data, converting migration time to µeff scale accounting for electroosmotic flow) — https://github.com/LiesaSalzer/MobilityTransformR
- **Spectra** (Loads and manages CE-MS raw data from mzML or netCDF files)
- **MSnbase** (Accesses and manipulates mass spectrometry data structures for ion trace extraction)
- **xcms** (Filters ion traces to specified m/z and mobility windows)
- **MetaboCoreUtils** (Provides utility functions for metabolomics data filtering and transformation)

## Examples

```
# R: Load data, transform to µeff, extract Lysine ion, and generate EIE
library(MobilityTransformR); library(Spectra)
data <- readMSData('lysine_ce_ms.mzML', mode='onDisk')
transformed <- transformEffectiveMobility(data)
eie <- filterMz(transformed, mz=147.112806, ppm=5) %>% filterMobility(min=1000, max=2500)
peakTable <- findPeaks(eie); write.csv(peakTable, 'lysine_eie_peaks.csv')
```

## Evaluation signals

- Extracted ion electropherogram displays a single well-resolved peak or expected multiplet within the specified µeff window (1000–2500 mm²/(kV·min) or user-defined range)
- Peak boundaries on the µeff axis are correctly identified and do not span unrealistic mobility ranges
- Exported peak record table contains three required fields: effective mobility position (mm²/(kV·min)), peak intensity (raw or normalized), and peak area (integrated signal)
- Peak position on µeff scale is stable and reproducible across multiple CE-MS runs of the same compound, with minimal drift compared to migration time-based alignment
- Output file format is a single unified file (not separate files for positive/negative mobilities), confirming MobilityTransformR (not ROMANCE) was used

## Limitations

- Effective mobility transformation for CE-MS is more complex than for CE-UV; implementation requires careful handling of electroosmotic flow corrections specific to the CE system used.
- The skill requires accurate knowledge of the target m/z value and an appropriate mass tolerance window; incorrect m/z selection will extract noise or co-eluting ions instead of the intended analyte.
- Mobility window boundaries (e.g., 1000–2500 mm²/(kV·min)) must be specified a priori; if the window is too narrow, true peaks may be excluded; if too wide, resolution may be lost.
- The transformation assumes a stable electrophoretic system; significant changes in capillary conditioning, buffer composition, or temperature between runs may degrade reproducibility of effective mobility values.

## Evidence

- [intro] Effective mobility transformation produces highly reproducible peaks: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] CE-MS effective mobility transformation lacked R implementation before MobilityTransformR: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] MobilityTransformR unifies output into single file: "However, the outputs are two separate files, each for positive and negative mobilities... the output will be a single file containing both, the positive and negative effective mobilities"
- [other] Workflow step: load CE-MS data and apply transformation: "Load CE-MS raw data (mzML or netCDF) containing Lysine signal using Spectra or MSnbase. 2. Apply effective mobility transformation to convert migration time to µeff scale using MobilityTransformR"
- [other] Workflow step: extract ion trace and export peak record: "Extract the ion trace for m/z 147.112806 with specified tolerance and filter to the mobility window 1000–2500 using xcms or MetaboCoreUtils. 4. Generate the extracted ion electropherogram and"
- [readme] Installation and repository access: "To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")"

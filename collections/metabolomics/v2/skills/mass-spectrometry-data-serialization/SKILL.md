---
name: mass-spectrometry-data-serialization
description: Use when after RAMClustR clustering and molecular weight inference via do.findmain, when you need to export deconvoluted cluster spectra for import into external annotation tools (MSFinder or Sirius).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - RAMClustR
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  - R
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
- The 'mat' contains spectra in .mat format suitable for import into MSFinder software
- The 'ms' contains spectra in .ms format suitable for import into Sirius software
- The 'ms' contains spectra in .ms format suitable for import into Sirius software.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
---

# mass-spectrometry-data-serialization

## Summary

Convert clustered mass spectrometry spectra into standardized file formats (.mat for MSFinder, .ms for Sirius) to enable downstream structural annotation and compound identification in specialized metabolomics software.

## When to use

After RAMClustR clustering and molecular weight inference via do.findmain, when you need to export deconvoluted cluster spectra for import into external annotation tools (MSFinder or Sirius). Trigger: you have a RAMClustR object (RC) with inferred molecular weights and cluster assignments, and you want to perform spectral matching or structure prediction outside RAMClustR.

## When NOT to use

- Input RAMClustR object has not yet completed do.findmain molecular weight inference — serialization requires inferred m/z values.
- You plan to perform all structural annotation within RAMClustR or R environment — external format export is unnecessary if annotation tools are already integrated.
- Output files are intended for human-readable inspection rather than software import — MSP or text formats may be more appropriate.

## Inputs

- RAMClustR clustered object (RC) with completed do.findmain molecular weight inference
- Inferred molecular weights and feature-to-cluster assignments
- Spectral data (m/z, intensity pairs) for each feature or cluster

## Outputs

- .mat files (MSFinder-compatible spectra) in 'mat' subdirectory
- .ms files (Sirius-compatible spectra) in 'ms' subdirectory
- Metadata annotations (retention time, molecular weight) embedded in output files

## How to apply

The do.findmain function automatically creates two subdirectories ('mat' and 'ms') within the existing 'spectrum' directory after inferring molecular weights. For each cluster, the function extracts m/z–intensity pairs and metadata (retention time, molecular weight, cluster assignment), then serializes spectral data into MSFinder-compatible .mat format (written to 'mat' subdirectory) and Sirius-compatible .ms format (written to 'ms' subdirectory). The conversion preserves all feature spectral information without data loss. Verify output by confirming that both subdirectories exist, contain one file per cluster, and that cluster counts match between formats.

## Related tools

- **RAMClustR** (Generates clustered spectra object and infers molecular weights via do.findmain; controls serialization to .mat and .ms formats) — https://github.com/cbroeckl/RAMClustR
- **MSFinder** (Downstream tool that imports .mat format spectra for spectral matching and structure prediction)
- **Sirius** (Downstream tool that imports .ms format spectra for CSI:FingerID structure elucidation)
- **InterpretMSSpectrum** (CRAN package from which do.findmain function was adapted; provides scoring methodology for molecular weight inference)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Two subdirectories ('mat' and 'ms') are created within the 'spectrum' directory after do.findmain execution.
- File count in 'mat' subdirectory equals file count in 'ms' subdirectory, matching the number of clusters in the RAMClustR object.
- .mat files are readable by MSFinder and .ms files by Sirius with no import errors or format corruption.
- Spectral data (m/z–intensity pairs, retention time, molecular weight) are preserved in both output formats with no loss of precision or metadata.
- Cluster identifiers and metadata in serialized files match those in the parent RAMClustR object (RC$ann, RC$SpecAbund).

## Limitations

- Serialization requires prior completion of do.findmain; spectra without inferred molecular weights cannot be exported.
- File format compatibility depends on MSFinder and Sirius version specifications — format schemas may change without warning or changelog documentation.
- No built-in validation or quality metrics for exported spectra — users must verify that spectra conform to downstream software expectations post-export.

## Evidence

- [other] export_structure: "The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory. The 'mat' subdirectory contains spectra formatted as .mat files for import into"
- [other] input_requirement: "Load the RAMClustR-clustered object (RC) containing inferred molecular weights and feature groupings from a prior do.findmain call."
- [other] serialization_process: "Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster."
- [other] verification_step: "Verify that all clusters are represented in both output formats and no data loss occurred during conversion."
- [readme] readme_usage: "ramclustObj <- do.findmain(ramclustObj = ramclustObj)

## Investigate the deconvoluted features in the `spectra` folder in MSP format"
- [intro] format_compatibility: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"

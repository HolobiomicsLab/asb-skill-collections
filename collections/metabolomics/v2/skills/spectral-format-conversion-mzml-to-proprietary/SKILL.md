---
name: spectral-format-conversion-mzml-to-proprietary
description: Use when after clustering features with RAMClustR and inferring molecular weights via do.findmain, when you need to perform structure elucidation or molecular formula prediction using MSFinder (for .mat format) or Sirius (for .ms format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
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

# spectral-format-conversion-mzml-to-proprietary

## Summary

Convert clustered mass spectrometry spectral data from RAMClustR-processed objects into vendor-specific formats (.mat for MSFinder, .ms for Sirius) to enable downstream structural annotation and molecular weight inference in specialized software environments.

## When to use

After clustering features with RAMClustR and inferring molecular weights via do.findmain, when you need to perform structure elucidation or molecular formula prediction using MSFinder (for .mat format) or Sirius (for .ms format). This skill is required when the RAMClustR output spectral representation must be imported into external annotation tools that do not natively parse R objects.

## When NOT to use

- Spectral data has not yet been clustered with RAMClustR—perform clustering and molecular weight inference first.
- You are working only with untargeted metabolomics peak tables without fragmentation spectra; .mat and .ms formats require matched m/z and intensity pairs.
- Your downstream annotation software natively accepts R objects or alternative formats (e.g., mzML, mzXML); conversion is unnecessary overhead.

## Inputs

- RAMClustR clustered object (RC) containing inferred molecular weights and feature groupings from a prior do.findmain call

## Outputs

- .mat files (MSFinder-compatible spectral format) in 'mat' subdirectory
- .ms files (Sirius-compatible spectral format) in 'ms' subdirectory

## How to apply

After running do.findmain on a RAMClustR object (RC) to infer molecular weights, the function automatically extracts spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each clustered feature. The spectral data is then converted to two separate formats: (1) .mat format (MSFinder-compatible structure) written to a 'mat' subdirectory within the 'spectrum' directory, and (2) .ms format (Sirius-compatible structure) written to an 'ms' subdirectory. Both formats are generated simultaneously from the same clustering result, preserving all cluster membership and quantitative metadata. Verify completeness by checking that all clusters present in the RC object are represented in both output directories and that no spectral information (m/z, intensity, retention time, molecular weight) is lost during conversion.

## Related tools

- **RAMClustR** (Source of clustered spectral data and molecular weight annotations; do.findmain function orchestrates the format conversion) — https://github.com/cbroeckl/RAMClustR
- **MSFinder** (Target software for .mat format import; performs structure elucidation and metabolite identification on converted spectra)
- **Sirius** (Target software for .ms format import; performs molecular formula prediction and fragmentation tree analysis on converted spectra)
- **InterpretMSSpectrum** (Original CRAN package from which the findMain function was adapted for RAMClustR; provides the underlying scoring logic for molecular weight inference)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Both 'mat' and 'ms' subdirectories are created within the 'spectrum' directory and contain files with counts matching the number of clusters in the RC object.
- Each .mat file is readable by MSFinder and contains valid numeric m/z and intensity arrays with consistent dimensionality.
- Each .ms file is readable by Sirius and conforms to MS format specification (header with metadata, followed by m/z–intensity pairs).
- Retention time and molecular weight metadata are preserved in both formats and match the values in the RC object.
- No spectral peaks or intensity values are missing or corrupted; a spot-check of cluster intensities in RC$SpecAbund matches the corresponding exported files.

## Limitations

- The conversion is lossy with respect to advanced RAMClustR metadata (e.g., per-sample quantification trends, QC batch corrections); only aggregate spectra and cluster IDs are exported.
- Software-specific format constraints may require post-export manual curation (e.g., MSFinder and Sirius have varying tolerance for metadata fields or spectral resolution).
- No version control or changelog for RAMClustR means format compatibility between RAMClustR versions and MSFinder/Sirius versions is not formally documented; breaking changes may occur silently.

## Evidence

- [other] Finding: Output directory structure and file formats: "The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory. The 'mat' subdirectory contains spectra formatted as .mat files for import into"
- [other] Finding: Metadata preservation during conversion: "Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster."
- [intro] Tool role: MSFinder format: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"
- [intro] Tool role: Sirius format: "The 'ms' contains spectra in .ms format suitable for import into Sirius software"
- [intro] Workflow step: Molecular weight inference prerequisite: "RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)"
- [readme] README example: Full stepwise workflow including conversion: "ramclustObj <- rc.ramclustr(ramclustObj = ramclustObj); ramclustObj <- rc.qc(ramclustObj = ramclustObj); ramclustObj <- do.findmain(ramclustObj = ramclustObj)"

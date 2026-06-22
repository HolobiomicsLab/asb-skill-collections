---
name: metabolite-cluster-export-formatting
description: Use when after running do.findmain on a RAMClustR-clustered object to infer molecular weights and assign features to compound clusters, when you need to conduct structural elucidation in MSFinder or Sirius and require spectra in their native import formats rather than the intermediate MSP or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-cluster-export-formatting

## Summary

Export RAMClustR-clustered mass spectrometry spectra into software-specific formats (.mat for MSFinder, .ms for Sirius) to enable downstream structural annotation and molecular weight inference. This skill bridges the output of unsupervised feature clustering with format requirements of specialized annotation tools.

## When to use

After running do.findmain on a RAMClustR-clustered object to infer molecular weights and assign features to compound clusters, when you need to conduct structural elucidation in MSFinder or Sirius and require spectra in their native import formats rather than the intermediate MSP or cluster-level representations.

## When NOT to use

- The input RC object has not yet been processed through do.findmain; molecular weight inference and cluster assignment must be complete first.
- You need spectra in a format other than .mat or .ms (e.g., mzML, mzXML, or MSP); use alternative export functions or manual conversion.
- The analysis does not require downstream annotation in MSFinder or Sirius; intermediate cluster-level representations may be sufficient.

## Inputs

- RAMClustR object (RC) with completed do.findmain molecular weight inference
- Spectral data (m/z, intensity pairs) and metadata (retention time, inferred MW, cluster ID)

## Outputs

- .mat files (MSFinder-compatible spectra in 'mat' subdirectory)
- .ms files (Sirius-compatible spectra in 'ms' subdirectory)
- Two parallel subdirectory trees ('mat' and 'ms') within the 'spectrum' output folder

## How to apply

The do.findmain function automatically creates two subdirectories ('mat' and 'ms') within the existing 'spectrum' directory. For each clustered compound, extract m/z, intensity pairs and metadata (retention time, inferred molecular weight, cluster assignment). Convert spectral data to .mat format (MSFinder-compatible structure) and write to the 'mat' subdirectory; simultaneously convert to .ms format (Sirius-compatible structure) and write to the 'ms' subdirectory. After export, verify all clusters are represented in both output formats and that no data loss occurred during conversion by comparing cluster counts between the original RC object and the two output directories.

## Related tools

- **RAMClustR** (Provides do.findmain function that performs molecular weight inference and automatically exports clustered spectra to both .mat and .ms formats) — https://github.com/cbroeckl/RAMClustR
- **MSFinder** (Target annotation software that accepts .mat format spectra for structural elucidation)
- **Sirius** (Target annotation software that accepts .ms format spectra for CSI:FingerID and molecular formula inference)
- **InterpretMSSpectrum** (Source package; RAMClustR adapted the findMain function for molecular weight scoring)

## Examples

```
RC <- do.findmain(ramclustObj = RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Both 'mat' and 'ms' subdirectories are created within the 'spectrum' directory with no errors during export.
- Cluster count in the 'mat' directory equals cluster count in the 'ms' directory and matches the number of clusters in RC$annotation.
- Spot-check a random .mat file with MSFinder and a random .ms file with Sirius to confirm successful import and correct m/z / intensity structure.
- All m/z and intensity values in exported files match the originating cluster spectra (bit-exact or within floating-point tolerance).
- No clusters from the RC object are missing from either output directory; verify via file count and cluster ID cross-reference.

## Limitations

- The RAMClustR repository contains no changelog; version history and breaking changes to the export format are undocumented, which may affect reproducibility across releases.
- Export success depends on successful prior execution of do.findmain; if molecular weight inference fails for certain clusters, those clusters may not be represented in both output formats uniformly.
- The skill assumes standard RAMClustR output structure (m/z-RT feature naming, default 'spectrum' directory). Non-standard or manually modified RC objects may fail during export.

## Evidence

- [other] The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory.: "The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory."
- [other] The 'mat' subdirectory contains spectra formatted as .mat files for import into MSFinder, and the 'ms' subdirectory contains spectra formatted as .ms files for import into Sirius.: "The 'mat' subdirectory contains spectra formatted as .mat files for import into MSFinder, and the 'ms' subdirectory contains spectra formatted as .ms files for import into Sirius."
- [other] Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster.: "Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster."
- [other] Verify that all clusters are represented in both output formats and no data loss occurred during conversion.: "Verify that all clusters are represented in both output formats and no data loss occurred during conversion."
- [intro] The 'mat' contains spectra in .mat format suitable for import into MSFinder software: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"
- [intro] The 'ms' contains spectra in .ms format suitable for import into Sirius software: "The 'ms' contains spectra in .ms format suitable for import into Sirius software"
- [readme] RC <- do.findmain(ramclustObj = ramclustObj): "RC <- do.findmain(ramclustObj = ramclustObj)"

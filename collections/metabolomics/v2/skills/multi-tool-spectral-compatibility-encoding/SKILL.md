---
name: multi-tool-spectral-compatibility-encoding
description: Use when after RAMClustR clustering and do.findmain molecular weight
  inference are complete, when you need to submit the same inferred spectra to multiple
  third-party annotation tools (MSFinder and Sirius) that each require distinct file
  formats and cannot share a common intermediate representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - RAMClustR
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  - R
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-tool-spectral-compatibility-encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Encode clustered mass spectrometry spectra into multiple downstream software-compatible formats (.mat for MSFinder, .ms for Sirius) to enable parallel structural annotation workflows. This skill bridges RAMClustR output with independent interpretation engines that require proprietary input formats.

## When to use

Apply this skill after RAMClustR clustering and do.findmain molecular weight inference are complete, when you need to submit the same inferred spectra to multiple third-party annotation tools (MSFinder and Sirius) that each require distinct file formats and cannot share a common intermediate representation.

## When NOT to use

- Input RC object has not yet passed through do.findmain; molecular weight inference must be completed first.
- You only need to use a single annotation tool (e.g., only MSFinder or only Sirius); single-format export is more efficient.
- Spectra are already in .mat or .ms format and do not need re-encoding; skip directly to tool-specific import.

## Inputs

- RAMClustR clustered object (RC) with completed clustering and do.findmain annotation
- Inferred molecular weights and feature–cluster assignments from do.findmain
- Raw m/z–intensity pairs and retention times for each feature

## Outputs

- .mat files in 'mat' subdirectory (MSFinder-compatible spectra)
- .ms files in 'ms' subdirectory (Sirius-compatible spectra)
- Metadata mappings (retention time, molecular weight, cluster ID for each spectrum)

## How to apply

After running do.findmain on a RAMClustR object (RC) to infer molecular weights and cluster spectra, the function automatically creates two subdirectories within the 'spectrum' directory: 'mat' for MSFinder-compatible spectra and 'ms' for Sirius-compatible spectra. For each cluster, extract the m/z–intensity pairs, retention time, inferred molecular weight, and cluster ID metadata. Convert spectral data to .mat format (a MATLAB-compatible structure expected by MSFinder) and write to the 'mat' subdirectory; simultaneously convert the same spectral data to .ms format (the mass spectrum text format expected by Sirius) and write to the 'ms' subdirectory. Verify that all clusters present in the RC object are represented in both output directories and that no spectral data or metadata is lost during either conversion.

## Related tools

- **RAMClustR** (Provides clustered spectral object and do.findmain function that orchestrates the creation of multi-format spectrum subdirectories) — https://github.com/cbroeckl/RAMClustR
- **MSFinder** (Downstream annotation tool that imports spectra from .mat format files created in the 'mat' subdirectory)
- **Sirius** (Downstream annotation tool that imports spectra from .ms format files created in the 'ms' subdirectory)
- **InterpretMSSpectrum** (Source package from which RAMClustR adapted the findMain function for molecular weight inference and spectrum organization)

## Examples

```
RC <- do.findmain(ramclustObj = RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Both 'mat' and 'ms' subdirectories exist and are populated within the 'spectrum' directory after do.findmain completes.
- Cluster count matches between the RC object and the number of spectrum files in each subdirectory (no clusters omitted).
- Each .mat file is readable by MSFinder (valid MATLAB structure) and each .ms file is readable by Sirius (valid mass spectrum format).
- Metadata (retention time, molecular weight, cluster ID) are preserved in both output formats and match the source RC object values.
- No spectral intensity data or m/z values are lost or corrupted during conversion between .mat and .ms formats.

## Limitations

- The skill is entirely downstream of do.findmain and depends on successful prior clustering and molecular weight inference; if do.findmain produces incorrect inferences, both output formats will propagate that error.
- No changelog is documented for RAMClustR; version-specific breaking changes in file format structure are undisclosed, which may cause compatibility issues when results are re-run or shared across RAMClustR versions.
- The .mat and .ms formats may diverge in how they encode metadata or handle edge cases (e.g., multiple isomeric clusters with identical mass); manual validation against downstream tool expectations is prudent.

## Evidence

- [other] The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory.: "The do.findmain function creates two new subdirectories ('mat' and 'ms') within the existing 'spectrum' directory. The 'mat' subdirectory contains spectra formatted as .mat files for import into"
- [other] Verify that all clusters are represented in both output formats and no data loss occurred during conversion.: "Verify that all clusters are represented in both output formats and no data loss occurred during conversion."
- [intro] RAMClustR adapted the findMain function from InterpretMSSpectrum for molecular weight inference and spectrum organization.: "We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package"
- [intro] The 'mat' subdirectory contains spectra in .mat format suitable for import into MSFinder software, and the 'ms' subdirectory contains spectra in .ms format suitable for import into Sirius software.: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software… The 'ms' contains spectra in .ms format suitable for import into Sirius software"
- [readme] do.findmain is called in the individual stepwise workflow after RAMClustR clustering and quality control.: "ramclustObj <- rc.ramclustr(ramclustObj = ramclustObj)
ramclustObj <- rc.qc(ramclustObj = ramclustObj)
ramclustObj <- do.findmain(ramclustObj = ramclustObj)"

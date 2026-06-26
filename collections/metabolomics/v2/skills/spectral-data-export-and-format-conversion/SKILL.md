---
name: spectral-data-export-and-format-conversion
description: Use when after running RAMClustR clustering on XCMS-processed metabolomics
  data, export spectral data when you need to share clustered spectra with external
  annotation software (MSFinder, Sirius), perform spectrum matching against reference
  databases, or prepare results for collaborative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3790
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RAMClustR
  - dynamicTreeCut
  - R
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting
  dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
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

# spectral-data-export-and-format-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Export clustered mass spectrometry spectral data from RAMClustR RC objects into standardized formats (.msp, .mat, .ms) suitable for downstream annotation and interpretation by external software. This enables seamless integration of metabolomics feature clustering results with spectrum matching and structure elucidation tools.

## When to use

After running RAMClustR clustering on XCMS-processed metabolomics data, export spectral data when you need to share clustered spectra with external annotation software (MSFinder, Sirius), perform spectrum matching against reference databases, or prepare results for collaborative analysis outside the R environment.

## When NOT to use

- Features have not yet been clustered by RAMClustR—run ramclustR() first.
- You need raw, unclustered XCMS feature data—export feature tables directly from XCMS instead.
- Spectra require custom, non-standard formatting beyond .msp/.mat/.ms formats—consider post-processing exported files with custom scripts.

## Inputs

- RC object from ramclustR() containing clustered features with retention time and spectral data
- Experiment design metadata (sample class, batch, QC labels)
- XCMS xcmsSet object (alternative direct input pathway)

## Outputs

- .msp spectral library file (all clusters in MSP format)
- .mat file suitable for MSFinder software import
- .ms file suitable for Sirius software import
- RC$SpecAbund matrix (spectral abundance dataset)
- 'spectra' directory containing formatted spectral files

## How to apply

RAMClustR automatically generates a 'spectra' directory during clustering that contains an .msp file named after the project, with all spectra for all detected clusters. The RC object contains three exportable spectral formats: .msp format (compatible with general spectrum matching), .mat format (for MSFinder import), and .ms format (for Sirius import). Access the spectral abundance matrix via RC$SpecAbund within the RC object. Select the export format based on your downstream annotation tool: use .msp for broad compatibility, .mat for MSFinder-specific structure prediction, or .ms for Sirius MS/MS fragmentation analysis. Verify export completeness by checking that the number of spectra in the output file matches the number of clusters in RC$nclust.

## Related tools

- **RAMClustR** (Primary tool that generates RC object and automatically exports spectra to .msp format during ramclustR() execution; also provides do.findmain() for molecular weight inference post-export) — https://github.com/cbroeckl/RAMClustR
- **MSFinder** (External software for structure prediction from MS1 and MS/MS spectra; accepts RAMClustR .mat export format)
- **Sirius** (External software for MS/MS fragmentation analysis and structure elucidation; accepts RAMClustR .ms export format)
- **InterpretMSSpectrum** (CRAN package; RAMClustR adapted its findMain function for molecular weight scoring, used in do.findmain() post-export molecular weight inference)

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes=experiment); RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Verify .msp file exists in 'spectra' directory with number of spectral entries matching RC$nclust (total clusters).
- Check that RC$SpecAbund matrix has cluster count matching number of spectra in exported files.
- Confirm each spectrum entry in .msp contains retention time, m/z, and intensity annotations for the cluster.
- Validate external software (MSFinder, Sirius) successfully imports the exported file without format errors.
- Verify molecular weight inferences from do.findmain() on exported data show ~90% agreement with alternative scoring methods as documented in the method.

## Limitations

- No changelog or version history documented—breaking changes in export format between versions are not tracked, potentially causing compatibility issues with archived workflows.
- Export format compatibility limited to .msp, .mat, and .ms—custom formats or direct database uploads require post-processing.
- Spectral abundance scaling and normalization (batch correction, QC median scaling) are applied during RC object creation, not during export—verify batch.qc.normalization parameters were correctly set before export if downstream analysis requires normalized intensities.
- Molecular weight inference via do.findmain() depends on ionization mode specification (positive/negative) and mz error tolerances (mzabs.error, ppm.error)—misspecification can degrade annotation quality.

## Evidence

- [intro] Automatic directory generation and file output: "a new 'spectra' directory containing a .msp file named after the project with all spectra for all detected clusters"
- [intro] RC object spectral data access: "a SpecAbund dataset within the RC object accessible via RC$SpecAbund"
- [intro] Multiple export format compatibility: "export spectra in .msp format for external software interpretation (MSFinder, Sirius)"
- [readme] Format-specific tool integration: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"
- [readme] Sirius format specification: "The 'ms' contains spectra in .ms format suitable for import into Sirius software"
- [intro] Post-export molecular weight inference: "RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)"

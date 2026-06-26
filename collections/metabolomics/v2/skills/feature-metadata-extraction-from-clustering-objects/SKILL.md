---
name: feature-metadata-extraction-from-clustering-objects
description: Use when after RAMClustR clustering and do.findmain molecular weight
  inference have been completed on XCMS-detected metabolomics features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RAMClustR
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  - R
  - XCMS
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

# feature-metadata-extraction-from-clustering-objects

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract spectral metadata (m/z, intensity pairs, retention time, molecular weight, cluster assignment) from RAMClustR clustering objects to enable downstream format conversion and structural annotation. This skill bridges unsupervised feature clustering and software-specific spectral export formats (MSFinder .mat, Sirius .ms).

## When to use

Apply this skill after RAMClustR clustering and do.findmain molecular weight inference have been completed on XCMS-detected metabolomics features. Use it when you need to transition from the RAMClustR object representation to software-agnostic intermediate spectral data for import into MSFinder or Sirius for structure elucidation.

## When NOT to use

- Feature detection has not yet been performed; XCMS preprocessing and fillPeaks steps must precede RAMClustR clustering.
- do.findmain molecular weight inference has not been run; clustering object lacks inferred masses required for annotation export.
- Input is already in target software format (.mat or .ms); no extraction or conversion is needed.

## Inputs

- RAMClustR object (RC) after do.findmain execution
- RC$SpecAbund (feature abundance matrix across samples)
- RC$frt (feature retention times)
- RC$mz (feature m/z values)
- RC$ann (cluster annotations and inferred molecular weights)
- RC$featclus (feature-to-cluster mapping)

## Outputs

- Extracted spectral metadata table (m/z, intensity pairs per cluster)
- Cluster-level retention time and molecular weight annotations
- Intermediate data structure ready for format-specific conversion (.mat or .ms)

## How to apply

Load the RAMClustR-clustered object (RC) containing inferred molecular weights and feature groupings from a prior do.findmain call. Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster from the RC object slots. Verify that extraction preserves the quantitative relationship between features assigned to the same cluster—features from the same compound should have approximately the same retention time and quantitative trend across samples. Map extracted metadata to the target software schema (e.g., MSFinder .mat structure or Sirius .ms structure). Validate that all clusters are represented and no data loss occurred during extraction.

## Related tools

- **RAMClustR** (Provides the clustering object (RC) containing grouped features, retention times, m/z values, and molecular weight annotations from which metadata is extracted) — https://github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Provides the findMain function (adapted in RAMClustR as do.findmain) that infers molecular weights and populates the RC object with annotations used in metadata extraction)
- **XCMS** (Upstream feature detection; generates the aligned feature matrix that is clustered by RAMClustR and whose metadata (m/z, retention time) is extracted here)
- **MSFinder** (Downstream consumer of extracted spectral data in .mat format for structure elucidation)
- **Sirius** (Downstream consumer of extracted spectral data in .ms format for structure elucidation)

## Examples

```
RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10); metadata <- data.frame(mz = RC$mz, rt = RC$frt, cluster = RC$featclus, mw = RC$ann$mw)
```

## Evaluation signals

- All clusters present in RC$featclus are represented in the extracted metadata table with no missing assignments.
- Extracted retention times match RC$frt values and m/z values match RC$mz for each feature.
- Features assigned to the same cluster have approximately identical retention times (expected clustering invariant).
- Cluster-level molecular weights (from RC$ann) are successfully mapped and present in output.
- Abundance matrix subsetting produces non-zero intensity pairs for all clusters across the sample set; no data loss in filtering.

## Limitations

- Metadata extraction is only valid if do.findmain has completed successfully; two scoring methods (findMain and RAMClustR) agree approximately 90% of the time for molecular weight inference, so extracted weights may have ~10% discordance.
- Extraction fidelity depends on upstream XCMS preprocessing quality (retention time correction, peak alignment); drift in retention time prior to grouping can produce inconsistent cluster assignments.
- No changelog or version history is available for RAMClustR, so breaking changes to object slot names or data structures across versions are undocumented and may affect extraction logic portability.

## Evidence

- [other] Extraction step — input definition: "Extract spectral data (m/z, intensity pairs) and metadata (retention time, molecular weight, cluster assignment) for each feature or feature cluster."
- [intro] Clustering invariant used for validation: "two features derived from the same compound will have (approximately) the same retention time"
- [intro] Molecular weight inference agreement rate: "In practice we find that the two scoring methods agree about 90% of the time."
- [intro] Output format specification for MSFinder: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"
- [intro] Output format specification for Sirius: "The 'ms' contains spectra in .ms format suitable for import into Sirius software"
- [readme] RAMClustR object structure and workflow context: "ramclustObj <- do.findmain(ramclustObj = ramclustObj)"
- [readme] Retention time and abundance data availability in RC object: "print(ramclustobj$ann); print(ramclustobj$nfeat); print(ramclustobj$SpecAbund[,1:6])"

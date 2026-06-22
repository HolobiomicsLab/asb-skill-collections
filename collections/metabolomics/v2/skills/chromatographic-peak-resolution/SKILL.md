---
name: chromatographic-peak-resolution
description: Use when when you have loaded raw GC-MS data in netCDF or mzML format and visual or statistical inspection reveals overlapping chromatographic peaks (i.e., multiple m/z ions co-eluting at the same retention time window).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - GNPS_GC
  techniques:
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub_cq
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-resolution

## Summary

Resolves overlapping or co-eluting components in gas chromatography–mass spectrometry (GC-MS) data by applying spectral deconvolution algorithms to separate composite signals into individual mass spectra. This skill is essential when raw GC-MS chromatograms contain multiple analytes eluting at the same or proximal retention times, producing composite peaks that obscure individual component identities.

## When to use

When you have loaded raw GC-MS data in netCDF or mzML format and visual or statistical inspection reveals overlapping chromatographic peaks (i.e., multiple m/z ions co-eluting at the same retention time window). Deconvolution is particularly important in untargeted metabolomics or environmental profiling workflows where sample complexity is high and peak overlap is expected.

## When NOT to use

- Input data already consists of a resolved feature table (e.g., already deconvolved or from targeted analysis with baseline separation).
- Chromatographic peaks are fully baseline-resolved and show no co-elution; deconvolution adds computational cost without benefit.
- Data quality is too poor to support reliable deconvolution (e.g., very low signal-to-noise ratio or severe instrumental artifacts).

## Inputs

- raw GC-MS data in netCDF or mzML format containing overlapping chromatographic peaks

## Outputs

- peak table in tabular format (one row per deconvolved component) with columns for retention time, m/z values, and intensity
- deconvolved mass spectra for each resolved component

## How to apply

Load raw GC-MS data (netCDF or mzML format) into the deconvolution pipeline. Apply a spectral deconvolution algorithm designed to separate co-eluting ions by decomposing composite mass spectra into constituent pure component spectra, assigning each a unique retention time and m/z profile. Extract deconvolved peak features (retention time, m/z values, intensity) for each resolved component. Generate an output peak table in tabular format with one row per deconvolved component. Validate deconvolution quality by confirming an increase in peak count relative to the input, inspecting spectral coherence (e.g., consistency of mass fragments within a resolved component), and reviewing retention time and intensity distributions for physical plausibility.

## Related tools

- **GNPS_GC** (Companion repository implementing the auto-deconvolution workflow for GC-MS data processing and molecular networking) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Peak count in the output table is greater than the number of distinct peaks in the raw data, indicating successful separation of co-eluting components.
- Each deconvolved mass spectrum shows internally consistent fragmentation patterns (related m/z peaks with expected intensity ratios) characteristic of a single molecular species.
- Retention time and m/z values for resolved components fall within physically expected ranges; no anomalously high or negative intensities.
- Spectral coherence of separated components can be verified by comparing each deconvolved spectrum against reference libraries or known compound profiles.
- Manual expert review confirms that separated components represent distinct analytes rather than fragmentation artifacts or noise.

## Limitations

- Deconvolution accuracy depends on the quality and resolution of the underlying mass spectrometry data; very low signal-to-noise ratios or severe peak overlap may result in incomplete or ambiguous separation.
- The method assumes that co-eluting components have distinguishable mass spectral signatures; compounds with identical or nearly identical fragmentation patterns cannot be reliably resolved by mass alone.
- No changelog or detailed algorithm parameter documentation was found in the referenced repository, limiting transparency around version updates and method refinement.
- Deconvolution is a post-hoc computational step and cannot recover chromatographic information lost during sample collection or instrument operation.

## Evidence

- [other] Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks. Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra from composite signals.: "Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks. 2. Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra"
- [other] Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component. Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns.: "Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component. 4. Generate output peak table in tabular format with one row per deconvolved"
- [other] Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components.: "Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components."
- [intro] Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data: "Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data"
- [readme] This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. et al. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data.: "This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."

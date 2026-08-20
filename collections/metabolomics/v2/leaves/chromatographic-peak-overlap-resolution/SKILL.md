---
name: chromatographic-peak-overlap-resolution
description: Use when analyzing GC-MS data containing overlapping chromatographic
  peaks—a common scenario in untargeted metabolomics and environmental screening where
  sample complexity or chromatographic resolution limitations cause co-elution of
  structurally similar or temporally proximate compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MSHub
  - GNPS
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry
  data
- GNPS molecular networking
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
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

# chromatographic-peak-overlap-resolution

## Summary

Auto-deconvolution of overlapping gas chromatography–mass spectrometry peaks to extract individual compound spectra from co-eluting analytes. This skill enables recovery of pure mass spectra from complex chromatographic mixtures where multiple compounds elute simultaneously.

## When to use

Apply this skill when analyzing GC-MS data containing overlapping chromatographic peaks—a common scenario in untargeted metabolomics and environmental screening where sample complexity or chromatographic resolution limitations cause co-elution of structurally similar or temporally proximate compounds. Use it as a preprocessing step before molecular networking or spectral library matching to recover compound-specific mass spectra.

## When NOT to use

- Input is liquid chromatography–mass spectrometry (LC-MS) data without GC separation—deconvolution algorithms are optimized for GC peak shapes and may not generalize to LC.
- Chromatographic peaks are well-resolved (baseline-separated) with no overlap—deconvolution introduces unnecessary complexity and risk of false peak splitting.
- Raw data is already in processed or centroided format without access to full mass spectral profiles—deconvolution requires high-resolution, continuous data.

## Inputs

- GC-MS raw data (NetCDF, .D vendor format, or equivalent)
- Chromatographic separation parameters (column type, temperature program, flow rate—metadata)
- Sample composition information or prior knowledge of expected number of compounds (optional)

## Outputs

- Deconvolved mass spectra in MGF or mzTab format
- Retention time and peak intensity annotations per spectrum
- Deconvolution quality metrics (e.g., spectral purity, residual error)

## How to apply

Load raw GC-MS data (NetCDF or vendor format) into MSHub and apply the auto-deconvolution algorithm to extract individual compound spectra from overlapping peaks. The algorithm resolves co-eluting analytes by deconvolving the mass spectral components within each chromatographic window. Export the resolved spectra in MGF or mzTab format, which preserves retention time and mass spectral metadata. Validate deconvolution quality by checking that extracted spectra are chemically interpretable (expected fragment patterns, reasonable molecular ion intensities) and that the number of deconvolved spectra matches the expected sample complexity. Compare network topology (node count, edge density) of the deconvolved data to published benchmarks or manual annotation to confirm peak resolution success.

## Related tools

- **MSHub** (Performs automated deconvolution of overlapping GC-MS peaks to extract individual compound spectra)
- **GNPS** (Accepts deconvolved spectra in MGF/mzTab format for downstream molecular networking and spectral library matching) — https://gnps.ucsd.edu

## Evaluation signals

- Deconvolved spectrum count increases from raw peak count, indicating successful splitting of co-eluting analytes.
- Exported spectra in MGF/mzTab format validate against schema (required fields: m/z, intensity, retention time, precursor mass).
- Molecular network constructed from deconvolved spectra shows expected topology: node count and edge density match published results or manual validation of the sample.
- Individual deconvolved spectra exhibit chemically reasonable fragmentation patterns (loss of common neutral masses, expected diagnostic ions for compound class).
- Residual error or spectral purity metrics (where reported by MSHub) confirm that reconstructed peaks reproduce the original chromatographic profile.

## Limitations

- Deconvolution success depends on spectral and chromatographic resolution; highly overlapped peaks with similar mass spectral patterns may not be fully separated.
- Algorithm is optimized for GC-MS and Electron Ionization (EI) spectra; applicability to other ionization methods or chromatographic modes is not established in this work.
- Retention time metadata must be preserved through the deconvolution–export–upload pipeline for accurate network interpretation and compound annotation.
- Computational cost and runtime scale with data size and peak complexity; no throughput benchmarks are provided in the source material.

## Evidence

- [other] Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks.: "Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks."
- [other] Export deconvolved spectra in a format compatible with GNPS (e.g., MGF or mzTab).: "Export deconvolved spectra in a format compatible with GNPS (e.g., MGF or mzTab)."
- [intro] Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis: "Development of auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
- [other] Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network.: "Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network."

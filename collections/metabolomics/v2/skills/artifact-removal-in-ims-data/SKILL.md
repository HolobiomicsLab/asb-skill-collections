---
name: artifact-removal-in-ims-data
description: Use when processing raw IM-MS data (UIMF or Agilent MassHunter .d format) that exhibits jagged peaks in low-abundance ions, isolated high-intensity noise spikes, or saturated detector signals that distort elution and mobility profiles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework
  - Microsoft Visual C++ Runtime x64
  - .NET Framework 4.7.2 or later
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
- .NET Framework 4.7.2 or later (included with Windows 10 update 1803 and later releases
- Microsoft Visual C++ Runtime x64 (may already be installed, if the program doesn't work then you can download vcredist_x64.exe
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# artifact-removal-in-ims-data

## Summary

Remove noise, spike, and saturation artifacts from ion mobility-mass spectrometry (IM-MS) data to enhance signal quality and recover low-abundance molecular signatures. This skill applies integrated noise filtering, spike removal, and saturation repair algorithms to improve peak deconvolution and quantitative accuracy in multiplexed IM-MS acquisitions.

## When to use

Apply this skill when processing raw IM-MS data (UIMF or Agilent MassHunter .d format) that exhibits jagged peaks in low-abundance ions, isolated high-intensity noise spikes, or saturated detector signals that distort elution and mobility profiles. Particularly critical when recovering multiplexed frames or processing structural isomers that rely on fine resolution of weak signals.

## When NOT to use

- Input data already processed by another vendor's proprietary deconvolution tool — reapplication may introduce over-processing and loss of fine structure.
- Highly convoluted elution/mobility profiles caused by severe co-eluting interferences — saturation repair may produce incorrect results (per article caveats).
- Already-exported feature tables or mzML files — this skill operates on raw instrument frames, not processed peak lists.

## Inputs

- raw IM-MS data file (UIMF format or Agilent MassHunter .d directory)
- interpolated and demultiplexed IM-MS frame data
- user-specified low-intensity threshold (abundance units)
- multidimensional smoothing kernel parameters (retention time, m/z, mobility windows)

## Outputs

- artifact-cleaned IM-MS data in original instrument format
- MS-file with reduced spike noise, baseline-corrected intensities, and repaired saturated peaks
- quality metrics (artifact count removed, smoothing extent applied)

## How to apply

After ion mobility dimension interpolation and demultiplexing, execute three sequential artifact-removal operations: (1) apply a low-intensity threshold filter to remove baseline noise below a user-specified abundance cutoff; (2) invoke the integrated spike-removal algorithm to eliminate isolated high-intensity artifacts that do not represent real molecular signals; (3) apply multidimensional smoothing across retention time, m/z, and mobility axes to enhance real signals while suppressing jagged peak artifacts common in low-abundance ions, followed by saturation repair to recover clipped intensity values. Rationale: smoothing removes artifacts in jagged peaks while preserving peak shape; spike removal reduces false positive identifications; saturation repair restores quantitative accuracy. Monitor for over-smoothing that may collapse fine structure or over-correction of highly convoluted elution/mobility profiles caused by co-eluting interferences.

## Related tools

- **PNNL PreProcessor** (Primary integrated tool for executing noise filtering, spike removal, saturation repair, and multidimensional smoothing on raw IM-MS data files in a single workflow.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Provides native .d format support and data access component library; PNNL PreProcessor depends on MassHunter Data Access Component for reading proprietary Agilent IM-MS frames.) — https://www.agilent.com
- **.NET Framework 4.7.2 or later** (Required runtime dependency for PNNL PreProcessor executable.)
- **Microsoft Visual C++ Runtime x64** (Required runtime dependency for PNNL PreProcessor executable.)

## Evaluation signals

- Spike count and artifact removal metrics reported by PNNL PreProcessor — verify that detected spike/noise artifacts are substantially reduced (>50% reduction typical for low-abundance data).
- Peak shape improvement: jagged low-abundance ion profiles smoothed to symmetric Gaussian-like distributions with preserved m/z and mobility centroids (inspect in IM-MS Browser or raw data visualization).
- Saturation repair fidelity: clipped intensity values at detector saturation threshold restored to physically plausible ranges without introducing artifactual intensity spikes or reversals in elution/mobility order.
- Signal-to-noise ratio (SNR) gain quantified from before/after comparison — low-abundance molecular signals should exhibit ≥2× SNR improvement post-smoothing without peak intensity loss >15%.
- Reproducibility check: re-run artifact removal on same input with identical parameters; output data should be byte-identical or differ only by floating-point precision (<1e-6 relative error in abundance values).

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, as noted in the methods section.
- Multidimensional smoothing can introduce bias in quantification of very low-abundance signals if kernel window sizes are not carefully tuned to the instrument resolution.
- Spike removal algorithm effectiveness depends on definition of 'spike' (isolated high-intensity point); threshold tuning is required and may not generalize across different sample types or instruments.
- No changelog or version tracking documented in repository — reproducibility and backward compatibility of artifact-removal parameters across software versions are unclear.

## Evidence

- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] An algorithm to remove noise in form of 'spikes' integrated into preprocessing: "An algorithm to remove noise in form of 'spikes'"
- [methods] Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [intro] PNNL-PreProcessor provides a software tool with various algorithms including noise filtering by low intensity threshold and spike removal, saturation repair: "noise filtering by low intensity threshold and spike removal, saturation repair"
- [methods] PNNL demultiplexing and artifact removal algorithm integrated with selectable pulse coverage percentage: "PNNL demultiplexing and artifact removal algorithm integrated. A new selectable pulse coverage percentage"
- [readme] Data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair"

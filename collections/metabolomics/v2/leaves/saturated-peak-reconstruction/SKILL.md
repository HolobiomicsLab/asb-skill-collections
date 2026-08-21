---
name: saturated-peak-reconstruction
description: Use when processing IM-MS data files (Agilent .d or UIMF format) that
  contain high-abundance ions suspected of signal saturation, particularly in untargeted
  or discovery proteomics/metabolomics workflows where dynamic range compression would
  obscure quantitative relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework 4.7.2
  - Microsoft Visual C++ Runtime x64
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files (MS-files) from drift tube (DT) and structure for lossless
  ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# saturated-peak-reconstruction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detect and computationally reconstruct ion signals that have exceeded the dynamic range of the mass spectrometry detector in ion mobility–mass spectrometry (IM-MS) data. This skill applies multidimensional smoothing algorithms across m/z, mobility, and retention time dimensions to restore intensity information and enable accurate quantification of high-abundance ions.

## When to use

Apply this skill when processing IM-MS data files (Agilent .d or UIMF format) that contain high-abundance ions suspected of signal saturation, particularly in untargeted or discovery proteomics/metabolomics workflows where dynamic range compression would obscure quantitative relationships. Saturation is indicated by flat-topped or clipped peaks in the raw m/z × drift time intensity map.

## When NOT to use

- Input data is already intensity-normalized or log-transformed — saturation repair operates on raw detector counts and assumes access to original bit depth.
- Data contains extensive interferences with highly convoluted elution/mobility profiles — the saturation repair software may produce incorrect results in these cases, as stated in the methods.
- Analysis goal is only spectral library matching or peak detection — repair is unnecessary if quantitative accuracy of saturated peaks is not required.

## Inputs

- Agilent MassHunter raw data file (.d format)
- UIMF ion mobility–mass spectrometry data file
- IM-MS drift time intensity map (m/z × drift time × retention time)

## Outputs

- Saturation-repaired IM-MS data matrix (m/z × drift time × retention time with reconstructed intensities)
- Ion mobility frame metadata export (field strength, pressure, temperature, MS actuals as text file)
- Repair quality log file (warnings and confidence flags for each repaired peak)

## How to apply

Load the raw Agilent MassHunter (.d) or UIMF IM-MS data file into PNNL PreProcessor. Apply the integrated multidimensional smoothing and saturation repair algorithm, which leverages the redundancy of signal across the m/z, mobility, and retention time dimensions to estimate the true peak shape and intensity of saturated ions. The algorithm works by analyzing neighboring unsaturated frames and mobility bins to infer the underlying Gaussian profile. After repair, export the ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) and inspect the output logs for warnings about convoluted elution/mobility profiles, which indicate potential repair failures. Verify repair success by visual inspection of corrected peak profiles and checking that repaired intensities are consistent with expected chromatographic and mobility distributions.

## Related tools

- **PNNL PreProcessor** (Primary preprocessing application that integrates saturation repair as part of its multidimensional smoothing pipeline; loads .d and UIMF files and applies the repair algorithm across m/z, mobility, and retention time dimensions.) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Instrument control and raw data acquisition software; generates the .d format input files that PNNL PreProcessor reads for saturation repair.)
- **.NET Framework 4.7.2** (Runtime dependency required to execute PNNL PreProcessor binaries on Windows.)
- **Microsoft Visual C++ Runtime x64** (Runtime library dependency for PNNL PreProcessor execution.)

## Evaluation signals

- Output log contains no 'convoluted elution/mobility profile' warnings for the repair regions of interest, indicating the algorithm did not encounter severe interferences during reconstruction.
- Repaired peak intensities across successive drift time frames and retention time points form smooth Gaussian distributions consistent with expected ion mobility and chromatographic profiles, not discontinuous or artifact-laden traces.
- Mass accuracy and isotope pattern fidelity of repaired ions remain within specification (< 5 ppm error, expected isotope ratio ≤ 10% deviation), confirming that repair did not introduce m/z shifts or pattern distortion.
- Metadata export file successfully contains all required fields (field strength, pressure, temperature, MS actuals) for each frame with no null or truncated values.
- Comparison of pre- and post-repair intensity distributions shows that repaired peaks lie within the expected dynamic range of unsaturated reference peaks of similar compound class, not exceeding physical instrument limits by orders of magnitude.

## Limitations

- Saturation repair may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, as the algorithm relies on local profile consistency to infer the saturated shape.
- Repair accuracy depends on the presence of unsaturated reference frames and mobility bins nearby; ions saturated across the entire retention time or drift time window cannot be reliably reconstructed.
- No changelog found in the repository, limiting reproducibility and version tracking of algorithmic improvements or bug fixes across releases.
- The method assumes that saturation is uniform across the m/z dimension; partial saturation or nonlinear detector response in edge regions may not be fully corrected.

## Evidence

- [other] Multidimensional smoothing and saturation repair algorithm to detect and reconstruct saturated peaks across the m/z, mobility, and retention time dimensions: "Apply multidimensional smoothing and saturation repair algorithm to detect and reconstruct saturated peaks across the m/z, mobility, and retention time dimensions."
- [methods] The saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [readme] PNNL-PreProcessor provides saturation repair and metadata export as separate utilities within its preprocessing pipeline: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
- [other] Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file: "Export ion mobility frame metadata (field strength, pressure, temperature, and MS actuals) to a text file."
- [methods] Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [other] Load a raw Agilent MassHunter (.d) or UIMF IM-MS data file into PNNL PreProcessor: "Load a raw Agilent MassHunter (.d) or UIMF IM-MS data file into PNNL PreProcessor."

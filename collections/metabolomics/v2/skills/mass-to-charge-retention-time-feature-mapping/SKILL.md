---
name: mass-to-charge-retention-time-feature-mapping
description: Use when you have centroided data-dependent acquisition (DDA) mzML files
  from LC- or GC-HRMS measurements and need to convert continuous raw mass spectrometric
  signals into discrete, quantifiable chromatographic features (m/z, RT, intensity,
  charge, isotope) before PFAS-specific prioritization or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS
  - OpenMS
  - Python
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
- pyOpenMS (Python interface to the C++ OpenMS library)
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data.
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-to-charge-retention-time-feature-mapping

## Summary

Extraction and delineation of chromatographic features from centroided high-resolution MS1 data by mapping signal intensity across the m/z and retention-time dimensions, producing tabular feature lists with mass, retention time, intensity, charge state, and isotope pattern annotations. This foundational step enables downstream feature prioritization in non-target screening workflows.

## When to use

You have centroided data-dependent acquisition (DDA) mzML files from LC- or GC-HRMS measurements and need to convert continuous raw mass spectrometric signals into discrete, quantifiable chromatographic features (m/z, RT, intensity, charge, isotope) before PFAS-specific prioritization or other analytical workflows. Use this skill when vendor software feature detection is unavailable or when reproducible, open-source feature extraction is required.

## When NOT to use

- Input is already a preprocessed feature table (e.g., from vendor software); re-running this skill would be redundant.
- Raw data is in profile (non-centroided) mode without prior centroiding; pyOpenMS FeatureFinder is optimized for centroided input.
- Data is from low-resolution MS (unit or nominal mass accuracy) where m/z–RT separation is insufficient to resolve overlapping features reliably.

## Inputs

- centroided mzML file (DDA mode, MS1 spectra)
- optional: blank/control mzML file (same format)
- FeatureFinder algorithm parameters (peak-picking thresholds, m/z tolerance, RT window)

## Outputs

- feature table (CSV or featureXML format)
- feature attributes: m/z, retention time, intensity, charge state, isotope pattern
- feature intensity matrix (features × samples)

## How to apply

Load the centroided DDA mzML file using pyOpenMS MSExperiment reader, then initialize the FeatureFinder algorithm with peak-picking parameters tuned for high-resolution MS1 data (typical settings balance signal-to-noise and feature width in both m/z and RT dimensions). Execute feature detection to identify connected peaks across the m/z–RT plane, then extract and annotate each feature's attributes (m/z, retention time, intensity, assigned charge state, isotope pattern). Export the resulting feature table to CSV or featureXML format for downstream processing. The rationale is that pyOpenMS provides vendor-independent, reproducible feature delineation by treating the MS1 data as a 2D intensity landscape and segmenting regions that exceed local noise thresholds, preserving chromatographic resolution and isotope information needed for later filtering or prioritization steps.

## Related tools

- **pyOpenMS** (Python interface to OpenMS FeatureFinder algorithm; loads centroided mzML and performs m/z–RT peak delineation) — https://github.com/OpenMS/OpenMS
- **OpenMS** (C++ library providing the underlying FeatureFinder algorithm and mzML I/O routines) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Converts vendor raw formats to mzML and performs centroiding if needed)
- **PFΔScreen** (Integrates this feature-mapping skill within a complete non-target PFAS screening workflow) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Feature table schema: all rows have valid m/z (> 0, typically 100–1000 Da), RT (non-negative, in acquisition order), intensity (> 0), charge state (≥ 1), and isotope pattern columns.
- Feature count and m/z–RT distribution match expectations for the sample complexity and chromatographic separation; visual inspection via interactive m/z vs. RT plot should show reasonable clustering (coeluting species, expected isotope spacing).
- Isotope pattern annotation: detected C13 or other isotopologue features align with theoretical monoisotopic m/z shifts (e.g., ~1 Da for singly charged compounds) and intensity ratios.
- Reproducibility: re-running the same mzML file with identical peak-picking parameters yields identical feature lists (bit-for-bit or within numerical precision of floating-point I/O).
- Blank correction (if control included): features in the blank are flagged or reported separately, enabling downstream filtering of contaminants (sample/blank intensity ratio > 3 is typical threshold in non-target screening).

## Limitations

- FeatureFinder performance depends on peak-picking parameter tuning; suboptimal thresholds may miss weak features or merge overlapping peaks, particularly in crowded m/z regions or at low RT resolution.
- pyOpenMS FeatureFinder assumes centroided input; uncorrected profile-mode data or improperly centroided spectra will degrade feature detection quality.
- Charge state and isotope pattern annotation rely on algorithm heuristics and may be ambiguous for multiply charged or overlapping isotope clusters; manual review of borderline cases is recommended.
- Data-dependent acquisition (DDA) MS2 information is preserved in mzML but not used during feature detection; MS2 alignment and fragment annotation occur in downstream prioritization steps.
- Runtime increases with spectral count (e.g., < 1 minute for 4000 spectra per sample on typical hardware), but very large datasets or complex matrix samples may require parameter optimization or memory management.

## Evidence

- [readme] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [other] Load centroided DDA mzML; initialize FeatureFinder; execute feature detection; extract attributes; export to CSV or featureXML: "Load centroided DDA mzML file using pyOpenMS MSExperiment reader. 2. Initialize FeatureFinder algorithm in pyOpenMS with appropriate peak-picking parameters for high-resolution MS1 data. 3. Execute"
- [readme] Raw data acceptance: vendor-independent mzML with DDA and centroided spectra: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [readme] Sample and blank measured under DDA with centroided spectra, ideally one collision energy per precursor: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
- [other] Feature extraction includes m/z, retention time, intensity, charge state, isotope pattern: "Extract feature attributes (m/z, retention time, intensity, charge state, isotope pattern) and construct feature table."

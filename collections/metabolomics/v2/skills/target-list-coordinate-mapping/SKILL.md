---
name: target-list-coordinate-mapping
description: Use when you have a CSV-formatted target list with m/z, retention time, or ion mobility identifiers and need to locate and extract peak abundances from raw MS data files (Agilent .d, Thermo .raw, Bruker .d, mzML) acquired across LC-MS, LC-IMS-MS, DDA, DIA, or direct infusion modes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3705
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - PeakQuant
  - Mirador
  techniques:
  - LC-MS
  - direct-infusion-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
- 'PeakQuant: Targeted MS1 peak abundance extraction for quantitation.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# target-list-coordinate-mapping

## Summary

Map user-supplied target coordinates (m/z, retention time, and ion mobility dimensions) to raw mass spectrometry data files in supported instrument formats to enable targeted feature extraction and quantitation. This skill bridges external target lists and instrument-native data by establishing precise coordinate correspondence for downstream quantitation workflows.

## When to use

You have a CSV-formatted target list with m/z, retention time, or ion mobility identifiers and need to locate and extract peak abundances from raw MS data files (Agilent .d, Thermo .raw, Bruker .d, mzML) acquired across LC-MS, LC-IMS-MS, DDA, DIA, or direct infusion modes. Use this skill when targets are defined externally (e.g., from prior discovery, literature, or external databases) and must be precisely matched to instrument-specific data coordinates with customizable tolerances.

## When NOT to use

- You do not have a pre-defined target list and need to perform untargeted feature discovery or peak detection—use untargeted peak-picking instead.
- Your input data is already a processed feature table or quantitation matrix; coordinate mapping is only applicable to raw instrument data.
- You require MS/MS fragment ion matching rather than MS1 parent ion extraction; use spectral library matching (TandemMatch) for fragment-based quantitation.

## Inputs

- Raw MS data files (Agilent .d, Thermo .raw, Bruker .d, mzML)
- Target list (CSV format with m/z, retention time, and/or ion mobility coordinates)
- Tolerance parameters (m/z range, retention time range, arrival time range if applicable)

## Outputs

- Quantitation table (CSV) with extracted MS1 peak abundances mapped to target coordinates
- Feature-to-target assignment map indicating which raw peaks matched which targets

## How to apply

Load raw MS data in a supported instrument format (Agilent .d, Thermo .raw, Bruker .d, or mzML) using IonToolPack. Load the target list in CSV format containing m/z, retention time, or other identifiers. Configure coordinate matching tolerances for m/z, retention time, and (if applicable) arrival time ranges based on your instrument resolution and expected peak width. PeakQuant's targeted extraction algorithm then maps each target coordinate to the corresponding MS1 peaks in the raw data, using the specified tolerances to handle instrument precision and chromatographic variation. The mapped abundances are compiled into a quantitation table and exported as CSV. Success depends on tolerance settings being appropriately calibrated to your instrument and acquisition method—tolerances that are too tight will miss true targets, while overly permissive tolerances risk false positives.

## Related tools

- **IonToolPack** (Host framework providing raw MS data import, format conversion, and GUI environment for target list ingestion and data visualization) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Core algorithm performing targeted MS1 peak abundance extraction and coordinate mapping using user-supplied target lists and customizable tolerances) — https://github.com/pnnl/IonToolPack
- **Mirador** (Visualization tool for validating coordinate mapping by displaying extracted ion chromatograms (XIC) and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Target list CSV is successfully parsed with all required coordinate columns (m/z, retention time, and optionally ion mobility) without format errors.
- Extracted peak abundances table has one row per target and non-zero abundance values for targets expected to be present in the sample; missing targets yield zero or null abundances only if they are genuinely absent.
- Retention time and m/z distributions of extracted peaks fall within the specified tolerance windows around target coordinates; out-of-tolerance matches indicate misconfigured tolerances.
- Comparison of extracted abundances with visual inspection of extracted ion chromatograms (XIC) in Mirador confirms that mapped peaks correspond to the visually apparent features at target coordinates.
- Quantitation CSV exports cleanly without data loss and can be reimported or compared against reference feature lists using Comparador.

## Limitations

- Coordinate mapping accuracy is constrained by tolerance parameter choices; users must empirically calibrate tolerances to instrument resolution and method—no automatic tolerance optimization is described.
- Mapping does not account for peak overlap or coelution; if two targets share very similar m/z or retention time, the algorithm may assign a single peak to both or fail to resolve them depending on tolerance configuration.
- Performance and memory requirements for large target lists or multi-dimensional data (LC-IMS-MS) are not quantified; scalability limits are not documented.
- No built-in handling of charge-state variants, isotopic variants, or adducts; target lists must be pre-processed to include all expected m/z variants separately.

## Evidence

- [other] Load raw MS data in a supported instrument format using IonToolPack. Load the target list (CSV format with m/z, retention time, or other identifiers). Extract MS1 peak abundances for each target using PeakQuant's targeted extraction algorithm.: "Load raw MS data in a supported instrument format using IonToolPack. Load the target list (CSV format with m/z, retention time, or other identifiers). Extract MS1 peak abundances for each target"
- [readme] PeakQuant: Targeted MS1 peak abundance extraction for quantitation.: "PeakQuant: Targeted MS1 peak abundance extraction for quantitation."
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS"
- [readme] extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges and tolerances: "extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges and tolerances"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"

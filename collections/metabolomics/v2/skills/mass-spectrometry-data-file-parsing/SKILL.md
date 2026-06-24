---
name: mass-spectrometry-data-file-parsing
description: Use when you receive raw MS data files from LC-MS, LC-IMS-MS, direct
  infusion, or DDA/DIA experiments and need to extract ion chromatograms, mobility
  heatmaps, quality metrics, or perform spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Mirador
  - IonToolPack
  - PeakQC
  - TandemMatch
  - PeakQuant
  techniques:
  - LC-MS
  - direct-infusion-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion
  chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots'
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-file-parsing

## Summary

Parse raw mass spectrometry data files from multiple instrument vendors and formats into a unified in-memory representation to enable downstream visualization, quality control, and quantitation workflows. This skill is essential because MS instrument vendors use proprietary binary formats (Agilent .d, Thermo .raw, Bruker .d) and open standards (mzML) that require format-specific readers and normalization before analysis.

## When to use

Apply this skill when you receive raw MS data files from LC-MS, LC-IMS-MS, direct infusion, or DDA/DIA experiments and need to extract ion chromatograms, mobility heatmaps, quality metrics, or perform spectral matching. The skill is triggered by the availability of raw instrument files (not already converted to feature tables or spectra libraries) and the need to preserve full chromatographic, mobility, and fragmentation information.

## When NOT to use

- Input is already a feature table (CSV with detected peaks, retention times, abundances) — use mass-spectrometry-peak-detection or mass-spectrometry-peak-quantitation instead.
- Input is a spectral library (MSP or NIST format) — use mass-spectrometry-spectral-library-matching instead.
- You only need to compare feature lists from different processing software without re-analyzing raw chromatography — use Comparador tool for CSV harmonization.

## Inputs

- Raw MS data file in Agilent .d, Thermo .raw, Bruker .d, or mzML format
- User-specified m/z range (min, max in Da or ppm tolerance)
- User-specified retention time range (min, max in minutes)
- User-specified arrival time / mobility range (min, max in ms or inverse reduced mobility units) — optional for LC-MS, required for LC-IMS-MS

## Outputs

- Parsed MS data structure indexed by (m/z, retention time, arrival time)
- Extracted ion chromatograms (XIC) as (time, intensity) vectors for each target m/z
- Ion mobility heatmaps (XIM) as 2D arrays (m/z × arrival time) with intensity
- MS/MS fragmentation spectra (precursor m/z, product m/z, intensity) for specified ranges
- Quality control metrics (peak count, intensity distribution, signal-to-noise ratios) per scan

## How to apply

Use Mirador's embedded data reader to load raw MS files in Agilent .d, Thermo .raw, Bruker .d, or mzML format through the IonToolPack GUI. The reader automatically detects instrument type and decompresses binary data into scanwise ion intensity arrays indexed by m/z, retention time (RT), and arrival time (for IMS data). Specify user-customizable m/z, RT, and arrival-time range parameters to define the region of interest. The parser extracts the subset of scans and peaks within those ranges, validates that all required dimensions (m/z, RT, optionally mobility) are present, and stores the result in an indexed structure compatible with downstream tools (Mirador visualization, PeakQC metrics, TandemMatch spectral matching, PeakQuant quantitation). Parsing is complete when all scans in the target range are readable and cross-referenced by time/m/z without gaps or decode errors.

## Related tools

- **Mirador** (Primary parser and visualization interface; handles multi-format data ingestion and exports parsed XIC/XIM/MS-MS as PDF and CSV) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Unified GUI container hosting Mirador data reader; manages file import and format auto-detection for LC-MS, LC-IMS-MS, and DDA/DIA modes) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Consumes parsed MS data to extract comprehensive quality metrics (PCA, peak counts, intensity distributions) from MS1 scans) — https://github.com/pnnl/IonToolPack
- **TandemMatch** (Receives parsed MS/MS fragmentation spectra for spectral library matching against MSP or CSV libraries) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Operates on parsed MS1 extracted ion chromatograms to extract targeted peak abundances for quantitation) — https://github.com/pnnl/IonToolPack

## Examples

```
Double-click IonToolPack.exe → Mirador tab → click Import → select raw .raw or .d file → specify m/z range (e.g., 100–1200 Da), RT range (e.g., 0–60 min), arrival time (optional) → click Process → export XIC/XIM/MS-MS as PDF or CSV.
```

## Evaluation signals

- All scans within the specified m/z, RT, and arrival-time ranges are successfully decoded and indexed without parse errors or truncation.
- Extracted ion chromatogram (XIC) for a known metabolite shows expected number of peaks and retention time consistency with instrument metadata.
- Ion mobility heatmap (XIM) displays expected mobility distribution for standards or controls (e.g., known lipid or peptide collision cross sections).
- MS/MS mirror plots align observed fragment m/z values with known library fragments within the specified m/z tolerance (user-defined, typically ±5–10 ppm).
- Output CSV and PDF files contain complete data rows (no null intensity or time values) and match expected dimensions (number of scans, peaks per scan, spectral fragmentation patterns).

## Limitations

- Parser supports only Agilent .d, Thermo .raw, Bruker .d, and mzML formats; other vendor formats (e.g., SCIEX .wiff, Waters .raw) are not mentioned and require external conversion.
- IMS arrival-time parsing requires specific instrument configuration; data from non-IMS instruments will not populate mobility dimensions.
- No changelog is publicly available, so compatibility with future or legacy instrument firmware versions is not documented.
- Direct infusion data (no chromatographic separation) requires special handling of retention-time range parameters; misspecification may exclude all scans.
- Parsing performance and memory consumption scale with file size and density of MS/MS fragmentation data; very large DIA experiments may require sub-range splitting.

## Evidence

- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [other] Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances.: "Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances."
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode,"
- [other] Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters.: "Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters."
- [other] Load raw MS data in multiple instrument formats using Mirador's data reader.: "Load raw MS data in multiple instrument formats using Mirador's data reader."

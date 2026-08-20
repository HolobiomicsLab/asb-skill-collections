---
name: extracted-ion-chromatogram-generation
description: Use when you have raw MS data (in Agilent .d, Thermo .raw, Bruker .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - Mirador
  - IonToolPack
  - PeakQuant
  techniques:
  - LC-MS
  - direct-infusion-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots'
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
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

# extracted-ion-chromatogram-generation

## Summary

Generate extracted ion chromatograms (XIC) from raw mass spectrometry data by isolating and visualizing ion signals within user-specified m/z and retention time windows. This skill is essential for targeted analysis of specific analytes in complex MS datasets and for quality assessment of chromatographic separations.

## When to use

Apply this skill when you have raw MS data (in Agilent .d, Thermo .raw, Bruker .d, or mzML format) and need to visualize the temporal profile of a specific ion or narrow m/z range to verify compound presence, assess peak shape and integration boundaries, or extract quantitative information for targeted metabolites. Use it especially when analyzing LC-MS or LC-IMS-MS experiments where retention time and m/z specificity are critical for distinguishing isobaric or co-eluting species.

## When NOT to use

- Input is a feature table or already-processed peak list; XIC generation requires raw time-series MS data.
- You do not know the target m/z or expected retention time; exploratory mass defect or untargeted analysis workflows are more appropriate.
- The m/z value is broader than ~50 ppm; at that width, multiple distinct analytes will co-extract and the chromatogram becomes ambiguous.

## Inputs

- Raw MS data file (Agilent .d, Thermo .raw, Bruker .d, mzML)
- m/z value (numeric, in Th)
- m/z tolerance (numeric, in ppm or Da)
- Retention time range (start and end, in minutes)
- Acquisition method type (LC-MS, LC-IMS-MS, DDA, DIA, direct infusion)

## Outputs

- Extracted ion chromatogram (XIC) plot (PDF format)
- Tabular XIC data (CSV format with retention time and intensity columns)
- XIC metrics (peak height, area, retention time at maximum intensity)

## How to apply

Load raw MS data into Mirador using its multi-format data reader. Specify the target m/z value and tolerance (in ppm or Da), and define the retention time range of interest. Mirador will extract all ions within the specified m/z and retention time windows and generate a chromatogram showing ion abundance as a function of retention time. The extraction operates on MS1 (full-scan) data by default; if MS/MS data is present, XIC can be generated for precursor or product ions. Export the resulting chromatogram as PDF for visualization or CSV for downstream quantitation. The quality of the XIC depends on the specified m/z tolerance—tighter tolerances (e.g., <5 ppm) reduce chemical noise but may miss isotopologues or adducts; wider tolerances (e.g., 10–50 ppm) capture more signal but increase background.

## Related tools

- **Mirador** (Performs raw MS data loading, XIC extraction, and export to PDF/CSV with customizable m/z, retention time, and tolerance parameters) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Host software suite providing GUI-based access to Mirador and other MS analysis tools; supports multiple instrument formats and omics-agnostic workflows) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Accepts XIC data or raw MS for targeted MS1 peak abundance extraction and quantitation after XIC generation) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- XIC peak is detected within the specified retention time window and m/z range with signal-to-noise ratio > 3:1.
- XIC integrates to a single, well-defined peak without artifactual shoulder or multiplet features (or multiple peaks are resolved if co-elution is expected).
- Exported CSV contains monotonically increasing retention time values with corresponding intensity values; no NaN or missing data in the time range of interest.
- Peak height and area reported in the XIC metrics are consistent across re-runs with identical m/z, RT, and tolerance parameters (reproducibility check).
- m/z tolerance used is appropriate for the instrument resolution: <5 ppm for high-resolution (Orbitrap, Q-TOF) instruments; 10–50 ppm acceptable for lower-resolution instruments (triple quadrupole in full-scan mode).

## Limitations

- XIC extraction is sensitive to m/z accuracy and mass calibration of the instrument; uncalibrated data may result in missed peaks or false extractions at the specified m/z ± tolerance.
- Mirador requires raw data in supported formats (Agilent, Thermo, Bruker, mzML); proprietary vendor formats not in this list cannot be processed without prior conversion.
- XIC does not deconvolute overlapping peaks in retention time; if two analytes with the same m/z co-elute, their signals will be summed in the chromatogram.
- GUI-based workflow in IonToolPack does not expose advanced parameters such as noise filtering, baseline correction, or smoothing; programmatic alternatives may be needed for batch processing or method optimization.
- No changelog or version history is documented, limiting reproducibility tracking across software updates.

## Evidence

- [other] Extract ion chromatograms (XIC) for the specified m/z and RT ranges.: "Extract ion chromatograms (XIC) for the specified m/z and RT ranges."
- [other] Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances.: "Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances."
- [readme] Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges and tolerances.: "Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode,"

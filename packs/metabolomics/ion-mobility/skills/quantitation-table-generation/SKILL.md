---
name: quantitation-table-generation
description: Use when you have raw MS data in a supported instrument format (Agilent .d, Thermo .raw, Bruker .d, mzML) and a defined list of m/z, retention time, or other identifiers for which you need to extract and quantify peak abundances across one or more samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - PeakQuant
  - Comparador
  techniques:
  - LC-MS
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

# quantitation-table-generation

## Summary

Extract targeted MS1 peak abundances from raw mass spectrometry data using a user-supplied target list and compile the results into a quantitation table for downstream statistical analysis. This skill transforms instrument-native MS data and CSV-formatted target lists into harmonized abundance matrices suitable for comparative and statistical workflows.

## When to use

Apply this skill when you have raw MS data in a supported instrument format (Agilent .d, Thermo .raw, Bruker .d, mzML) and a defined list of m/z, retention time, or other identifiers for which you need to extract and quantify peak abundances across one or more samples. Use this approach when a targeted (not untargeted discovery) quantitation strategy is appropriate—i.e., when your analyte list is pre-specified rather than learned from the data.

## When NOT to use

- Input data is already a pre-compiled feature/abundance table or quantitation matrix; use Comparador or downstream statistical tools instead.
- Your analysis goal is untargeted discovery and you lack a pre-specified list of analytes; consider PeakQC for quality assessment or other feature detection workflows first.
- Raw MS data is in an unsupported instrument format not listed (Agilent, Thermo, Bruker, mzML).

## Inputs

- Raw mass spectrometry data files (Agilent .d, Thermo .raw, Bruker .d, mzML)
- Target list in CSV format with m/z, retention time, and/or other identifiers

## Outputs

- Quantitation table (CSV format) with sample rows and target analyte columns containing extracted peak abundances

## How to apply

Load raw MS data in a supported instrument format using IonToolPack. Prepare a target list in CSV format containing m/z, retention time, and/or other identifiers for your analytes of interest. Import both the raw data and target list into PeakQuant, which applies its targeted extraction algorithm to identify and measure MS1 peak abundances for each target across the dataset. The algorithm respects user-specified m/z and retention time tolerances (customizable ranges) to assign peaks to targets. Compile the extracted abundances into a quantitation table with rows representing samples and columns representing targets, then export the result as CSV for downstream analysis (statistical testing, normalization, or comparison with other datasets via Comparador).

## Related tools

- **IonToolPack** (Host software suite that orchestrates raw MS data import across multiple instrument formats and provides the GUI interface for launching PeakQuant and exporting results) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Core tool that executes targeted MS1 peak abundance extraction algorithm using the supplied target list and customizable m/z and retention time tolerances) — https://github.com/pnnl/IonToolPack
- **Comparador** (Downstream tool for comparing and harmonizing quantitation tables generated from different acquisition methods or processing software) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Quantitation table is valid CSV with sample identifiers as rows and target m/z/identifiers as columns; all cells contain numeric abundance values or explicit missing-value indicators.
- Number of targets in output table matches the number of entries in the input target list; no targets are silently dropped.
- Extracted abundances fall within expected dynamic range for the instrument and sample type; no abundance values are negative or suspiciously uniform across samples.
- Peaks assigned to targets respect the specified m/z and retention time tolerances; visual inspection of extracted ion chromatograms (XIC) in Mirador confirms correct peak assignment for a random subset of targets.
- Quantitation table can be successfully imported into downstream tools (e.g., Comparador for cross-method comparison, or statistical analysis software) without format errors.

## Limitations

- PeakQuant operates on targeted lists only; it cannot discover or quantify analytes not in the supplied target list.
- Extraction relies on user-specified m/z and retention time tolerances; incorrect or overly broad tolerances may cause misassignment of peaks to wrong targets or abundance inflation from co-eluting species.
- Performance and accuracy depend on MS1 peak quality; poor ionization, peak overlap, or high chemical noise may compromise abundance estimates.
- No changelog is available in the repository, limiting visibility into algorithm improvements or bug fixes between versions.

## Evidence

- [other] PeakQuant is designed to perform targeted MS1 peak abundance extraction for quantitation purposes, operating on user-supplied target lists to generate quantitation data.: "PeakQuant is designed to perform targeted MS1 peak abundance extraction for quantitation purposes, operating on user-supplied target lists to generate quantitation data."
- [other] Workflow prescribes loading raw MS data, loading CSV target list, extracting MS1 peak abundances per target, compiling into quantitation table, and exporting as CSV.: "1. Load raw MS data in a supported instrument format using IonToolPack. 2. Load the target list (CSV format with m/z, retention time, or other identifiers). 3. Extract MS1 peak abundances for each"
- [readme] IonToolPack reads multiple instrument formats, requires no installation, and provides omics-agnostic functionality across metabolomics, lipidomics, and proteomics.: "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] Supported MS data formats include Agilent .d, Thermo .raw, Bruker .d, and mzML, with support for LC-MS, LC-IMS-MS, and DDA/DIA acquisition modes.: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode"
- [readme] PeakQuant feature description emphasizes targeted MS1 peak abundance extraction with customizable m/z, RT, and arrival time ranges and tolerances.: "Targeted MS1 peak abundance extraction for quantitation."

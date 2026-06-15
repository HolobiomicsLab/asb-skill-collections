---
name: biochemical-transformation-matching
description: Use when you have a filtered FT-ICR MS peak list (m/z values and assigned molecular formulas per sample) and wish to reconstruct biochemical transformation networks ab initio to characterize how microbial or environmental metabolic pathways differ across conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDirect
  - Cytoscape
  - KEGG database
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# biochemical-transformation-matching

## Summary

Identify chemically transformed species in FT-ICR MS peak data by matching observed mass differences against a reference biochemical transformation key, yielding a biotic/abiotic-classified edge list for metabolic pathway networks. This skill enables quantification of microbial metabolic diversity and detection of hub metabolites from high-resolution mass spectrometry.

## When to use

Apply this skill when you have a filtered FT-ICR MS peak list (m/z values and assigned molecular formulas per sample) and wish to reconstruct biochemical transformation networks ab initio to characterize how microbial or environmental metabolic pathways differ across conditions. Use it specifically when mass-difference network topology (rather than compound identity alone) is your analytical target, and when you have or can construct a reference key of expected metabolic transformations with known mass shifts (e.g., oxidation, methylation, decarboxylation).

## When NOT to use

- Raw FT-ICR MS spectra without prior molecular formula assignment—MetaboDirect requires pre-processed peak data with assigned formulas as input
- Samples with very low peak count (<50 peaks with formula assignment) where pairwise transformation matching will yield sparse or unreliable networks
- When the reference transformation key does not match your biological system or metabolic context (e.g., using a microbial key for plant-only samples without validation)

## Inputs

- Filtered peak list CSV (m/z values, molecular formulas, per-sample abundance)
- Reference biochemical transformation key (transformation names, mass shifts, biotic/abiotic classification)

## Outputs

- Per-sample edge CSV files (source m/z, target m/z, transformation type, mass error)
- Node CSV file (m/z, molecular formula, compound class for all detected peaks)
- Transformation statistics CSV (count per sample, frequency distribution)
- Cytoscape-formatted node and edge files for network visualization

## How to apply

Load the filtered peak list (CSV format with m/z and molecular formula columns) and a reference biochemical transformation key containing predefined masses of common metabolic reactions. Calculate all pairwise mass differences between detected peaks within each sample independently. For each mass difference, match it to the reference key and retain only matches with mass error ≤1 ppm against reference values—this tight tolerance is critical for distinguishing true biochemical transformations from noise in high-resolution data. Classify each retained transformation as biotic or abiotic based on prior categorization in your reference key. Generate output edge CSV files (source peak m/z, target peak m/z, transformation type, and error) for each sample, and a node CSV file with all detected peaks, their m/z, molecular formula, and compound class. Output summary statistics (transformation count per sample, frequency distribution) to guide interpretation of pathway complexity differences.

## Related tools

- **MetaboDirect** (Command-line pipeline that implements the full workflow: peak filtering, transformation network generation, and network file output for Cytoscape import) — https://github.com/Coayala/MetaboDirect
- **Cytoscape** (Network visualization and analysis of the generated transformation node and edge files; required version 3.8 and above with FileTransfer plugin)
- **KEGG database** (Optional reference for biochemical transformation classification and biotic/abiotic categorization during pipeline execution)

## Examples

```
metabodirect -i filtered_peaks.csv -r transformation_key.csv -o output_dir
```

## Evaluation signals

- Mass error for all matched transformations must be ≤1 ppm; verify by checking error column in output edge CSV
- Node CSV contains all peaks from input peak list with m/z, formula, and compound class; row count should match input peak count
- Edge CSV contains only pairs of peaks with valid mass differences matching the reference transformation key; no spurious or unmatched differences should appear
- Per-sample transformation counts should be reasonable given peak density (e.g., 500 peaks might yield 50–500 transformations depending on network connectivity); extreme outliers may indicate reference key mismatch or data quality issues
- Cytoscape-formatted files are importable without error and yield visualizable networks with both nodes and edges populated; network should show identifiable hub metabolites (high-degree nodes)

## Limitations

- Cannot distinguish chemical isomers—FT-ICR MS provides m/z and formula only, not structural information, so multiple isomers map to the same peak
- Transformation matching depends critically on the completeness and accuracy of the reference biochemical transformation key; missing or incorrect transformations in the key will be undetected
- Mass error tolerance of 1 ppm is stringent and may miss true biological transformations if peak calibration or formula assignment error exceeds this threshold; requires high-quality input peak data
- Biotic vs. abiotic classification is only as reliable as the prior categorization in the reference key; manual curation or validation against literature is recommended for novel metabolic contexts

## Evidence

- [other] MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences: "MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences"
- [other] Calculate all pairwise mass differences between detected peaks in each sample. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values.: "Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error"
- [other] Classify matched transformations as biotic or abiotic based on prior categorization: "Classify matched transformations as biotic or abiotic based on prior categorization."
- [other] Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample: "Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample."
- [abstract] MetaboDirect is uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network-based approach): "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach)"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT‑ICR MS spectra or any other high‑resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT‑ICR MS spectra or any other high‑resolution MS technique"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above): "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"

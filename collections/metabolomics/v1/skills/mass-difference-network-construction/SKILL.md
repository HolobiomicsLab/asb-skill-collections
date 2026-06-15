---
name: mass-difference-network-construction
description: Use when you have a filtered peak list (CSV with m/z values and assigned molecular formulas) from FT-ICR MS and want to infer biochemical transformations occurring in microbial or environmental samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MetaboDirect
  - KEGG database
  - Cytoscape
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

# mass-difference-network-construction

## Summary

Automatically generate biochemical transformation networks from FT-ICR MS peak data by computing all pairwise mass differences and matching them against a reference transformation key with strict mass error tolerance. This skill enables identification of hub metabolites and quantification of metabolic pathway differences across samples.

## When to use

You have a filtered peak list (CSV with m/z values and assigned molecular formulas) from FT-ICR MS and want to infer biochemical transformations occurring in microbial or environmental samples. Use this skill when you need to understand which metabolic reactions are active, identify metabolites involved in multiple transformations, or compare transformation networks across treatment groups or samples.

## When NOT to use

- Input peak list has not been assigned molecular formulas or has not been filtered for isotopic presence and formula assignment error — preprocessing must be completed first.
- Raw FT-ICR MS spectra are available but have not undergone signal processing and molecular formula assignment — use upstream signal processing tools first.
- Transformation networks are not relevant to your research question (e.g., you only need abundance profiles or elemental composition, not reaction pathways).

## Inputs

- Filtered peak list (CSV): m/z values, molecular formulas, compound class assignments
- Reference biochemical transformation key: predefined masses of common metabolic reactions
- Sample identifiers and grouping metadata

## Outputs

- Edge CSV files per sample: source peak m/z, target peak m/z, transformation type, mass error
- Node CSV file: detected peaks with m/z values, molecular formulas, compound class assignments
- Transformation statistics CSV: count per sample, transformation frequency distribution
- Summary bar plots: transformation counts and frequency distributions
- Cytoscape-formatted node and edge files for network visualization

## How to apply

Load the filtered peak list and a reference biochemical transformation key containing predefined masses of common metabolic reactions (e.g., from KEGG). Calculate all pairwise mass differences between detected peaks within each sample. For each mass difference, query the reference key and retain matches with mass error ≤1 ppm. Classify matched transformations as biotic or abiotic using prior categorization. Generate edge CSV files for each sample (containing source peak m/z, target peak m/z, transformation type, and error) and a unified node CSV file with all detected peaks, their m/z values, molecular formulas, and compound class assignments. Output transformation statistics (count per sample, transformation frequency distribution) as summary CSV and visualizations. Format node and edge files for Cytoscape import to enable interactive network visualization and hub metabolite identification.

## Related tools

- **MetaboDirect** (Command-line pipeline that implements mass-difference network generation, transformation matching against KEGG, and automated Cytoscape file export) — https://github.com/Coayala/MetaboDirect
- **KEGG database** (Source of predefined biochemical transformation masses and reaction types for reference transformation key)
- **Cytoscape** (Interactive network visualization and analysis of generated transformation networks; requires version 3.8 and above and FileTransfer plugin)

## Examples

```
metabodirect --input peaks.csv --reference_transformations kegg_transformations.csv --output results/ --ppm_tolerance 1.0 --cytoscape_export
```

## Evaluation signals

- Edge CSV files contain only transformations with mass error ≤1 ppm against reference values; spot-check a sample of edges to verify error calculations.
- Node CSV file is complete: all peaks in the input filtered list appear as nodes with m/z, molecular formula, and compound class fields populated.
- Transformation count statistics are reasonable: typically report average counts per sample and frequency distribution of transformation types across the cohort.
- Cytoscape network imports without errors and renders node-edge topology that is visually interpretable; hub metabolites (high node degree) should correspond to known central metabolites in the system.
- Transformation classification (biotic vs. abiotic) is consistent with prior biochemical knowledge; validate that transformation types match expected metabolic pathways for the sample system (e.g., bacterium-phage interactions, plant-microbe interactions).

## Limitations

- Mass-difference networks cannot distinguish between chemical isomers; high-resolution m/z alone does not resolve isomeric structures.
- Transformation matching relies on strict 1 ppm mass error tolerance; transformations with larger mass errors may be missed or confounded with near-identical reaction masses.
- Network construction is ab initio and does not require validation against authenticated biochemical databases; some matched transformations may be spurious if the reference key includes unvalidated reactions.
- Signal suppression or enhancement in FT-ICR MS can confound peak detection and abundance, potentially leading to missing or artificially enhanced transformation edges.
- MetaboDirect does not provide raw spectra data preprocessing; input peaks must already be processed and formula-assigned using external tools.

## Evidence

- [other] MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences: "MetaboDirect generates transformation networks ab initio from high-resolution mass spectrometry data by identifying chemically transformed species using clearly defined mass differences"
- [other] Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values.: "Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error"
- [other] Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample.: "Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample."
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach): "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach)"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above): "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"

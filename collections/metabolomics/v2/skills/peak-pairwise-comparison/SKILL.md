---
name: peak-pairwise-comparison
description: Use when after molecular formula assignment and peak filtering are complete,
  when you have a filtered peak list (m/z values and molecular formulas) and want
  to discover biochemical transformations without prior knowledge of reaction networks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - MetaboDirect
  - Cytoscape
  - KEGG database
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-pairwise-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically compare all pairs of detected peaks in FT-ICR MS samples by calculating mass differences to identify potential biochemical transformations. This pairwise comparison is the foundation for generating mass-difference networks that reveal metabolic pathway connectivity and hub metabolites.

## When to use

Apply this skill after molecular formula assignment and peak filtering are complete, when you have a filtered peak list (m/z values and molecular formulas) and want to discover biochemical transformations without prior knowledge of reaction networks. Use it specifically when investigating how microbial metabolic pathways differ across samples or when identifying hub metabolites involved in many reactions.

## When NOT to use

- Raw, unprocessed FT-ICR MS spectra without prior molecular formula assignment — MetaboDirect does not provide raw spectra preprocessing
- Peak lists that have not been filtered for isotopic presence (13C peaks), formula assignment error (≥0.5 ppm), or sample presence thresholds — the comparison requires clean, validated peaks
- When chemical isomer separation or fine resolving power is critical — DI FT-ICR MS cannot separate isomers and signal suppression or enhancement can confound results

## Inputs

- Filtered peak list (CSV): m/z values, assigned molecular formulas, abundance values, and compound class assignments
- Reference biochemical transformation key: predefined masses of common metabolic reactions with biotic/abiotic categorization

## Outputs

- Edge CSV files per sample: source peak m/z, target peak m/z, transformation type, mass error
- Node CSV file: all detected peaks with m/z, molecular formula, compound class
- Transformation statistics (CSV): count per sample, transformation frequency distribution
- Cytoscape-importable node and edge files for network visualization

## How to apply

Load the filtered peak list (CSV format with m/z values and assigned molecular formulas) for each sample. Calculate all pairwise mass differences between detected peaks within that sample. Match each calculated mass difference against a reference biochemical transformation key (predefined masses of common metabolic reactions) using a mass error threshold of ≤1 ppm. Retain only transformations meeting this tolerance. Classify matched transformations as biotic or abiotic using prior biochemical categorization. Output edge lists per sample (source peak m/z, target peak m/z, transformation type, observed mass error) and consolidated node files with all detected peaks, their m/z values, molecular formulas, and compound class assignments.

## Related tools

- **MetaboDirect** (Executes pairwise mass difference calculation, transformation matching against reference keys, and generates edge/node CSV outputs for network construction) — https://github.com/Coayala/MetaboDirect
- **Cytoscape** (Imports and visualizes the node and edge CSV files as biochemical transformation networks)
- **KEGG database** (Provides reference biochemical transformation definitions and metabolic reaction context)

## Evaluation signals

- Mass error of retained transformations is ≤1 ppm when compared to reference biochemical transformation key entries
- Edge CSV files contain valid pairwise comparisons (no self-loops, source and target m/z values present in node file)
- Transformation frequency distribution shows expected patterns (some transformations appear in multiple samples, others are sample-specific)
- Node file accounts for all peaks in the input filtered peak list (row count consistency)
- Generated edge/node files import without schema errors into Cytoscape and produce connected or near-connected components representing metabolic pathways

## Limitations

- Pairwise comparison scales quadratically with peak count; samples with very large peak lists (>5000 peaks) may require extended computation time
- Mass error tolerance (1 ppm) may miss true transformations in lower-resolution instruments or may retain false positives in complex mixtures with overlapping m/z regions
- Signal suppression or enhancement in direct injection MS can mask real peaks or introduce artificial ones, confounding transformation network interpretation
- Transformation matching depends entirely on the completeness and accuracy of the reference biochemical transformation key; novel or poorly characterized reactions will not be detected

## Evidence

- [other] Calculate all pairwise mass differences between detected peaks in each sample and match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values.: "Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error"
- [abstract] MetaboDirect is uniquely able to automatically generate biochemical transformation networks based on mass differences.: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences"
- [other] The networks are designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions.: "networks designed to quantify differences in microbial metabolic pathways and identify hub metabolites involved in many reactions"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after initial processing of raw FT-ICR MS spectra.: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra"
- [intro] Signal suppression or enhancement is a key drawback that can confound downstream data analysis.: "signal suppression or enhancement that can confound downstream data analysis"

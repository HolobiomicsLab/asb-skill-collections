---
name: mass-difference-network-construction
description: Use when you have a preprocessed peak list (m/z values and assigned molecular formulas) from direct injection FT-ICR MS of a complex organic mixture (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - NumPy
  - pandas
  - KEGG database
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 and requires the Python dependencies NumPy, pandas
- developed in Python 3.8 [38] and R 4.0.2 [39]
- Networks are then constructed using Cytoscape and colored based on their molecular class
- Networks are then constructed using Cytoscape [79] and colored based on their molecular class.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-difference-network-construction

## Summary

Constructs biochemical transformation networks ab initio from FT-ICR MS peak data by computing all pairwise mass differences between detected m/z values and matching them against a reference database of known biochemical transformations. This skill enables discovery of metabolic pathways and hub metabolites without requiring compound identification or chromatographic separation.

## When to use

Apply this skill when you have a preprocessed peak list (m/z values and assigned molecular formulas) from direct injection FT-ICR MS of a complex organic mixture (e.g., environmental samples, microbial cultures, or natural organic matter), and you want to infer which biochemical transformations have occurred within the sample. Use it specifically when ultra-high mass accuracy (sub-ppm error tolerance) allows reliable matching of mass differences to known transformations, and when you seek to identify transformation hubs and network topology rather than individual compound identities.

## When NOT to use

- Input peak list lacks molecular formula assignments or has low mass accuracy (>5 ppm error); mass difference matching will fail or produce false positives.
- Sample has been chromatographically separated (LC-MS) prior to analysis; you should use retention time and fragmentation patterns instead of mass-difference networks.
- Goal is to identify individual compound structures or absolute metabolite quantities; transformation networks reveal relative pathway connectivity, not species identity or abundance.

## Inputs

- Preprocessed peak m/z list (CSV format)
- Assigned molecular formulas for peaks
- Reference biochemical transformation database with mass differences and biotic/abiotic classification
- Mass accuracy specification for FT-ICR MS instrument (typically sub-ppm)

## Outputs

- Edge table (CSV): source m/z, target m/z, mass difference, transformation name, biotic/abiotic class
- Node table (CSV): peak m/z values, molecular class assignments
- Cytoscape-compatible network files
- Network statistics (degree distribution, component count, hub metabolite rankings)

## How to apply

Load the preprocessed peak m/z list and molecular formulas from CSV output. Compute all pairwise mass differences using vectorized subtraction (NumPy) across the entire peak set. Match each observed mass difference against a reference biochemical transformation key, retaining only matches with ≤1 ppm error tolerance to exploit FT-ICR MS mass accuracy. Classify each matched transformation as biotic or abiotic according to the reference key. Generate an edge table (CSV) recording source m/z, target m/z, mass difference, transformation name, and classification for all validated transformations. Generate a complementary node table (CSV) listing all peaks and their molecular class assignments. Export both tables in Cytoscape-compatible format and compute network statistics (degree distribution, connected component count) to characterize metabolic topology.

## Related tools

- **MetaboDirect** (Command-line pipeline orchestrating full mass-difference network construction workflow including pairwise difference computation, transformation matching, network export, and visualization) — https://github.com/Coayala/MetaboDirect
- **NumPy** (Vectorized array computation for efficient pairwise mass difference subtraction across peak sets)
- **pandas** (Tabular data manipulation for loading peak lists, filtering results, and generating edge/node CSV tables)
- **Cytoscape** (Interactive network visualization and analysis of generated transformation graphs with degree/topology statistics)
- **KEGG database** (Reference source for known biochemical transformations and mass differences used to build the transformation matching key)

## Examples

```
metabodirect -i sample_peaks.csv -f formulas.csv -o output_dir --transformation_db kegg_transformations.csv --ppm_tolerance 1
```

## Evaluation signals

- All pairwise mass differences computed without exception (output edge count ≤ n(n−1)/2 where n = peak count); missing pairs indicate computation failure.
- Every matched transformation mass difference is within ≤1 ppm error tolerance of the reference database entry; audit a random sample of 50+ matches against KEGG.
- Edge and node tables have consistent m/z coverage (all m/z values in edge table appear in node table; node table contains only m/z present in raw input); schema validation for required columns (source m/z, target m/z, mass difference, transformation name, biotic/abiotic).
- Network exhibits expected topological properties for metabolic systems: degree distribution is skewed (few hub metabolites with high degree); connected component count is reasonable relative to sample complexity (typically 1–5 major components for environmental samples).
- Biotic transformations align with known microbial metabolism (e.g., demethylation, oxidation, acetylation); spot-check transformation types against literature on sample type (e.g., soil, peatland leachate, wastewater).

## Limitations

- Cannot distinguish chemical isomers: mass-difference networks conflate structural isomers with identical mass; FT-ICR MS lacks fine resolving power to separate them without complementary NMR or MS/MS fragmentation.
- Ion suppression and signal enhancement can cause false negatives (missed transformations) or false positives (spurious peaks misidentified as transformed metabolites).
- Reference transformation database must be curated and comprehensive; missing or incorrect entries in the reference key will produce incomplete or incorrect networks.
- Mass difference matching assumes transformations are elementary (single step); multi-step pathways involving intermediate species undetected in the sample will not be resolved.

## Evidence

- [other] MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically transformed species: "MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically"
- [other] Nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations, with network outputs showing hub metabolites and transformation types: "nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations, with network outputs showing hub metabolites and transformation types"
- [other] Compute all pairwise mass differences between peaks using vectorized subtraction. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance.: "Compute all pairwise mass differences between peaks using vectorized subtraction. 3. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm"
- [other] Classify retained transformations as biotic or abiotic according to the reference key. Generate edge table (CSV) listing source peak m/z, target peak m/z, mass difference, transformation name, and classification.: "Classify retained transformations as biotic or abiotic according to the reference key. 5. Generate edge table (CSV) listing source peak m/z, target peak m/z, mass difference, transformation name, and"
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences"
- [intro] Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers, lack of: "Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers"
- [methods] consists of two main processes: the calculation of mass-based chemical transformations: "consists of two main processes: the calculation of mass-based chemical transformations"

---
name: cytoscape-edge-node-file-formatting
description: Use when after computing pairwise mass-difference transformations between FT-ICR MS peaks and matching them to a reference biochemical transformation key, you have putative edge data (source peak, target peak, transformation type, mass error) and node data (peaks with m/z, molecular formula.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDirect
  - Cytoscape
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- Networks are then constructed using Cytoscape [79] and colored based on their molecular class.
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

# cytoscape-edge-node-file-formatting

## Summary

Format transformation network data (edges and nodes) from mass-difference network analysis into CSV files compatible with Cytoscape import for interactive visualization and network exploration. This skill bridges algorithmic metabolite transformation detection and graph-based visualization of biochemical networks.

## When to use

After computing pairwise mass-difference transformations between FT-ICR MS peaks and matching them to a reference biochemical transformation key, you have putative edge data (source peak, target peak, transformation type, mass error) and node data (peaks with m/z, molecular formula, compound class). Format these into Cytoscape CSV before interactive network exploration or topological analysis (e.g., hub metabolite identification).

## When NOT to use

- Input data has not yet been matched against the reference transformation key — formatting will produce empty or disconnected edges.
- Peaks lack assigned molecular formulas; node file cannot be populated with required compound class metadata.
- Mass difference matching has not been filtered to acceptable error threshold (>1 ppm); edge list will contain too many spurious transformations to visualize meaningfully.

## Inputs

- CSV file: filtered peak list with m/z values and assigned molecular formulas
- Reference biochemical transformation key (predefined masses of metabolic reactions)
- Pairwise mass difference matrix (all m/z differences per sample)
- Mass-matched transformation records (source m/z, target m/z, transformation ID, error in ppm)

## Outputs

- CSV file: edge list for Cytoscape (source m/z, target m/z, transformation type, mass error)
- CSV file: node list for Cytoscape (m/z, molecular formula, compound class)
- Cytoscape-compatible network file (.cys session, optional)

## How to apply

Prepare two separate CSV files: (1) an edge file containing one row per putative transformation with columns for source peak m/z, target peak m/z, transformation type (biotic or abiotic), and mass error (ppm); (2) a node file listing all detected peaks with m/z value, assigned molecular formula, and compound class. Ensure edge m/z values match node m/z values exactly to enable proper graph linking. Include transformation metadata (e.g., mass error ≤1 ppm tolerance from reference key matching) as edge attributes. Export both files with UTF-8 encoding and import both simultaneously into Cytoscape (version 3.8+) using the 'Import Network from File' dialog to reconstruct the full transformation network as an undirected or directed graph suitable for layout and visual analysis.

## Related tools

- **MetaboDirect** (Computes mass-difference transformations, classifies them as biotic/abiotic, and generates edge/node CSV files formatted for Cytoscape import) — https://github.com/Coayala/MetaboDirect
- **Cytoscape** (Imports formatted edge and node CSV files to construct, visualize, and analyze the transformation network interactively)

## Evaluation signals

- Edge CSV contains exactly 4 columns (source m/z, target m/z, transformation type, mass error) with one row per putative transformation; no missing or malformed entries.
- Node CSV contains exactly 3 columns (m/z, molecular formula, compound class) with one row per unique detected peak; all m/z values in edge CSV are present in node CSV.
- Mass error values in edge CSV are numeric, ≤1 ppm, and represent the deviation from reference transformation key values.
- Cytoscape successfully imports both files without parsing errors; network graph renders with expected node count and edge density reflecting the transformation dataset size.
- Transformation type column contains only expected biotic/abiotic categories with no null or mixed case values.

## Limitations

- Formatting does not validate chemical feasibility of matched transformations — only m/z and error tolerance are checked. False positives are possible if mass-matching threshold is too permissive.
- Node and edge files do not capture peak abundance or intensity information; visualization reflects network topology but not quantitative metabolite dynamics across samples.
- Formatting assumes m/z values are unique per sample; duplicate m/z entries in input will cause ambiguous linking in Cytoscape.
- MetaboDirect does not provide raw spectra preprocessing; input peak lists must be pre-processed and formula-assigned by external tools.

## Evidence

- [other] Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample.: "Generate edge CSV files containing putative transformations (source peak m/z, target peak m/z, transformation type, error) for each sample."
- [other] Generate node CSV file with all detected peaks, their m/z values, molecular formulas, and compound class assignments.: "Generate node CSV file with all detected peaks, their m/z values, molecular formulas, and compound class assignments."
- [other] Prepare node and edge files formatted for Cytoscape import.: "Prepare node and edge files formatted for Cytoscape import."
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
- [other] Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm against reference values.: "Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error ≤1 ppm"

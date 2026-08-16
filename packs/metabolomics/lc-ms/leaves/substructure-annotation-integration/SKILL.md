---
name: substructure-annotation-integration
description: Use when you have (1) a GNPS molecular network (classical or feature-based) with cluster/feature identifiers, (2) MS2LDA output containing Mass2Motif assignments with probability and overlap scores for those same clusters/features, and (3) a goal to annotate network nodes with substructural and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  - build: coll_molnetenhancer_cq
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo9070144
  all_source_dois:
  - 10.3390/metabo9070144
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# substructure-annotation-integration

## Summary

Integrate MS2LDA Mass2Motif substructural annotations and chemical class information onto GNPS molecular network nodes to produce annotated network outputs suitable for visualization and molecular family interpretation. This skill bridges spectral motif discovery and network-level chemical structure annotation.

## When to use

Apply this skill when you have (1) a GNPS molecular network (classical or feature-based) with cluster/feature identifiers, (2) MS2LDA output containing Mass2Motif assignments with probability and overlap scores for those same clusters/features, and (3) a goal to annotate network nodes with substructural and chemical class metadata for downstream visualization or family-level chemical interpretation.

## When NOT to use

- MS2LDA job has not been created using the appropriate MGF input (clustered spectra from GNPS for classical networks, or MZmine MGF for feature-based networks); motif-to-cluster/feature matching will fail.
- GNPS network already contains motif annotations from another source; re-annotation may introduce redundant or conflicting labels.
- Probability or overlap thresholds have not been validated in the MS2LDA web app; unfiltered summary tables may contain spurious low-confidence motif assignments that propagate into the network.

## Inputs

- GNPS classical molecular network file (.graphml or edge/node tables)
- GNPS feature-based molecular network file (.graphml or edge/node tables)
- MS2LDA Mass2Motif summary table (TSV or CSV with cluster/feature IDs, motif names, probability, overlap scores)
- Optional: chemical class annotations (TSV with class assignments per cluster/feature)

## Outputs

- Annotated node table (TSV) with cluster/feature IDs, MS2LDA Mass2Motif assignments, probability/overlap scores, and top shared motifs per molecular family
- Annotated edge table (TSV) with interaction types labeled by shared Mass2Motifs
- GraphML network file with embedded substructure and chemical class annotations
- Visualization-ready network suitable for import into Cytoscape

## How to apply

Load the GNPS network file (in classical or feature-based format) and MS2LDA Mass2Motif summary table, then use pyMolNetEnhancer or RMolNetEnhancer to overlay motif assignments onto network nodes by matching cluster/feature identifiers. Filter Mass2Motif results using user-defined probability (default 0.01) and overlap (default 0.3) thresholds to retain only high-confidence substructure assignments. Optionally integrate chemical class predictions if available. Output annotated node and edge tables (TSV format) and GraphML network file with embedded motif labels and interaction types. The probability and overlap thresholds should ideally be set in the MS2LDA web app first to ensure the summary table reflects these filters before integration.

## Related tools

- **pyMolNetEnhancer** (Python module that performs the core mapping of MS2LDA substructures and chemical classes onto feature-based or classical GNPS molecular networks) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package implementation of substructure and chemical class integration onto GNPS molecular networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Generates classical and feature-based molecular networks (nodes = clusters/features, edges = spectral similarity); provides network file formats and cluster/feature identifiers required for motif integration)
- **MS2LDA** (Performs latent Dirichlet allocation on MS/MS spectra to discover Mass2Motif substructures; outputs summary tables with probability and overlap scores that are mapped onto network nodes) — http://ms2lda.org/
- **Cytoscape** (Visualization tool for rendering annotated networks with colored nodes (by top shared motifs) and edges (by interaction type/shared motifs))

## Evaluation signals

- Node identifiers in the output match input GNPS cluster/feature IDs and are linked to at least one Mass2Motif with probability ≥ threshold and overlap ≥ threshold.
- Edges in the output edge table correctly identify shared Mass2Motifs between connected nodes and label interaction type accordingly.
- GraphML output imports successfully into Cytoscape without errors; nodes can be colored by TopSharedMotifs and edges by interaction type using discrete mapping.
- Top shared motifs per molecular family (network component index) are ranked and limited to the specified 'top' parameter (default 5), and motif counts match manual review of input MS2LDA summary.
- Optional chemical class annotations are present in output node table and do not contain null values for clusters/features that were assigned classes in the input file.

## Limitations

- Server connection timeouts can occur when retrieving large MS2LDA summary files; manual download from ms2lda.org is recommended as an alternative.
- Feature-based networks require MS2LDA experiments created from MZmine-generated MGF files; incompatible MGF formats will result in failed feature identifier matching.
- Probability and overlap thresholds set in the integration step do not retroactively filter the MS2LDA input table; filtering must occur in the MS2LDA web app Experimental Options tab beforehand for reproducibility.
- Network visualizations with very large motif labels or dense node annotations may become difficult to interpret in Cytoscape; additional filtering or layout optimization may be needed.

## Evidence

- [other] pyMolNetEnhancer is a python module that integrates substructure information from MS2LDA within mass spectral molecular networks created through the GNPS platform, with distinct implementation pathways for feature-based network variants.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [other] Execute pyMolNetEnhancer's feature-based mapping function to overlay MS2LDA substructural information onto network nodes, matching nodes by feature identifiers.: "Execute pyMolNetEnhancer's feature-based mapping function to overlay MS2LDA substructural information onto network nodes, matching nodes by feature identifiers."
- [readme] Filter thresholds for probability (default 0.01) and overlap (default 0.3) applied during motif-to-network integration.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [other] Output formats include annotated node/edge TSV tables and GraphML network file.: "Output the annotated network table with node identifiers, edges, and attached MS2LDA substructure labels and chemical class information."
- [readme] Top parameter controls number of most shared motifs per molecular family shown in output.: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] Thresholds should be configured in MS2LDA web app first to ensure the summary table reflects these filters.: "The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. It is recommendable to do so when inspecting results in the web app."
- [readme] Cytoscape-based visualization with discrete mapping of motif labels to node colors and interaction types to edge stroke colors.: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose"

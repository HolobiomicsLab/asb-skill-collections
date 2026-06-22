---
name: molecular-network-node-annotation
description: Use when you have a GNPS-generated molecular network (classical or feature-based workflow) and corresponding MS2LDA LDA experiment results (Mass2Motif assignments and/or chemical class predictions), and you need to propagate those annotations to individual network nodes to support visual and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA
  - Cytoscape
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Network Node Annotation

## Summary

Integrate MS2LDA-derived Mass2Motif substructural annotations and chemical class labels onto nodes of GNPS mass spectral molecular networks using pyMolNetEnhancer or RMolNetEnhancer. This enriches network nodes with interpretable structural and chemical metadata to enable structure-driven network exploration and compound family characterization.

## When to use

You have a GNPS-generated molecular network (classical or feature-based workflow) and corresponding MS2LDA LDA experiment results (Mass2Motif assignments and/or chemical class predictions), and you need to propagate those annotations to individual network nodes to support visual and computational interpretation of the network by molecular family and substructural content.

## When NOT to use

- GNPS network has not been created or is in a non-standard format incompatible with pyMolNetEnhancer/RMolNetEnhancer input specifications.
- MS2LDA experiment has not been run on the corresponding MGF data, or motif/chemical class assignments are not available.
- You require node annotation solely from spectral library matches or in silico prediction tools other than MS2LDA (use alternative network annotation workflows in that case).

## Inputs

- GNPS molecular network edge table (GraphML or GML format)
- GNPS job ID (or GNPS clustered MGF file)
- MS2LDA experiment job ID (or manually downloaded MS2LDA summary table)

## Outputs

- Annotated molecular network (GraphML/GML) with motif and chemical class node attributes
- Node attribute table (TSV) with Mass2Motif assignments and chemical class labels
- Edge table (TSV) with shared motif interaction annotations
- Top shared motifs per molecular family (network component index)

## How to apply

Obtain your GNPS job ID and MS2LDA job ID (or manually download the MS2LDA summary file from ms2lda.org to avoid server timeouts). Load the GNPS edge table and MS2LDA motif assignments into pyMolNetEnhancer or RMolNetEnhancer. Apply user-defined thresholds: set a minimal probability score (default 0.01) and overlap score (default 0.3) to filter motif-document relations; these should ideally match thresholds set in the MS2LDA web app. Specify the `top` parameter (default 5) to select the N most-shared motifs per molecular family (network component index). Execute the appropriate mapping function (classical or feature-based) to merge motif and chemical class assignments into unified node attributes. Export as GraphML for Cytoscape visualization or as TSV for external table-based analysis.

## Related tools

- **pyMolNetEnhancer** (Python module that maps MS2LDA substructural motifs and chemical class information to GNPS network nodes and edges) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package implementing the same molecular network node annotation functionality as pyMolNetEnhancer) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Web platform that creates classical and feature-based mass spectral molecular networks; output edge tables and network files serve as input to pyMolNetEnhancer/RMolNetEnhancer) — https://gnps.ucsd.edu/
- **MS2LDA** (Latent Dirichlet Allocation tool that discovers and assigns Mass2Motif substructural patterns; outputs motif-document probability and overlap tables consumed by annotation workflow) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis platform; imports annotated GraphML files and supports discrete mapping of node/edge attributes (e.g., motif colors, chemical class labels)) — https://cytoscape.org/

## Evaluation signals

- Node attribute table contains non-null Mass2Motif assignments for nodes passing the specified probability (default ≥0.01) and overlap (default ≥0.3) thresholds.
- Chemical class labels are present in node attributes when chemical class information was integrated; verify that all network nodes are classified or marked as unassigned.
- Exported GraphML file opens without errors in Cytoscape and displays node/edge attributes correctly after import.
- TopSharedMotifs column in edge output reflects at most N motifs per molecular family (where N = `top` parameter, default 5), confirming correct ranking and filtering.
- Motif-to-node mapping is bidirectional and consistent: motifs listed in node attributes correspond to edges/interactions in the edge output table.

## Limitations

- Server connection timeout may occur when fetching large MS2LDA summary files directly; manual download from ms2lda.org is recommended as an alternative.
- Probability and overlap thresholds applied during pyMolNetEnhancer/RMolNetEnhancer execution should ideally match thresholds set in the MS2LDA web app Experimental Options tab; misalignment may result in inconsistent motif filtering between web and local analyses.
- The module operates only on already-networked nodes; nodes not present in the GNPS edge table or lacking MS2LDA assignments will not receive annotations.
- Feature-based workflow requires MGF file generated by MZmine (or equivalent) during GNPS feature-based molecular networking; classical workflow uses MGF downloaded directly from GNPS.

## Evidence

- [readme] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the [Global Natural Products Social Molecular"
- [readme] Probability and overlap threshold setting and rationale: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] Thresholds should match MS2LDA web app settings for consistency: "Important: The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. It is recommendable to do so when inspecting results in the web app."
- [readme] TopSharedMotifs parameter controls motif ranking and output count: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] Server timeout risk and manual download alternative: "Note: Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] Output formats and visualization workflow: "To visualize results import the .graphml output file into [Cytoscape](https://cytoscape.org/). To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to"
- [readme] Mapping method for classical workflow: "In order to map substructural information to a mass spectral molecular network you need to: [Create a molecular network](https://ccms-ucsd.github.io/GNPSDocumentation/quickstart/) through the Global"

---
name: graph-based-feature-annotation
description: Use when you have a GNPS molecular network (in GML or GraphML format) and corresponding MS2LDA substructural feature assignments or chemical class predictions, and you want to systematically propagate these annotations to individual network nodes to enable feature-aware visualization and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA
  - Cytoscape
  techniques:
  - tandem-MS
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

# graph-based-feature-annotation

## Summary

Annotate nodes in mass spectral molecular networks with chemical class and MS2LDA substructural feature assignments by integrating external feature metadata into network graph structures. This enriches molecular network visualization and interpretation by mapping discrete biochemical features to network topology.

## When to use

You have a GNPS molecular network (in GML or GraphML format) and corresponding MS2LDA substructural feature assignments or chemical class predictions, and you want to systematically propagate these annotations to individual network nodes to enable feature-aware visualization and comparative analysis.

## When NOT to use

- Your GNPS network is already in a non-standard format that cannot be parsed as GML or GraphML.
- You do not have corresponding MS2LDA or chemical class assignments for your network — the skill requires external feature metadata to annotate.
- Your analysis goal is de novo substructure discovery rather than annotation of known features onto existing networks.

## Inputs

- GNPS molecular network file (GML or GraphML format)
- MS2LDA job summary table (TSV or CSV exported from http://ms2lda.org/)
- GNPS job ID
- MS2LDA job ID
- Chemical class predictions (if available)

## Outputs

- Annotated molecular network file (GraphML format)
- Node attribute table with chemical class and MS2LDA motif annotations (CSV/TSV)
- Edge table with shared motif interaction metadata (TSV)
- Class-colored network suitable for Cytoscape visualization

## How to apply

Load the GNPS molecular network file and MS2LDA substructural feature summary table into pyMolNetEnhancer or RMolNetEnhancer. Apply probability and overlap thresholds (default prob≥0.01, overlap≥0.3) to filter motif-spectrum associations. Map MS2LDA features to nodes using either classical (clustering-based) or feature-based (ion-based) approaches depending on the GNPS workflow type. Simultaneously integrate chemical class information via the module's dedicated chemical class mapping functions. Merge all annotations into unified node attribute tables, then export as GraphML and CSV formats. The rationale is that threshold filtering prevents spurious low-confidence annotations, while dual-method support accommodates different GNPS workflow pipelines.

## Related tools

- **pyMolNetEnhancer** (Core module for integrating chemical class and MS2LDA substructural information into GNPS molecular networks via Python API) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing equivalent graph-based feature annotation workflows) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Platform for generating molecular networks (GML/GraphML output) from mass spectrometry data) — https://gnps.ucsd.edu/
- **MS2LDA** (Web service for generating substructural motif assignments (Mass2Motifs) from tandem MS spectra) — http://ms2lda.org/
- **Cytoscape** (Desktop tool for loading, visualizing, and interacting with annotated molecular network graphs) — https://cytoscape.org/

## Examples

```
import pyMolNetEnhancer; net = pyMolNetEnhancer.load_network('gnps_network.graphml'); motifs = pyMolNetEnhancer.map_ms2lda_classical(net, ms2lda_summary_file, prob=0.01, overlap=0.3, top=5); net_out = pyMolNetEnhancer.export_annotated_network(net, motifs, 'output_annotated.graphml')
```

## Evaluation signals

- All network nodes have non-null chemical class and/or MS2LDA motif attributes in the exported node attribute table.
- Edge interaction column correctly reflects shared motifs between connected nodes; verify by spot-checking 5–10 edges in Cytoscape against the edge TSV.
- Probability and overlap thresholds are applied consistently: no motif with prob < 0.01 or overlap < 0.3 appears in output unless explicitly overridden by user parameters.
- Network topology is preserved: node and edge counts in the output GraphML match the input GNPS network file.
- Cytoscape stroke color and node image/chart mappings render without errors and display distinct motif assignments across molecular families (network component indices).

## Limitations

- Server connection timeouts may occur when fetching large MS2LDA summary tables; manual download from http://ms2lda.org/ is recommended as a workaround.
- Probability and overlap thresholds are independent between the ms2lda.org web app and the local mapping module; users must ensure consistent threshold settings across platforms to avoid double-filtering.
- The 'top' parameter (default=5 most shared motifs per molecular family) may suppress lower-ranked but biologically relevant features; users should inspect the full output TSV rather than relying solely on network visualization.
- Feature-based mapping requires MZmine output from the GNPS feature-based molecular networking workflow; classical clustering-based networks follow a different input preparation protocol.

## Evidence

- [other] 1. Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer.: "Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer."
- [other] 2. Map chemical class information to network nodes using the module's chemical class integration functions.: "Map chemical class information to network nodes using the module's chemical class integration functions."
- [other] 3. Map MS2LDA substructural information to network nodes via both classical and feature-based approaches.: "Map MS2LDA substructural information to network nodes via both classical and feature-based approaches within pyMolNetEnhancer."
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column: "To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column"
- [readme] Alternatively, you may download the file manually at http://ms2lda.org/ Depending on the size of this file, a server connection timeout may occur.: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"

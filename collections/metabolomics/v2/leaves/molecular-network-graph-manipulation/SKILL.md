---
name: molecular-network-graph-manipulation
description: Use when you have a GNPS-generated classical or feature-based molecular
  network (in graphml or JSON format) and corresponding MS2LDA or chemical class assignment
  data, and you need to embed substructural motif identifiers, confidence scores,
  or chemical class labels as node/edge attributes for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0602
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS (Global Natural Products Social Molecular Networking)
  - ms2lda.org
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure
  information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer
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

# molecular-network-graph-manipulation

## Summary

Integrate MS2LDA-derived Mass2Motif substructural information and chemical class annotations into GNPS mass spectral molecular network graphs via node and edge attribute enrichment. This skill enables systematic mapping of structural motifs onto network topology, facilitating downstream visual and computational analysis of chemical relationships.

## When to use

Apply this skill when you have a GNPS-generated classical or feature-based molecular network (in graphml or JSON format) and corresponding MS2LDA or chemical class assignment data, and you need to embed substructural motif identifiers, confidence scores, or chemical class labels as node/edge attributes for network visualization or community-based chemical annotation.

## When NOT to use

- MS2LDA analysis has not been performed on the spectral data; the mapping step requires pre-computed motif assignments.
- Input is already a fully annotated network with motif and chemical class labels; re-running enrichment would redundantly overwrite existing attributes.
- The molecular network was created using a non-GNPS platform (e.g., custom Cytoscape or NetworkX graph); pyMolNetEnhancer and RMolNetEnhancer are designed specifically for GNPS-format networks.

## Inputs

- GNPS classical or feature-based molecular network file (graphml or JSON format)
- MS2LDA job ID or MS2LDA summary export table (TSV/CSV with motif-document assignments)
- Chemical class assignment table (optional, if mapping chemical class annotations)

## Outputs

- Annotated molecular network file (graphml or JSON) with motif metadata embedded in node attributes
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node attribute table with motif assignments and confidence scores)
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge interaction table with shared motif annotations)

## How to apply

Load the GNPS molecular network file and MS2LDA summary export (or chemical class table) into pyMolNetEnhancer or RMolNetEnhancer. Specify the GNPS job ID and MS2LDA job ID as required inputs. Set user-defined thresholds: prob (minimal probability score, default 0.01), overlap (minimal overlap score, default 0.3), and top (number of most-shared motifs per network component, default 5). The tool aligns MS2LDA motif identifiers to network nodes by matching precursor m/z and spectral similarity, then annotates nodes with motif IDs, confidence indicators, and chemical class labels. Export the enhanced network as a .graphml or JSON file with embedded motif metadata in node/edge attributes, and optionally generate separate .tsv files for nodes and edges to support downstream visualization in Cytoscape or other network analysis platforms.

## Related tools

- **pyMolNetEnhancer** (Primary Python module for integrating MS2LDA substructural and chemical class information into GNPS mass spectral molecular networks; performs node/edge attribute mapping and export.) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package with identical functionality to pyMolNetEnhancer for integrating substructural and chemical class information into GNPS networks.) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS (Global Natural Products Social Molecular Networking)** (Provides the classical and feature-based molecular network generation and outputs the graphml/JSON network files that serve as input to the enrichment workflow.) — https://gnps.ucsd.edu/
- **ms2lda.org** (Generates MS2LDA experiments and Mass2Motif assignments from clustered MGF spectra; outputs summary tables consumed by pyMolNetEnhancer/RMolNetEnhancer.) — http://ms2lda.org/
- **Cytoscape** (Network visualization platform for importing and rendering the enriched .graphml files, enabling color-coding of nodes and edges by motif and chemical class.) — https://cytoscape.org/

## Examples

```
# After installing pyMolNetEnhancer: pip install pyMolNetEnhancer
# Then in Python: from pyMolNetEnhancer import classical_network_motif_mapping; classical_network_motif_mapping(gnps_job_id='GNPS_JOB_ID', ms2lda_job_id='MS2LDA_JOB_ID', prob=0.01, overlap=0.3, top=5)
```

## Evaluation signals

- All nodes in the enriched network file possess motif ID attributes with non-null values; check the node attribute table (.tsv) for presence and cardinality of motif assignments.
- Probability and overlap scores for all mapped motifs meet or exceed user-specified thresholds (prob ≥ 0.01, overlap ≥ 0.3 by default); verify in node/edge .tsv output.
- Shared motif identifiers appear in edge attributes ('interact' column in .tsv), and each edge links only nodes that share at least one motif above the threshold.
- The 'TopSharedMotifs' attribute per network component (molecular family) contains ≤ top parameter value (default 5) motifs, sorted by frequency.
- The enriched .graphml file opens without errors in Cytoscape and nodes/edges can be colored using the embedded motif metadata attributes without manual data re-import.

## Limitations

- Server connection timeouts may occur when fetching large MS2LDA summary files via the API; manual download from ms2lda.org is recommended as an alternative.
- Mapping accuracy depends on the alignment of precursor m/z and spectral similarity between GNPS clusters and MS2LDA documents; mismatches due to data preprocessing differences may result in incomplete motif assignment.
- The probability and overlap filtering thresholds (prob, overlap) must be consistent with those applied in the ms2lda.org web interface to ensure the summary table contains the intended motif-document relations.
- No changelog is available in the repository, limiting visibility into version-specific changes or breaking updates.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [other] Load the GNPS-generated classical molecular network file (graphml or JSON format) and MS2LDA Mass2Motif output data containing substructural motif assignments: "Load the GNPS-generated classical molecular network file (graphml or JSON format) and MS2LDA Mass2Motif output data"
- [other] Use pyMolNetEnhancer's classical-mode mapping function to align MS2LDA motif identifiers to corresponding nodes in the molecular network based on precursor m/z and spectral similarity: "align MS2LDA motif identifiers to corresponding nodes in the molecular network based on precursor m/z and spectral similarity"
- [other] Export the enhanced network as an annotated molecular network file (graphml or JSON) with motif metadata embedded in node attributes: "Export the enhanced network as an annotated molecular network file (graphml or JSON) with motif metadata embedded in node attributes"
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how"
- [readme] Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes"

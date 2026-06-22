---
name: graph-enrichment-operations
description: Use when you have a GNPS mass spectral molecular network and wish to annotate its nodes with both chemical class assignments (from GNPS public library matches) and MS2LDA-derived substructural motifs (from classical or feature-based LDA experiments) in a single integrated operation, typically for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3047
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

# graph-enrichment-operations

## Summary

Integrates multiple layers of chemical annotations (class information and MS2LDA substructural motifs) onto mass spectral molecular network graphs via pyMolNetEnhancer or RMolNetEnhancer, enabling joint visualization and analysis of both chemical and structural features on network nodes and edges.

## When to use

You have a GNPS mass spectral molecular network and wish to annotate its nodes with both chemical class assignments (from GNPS public library matches) and MS2LDA-derived substructural motifs (from classical or feature-based LDA experiments) in a single integrated operation, typically for metabolite discovery or natural products characterization workflows where chemical family context and fragmentation patterns both inform interpretation.

## When NOT to use

- You do not have both a completed GNPS molecular network and a corresponding MS2LDA experiment; missing either input makes joint enrichment impossible.
- Your MS2LDA experiment has not been run or exported as a summary table (server timeout occurred and manual download was not performed).
- You require only chemical class annotation without substructural motif information, or vice versa; single-layer enrichment does not require this skill.

## Inputs

- GNPS job ID (identifier for completed molecular network)
- MS2LDA job ID (identifier for completed LDA experiment)
- Clustered MGF spectra (for classical approach) or MZmine-generated MGF file (for feature-based approach)
- GNPS public library match data (chemical class annotations)

## Outputs

- .graphml annotated network file with integrated chemical class and MS2LDA motif node/edge attributes
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge table with interaction annotations)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node table with TopSharedMotifs)
- ChemicalClasses_Nodes.tsv (chemical class per node, if applicable)

## How to apply

Obtain a GNPS job ID from a completed molecular network task and an MS2LDA job ID from a corresponding LDA experiment run on the clustered or feature-based MGF spectra. Load both datasets into pyMolNetEnhancer (Python) or RMolNetEnhancer (R) and select your mapping strategy: classical (for clustered spectra) or feature-based (for MZmine-derived features). Set filtering thresholds for motif inclusion (prob: minimum probability score, default 0.01; overlap: minimum overlap score, default 0.3; top: number of most-shared motifs per molecular family, default 5). Execute the integration workflow, which maps chemical classes to nodes via GNPS library matches and MS2LDA motifs to nodes using the selected approach, then merges both annotation layers onto the network graph. Export the result as a .graphml file (or separate TSV edge/node tables) for visualization in Cytoscape, where edges can be colored by shared motifs and nodes by top motifs per component.

## Related tools

- **pyMolNetEnhancer** (Primary Python module for integrating chemical class and MS2LDA motif annotations onto GNPS molecular networks) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package for performing the same graph enrichment operations as pyMolNetEnhancer) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Source platform for mass spectral molecular networks and public library chemical class matches) — https://gnps.ucsd.edu/
- **MS2LDA** (Source platform for MS2 fragmentation pattern-based LDA topic modeling and substructural motif discovery) — http://ms2lda.org/
- **Cytoscape** (Visualization software for importing and rendering the enriched .graphml network with colored edges and nodes) — https://cytoscape.org/

## Evaluation signals

- The exported .graphml file contains node attributes for both chemical classes and MS2LDA motifs; inspect the graph XML to confirm both annotation keys are present.
- TSV node output files (Mass2Motifs_Nodes_*.tsv and ChemicalClasses_Nodes.tsv) each contain rows matching the number of network nodes, with no null values in key annotation columns.
- When imported into Cytoscape, edges are colorable by the 'interact' column (shared motif annotations) and nodes by 'TopSharedMotifs' column without missing values.
- Probability and overlap thresholds applied during mapping match the specified parameters (prob, overlap); verify in output summary or log that threshold filtering was applied correctly.
- Manual inspection of a sample network component confirms that nodes belonging to the same molecular family share consistent TopSharedMotifs entries, indicating correct motif aggregation.

## Limitations

- MS2LDA server connection timeouts may occur on large files; manual download from ms2lda.org is a required fallback.
- Chemical class annotations depend on matches to the GNPS public library, which may not cover novel or rare metabolites, resulting in sparse chemical class coverage.
- The quality of substructural motifs is contingent on the quality and size of the LDA training data; small or low-quality MS2 datasets yield uninformative motifs.
- No changelog is currently available for either pyMolNetEnhancer or RMolNetEnhancer, limiting reproducibility across package versions.
- Probability and overlap threshold settings in the ms2lda.org web interface must be manually coordinated with thresholds set during mapping; mismatch between settings and output filtering can cause inconsistencies.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [intro] Map chemical class and MS2LDA substructural information to mass spectral molecular networks: "Map chemical class and MS2LDA substructural information to mass spectral molecular networks"
- [readme] The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab; the summary table contains filtered motif-document relations using the set thresholds in the web app.: "The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. Importantly, the summary table contains filtered motif-document relations using"
- [readme] To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs between nodes select 'Stroke Color' in the 'Edge' tab"
- [readme] This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5.: "This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"

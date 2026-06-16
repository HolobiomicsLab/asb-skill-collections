# Evaluation Strategy

## Direct Checks

- verify file exists at github:kopeckylukas__py-mamsi containing NetworkX graph construction code for structural clusters
- script_runs: execute the structural cluster-to-network conversion step from py-mamsi package on sample data from kopeckylukas/py-mamsi-tutorials repository
- file_format_is: output NetworkX object is serializable as .graphml or .gexf format (or equivalent NetworkX-native pickle)
- file_format_is: output pyvis HTML artifact is valid HTML5 with .html extension and contains interactive graph visualization
- field_present: NetworkX graph object contains node attributes capturing structural cluster identity and m/z/RT properties
- field_present: pyvis HTML output contains interactive elements (zoom, pan, node-drag functionality) — robust to parameter choices in visualization layout
- output_matches_reference: graph node count and edge count match documented example in py-mamsi-tutorials or README, allowing multiple defensible graph layouts

## Expert Review

- biochemical validity: verify that structural relationships encoded in graph edges (isotopologue, adduct, cross-assay links) correctly reflect the m/z and RT clustering logic described in methods
- usability assessment: confirm that resulting NetworkX object is compatible with downstream tools (Cytoscape, networkx library functions) as stated in documentation

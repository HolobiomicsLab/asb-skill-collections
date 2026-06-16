# Evaluation Strategy

## Direct Checks

- verify file network.graphml exists in expected outputs or repository
- file_format_is network.graphml: verify XML structure conforms to GraphML schema (http://graphml.graphdrawing.org/)
- field_present: verify 'node' elements exist with 'id' attribute
- field_present: verify 'data' child elements within nodes include motif-membership attributes
- field_present: verify 'edge' elements exist with 'source' and 'target' attributes
- field_present: verify 'data' child elements within edges encode spectral similarity weights or scores
- script_runs: verify the postprocessing script executes without error when provided valid ARTIFACT-MOTIFSET and optional ARTIFACT-LDA-MODEL inputs
- output_matches_reference: node count and edge count are consistent with input motif set cardinality (no canonical answer — depends on spectral similarity threshold and motif clustering parameters)
- verify network.graphml can be parsed by a standard GraphML reader (robust to GraphML schema version, parameter-sensitive to node/edge attribute names)

## Expert Review

- Verify that spectral similarity edge weights are computed using an appropriate metric (e.g., cosine similarity, Euclidean distance) and that the choice of metric is documented
- Verify that motif-membership node attributes correctly encode the assignment of spectra or fragments to discovered motifs from the LDA model
- Verify that the graph structure meaningfully represents the relationships between motifs or spectra based on spectral similarity and shared motif membership
- Assess whether the GraphML serialisation preserves all relevant metadata (motif identifiers, similarity thresholds, LDA model hyperparameters) needed for downstream analysis or visualization

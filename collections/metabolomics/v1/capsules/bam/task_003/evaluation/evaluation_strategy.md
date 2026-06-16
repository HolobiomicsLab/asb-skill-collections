# Evaluation Strategy

## Direct Checks

- verify that inputs include at least one concrete artifact: either a file from the BAM package (github:HassounLab__BAM), a deposited dataset with public accession, or task output from a preceding biotransformation-rules sub-task
- verify file_exists for the molecular network output file (expected format: .graphml, .gexf, or .net)
- verify file_exists for the annotation table output (expected format: .csv, .tsv, or .xlsx)
- verify that the annotation table contains at least the following fields: node_id, compound_name, mass, or equivalent identifiers — exact field names may vary; no canonical answer
- verify that the molecular network file is valid and parseable in its declared format (robust to node/edge count variation)
- verify row_count_equals or row_count_is_greater_than for the annotation table (at least 1 data row beyond headers)
- verify that molecular network nodes correspond to entries in the annotation table — at least one mapping present

## Expert Review

- assess whether the global molecular networking component executed without errors or warnings and completed the full network assembly pipeline
- assess the chemical plausibility and coherence of node connectivity in the molecular network (whether edges reflect realistic biotransformation or spectral similarity relationships)
- assess whether annotation table entries show reasonable mass-to-charge and structural relationships consistent with untargeted metabolomics data
- assess whether the network structure and annotations reflect integration of the candidate transformed structures from the preceding biotransformation-rules module

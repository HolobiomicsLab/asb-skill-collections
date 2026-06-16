# Evaluation Strategy

## Direct Checks

- verify that the enpkg_full repository (github:enpkg__enpkg_full) is accessible and contains executable workflow code
- verify file_exists for a test or example dataset directory within the repository
- script_runs: execute the ENPKG full workflow against the provided example/test dataset without errors
- file_exists: verify that expected annotated output files are generated in the designated output directory after workflow completion
- file_format_is: verify that output files conform to knowledge-graph-ready formats (e.g., GraphML, JSON, TSV, or other structured formats documented in the repository)
- output_matches_reference: compare generated outputs against reference outputs (if provided in the repository) byte-for-byte or robust to minor formatting variations depending on output specification

## Expert Review

- evaluate whether the generated knowledge graph outputs are scientifically coherent and contain expected natural products annotations (structures, metadata, relationships)
- assess whether the workflow execution demonstrates successful integration of all stated pipeline components (sample annotation, chemical annotation, network inference)

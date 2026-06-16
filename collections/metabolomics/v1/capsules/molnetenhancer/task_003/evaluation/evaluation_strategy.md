# Evaluation Strategy

## Direct Checks

- verify file exists: pyMolNetEnhancer package accessible from github:madeleineernst__pyMolNetEnhancer
- script_runs: pyMolNetEnhancer chemical class mapping function executes on a GNPS network JSON or GraphML input file without raising exceptions
- file_format_is: output annotated network file is valid GraphML or JSON format (robust to GraphML/JSON variant specifications)
- file_exists: output file contains at least one node with chemical class attribute added relative to input network
- field_present: output network nodes include chemical class label field(s)
- contains_substring: output network artifact contains evidence of class-to-node mapping (e.g., class field values populated, not null or empty)

## Expert Review

- chemical class assignments are biochemically sensible for the compound nodes in the test network
- chemical class mapping preserves the original GNPS molecular network structure and edge connectivity
- annotation coverage and accuracy of chemical class assignments match expectations for the input dataset

# Evaluation Strategy

## Direct Checks

- verify that the BAM codebase (github:HassounLab__BAM) contains a biotransformation rules module or file
- verify that the module accepts molecular structures in SMILES format as input
- verify that the module produces a structured output file (CSV, JSON, or TSV format) containing transformed structures
- script_runs: execute the biotransformation rule-application function on a test set of 5–10 SMILES strings and confirm no runtime errors occur
- verify that output file contains at least one column for input SMILES and at least one column for output/transformed SMILES
- verify output_matches_reference: compare a sample of rule-applied transformations against documented biotransformation rules in the repository documentation or codebase comments (if available)

## Expert Review

- assess whether the biotransformation rules applied are chemically and metabolically plausible for the input structures tested
- assess whether the transformed structures follow valid chemical valence and bonding rules
- assess whether the rule-application logic correctly encodes the intended biotransformation pathways (e.g., oxidation, conjugation, phase I/II metabolism)

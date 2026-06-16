# Evaluation Strategy

## Direct Checks

- verify file exists: ComputeConverter subclass implementation in MSMetaEnhancer repository (e.g., rdkit_converter.py or equivalent)
- verify file_format_is: implementation file contains valid Python syntax, parseable by AST or direct import
- verify script_runs: `python -c 'from msmetaenhancer.converters import ComputeConverter; assert hasattr(ComputeConverter, "convert")'` executes without error
- verify script_runs: test suite for ComputeConverter subclass executes via pytest on local repository
- verify output_matches_reference: for at least 3 reference SMILES strings (e.g., 'CCO', 'c1ccccc1', 'CC(=O)O'), the subclass output matches expected InChI or molecular formula strings (exact or robust to canonicalization), no canonical answer — multiple SMILES representations may convert to same InChI
- verify field_present: ComputeConverter subclass implements at least one method signature matching base-class contract (e.g., `convert(self, query: str, representation: str) -> str`)
- verify contains_substring: implementation documentation or docstring describes which chemical structure conversions are supported (e.g., 'SMILES to InChI', 'SMILES to molecular formula')

## Expert Review

- Confirm that the ComputeConverter subclass correctly uses RDKit APIs (Chem.MolFromSmiles, Chem.MolToInchi, Chem.rdMolDescriptors) for local structure conversion and does not fall back to web services
- Validate that the reference SMILES test set covers chemically diverse structures (e.g., aliphatic, aromatic, functional groups) and are correctly converted to intended representations
- Assess whether error handling for invalid SMILES or unsupported conversions is documented and tested (e.g., return of None, exception, or logged warning)

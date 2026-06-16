# SciTask Card: Reconstruct the RDKit-based ComputeConverter template for local chemical property computation

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:39:21.024441+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_msmetaenhancer/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- GitHub: `RECETOX/MSMetaEnhancer`
- Quality: Score 2/5 — Coherent: false, placeholder, 8 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `cheminformatics`
- Subdomains: `computational-metabolomics`
- Techniques: `database-annotation`, `metabolite-identification`

## Research Question
How does a ComputeConverter subclass using RDKit perform local chemical structure conversions (e.g., SMILES to InChI) without relying on web services?

## Connected Finding
MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses that perform local chemical structure conversions.

## Task Description
Implement a ComputeConverter subclass using RDKit to perform local chemical structure conversions (e.g., SMILES to InChI or molecular formula) following the ComputeConverter base-class contract, and verify correct output for a set of reference SMILES strings.

## Inputs
- RDKit library installation and MSMetaEnhancer package source code with ComputeConverter base class
- Reference SMILES strings for validation testing

## Expected Outputs
- ComputeConverter subclass Python module (e.g., MyComputeService.py) with at least one functional conversion method
- pytest test file (test_MyComputeService.py) demonstrating converter availability and conversion accuracy
- Updated __init__.py in MSMetaEnhancer/libs/converters/compute/ registering the new converter
- Test execution report showing all tests passing (pytest output)

## Expected Output File

- `MyComputeService.py`

## Landmark Outputs

- `MSMetaEnhancer/libs/converters/compute/MyComputeService.py`
- `tests/test_MyComputeService.py`
- `MSMetaEnhancer/libs/converters/compute/__init__.py`
- `pytest_output.log`

## Tools
- MSMetaEnhancer
- RDKit
- pytest
- Python

## Skills
- chemical-structure-representation-conversion
- rdkit-molecular-descriptor-computation
- compute-converter-interface-implementation
- python-async-method-definition
- unit-test-design-for-cheminformatics
- smiles-inchi-round-trip-validation

## Workflow Description
1. Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter. 2. Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods with asynch=False. 3. Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi). 4. Return converted data as a dictionary with target attribute keys. 5. Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__. 6. Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness. 7. Run pytest to confirm existing tests still pass and new converter tests execute successfully.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/scheme.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No specific documentation or code examples are provided for the ComputeConverter base-class contract, expected method signatures, or input/output formats.
- No reference SMILES strings or expected conversion outputs are provided in the article or discussion section for validation of local chemical structure conversions.
- No explicit statement of which chemical structure conversions (SMILES → InChI, SMILES → molecular formula, etc.) should be prioritized or are required for a minimal ComputeConverter subclass implementation.

## Domain Knowledge
- ComputeConverters perform local computations without external API calls, inheriting from the ComputeConverter base class and calling create_top_level_conversion_methods with asynch=False to generate synchronous dynamic methods.
- RDKit is a cheminformatics toolkit that converts molecular representations in-memory; common conversions include SMILES parsing (Chem.MolFromSmiles), InChI generation (Chem.inchi.MolToInchi), and molecular formula derivation (Chem.rdMolDescriptors.CalcMolFormula).
- Converter registration in __init__.py is required for the ConverterBuilder to auto-discover and instantiate converters, making them available to the annotation pipeline.
- Conversion methods must return a dictionary with target attribute names as keys to satisfy the dynamic method contract and integrate with the Job system (source_attribute, target_attribute, converter_name tuples).
- Error handling must gracefully return empty dictionaries when input parsing fails, following the pattern of web converters for consistent behavior across API and compute services.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pytest, ComputeConverter subclass Python module (e.g., MyComputeService.py) with at least one functional conversion method, pytest test file (test_MyComputeService.py) demonstrating converter availability and conversion accuracy, Updated __init__.py in MSMetaEnhancer/libs/converters/compute/ registering the new converter, Test execution report showing all tests passing (pytest output).

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does a ComputeConverter subclass using RDKit perform local chemical structure conversions (e.g., SMILES to InChI) without relying on web services?: 'Use the RDKit converter as a reference implementation'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses that perform local chemical structure conversions.: 'Use the RDKit converter as a reference implementation'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] RDKit library installation and MSMetaEnhancer package source code with ComputeConverter base class: 'Use the RDKit converter as a reference implementation'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Reference SMILES strings for validation testing: 'Test the conversion functionality'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] ComputeConverter subclass Python module (e.g., MyComputeService.py) with at least one functional conversion method: 'Create a new Python file in `MSMetaEnhancer/libs/converters/compute/` named after your service'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] pytest test file (test_MyComputeService.py) demonstrating converter availability and conversion accuracy: 'Create a test file `tests/test_MyService.py`'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Updated __init__.py in MSMetaEnhancer/libs/converters/compute/ registering the new converter: 'Add your new converter to `MSMetaEnhancer/libs/converters/compute/__init__.py`'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Test execution report showing all tests passing (pytest output): 'make sure the existing tests still work by running ``pytest``'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] RDKit: 'Use the RDKit converter as a reference implementation'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] pytest: 'make sure the existing tests still work by running ``pytest``'
- `ev_011` from `agent2_synthesis` (agent2_traced): [intro] Python: 'A Python package for mass spectra metadata annotation'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No specific documentation or code examples are provided for the ComputeConverter base-class contract, expected method signatures, or input/output formats.: 'The discussion section does not describe ComputeConverter base-class API or contract requirements.'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No reference SMILES strings or expected conversion outputs are provided in the article or discussion section for validation of local chemical structure conversions.: 'The discussion mentions 'CIR: Inchi -> SMILES conversion' and 'support `ISOMERIC_SMILES` and `CANONICAL_SMILES` in PubChem' but does not provide test data.'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No explicit statement of which chemical structure conversions (SMILES → InChI, SMILES → molecular formula, etc.) should be prioritized or are required for a minimal ComputeConverter subclass implementation.: 'The discussion lists conversion types (e.g., 'Inchi -> SMILES', 'ISOMERIC_SMILES', 'CANONICAL_SMILES') but does not specify a required set for the ComputeConverter implementation.'

## Evaluation Strategy
### Direct Checks
- verify file exists: ComputeConverter subclass implementation in MSMetaEnhancer repository (e.g., rdkit_converter.py or equivalent)
- verify file_format_is: implementation file contains valid Python syntax, parseable by AST or direct import
- verify script_runs: `python -c 'from msmetaenhancer.converters import ComputeConverter; assert hasattr(ComputeConverter, "convert")'` executes without error
- verify script_runs: test suite for ComputeConverter subclass executes via pytest on local repository
- verify output_matches_reference: for at least 3 reference SMILES strings (e.g., 'CCO', 'c1ccccc1', 'CC(=O)O'), the subclass output matches expected InChI or molecular formula strings (exact or robust to canonicalization), no canonical answer — multiple SMILES representations may convert to same InChI
- verify field_present: ComputeConverter subclass implements at least one method signature matching base-class contract (e.g., `convert(self, query: str, representation: str) -> str`)
- verify contains_substring: implementation documentation or docstring describes which chemical structure conversions are supported (e.g., 'SMILES to InChI', 'SMILES to molecular formula')

### Expert Review
- Confirm that the ComputeConverter subclass correctly uses RDKit APIs (Chem.MolFromSmiles, Chem.MolToInchi, Chem.rdMolDescriptors) for local structure conversion and does not fall back to web services
- Validate that the reference SMILES test set covers chemically diverse structures (e.g., aliphatic, aromatic, functional groups) and are correctly converted to intended representations
- Assess whether error handling for invalid SMILES or unsupported conversions is documented and tested (e.g., return of None, exception, or logged warning)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Create a new ComputeConverter subclass file in the compute converters directory.
2. Define conversions list (source → target mappings) and invoke create_top_level_conversion_methods with asynch=False.
3. Implement RDKit-based conversion methods (e.g., SMILES to InChI via Chem.MolFromSmiles and Chem.inchi.MolToInchi).
4. Return results as dictionaries mapping target attribute names to converted values.
5. Register the converter in __init__.py for auto-discovery.
6. Write pytest tests validating converter instantiation and conversion accuracy on reference SMILES inputs.
7. Validation: all pytest tests pass, including new converter tests and existing test suite, confirming correct implementation of ComputeConverter interface and accurate molecular structure conversions.

## Workflow Ports

**Inputs:**

- `rdkit_lib` — RDKit library installation
- `compute_converter_base` — ComputeConverter base class
- `reference_smiles` — Reference SMILES strings for validation

**Outputs:**

- `compute_converter_module` — ComputeConverter subclass implementation
- `test_module` — pytest test file for converter validation
- `updated_init` — Updated __init__.py with converter registration
- `test_report` — pytest execution report (passing tests)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:RECETOX__MSMetaEnhancer`
- **Synthesized at:** 2026-06-16T05:45:57+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (8):
  - research_question: evidence_span not found in section 'intro' (value='How does a ComputeConverter subclass using RDKit perform loc', span='Use the RDKit converter as a reference implementation')
  - missing_information[0]: evidence_span not found in section 'discussion' (value='No specific documentation or code examples are provided for ', span='The discussion section does not describe ComputeConverter ba')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='No reference SMILES strings or expected conversion outputs a', span='The discussion mentions 'CIR: Inchi -> SMILES conversion' an')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='No explicit statement of which chemical structure conversion', span='The discussion lists conversion types (e.g., 'Inchi -> SMILE')
  - research_question and finding semantic mismatch: RQ asks 'How does...' (mechanism) but finding only asserts 'MSMetaEnhancer uses RDKit as reference' (existence claim, not mechanism explanation)
  - finding evidence_span identical to research_question but section is 'other' instead of article section; unclear source document
  - inputs[1] uses placeholder 'Reference SMILES strings' without naming concrete test compounds
  - expected_outputs use placeholder filenames 'MyComputeService.py' and 'test_MyService.py' that are templates, not article-specific artifacts
- Notes: This task card exhibits severe quality issues: (1) Groundedness failure on all major claims—evidence spans are either not found in cited sections or reused verbatim across multiple claims without specificity. (2) Semantic incoherence—research question asks a mechanism question ('How does...perform...') but the finding provides only a design statement ('X uses Y'). (3) Placeholder pollution—inputs and outputs use generic template names ('MyComputeService.py', 'Reference SMILES strings') rather than concrete article-specific references. (4) Detached from source—no source document, DOI, section content, or verifiable reference provided; all evidence_spans point to a single generic sentence. (5) Domain knowledge appears sound (RDKit API, ComputeConverter pattern) but assertions lack grounding in actual article text. Recommend: (A) Provide actual article title, section content, and evidence spans extracted via substring-match from real document; (B) Rewrite research_question and finding to match (either both mechanism questions or both existence claims); (C) Replace placeholder artifact names and SMILES references with concrete examples from the article or a canonical test set; (D) Verify 'MSMetaEnhancer' and 'ComputeConverter' against actual project documentation.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

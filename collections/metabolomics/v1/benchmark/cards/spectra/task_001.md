# SciTask Card: Implement the MsBackend virtual class API for a new in-memory backend (MsBackendTest)

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:59:54.721704+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectra/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- GitHub: `rformassspectrometry/Spectra`
- Quality: Score 2/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`

## Research Question
What are the required method signatures and implementations needed to create a complete MsBackendTest class that extends MsBackend and provides full read-write access to mass spectrometry spectral data?

## Connected Finding
MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) plus 7 data replacement methods ($<-, spectraData<-, intensity<-, mz<-, peaksData<-, selectSpectraVariables, dataStorage<-, spectraNames<-) with specific signatures. The class uses three slots: spectraVars (data.frame), mz (NumericList), and intensity (NumericList), where each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data.

## Task Description
Implement a complete MsBackendTest class extending the virtual MsBackend class with all required accessor and data-replacement methods to enable creation of custom MS data backends compatible with the Spectra infrastructure.

## Inputs
- MsBackend virtual class API specification and documentation

## Expected Outputs
- R source file containing complete MsBackendTest class implementation with all required methods

## Expected Output File

- `MsBackendTest.R`

## Landmark Outputs

- `MsBackendTest_class_skeleton.R`
- `MsBackendTest_accessors.R`
- `MsBackendTest_replacement_methods.R`
- `MsBackendTest_complete.R`

## Tools
- Spectra
- S4Vectors
- R

## Skills
- s4-class-definition-and-inheritance
- backend-api-method-implementation
- mass-spectrometry-data-representation
- peak-data-extraction-and-formatting
- dataframe-and-numericlist-manipulation
- spectrum-subsetting-and-merging

## Workflow Description
1. Define an S4 class MsBackendTest extending MsBackend with slots for spectraVars (data.frame), mz (NumericList), and intensity (NumericList). 2. Implement spectraData() method returning full spectra data as a DataFrame object combining all variables. 3. Implement spectraVariables() method returning a character vector of all available variable names. 4. Implement backendInitialize() method to initialize and load MS data into the backend instance. 5. Implement peaksData() method extracting m/z and intensity values as a list of matrices. 6. Implement extractByIndex() and [ methods to subset the backend by selected spectrum indices. 7. Implement backendMerge() method combining multiple MsBackendTest instances. 8. Implement intensity() and mz() accessor methods returning NumericList objects for peak values. 9. Implement spectraNames() method to extract optional spectrum names or identifiers. 10. Implement data replacement methods (intensity<-, mz<-, spectraData<-) for modifying backend data.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/apple-touch-icon-120x120.png` | figure | False |
| `figures/apple-touch-icon-152x152.png` | figure | False |
| `figures/apple-touch-icon-180x180.png` | figure | False |
| `figures/apple-touch-icon-60x60.png` | figure | False |
| `figures/apple-touch-icon-76x76.png` | figure | False |
| `figures/apple-touch-icon.png` | figure | False |
| `figures/favicon-16x16.png` | figure | False |
| `figures/favicon-32x32.png` | figure | False |
| `figures/logo.png` | figure | False |
| `figures/plot-single-spectrum-basic.svg` | figure | False |
| `figures/plot-single-spectrum-labels-ass.svg` | figure | False |
| `figures/plot-single-spectrum-labels.svg` | figure | False |
| `figures/plot-single-spectrum-xlim.svg` | figure | False |
| `figures/plotmzdelta-1000.svg` | figure | False |
| `figures/plotspectra-asp05.svg` | figure | False |
| `figures/plotspectra-asp2.svg` | figure | False |
| `figures/plotspectra-color-each.svg` | figure | False |
| `figures/plotspectra-color-peaks-label-labelcol.svg` | figure | False |
| `figures/plotspectra-color-peaks-label.svg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog document available to verify version history or API changes to MsBackendTest class
- Specific implementation details of MsBackendTest class methods are not provided in the discussion section

## Domain Knowledge
- MsBackend is a virtual class defining the API contract that all custom MS data backends must implement to integrate with Spectra-based analysis workflows.
- m/z values within each spectrum must be sorted in increasing order, a constraint that must be maintained by all data replacement methods.
- dataStorage and dataOrigin are two special required variables that every backend must provide, specifying where data is stored and its origin.
- Peak data is represented internally as lists of matrices with m/z and intensity columns, extracted via peaksData() method.
- Read-only backends need only implement accessor methods (spectraData, peaksData, intensity, mz) and may omit data replacement methods entirely.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: S4Vectors, R source file containing complete MsBackendTest class implementation with all required methods.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] What are the required method signatures and implementations needed to create a complete MsBackendTest class that extends MsBackend and provides full read-write access to mass spectrometry spectral data?: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented. In the example below we create thus a simple class with a `data.frame` to contain general spectral'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) plus 7 data replacement methods ($<-, spectraData<-, intensity<-, mz<-, peaksData<-, selectSpectraVariables, dataStorage<-, spectraNames<-) with specific signatures. The class uses three slots: spectraVars (data.frame), mz (NumericList), and intensity (NumericList), where each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data.: 'The 3 slots `spectraVars`, `mz` and `intensity` will be used to store our MS data, each row in `spectraVars` being data for one spectrum with the columns being the different *spectra variables* (i.e.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] MsBackend virtual class API specification and documentation: 'The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] R source file containing complete MsBackendTest class implementation with all required methods: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Spectra: 'The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] S4Vectors: 'return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] R: 'library(Spectra)
library(IRanges)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog document available to verify version history or API changes to MsBackendTest class: '_No changelog found._'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] Specific implementation details of MsBackendTest class methods are not provided in the discussion section: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that MsBackendTest class definition file exists in github:rformassspectrometry__Spectra repository
- verify file_format_is R script or documentation file containing class definition
- verify that MsBackendTest extends MsBackend (check class inheritance declaration)
- verify field_present in MsBackendTest class definition for all required slots: spectraVars, mz, intensity
- verify that methods spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames are defined in or inherited by MsBackendTest
- verify script_runs: load MsBackendTest class definition and instantiate object without error
- verify that spectraData() method returns S4Vectors DataFrame object
- verify that spectraVariables() method returns character vector
- verify that peaksData() method returns list-like structure with m/z and intensity matrices
- verify that intensity() and mz() methods return NumericList objects

### Expert Review
- confirm that MsBackendTest implementation correctly satisfies the MsBackend virtual class contract for all required accessor methods
- confirm that data replacement method implementations (if present) are semantically correct for modifying spectra data
- confirm that backendMerge() correctly combines multiple MsBackendTest instances without data loss or corruption
- confirm that extractByIndex() correctly subsets backend while maintaining data integrity and proper indexing
- confirm that m/z values in peaksData output are sorted increasingly as required by specification

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Define S4 class MsBackendTest extending MsBackend with typed slots for spectraVars, mz, and intensity data
2. Implement core accessor methods (spectraData, spectraVariables, peaksData, intensity, mz, spectraNames) following DataFrame/NumericList conventions
3. Implement backend lifecycle methods (backendInitialize) and collection operations (extractByIndex, backendMerge, [)
4. Implement data replacement methods (intensity<-, mz<-, spectraData<-) ensuring m/z values remain sorted
5. Validation: class instantiation succeeds, all required methods execute without error, output types match API contract (DataFrame, NumericList, character vector)

## Workflow Ports

**Inputs:**

- `msbackend_api` — MsBackend virtual class API specification

**Outputs:**

- `backend_class` — MsBackendTest class implementation file

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:rformassspectrometry__Spectra`
- **Synthesized at:** 2026-06-16T06:07:35+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - research_question: evidence_span not found in section 'results' (value='What are the required method signatures and implementations ', span='To create a new backend a class extending the virtual `MsBac')
  - finding: evidence_span not found in section 'results' (value='MsBackendTest requires implementation of 9 required accessor', span='The 3 slots `spectraVars`, `mz` and `intensity` will be used')
  - finding: The 16 specific method names (9 accessors + 7 replacements) are inferred/synthesized, not explicitly grounded in the evidence_span which only mentions the 3 slots
  - research_question asks for 'required method signatures' but evidence_span provides no signature specifications
- Notes: This card shows significant groundedness and coherence problems. The research_question and finding are not properly anchored to the provided evidence spans—the spans don't match the claimed sections, and the specific technical claims (16 method names, exact slot structure) are inferred rather than directly quoted from source text. The research_question asks about 'method signatures' but the evidence only discusses data slots. The finding's assertion of 9 + 7 methods lacks numerical justification in the evidence. The task_description and workflow_description contain much more detail than either the question or finding, suggesting the card conflates synthesis with grounding. Generic language like 'a complete class' and 'full read-write access' reduces clarity. The card would benefit from: (1) correcting section citations and re-grounding with actual text excerpts, (2) either removing the specific method count claim or providing proper evidence, (3) refocusing the research_question on data representation and slot usage rather than method signatures, or (4) splitting into separate questions for different aspects. The expected_artifact_name field provides helpful concreteness, but the expected_outputs and landmark_outputs fields still lack file paths or concrete references.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

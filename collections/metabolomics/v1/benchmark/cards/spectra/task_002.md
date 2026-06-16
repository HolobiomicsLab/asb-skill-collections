# SciTask Card: Reproduce the fillCoreSpectraVariables() behavior for missing core spectra variables in spectraData()

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:59:54.721704+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_spectra/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- GitHub: `rformassspectrometry/Spectra`
- Quality: Score 2/5 — placeholder, 4 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Techniques: `feature-detection`, `spectral-library-matching`

## Research Question
Does the spectraData() method on a MsBackendTest instance correctly return all core spectra variables with NA values when only user-supplied spectra variables are stored in the backend?

## Connected Finding
The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored.

## Task Description
Implement and test a MsBackendTest class that correctly handles user-supplied spectra variables (msLevel, rtime) and uses fillCoreSpectraVariables() to populate missing core variables with NA values, verifying that spectraData() returns the complete set of core spectra variables.

## Inputs
- Spectra package documentation and API specification
- User-supplied spectra variables: msLevel and rtime values

## Expected Outputs
- MsBackendTest class definition extending MsBackend with implemented core methods
- DataFrame returned by spectraData() containing all core spectra variables with NA for missing user-supplied values

## Landmark Outputs

- `MsBackendTest_class_definition.R`
- `spectra_dataframe_output.csv`

## Tools
- Spectra
- S4Vectors
- R

## Skills
- ms-backend-api-implementation
- s4-class-definition-and-slot-management
- spectra-variable-core-population
- dataframe-construction-from-backend-sources
- missing-value-imputation-with-na

## Workflow Description
1. Create a MsBackendTest class extending the virtual MsBackend with slots for storing user-supplied spectra variables (msLevel, rtime) and peak data (mz, intensity). 2. Implement backendInitialize() method to initialize the backend instance with user-supplied data. 3. Implement spectraData() method to return spectra variables as a DataFrame, invoking fillCoreSpectraVariables() internally to populate missing core variables with NA values. 4. Implement spectraVariables() method to return names of all available spectra variables including both user-supplied and core variables. 5. Implement peaksData(), intensity(), mz(), and extractByIndex() accessor methods to support the backend API. 6. Call spectraData() on a MsBackendTest instance and verify that all core spectra variables (e.g., centroided, polarity) are present in the returned DataFrame with NA values for those not explicitly provided by the user.

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
- No changelog documenting changes to spectraData() method behavior or fillCoreSpectraVariables() implementation

## Domain Knowledge
- Core spectra variables are mandatory in any MsBackend implementation; dataStorage and dataOrigin are special required variables that define where spectrum data is stored and derived.
- The fillCoreSpectraVariables() function is a helper that must be invoked within spectraData() to ensure all core variables are present even when not explicitly provided by the user.
- The spectraData() method must return a DataFrame (from S4Vectors) as the standard container for structured spectra metadata across all MsBackend implementations.
- m/z values within each spectrum must be stored in sorted increasing order to comply with MS data standards.
- User-supplied variables (msLevel, rtime) are optional; all other core variables missing from user input should be populated with NA values rather than omitted.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: S4Vectors, MsBackendTest class definition extending MsBackend with implemented core methods, DataFrame returned by spectraData() containing all core spectra variables with NA for missing user-supplied values.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does the spectraData() method on a MsBackendTest instance correctly return all core spectra variables with NA values when only user-supplied spectra variables are stored in the backend?: 'The `DataFrame` **must** provide values (even if they are `NA`) for **all** requested spectra variables of the backend (**including** the core spectra variables).'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored.: 'To ensure that `spectraData()` always returns all required *core* spectra variables (of the correct data type) we can use however the `fillCoreSpectraVariables()` function. This function adds'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] Spectra package documentation and API specification: 'The `MsBackend` virtual class defines the API that new *backend* classes need to implement'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] User-supplied spectra variables: msLevel and rtime values: 'slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] MsBackendTest class definition extending MsBackend with implemented core methods: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] DataFrame returned by spectraData() containing all core spectra variables with NA for missing user-supplied values: 'The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Spectra: 'The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] S4Vectors: 'return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] R: 'library(Spectra)
library(IRanges)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting changes to spectraData() method behavior or fillCoreSpectraVariables() implementation: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that calling spectraData() on a MsBackendTest instance with only user-supplied spectra variables (msLevel, rtime) returns a DataFrame
- verify that the returned DataFrame contains all core spectra variables as columns
- verify that columns corresponding to missing core spectra variables (e.g., centroided, polarity) contain NA values
- verify that fillCoreSpectraVariables() is invoked during spectraData() execution by inspecting function call stack or code inspection

### Expert Review
- expert review of whether the set of core spectra variables returned matches the documented specification for core variables
- expert review of whether NA-filling behavior is appropriate and consistent with the MsBackend API contract

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Define a MsBackendTest class extending the virtual MsBackend with slots for user-supplied variables and peak data
2. Implement required accessor methods (spectraData, spectraVariables, peaksData, intensity, mz, extractByIndex) according to the MsBackend API
3. Invoke fillCoreSpectraVariables() within spectraData() to populate missing core spectra variables with NA
4. Return a DataFrame containing both user-supplied and filled core variables
5. Validation: verify that spectraData() output contains all expected core spectra variables and user-supplied variables are preserved with NA values for missing core columns

## Workflow Ports

**Inputs:**

- `spectra_api_spec` — Spectra package MsBackend API specification
- `user_variables` — User-supplied spectra variables (msLevel, rtime)

**Outputs:**

- `backend_class` — MsBackendTest class definition with implemented methods
- `spectra_dataframe` — DataFrame with all core spectra variables returned by spectraData()

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:rformassspectrometry__Spectra`
- **Synthesized at:** 2026-06-16T06:07:49+00:00

## Extraction Quality
- Score: 2/5
- Coherent: true
- Placeholder detected: true
- Groundedness failures (4):
  - research_question: evidence_span not found in section 'results' (value='Does the spectraData() method on a MsBackendTest instance co', span='The `DataFrame` **must** provide values (even if they are `N')
  - finding: evidence_span not found in section 'results' (value='The spectraData() implementation for MsBackendTest uses fill', span='To ensure that `spectraData()` always returns all required *')
  - research_question: evidence_span appears to be from 'intro' or 'methods' section, not 'results' as claimed
  - finding: evidence_span is truncated and incomplete ('This function adds' cuts off mid-sentence), indicating extraction error
- Notes: This card has significant groundedness issues preventing verification. The research_question and finding both cite evidence from wrong sections (intro/methods instead of results), and the finding's evidence_span is truncated mid-sentence. The card lacks specificity throughout: inputs are generic ('Spectra package documentation'), tools are not versioned, and landmark outputs lack repository/path information. While coherence between research_question and finding is acceptable (both address spectraData() + fillCoreSpectraVariables() + NA filling), the execution cannot be verified without corrected evidence spans and concrete artifact references. The placeholder detection flags generic references like 'a tool' (tools section uses generic descriptions rather than specific versions/implementations) and abstract port identifiers without backing data sources. Recommend: (1) correct section mappings for research_question and finding, (2) provide complete evidence_span text, (3) add concrete file paths, repository URLs, or version numbers, (4) specify exact list of core spectra variables expected, (5) replace abstract port_ids with concrete artifact references.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

# Workflow Challenge: `coll_spectripy_workflow`


> SpectriPy enables seamless integration of Python mass spectrometry packages into R-based Spectra analysis by wrapping Python functionality as R callables.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

SpectriPy is an R package that facilitates cross-language mass spectrometry data analysis by wrapping Python MS library functions into R functions. The package describes two key mechanisms: a cross-language integration layer that exposes Python MS functions as callable R routines, and a minimal Spectra-based R workflow architecture that invokes Python MS package functions through SpectriPy's wrapper interface. Together, these mechanisms enable users to leverage Python MS libraries within their R-based Spectra mass spectrometry analysis pipelines without requiring direct Python programming.

## Research questions

- How does SpectriPy wrap Python mass spectrometry package functionality to enable seamless integration into R-based Spectra analysis workflows?
- How does SpectriPy wrap Python MS package functionality to enable seamless integration into R-based Spectra analysis workflows?

## Methods overview

Examine SpectriPy source code to identify how Python MS package functions are wrapped and exposed as R functions Map the data structures and conversion mechanisms between Spectra (R) objects and Python library objects within the same process Document the fixed architecture of the CrossLanguageIntegrationLayer showing function binding, argument marshalling, and return value conversion Design and execute representative interoperability tests combining R Spectra operations with wrapped Python MS library calls Validation: Confirm that wrapped functions execute with correct semantics, proper data interchange, and appropriate error handling Install and load SpectriPy and Spectra packages in R. Load or generate a sample mass spectrometry dataset and instantiate a Spectra object. Identify and invoke a Python MS package function exposed through the SpectriPy wrapper layer. Capture and validate the returned R-native object for type, structure, and content integrity. Validation: function call executes without error, return value is an R object (not NULL), and output type matches wrapper specification.

**Domain:** bioinformatics

**Techniques:** machine-learning, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The SpectriPy package allows integration of Python MS packages into a Spectra-based MS analysis in R. _[grounded: SpectriPy]_
- **(finding)** SpectriPy achieves seamless integration of Python libraries into R by wrapping Python functionality into R functions. _[grounded: SpectriPy]_
- **(finding)** The SpectriPy project has reached a stable, usable state and is being actively developed. _[grounded: SpectriPy]_
- **(finding)** SpectriPy is licensed under the Artistic-2.0 license. _[grounded: SpectriPy]_
- **(finding)** SpectriPy has been published with DOI 10.21105/joss.08070. _[grounded: SpectriPy]_

## Steps

### Step `task_001`
- Title: Reconstruct the Cross-Language Integration Layer wrapping Python MS functions as R callables in SpectriPy
- Task kind: `component_reconstruction`
- Task: Document and validate the CrossLanguageIntegrationLayer architecture that enables SpectriPy to wrap Python mass spectrometry package functions into R-compatible interfaces, allowing seamless in-process interoperability between Spectra (R) and Python MS libraries.
- Inputs:
  - SpectriPy source code and documentation from RforMassSpectrometry/SpectriPy repository
  - Spectra package structure and API documentation from RforMassSpectrometry/Spectra repository
- Expected outputs:
  - Architecture diagram or document describing the CrossLanguageIntegrationLayer showing how Python MS package functions are wrapped into R function interfaces
  - Technical specification document detailing the function-wrapping mechanism, data marshalling protocol, and type conversion rules between R and Python
  - Validation report confirming wrapped Python MS functions execute correctly within R Spectra workflows with correct data interchange
- Tools: SpectriPy, Spectra, R, Python
- Landmark output files: function_wrapping_inventory.csv, data_interchange_protocol.md, integration_test_results.json
- Primary expected artifact: `cross_language_integration_architecture.pdf`

### Step `task_002`
- Title: Implement a minimal Spectra-based R workflow that calls a Python MS package function via SpectriPy
- Task kind: `component_reconstruction`
- Task: Load the SpectriPy package in R, instantiate a Spectra object, and invoke at least one Python MS package function through the SpectriPy wrapper, verifying the call succeeds and returns an R-native result.
- Inputs:
  - SpectriPy R package from RforMassSpectrometry/SpectriPy repository or CRAN/Bioconductor
  - Spectra R package from RforMassSpectrometry/Spectra repository
  - Sample mass spectrometry dataset (mzML, mzXML, or compatible format) or synthetic MS data
- Expected outputs:
  - Execution log or R console output showing successful package load, Spectra object creation, and Python function invocation
  - R object returned from the Python MS package function call (e.g., numeric vector, data frame, or modified Spectra object)
  - Validation report confirming function call success, output type, and R-native data structure integrity
- Tools: SpectriPy, Spectra, R, Python
- Landmark output files: spectra_object.rds, python_function_output.rds, integration_test_log.txt
- Primary expected artifact: `spectripy_integration_example.R`

## Final expected outputs

- `Architecture diagram or document describing the CrossLanguageIntegrationLayer showing how Python MS package functions are wrapped into R function interfaces` (type: file, tolerance: hash)
- `Technical specification document detailing the function-wrapping mechanism, data marshalling protocol, and type conversion rules between R and Python` (type: file, tolerance: hash)
- `Validation report confirming wrapped Python MS functions execute correctly within R Spectra workflows with correct data interchange` (type: file, tolerance: hash)
- `Execution log or R console output showing successful package load, Spectra object creation, and Python function invocation` (type: file, tolerance: hash)
- `R object returned from the Python MS package function call (e.g., numeric vector, data frame, or modified Spectra object)` (type: file, tolerance: hash)
- `Validation report confirming function call success, output type, and R-native data structure integrity` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** tight

- **Composition modularity:** flat

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_spectripy_workflow",
  "agent_order": [
    "task_001",
    "task_002"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Architecture diagram or document describing the CrossLanguageIntegrationLayer showing how Python MS package functions are wrapped into R function interfaces": "<locator>",
    "Technical specification document detailing the function-wrapping mechanism, data marshalling protocol, and type conversion rules between R and Python": "<locator>",
    "Validation report confirming wrapped Python MS functions execute correctly within R Spectra workflows with correct data interchange": "<locator>",
    "Execution log or R console output showing successful package load, Spectra object creation, and Python function invocation": "<locator>",
    "R object returned from the Python MS package function call (e.g., numeric vector, data frame, or modified Spectra object)": "<locator>",
    "Validation report confirming function call success, output type, and R-native data structure integrity": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._

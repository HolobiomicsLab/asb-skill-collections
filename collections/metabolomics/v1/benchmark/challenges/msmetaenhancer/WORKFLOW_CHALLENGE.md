# Workflow Challenge: `coll_msmetaenhancer_workflow`


> MSMetaEnhancer is a Python tool that enriches mass spectrometry metadata files (.msp) by asynchronously fetching chemical identifiers (SMILES, InChI, CAS numbers) from multiple external services.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MSMetaEnhancer adds metadata including SMILES, InChI, and CAS number to .msp files through asynchronous annotation processing, retrieving data from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb. The tool implements a modular architecture comprising web-based converters that make HTTP requests to external APIs and compute-based converters for local chemical structure transformations. The system uses a ConverterBuilder mechanism to automatically discover and instantiate available converters into Job objects that define conversion tasks, and employs Monitor-based service status tracking during the annotation process. RDKit serves as a reference implementation for ComputeConverter subclasses that perform local chemical property computations.

## Research questions

- What metadata fields can MSMetaEnhancer add to mass spectra records by querying external web services?
- How does the ConverterBuilder component automatically discover and instantiate all available converter classes to create a complete set of source-to-target conversion Job objects?
- How does MSMetaEnhancer track the availability and error state of external web services during annotation runs?
- How does a ComputeConverter subclass using RDKit perform local chemical structure conversions (e.g., SMILES to InChI) without relying on web services?
- What are the per-attribute fill-rate statistics and annotation coverage metrics produced by MSMetaEnhancer's Logger component when running the full annotation pipeline on a test .msp file?

## Methods overview

Instantiate MSMetaEnhancer Application and load sample .msp spectra file. Define conversion jobs specifying source compound attributes, target metadata fields (SMILES, InChI, CAS), and web converter services (CIR, CTS, PubChem, IDSM, BridgeDb). Invoke asynchronous `annotate_spectra` method to dispatch enrichment requests to each service via WebConverter HTTP queries. Aggregate parsed API responses into enriched spectra records. Validation: verify all target metadata fields are populated in output .msp file and conform to expected chemical identifier formats (SMILES syntax, InChI structure, CAS registry numbering). Dynamically discover all converter class definitions in the web and compute converter packages using Python module introspection. Instantiate each discovered converter class with appropriate initialization parameters (session for web, no args for compute). Extract the conversions tuple list from each converter's __init__ method via attribute inspection. Transform each conversion tuple into a Job object and aggregate into a master enumeration. Validate that all declared conversion methods are callable and match their specifications. Validation: Run pytest on ConverterBuilder tests to confirm that the enumerated job list matches the expected set of conversions for all registered services. Instantiate Monitor class with registry of active web service converters (CIR, CTS, PubChem, IDSM, BridgeDb) and initialize per-service state dictionaries for uptime, error counts, latency, and last-check timestamp. Integrate Monitor with asynchronous annotation event loop to capture request-start, response-received, and error-occurred events from WebConverter base class. Compute per-service metrics: uptime percentage (successful requests / total requests), cumulative error count, mean response latency, and wall-clock timestamp of last status check. Serialize aggregated status as JSON with per-service summaries (availability %, error count, mean latency ms, last check) and overall health indicator. Validation: verify JSON output contains all five registered services, all uptime and error counts are non-negative integers, latency values are positive floats, and timestamps are ISO 8601 format. Create a new ComputeConverter subclass file in the compute converters directory. Define conversions list (source → target mappings) and invoke create_top_level_conversion_methods with asynch=False. Implement RDKit-based conversion methods (e.g., SMILES to InChI via Chem.MolFromSmiles and Chem.inchi.MolToInchi). Return results as dictionaries mapping target attribute names to converted values. Register the converter in __init__.py for auto-discovery. Write pytest tests validating converter instantiation and conversion accuracy on reference SMILES inputs. Validation: all pytest tests pass, including new converter tests and existing test suite, confirming correct implementation of ComputeConverter interface and accurate molecular structure conversions. Load the example .msp file and initialize the MSMetaEnhancer Application with all available converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) via ConverterBuilder. Run the asynchronous annotate_spectra() method with all supported conversion jobs to enrich spectra metadata in parallel. Capture structured Logger output events recording per-attribute conversion success, failure, and enrichment outcome for each spectrum. Parse Logger records to compute initial and final fill rates (non-null counts) for each metadata field across the spectra dataset. Construct a summary table with metadata fields as rows and fill-rate before/after annotation, absolute and relative gain as columns. Validation: verify that summary table row count matches the number of metadata fields present in the annotated .msp file, and that all fill-rate values are in [0, 1].

**Domain:** cheminformatics

**Techniques:** database-annotation, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MSMetaEnhancer is a tool used for .msp files annotation. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** MSMetaEnhancer adds metadata like SMILES, InChI, and CAS number to files. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** MSMetaEnhancer fetches metadata from CIR, CTS, PubChem, IDSM, and BridgeDb services. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** MSMetaEnhancer uses asynchronous implementation of annotation process allowing for optimal fetching speed. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** The citation for MSMetaEnhancer is Troják et al., (2022). MSMetaEnhancer: A Python package for mass spectra metadata annotation. Journal of Open Source Software, 7(79), 4494. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** MSMetaEnhancer has a modular architecture that makes it easy to add new conversion services. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** There are two main types of converters in MSMetaEnhancer: Web Converters and Compute Converters. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Web Converters are services that make HTTP requests to external APIs.
- **(finding)** Compute Converters are services that perform local computations.
- **(finding)** Converter is an abstract base class for all converters in MSMetaEnhancer. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** WebConverter is a base class for web-based API services in MSMetaEnhancer. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** ComputeConverter is a base class for local computation services in MSMetaEnhancer. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Job represents a conversion task defined as source attribute to target attribute using specific converter. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter Builder automatically discovers and instantiates available converters. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converters automatically generate methods like compound_name_to_inchi() based on conversions list. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Web converters should be created in MSMetaEnhancer/libs/converters/web/ directory. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Converters should define endpoints as a dictionary in their __init__ method.
- **(finding)** Converters should define conversions as tuples of source attribute, target attribute, and conversion method.
- **(finding)** Web converters should use Throttler for rate limiting if needed. _[grounded: COMP_THROTTLER]_
- **(finding)** Web converters should be registered in MSMetaEnhancer/libs/converters/web/__init__.py file. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Compute converters should be created in MSMetaEnhancer/libs/converters/compute/ directory. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Compute converters should use asynch=False when creating conversion methods.
- **(finding)** Compute converters should be registered in MSMetaEnhancer/libs/converters/compute/__init__.py file. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** Converter developers should always handle API errors gracefully and return empty dictionaries when data is not available. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter developers should respect API rate limits using throttling mechanisms. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter developers should validate input data before making API calls. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter developers should implement robust response parsing that handles various response formats. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter developers should include docstrings for all methods explaining parameters and return values. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Converter developers should write comprehensive tests including service availability and conversion functionality. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** Developers should run pytest tests/ to ensure they haven't broken existing tests.
- **(finding)** Developers can use Throttler class for rate limiting in converters. _[grounded: COMP_THROTTLER]_
- **(finding)** Developers can use @lru_cache decorator for caching responses in converters.
- **(finding)** Developers can use @escape_single_quotes decorator for input sanitization in converters.
- **(finding)** CTS or PubChem converters serve as reference implementations for Web Converter Template. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** RDKit converter serves as a reference implementation for Compute Converter Template. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** The Application class serves as a top-level interface to use MSMetaEnhancer tool. _[grounded: SYS_MSMETAENHANCER]_
- **(finding)** The main method of Application class is asynchronous annotate_spectra method. _[grounded: COMP_APPLICATION]_
- **(finding)** annotate_spectra method runs annotation process using given conversions. _[grounded: COMP_SPECTRA]_
- **(finding)** It is possible to specify particular conversion jobs in annotate_spectra which will be executed in respecting the given order. _[grounded: COMP_SPECTRA]_
- **(finding)** If no jobs are given to annotate_spectra, all jobs supported by given services are used. _[grounded: COMP_SPECTRA]_
- **(finding)** Application class allows loading and saving spectra files in supported formats. _[grounded: COMP_APPLICATION]_
- **(finding)** Application class allows curation of given spectra. _[grounded: COMP_APPLICATION]_
- **(finding)** In version 0.1.3, multidict was passed instead of frozendict to aiohttp.ClientSession.post because it is required by the package.
- **(finding)** In version 0.1.3, only the first result is taken when there are multiple hits in CIR conversions.
- **(finding)** In version 0.1.3, PubChem now supports ISOMERIC_SMILES and CANONICAL_SMILES instead of generic SMILES. _[grounded: TOOL_PUBCHEM]_
- **(finding)** In version 0.1.2 released on 2022-01-06, generate_options() function was added to Galaxy submodule.
- **(finding)** In version 0.1.2, monitoring of services status during annotation process was added. _[grounded: COMP_MONITOR]_
- **(finding)** In version 0.1.2, validation of obtained metadata was added.
- **(finding)** In version 0.1.2, structure and contents of documentation were changed.
- **(finding)** In version 0.1.2, tests checking contents and consistency of individual services were removed.
- **(finding)** In version 0.1.1 released on 2021-12-07, get_conversion_functions was added on the level of Converter. _[grounded: COMP_CONVERTER_BASE]_
- **(finding)** In version 0.1.1, computation of all available jobs in Application was changed. _[grounded: COMP_APPLICATION]_
- **(finding)** In version 0.1.1, get_all_conversions on the level of Annotator was removed. _[grounded: COMP_ANNOTATOR]_
- **(finding)** In version 0.1.0 released on 2021-11-16, conda environment files were added.
- **(finding)** In version 0.1.0, IDSM SPARQL was used for PubChem service. _[grounded: TOOL_PUBCHEM]_
- **(finding)** In version 0.1.0, logging and quantitative progress of annotation process were added.
- **(finding)** In version 0.1.0, generalised requests to obtain multiple values at once were added.
- **(finding)** In version 0.1.0, asynchronous requests were added to MSMetaEnhancer. _[grounded: SYS_MSMETAENHANCER]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Web Converters as alternative to Compute Converters

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Rate limiting must respect API rate limits using throttling mechanisms

## Steps

### Step `task_001`
- Title: Reproduce the asynchronous annotation pipeline for .msp spectral library files
- Task kind: `reproduction`
- Task: Execute MSMetaEnhancer's `annotate_spectra` asynchronous method on a sample .msp file to enrich compound metadata (SMILES, InChI, CAS number) by dispatching conversion jobs to external web services (CIR, CTS, PubChem, IDSM, BridgeDb), and produce an annotated .msp output file.
- Inputs:
  - Sample .msp spectra file with compound metadata (e.g., compound name, molecular weight, retention time)
- Expected outputs:
  - Annotated .msp file with enriched metadata fields (SMILES, InChI, CAS number) populated from web service conversions
- Tools: MSMetaEnhancer, CIR, CTS, PubChem, IDSM, BridgeDb, Python
- Landmark output files: spectra_loaded.log, conversion_jobs_configured.json, enriched_records.json, annotated.msp
- Primary expected artifact: `annotated.msp`

### Step `task_002`
- Title: Reconstruct the ConverterBuilder automatic service discovery and Job enumeration mechanism
- Task kind: `component_reconstruction`
- Task: Implement the ConverterBuilder component that automatically discovers all available WebConverter and ComputeConverter subclasses from the MSMetaEnhancer package and instantiates the complete set of Job objects representing all supported source→target conversion pairs. Verify the enumerated jobs match the conversion functions defined in each converter class.
- Inputs:
  - MSMetaEnhancer source code package including libs/converters/web/ and libs/converters/compute/ directories
  - WebConverter and ComputeConverter base class definitions with conversion specifications
- Expected outputs:
  - Enumerated list of Job objects (source_attribute, target_attribute, converter_name) representing all supported conversions
  - Test report (pytest output) verifying discovered jobs match converter-defined conversion methods
  - ConverterBuilder instantiation log or manifest showing all discovered converter classes and their conversion counts
- Tools: pytest, Python, MSMetaEnhancer
- Landmark output files: discovered_converters.txt, converter_conversions_list.csv, pytest_output.log
- Primary expected artifact: `converter_jobs_manifest.json`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Monitor-based service status tracking during annotation
- Task kind: `component_reconstruction`
- Task: Implement the Monitor component to track availability and error state of external web services (CIR, CTS, PubChem, IDSM, BridgeDb) during annotation runs. Produce a structured JSON status report per service including uptime, error counts, and response times.
- Inputs:
  - List of active web service converters (CIR, CTS, PubChem, IDSM, BridgeDb) and their endpoint URLs
  - Asynchronous annotation run events (request start, response received, error occurred)
- Expected outputs:
  - Structured JSON status report per service including uptime percentage, error count, mean response time, and last check timestamp
- Tools: MSMetaEnhancer, Python, CIR, CTS, PubChem, IDSM, BridgeDb, pytest
- Landmark output files: service_endpoints.json, error_log_per_service.csv, service_status_report.json
- Primary expected artifact: `service_status_report.json`

### Step `task_004`
- Title: Reconstruct the RDKit-based ComputeConverter template for local chemical property computation
- Task kind: `component_reconstruction`
- Task: Implement a ComputeConverter subclass using RDKit to perform local chemical structure conversions (e.g., SMILES to InChI or molecular formula) following the ComputeConverter base-class contract, and verify correct output for a set of reference SMILES strings.
- Inputs:
  - RDKit library installation and MSMetaEnhancer package source code with ComputeConverter base class
  - Reference SMILES strings for validation testing
- Expected outputs:
  - ComputeConverter subclass Python module (e.g., MyComputeService.py) with at least one functional conversion method
  - pytest test file (test_MyComputeService.py) demonstrating converter availability and conversion accuracy
  - Updated __init__.py in MSMetaEnhancer/libs/converters/compute/ registering the new converter
  - Test execution report showing all tests passing (pytest output)
- Tools: MSMetaEnhancer, RDKit, pytest, Python
- Landmark output files: MSMetaEnhancer/libs/converters/compute/MyComputeService.py, tests/test_MyComputeService.py, MSMetaEnhancer/libs/converters/compute/__init__.py, pytest_output.log
- Primary expected artifact: `MyComputeService.py`

### Step `task_005`
- Depends on: `task_004`
- Title: Analyze the metadata annotation coverage and logging output produced on a reference .msp dataset
- Task kind: `analysis`
- Task: Execute the MSMetaEnhancer annotation pipeline on a public .msp test file using all available converters (web and compute services), then extract and summarize the structured Logger output to produce a per-attribute annotation fill-rate table showing metadata enrichment coverage.
- Inputs:
  - MSMetaEnhancer public example .msp test file
- Expected outputs:
  - Structured Logger output with per-attribute annotation events and statistics
  - Summary table of annotation coverage per metadata field (CSV or structured format)
- Tools: MSMetaEnhancer, CIR, CTS, PubChem, IDSM, BridgeDb, RDKit, Python
- Landmark output files: raw_annotation_log.json, per_field_fill_rates.csv
- Primary expected artifact: `annotation_coverage_summary.csv`

## Final expected outputs

- `Annotated .msp file with enriched metadata fields (SMILES, InChI, CAS number) populated from web service conversions` (type: file, tolerance: hash)
- `Structured JSON status report per service including uptime percentage, error count, mean response time, and last check timestamp` (type: file, tolerance: hash)
- `Structured Logger output with per-attribute annotation events and statistics` (type: file, tolerance: hash)
- `Summary table of annotation coverage per metadata field (CSV or structured format)` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** dynamic

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
  "workflow_id": "coll_msmetaenhancer_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Annotated .msp file with enriched metadata fields (SMILES, InChI, CAS number) populated from web service conversions": "<locator>",
    "Structured JSON status report per service including uptime percentage, error count, mean response time, and last check timestamp": "<locator>",
    "Structured Logger output with per-attribute annotation events and statistics": "<locator>",
    "Summary table of annotation coverage per metadata field (CSV or structured format)": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._

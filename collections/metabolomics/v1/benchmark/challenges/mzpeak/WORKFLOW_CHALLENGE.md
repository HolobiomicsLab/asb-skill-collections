# Workflow Challenge: `coll_mzpeak_workflow`


> This work presents prototype implementations of the mzPeak mass spectrometry data format across three programming languages, with a draft specification document available for compliance validation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: A draft mzPeak specification document is publicly available at https://hupo-psi.github.io/mzPeak-specification/ against which Rust implementation output can be validated for compliance. Analyses 1 derived result: Three independent mzPeak reader implementations exist: a Rust library, a Python implementation using pyarrow, and an R implementation using arrow, all capable of reading mzPeak files. Reconstructs 3 described mechanisms (described in the paper but not separately evaluated there): The Rust implementation at the repository root includes command-line tools capable of converting existing mass spectrometry data formats into the mzPeak format, operating as a library for both reading and writing mzPeak files. The Python implementation provides a complete re-implementation for reading mzPeak files using the pyarrow library, enabling conversion of mzPeak spectrum data into structured tabular artifacts compatible with the PyData stack. The R implementation provides a complete re-implementation for reading mzPeak files using the arrow package, enabling loading of valid mzPeak files into structured tabular format.

## Research questions

- What are the input formats supported by the Rust command-line converter tool in the mzpeak_prototyping repository, and what is the mechanism by which it converts them into mzPeak output?
- How does the Python implementation using pyarrow enable reading of mzPeak files into a structured tabular format?
- How does the R implementation using the arrow package read and parse a valid mzPeak file into a structured tabular representation of spectrum data?
- Do the Rust, Python/pyarrow, and R/arrow implementations of mzPeak file readers produce field-level agreement when loading the same input file?
- Does the Rust implementation of mzPeak produce files that conform to all mandatory fields and structural elements defined in the published mzPeak specification?

## Methods overview

Obtain the Rust implementation from github.com/mobiusklein/mzpeak_prototyping. Compile the command-line converter tool using Rust's cargo build system. Run the converter with mzML input file and specify the mzPeak output file path. Validate: output file is generated in valid mzPeak binary format matching the draft specification structure. References: source article (DOI: 10.1021/acs.jproteome.5c00435) Access the Python mzPeak reader implementation from the mobiusklein/mzpeak_prototyping repository. Load the mzPeak binary file using the Python reader module with pyarrow as the backing table library. Convert the in-memory spectrum data structure to a pandas DataFrame or pyarrow Table. Serialize the tabular data to Parquet format for structured output and downstream interoperability. Validation: verify that the output Parquet file contains all spectrum records with correctly parsed m/z and intensity columns and matches the row count of the source mzPeak file. References: source article (DOI: 10.1021/acs.jproteome.5c00435) Access the R implementation in the mobiusklein/mzpeak_prototyping repository. Load the arrow R package for mzPeak file I/O. Invoke the R read function to load a valid mzPeak file into memory. Convert the in-memory representation to a structured data frame with spectrum fields. Validation: Output contains spectrum records with expected schema (m/z, intensity, metadata fields) and row count ≥ 1. References: source article (DOI: 10.1021/acs.jproteome.5c00435) Load and parse mzPeak file using Rust library reader; export tabular spectrum output to standardized CSV format. Load and parse identical mzPeak file using Python/pyarrow reader implementation; export tabular spectrum output to standardized CSV format. Load and parse identical mzPeak file using R/arrow reader implementation; export tabular spectrum output to standardized CSV format. Perform field-by-field comparison of three CSV outputs: verify field names match, data types agree, row counts are identical, and numerical values are consistent across implementations. Validation: Generate consistency report confirming all three implementations produce identical field structure and values; flag any discrepancies in field presence, type, or numerical content as implementation divergences. References: source article (DOI: 10.1021/acs.jproteome.5c00435) Retrieve the draft mzPeak specification document from the published HUPO-PSI living specification URL. Extract the list of mandatory fields and required structural elements from the specification. Obtain a reference mzPeak file generated by the Rust implementation. Parse the file using Rust library reading functionality and examine its structure. Cross-reference all mandatory fields and structural elements against the parsed file. Validation: compliance is achieved when all mandatory fields listed in the specification are present in the mzPeak file with correct structural nesting and data types. References: source article (DOI: 10.1021/acs.jproteome.5c00435)

**Domain:** bioinformatics

**Techniques:** feature-detection, quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The mzPeak file format was initially described in a peer-reviewed publication. _[grounded: mzPeak_format]_
- **(finding)** The mzPeak format was presented at the HUPO conference in Toronto, Canada on November 11, 2025. _[grounded: mzPeak_format]_
- **(finding)** The mzPeak name is currently held in trust by the OpenMS Inc. _[grounded: mzPeak_format]_
- **(finding)** This project is a work in progress with no stability guaranteed.
- **(finding)** The primary mzPeak implementation is written in Rust and includes a library for reading and writing mzPeak files. _[grounded: mzPeak_format]_
- **(finding)** The Rust implementation includes command line tools for converting existing formats into mzPeak. _[grounded: mzPeak_format]_
- **(finding)** A separate Python implementation exists in the `python/` directory. _[grounded: mzPeak_format]_
- **(finding)** The Python implementation uses `pyarrow` and the PyData stack for reading mzPeak files. _[grounded: mzPeak_format]_
- **(finding)** The Python implementation does not currently support writing mzPeak files. _[grounded: mzPeak_format]_
- **(finding)** An R implementation exists in the `R/` directory for reading mzPeak files. _[grounded: mzPeak_format]_
- **(finding)** A draft specification document for the mzPeak format is available online. _[grounded: mzPeak_format]_

## Steps

### Step `task_001`
- Title: Reconstruct the mzPeak CLI Converter tool for transforming existing mass-spectrometry formats into mzPeak
- Task kind: `component_reconstruction`
- Task: Build and execute the Rust command-line converter tool to convert an mzML input file into a valid mzPeak output file. Produce a single converted mzPeak file in the correct binary format.
- Inputs:
  - mzML mass spectrometry data file (raw or test input)
- Expected outputs:
  - mzPeak binary output file with valid format structure and metadata
- Tools: OpenMS, Rust
- Landmark output files: converter_binary, output.mzpeak
- Primary expected artifact: `output.mzpeak`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct mzPeak file reading using the Python (pyarrow) implementation
- Task kind: `component_reconstruction`
- Task: Load a valid mzPeak file using the Python implementation from the mobiusklein/mzpeak_prototyping repository and pyarrow library, then produce a structured tabular artifact (DataFrame or Parquet file) representing the spectrum data.
- Inputs:
  - Valid mzPeak file (binary format compliant with draft mzPeak specification)
  - Python mzPeak reader implementation from mobiusklein/mzpeak_prototyping repository
- Expected outputs:
  - Structured tabular artifact (Parquet or CSV file) containing parsed spectrum data with annotated columns (m/z values, intensities, spectrum metadata)
- Tools: OpenMS, Python, pyarrow
- Landmark output files: mzpeak_raw_load.py, spectrum_data.parquet, spectrum_summary.csv
- Primary expected artifact: `spectrum_data.parquet`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct mzPeak file reading using the R (arrow) implementation
- Task kind: `component_reconstruction`
- Task: Load a valid mzPeak file using the R implementation with the arrow package and produce a structured tabular artifact (data frame or table) representing the spectrum data.
- Inputs:
  - Valid mzPeak file (mzPeak format)
  - R implementation from mobiusklein/mzpeak_prototyping repository, R/ subdirectory
- Expected outputs:
  - Structured tabular artifact (R data frame) containing spectrum data fields
- Tools: OpenMS, arrow, R
- Landmark output files: mzpeak_file_loaded.rds, spectrum_data.csv
- Primary expected artifact: `spectrum_data.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze cross-implementation output consistency across Rust, Python, and R mzPeak readers
- Task kind: `analysis`
- Task: Load the same mzPeak file using three independent reader implementations (Rust library, Python/pyarrow, and R/arrow) and compare the resulting tabular outputs to verify field-level agreement across all three readers. Generate a cross-implementation consistency report.
- Inputs:
  - mzPeak test file in mzPeak format
- Expected outputs:
  - Rust implementation spectrum table (CSV format)
  - Python/pyarrow implementation spectrum table (CSV format)
  - R/arrow implementation spectrum table (CSV format)
  - Cross-implementation consistency report documenting field-level agreement and any divergences
- Tools: OpenMS, Rust, Python, pyarrow, R, arrow
- Landmark output files: rust_spectrum_table.csv, python_spectrum_table.csv, r_spectrum_table.csv
- Primary expected artifact: `cross_implementation_consistency_report.txt`

### Step `task_005`
- Depends on: `task_001`
- Title: Reproduce the mzPeak specification compliance of the prototype implementations against the published draft specification
- Task kind: `reproduction`
- Task: Retrieve the draft mzPeak specification from https://hupo-psi.github.io/mzPeak-specification/ and verify that at least one mzPeak file produced by the Rust implementation contains all mandatory fields and structural elements defined in the specification. Output a compliance report.
- Inputs:
  - mzPeak specification document (living draft) from https://hupo-psi.github.io/mzPeak-specification/
  - mzPeak file produced by Rust implementation from HUPO-PSI/mzPeak repository
- Expected outputs:
  - Compliance report verifying presence/absence of all mandatory fields and structural elements
- Tools: OpenMS, Rust
- Landmark output files: specification_mandatory_fields.txt, parsed_mzpeak_structure.json, field_presence_matrix.csv
- Primary expected artifact: `mzpeak_compliance_report.txt`

## Final expected outputs

- `Structured tabular artifact (Parquet or CSV file) containing parsed spectrum data with annotated columns (m/z values, intensities, spectrum metadata)` (type: file, tolerance: hash)
- `Structured tabular artifact (R data frame) containing spectrum data fields` (type: file, tolerance: hash)
- `Rust implementation spectrum table (CSV format)` (type: file, tolerance: hash)
- `Python/pyarrow implementation spectrum table (CSV format)` (type: file, tolerance: hash)
- `R/arrow implementation spectrum table (CSV format)` (type: file, tolerance: hash)
- `Cross-implementation consistency report documenting field-level agreement and any divergences` (type: file, tolerance: hash)
- `Compliance report verifying presence/absence of all mandatory fields and structural elements` (type: file, tolerance: hash)

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

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mzpeak_workflow",
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
    "Structured tabular artifact (Parquet or CSV file) containing parsed spectrum data with annotated columns (m/z values, intensities, spectrum metadata)": "<locator>",
    "Structured tabular artifact (R data frame) containing spectrum data fields": "<locator>",
    "Rust implementation spectrum table (CSV format)": "<locator>",
    "Python/pyarrow implementation spectrum table (CSV format)": "<locator>",
    "R/arrow implementation spectrum table (CSV format)": "<locator>",
    "Cross-implementation consistency report documenting field-level agreement and any divergences": "<locator>",
    "Compliance report verifying presence/absence of all mandatory fields and structural elements": "<locator>"
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

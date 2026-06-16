# Workflow Challenge: `coll_matchms_workflow`


> Matchms is an open-source Python package for importing, processing, cleaning, and comparing mass spectrometry data. The package supports multiple spectral data formats and provides tools for metadata cleaning, peak filtering, and pairwise spectral similarity comparisons.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Matchms facilitates reproducible workflows for mass spectrometry (MS/MS) data analysis, supporting popular spectral data formats including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON. The package implements metadata cleaning and validation tools alongside basic peak filtering mechanisms to ensure data accuracy and integrity. For spectral comparison, matchms applies various pairwise similarity measures, encompassing Cosine-related scores, molecular fingerprint-based comparisons, and metadata-related assessments. The software is distributed through multiple channels including PyPI and Bioconda, with release management procedures documented in the contributing guidelines.

## Research questions

- What metadata cleaning and validation tools does matchms provide, and how do they operate on mass spectrometry spectral data?
- What are the input requirements and operational mechanics of matchms' peak filtering capability when applied to spectral data files?
- How does matchms compute pairwise cosine similarity scores across a set of preprocessed mass spectra?
- What is the operational mechanism by which matchms applies molecular fingerprint-based similarity measures to compare pairs of mass spectra?
- Are the documented distribution channels (PyPI and Bioconda) for matchms functional and does the package import successfully after installation from these channels?

## Methods overview

Import spectral data from a public MGF or MSP file repository using matchms I/O functions. Apply matchms metadata cleaning filters to standardize spectrum annotations (precursor m/z, retention time, compound identifiers, instrument metadata). Apply matchms validation filters to remove spectra with missing or malformed critical metadata fields. Export cleaned spectrum collection to output file in MGF or JSON format. Validation: Run pytest on the cleaning module to confirm filter logic executes without error and output spectrum count and metadata completeness match expected thresholds. Load spectral data from a file in a supported format using matchms import functionality. Apply matchms peak-filtering functions to remove low-intensity and irrelevant peaks for data accuracy and integrity. Export the filtered spectrum collection to an output file in the original or compatible spectral format. Validation: filtered spectrum collection is produced in valid spectral format (MGF, MSP, mzML, or JSON) with all peaks from the original input preserved or removed according to the specified filtering criteria. Load preprocessed spectra from input file using matchms spectrum importers. Initialize cosine similarity scorer within matchms. Compute pairwise cosine similarity scores across all spectrum pairs. Construct scores matrix with spectrum identifiers as row and column labels. Validation: Verify output scores matrix has dimensions N×N where N equals the number of input spectra, and all values are in the range [0, 1]. Load preprocessed mass spectra from a matchms-compatible file format (mzML, mzXML, msp, MGF, or JSON) into memory. Apply the molecular fingerprint-based similarity measure available in matchms to compute pairwise similarity scores for all spectra. Export the pairwise similarity matrix to a named output file in tabular format. Validation: Output matrix is symmetric, contains similarity scores for all spectrum pairs, and matches expected dimensions (N×N where N is number of spectra). Create isolated Python environment (virtual environment or fresh conda env) to ensure clean installation baseline. Download and install matchms from PyPI using pip, capturing installation logs and any error messages. Execute Python import statement 'import matchms' and verify no ImportError or ModuleNotFoundError exceptions occur; record success status. Create second isolated conda environment and install matchms from Bioconda channel, capturing installation logs. Execute Python import statement 'import matchms' in the Bioconda environment and verify no ImportError or ModuleNotFoundError exceptions occur; record success status. Validation: Both PyPI and Bioconda installations complete without error, and matchms module imports successfully in both environments, confirming both distribution channels are functional.

**Domain:** cheminformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Matchms is an open-source Python package for importing, processing, cleaning, and comparing mass spectrometry data. _[grounded: matchms_system]_
- **(finding)** Matchms facilitates the implementation of straightforward, reproducible workflows for transforming raw mass spectra data. _[grounded: matchms_system]_
- **(finding)** Matchms enables large-scale spectral similarity comparisons. _[grounded: matchms_system]_
- **(finding)** Matchms supports mzML, mzXML, msp, metabolomics-USI, MGF, and JSON spectral data formats. _[grounded: matchms_system]_
- **(finding)** Matchms offers tools for metadata cleaning and validation. _[grounded: matchms_system]_
- **(finding)** Matchms offers tools for basic peak filtering. _[grounded: matchms_system]_
- **(finding)** Matchms can apply Cosine-related scores for comparing spectra. _[grounded: matchms_system]_
- **(finding)** Matchms can apply molecular fingerprint-based comparisons for comparing spectra. _[grounded: matchms_system]_
- **(finding)** Matchms is extensible, allowing users to integrate custom implementations. _[grounded: matchms_system]_
- **(finding)** Contributions to matchms can take the form of questions, bug reports, code changes, or release work. _[grounded: matchms_system]_
- **(finding)** When making a question-related contribution to matchms, contributors should search existing issues first. _[grounded: matchms_system]_
- **(finding)** When reporting a bug in matchms, contributors should search existing issues first. _[grounded: matchms_system]_
- **(finding)** When reporting a bug in matchms, contributors should provide the SHA hashcode of the commit causing the problem. _[grounded: matchms_system]_
- **(finding)** When reporting a bug in matchms, contributors should provide dependency name and version information. _[grounded: matchms_system]_
- **(finding)** When reporting a bug in matchms, contributors should provide information about the operating system. _[grounded: matchms_system]_
- **(finding)** Before making code changes to matchms, contributors must announce their plan to the community as an issue. _[grounded: matchms_system]_
- **(finding)** Before making code changes to matchms, contributors must wait for consensus to be reached about the proposed idea. _[grounded: matchms_system]_
- **(finding)** Contributors to matchms should run pytest to ensure existing tests still work. _[grounded: matchms_system]_
- **(finding)** Contributors to matchms should update the CHANGELOG.md file with their changes. _[grounded: matchms_system]_
- **(finding)** To release matchms, the version can be bumped using the poetry version command. _[grounded: matchms_system]_
- **(finding)** When releasing matchms, the version can be manually changed in __version__.py and pyproject.toml. _[grounded: matchms_system]_
- **(finding)** When releasing matchms, the author list in citation.cff and .zenodo.json files should be checked. _[grounded: matchms_system]_
- **(finding)** Matchms releases are published to PyPI via a PyPI publish workflow. _[grounded: matchms_system]_
- **(finding)** Matchms releases are available on Bioconda via automatically created pull requests on the bioconda-recipes repository. _[grounded: matchms_system]_
- **(finding)** A Zenodo entry with its own DOI is created for each matchms release. _[grounded: matchms_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the metadata cleaning and validation pipeline step in matchms
- Task kind: `component_reconstruction`
- Task: Load a publicly available mass spectrometry spectral dataset (MGF or MSP file from the matchms repository) and apply matchms metadata cleaning and validation filters to produce a cleaned spectrum collection. Output the cleaned spectra as a validated dataset file.
- Inputs:
  - Public spectral dataset in MGF or MSP format from matchms repository
- Expected outputs:
  - Cleaned spectrum collection with validated metadata as MGF or JSON file
  - Test report confirming metadata validation filters pass
- Tools: matchms, Python, pytest
- Landmark output files: raw_spectrum_count.txt, metadata_validation_log.csv, cleaned_spectra.mgf, pytest_report.txt
- Primary expected artifact: `cleaned_spectra.mgf`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the peak filtering pipeline step in matchms
- Task kind: `component_reconstruction`
- Task: Apply matchms peak-filtering functions to a spectral data file (MGF, MSP, or mzML format) from the matchms repository, producing a filtered spectrum collection with low-intensity and irrelevant peaks removed.
- Inputs:
  - Raw spectral data file in MGF, MSP, or mzML format from matchms GitHub repository
- Expected outputs:
  - Filtered spectrum collection with peaks removed by matchms peak-filtering functions
- Tools: matchms, Python
- Landmark output files: raw_spectrum_collection.mgf, filtered_spectrum_collection.mgf
- Primary expected artifact: `filtered_spectrum_collection.mgf`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct pairwise cosine similarity scoring with matchms
- Task kind: `component_reconstruction`
- Task: Compute a pairwise cosine similarity score matrix for a set of preprocessed spectra using matchms, and save the resulting scores matrix as a named file.
- Inputs:
  - Preprocessed spectra (peak-filtered or reference spectral library in mzML, mzXML, msp, MGF, or JSON format)
- Expected outputs:
  - Pairwise cosine similarity scores matrix file (CSV or pickle format with spectrum identifiers and similarity scores)
- Tools: matchms, Python
- Landmark output files: spectra_loaded.log, cosine_scores_matrix.csv
- Primary expected artifact: `cosine_scores_matrix.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct molecular fingerprint-based pairwise comparison with matchms
- Task kind: `component_reconstruction`
- Task: Apply molecular fingerprint-based similarity measures in matchms to a set of preprocessed mass spectra, producing a pairwise similarity scores matrix as a named output file.
- Inputs:
  - Preprocessed mass spectra data in a supported matchms format (mzML, mzXML, msp, MGF, or JSON)
- Expected outputs:
  - Pairwise similarity scores matrix from fingerprint-based spectral comparison
- Tools: matchms, Python
- Landmark output files: loaded_spectra.pkl, fingerprint_similarity_matrix.csv
- Primary expected artifact: `fingerprint_similarity_matrix.csv`

### Step `task_005`
- Title: Reproduce matchms installation and import across supported distribution channels
- Task kind: `reproduction`
- Task: Verify that matchms installs correctly from PyPI and Bioconda package repositories and that the package imports without error, confirming both documented distribution channels are functional for the current release version.
- Inputs:
  - Current matchms release version identifier (e.g., from PyPI or GitHub releases page)
  - Access to PyPI package repository
  - Access to Bioconda package repository
- Expected outputs:
  - Installation log from PyPI showing successful package installation with no errors
  - Installation log from Bioconda showing successful package installation with no errors
  - Import test result confirming matchms module loads without errors from both installations
- Tools: matchms, Python, pip, conda
- Landmark output files: pypi_install.log, bioconda_install.log, pypi_import_test.txt, bioconda_import_test.txt
- Primary expected artifact: `installation_smoke_test_report.txt`

## Final expected outputs

- `Filtered spectrum collection with peaks removed by matchms peak-filtering functions` (type: file, tolerance: hash)
- `Pairwise cosine similarity scores matrix file (CSV or pickle format with spectrum identifiers and similarity scores)` (type: file, tolerance: hash)
- `Pairwise similarity scores matrix from fingerprint-based spectral comparison` (type: file, tolerance: hash)
- `Installation log from PyPI showing successful package installation with no errors` (type: file, tolerance: hash)
- `Installation log from Bioconda showing successful package installation with no errors` (type: file, tolerance: hash)
- `Import test result confirming matchms module loads without errors from both installations` (type: file, tolerance: hash)

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

- **Abstraction level:** intermediate

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
  "workflow_id": "coll_matchms_workflow",
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
    "Filtered spectrum collection with peaks removed by matchms peak-filtering functions": "<locator>",
    "Pairwise cosine similarity scores matrix file (CSV or pickle format with spectrum identifiers and similarity scores)": "<locator>",
    "Pairwise similarity scores matrix from fingerprint-based spectral comparison": "<locator>",
    "Installation log from PyPI showing successful package installation with no errors": "<locator>",
    "Installation log from Bioconda showing successful package installation with no errors": "<locator>",
    "Import test result confirming matchms module loads without errors from both installations": "<locator>"
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

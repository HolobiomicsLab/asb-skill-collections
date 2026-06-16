# Workflow Challenge: `coll_pyteomics_workflow`


> Pyteomics is a Python package providing lightweight tools for proteomics data analysis, with modules for calculating polypeptide properties and accessing common proteomics data formats. The package is installable via pip and conda, with optional dependencies for extended functionality.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Pyteomics offers a collection of modules designed to facilitate common proteomics data analysis tasks, including calculation of basic physico-chemical properties of polypeptides such as mass, isotopic distribution, charge, and pI, as well as chromatographic retention time. The package supports access to proteomics data formats and provides modular functionality where core features are available through standard installation, while extended capabilities rely on optional dependencies: the mzMLb module requires h5py and hdf5plugin for accessing mzMLb data formats, the mass.unimod module depends on sqlalchemy for Unimod database access, and the proforma module uses psims for additional functionality. Pyteomics is distributed through multiple package managers including pip and Bioconda, supporting recent versions of Python 3.

## Research questions

- Can the core Pyteomics modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) be successfully installed and imported after pip installation from PyPI?
- What conditional dependencies must be installed to enable mzMLb format support in pyteomics?
- Does the pyteomics.mass.unimod module successfully initialize when sqlalchemy is installed as a conditional dependency?
- What is the mechanism by which the pyteomics.proforma module becomes available after installing the psims conditional dependency?
- Can Pyteomics be successfully installed via the Bioconda conda channel and do its core modules import without errors?

## Methods overview

Execute pip install command for Pyteomics package from PyPI in a Python 3 environment Sequentially import each of the five core modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) to verify module availability Capture and log import status (success or exception details) for each module Validation: confirm installation completes without error and all five core modules import successfully without ImportError or missing dependency exceptions Install Pyteomics with the mzMLb extra specifier to fetch h5py and hdf5plugin dependencies. Execute Python import statement for pyteomics.mzmlb module. Validation: confirm that the import completes without ImportError, indicating successful dependency resolution and module accessibility. Install the sqlalchemy package dependency using pip package manager. Import the pyteomics.mass.unimod module in a Python script or interactive session. Instantiate the Unimod database accessor object to confirm initialization without errors. Validation: Successful module import and object instantiation with no exceptions raised indicates correct conditional dependency wiring. Execute pip install command targeting psims package from PyPI Import pyteomics.proforma module in interactive Python or test script Verify module loads without ImportError or ModuleNotFoundError exceptions Inspect module for ProForma-related functions and classes to confirm parsing capability is present Validation: Confirm pip installation exits with status 0, import statement executes without exception, and ProForma parsing callables are discoverable via introspection (dir() or hasattr()) Install Pyteomics using conda from the Bioconda channel Launch Python and attempt to import pyteomics.mass Attempt to import pyteomics.pepxml and pyteomics.mzid Record version information and import success status Validation: All three core module imports execute without errors and version information is captured in the verification report

**Domain:** proteomics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics provides modules to facilitate calculation of mass and isotopic distribution of polypeptides. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics provides modules to facilitate calculation of charge and pI of polypeptides. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics provides modules to facilitate prediction of chromatographic retention time of polypeptides. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics supports recent versions of Python 3. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics can be installed using pip Python package manager. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics can be installed from Bioconda using conda. _[grounded: pyteomics_system]_
- **(finding)** On Arch Linux and related distros, Pyteomics can be installed from AUR. _[grounded: pyteomics_system]_
- **(finding)** NumPy is an optional dependency for Pyteomics. _[grounded: pyteomics_system]_
- **(finding)** Matplotlib is used by the pyteomics.pylab_aux module. _[grounded: pyteomics_system]_
- **(finding)** lxml is used by XML parsing modules and the pyteomics.mass.mass.Unimod class. _[grounded: pyteomics_system]_
- **(finding)** Pandas can be used with pyteomics.pepxml, pyteomics.tandem, pyteomics.mzid, and pyteomics.auxiliary modules. _[grounded: pyteomics_system]_
- **(finding)** SQLAlchemy is used by the pyteomics.mass.unimod module. _[grounded: pyteomics_system]_
- **(finding)** Pynumpress adds support for Numpress compression in mzML. _[grounded: tool_pynumpress]_
- **(finding)** h5py and optionally hdf5plugin are used by the pyteomics.mzmlb module. _[grounded: pyteomics_system]_
- **(finding)** psims is used by the pyteomics.proforma module. _[grounded: pyteomics_system]_
- **(finding)** spectrum_utils is optionally used for spectrum annotation in the pyteomics.pylab_aux module. _[grounded: pyteomics_system]_
- **(finding)** All dependencies in Pyteomics are optional. _[grounded: pyteomics_system]_
- **(finding)** Pyteomics can be installed with the XML extra to get dependencies needed to read XML format. _[grounded: pyteomics_system]_
- **(finding)** Currently provided extras for Pyteomics installation are XML, TDA, graphics, DF, Unimod, numpress, mzMLb, and proforma. _[grounded: pyteomics_system]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- All dependencies are optional

## Steps

### Step `task_001`
- Title: Reproduce the Pyteomics installation via pip and verify core module imports
- Task kind: `reproduction`
- Task: Install the Pyteomics package via pip from PyPI and verify successful import of five core modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) in a Python environment. Produce a validation report confirming installation success and module availability.
- Inputs:
  - Python 3 interpreter with pip package manager available
  - PyPI repository access (public package index)
- Expected outputs:
  - Installation validation report (text or JSON) confirming successful pip installation and listing import status (success/failure) for each of the five core modules
- Tools: Python, pip
- Landmark output files: pip_install_output.log, module_import_test.py
- Primary expected artifact: `installation_validation_report.txt`

### Step `task_002`
- Title: Reconstruct optional-dependency resolution for pyteomics.mzmlb using h5py and hdf5plugin
- Task kind: `component_reconstruction`
- Task: Install h5py and hdf5plugin optional dependencies for Pyteomics, then verify that mzMLb format support is available by successfully importing pyteomics.mzmlb.
- Inputs:
  - Pyteomics package (installed via pip with mzMLb extra)
- Expected outputs:
  - Confirmation that pyteomics.mzmlb module imports successfully without errors
- Tools: pip, Python, h5py, hdf5plugin

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct optional-dependency resolution for pyteomics.mass.unimod using sqlalchemy
- Task kind: `component_reconstruction`
- Task: Install sqlalchemy via pip, then import pyteomics.mass.unimod and verify the Unimod database accessor initializes without error.
- Inputs:
  - Python 3.x environment with pip package manager and git access to levitsky/pyteomics repository
- Expected outputs:
  - Successful import of pyteomics.mass.unimod module with no errors and instantiated Unimod accessor object ready for use
- Tools: Python, pip, sqlalchemy
- Landmark output files: pip_install.log, import_test.py

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct optional-dependency resolution for pyteomics.proforma using psims
- Task kind: `component_reconstruction`
- Task: Install the psims package via pip, then import pyteomics.proforma and verify that ProForma notation parsing functionality is available and operational.
- Inputs:
  - Python 3 environment with pip package manager
  - pip Python package manager installed
- Expected outputs:
  - Installation log confirming psims package installed successfully
  - Python import statement execution log confirming pyteomics.proforma module imported without error
  - Verification report confirming ProForma notation parsing functions are accessible in imported module
- Tools: Python, pip, psims
- Landmark output files: psims_install.log, import_test.py
- Primary expected artifact: `proforma_import_verification.log`

### Step `task_005`
- Depends on: `task_001`
- Title: Extend Pyteomics installation to Bioconda and verify conda-installed package imports
- Task kind: `extension`
- Task: Install Pyteomics via conda from the Bioconda channel and verify that core module imports (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid) succeed, confirming the conda distribution is functional.
- Inputs:
  - Access to conda package manager and Bioconda channel
- Expected outputs:
  - Installation verification report documenting successful conda installation and module import test results
- Tools: conda, Bioconda, Python
- Primary expected artifact: `conda_installation_verification.txt`

## Final expected outputs

- `Confirmation that pyteomics.mzmlb module imports successfully without errors` (type: file, tolerance: hash)
- `Successful import of pyteomics.mass.unimod module with no errors and instantiated Unimod accessor object ready for use` (type: file, tolerance: hash)
- `Installation log confirming psims package installed successfully` (type: file, tolerance: hash)
- `Python import statement execution log confirming pyteomics.proforma module imported without error` (type: file, tolerance: hash)
- `Verification report confirming ProForma notation parsing functions are accessible in imported module` (type: file, tolerance: hash)
- `Installation verification report documenting successful conda installation and module import test results` (type: file, tolerance: hash)

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
  "workflow_id": "coll_pyteomics_workflow",
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
    "Confirmation that pyteomics.mzmlb module imports successfully without errors": "<locator>",
    "Successful import of pyteomics.mass.unimod module with no errors and instantiated Unimod accessor object ready for use": "<locator>",
    "Installation log confirming psims package installed successfully": "<locator>",
    "Python import statement execution log confirming pyteomics.proforma module imported without error": "<locator>",
    "Verification report confirming ProForma notation parsing functions are accessible in imported module": "<locator>",
    "Installation verification report documenting successful conda installation and module import test results": "<locator>"
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

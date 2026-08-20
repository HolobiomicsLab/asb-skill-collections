---
name: entry-point-script-validation
description: Use when after installing a Python package or cloning its repository,
  to verify that the primary command-line interface is functional and discoverable
  before attempting analysis workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - annotate.py
  - argparse
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/bty080
  title: ChemDistiller
evidence_spans:
- ChemDistiller supports Python 2 and 3 (64-bit version recommended)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemdistiller_cq
    doi: 10.1093/bioinformatics/bty080
    title: ChemDistiller
  dedup_kept_from: coll_chemdistiller_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty080
  all_source_dois:
  - 10.1093/bioinformatics/bty080
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# entry-point-script-validation

## Summary

Verify that a Python package's command-line entry point script executes successfully and emits help documentation when invoked with the --help flag. This confirms the script is properly installed, importable, and has valid argument parsing configured.

## When to use

After installing a Python package or cloning its repository, to verify that the primary command-line interface is functional and discoverable before attempting analysis workflows. This is particularly important for high-throughput annotation engines like ChemDistiller where the entry point (annotate.py) serves as the gateway to all downstream functionality.

## When NOT to use

- When the package has already passed integration testing in a CI/CD pipeline and you are running production analyses; use this skill only once per fresh installation or environment.
- If your goal is to execute an actual analysis workflow (e.g., annotate spectra); use this skill first to validate the entry point, then move to full analysis with appropriate input data and parameters.
- When the entry point is known to require external resources (databases, SVMs) that are not yet downloaded; validate the script first, then acquire dependencies before running --test or analysis workflows.

## Inputs

- Python executable environment with package installed or repository cloned
- Command-line shell access
- Entry-point script file (e.g., annotate.py)

## Outputs

- Help text emitted to standard output
- Exit code 0 (success)
- Documentation of available command-line arguments and their descriptions

## How to apply

Locate the entry-point script (annotate.py) in the package installation directory or repository root. Invoke it via Python with the --help flag from the command line. Capture the standard output and validate that help text is emitted describing available command-line arguments and their purposes. The help output should document key parameters such as --ncpu (processor count), --delta_mz (m/z tolerance in ppm), --max_results (candidate compound limit), --test (test mode), and --svm_folder (custom SVM path). Success indicates the script can be imported without errors, argument parsing is configured, and the entry point is ready for actual analysis runs.

## Related tools

- **Python** (Interpreter for executing the entry-point script; supports both Python 2 and 3 (64-bit recommended)) — https://www.python.org
- **annotate.py** (Primary entry-point script for ChemDistiller command-line interface; orchestrates tandem MS spectra annotation) — https://github.com/Mrqeoqqt/chemdistiller
- **argparse** (Built-in Python module for command-line argument parsing that generates --help documentation)

## Examples

```
python annotate.py --help
```

## Evaluation signals

- Exit code is 0 (no errors or exceptions raised)
- Help text is emitted to stdout and includes documentation of all major arguments (--test, --ncpu, --delta_mz, --max_results, --svm_folder, input/output folder paths)
- Help text specifies default values and valid ranges (e.g., 'Default: 1' for --ncpu, 'Default: 10' for --max_results, ppm units for --delta_mz)
- No traceback or import errors appear in stderr; all dependencies (NumPy, SciPy, h5py) are successfully resolved
- Script can be invoked from any working directory without path errors, indicating proper package installation

## Limitations

- Help text validation does not confirm that the annotate.py script will successfully run an analysis; it only verifies the entry point is callable and argument parsing is configured. Use --test flag to validate end-to-end functionality.
- Help text may not reflect optional dependencies (RDKit for 2D structure image generation) or downloadable resources (external compound databases, SVM models from MediaFire); help validation passes even if these optional components are absent.
- On systems with multiple Python versions or conflicting package installations, the --help invocation may call an unexpected Python version or a different installation of ChemDistiller; ensure correct Python path and environment activation before validation.

## Evidence

- [other] Does the annotate.py entry-point script execute successfully and emit help documentation when invoked with the --help flag?: "Does the annotate.py entry-point script execute successfully and emit help documentation when invoked with the --help flag?"
- [readme] Try running __ChemDistiller__ from the command line: `python annotate.py --help` This should give you the list of currently available command line arguments.: "Try running __ChemDistiller__ from the command line: `python annotate.py --help` This should give you the list of currently available command line arguments."
- [other] Invoke annotate.py with the --help flag using Python. Capture and validate that the help output is emitted to standard output.: "Invoke annotate.py with the --help flag using Python. Capture and validate that the help output is emitted to standard output."
- [readme] _--ncpu_ tells how many processors to use in the multiprocessor/multicore environment. Default: 1, maximum for your PC will be shown in help screen: "_--ncpu_ tells how many processors to use in the multiprocessor/multicore environment. Default: 1, maximum for your PC will be shown in help screen"
- [readme] _--delta_mz_ - tolerance for the MS1 peak _m/z_ values when searching in the databases, _i.e._ candidates should be withing +/- _delta_mz_ from MS1 peak _m/z_ value (_delta_mz_ is in ppm): "_--delta_mz_ - tolerance for the MS1 peak _m/z_ values when searching in the databases, _i.e._ candidates should be withing +/- _delta_mz_ from MS1 peak _m/z_ value (_delta_mz_ is in ppm)"

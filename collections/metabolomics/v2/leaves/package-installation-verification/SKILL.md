---
name: package-installation-verification
description: Use when after installing ChemDistiller or similar Python-based command-line
  analysis packages, to confirm the package is properly installed in the Python environment
  and the primary entry point script is accessible and executable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Anaconda
  - ChemDistiller
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

# Verify Command-Line Entry Point Invocation with Help Flag

## Summary

Validates that a scientific Python package's command-line entry point script executes successfully and emits help documentation when invoked with the --help flag. This skill confirms the package installation is functional and the CLI interface is available before attempting analysis workflows.

## When to use

After installing ChemDistiller or similar Python-based command-line analysis packages, to confirm the package is properly installed in the Python environment and the primary entry point script is accessible and executable. Run this as an immediate post-installation sanity check before attempting to process input data.

## When NOT to use

- When the package has already been validated through prior successful analysis runs (redundant check).
- When diagnosing issues with input data processing or annotation results (this skill only verifies CLI availability, not analysis correctness).
- When the package does not expose a command-line interface or requires programmatic import only.

## Inputs

- Python package installation directory
- Entry-point script path (e.g., annotate.py)

## Outputs

- Help documentation text emitted to standard output
- Exit code 0 indicating successful script completion

## How to apply

Locate the main entry-point script (e.g., annotate.py) within the installed package directory. From that directory, invoke the script with Python and the --help flag. Capture and examine the standard output to verify that a non-empty help message describing available command-line arguments and options is emitted. The script should complete without ImportError, SyntaxError, or runtime exceptions. If help documentation is successfully printed to stdout, the installation and entry point are verified functional.

## Related tools

- **Python** (Interpreter for executing annotate.py and other package scripts; required to support ChemDistiller v0.1)
- **Anaconda** (Recommended Python distribution for managing dependencies (SciPy, NumPy, h5py); simplifies package environment setup) — https://www.anaconda.com/download/
- **ChemDistiller** (High-throughput tandem MS spectra annotation engine; annotate.py is the primary entry point being verified) — https://github.com/Mrqeoqqt/chemdistiller

## Examples

```
python annotate.py --help
```

## Evaluation signals

- Help output contains a list of command-line arguments (e.g., --help, --test, --ncpu, --delta_mz, --max_results) as described in the README.
- Script execution completes without raising ImportError, ModuleNotFoundError, or SyntaxError.
- Standard output is non-empty and contains human-readable documentation of available options.
- Exit code is 0, indicating successful termination.
- Help text is emitted within a reasonable time (< 5 seconds) with no hanging or timeout.

## Limitations

- This skill only verifies that the entry point is invocable and returns help; it does not validate that all dependencies (SciPy, NumPy, h5py, optional RDKit) are correctly installed or functional.
- Successful help output does not guarantee that actual annotation or analysis operations will work correctly or produce correct results.
- The skill assumes the entry-point script supports the --help flag; alternative help invocation patterns (e.g., -h, help subcommand) may not be detected by this method.

## Evidence

- [other] Locate the annotate.py script in the ChemDistiller package installation directory. Invoke annotate.py with the --help flag using Python.: "Locate the annotate.py script in the ChemDistiller package installation directory. Invoke annotate.py with the --help flag using Python."
- [other] The annotate.py script can be invoked from the command line with the --help flag to display available options and functionality.: "The annotate.py script can be invoked from the command line with the --help flag to display available options and functionality."
- [readme] Try running __ChemDistiller__ from the command line: python annotate.py --help. This should give you the list of currently available command line arguments.: "Try running __ChemDistiller__ from the command line: python annotate.py --help. This should give you the list of currently available command line arguments."
- [other] Capture and validate that the help output is emitted to standard output.: "Capture and validate that the help output is emitted to standard output."
- [readme] ChemDistiller supports Python 2 and 3 (64-bit version recommended) and requires _SciPy_, _NumPy_, _h5py_ libraries.: "ChemDistiller supports Python 2 and 3 (64-bit version recommended) and requires _SciPy_, _NumPy_, _h5py_ libraries."

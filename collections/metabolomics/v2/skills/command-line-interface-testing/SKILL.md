---
name: command-line-interface-testing
description: Use when after installing a Python package or before running a computational
  workflow for the first time, to verify that the CLI entry point is properly configured,
  the Python environment is correctly set up, and to discover available command-line
  arguments and their defaults (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - annotate.py
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# command-line-interface-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a Python-based command-line tool (such as ChemDistiller's annotate.py) executes correctly and emits expected help documentation when invoked with the --help flag. This skill confirms entry-point accessibility and documents available command-line arguments before running production analyses.

## When to use

After installing a Python package or before running a computational workflow for the first time, to verify that the CLI entry point is properly configured, the Python environment is correctly set up, and to discover available command-line arguments and their defaults (e.g., number of CPUs, MS1 m/z tolerance, output folder specification) that must be configured for your specific analysis.

## When NOT to use

- The script has already been validated by prior successful test runs; further --help invocations add no new diagnostic value.
- You are performing interactive Python development and need programmatic access to argument definitions; use introspection or argparse module inspection instead.
- The Python environment or package is not installed; resolve installation errors before attempting CLI testing.

## Inputs

- Python package installation directory path
- Shell environment with Python 2 or 3 (64-bit recommended)
- Required dependencies installed (SciPy, NumPy, h5py for ChemDistiller)

## Outputs

- Help documentation text printed to standard output
- List of available command-line arguments and their descriptions
- Default parameter values
- Usage examples or command syntax patterns

## How to apply

Navigate to the installed package directory (e.g., .../ChemDistiller/). Invoke the entry-point script with the --help flag using Python (e.g., `python annotate.py --help`). Capture and validate the standard output for the presence of documented command-line arguments, their descriptions, default values, and usage examples. Check that the help output is well-formed and lists all parameters relevant to your analysis (e.g., --ncpu, --delta_mz, --max_results for ChemDistiller). A successful invocation confirms the script's executable state, the Python environment's availability, and provides the reference documentation needed to construct valid production commands.

## Related tools

- **Python** (Interpreter for executing the annotate.py entry-point script and capturing CLI output)
- **annotate.py** (ChemDistiller command-line entry point being tested for proper invocation and help documentation emission) — https://github.com/Mrqeoqqt/chemdistiller

## Examples

```
python annotate.py --help
```

## Evaluation signals

- Exit code is 0 (success) when --help is invoked.
- Help text is emitted to standard output without error messages or exceptions.
- All expected command-line arguments (--ncpu, --delta_mz, --max_results, --test, --svm_folder, etc.) are documented in the output.
- Default values are explicitly stated for optional parameters (e.g., --ncpu default: 1, --max_results default: 10).
- Help output includes usage examples or a description of positional arguments such as Input_Spectra_folder and optional output_folder.

## Limitations

- The --help flag documents only the entry point's static argument schema; it does not validate runtime behavior, database connectivity, or file I/O against actual input spectra.
- Help output does not confirm that optional dependencies (RDKit for 2D structure image generation) are installed; a separate verification step is needed for optional features.
- Help invocation does not test the tool's ability to process actual spectra or produce correct annotations; use --test mode or a small validation dataset for end-to-end validation.

## Evidence

- [readme] Try running __ChemDistiller__ from the command line: `python annotate.py --help`. This should give you the list of currently available command line arguments.: "Try running __ChemDistiller__ from the command line: `python annotate.py --help`. This should give you the list of currently available command line arguments."
- [other] The annotate.py script can be invoked from the command line with the --help flag to display available options and functionality.: "The annotate.py script can be invoked from the command line with the --help flag to display available options and functionality."
- [other] Capture and validate that the help output is emitted to standard output.: "Capture and validate that the help output is emitted to standard output."
- [readme] ChemDistiller supports Python 2 and 3 (64-bit version recommended) and requires _SciPy_, _NumPy_, _h5py_ libraries.: "ChemDistiller supports Python 2 and 3 (64-bit version recommended) and requires _SciPy_, _NumPy_, _h5py_ libraries."
- [readme] maximum for your PC will be shown in help screen (see `python annotate.py --help`): "maximum for your PC will be shown in help screen (see `python annotate.py --help`)"

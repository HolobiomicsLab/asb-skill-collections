---
name: python-package-installation-and-dependency-management
description: Use when when setting up a new computational environment for tandem MS/MS spectrum clustering or other proteomics analysis, and you need to install a tool (like falcon) that depends on specific versions of auxiliary packages (like spectrum-utils==0.3.5).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - Python 3.8+
  - falcon-ms
  - spectrum-utils
  - pip
  techniques:
  - LC-MS
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
- _falcon_ requires Python 3.8+ and is available on the Linux and OSX platforms.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python Package Installation and Dependency Management

## Summary

Install and configure Python bioinformatics packages with pinned dependencies to ensure reproducible execution of mass spectrometry analysis workflows. This skill addresses version-specific compatibility constraints that arise when combining multiple scientific packages.

## When to use

When setting up a new computational environment for tandem MS/MS spectrum clustering or other proteomics analysis, and you need to install a tool (like falcon) that depends on specific versions of auxiliary packages (like spectrum-utils==0.3.5). Use this skill when the tool's documentation specifies exact version pins and platform constraints (e.g., Linux/OSX only, Python 3.8+ required).

## When NOT to use

- Environment already has incompatible package versions installed that cannot be reconciled (e.g., spectrum-utils 0.4.0 required by another tool)
- Platform is Windows (falcon is documented for Linux and OSX only)
- Python version is 3.7 or earlier (falcon requires Python 3.8+)

## Inputs

- Python 3.8+ runtime environment
- pip package manager
- Internet access to PyPI package repository
- Tool installation specification with pinned dependencies (e.g., from tool README or publication)

## Outputs

- Installed falcon-ms command-line tool
- Installed spectrum-utils==0.3.5 library
- Python environment with validated package versions

## How to apply

First, verify your Python version meets the minimum requirement (Python 3.8+) and that your operating system is supported (Linux or OSX). Then install the primary tool and its pinned dependencies together using pip, specifying exact versions as documented: `pip install falcon-ms spectrum-utils==0.3.5`. After installation, verify successful setup by invoking the tool's help or running it on a small test dataset to confirm no import errors or version conflicts occur. Version pinning is critical because spectrum-utils and falcon use feature hashing and nearest neighbor indexing that may break across minor version boundaries.

## Related tools

- **falcon-ms** (Primary spectrum clustering tool; installed via pip with pinned dependencies) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Auxiliary library for spectrum handling and preprocessing; pinned to version 0.3.5 for compatibility with falcon)
- **pip** (Package manager used to install falcon-ms and spectrum-utils with exact version specifications)

## Examples

```
pip install falcon-ms spectrum-utils==0.3.5
```

## Evaluation signals

- pip install command completes without errors and reports successful installation of both falcon-ms and spectrum-utils==0.3.5
- Running `falcon --help` or `falcon -h` produces help text without ImportError or version mismatch warnings
- Invoking falcon on a small test mzML/mzXML/MGF file runs to completion without exceptions
- Installed package versions match documentation requirements: `python -c 'import falcon; import spectrum_utils; print(spectrum_utils.__version__)'` returns '0.3.5'
- Cluster output files (*.csv) are generated with non-empty cluster assignments

## Limitations

- falcon is restricted to Linux and OSX platforms; Windows users cannot use this tool
- Older Python versions (< 3.8) are incompatible; users on legacy environments must upgrade
- spectrum-utils version 0.3.5 is a strict requirement; newer or older versions may introduce incompatibilities in feature hashing or vector construction steps
- pip requires internet connectivity to download packages from PyPI; offline environments need pre-cached wheels

## Evidence

- [readme] falcon requires Python 3.8+ and is available on the Linux and OSX platforms: "falcon requires Python 3.8+ and is available on the Linux and OSX platforms."
- [readme] pip installation with pinned spectrum-utils version: "You can easily install _falcon_ with pip:

    pip install falcon-ms spectrum-utils==0.3.5"
- [readme] Feature hashing and nearest neighbor indexing depend on spectrum-utils implementation details: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing. Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity"

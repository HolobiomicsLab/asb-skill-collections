---
name: sphinx-documentation-generation-and-api-reference-inclusion
description: Use when after implementing or modifying utility functions in a library subpackage (e.g., cooltools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - flake8
  - Sphinx
  - conda
  - Numpy style docstrings
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- We use [flake8](http://flake8.pycqa.org/en/latest/) to automatically lint the code
- We use [Numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html>) and [Sphinx](http://www.sphinx-doc.org/en/stable) to document this library
- we recommend using [conda](https://docs.conda.io/en/latest/miniconda.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# Sphinx Documentation Generation and API Reference Inclusion

## Summary

Build and validate Sphinx documentation for a Python library, ensuring that utility functions and their docstrings are correctly rendered in the generated API reference. This workflow integrates Numpy-style docstrings with Sphinx to produce HTML documentation that exposes the library's public API.

## When to use

After implementing or modifying utility functions in a library subpackage (e.g., cooltools.lib), use this skill to verify that the function is discoverable in the generated API documentation, that its docstring is properly formatted, and that the documentation build succeeds without warnings or errors.

## When NOT to use

- Function docstrings are written in a non-Numpy style (e.g., Google or reST style) without Sphinx extensions configured to parse them — the resulting API documentation will render incorrectly or be missing parameter details.
- The target function has not been added to the library's public API interface or __init__.py imports — Sphinx will not discover it for inclusion in the reference.
- The Sphinx configuration is not set up to parse Python docstrings (e.g., sphinx.ext.autodoc or sphinx.ext.napoleon is not enabled) — no docstring content will be extracted.

## Inputs

- Python source code files with function definitions in a library subpackage (e.g., cooltools/lib/adaptive_coarsegrain.py)
- Numpy-style docstrings attached to functions and classes
- Sphinx configuration file (conf.py)
- Documentation source files (e.g., docs/api.rst or equivalent)

## Outputs

- Generated HTML documentation (docs/_build/html/)
- API reference pages listing functions, classes, and their docstrings
- Build report indicating successful or failed Sphinx compilation
- Documentation validation report confirming function visibility and formatting

## How to apply

First, ensure that all utility functions use Numpy-style docstrings, which Sphinx can automatically parse and render into the API reference. Run `make docs` from the repository root to trigger the Sphinx build process, which will generate HTML documentation from the source code and docstrings. Inspect the generated HTML files in the build directory (typically `docs/_build/html/`) to confirm that the target function appears in the appropriate API section (e.g., cooltools.lib) with correctly formatted parameters, returns, and examples. If the function is missing or malformed, verify that (1) the module is correctly imported in the documentation configuration, (2) the docstring follows Numpy format conventions, and (3) no Sphinx warnings were emitted during the build. Re-run the build after corrections and re-inspect the HTML output.

## Related tools

- **Sphinx** (Documentation generator that parses Python source code and docstrings to produce HTML API reference pages) — http://www.sphinx-doc.org/en/stable
- **Numpy style docstrings** (Structured docstring format that Sphinx parses to extract parameter, return type, and example information for the API reference) — https://numpydoc.readthedocs.io/en/latest/format.html
- **Python** (Language in which the library code and docstrings are written)

## Examples

```
cd /path/to/cooltools && make docs && open docs/_build/html/api/cooltools.lib.html
```

## Evaluation signals

- Sphinx build completes without errors or warnings related to missing docstrings, malformed markup, or module import failures.
- The target function appears in the rendered HTML API reference under the correct subpackage path (e.g., cooltools.lib).
- The function's parameters, return type, and description are correctly formatted and readable in the generated HTML (Numpy docstring sections are properly parsed).
- Cross-references and internal links in the docstring (e.g., links to other functions or classes) resolve correctly in the HTML output.
- A test report or build log confirms that the function is discoverable via the library's import path (e.g., `from cooltools.lib import adaptive_coarsegrain`) and is listed in the API index.

## Limitations

- Sphinx documentation generation requires the source code repository to be available and correctly configured; it cannot be run on compiled binaries or incomplete installations.
- If docstrings are incomplete or poorly formatted, Sphinx may emit warnings but will still generate output; inspection of the HTML is necessary to catch quality issues.
- The skill does not guarantee that the API documentation is correct or complete — it only validates that the build succeeds and the function is included. Content accuracy must be verified manually.
- New or unstable functionality with an unstable API (as noted in the cooltools discussion) may be difficult to document in a stable way; Sphinx can still generate the reference, but the documentation may require frequent updates.

## Evidence

- [other] We use [Numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html>) and [Sphinx](http://www.sphinx-doc.org/en/stable) to document this library: "We use [Numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html>) and [Sphinx](http://www.sphinx-doc.org/en/stable) to document this library"
- [other] Build the Sphinx documentation using make docs and verify the function appears in the cooltools.lib API reference.: "Build the Sphinx documentation using make docs and verify the function appears in the cooltools.lib API reference."
- [other] To build the documentation: `make docs`: "To build the documentation: `make docs`"

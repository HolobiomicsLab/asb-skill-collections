---
name: documentation-generation-with-sphinx
description: 'Use when you have a Python package with docstrings and want to produce
  publicly browsable API documentation. Typical triggers: (1) package is being released
  or deployed; (2) you need to host documentation on ReadTheDocs or similar;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0092
  tools:
  - pip
  - Sphinx
  - sphinx-apidoc
  license_tier: open
derived_from:
- doi: 10.1038/s41587-025-02663-3
  title: DreaMS
evidence_spans:
- pip install -r requirements.txt
- sphinx-apidoc -o . ../dreams && make html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dreams_cq
    doi: 10.1038/s41587-025-02663-3
    title: DreaMS
  dedup_kept_from: coll_dreams_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-025-02663-3
  all_source_dois:
  - 10.1038/s41587-025-02663-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# documentation-generation-with-sphinx

## Summary

Generate browsable HTML API documentation from Python source code using Sphinx and sphinx-apidoc. This skill automates the extraction of docstrings and module structure into reStructuredText stubs, then compiles them into a static HTML documentation site.

## When to use

You have a Python package with docstrings and want to produce publicly browsable API documentation. Typical triggers: (1) package is being released or deployed; (2) you need to host documentation on ReadTheDocs or similar; (3) you want to generate API reference alongside hand-written guides (tutorials, methods). This is most useful when documentation source files (conf.py, index.rst, tutorials) already exist in a docs/ directory and you need to regenerate or update the API stubs from source code changes.

## When NOT to use

- Your package uses a different documentation framework (e.g., MkDocs, Jupyter Book, pdoc) — Sphinx is not universal.
- You need dynamic, runtime-generated documentation (e.g., API introspection on-the-fly) — Sphinx generates static HTML only.
- Your source code lacks docstrings or uses non-standard docstring formats that Sphinx autodoc does not parse correctly.

## Inputs

- Python source package directory (e.g., ../dreams)
- Sphinx configuration file (conf.py) with theme, extensions, and metadata
- requirements.txt listing Sphinx, sphinx-apidoc, and other build dependencies
- Hand-written reStructuredText files (index.rst, tutorials, guides) in docs/
- External tutorial or documentation folders to be linked (optional)

## Outputs

- Generated API documentation .rst stub files in docs/ (one per module/class hierarchy)
- Compiled HTML site in _build/html/ with index.html as entry point
- Cross-referenced API reference with searchable module and function indices
- Static files (CSS, JavaScript, images) for browser navigation

## How to apply

First, ensure Python dependencies (including Sphinx and sphinx-apidoc) are installed via pip install -r requirements.txt in the docs directory. Create a symbolic link from external tutorial folders into the docs directory (e.g., ln -s ../tutorials tutorials) so they appear in the build. Run sphinx-apidoc -o . ../dreams to scan the source module (e.g., ../dreams) and generate .rst stub files in the current docs directory; this introspects all modules, classes, and functions and writes their signatures and docstrings into reStructuredText format. Finally, execute make html to invoke Sphinx's build system, which processes all .rst files (both generated stubs and hand-written pages) and outputs a complete, cross-linked HTML site to _build/html/. The build is idempotent and will only rebuild changed files.

## Related tools

- **Sphinx** (Documentation generator; processes .rst source files and themes to produce HTML, PDF, or other outputs. Invoked via make html after sphinx-apidoc generates stubs.) — https://www.sphinx-doc.org/
- **sphinx-apidoc** (Scans Python source directory, introspects modules and docstrings, and auto-generates reStructuredText stub files for Sphinx to consume.) — https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
- **pip** (Package manager; installs Sphinx, sphinx-apidoc, and other build dependencies from requirements.txt.) — https://pip.pypa.io/

## Examples

```
cd docs && pip install -r requirements.txt && ln -s ../tutorials tutorials && sphinx-apidoc -o . ../dreams && make html && open _build/html/index.html
```

## Evaluation signals

- Verify that _build/html/index.html exists and opens in a browser without 404 errors.
- Check that the API reference index (e.g., _build/html/modules.html) lists all expected modules and classes from the source package.
- Confirm that cross-references between modules (e.g., class inheritance, function parameter types) are rendered as hyperlinks in the HTML.
- Validate that docstrings from source code appear verbatim in the corresponding .rst stubs and are rendered in the final HTML.
- Ensure that hand-written tutorial content (e.g., ../tutorials linked via ln -s) appears in the generated HTML navigation and is searchable.

## Limitations

- Sphinx autodoc relies on importable, syntactically correct Python code; broken imports or syntax errors in source modules will cause sphinx-apidoc to fail or skip those modules.
- Docstring extraction quality depends on compliance with a standard format (NumPy, Google, or reStructuredText); non-standard or missing docstrings will appear incomplete or blank in the HTML output.
- Symbolic links (ln -s) for tutorial folders may not be portable across operating systems or file systems; absolute paths in docs configuration may be more robust.
- Large source packages with hundreds of modules can produce very large HTML sites; consider filtering or excluding modules via sphinx-apidoc options (-e, --exclude-patterns) to keep builds fast.

## Evidence

- [other] Generate API documentation stubs by running sphinx-apidoc to scan the ../dreams module and output documentation source files.: "Generate API documentation stubs by running sphinx-apidoc to scan the ../dreams module and output documentation source files."
- [other] Build HTML documentation using make html, which processes Sphinx source files and generates the browsable output in _build/html/.: "Build HTML documentation using make html, which processes Sphinx source files and generates the browsable output in _build/html/."
- [methods] sphinx-apidoc -o . ../dreams && make html: "sphinx-apidoc -o . ../dreams && make html"
- [other] Install Python dependencies from requirements.txt using pip.: "Install Python dependencies from requirements.txt using pip."
- [other] Create a symbolic link from the tutorials folder to the current documentation directory using ln -s.: "Create a symbolic link from the tutorials folder to the current documentation directory using ln -s."

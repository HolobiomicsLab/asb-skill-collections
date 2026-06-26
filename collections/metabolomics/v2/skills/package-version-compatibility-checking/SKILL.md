---
name: package-version-compatibility-checking
description: Use when after creating a fresh conda environment from a pinned dependency
  specification (environment.yml or requirements.txt) and installing packages via
  conda and/or pip.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3473
  tools:
  - ENPKG
  - conda
  - pip
  - uv
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-version-compatibility-checking

## Summary

Verify that all declared Python packages in a conda or pip dependency manifest are installed at the correct versions in an isolated environment. This skill ensures reproducibility and prevents runtime errors caused by version mismatches or missing dependencies in computational workflows.

## When to use

After creating a fresh conda environment from a pinned dependency specification (environment.yml or requirements.txt) and installing packages via conda and/or pip. Apply this skill before running the workflow to detect incomplete installations, version conflicts, or stale environments that may cause silent failures during execution.

## When NOT to use

- Dependency manifest is not pinned or does not specify exact versions — use a dependency resolver (e.g., `pip freeze`, `conda export`) first to lock versions.
- Environment has already been validated in a prior workflow run and no new packages have been installed or updated.
- You are working in a shared/system-wide Python installation rather than an isolated environment — version conflicts with other users' installations are unavoidable.

## Inputs

- conda environment (active .venv or named environment)
- dependency manifest (environment.yml, requirements.txt, or pyproject.toml with pinned versions)
- optional: diagnostic/test script that imports core modules

## Outputs

- compatibility report (list of installed packages with versions)
- version mismatch log (if any declared packages differ from installed versions)
- test import results (pass/fail status for core modules)

## How to apply

Run `conda list` to enumerate all installed packages and their versions, then cross-reference against the original dependency manifest to confirm each declared package is present and matches the pinned version. For packages installed via pip, use `pip show <package_name>` to verify version numbers. Document any discrepancies (missing packages, version mismatches, or orphaned dependencies) as potential blockers. Finally, run a lightweight test import or diagnostic script that exercises core modules (e.g., importing ENPKG submodules) to confirm the environment is functional before launching the full workflow.

## Related tools

- **conda** (Environment manager and package installer; used to create isolated environments and verify installed package versions.) — https://docs.anaconda.com/free/anaconda/install/index.html
- **pip** (Python package installer; used to install or verify versions of packages managed outside conda.)
- **uv** (Modern dependency manager replacing conda/pip for ENPKG; syncs dependencies into isolated .venv and maintains lock files.) — https://docs.astral.sh/uv/latest/
- **ENPKG** (Target computational workflow; compatibility check ensures all ENPKG submodules and dependencies are correctly installed before execution.) — https://github.com/enpkg/enpkg_full

## Examples

```
conda list && pip show enpkg && python -c 'import enpkg.graph_builder; print("ENPKG environment validated")'
```

## Evaluation signals

- All packages declared in the dependency manifest appear in `conda list` or `pip list` output with matching version numbers.
- Running `pip show <package_name>` for each package returns a valid version string that matches the pinned specification.
- Test import script (e.g., `python -c 'import enpkg; import enpkg.graph_builder'`) completes without ImportError or version-related AttributeError.
- No orphaned or missing dependencies detected (no unmet 'requires' entries in `pip show` output).
- Diagnostic check confirms core ENPKG modules (e.g., graph_builder, taxo_enhancer) are accessible and functional.

## Limitations

- Does not detect transitive dependency version conflicts (e.g., package A requires B ≥1.0 but installed B is 0.9); use `pip check` or `conda-build check` for deeper validation.
- Platform-specific packages (e.g., numpy with BLAS variants) may have version strings that vary by OS; verify against the target platform's manifest.
- Pinned versions in the manifest may not be available for all Python versions or architectures; environment creation itself may fail before compatibility checking begins.
- Does not validate optional dependencies (extras) installed via pip `[package[extra]]` syntax unless explicitly listed in the manifest.

## Evidence

- [other] 3. Create a fresh conda environment using the declared specification and pinned dependency versions.: "Create a fresh conda environment using the declared specification and pinned dependency versions."
- [other] 5. Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show.: "Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show."
- [other] 6. Validate the environment by running a lightweight test import or diagnostic script that exercises core ENPKG modules.: "Validate the environment by running a lightweight test import or diagnostic script that exercises core ENPKG modules."
- [readme] We now rely on uv for dependency management. Install it if needed (see the uv docs for alternative methods): curl -LsSf https://astral.sh/uv/install.sh | sh: "We now rely on uv for dependency management. Install it if needed (see the uv docs for alternative methods)"
- [readme] uv sync creates a .venv in the project root. Activate it with: source .venv/bin/activate: "uv sync creates a .venv in the project root. Activate it with"

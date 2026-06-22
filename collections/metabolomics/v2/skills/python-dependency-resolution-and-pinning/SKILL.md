---
name: python-dependency-resolution-and-pinning
description: Use when when setting up a multi-stage bioinformatics workflow (e.g., ENPKG) that calls external tools (MZmine, Sirius, SPARQL engines) and depends on specific Python libraries; when reproducibility across team members or cloud infrastructure is required;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - ENPKG
  - uv
  - conda
  - pip
  - ENPKG full workflow
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
---

# Python Dependency Resolution and Pinning

## Summary

Establish a reproducible Python environment for a scientific workflow by declaring, resolving, and pinning all direct and transitive dependencies to exact versions. This ensures that the same code produces identical results across machines and time, critical for computational metabolomics and knowledge graph pipelines.

## When to use

When setting up a multi-stage bioinformatics workflow (e.g., ENPKG) that calls external tools (MZmine, Sirius, SPARQL engines) and depends on specific Python libraries; when reproducibility across team members or cloud infrastructure is required; when you need to version-lock a working environment before adding new samples or features.

## When NOT to use

- Environment is already provisioned and verified; use it directly instead of re-resolving.
- Workflow requires interactive dependency negotiation or manual version selection; use a package manager UI or manual editing instead.
- Dependencies are system-wide or pre-installed at the OS level; pin only the additional Python packages your workflow adds.

## Inputs

- Dependency manifest file (environment.yml, pyproject.toml, or requirements.txt)
- Git repository clone with setup documentation
- Lock file (uv.lock or pinned requirements.txt, if pre-generated)

## Outputs

- Isolated Python environment (.venv or conda env) with all dependencies installed at exact versions
- Lock file recording all transitive dependency versions (uv.lock or requirements.lock)
- Verification log showing package names, versions, and import status

## How to apply

Declare dependencies in a manifest file (environment.yml for conda, pyproject.toml + uv.lock for uv, or requirements.txt for pip). Use a lock file (uv.lock or pinned requirements.txt) to fix all transitive dependencies to exact versions, not ranges. Create a fresh isolated environment (conda env create or uv sync) from the manifest in a clean directory. Install all packages at the pinned versions using conda or uv. Verify environment integrity by listing installed packages (conda list, pip show) and running diagnostic imports of core modules (e.g., import enpkg) to confirm all declared packages are present at correct versions. Optionally run a lightweight test script to exercise key functionality before full workflow execution.

## Related tools

- **uv** (Modern Python package manager used to resolve and lock dependencies; creates isolated .venv and reads pyproject.toml) — https://docs.astral.sh/uv/latest/
- **conda** (Package manager for resolving conda dependencies from environment.yml; creates isolated conda environments) — https://docs.anaconda.com/free/anaconda/install/index.html
- **pip** (Package installer for Python packages specified in requirements.txt; used alongside conda for mixed dependency trees) — https://pip.pypa.io/
- **ENPKG full workflow** (Target workflow whose dependencies are resolved and pinned; uses uv for dependency management) — https://github.com/enpkg/enpkg_full

## Examples

```
uv sync && source .venv/bin/activate && python -c "import enpkg; print('Environment ready')"
```

## Evaluation signals

- All packages listed in manifest appear in conda list or pip show output with exact pinned versions
- Lock file (uv.lock or requirements.lock) is generated with all transitive dependency versions explicitly recorded
- Diagnostic import script (e.g., import enpkg, import networkx) runs without ImportError or version mismatch warnings
- Environment can be recreated identically on a clean machine using the lock file
- No conflicting version constraints or unmet dependencies reported during environment creation (conda env create or uv sync)

## Limitations

- System-level dependencies (C libraries, Java, SIRIUS binary) must be installed separately; Python dependency pinning does not cover OS-level requirements.
- Lock files are platform-specific; uv.lock and pip wheels may differ between Linux, macOS, and Windows; regenerate lock on each target OS if needed.
- Transitive dependencies of large workflows (e.g., ENPKG with Sirius, MZmine integration) can be numerous and slow to resolve; use uv or pip-tools for efficiency.
- Pinned versions may become outdated or insecure over time; periodic review and refresh of lock files is recommended for long-running projects.

## Evidence

- [other] Locate and parse the conda environment specification file (environment.yml or requirements.txt) at the repository root or setup documentation.: "Locate and parse the conda environment specification file (environment.yml or requirements.txt)"
- [other] Create a fresh conda environment using the declared specification and pinned dependency versions.: "Create a fresh conda environment using the declared specification and pinned dependency versions"
- [other] Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show.: "Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show"
- [readme] We now rely on uv for dependency management. Install it if needed (see the uv docs for alternative methods): curl -LsSf https://astral.sh/uv/install.sh | sh. With uv installed, sync the project dependencies into an isolated .venv: uv sync: "We now rely on uv for dependency management. Install it if needed... With uv installed, sync the project dependencies into an isolated .venv: uv sync"
- [readme] You will need to have Git and Anaconda (or Miniconda) installed.: "You will need to have Git and Anaconda (or Miniconda) installed."

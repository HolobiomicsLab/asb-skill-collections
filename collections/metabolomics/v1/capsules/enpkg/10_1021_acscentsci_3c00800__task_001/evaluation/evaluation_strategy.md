# Evaluation Strategy

## Direct Checks

- Verify file exists: environment.yml or conda specification file in github:enpkg__enpkg_full root or docs/ directory
- Verify file exists: requirements.txt or setup.py or pyproject.toml in github:enpkg__enpkg_full root
- Verify file_format_is: conda environment specification (YAML or JSON) parses without syntax errors
- Verify script_runs: conda env create -f [environment_spec] completes without unresolved dependency conflicts
- Verify script_runs: pip install -r [requirements_file] completes without version resolution errors
- Verify file_exists: environment lock file (conda-lock.yml, poetry.lock, or Pipfile.lock) documenting pinned transitive dependencies
- Verify contains_substring: environment specification includes Python version constraint (e.g., 'python=3.x' or 'python>=3.x')
- Verify contains_substring: environment specification lists all top-level dependencies named in ENPKG documentation or source imports

## Expert Review

- Assess completeness: do all declared dependencies in the specification match actual package imports in enpkg_full source code (no missing transitive deps that would cause import failures)?
- Assess reproducibility: will the specified environment (with pinned versions where present) rebuild consistently across different systems and installation dates?
- Assess documentation alignment: do installation instructions in README or docs match the environment specification provided (no contradictions or outdated step descriptions)?

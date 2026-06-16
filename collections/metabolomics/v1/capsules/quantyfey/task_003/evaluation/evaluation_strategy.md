# Evaluation Strategy

## Direct Checks

- verify file exists: modified app configuration file (e.g., app.R, ui.R, server.R, or shiny.yaml) in the output artifact
- verify file_format_is: configuration file is valid R syntax or YAML, script_runs without parse errors
- verify script_runs: modified Shiny application launches successfully on Linux or macOS without dependency resolution errors
- verify contains_substring: documentation or configuration identifies at least one platform-specific dependency that was modified or resolved
- verify output_matches_reference: launched application displays the same core UI and data visualization components as the Windows baseline (robust to minor rendering differences across platforms)

## Expert Review

- assess whether all identified platform-specific dependencies (e.g., file paths, system calls, graphics libraries, R package binaries) have been correctly diagnosed and addressed for Linux/macOS compatibility
- evaluate whether the modified configuration preserves the original application's intended functionality for intensity drift correction and mass spectrometry quantification workflows
- review whether the cross-platform solution is maintainable and whether configuration changes are properly documented for future deployment

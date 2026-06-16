# Evaluation Strategy

## Direct Checks

- verify file exists at https://github.com/sdrogers/nplinker (GitHub repository root)
- verify file exists at http://doi.org/10.5281/zenodo.4680579 (Zenodo release archive)
- script_runs: clone NPLinker repository and execute setup.py or equivalent package installation without errors
- file_format_is: NPLinker source tree contains nplinker/ module directory with __init__.py
- file_exists: NPLinker repository contains documented integration point for antiSMASH output (file path or module name)
- file_exists: NPLinker repository contains documented integration point for BiG-SCAPE output (file path or module name)
- file_exists: NPLinker repository contains documented integration point for GNPS output (file path or module name)
- contains_substring: NPLinker codebase or documentation references 'GCF' and 'MF' (molecular feature) as object types
- contains_substring: NPLinker codebase or documentation describes strain correlation scoring function or method
- contains_substring: NPLinker codebase or documentation describes IOKR (Input-Output Kernel Regression) scoring function or integration
- file_exists: NPLinker source tree contains implementation of combined scoring function (strain correlation + IOKR)
- output_matches_reference: run NPLinker on a small test dataset (subset of Crüsemann or similar public paired omics data) and verify output table structure contains columns for GCF identifier, spectrum identifier, strain correlation score, IOKR score, and combined rank
- file_format_is: NPLinker primary output artifact is a table (CSV, TSV, JSON, or database format) with filterable ranked link records
- field_present: output link table contains at least the following fields: GCF_ID, spectrum_ID, strain_correlation_score, IOKR_score, combined_score, rank
- script_runs: NPLinker orchestration layer accepts antiSMASH BGC annotations (GenBank or JSON format) without format conversion errors
- script_runs: NPLinker orchestration layer accepts BiG-SCAPE GCF clustering output without format conversion errors
- script_runs: NPLinker orchestration layer accepts GNPS MS/MS spectrum library metadata without format conversion errors
- value_in_range: combined scoring function applies ℓp-norm with p=0.5 and sign-adjusted absolute values (robust to parameter choices in combining function)
- contains_substring: NPLinker documentation or code comments explain the control loop: input → GCF-MF hypothetical link enumeration → score application → filtering → ranked output
- file_exists: NPLinker repository includes example or demo configuration file showing how to chain antiSMASH → BiG-SCAPE → GNPS inputs

## Expert Review

- Verify that the NPLinker orchestration logic correctly maps antiSMASH-detected BGCs into BiG-SCAPE GCF clusters (no misalignment of identifiers or lost BGCs)
- Verify that strain correlation score computation accurately reflects the presence/absence of shared strains between GCF and MF (biological correctness of the metric)
- Verify that IOKR scoring function is correctly applied: molecular fingerprints are derived from structures, kernel is applied to spectra, predictions are bounded in expected range
- Verify that the combined scoring function (ℓp-norm with p=0.5) preserves directionality and relative ranking of both component scores
- Verify that the output ranked link table is filterable by percentile threshold (e.g., 90th percentile) and that filtered results match the proportions and p-values reported in Table 2 of the article
- Verify that NPLinker handles edge cases correctly: BGCs with no MIBiG homology (should be excluded from IOKR scoring), spectra with insufficient peaks (should be denoised or excluded), multiple GCFs mapping to the same BGC (antiSMASH edge case mentioned in results)
- Verify that the control loop terminates gracefully and produces interpretable error messages when inputs are malformed or incomplete

# Evaluation Strategy

## Direct Checks

- verify file exists in repository samgoldman97/mist-cf containing subformula assignment implementation (e.g., Python module or configuration file naming or documenting internal subformula protocol)
- verify that subformula assignment component does NOT invoke SIRIUS fragmentation tree computation (scan codebase for absence of SIRIUS API calls or tree construction in subformula assignment pathway)
- verify that held-out test set exists in repository or linked deposit (Zenodo/GitHub) with annotated MS/MS spectra and reference per-peak subformula labels
- file_format_is: output predictions file (CSV, JSON, or TSV) with at least columns: [peak_m_z, predicted_subformula, reference_subformula] or equivalent
- row_count_equals or file_exists: number of predictions in output must match number of peaks in held-out test set (verify row count or file completeness)
- script_runs: end-to-end inference script on held-out spectra completes without error and produces per-peak subformula predictions

## Expert Review

- chemical validity: predicted subformulas for each MS/MS peak are chemically plausible (e.g., no impossible charge states, mass balance consistent with precursor formula and fragmentation logic)
- assignment accuracy: per-peak subformula predictions match or closely align with reference annotations on held-out set (requires domain judgment of acceptable deviation or match criteria)
- independence from SIRIUS: verification that subformula assignment uses learned embeddings or energy-based scoring (per SCARF/transformer approach) rather than pre-computed fragmentation trees

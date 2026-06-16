# Evaluation Strategy

## Direct Checks

- verify that input metabolomics dataset file exists in glasgowcompbio/PALS repository or is a publicly deposited reference dataset with accession or DOI
- verify that PALS software can be installed and executed from github:glasgowcompbio/PALS source
- verify that noise injection script produces output files with Gaussian noise applied at each specified level (e.g., SNR = 10, 5, 2, 1) — file_exists and file_format_is CSV or HDF5
- verify that peak removal simulation script executes without error and produces degraded datasets with 5%, 10%, 20%, 50% random peak removal — script_runs and output_matches_reference structure
- verify that pathway rank-order stability metric (e.g., Spearman correlation or Kendall τ of top-N pathway scores) is computed for each noise/peak-removal condition relative to clean-data baseline — value_in_range [0, 1]
- verify that stability scores decrease monotonically or show expected degradation pattern as noise and peak removal increase — robust to parameter choices within reasonable noise and removal ranges
- verify that final summary table contains columns: [noise_level, peak_removal_percent, top_N_pathways_corr, rank_stability_score, pathway_count_affected] with numeric values populated — field_present and row_count_equals ≥ number of noise/removal combinations tested

## Expert Review

- validate that the choice of noise model (Gaussian with specified SNR levels) and peak-removal mechanism (random selection) are appropriate for assessing metabolomics data robustness; confirm alignment with experimental noise profiles in LC-MS/MS data
- assess whether the rank-order stability metric (e.g., Spearman ρ or Kendall τ) and the choice of top-N pathways (N=5, 10, etc.) capture clinically or biologically meaningful shifts in pathway prioritization
- review whether observed stability patterns (e.g., PALS outperforming ORA/GSEA under noise, as claimed in literature) are replicated; interpret any deviations and assess whether they support or contradict the robustness finding

# SciTask Card: Reproduce Monte-Carlo Dropout uncertainty estimation and per-bin RMSE improvement

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:16:21.763690+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_ms2deepscore`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1186/s13321-021-00558-4`
- GitHub: `matchms/ms2deepscore`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `artificial-intelligence`, `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `deep-learning`, `machine-learning`, `spectral-library-matching`, `tandem-ms`, `metabolite-identification`, `transfer-learning`

## Research Question
Does applying Monte-Carlo Dropout ensemble filtering (IQR < 0.025) to MS2DeepScore predictions significantly reduce root mean squared error across different Tanimoto score ranges, particularly in low (< 0.4) and high (> 0.8) bins?

## Connected Finding
Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7).

## Task Description
Apply Monte-Carlo Dropout ensemble inference (N=10 predictions per spectrum pair) to the 3,601 test-set spectra, compute per-Tanimoto-bin RMSE before and after filtering predictions with IQR < 0.025, and verify the reported RMSE reduction in low (< 0.4) and high (> 0.7) Tanimoto bins matches published results.

## Inputs
- Trained MS2DeepScore base network model (200-dimensional embedding layer) and test-set spectrum pair labels from Zenodo deposit zenodo.org/record/4699356
- Test set of 3,601 spectra with 500 unique InChIKeys and corresponding reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits)

## Expected Outputs
- Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) before uncertainty filtering, showing RMSE values for each bin across all 6,485,401 test pairs
- Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) after IQR < 0.025 filtering, showing RMSE reduction and pair count per bin
- Summary comparison figure or table showing RMSE values and improvements (unfiltered vs. IQR-filtered) for low (< 0.4) and high (> 0.7) Tanimoto bins, matching reported findings

## Expected Output File

- `rmse_comparison_iqr_filtered.csv`

## Landmark Outputs

- `mc_dropout_predictions.csv`
- `rmse_by_tanimoto_bin_unfiltered.csv`
- `rmse_by_tanimoto_bin_iqr_filtered.csv`

## Tools
- matchms
- MS2DeepScore
- Python
- Monte-Carlo Dropout
- RDKit
- scikit-learn

## Skills
- monte-carlo-dropout-uncertainty-quantification
- mass-spectral-similarity-binning-and-stratification
- root-mean-squared-error-computation-by-bin
- interquartile-range-filtering-for-outlier-rejection
- deep-learning-model-inference-and-ensemble-prediction
- siamese-network-embedding-generation

## Workflow Description
1. Load the trained MS2DeepScore model and test-set spectrum embeddings (3,601 spectra) from the published Zenodo deposit. 2. Run Monte-Carlo Dropout inference with dropout enabled (N=10 forward passes per spectrum pair) on all 6,485,401 unique test-set spectrum pairs to generate 10 structural similarity predictions per pair. 3. For each pair, compute the median prediction and interquartile range (IQR) from the 10 predictions. 4. Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). 5. Compute RMSE (root mean squared error) for each bin using all predictions. 6. Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE. 7. Calculate the RMSE difference (improvement) between unfiltered and IQR-filtered predictions for each Tanimoto bin, with particular focus on bins < 0.4 and > 0.7. 8. Compare computed RMSE values and reduction patterns against the reported figures.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `ms2deepscore.pdf` | main_article | True |

## Missing Information
- No specification of the number of Monte-Carlo Dropout iterations or ensemble size for uncertainty quantification
- No definition of IQR filtering threshold or justification for the specific cutoff value used
- No quantitative RMSE results reported in discussion; claims about accuracy improvement lack specific numerical values
- No information on which specific Tanimoto score bins (e.g., low < 0.4, high > 0.7) show the most improvement

## Domain Knowledge
- Monte-Carlo Dropout at inference time requires dropout layers to remain active (not in inference/eval mode) and multiple forward passes (N=10 here) to generate a distribution of predictions from which median and IQR are derived.
- Interquartile range (IQR) reflects the spread between the 25th and 75th percentiles of the 10 predictions; IQR < 0.025 indicates high confidence/low uncertainty in the predicted structural similarity score.
- Tanimoto similarity score based on RDKit Daylight fingerprints (2048 bits) ranges from 0 (completely dissimilar) to 1 (identical); the reference ground truth is computed from molecular fingerprints, not spectral data.
- RMSE computation per Tanimoto bin requires stratifying all 6.48M spectrum pairs by their reference (ground-truth) Tanimoto bin, then measuring prediction error within each stratum; low and high bins (< 0.4 and > 0.7) are particularly important for detecting structural similarity.
- IQR-based filtering trades off precision (lower RMSE from removing uncertain predictions) against recall (fewer pairs retained); the reported drop from ~0.15 RMSE to ~0.1 is achieved by retaining only high-confidence (low-IQR) predictions.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does applying Monte-Carlo Dropout ensemble filtering (IQR < 0.025) to MS2DeepScore predictions significantly reduce root mean squared error across different Tanimoto score ranges, particularly in low (< 0.4) and high (> 0.8) bins?: 'For instance, all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11 (Fig. 7A). It is important to note,'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7).: 'all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11 (Fig. 7A). The RMSE drops most significantly in'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Trained MS2DeepScore base network model (200-dimensional embedding layer) and test-set spectrum pair labels from Zenodo deposit zenodo.org/record/4699356: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Test set of 3,601 spectra with 500 unique InChIKeys and corresponding reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits): 'For the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) before uncertainty filtering, showing RMSE values for each bin across all 6,485,401 test pairs: 'MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Per-Tanimoto-bin RMSE table (10 bins from 0.0–1.0) after IQR < 0.025 filtering, showing RMSE reduction and pair count per bin: 'filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Summary comparison figure or table showing RMSE values and improvements (unfiltered vs. IQR-filtered) for low (< 0.4) and high (> 0.7) Tanimoto bins, matching reported findings: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] MS2DeepScore: 'Our MS2DeepScore Python library offers two types of data generators'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Monte-Carlo Dropout: 'To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn: 'Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No specification of the number of Monte-Carlo Dropout iterations or ensemble size for uncertainty quantification: 'by applying Monte-Carlo Dropout to sample from random model variations'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No definition of IQR filtering threshold or justification for the specific cutoff value used: 'by merging predicted scores of spectra belonging to the same compound pair or by applying Monte-Carlo Dropout'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No quantitative RMSE results reported in discussion; claims about accuracy improvement lack specific numerical values: 'the accuracy of the predictions can be improved notably by using various ensemble learning techniques'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] No information on which specific Tanimoto score bins (e.g., low < 0.4, high > 0.7) show the most improvement: 'The accuracy of the predictions can be improved notably by using various ensemble learning techniques'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that deposited model file (zenodo.org/record/4699356) is accessible and contains trained weights
- file_exists: verify that GitHub repository (https://github.com/matchms/ms2deepscore) contains Monte-Carlo Dropout implementation and inference scripts
- script_runs: execute Monte-Carlo Dropout ensemble inference (N=100 predictions) on test set (3601 spectra) using deposited model and verify script completes without error
- output_matches_reference: verify computed per-Tanimoto-bin RMSE values (without IQR filtering) match reported values from article figures/tables to within parameter-sensitive tolerance (robust to minor numerical precision variations across platforms)
- output_matches_reference: verify computed per-Tanimoto-bin RMSE values (with IQR < 0.025 filtering) match reported values from article figures/tables to within parameter-sensitive tolerance
- value_in_range: RMSE reduction in low Tanimoto bin (< 0.4) after IQR < 0.025 filtering is positive and exceeds baseline noise floor (no canonical answer; multiple defensible filtering thresholds exist)
- value_in_range: RMSE reduction in high Tanimoto bin (> 0.7) after IQR < 0.025 filtering is positive and exceeds baseline noise floor (no canonical answer; multiple defensible filtering thresholds exist)

### Expert Review
- Assess whether reported RMSE drops are statistically significant and meaningful given test set size and score distribution across Tanimoto bins
- Evaluate whether IQR < 0.025 filtering threshold is appropriate and whether alternative uncertainty quantiles would be more defensible
- Verify that Monte-Carlo Dropout with N=100 samples provides adequate convergence of uncertainty estimates and whether reported ensemble size is justified
- Judge whether per-bin RMSE metrics are computed correctly (e.g., bin boundaries, sample counts per bin, treatment of boundary cases)
- Review whether the reported RMSE improvements are practically meaningful for metabolomic workflows (e.g., impact on spectral matching accuracy, network analysis quality)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load trained MS2DeepScore model (base network + Siamese head) and test-set spectrum pairs with reference Tanimoto labels.
2. Run Monte-Carlo Dropout inference with N=10 forward passes per spectrum pair, generating 10 predictions and computing median and IQR.
3. Stratify predictions into 10 equally-sized Tanimoto bins (0.0–0.1, 0.1–0.2, …, 0.9–1.0) by reference Tanimoto score.
4. Compute per-bin RMSE for unfiltered predictions and separately for IQR-filtered predictions (retain IQR < 0.025 only).
5. Calculate RMSE reduction (improvement) by bin, with focus on low (< 0.4) and high (> 0.7) Tanimoto regions.
6. Validation: verify that reported RMSE drop from ~0.15 (unfiltered) to ~0.1 (IQR < 0.025 filtered) is reproduced in published figures.
7. References: source article (DOI: 10.1186/s13321-021-00558-4)

## Workflow Ports

**Inputs:**

- `trained_model` — Trained MS2DeepScore model with base network and Siamese head ← `task_001/rmse_no_filter`
- `test_spectra_pairs` — Test set spectrum pairs (3,601 spectra, 6.48M pairs) with reference Tanimoto labels

**Outputs:**

- `rmse_unfiltered` — RMSE per Tanimoto bin (0.0–1.0) without IQR filtering
- `rmse_iqr_filtered` — RMSE per Tanimoto bin after IQR < 0.025 filtering
- `rmse_comparison` — RMSE improvement table and figure (low/high Tanimoto bins)

**Used:** `urn:asb:port:task_001/rmse_no_filter`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

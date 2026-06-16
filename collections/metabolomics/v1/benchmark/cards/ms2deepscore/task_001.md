# SciTask Card: Reproduce MS2DeepScore Tanimoto score prediction RMSE on held-out test set

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:16:21.763690+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_ms2deepscore`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `data-analysis`
- DOI: `10.1186/s13321-021-00558-4`
- GitHub: `matchms/ms2deepscore`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `artificial-intelligence`, `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `deep-learning`, `machine-learning`, `spectral-library-matching`, `tandem-ms`, `metabolite-identification`, `transfer-learning`

## Research Question
Does the MS2DeepScore model trained on RDKit Daylight fingerprints achieve the reported prediction accuracy (RMSE ~0.15 without uncertainty filtering, ~0.10 with IQR < 0.025 filtering) when run on the held-out test set of 3,601 spectra from 500 unique compounds?

## Connected Finding
MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds to remove high-uncertainty predictions.

## Task Description
Load the trained MS2DeepScore Siamese network model and the reserved 3,601-spectrum test set (500 unique compounds), run inference on all 6,485,401 unique spectrum pairs to predict Tanimoto scores, compute RMSE against ground-truth structural similarity labels, and reproduce reported performance (~0.15 RMSE without uncertainty filtering, ~0.10 RMSE with IQR < 0.025 filtering).

## Inputs
- Pre-trained MS2DeepScore model (Daylight Tanimoto condition) with Siamese network weights and architecture specification
- Reserved test set: 3,601 preprocessed MS/MS spectra and corresponding ground-truth Tanimoto structural similarity labels (15×15 matrix subset for 500 unique InChIKeys)
- GNPS-derived cleaned dataset with metadata including InChIKey, SMILES/InChI, and peak information for test subset

## Expected Outputs
- RMSE value (single float) comparing predicted Tanimoto scores to ground-truth for full test set (no uncertainty filter), reported as ~0.15
- RMSE value (single float) comparing predicted Tanimoto scores to ground-truth after filtering with IQR < 0.025 threshold, reported as ~0.10
- CSV table with columns: spectrum_pair_id, spectrum_1_idx, spectrum_2_idx, predicted_tanimoto, ground_truth_tanimoto, prediction_uncertainty_iqr, passed_iqr_filter

## Expected Output File

- `test_set_predictions.csv`

## Landmark Outputs

- `preprocessed_test_spectra.pkl`
- `ground_truth_tanimoto_matrix.csv`
- `monte_carlo_predictions.csv`
- `rmse_metrics.json`

## Tools
- MS2DeepScore
- RDKit
- Python
- matchms
- Monte-Carlo Dropout

## Skills
- spectral-similarity-prediction-neural-networks
- siamese-network-inference-spectrum-pairs
- monte-carlo-dropout-uncertainty-quantification
- tanimoto-fingerprint-ground-truth-computation
- spectrum-preprocessing-binning-normalization
- root-mean-squared-error-regression-evaluation

## Workflow Description
1. Load the pre-trained MS2DeepScore model weights and base network architecture (200-dimensional embedding layer, 2×500-node hidden layers, L1/L2 regularization, batch normalization, dropout rate 0.2) from the Zenodo deposit. 2. Load the test set spectrum data and corresponding ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints, 2048 bits) for all 3,601 test spectra with 500 unique InChIKeys. 3. Prepare test spectra by applying the same preprocessing: remove peaks with intensity < 0.1% of maximum, keep top 1,000 peaks, apply square-root transformation to intensities, and bin into 10,000 equally-sized bins (10–1000 m/z). 4. Perform Siamese network inference on all unique spectrum pairs (n=6,485,401), computing cosine similarity between paired 200-dimensional embeddings to yield predicted Tanimoto scores. 5. Calculate root mean squared error (RMSE) between predicted and ground-truth scores for the full test set (no filter). 6. Apply Monte-Carlo Dropout uncertainty quantification (N=10 forward passes with dropout enabled, compute interquartile range on predictions) and filter predictions to retain only pairs with IQR < 0.025, then recalculate RMSE on the filtered subset.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `ms2deepscore.pdf` | main_article | True |

## Missing Information
- No specification of how many spectrum pairs (total cardinality) were evaluated or whether all possible pairs from 3,601 spectra were tested
- No details on inference time, computational requirements (CPU/GPU), or memory footprint needed to run the full test set inference
- No confidence intervals, standard deviations, or statistical significance tests reported for the RMSE values (0.15 and 0.10)
- No discussion of failure cases, edge cases where the model performs poorly, or structural similarity ranges where prediction accuracy degrades

## Domain Knowledge
- Tanimoto scores on RDKit Daylight fingerprints (2048 bits) serve as ground-truth structural similarity labels; scores range from 0 (no structural similarity) to 1 (identical structure).
- Siamese networks learn embeddings by computing cosine similarity between paired input embeddings; the model outputs a single scalar structural similarity prediction per spectrum pair.
- Monte-Carlo Dropout ensemble inference (N=10 forward passes with dropout enabled on all but the first layer) quantifies prediction uncertainty; interquartile range (IQR) of the 10 predictions estimates confidence.
- MS/MS spectra are binned into 10,000 equally-sized bins (10–1000 m/z) with square-root-transformed peak intensities; this binned vector is the input to the Siamese base network.
- RMSE ~0.15 without uncertainty filtering reflects prediction error across all spectrum pairs; stricter IQR thresholds (e.g., IQR < 0.025) reduce RMSE by filtering high-uncertainty predictions, improving to ~0.10.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: CSV table with columns: spectrum_pair_id, spectrum_1_idx, spectrum_2_idx, predicted_tanimoto, ground_truth_tanimoto, prediction_uncertainty_iqr, passed_iqr_filter.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does the MS2DeepScore model trained on RDKit Daylight fingerprints achieve the reported prediction accuracy (RMSE ~0.15 without uncertainty filtering, ~0.10 with IQR < 0.025 filtering) when run on the held-out test set of 3,601 spectra from 500 unique compounds?: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds to remove high-uncertainty predictions.: 'all predictions within IQR < 0.025—which will discard about 75% of the scores—will result in a drop of the average RMSE from about 0.17 to about 0.11'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained MS2DeepScore model (Daylight Tanimoto condition) with Siamese network weights and architecture specification: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo: https:// zenodo. org/ record/ 46993 56'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Reserved test set: 3,601 preprocessed MS/MS spectra and corresponding ground-truth Tanimoto structural similarity labels (15×15 matrix subset for 500 unique InChIKeys): 'For the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs).'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] GNPS-derived cleaned dataset with metadata including InChIKey, SMILES/InChI, and peak information for test subset: 'The full cleaned dataset (210,407 spectra, 184,698 annotated with InChIKey and SMILES and/or InChI) can be found on zenodo: https:// zenodo. org/ record/ 46993 00'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] RMSE value (single float) comparing predicted Tanimoto scores to ground-truth for full test set (no uncertainty filter), reported as ~0.15: 'we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] RMSE value (single float) comparing predicted Tanimoto scores to ground-truth after filtering with IQR < 0.025 threshold, reported as ~0.10: 'and down to 0.1 with stronger restrictions on model uncertainty'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] CSV table with columns: spectrum_pair_id, spectrum_1_idx, spectrum_2_idx, predicted_tanimoto, ground_truth_tanimoto, prediction_uncertainty_iqr, passed_iqr_filter: 'At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were created from an ensemble of these networks with dropout enabled. This resulted in a'
- `ev_009` from `agent2_synthesis` (agent2_traced): [abstract] MS2DeepScore: 'MS2DeepScore to predict structural similarity scores for spe'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] matchms: 'Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names'
- `ev_013` from `agent2_synthesis` (agent2_traced): [abstract] Monte-Carlo Dropout: 'different model varieties through Monte-Carlo Dropout is u'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No specification of how many spectrum pairs (total cardinality) were evaluated or whether all possible pairs from 3,601 spectra were tested: 'MS2DeepScore is very fast and scalable. We conclude that this makes MS2DeepScore a powerful novel tool for running large scale comparisons and analy­ses'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No details on inference time, computational requirements (CPU/GPU), or memory footprint needed to run the full test set inference: 'MS2DeepScore is very fast and scalable.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] No confidence intervals, standard deviations, or statistical significance tests reported for the RMSE values (0.15 and 0.10): 'a root mean squared error of about 0.15'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] No discussion of failure cases, edge cases where the model performs poorly, or structural similarity ranges where prediction accuracy degrades: 'MS2DeepScore can infer structural similarities between mass spectra with high overall precision, without requiring any additional meta­data or library data.'

## Evaluation Strategy
### Direct Checks
- file_exists: verify trained MS2DeepScore model (Daylight Tanimoto condition) is accessible from zenodo.org/record/4699356
- file_exists: verify test set containing 3,601 spectra / 500 compounds is accessible from GNPS-derived deposit or supplementary data
- script_runs: execute inference pipeline on all spectrum pairs from the 3,601-spectra test set using the loaded model
- output_matches_reference: RMSE value computed on full test set (no uncertainty filter) is approximately 0.15 (robust to ±0.02 tolerance)
- output_matches_reference: RMSE value computed on test set filtered by interquartile range (IQR < 0.025) is approximately 0.10 (robust to ±0.02 tolerance)
- value_in_range: verify number of spectrum pairs in inference output equals the expected cardinality (3,601 × 3,600 / 2 for unique pairs, or as specified in methods)
- contains_substring: verify inferred predictions are continuous numeric values (Tanimoto scores) in range [0, 1]

### Expert Review
- Confirm that the reported RMSE ~0.15 (no filter) and ~0.10 (IQR < 0.025 filter) are consistent with the numerical outputs and reflect appropriate ground-truth Tanimoto score computation from RDKit Daylight fingerprints
- Assess whether the test set composition (500 unique compounds, 3,601 spectra) and data split strategy ensure no leakage from training data and represent a fair held-out evaluation
- Evaluate whether the uncertainty filtering approach (IQR < 0.025 threshold) is defensible and whether the reported improvement from ~0.15 to ~0.10 RMSE is substantial given the filtering mechanism

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load pre-trained Siamese network model with 200-dimensional embedding layer and cosine similarity head from Zenodo deposit.
2. Preprocess test spectra: filter peaks (<0.1% intensity, limit to 1,000 peaks), apply square-root transformation, bin into 10,000 equally-sized bins (10–1000 m/z).
3. Run Siamese network inference on all 6,485,401 unique test spectrum pairs; each pair yields a predicted structural similarity score (cosine of embedding pair).
4. Quantify uncertainty via Monte-Carlo Dropout: execute N=10 forward passes with dropout enabled; compute median and interquartile range (IQR) of 10 predictions per pair.
5. Compute RMSE between predicted and ground-truth Tanimoto scores for full test set (no filter) and for filtered subset (IQR < 0.025).
6. Validation: verify RMSE without filter ≈ 0.15 and RMSE with IQR < 0.025 filter ≈ 0.10, matching reported performance in methods and results sections.
7. References: source article (DOI: 10.1186/s13321-021-00558-4)

## Workflow Ports

**Inputs:**

- `trained_model` — Pre-trained MS2DeepScore model (Daylight Tanimoto condition)
- `test_spectra` — Test set MS/MS spectra and ground-truth Tanimoto labels
- `metadata` — GNPS cleaned metadata (InChIKey, SMILES/InChI for test compounds)

**Outputs:**

- `rmse_no_filter` — RMSE without uncertainty filtering (~0.15)
- `rmse_iqr_filter` — RMSE with IQR < 0.025 filter (~0.10)
- `predictions_table` — Full prediction results table with uncertainty estimates

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

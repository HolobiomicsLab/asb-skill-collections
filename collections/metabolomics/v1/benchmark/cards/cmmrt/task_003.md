# SciTask Card: Reconstruct the Bayesian meta-learning RT projection module

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:49:30.022773+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_cmmrt/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`, `model-training`
- DOI: `10.1186/s13321-022-00613-8`
- GitHub: `constantino-garcia/cmmrt`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `retention-time-prediction`, `machine-learning`, `metabolite-identification`, `database-annotation`, `deep-learning`

## Research Question
How does the Bayesian meta-learning approach enable retention time projection between different chromatographic methods using minimal calibration data?

## Connected Finding
A Bayesian meta-learning approach projects retention times between chromatographic methods using as few as 10 calibration molecules while maintaining competitive error rates relative to previous methods.

## Task Description
Implement a Bayesian meta-learning projection mechanism that maps retention times from an external chromatographic method onto the SMRT-trained DNN's latent space using as few as 10 calibration molecules, and generate projected RT predictions for a held-out test set.

## Inputs
- Pre-trained DNN model checkpoint trained on METLIN SMRT dataset (80,038 experimental retention times)
- Calibration set: 10 molecules with measured retention times from external chromatographic method and corresponding structures
- Held-out test set: molecules with experimental retention times from external chromatographic method and structures

## Expected Outputs
- Projected RT predictions for test set molecules (CSV table with molecule identifiers, predicted RTs, reference RTs)
- Performance metrics: mean absolute error and median absolute error comparing predicted vs. reference RTs
- Fitted Bayesian meta-learning projection model (serialized model object)

## Expected Output File

- `projected_rt_predictions.csv`

## Landmark Outputs

- `calibration_fingerprints.csv`
- `test_fingerprints.csv`
- `calibration_latent_features.npy`
- `test_latent_features.npy`
- `projection_model.pkl`
- `test_set_predictions.csv`

## Tools
- alvaDesc

## Skills
- retention-time-projection-across-chromatographic-methods
- bayesian-meta-learning-model-fitting
- molecular-fingerprint-generation-and-representation
- deep-neural-network-latent-space-mapping
- regression-error-metrics-calculation

## Workflow Description
1. Load the pre-trained DNN model trained on METLIN SMRT data (80,038 experimental RTs) using fingerprint features (MACCS166, Extended Connectivity, Path Fingerprints). 2. Generate molecular fingerprints for the 10 calibration molecules and the held-out test set using alvaDesc with the same fingerprint schemes (MACCS166, Extended Connectivity, Path Fingerprints). 3. Extract feature representations from the penultimate layer of the pre-trained DNN for calibration and test molecules. 4. Fit a Bayesian meta-learning projection model to learn the mapping from the external chromatographic method's space to the DNN's latent feature space using only the 10 calibration molecules and their known retention times. 5. Apply the learned projection to transform test set molecules into the DNN's latent space. 6. Generate RT predictions for the test set by passing projected representations through the DNN's final regression layer, comparing against reference RTs to assess mean and median absolute errors.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog found.
- The article text does not specify the exact location (section, table, figure, or supplementary file) where the Bayesian meta-learning projection mechanism is described, the algorithm pseudocode, or reference results for the held-out test set predictions.
- The discussion section does not report numerical results (mean/median absolute errors) for the meta-learning projection on a held-out test set that could serve as a reference for validation.

## Domain Knowledge
- Fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) are superior features to molecular descriptors alone for retention time prediction in this context.
- Bayesian meta-learning enables effective parameter estimation from minimal calibration data (10 molecules) by leveraging prior knowledge from the pre-trained DNN trained on 80,038 reference RTs.
- Retention time projection must map between the external chromatographic method's RT space and the latent feature representation learned by the SMRT-trained DNN.
- Competitive error rates are benchmarked against the base DNN's median absolute error of 17.2 ± 0.9 s and mean absolute error of 39.2 ± 1.2 s achieved on its native training distribution.
- The pre-trained DNN employs heavy regularization with cosine annealing warm restarts and stochastic weight averaging to prevent overfitting and ensure robust generalization.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Fitted Bayesian meta-learning projection model (serialized model object).

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the Bayesian meta-learning approach enable retention time projection between different chromatographic methods using minimal calibration data?: 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] A Bayesian meta-learning approach projects retention times between chromatographic methods using as few as 10 calibration molecules while maintaining competitive error rates relative to previous methods.: 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] Pre-trained DNN model checkpoint trained on METLIN SMRT dataset (80,038 experimental retention times): 'trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] Calibration set: 10 molecules with measured retention times from external chromatographic method and corresponding structures: 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Held-out test set: molecules with experimental retention times from external chromatographic method and structures: 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Projected RT predictions for test set molecules (CSV table with molecule identifiers, predicted RTs, reference RTs): 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Performance metrics: mean absolute error and median absolute error comparing predicted vs. reference RTs: 'achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Fitted Bayesian meta-learning projection model (serialized model object): 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] alvaDesc: '5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: '_No changelog found._'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] The article text does not specify the exact location (section, table, figure, or supplementary file) where the Bayesian meta-learning projection mechanism is described, the algorithm pseudocode, or reference results for the held-out test set predictions.: '(absent — flagged as missing)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] The discussion section does not report numerical results (mean/median absolute errors) for the meta-learning projection on a held-out test set that could serve as a reference for validation.: '(absent — flagged as missing)'

## Evaluation Strategy
### Direct Checks
- verify that repository constantino-garcia/cmmrt contains implementation of Bayesian meta-learning projection mechanism
- verify that implementation accepts as input: (i) a pre-trained DNN model trained on METLIN SMRT dataset, (ii) calibration molecules (≥10), and (iii) a held-out test set with known retention times
- verify that code produces projected RT predictions (numeric values in seconds) for the held-out test set as named output artifact
- verify that projection mechanism maps retention times from external chromatographic method onto METLIN-trained DNN's feature space
- script_runs: execute meta-learning projection pipeline with minimum 10 calibration molecules and report absence of runtime errors
- value_in_range: reported mean absolute error on held-out test set is within the range cited in article (39.2±1.2 s or better), or expert review explains variance
- file_exists: verify presence of trained model weights or checkpoint file for METLIN-trained DNN in repository

### Expert Review
- assess whether Bayesian formulation of meta-learning projection is mathematically sound and implements posterior inference over projection parameters
- evaluate whether projected RT predictions on held-out test set are competitive with baseline methods (as claimed in article abstract)
- review whether the implementation correctly handles the low-data regime (10 calibration molecules) and produces credible uncertainty estimates
- assess reproducibility: compare projected RT predictions against reference results reported in article or supplementary material if available

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** light
- **Commercial software:** alvaDesc
- **Open-source alternatives:**
  - alvaDesc → RDKit

## Methodology Summary
1. Load the pre-trained DNN model trained on METLIN SMRT data with 80,038 experimental retention times
2. Generate molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration and test molecules using alvaDesc
3. Extract latent feature representations from the pre-trained DNN for calibration and test sets
4. Fit a Bayesian meta-learning projection model using 10 calibration molecules to map external chromatographic RT space to DNN latent space
5. Generate RT predictions for test set by projecting through learned mapping and DNN regression head
6. Validation: calculate mean and median absolute errors on test predictions, confirming competitive error rates against base DNN benchmarks (MAE 39.2±1.2 s, MedAE 17.2±0.9 s)
7. References: source article (DOI: 10.1186/s13321-022-00613-8)

## Workflow Ports

**Inputs:**

- `pretrained_dnn_model` — Pre-trained DNN model trained on METLIN SMRT (80,038 RTs) ← `task_001/trained_dnn_model`
- `calibration_molecules` — 10 calibration molecules with external chromatographic RTs
- `test_molecules` — Held-out test set with external chromatographic RTs

**Outputs:**

- `projected_rt_predictions` — Projected RT predictions for test set
- `performance_metrics` — Mean and median absolute error metrics
- `fitted_projection_model` — Fitted Bayesian meta-learning projection model

**Used:** `urn:asb:port:task_001/trained_dnn_model`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:constantino-garcia__cmmrt`
- **Synthesized at:** 2026-06-15T12:55:29+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

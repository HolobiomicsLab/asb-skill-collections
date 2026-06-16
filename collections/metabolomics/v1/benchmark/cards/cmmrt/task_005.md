# SciTask Card: Extend DNN+meta-learned projections integration for probabilistic metabolite annotation scoring

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:49:30.022773+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_cmmrt/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `modeling`, `information-extraction`
- DOI: `10.1186/s13321-022-00613-8`
- GitHub: `constantino-garcia/cmmrt`
- Input from: `task_003`

## Classification

- Task kind: `extension`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `retention-time-prediction`, `machine-learning`, `metabolite-identification`, `database-annotation`, `deep-learning`

## Research Question
How can DNN-predicted retention times be combined with meta-learned chromatographic projections to generate probabilistic likelihood scores for ranking candidate metabolite annotations?

## Connected Finding
A Bayesian meta-learning approach enables retention time projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches.

## Task Description
Combine DNN-predicted retention times with meta-learned chromatographic projections to generate RT-based likelihood scores for candidate metabolite annotations. Produce a ranked candidate list with RT probability scores for a query spectrum.

## Inputs
- Query spectrum (m/z, intensity pairs) and neutral mass of unknown metabolite
- Candidate metabolite structures (SMILES or InChI) from reference database (e.g., METLIN)
- Trained DNN regression model (checkpoint) for retention time prediction
- Bayesian meta-learning model for RT projection between chromatographic methods
- Calibration molecules (≥10) with known RTs in both reference and target chromatographic methods

## Expected Outputs
- Ranked candidate list with RT probability scores (CSV or TSV table: candidate_id, molecular_formula, predicted_rt, rt_score, rank)

## Expected Output File

- `ranked_candidates_rt_scores.csv`

## Landmark Outputs

- `candidate_fingerprints.csv`
- `predicted_rts.csv`
- `projected_rts.csv`
- `rt_likelihood_scores.csv`

## Tools
- alvaDesc

## Skills
- molecular-descriptor-fingerprint-generation
- retention-time-prediction-deep-neural-network
- bayesian-meta-learning-chromatographic-projection
- metabolite-candidate-ranking-likelihood-scoring
- uncertainty-quantification-rt-prediction

## Workflow Description
1. Load query spectrum and candidate metabolite structures (SMILES or InChI). 2. Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for all candidates using alvaDesc. 3. Apply the trained DNN model (regularized with cosine annealing warm restarts and stochastic weight averaging) to predict retention times for each candidate, yielding point estimates and uncertainty bounds (mean absolute error 39.2±1.2 s). 4. Use the Bayesian meta-learning approach to project predicted RTs from reference chromatographic method to the target chromatographic method (with ≥10 calibration molecules). 5. Convert projected RTs and prediction uncertainties into RT-based likelihood scores (probability density or normalized Gaussian kernel). 6. Rank candidates by likelihood score in descending order and output as ranked candidate list with associated RT probability scores.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, updates, or modifications to the CMM-RT system implementation
- No specific description of the example query spectrum input format or content used to demonstrate the ranked candidate list generation
- No explicit documentation of the output format or schema for the ranked candidate list with RT probability scores
- No reference to a deposited or reproducible example demonstrating end-to-end execution of the RT-based annotation workflow

## Domain Knowledge
- The DNN model achieves mean absolute error of 39.2±1.2 s and median absolute error of 17.2±0.9 s on independent test sets; these error bounds define the prediction uncertainty for likelihood score calculation.
- Fingerprints (MACCS166, Extended Connectivity, Path) outperform descriptors alone for RT prediction, so feature inputs should prioritize fingerprint representations.
- Bayesian meta-learning enables RT projection between different chromatographic methods (e.g., RP-LC to HILIC) with as few as 10 calibration molecules, making cross-method annotation feasible.
- RT likelihood scores must account for both point-estimate prediction error and systematic offset between reference and target chromatographic systems; the meta-learned projection corrects the latter.
- Ranked candidate lists should be thresholded by RT score to filter implausible structures; metabolites with projected RTs far outside measured experimental range (>3 SD from prediction) should be deprioritized.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] How can DNN-predicted retention times be combined with meta-learned chromatographic projections to generate probabilistic likelihood scores for ranking candidate metabolite annotations?: 'We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotati'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] A Bayesian meta-learning approach enables retention time projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches.: 'A novel Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules while still obtaining competitive error rates compared with previous approaches.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Query spectrum (m/z, intensity pairs) and neutral mass of unknown metabolite: 'example query spectrum'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Candidate metabolite structures (SMILES or InChI) from reference database (e.g., METLIN): 'candidate metabolite annotations'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Trained DNN regression model (checkpoint) for retention time prediction: 'heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Bayesian meta-learning model for RT projection between chromatographic methods: 'Bayesian meta-learning approach is proposed for RT projection between CMs from as few as 10 molecules'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Calibration molecules (≥10) with known RTs in both reference and target chromatographic methods: 'from as few as 10 molecules while still obtaining competitive error rates'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Ranked candidate list with RT probability scores (CSV or TSV table: candidate_id, molecular_formula, predicted_rt, rt_score, rank): 'producing a ranked candidate list with associated RT probability scores'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] alvaDesc: '5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, updates, or modifications to the CMM-RT system implementation: '_No changelog found._'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No specific description of the example query spectrum input format or content used to demonstrate the ranked candidate list generation: 'No relevant span in provided section text'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No explicit documentation of the output format or schema for the ranked candidate list with RT probability scores: 'No relevant span in provided section text'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No reference to a deposited or reproducible example demonstrating end-to-end execution of the RT-based annotation workflow: 'No relevant span in provided section text'

## Evaluation Strategy
### Direct Checks
- verify that github:constantino-garcia/cmmrt repository is accessible and contains source code for the CMM-RT system
- verify that the repository contains implementation of DNN-based retention time prediction model
- verify that the repository contains implementation of Bayesian meta-learning projection module
- verify that the repository contains a working example or script that accepts a query mass spectrum and outputs a ranked candidate list
- verify that expected_outputs[0] (ranked candidate list with RT probability scores) is a structured file (JSON, CSV, or TSV format) with at least three columns: candidate_identifier, RT_probability_score, and rank
- verify that RT probability scores in expected_outputs[0] are numeric values in range [0.0, 1.0]
- verify script_runs: that a computational agent can execute the CMM-RT annotation pipeline with the example query spectrum without errors
- verify that output_matches_reference: the number and order of candidate annotations in the ranked list are consistent with the meta-learned projection methodology (no canonical answer for exact ordering, but output must be deterministic and defensible)

### Expert Review
- assess whether the RT probability scores assigned to each candidate metabolite annotation are mathematically sound and properly calibrated from the DNN predictions and meta-learned projections
- assess whether the ranked candidate list reflects appropriate integration of DNN-predicted retention times with meta-learned chromatographic method projections
- assess whether the RT probability scores are meaningful for discriminating true metabolite identities from incorrect candidates in the example query spectrum
- assess whether the example query spectrum and its ranked results are representative of typical metabolomics use cases

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
1. Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path) for each candidate structure using alvaDesc.
2. Apply trained DNN regression model to predict retention times and extract prediction uncertainty from model outputs.
3. Use Bayesian meta-learning to project predicted RTs from reference chromatographic method to target method using calibration molecules (≥10).
4. Convert projected RTs and uncertainties into normalized RT-based likelihood scores (probability density function).
5. Rank candidates by RT likelihood score and output ranked list with scores.
6. Validation: Confirm ranked list contains all input candidates, RT scores sum to or normalize appropriately, and no candidate has missing or NaN likelihood value.
7. References: source article (DOI: 10.1186/s13321-022-00613-8)

## Workflow Ports

**Inputs:**

- `query_spectrum` — Query spectrum (m/z, intensity pairs) and neutral mass ← `task_003/projected_rt_predictions`
- `candidate_structures` — Candidate metabolite structures (SMILES or InChI)
- `dnn_model` — Trained DNN retention time prediction model
- `meta_learning_model` — Bayesian meta-learning model for RT projection
- `calibration_molecules` — Calibration molecules with RTs in reference and target chromatographic methods

**Outputs:**

- `ranked_candidates` — Ranked candidate list with RT probability scores

**Used:** `urn:asb:port:task_003/projected_rt_predictions`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:constantino-garcia__cmmrt`
- **Synthesized at:** 2026-06-15T12:55:29+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

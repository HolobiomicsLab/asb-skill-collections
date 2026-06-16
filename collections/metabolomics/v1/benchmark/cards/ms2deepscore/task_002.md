# SciTask Card: Reproduce precision–recall comparison of MS2DeepScore vs. Spec2Vec and Modified Cosine baselines

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T07:16:21.763690+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_ms2deepscore`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `benchmark-evaluation`, `visualization`, `data-analysis`
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
Does MS2DeepScore outperform classical spectral similarity measures (modified Cosine) and the unsupervised Spec2Vec method in retrieving chemically related compound pairs from mass spectral datasets?

## Connected Finding
MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.

## Task Description
Compute precision and recall curves for MS2DeepScore, Spec2Vec, and classical spectral similarity on the reserved test set (3,601 spectra, 6,485,401 unique pairs) by varying Tanimoto score thresholds and measuring retrieval performance for structurally related compounds; save the precision/recall plot reproducing Figure 4.

## Inputs
- Pretrained MS2DeepScore Siamese network model weights and architecture
- Test set spectra (3,601 spectra of 500 unique InChIKeys) with binned peak vectors and structural annotations
- Ground-truth Tanimoto scores matrix (500 × 500) computed from RDKit Daylight fingerprints
- Spec2Vec and classical spectral similarity baseline predictions on test set pairs

## Expected Outputs
- Precision-recall curve plot comparing MS2DeepScore, Spec2Vec, and classical spectral similarity methods across Tanimoto score thresholds

## Expected Output File

- `precision_recall_curve.png`

## Landmark Outputs

- `embeddings_test_set.npy`
- `ms2deepscore_predictions.csv`
- `tanimoto_ground_truth.csv`
- `precision_recall_metrics.csv`

## Tools
- matchms
- MS2DeepScore
- RDKit
- Python
- scikit-learn

## Skills
- spectral-embedding-generation-from-neural-networks
- compound-structural-similarity-retrieval
- precision-recall-curve-generation-for-ranking-tasks
- tanimoto-score-threshold-optimization
- deep-learning-model-inference-on-test-sets

## Workflow Description
1. Load the reserved test set (3,601 spectra) and the pretrained MS2DeepScore base network from the Zenodo deposit. 2. Compute 200-dimensional spectral embeddings for all test spectra using the MS2DeepScore base network. 3. Generate all possible spectrum pairs from the test set (6,485,401 unique pairs) and compute MS2DeepScore structural similarity predictions using cosine distance between embeddings. 4. Retrieve ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints with 2048 bits) for each test pair using the 14-character InChIKey structural labels. 5. For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected pairs) and recall (high Tanimoto pairs in selection / all high Tanimoto pairs), where 'high Tanimoto' is defined as Tanimoto ≥ threshold. 6. Plot precision versus recall for all three methods on a single figure and save as precision_recall_curve.png.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `ms2deepscore.pdf` | main_article | True |

## Missing Information
- No specification of which two baseline scoring methods are used for comparison in precision-recall curves or their exact parameter configurations
- No reporting of computational time or inference speed benchmarks comparing MS2DeepScore to baseline methods on the test set
- No discussion of how the Tanimoto threshold parameter affects precision-recall trade-offs or guidance on threshold selection for practical use
- No information on model ensemble method details (how many Monte-Carlo Dropout samples, how scores are aggregated, uncertainty filtering thresholds) used during precision-recall evaluation

## Domain Knowledge
- Precision in this context is the fraction of predicted high-similarity pairs that have ground-truth Tanimoto ≥ threshold; recall is the fraction of all ground-truth high-similarity pairs that are retrieved by the method.
- Tanimoto similarity on binary fingerprints ranges from 0 (completely dissimilar) to 1 (identical); RDKit Daylight fingerprints with 2048 bits are the canonical ground truth in this study.
- A left-skewed distribution of Tanimoto scores (most pairs dissimilar) means performance at high thresholds is constrained by fewer positive examples; precision-recall curves are more informative than ROC curves for imbalanced retrieval tasks.
- The Siamese network architecture produces cosine similarity scores directly from spectral embeddings without explicit fingerprint computation, enabling fast inference on large test sets (6.5M pairs).
- Varying the threshold from 0 to near 1 traces the trade-off between selecting more candidate pairs (higher recall, lower precision) and stricter selectivity (lower recall, higher precision).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does MS2DeepScore outperform classical spectral similarity measures (modified Cosine) and the unsupervised Spec2Vec method in retrieving chemically related compound pairs from mass spectral datasets?: 'MS2DeepScore clearly outperforms both classical measures (two forms of the modified Cosine) as well as the unsupervised spectral similarity measure Spec2Vec, with respect to identifying high Tanimoto'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: 'MS2DeepScore gives notably better precision/recall combination over the entire range, followed by Spec2Vec and only then modified Cosine'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Pretrained MS2DeepScore Siamese network model weights and architecture: 'The fully trained model used to create Fig. 2, 4, 5, 7, 8 can be downloaded from zenodo: https:// zenodo. org/ record/ 46993 56'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Test set spectra (3,601 spectra of 500 unique InChIKeys) with binned peak vectors and structural annotations: 'for the final evaluation on the reserved test set, we used all possible spectrum pairs between the 3601 for the test set (n = 6,485,401 unique spectrum pairs)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Ground-truth Tanimoto scores matrix (500 × 500) computed from RDKit Daylight fingerprints: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities. For every unique 14-character InChIKey the most common InChI was selected (if different'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Spec2Vec and classical spectral similarity baseline predictions on test set pairs: 'The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold were among a subset of all pairs for which the spectral similarity score was >'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Precision-recall curve plot comparing MS2DeepScore, Spec2Vec, and classical spectral similarity methods across Tanimoto score thresholds: 'The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold were among a subset of all pairs for which the spectral similarity score was >'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] MS2DeepScore: 'we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] RDKit: 'we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Our MS2DeepScore Python library offers two types of data generators'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] scikit-learn: 'Using the t-SNE [28] implementation from scikit-learn [29]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No specification of which two baseline scoring methods are used for comparison in precision-recall curves or their exact parameter configurations: 'MS2DeepScore can generally be used to complement -or replace- common currently used spectral similarity measures'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No reporting of computational time or inference speed benchmarks comparing MS2DeepScore to baseline methods on the test set: 'MS2DeepScore is very fast and scalable.'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No discussion of how the Tanimoto threshold parameter affects precision-recall trade-offs or guidance on threshold selection for practical use: 'We demonstrate that the accuracy of the predictions can be improved notably by using various ensemble learning techniques'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No information on model ensemble method details (how many Monte-Carlo Dropout samples, how scores are aggregated, uncertainty filtering thresholds) used during precision-recall evaluation: 'by applying Monte-Carlo Dropout to sample from random model variations'

## Evaluation Strategy
### Direct Checks
- verify file exists at zenodo.org/record/4699356 (fully trained model)
- verify file exists at https://github.com/matchms/ms2deepscore (source code repository)
- verify test set file exists and contains 3601 spectra with structural similarity labels
- script_runs: execute precision-recall computation script with test set and model inputs without errors
- output_matches_reference: precision and recall curves (any of the following formats: PNG/PDF figure, CSV table with threshold, precision, recall columns, or pickle serialized curve object) computed from test set match reported results in article figures within ±0.02 absolute difference in precision/recall values across thresholds
- value_in_range: computed RMSE of MS2DeepScore predictions on test set is between 0.13 and 0.20 (as stated in results section)
- contains_substring: generated precision-recall output documentation clearly labels which scoring method (MS2DeepScore vs. baseline 1 vs. baseline 2) produced each curve

### Expert Review
- assess whether the three scoring methods (MS2DeepScore, baseline 1, baseline 2) are identically configured and fairly compared (same hyperparameters, same data splits, same evaluation protocol)
- judge whether precision and recall curves demonstrate that MS2DeepScore 'clearly outperforms' baselines as claimed—evaluate the magnitude of difference and statistical significance (no canonical answer: depends on domain expectations for 'clear' outperformance)
- evaluate whether the test set (3601 spectra, 500 unique InChIKeys) is sufficiently representative and independent from training/validation to support the claimed generalization
- assess appropriateness of Tanimoto ≥ threshold definition as the ground-truth label for 'structural similarity' and whether this aligns with chemical domain expectations

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load pretrained MS2DeepScore base network and test set spectra (3,601 spectra, 500 unique InChIKeys).
2. Compute 200-dimensional spectral embeddings for all test spectra via forward pass through the base network.
3. Generate all 6,485,401 unique spectrum pair combinations and compute pairwise cosine similarity scores (MS2DeepScore predictions).
4. Retrieve ground-truth Tanimoto scores from RDKit Daylight fingerprints (2048 bits) for the same pairs.
5. For each method (MS2DeepScore, Spec2Vec, classical similarity), vary Tanimoto threshold from 0 to ~1 and compute precision and recall at each threshold.
6. Plot precision versus recall for all three methods on a single curve and save as PNG.
7. Validation: Confirm that MS2DeepScore curve dominates (higher precision at matched recall) compared to Spec2Vec and classical methods across the threshold range, matching the reported result in Figure 4.
8. References: source article (DOI: 10.1186/s13321-021-00558-4)

## Workflow Ports

**Inputs:**

- `pretrained_model` — Pretrained MS2DeepScore model weights ← `task_001/rmse_no_filter`
- `test_spectra` — Test set binned spectra with InChIKey annotations
- `tanimoto_labels` — Ground-truth Tanimoto score matrix (500×500)
- `baseline_scores` — Spec2Vec and classical similarity predictions on test pairs

**Outputs:**

- `precision_recall_plot` — Precision-recall curve for structural similarity retrieval

**Used:** `urn:asb:port:task_001/rmse_no_filter`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

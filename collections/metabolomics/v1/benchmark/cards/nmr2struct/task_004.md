# SciTask Card: Extend NMR2Struct structure prediction to molecules beyond 19 heavy atoms

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T09:55:01.678255+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_nmr2struct/synthesized_package`
- Domain: `chemistry / chemoinformatics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `data-analysis`
- Input from: `task_001`
- Quality: Score 2/5 — placeholder, 7 grounding failures

## Classification

- Task kind: `extension`
- Article type: `research-article`
- Primary domain: `cheminformatics`
- Subdomains: `artificial-intelligence`
- Techniques: `nmr`, `deep-learning`, `machine-learning`, `transformer-model`

## Research Question
Does the NMR2Struct model maintain accurate structure recovery performance when applied to molecules with more than 19 heavy atoms, or does accuracy degrade significantly beyond this training scope?

## Connected Finding
The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.

## Task Description
Apply a pretrained NMR2Struct model to a held-out test set of molecules with >19 heavy atoms from a public chemical database (PubChem or equivalent), and quantify the degradation in top-k structure recovery accuracy relative to the in-scope (≤19 heavy atom) baseline condition.

## Inputs
- Pretrained or fine-tuned NMR2Struct model checkpoint (transformer + CNN weights)
- Held-out test set of molecules exceeding 19 heavy atoms from PubChem or equivalent public chemical database
- 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules (experimental or simulated)
- In-scope baseline accuracy metrics (top-k structure recovery for molecules ≤19 heavy atoms)

## Expected Outputs
- Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms)
- Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss)
- Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly

## Expected Output File

- `oos_accuracy_degradation_report.csv`

## Landmark Outputs

- `oos_predictions.json`
- `oos_top_k_accuracy.csv`
- `degradation_baseline_comparison.csv`
- `failure_mode_analysis.txt`

## Tools
- transformer architecture
- convolutional neural network

## Skills
- nmr-spectrum-to-structure-inference
- molecular-structure-prediction-out-of-distribution
- top-k-accuracy-ranking-and-evaluation
- model-generalization-assessment-across-molecular-size-regimes
- chemical-graph-connectivity-validation
- performance-degradation-quantification-and-analysis

## Workflow Description
1. Load the pretrained or fine-tuned NMR2Struct model (transformer + CNN architecture) from the deposited checkpoint. 2. Retrieve or construct a held-out test set of molecules exceeding 19 heavy atoms from PubChem or an equivalent public chemical database. 3. Generate or obtain 1D ¹H and/or ¹³C NMR spectra for each out-of-scope molecule (via simulation, experimental data, or database retrieval). 4. Feed each NMR spectrum through the model to generate predicted molecular formula and connectivity graphs. 5. Rank predictions by confidence score and compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity). 6. Compare out-of-scope accuracy metrics against the reported in-scope baseline (molecules ≤19 heavy atoms) and quantify the absolute and relative degradation. 7. Document accuracy loss, error distribution, and failure modes in a summary report.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history provided; unknown whether models, datasets, or evaluation code have been updated since publication date
- No explicit statement of the upper heavy-atom threshold tested (19 atoms mentioned as demonstration scope in intro, but no explicit out-of-scope test boundary stated in discussion)
- No reference to deposited code, model weights, or held-out test set location (only GitHub source cited generically; specific branch, release tag, or supplementary data accession not identified)

## Domain Knowledge
- The NMR2Struct framework was trained and validated on molecules with up to 19 heavy atoms; applying it to larger molecules tests extrapolation beyond the training regime and expected performance degradation.
- Top-k structure recovery accuracy measures whether the ground-truth connectivity graph appears in the model's ranked list of k most-confident predictions; this is more lenient than top-1 accuracy and captures partial model knowledge.
- 1D ¹H and ¹³C NMR spectra are the primary input; molecules with >19 heavy atoms introduce combinatorial complexity (more fragment possibilities) that can exceed the model's learned capacity for assembly.
- Out-of-distribution (OOD) performance degradation is expected because the transformer's fragment assembly strategy was optimized for in-scope molecular sizes; larger molecules may require architectural or training adaptations not present in the base model.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms), Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss), Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] Does the NMR2Struct model maintain accurate structure recovery performance when applied to molecules with more than 19 heavy atoms, or does accuracy degrade significantly beyond this training scope?: 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms, a size for which there are trillions of possibl'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.: 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Pretrained or fine-tuned NMR2Struct model checkpoint (transformer + CNN weights): 'a transformer architecture can be constructed to efficiently solve the task... Integrating this capability with a convolutional neural network, we build an end-to-end model'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Held-out test set of molecules exceeding 19 heavy atoms from PubChem or equivalent public chemical database: 'held-out set of molecules exceeding 19 heavy atoms (sourced from a public chemical database such as PubChem or the deposited dataset)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules (experimental or simulated): 'predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] In-scope baseline accuracy metrics (top-k structure recovery for molecules ≤19 heavy atoms): 'We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms): 'measure the degradation or retention of top-k structure recovery accuracy relative to the in-scope condition'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss): 'measure the degradation or retention of top-k structure recovery accuracy relative to the in-scope condition'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly: 'held-out set of molecules exceeding 19 heavy atoms'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] transformer architecture: 'a transformer architecture can be constructed to efficiently solve the task'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] convolutional neural network: 'Integrating this capability with a convolutional neural network, we build an end-to-end model'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] No changelog or version history provided; unknown whether models, datasets, or evaluation code have been updated since publication date: '_No changelog found._'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No explicit statement of the upper heavy-atom threshold tested (19 atoms mentioned as demonstration scope in intro, but no explicit out-of-scope test boundary stated in discussion): '[Section contains no technical details; only header and metadata]'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] No reference to deposited code, model weights, or held-out test set location (only GitHub source cited generically; specific branch, release tag, or supplementary data accession not identified): 'Source: github:MarklandGroup__NMR2Struct'

## Evaluation Strategy
### Direct Checks
- verify that a held-out test set of molecules with ≥20 heavy atoms exists in the deposited dataset or public chemical database (PubChem/other); file_exists and row_count_equals or field_present for molecule count and heavy atom count field
- verify that NMR2Struct model checkpoint or weights file exists in the repository or supplementary deposit; file_exists
- verify that model inference script runs successfully on the held-out set without errors; script_runs
- verify that top-k structure recovery accuracy metric (e.g., exact match, canonical SMILES match, or graph edit distance threshold) is computed and reported as a single numerical score or per-molecule prediction table; file_exists and format_is for output table/CSV
- verify that in-scope baseline accuracy (molecules ≤19 heavy atoms) is retrieved from article text, SI, or model evaluation deposit; output_matches_reference or contains_substring of reported number
- verify that degradation/retention ratio or absolute accuracy difference (out-of-scope vs. in-scope) is computed; value_in_range or exact numerical output artifact

### Expert Review
- assess whether the choice of held-out test set is representative and unbiased (no data leakage from training or hyperparameter tuning); confirm sampling strategy or stratification by molecular properties
- evaluate the appropriateness of the top-k metric definition (k value, exact vs. relaxed matching criterion) and whether it aligns with chemical validity (e.g., whether isomers or stereochemically distinct structures are penalized equally)
- interpret the magnitude of accuracy degradation beyond 19 heavy atoms in light of model architecture (receptive field, sequence length limits, training data composition) and chemical complexity
- confirm that any reported accuracy figures use consistent evaluation protocol and do not conflate different ranking metrics (e.g., top-1 vs. top-10)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load the pretrained transformer + CNN NMR2Struct model from checkpoint
2. Retrieve or construct a held-out test set of molecules with >19 heavy atoms from PubChem or equivalent database
3. Obtain 1D ¹H and/or ¹³C NMR spectra for each out-of-scope molecule
4. Generate ranked predictions of molecular formula and connectivity for each spectrum
5. Compute top-1, top-3, and top-5 structure recovery accuracy on out-of-scope test set
6. Compare out-of-scope accuracy to reported in-scope baseline (≤19 heavy atoms) and quantify absolute and relative degradation
7. Validation: verify that reported accuracy metrics for in-scope and out-of-scope conditions are reproducible and documented, and that degradation is quantified against the published baseline

## Workflow Ports

**Inputs:**

- `model_checkpoint` — Pretrained NMR2Struct model (transformer + CNN) ← `task_001/accuracy_metrics`
- `test_molecules_oos` — Out-of-scope test molecules (>19 heavy atoms) from PubChem
- `nmr_spectra_oos` — 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules
- `baseline_metrics` — In-scope (≤19 heavy atoms) baseline top-k accuracy

**Outputs:**

- `oos_accuracy_scores` — Top-k structure recovery accuracy for out-of-scope molecules
- `degradation_table` — Comparative accuracy degradation (out-of-scope vs. baseline)
- `failure_report` — Error analysis and failure mode summary

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:MarklandGroup__NMR2Struct`
- **Synthesized at:** 2026-06-15T09:59:33+00:00

## Extraction Quality
- Score: 2/5
- Coherent: true
- Placeholder detected: true
- Groundedness failures (7):
  - inputs[0]: evidence_span not found in section 'other' (value='Pretrained or fine-tuned NMR2Struct model checkpoint (transf', span='a transformer architecture can be constructed to efficiently')
  - inputs[1]: evidence_span not found in section 'other' (value='Held-out test set of molecules exceeding 19 heavy atoms from', span='held-out set of molecules exceeding 19 heavy atoms (sourced ')
  - expected_outputs[0]: evidence_span not found in section 'other' (value='Top-1, top-3, and top-5 structure recovery accuracy scores f', span='measure the degradation or retention of top-k structure reco')
  - expected_outputs[1]: evidence_span not found in section 'other' (value='Comparative accuracy degradation table (out-of-scope vs. in-', span='measure the degradation or retention of top-k structure reco')
  - expected_outputs[2]: evidence_span not found in section 'other' (value='Summary report documenting failure modes, error distribution', span='held-out set of molecules exceeding 19 heavy atoms')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='No explicit statement of the upper heavy-atom threshold test', span='[Section contains no technical details; only header and meta']
  - Semantic gap: The research_question asks whether accuracy 'degrades significantly' beyond 19 atoms, but the finding only characterizes the limit as 'uncharacterized' — this is asymmetric. The RQ presupposes degradation; the finding merely notes absence of data.
- Notes: This task card is well-structured in intent (testing OOD generalization of NMR2Struct beyond its training scope) and domain-coherent, but suffers from severe groundedness and specificity failures. Most evidence_spans are paraphrases or inferences rather than direct quotations, and the card conflates article-reported findings with task-derived expectations. The research question and finding are semantically related but asymmetric: the RQ asks 'does it degrade?', the finding answers 'we don't know'—which is correct but does not address the RQ's implicit hypothesis. Inputs and expected_outputs are task-derived rather than source-grounded, making them task instructions rather than card-claimed facts. The card would benefit from: (1) re-grounding all evidence_spans against actual source sections with precise line numbers, (2) separating task objectives (what the user will do) from research findings (what the article claims), (3) clarifying baseline accuracy metrics from the source, (4) resolving the RQ/finding asymmetry, and (5) removing generic tool descriptions in favor of article-specific model details (e.g., transformer layer count, CNN kernel sizes). Quality score reflects coherent design but low verifiability and partial placeholder use.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

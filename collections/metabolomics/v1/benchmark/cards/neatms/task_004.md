# SciTask Card: Reconstruct the Class-Normalized Batch Creation Step for Neural Network Training

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:11:40.529655+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_neatms/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- GitHub: `bihealth/NeatMS`
- Input from: `task_001`
- Quality: Score 3/5 — 3 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `artificial-intelligence`, `untargeted-metabolomics`
- Techniques: `machine-learning`, `deep-learning`, `feature-detection`, `metabolite-identification`, `dimensionality-reduction`
- Keywords: `untargeted lcms` · `signal labelling` · `peak filtering` · `false positive detection` · `neural network classification` · `ms1 peaks` · `metabolomics data processing`

## Research Question
How does the nn_handler.create_batches() method operate when invoked with normalise_class=True versus normalise_class=False, and what are the structural differences in the resulting batch artifacts?

## Connected Finding
When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count; when set to False, class counts remain unequal, reflecting the original distribution in the dataset.

## Task Description
Create training/validation/test batches from a labeled LC-MS peak dataset using NeatMS.NN_handler.create_batches() with both class-normalization modes (normalise_class=True and False) at the default 80:10:10 split, producing batch artifacts and validating that class-normalized batches enforce equal peak counts across all classes.

## Inputs
- task_001.expected_outputs[0]: Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification
- Labeled LC-MS experiment object with raw mzML files and feature table (CSV format from mzMine or XCMS) containing 10–20 representative pooled samples and manually annotated peak labels (High_quality, Low_quality, Noise)

## Expected Outputs
- Training batch artifact (80% of peaks, class-imbalanced distribution)
- Test batch artifact (10% of peaks, class-imbalanced distribution)
- Validation batch artifact (10% of peaks, class-imbalanced distribution)
- Training batch artifact with equal class counts (80% of normalized peaks, all classes equal to smallest class size)
- Test batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size)
- Validation batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size)
- Verification report documenting per-class peak counts in each batch condition (normalise_class=False vs True)

## Expected Output File

- `batch_verification_report.txt`

## Landmark Outputs

- `train_batch_unnormalized.pkl`
- `test_batch_unnormalized.pkl`
- `val_batch_unnormalized.pkl`
- `train_batch_normalized.pkl`
- `test_batch_normalized.pkl`
- `val_batch_normalized.pkl`

## Tools
- NeatMS
- Python

## Skills
- peak-quality-label-stratification
- training-validation-test-set-allocation
- class-imbalance-mitigation-via-normalization
- batch-construction-parameter-optimization
- neural-network-training-data-preparation

## Workflow Description
1. Load a labeled experiment object into NeatMS using ntms.Experiment(raw_data_folder_path, feature_table_path, input_data) with 10–20 pooled representative samples and their corresponding feature tables. 2. Instantiate an NN_handler object with ntms.NN_handler(experiment, matrice_size=120, margin=1, min_scan_num=5) using default matrix size, margin, and minimum scan filtering. 3. Call nn_handler.create_batches(validation_split=0.1, normalise_class=False) to generate training (80%), test (10%), and validation (10%) batches without class balancing, recording class distributions in each batch. 4. Call nn_handler.create_batches(validation_split=0.1, normalise_class=True) to regenerate batches with class normalization, verifying that all three classes have equal peak counts within each batch (set to the size of the smallest class). 5. Export or inspect batch metadata (peak counts per class per batch) to verify that normalized batches satisfy the constraint 'number of peaks for each class will be equal to the smallest class' while unnormalized batches preserve original class imbalance.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ADAP_threshold_all_vs_recall_training_500.png` | figure | False |
| `figures/ROC_recall_High_vs_all.png` | figure | False |
| `figures/Screenshot 2020-04-28 at 16.43.33.png` | figure | False |
| `figures/annotation_tool.png` | figure | False |
| `figures/recall_table.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found.

## Domain Knowledge
- NeatMS classifies LC-MS peaks into three mutually exclusive classes: High_quality, Low_quality, and Noise; all peaks must be assigned exactly one label for batch construction.
- The normalise_class=True flag automatically rebalances training data by downsampling all classes to the size of the smallest class, which prevents minority-class under-fitting but discards data.
- Default validation_split=0.1 allocates 80% training, 10% test, and 10% validation; the test set (called 'validation' in TensorFlow output) is used during model training to detect overfitting.
- The min_scan_num=5 default threshold filters out peaks with fewer than 5 points before batch assembly, removing signal-to-noise ambiguous cases that degrade model robustness.
- Batch construction operates on peaks extracted from raw mzML via a two-dimensional matrix: dimension 1 encodes margin vs. peak signal (binary 0/1), dimension 2 represents the peak (interpolated to matrice_size=120 points) with surrounding context controlled by margin=1 (margins = peak width on each side).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] How does the nn_handler.create_batches() method operate when invoked with normalise_class=True versus normalise_class=False, and what are the structural differences in the resulting batch artifacts?: 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count; when set to False, class counts remain unequal, reflecting the original distribution in the dataset.: 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Labeled LC-MS experiment object with raw mzML files and feature table (CSV format from mzMine or XCMS) containing 10–20 representative pooled samples and manually annotated peak labels (High_quality, Low_quality, Noise): 'create our experiment object and load the data, we can do that the exact same way as we have done before'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Training batch artifact (80% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Test batch artifact (10% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Validation batch artifact (10% of peaks, class-imbalanced distribution): 'By default, the split between training:test:validation batches is 80:10:10'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Training batch artifact with equal class counts (80% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Test batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Validation batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size): 'when set to `True`, the number of peaks for each class will be equal to the smallest'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Verification report documenting per-class peak counts in each batch condition (normalise_class=False vs True): 'The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Python: 'open source python package'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists at github:bihealth__NeatMS containing nn_handler module with create_batches() method
- script_runs: invoke nn_handler.create_batches() with normalise_class=True using default 80:10:10 split and confirm execution completes without error
- script_runs: invoke nn_handler.create_batches() with normalise_class=False using default 80:10:10 split and confirm execution completes without error
- file_exists: batch artifacts generated for normalise_class=True condition (train, test, validation batch files)
- file_exists: batch artifacts generated for normalise_class=False condition (train, test, validation batch files)
- value_in_range: verify train/test/validation split proportions are approximately 80:10:10 (±2 percentage points) for both conditions
- row_count_equals: sum of train + test + validation batch row counts equals total input dataset row count for both conditions

### Expert Review
- verify that class-normalized batches (normalise_class=True) satisfy equal-class-count constraint: all classes present in each batch have equal or near-equal peak counts as documented
- verify that non-normalized batches (normalise_class=False) preserve original class distribution without forced equalization
- assess whether batch creation parameters and output structure conform to NeatMS design specification for downstream neural network training

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load labeled experiment object containing raw LC-MS data (mzML) and feature table (CSV) from 10–20 representative samples with manual peak annotations across High_quality, Low_quality, and Noise classes.
2. Instantiate NN_handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) to configure peak matrix extraction and filtering thresholds.
3. Invoke create_batches(validation_split=0.1, normalise_class=False) to generate training (80%), test (10%), and validation (10%) splits preserving original class-frequency distributions.
4. Invoke create_batches(validation_split=0.1, normalise_class=True) to regenerate the same splits with class balancing, reducing all classes to the minority-class size.
5. Extract and compare per-class peak counts across all six batches (three splits × two normalization modes) to verify that normalized batches enforce equal class cardinality and unnormalized batches preserve imbalance.
6. Validation: Confirm that for each normalized batch, the count of High_quality peaks equals the count of Low_quality peaks equals the count of Noise peaks; and that unnormalized batches retain the original imbalanced distribution without modification.

## Workflow Ports

**Inputs:**

- `labeled_experiment` — Labeled LC-MS experiment object with raw mzML files and feature tables

**Outputs:**

- `train_batch_unnormalized` — Training batch (80%, class-imbalanced)
- `test_batch_unnormalized` — Test batch (10%, class-imbalanced)
- `val_batch_unnormalized` — Validation batch (10%, class-imbalanced)
- `train_batch_normalized` — Training batch (80%, equal class counts)
- `test_batch_normalized` — Test batch (10%, equal class counts)
- `val_batch_normalized` — Validation batch (10%, equal class counts)
- `batch_verification_report` — Batch class-distribution verification report

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bihealth__NeatMS`
- **Synthesized at:** 2026-06-16T07:21:51+00:00

## Extraction Quality
- Score: 3/5
- Coherent: true
- Placeholder detected: false
- Groundedness failures (3):
  - tools[1]: evidence_span 'open source python package' not found in section 'methods' (value='Python')
  - inputs[0]: evidence_span is vague and generic ('create our experiment object and load the data, we can do that the exact same way as we have done before') — does not substantively ground the specific input format or requirements
  - research_question and finding: evidence_span is incomplete — truncated mid-sentence ('equal to the smallest') without finishing the thought or confirming the False case behavior
- Notes: The task card is well-structured and methodologically sound overall, with clear step-by-step workflows and detailed domain knowledge. However, three evidence spans are problematic: (1) research_question and finding evidence are truncated and incomplete, (2) inputs[0] grounding is circular/contextual rather than self-contained, and (3) tools[1] (Python) lacks proper grounding in the source text. The domain knowledge is rich and helpful, but there is ambiguity around whether 'test' and 'validation' refer to the same or different splits given the 80:10:10 split scheme and TensorFlow terminology note. The evaluation_strategy is strong with concrete direct checks and expert review criteria. Recommend: (a) extend evidence_span for research_question/finding to include the complete statement and explicit description of False case, (b) ground inputs[0] with the specific feature table schema and labeling requirements, (c) re-ground tools[1] or remove if Python is assumed to be implicit, and (d) clarify the test/validation distinction in domain_knowledge.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

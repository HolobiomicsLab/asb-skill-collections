# SciTask Card: Analyze missing-fraction metric as a function of training corpus size using the AllPositive dataset

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T06:52:35.005391+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_spec2vec`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `model-inference`, `benchmark-evaluation`
- DOI: `10.1371/journal.pcbi.1008724`
- GitHub: `matchms/matchms`
- Input from: `task_002`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`, `artificial-intelligence`
- Techniques: `spectral-library-matching`, `molecular-networking`, `tandem-ms`, `machine-learning`, `natural-language-processing`, `cosine-similarity-scoring`
- Keywords: `mass spectrometry fragmentation` · `spectral similarity scoring` · `untargeted metabolomics` · `metabolite identification` · `lc-ms/ms` · `word embeddings` · `natural language processing` · `molecular networks` · `database searching` · `structural annotation` · `cosine similarity` · `ms2 spectra`

## Research Question
How does the fraction of peak coverage achieved by a Spec2Vec Word2Vec model vary as a function of training corpus size, and can a 97% coverage threshold be reproduced with the AllPositive dataset trained for 15 epochs?

## Connected Finding
A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic (1 − Σ√w_i / Σ√w_i) across spectra.

## Task Description
Compute the missing-fraction statistic across the AllPositive dataset (95,320 spectra) using a Spec2Vec Word2Vec model trained on 15 epochs, measuring the fraction of weighted spectrum intensity not represented in the model as corpus size varies, and reproduce the reported 97% peak coverage result.

## Inputs
- AllPositive dataset (95,320 positive ionization mode spectra with InChIKey), filtered to m/z ∈ [0, 1000] and ≥10 peaks
- Pre-trained Word2Vec model (gensim, CBOW, window-size=500, negative=5, 15 epochs) trained on AllPositive dataset
- Spec2Vec library (Python package) and matchms ≥0.6.0 for spectrum document conversion and word embedding lookup

## Expected Outputs
- Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size
- Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra
- Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent

## Expected Output File

- `missing_fraction_coverage_stats.csv`

## Landmark Outputs

- `spectrum_embeddings.npy`
- `missing_fraction_per_spectrum.csv`
- `coverage_vs_corpus_size.csv`
- `coverage_curve.png`
- `coverage_summary_metrics.json`

## Tools
- Spec2Vec
- Word2Vec
- matchms
- gensim
- NumPy
- Numba
- Pandas

## Skills
- spectral-peak-word-embedding-representation
- word2vec-model-inference-unknown-word-handling
- mass-spectral-missing-word-fraction-computation
- corpus-size-coverage-scaling-analysis
- neutral-loss-extraction-and-weighting
- peak-intensity-normalization-and-weighted-aggregation

## Workflow Description
1. Load the AllPositive dataset (95,320 spectra) from Zenodo (10.5281/zenodo.3978118) and the pre-trained Spec2Vec Word2Vec model trained on 15 epochs (zenodo.org/record/4173596). 2. For each spectrum, convert peaks to words with format 'peak@xxx.xx' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words. 3. Normalize peak intensities to maximum = 1 for each spectrum. 4. For each spectrum, compute the missing fraction as: missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity. 5. Aggregate missing-fraction statistics across all spectra and compute the proportion of peaks with known word embeddings (coverage = 1 − mean missing fraction). 6. Vary effective corpus size by progressively adding spectra and recompute coverage at each step to generate a coverage-vs-corpus-size curve. 7. Compare the final coverage result (97% for AllPositive at 15 epochs) against the computed mean coverage and verify convergence.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `spec2vec.pdf` | main_article | True |

## Missing Information
- Exact formula or implementation reference for computing missing-fraction statistic (1 − Σ√w_i / Σ√w_i) and definition of w_i weighting scheme
- Specific corpus size sampling strategy (which intermediate corpus sizes were tested to generate the coverage curve toward 97% coverage)
- Location and format of reported 97% peak coverage curve (whether in Figure G of S3 Text, a supplementary table, or main figure)
- Detailed definition of how peak weights (w_i) are computed from spectra (intensity-based, frequency-based, or other metric)

## Domain Knowledge
- Missing fraction is defined as 1 − (weighted sum of peaks found in model) / (weighted sum of all peaks), where weights are square-root-normalized intensities; this metric quantifies model vocabulary coverage for novel spectra.
- Spec2Vec peak words are binned to 2 decimal places (e.g., m/z 200.445 → 'peak@200.45') and neutral losses are represented as 'loss@xxx.xx' for m/z differences from precursor; only words present in the trained Word2Vec vocabulary contribute to the denominator.
- A threshold of missing_fraction < 0.05 is recommended to avoid returning Spec2Vec scores for spectra with poor model vocabulary overlap; this threshold can be tuned per application.
- The AllPositive model trained on 95,320 spectra achieves ~97% coverage of all possible 2-decimal-binned peaks and losses, meaning only ~3% of spectrum words are out-of-vocabulary, even for novel spectra.
- Window-size of 500 in Word2Vec training means the entire spectrum document is treated as context (no positional ordering), which differs from typical NLP where word order is preserved.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size, Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra, Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the fraction of peak coverage achieved by a Spec2Vec Word2Vec model vary as a function of training corpus size, and can a 97% coverage threshold be reproduced with the AllPositive dataset trained for 15 epochs?: 'In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic (1 − Σ√w_i / Σ√w_i) across spectra.: 'Training a model on the UniqueInchikey dataset takes about 30 minutes on an Intel i7-8550U CPU.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AllPositive dataset (95,320 positive ionization mode spectra with InChIKey), filtered to m/z ∈ [0, 1000] and ≥10 peaks: 'We removed all peaks with m/z ratios outside the range [0, 1000] and discarded all spectra with less than 10 peaks. This left us with 95,320 spectra'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained Word2Vec model (gensim, CBOW, window-size=500, negative=5, 15 epochs) trained on AllPositive dataset: 'training a model with negative sampling (negative = 5) and 15 (AllPositive) up to 50 (UniqueInchikey) epochs were best suited for obtaining close to optimal model performance'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Spec2Vec library (Python package) and matchms ≥0.6.0 for spectrum document conversion and word embedding lookup: 'The underlying code was developed into two Python packages to handle and compare mass spectra, matchms (https://github.com/matchms/matchms) and spec2vec (https://github.com/iomega/spec2vec)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size: 'missing fraction = 1 − (Σ√w_i for model words) / (Σ√w_i all words), where w_i is normalized intensity'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra: 'models we trained on AllPositive (95,320 spectra) with 2-decimal rounding contained about 97% of all possible peaks and losses'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent: 'having different peak filtering for the different similarity scores, we also repeated the library matching with cosine scores computed based on the Spec2Vec-processed data'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Spec2Vec: 'The underlying code was developed into two Python packages to handle and compare mass spectra, matchms (https://github.com/matchms/matchms) and spec2vec (https://github.com/iomega/spec2vec)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Word2Vec: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] NumPy: 'optimized by making extensive use of Numpy [24] and Numba [25]'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Numba: 'optimized by making extensive use of Numpy [24] and Numba [25]'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Pandas: 'was optimized using Pandas [40]'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Exact formula or implementation reference for computing missing-fraction statistic (1 − Σ√w_i / Σ√w_i) and definition of w_i weighting scheme: 'For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training (see Fig G in'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Specific corpus size sampling strategy (which intermediate corpus sizes were tested to generate the coverage curve toward 97% coverage): 'training the embedding on 95,320 spectra took 40 minutes (when training for 15 iterations)'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Location and format of reported 97% peak coverage curve (whether in Figure G of S3 Text, a supplementary table, or main figure): 'For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training (see Fig G in'
- `ev_019` from `agent2_synthesis` (agent2_traced): [methods] Detailed definition of how peak weights (w_i) are computed from spectra (intensity-based, frequency-based, or other metric): 'In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part'

## Evaluation Strategy
### Direct Checks
- file_exists: verify AllPositive dataset is accessible at https://doi.org/10.5281/zenodo.3978118
- file_exists: verify trained Word2Vec model (AllPositive, 15-epoch) is accessible at https://zenodo.org/record/4173596
- script_runs: verify spec2vec package (https://github.com/iomeva/spec2vec) can be installed and imported successfully
- file_format_is: verify AllPositive dataset contains mass spectra in a loadable format (e.g., JSON, MGF, or compatible pickle)
- row_count_equals: verify AllPositive dataset contains exactly 95,320 spectra as reported in methods section
- value_in_range: verify computed peak coverage statistic (missing-fraction = 1 − Σ√w_i / Σ√w_i) outputs a value between 0.0 and 1.0 for each corpus size
- output_matches_reference: verify final missing-fraction value for full 95,320-spectrum corpus matches the reported 97% peak coverage (or equivalently, 0.03 missing fraction) from discussion text, within ±1 percentage point
- script_runs: verify analysis script (from https://github.com/iomega/spec2vec_gnps_data_analysis or equivalent) can compute coverage curve without errors
- contains_substring: verify output plot or table contains coverage measurements at multiple corpus sizes showing progression toward 97% coverage, parameter-sensitive to corpus size intervals chosen

### Expert Review
- Verify that the missing-fraction calculation (1 − Σ√w_i / Σ√w_i) correctly implements the intended peak coverage metric described in methods; confirm interpretation of w_i as peak weights and that square root weighting is appropriate for this analysis
- Assess whether the reported 97% peak coverage for the 15-epoch model is consistent with the claim that 'a model pre-trained on a large spectra dataset will cover a large enough fraction of the features' from the discussion section
- Evaluate whether coverage curve shape and saturation behavior are reasonable given typical Word2Vec learning dynamics on ~95k spectra

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load AllPositive dataset (95,320 spectra, pre-filtered to m/z ∈ [0, 1000], ≥10 peaks) and pre-trained Word2Vec model (15 epochs, CBOW, window=500, negative=5).
2. Convert each spectrum to a document: represent peaks as 'peak@xxx.xx' words (2-decimal binning) and add neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words.
3. Normalize peak intensities to maximum = 1 per spectrum; compute missing fraction as 1 − (Σ√w_i for words in model vocabulary) / (Σ√w_i for all words).
4. Aggregate missing-fraction statistics across all spectra and compute mean coverage (1 − mean missing fraction).
5. Vary effective corpus size by progressively adding spectra in order and recompute coverage metrics at each step to generate a corpus-size scaling curve.
6. Validation: verify that final mean coverage reaches ≥97% when corpus includes all 95,320 spectra, matching the reported 97% peak coverage for the AllPositive 15-epoch model; confirm no missing-fraction value exceeds the recommended threshold of 0.05 for ≥95% of spectra.
7. References: source article (DOI: 10.1371/journal.pcbi.1008724)

## Workflow Ports

**Inputs:**

- `allpositive_dataset` — AllPositive LC-MS dataset (95,320 spectra, filtered m/z ∈ [0, 1000], ≥10 peaks) ← `task_002/library_matching_results`
- `word2vec_model` — Pre-trained Spec2Vec Word2Vec model (15 epochs, trained on AllPositive)
- `spec2vec_library` — Spec2Vec and matchms Python packages

**Outputs:**

- `missing_fraction_table` — Missing-fraction statistics per spectrum (CSV)
- `coverage_curve` — Coverage-vs-corpus-size curve (PNG)
- `summary_metrics` — Coverage summary metrics and validation (JSON)

**Used:** `urn:asb:port:task_002/library_matching_results`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

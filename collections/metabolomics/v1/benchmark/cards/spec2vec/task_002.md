# SciTask Card: Reproduce library matching true-to-false-positive performance of Spec2Vec versus cosine scores

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T06:52:35.005391+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_spec2vec`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `benchmark-evaluation`, `data-analysis`
- DOI: `10.1371/journal.pcbi.1008724`
- GitHub: `matchms/matchms`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`, `artificial-intelligence`
- Techniques: `spectral-library-matching`, `molecular-networking`, `tandem-ms`, `machine-learning`, `natural-language-processing`, `cosine-similarity-scoring`
- Keywords: `mass spectrometry fragmentation` · `spectral similarity scoring` · `untargeted metabolomics` · `metabolite identification` · `lc-ms/ms` · `word embeddings` · `natural language processing` · `molecular networks` · `database searching` · `structural annotation` · `cosine similarity` · `ms2 spectra`

## Research Question
How do Spec2Vec similarity scores compare to cosine and modified cosine scores in terms of true-to-false-positive rate during library matching on the AllPositive dataset?

## Connected Finding
Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.

## Task Description
Reproduce library matching performance results for the AllPositive dataset using cosine, modified cosine, and Spec2Vec similarity scores with reported experimental parameters, computing true-positive and false-positive rates for validation against structural similarity labels.

## Inputs
- AllPositive dataset (95,320 positive-mode LC-MS spectra with InChIKey annotations)
- Pre-trained Word2Vec models (15-epoch and 50-epoch) trained on AllPositive dataset
- Cosine similarity score implementation from matchms package (>=0.6.0)
- Modified cosine similarity score implementation from matchms package

## Expected Outputs
- Library matching results table with true-positive rates, false-positive rates, and area-under-curve for cosine, modified cosine, and Spec2Vec (15-epoch and 50-epoch) similarity scores
- ROC curves comparing performance of cosine, modified cosine, and Spec2Vec similarity scores on AllPositive library matching task
- Quantitative performance metrics (TP/FP counts and rates) for each similarity scoring method

## Expected Output File

- `library_matching_performance_results.csv`

## Landmark Outputs

- `filtered_allpositive_spectra.mgf`
- `cosine_similarity_matrix.csv`
- `modified_cosine_similarity_matrix.csv`
- `spec2vec_similarity_matrix_15epoch.csv`
- `spec2vec_similarity_matrix_50epoch.csv`
- `roc_curves_comparison.png`

## Tools
- spec2vec
- matchms
- Word2Vec
- gensim
- Numpy
- Numba
- Pandas
- scipy

## Skills
- mass-spectrometry-library-matching
- spectral-similarity-scoring-cosine-variants
- word-embedding-based-spectrum-representation
- receiver-operator-characteristic-curve-generation
- structural-similarity-ground-truth-validation
- peak-filtering-and-preprocessing-LC-MS
- chemical-structure-fingerprint-comparison

## Workflow Description
1. Download the AllPositive dataset (95,320 spectra with InChIKey annotations) from Zenodo 10.5281/zenodo.3978118 and the pre-trained Word2Vec models (15-epoch and 50-epoch versions trained on AllPositive data) from zenodo.org/record/4173596. 2. Filter spectra: remove peaks with m/z outside [0, 1000], discard spectra with fewer than 10 peaks, and remove spectra without InChIKey annotation. 3. For cosine and modified cosine scoring, apply peak filtering by ignoring peaks with relative intensities <0.01 compared to the highest intensity peak; for Spec2Vec, apply parent-mass-scaled peak filtering (max_peaks = 0.5 × parentmass). 4. Pre-select potentially matching spectra using precursor m/z matching with 1 ppm tolerance. 5. Compute similarity scores: apply cosine similarity with tolerance 0.005 and minimum matching peaks = 6; apply modified cosine with tolerance 0.005 and minimum matching peaks = 10; apply Spec2Vec similarity using both the 15-epoch and 50-epoch Word2Vec models. 6. For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure) to construct receiver-operator-characteristic curves. 7. Calculate and report true-positive rate, false-positive rate, and area-under-curve for each method and compare against reported paper results.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `spec2vec.pdf` | main_article | True |

## Missing Information
- Exact number of spectra used as queries vs. library spectra in the reported library matching experiment is not specified
- The specific figure or table location in the paper where library matching true-positive and false-positive rates are reported is not identified in the provided discussion text
- Minimum matching peaks threshold (min_match) specified for Spec2Vec models in library matching is not explicitly stated in the provided discussion
- Whether the reported library matching results use the same AllPositive dataset for both training the Word2Vec model and evaluating performance, or use a held-out test set, is not clearly specified

## Domain Knowledge
- InChIKey first 14 characters (planar InChIKey) represent the planar graph topology of a molecule and are used as ground truth for structural similarity classification in library matching tasks.
- Cosine similarity score requires minimum matching peaks (min_match=6) and relative intensity threshold of 0.01 to filter low-intensity noise; modified cosine additionally allows matching peaks shifted by precursor m/z difference.
- Spec2Vec requires Word2Vec model trained on spectrum documents where peaks are binned to 2 decimal precision (e.g., 'peak@200.45') and neutral losses (5.0–200.0 Da) are added as features.
- The parent mass scaling rule (max_peaks = 0.5 × parentmass) for Spec2Vec ensures larger molecules with more fragments are represented proportionally during model training, preventing bias toward high-mass fragmentation patterns.
- Missing fraction threshold (fraction of unknown peaks <0.05) should be checked to ensure Spec2Vec similarity scores for out-of-distribution spectra are not returned, as the pre-trained model may lack learned embeddings for uncommon fragments.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Library matching results table with true-positive rates, false-positive rates, and area-under-curve for cosine, modified cosine, and Spec2Vec (15-epoch and 50-epoch) similarity scores.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How do Spec2Vec similarity scores compare to cosine and modified cosine scores in terms of true-to-false-positive rate during library matching on the AllPositive dataset?: 'Spec2Vec model was trained only on the library set and Spec2Vec and cosine similarity scores were compared with h cosine similarity scores for library matching (Fig 4). Both Spec2Vec and cosine'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.: 'Spec2Vec resulted in a notably better true/false positive ratio at all thresholds. Spec2Vec also allowed to correctly match the query spectra with up to 88% accuracy and showed both higher accuracy'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AllPositive dataset (95,320 positive-mode LC-MS spectra with InChIKey annotations): 'The here used subset contains all spectra with positive ionization mode containing 112,956 spectra, out of which 92,954 with InChIKey'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained Word2Vec models (15-epoch and 50-epoch) trained on AllPositive dataset: 'The two most important trained Word2Vec models used in this work can be downloaded from https://zenodo.org/record/4173596 (trained on AllPositive dataset)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Cosine similarity score implementation from matchms package (>=0.6.0): 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (> = 0.6.0)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Modified cosine similarity score implementation from matchms package: 'Following Watrous [11], our modified cosine score combines both the matching peak m/z and the m/z shifted by the difference in precursor m/z'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Library matching results table with true-positive rates, false-positive rates, and area-under-curve for cosine, modified cosine, and Spec2Vec (15-epoch and 50-epoch) similarity scores: 'high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] ROC curves comparing performance of cosine, modified cosine, and Spec2Vec similarity scores on AllPositive library matching task: 'The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] Quantitative performance metrics (TP/FP counts and rates) for each similarity scoring method: 'ignoring scores based on fewer than min_match matching peak ks (here: min_match = 10)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] spec2vec: 'spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [abstract] Word2Vec: 'inspired by a natural language processing algorithm—Word2Vec'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Numpy: 'Spec2Vec by making extensive use of Numpy [24] and Numba [25]'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Numba: 'by making extensive use of Numpy [24] and Numba [25], the library'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] Pandas: 'Spec2Vec by making extensive use of Numpy [24] and Numba [25], the library was optimised by making extensive use of Pandas [40]'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] scipy: 'An additional cosine score implementation (Fig C in S3 Text) relies on scipy [41]'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Exact number of spectra used as queries vs. library spectra in the reported library matching experiment is not specified: 'each removed 'query' spectrum was compared to the dataset by only using the Spec2Vec similarity score'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] The specific figure or table location in the paper where library matching true-positive and false-positive rates are reported is not identified in the provided discussion text: 'Here, the performance was assessed based on library matching and unknown compound matching results'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] Minimum matching peaks threshold (min_match) specified for Spec2Vec models in library matching is not explicitly stated in the provided discussion: 'Spec2Vec scores correlate better with structural similarity than cosine-based scores'
- `ev_021` from `agent2_synthesis` (agent2_traced): [discussion] Whether the reported library matching results use the same AllPositive dataset for both training the Word2Vec model and evaluating performance, or use a held-out test set, is not clearly specified: 'A separate Word2Vec model was trained on the remaining data of 76,062 spectra'

## Evaluation Strategy
### Direct Checks
- verify file exists at Zenodo deposit 10.5281/zenodo.3978118 (AllPositive dataset)
- verify AllPositive dataset contains exactly 95,320 spectra or 92,954 spectra with InChIKey as reported in methods
- verify trained Word2Vec models exist at Zenodo deposit zenodo.org/record/4173596 (AllPositive dataset models)
- verify spec2vec Python package (https://github.com/iomega/spec2vec) can be installed and imported
- verify matchms Python package (https://github.com/matchms/matchms) contains cosine and modified cosine implementations
- script_runs: library matching experiment with cosine score (tolerance=0.005, min_match=6) on AllPositive dataset subset
- script_runs: library matching experiment with modified cosine score (tolerance=0.005, min_match=10) on AllPositive dataset subset
- script_runs: library matching experiment with Spec2Vec 15-epoch model on AllPositive dataset subset
- script_runs: library matching experiment with Spec2Vec 50-epoch model on AllPositive dataset subset
- output_matches_reference: true-positive and false-positive rate values from cosine library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from modified cosine library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from Spec2Vec 15-epoch library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- output_matches_reference: true-positive and false-positive rate values from Spec2Vec 50-epoch library matching match reported figure/table location in published paper (multiple defensible rounding approaches)
- file_format_is: AllPositive dataset in JSON or MGF format (standard metabolomics spectrum format)
- field_present: each spectrum in dataset contains required fields for library matching (m/z, intensity, precursor_mz, InChIKey)

### Expert Review
- verify that reported library matching experimental conditions (tolerance and min_match thresholds) are appropriate for LC-MS metabolomics data
- verify that the query spectrum subset and library spectrum subset used in reported results are properly stratified (no leakage between training and test sets)
- assess whether reported true-positive and false-positive rates are consistent with expected performance differences between cosine, modified cosine, and Spec2Vec approaches
- confirm that the 15-epoch and 50-epoch training iterations for Word2Vec models are computationally justified and reasonable for the AllPositive dataset size
- assess whether precursor m/z tolerance (1ppm) used for pre-selection is appropriate for high-resolution LC-MS instruments

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load and filter AllPositive dataset: remove peaks with m/z outside [0, 1000], discard spectra with <10 peaks, remove spectra without InChIKey annotation.
2. Pre-select library candidate spectra using precursor m/z matching (1 ppm tolerance) to reduce computational cost.
3. Compute cosine similarity scores with relative intensity threshold <0.01, tolerance 0.005, and min_match=6; compute modified cosine with tolerance 0.005 and min_match=10.
4. Compute Spec2Vec similarity scores using both 15-epoch and 50-epoch pre-trained Word2Vec models on parent-mass-scaled peak subsets.
5. For each similarity method, rank query spectra and classify hits as true positives (matching planar InChIKey) or false positives (non-matching structure) to construct ROC curves.
6. Calculate true-positive rate, false-positive rate, and area-under-curve for each method and compare against reported paper benchmarks.
7. Validation: ROC curve performance metrics (AUC, TP/FP rates) must show Spec2Vec (especially 50-epoch model) superior to cosine and modified cosine, with lower false-positive rates at equivalent true-positive thresholds, matching patterns reported in the paper.
8. References: source article (DOI: 10.1371/journal.pcbi.1008724)

## Workflow Ports

**Inputs:**

- `allpositive_spectra` — AllPositive dataset (95,320 LC-MS spectra with InChIKey) ← `task_001/spec2vec_scores_allpositive`
- `word2vec_models` — Pre-trained Word2Vec models (15-epoch and 50-epoch AllPositive)
- `matchms_pkg` — matchms Python package (>=0.6.0) for cosine/modified cosine scoring
- `spec2vec_pkg` — spec2vec Python package for Spec2Vec similarity computation

**Outputs:**

- `library_matching_results` — Library matching performance table (TP/FP rates, AUC by method)
- `roc_curves` — ROC curve plots comparing similarity scoring methods
- `performance_metrics` — Quantitative metrics and statistical comparisons

**Used:** `urn:asb:port:task_001/spec2vec_scores_allpositive`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

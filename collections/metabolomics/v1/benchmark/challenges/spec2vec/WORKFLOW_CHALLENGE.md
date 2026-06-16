# Workflow Challenge: `spec2vec_grounded_workflow`


> Spec2Vec is a novel spectral similarity score inspired by Word2Vec that learns fragmental relationships from large MS/MS datasets to better correlate with structural similarity than cosine-based scores. The method enables improved library matching and molecular networking with greater computational scalability.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Spectral similarity scoring is fundamental to metabolomics analyses such as library matching and molecular networking, yet cosine-based scores, the current standard, show only partial correlation with true structural similarity. This work introduces Spec2Vec, which adapts Word2Vec algorithms from natural language processing to learn abstract spectral embeddings from co-occurrences of peaks and neutral losses across large MS/MS datasets. Using GNPS data from approximately 13,000 unique molecules, Spec2Vec similarity scores demonstrate stronger correlation with structural similarity (measured by Tanimoto fingerprint similarity) than cosine or modified cosine scores when evaluated across the top 0.1% of scoring pairs in the UniqueInchikey dataset. In library matching experiments, Spec2Vec achieved notably better true-to-false-positive ratios at all thresholds compared to cosine-based methods, reaching up to 88% accuracy with higher retrieval rates. A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage. The method is computationally more scalable than cosine-based approaches, enabling rapid screening of unknown compounds against large spectral databases and improving clustering performance in molecular network analysis.

## Research questions

- How do Spec2Vec, cosine, and modified cosine similarity scores compare in their correlation with structural similarity when computed across all spectral pairs in the UniqueInchikey dataset?
- How do Spec2Vec similarity scores compare to cosine and modified cosine scores in terms of true-to-false-positive rate during library matching on the AllPositive dataset?
- How does the Spec2Vec method convert a pre-processed MS/MS spectrum into a fixed-length vector representation suitable for efficient similarity comparisons?
- How does the fraction of peak coverage achieved by a Spec2Vec Word2Vec model vary as a function of training corpus size, and can a 97% coverage threshold be reproduced with the AllPositive dataset trained for 15 epochs?

## Methods overview

Load pre-processed spectral datasets (AllPositive: 95,320 spectra; UniqueInchiKeys: 12,797 spectra) from Zenodo. Obtain or train Word2Vec models using gensim (CBOW, window 500, 15–50 epochs, negative sampling=5). Convert all spectra to documents: represent peaks as 'peak@xxx.xx' (2-decimal binning) and add neutral losses ('loss@xxx.xx') between 5.0–200.0 Da. Compute all-pairs Spec2Vec similarities via weighted spectrum vectors (weight = sqrt-normalized intensity) and cosine distance; filter peaks by parent-mass scaling (max_peaks=0.5×parent_mass). Compute all-pairs cosine and modified cosine similarities using matchms with intensity threshold <0.01. Compute all-pairs Tanimoto structural similarity from RDKit daylight fingerprints (2048 bits) for annotated pairs. Rank similarities in descending order, select top 0.1% of pairs, and calculate mean Tanimoto for each method. Validation: mean Tanimoto values for Spec2Vec must exceed those for cosine and modified cosine at top 0.1% percentile, confirming stronger correlation with structural similarity. References: source article (DOI: 10.1371/journal.pcbi.1008724) Load and filter AllPositive dataset: remove peaks with m/z outside [0, 1000], discard spectra with <10 peaks, remove spectra without InChIKey annotation. Pre-select library candidate spectra using precursor m/z matching (1 ppm tolerance) to reduce computational cost. Compute cosine similarity scores with relative intensity threshold <0.01, tolerance 0.005, and min_match=6; compute modified cosine with tolerance 0.005 and min_match=10. Compute Spec2Vec similarity scores using both 15-epoch and 50-epoch pre-trained Word2Vec models on parent-mass-scaled peak subsets. For each similarity method, rank query spectra and classify hits as true positives (matching planar InChIKey) or false positives (non-matching structure) to construct ROC curves. Calculate true-positive rate, false-positive rate, and area-under-curve for each method and compare against reported paper benchmarks. Validation: ROC curve performance metrics (AUC, TP/FP rates) must show Spec2Vec (especially 50-epoch model) superior to cosine and modified cosine, with lower false-positive rates at equivalent true-positive thresholds, matching patterns reported in the paper. References: source article (DOI: 10.1371/journal.pcbi.1008724) Load pre-processed spectra and pre-trained Word2Vec model into memory Tokenize each spectrum: convert peaks to 'peak@xxx.xx' words (2-decimal binning) and neutral losses (5.0–200.0 Da range) to 'loss@xxx.xx' words Retrieve Word2Vec embeddings for all peak and loss words; track unknown words not in vocabulary Compute weighted spectrum vector as sum of embeddings scaled by square root of normalized peak intensity Calculate missing fraction (ratio of intensity from unknown peaks to total intensity) and filter spectra with missing fraction ≥0.05 Validation: confirm spectrum vectors have correct dimensionality (matching Word2Vec embedding size), all vectors are non-zero, and missing fraction metric is computed for every spectrum References: source article (DOI: 10.1371/journal.pcbi.1008724) Load AllPositive dataset (95,320 spectra, pre-filtered to m/z ∈ [0, 1000], ≥10 peaks) and pre-trained Word2Vec model (15 epochs, CBOW, window=500, negative=5). Convert each spectrum to a document: represent peaks as 'peak@xxx.xx' words (2-decimal binning) and add neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words. Normalize peak intensities to maximum = 1 per spectrum; compute missing fraction as 1 − (Σ√w_i for words in model vocabulary) / (Σ√w_i for all words). Aggregate missing-fraction statistics across all spectra and compute mean coverage (1 − mean missing fraction). Vary effective corpus size by progressively adding spectra in order and recompute coverage metrics at each step to generate a corpus-size scaling curve. Validation: verify that final mean coverage reaches ≥97% when corpus includes all 95,320 spectra, matching the reported 97% peak coverage for the AllPositive 15-epoch model; confirm no missing-fraction value exceeds the recommended threshold of 0.05 for ≥95% of spectra. References: source article (DOI: 10.1371/journal.pcbi.1008724)

**Domain:** metabolomics

**Techniques:** spectral-library-matching, molecular-networking, tandem-ms, machine-learning, natural-language-processing, cosine-similarity-scoring

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Spec2Vec is a novel spectral similarity score inspired by Word2Vec, a natural language processing algorithm. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec learns fragmental relationships within a large set of spectral data to derive abstract spectral embeddings. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec scores correlate better with structural similarity than cosine-based scores using data from nearly 13,000 unique molecules. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec is computationally more scalable, allowing structural analogue searches in large databases within seconds. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Cosine-based similarity scores are the most widely used measures of spectral similarity.
- **(finding)** Studies investigating whether molecules with high structural similarity result in spectra with high spectral cosine similarity show only partial support for this relationship.
- **(finding)** Modifications of cosine-based scores have been proposed including raising the m/z and intensity components to different powers and shifting fragment peaks by the difference in precursor m/z.
- **(finding)** Despite limitations of cosine-based methods, no fundamentally different spectral similarity scores have been proposed.
- **(finding)** The AllPositive dataset comprised 95,320 positive ionization mode mass spectra, of which 77,092 had InChIKey annotations. _[grounded: ALLPOSITIVE_DATASET]_
- **(finding)** The UniqueInchikey dataset consisted of 12,797 spectra with unique InChIKeys.
- **(finding)** Spec2Vec spectrum similarity score correlates stronger with structural similarity than cosine or modified cosine scores. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** The poor correlation between cosine and modified cosine similarity scores and structural similarity can largely be explained by high false positive rates.
- **(finding)** Spec2Vec library matching achieved up to 88% accuracy compared to cosine similarity score based library matching. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Training a Spec2Vec model on the UniqueInchikey dataset takes about 30 minutes on an Intel i7-8550U CPU. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Querying 1030 spectra against 76,062 spectra took 140 seconds on an Intel i7-8550U CPU, or 0.14 seconds per query spectrum.
- **(finding)** For 60% of queries for unknown molecules, the top-10 list contained suggested molecules with a structural similarity score of greater than 0.6.
- **(finding)** For molecules with masses larger than 200 Da, Spec2Vec was often able to detect highly related molecules for unknown queries. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec is able to cluster higher fractions of spectra into high structural similarity clusters when compared to the modified cosine score. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Computing spectral similarities between all possible spectra pairs (approximately 82 million unique pairs) took 300 seconds on an Intel i7-8550U CPU using Spec2Vec. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec is an unsupervised method that can be trained on any collection of spectra, independent of whether chemical structures are known. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Peaks in mass spectra have no particular order comparable to word order in a document, so Spec2Vec sets window-size to 500 meaning the entire spectrum counts as context. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Continuous bag of words (CBOW) was generally observed to perform better than skip gram for Spec2Vec. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Model performance for Spec2Vec does not necessarily improve with longer training runs when using negative sampling. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Training a Spec2Vec model with negative sampling (negative = 5) and 15 iterations on AllPositive or up to 50 epochs on UniqueInchikey achieves optimal model performance. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec represents a spectrum as a weighted sum of its fragment and loss word vectors. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** The structural similarity between two molecules was measured using Tanimoto similarity based on daylight-like molecular fingerprints. _[grounded: TANIMOTO_SIMILARITY]_
- **(finding)** Neutral losses between 5.0 and 200.0 Da were added as features in Spec2Vec document representation. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Peaks are represented in Spec2Vec documents with their position up to a defined decimal precision, using a binning of two decimals. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Models trained on AllPositive with 2-decimal binning contained about 97% of all possible peaks and losses. _[grounded: ALLPOSITIVE_DATASET]_
- **(finding)** Spec2Vec is particularly suited to act as a pre-selection funnel for selecting promising candidates for further exploration using computationally more expensive similarity measures. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec can be applied to molecular networking, which is becoming an increasingly popular tool for exploring metabolomic datasets. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** GNPS users can calculate Spec2Vec scores for spectra in their positive ionisation mode datasets using a pretrained model. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Training the Spec2Vec embedding on 95,320 spectra took 40 minutes when training for 15 iterations. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec requires training on a large spectra dataset to work effectively, but this does not necessarily need to be library spectra. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Cosine-based methods are very good at revealing nearly equal spectra but are not well-suited to handle molecules with multiple local chemical modifications.
- **(finding)** Spec2Vec takes relationships between fragments into account rather than relying only on binary assessment of each fragment match. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec is unsupervised and can be trained on any collection of spectra, unlike database searching methods that require known structural information. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** The probability of randomly picking a spectral pair with structural similarity score greater than 0.6 is p = 0.0103.
- **(finding)** Spec2Vec improved performance for larger compounds (greater than 400 Da) is likely explained by the higher number of relevant fragments. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** The current study used a large LC-MS dataset from GNPS containing 154,820 spectra. _[grounded: GNPS_TOOL]_
- **(finding)** After data cleaning and automated lookup, 128,042 out of 154,820 spectra could be linked to an InChIKey. _[grounded: INCHIKEY_ANNOTATION]_
- **(finding)** The AllPositive dataset contains 112,956 spectra with positive ionization mode, of which 92,954 have InChIKey annotations. _[grounded: ALLPOSITIVE_DATASET]_
- **(finding)** All peaks with m/z ratios outside the range [0, 1000] were removed from spectra.
- **(finding)** All spectra with fewer than 10 peaks were discarded from the analysis.
- **(finding)** Different peak filtering procedures were used for Spec2Vec and cosine-based similarity scores to ensure fair comparison. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** For cosine score calculations, all peaks with relative intensities less than 0.01 compared to the highest intensity peak were ignored. _[grounded: COSINE_SCORE]_
- **(finding)** The maximum number of peaks kept per spectrum in Spec2Vec was set to scale linearly with the estimated parent mass. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** Spec2Vec can estimate the impact of unknown words (peaks) by assessing the uncovered weighted part of a spectrum. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** By setting a missing fraction threshold at less than 0.05, Spec2Vec similarity scores for spectra far outside the learned peaks can be avoided. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** A two-step verbatim-first discipline was used to ensure that spectral similarity claims are grounded in the actual data. _[grounded: COSINE_SCORE]_
- **(finding)** The modified cosine score combines matching peak m/z and the m/z shifted by the difference in precursor m/z. _[grounded: COSINE_SCORE]_
- **(finding)** Spec2Vec and modified cosine score matchms packages are freely available and can be installed via conda. _[grounded: SPEC2VEC_SYSTEM]_
- **(finding)** All-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity are available on Zenodo for the UniqueInchikey dataset. _[grounded: COSINE_SCORE]_
- **(finding)** The two most important trained Word2Vec models can be downloaded from Zenodo: one trained on UniqueInchikey and one trained on AllPositive. _[grounded: WORD2VEC_MODEL]_

**Speculative claims (excluded from scoring):**
- **(finding)** Spec2Vec is not meant to be the endpoint but rather the start of a new direction in spectral similarity scoring. _[grounded: SPEC2VEC_SYSTEM]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- cosine-based similarity score
- Modified cosine score can raise m/z and intensity components to different powers and shift fragment peaks
- Cosine and modified cosine scores could be used together with Spec2Vec for library matching
- SIRIUS/CSI:FingerID scores could be combined with Spec2Vec
- In silico fragmentation trees (SIRIUS, IOKR) as computationally more expensive alternative approaches for compound identification
- Hypothetical neutral losses as input to train Spec2Vec model, following approach of Kreitzberg et al.
- Combining Spec2Vec with hypothetical neutral losses concept as proposed by reference [30]
- Continuous Bag of Words (CBOW) vs Skip-gram Word2Vec architecture
- Training with negative sampling vs without negative sampling
- Different peak filtering for Spec2Vec vs cosine-like similarity

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Spec2Vec requires model training on a spectral library; cannot be applied without a training dataset
- Spec2Vec requires training on large reference datasets to capture structural relationships
- Missing words problematic for Spec2Vec models trained on smaller datasets

## Steps

### Step `task_001`
- Title: Reproduce Spec2Vec vs. cosine score structural similarity correlation (Fig 3B average Tanimoto at top 0.1%)
- Task kind: `reproduction`
- Task: Compute all-pairs Spec2Vec, cosine, and modified cosine similarity scores for the AllPositive (95,320 spectra) and UniqueInchiKeys (12,797 spectra) datasets, then extract and report the average Tanimoto structural similarity at the top 0.1% of scores for each method to reproduce Figure 3B.
- Inputs:
  - AllPositive dataset (95,320 spectra with positive ionization mode)
  - UniqueInchiKeys dataset (12,797 spectra with unique InChIKeys, one spectrum per InChIKey)
  - Pre-trained Word2Vec model trained on UniqueInchiKeys dataset
  - Pre-trained Word2Vec model trained on AllPositive dataset
- Expected outputs:
  - All-pairs Spec2Vec similarity score matrix for AllPositive dataset
  - All-pairs cosine similarity score matrix for AllPositive dataset
  - All-pairs modified cosine similarity score matrix for AllPositive dataset
  - All-pairs Spec2Vec similarity score matrix for UniqueInchiKeys dataset
  - All-pairs cosine similarity score matrix for UniqueInchiKeys dataset
  - All-pairs modified cosine similarity score matrix for UniqueInchiKeys dataset
  - Table reporting average Tanimoto structural similarity at top 0.1% of scores for each method (Spec2Vec, cosine, modified cosine) on both datasets
- Tools: Spec2Vec, Word2Vec, matchms, gensim, RDKit, NumPy, Numba, Pandas, scipy
- Landmark output files: allpositive_spectrum_documents.pkl, uniqueinchikeys_spectrum_documents.pkl, spec2vec_similarity_allpositive.npy, cosine_similarity_allpositive.npy, modcos_similarity_allpositive.npy, tanimoto_structural_similarity_allpositive.npy
- Primary expected artifact: `top_0p1_percent_tanimoto_comparison.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce library matching true-to-false-positive performance of Spec2Vec versus cosine scores
- Task kind: `reproduction`
- Task: Reproduce library matching performance results for the AllPositive dataset using cosine, modified cosine, and Spec2Vec similarity scores with reported experimental parameters, computing true-positive and false-positive rates for validation against structural similarity labels.
- Inputs:
  - AllPositive dataset (95,320 positive-mode LC-MS spectra with InChIKey annotations)
  - Pre-trained Word2Vec models (15-epoch and 50-epoch) trained on AllPositive dataset
  - Cosine similarity score implementation from matchms package (>=0.6.0)
  - Modified cosine similarity score implementation from matchms package
- Expected outputs:
  - Library matching results table with true-positive rates, false-positive rates, and area-under-curve for cosine, modified cosine, and Spec2Vec (15-epoch and 50-epoch) similarity scores
  - ROC curves comparing performance of cosine, modified cosine, and Spec2Vec similarity scores on AllPositive library matching task
  - Quantitative performance metrics (TP/FP counts and rates) for each similarity scoring method
- Tools: spec2vec, matchms, Word2Vec, gensim, Numpy, Numba, Pandas, scipy
- Landmark output files: filtered_allpositive_spectra.mgf, cosine_similarity_matrix.csv, modified_cosine_similarity_matrix.csv, spec2vec_similarity_matrix_15epoch.csv, spec2vec_similarity_matrix_50epoch.csv, roc_curves_comparison.png
- Primary expected artifact: `library_matching_performance_results.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Spec2Vec spectrum-document construction and weighted vector aggregation step
- Task kind: `component_reconstruction`
- Task: Convert pre-processed MS/MS spectra into spectrum documents by representing peaks and neutral losses as words, then aggregate pre-trained Word2Vec word vectors into single spectrum vectors via weighted summation, outputting one vector file per spectrum.
- Inputs:
  - Pre-processed MS/MS spectra in mzML, mzXML, or tabular format (m/z, intensity, precursor m/z per spectrum)
  - Pre-trained Word2Vec model (gensim format) from reference dataset (e.g., AllPositive or UniqueInchikey)
- Expected outputs:
  - Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum)
- Tools: Word2Vec, gensim, matchms, spec2vec, Numpy, Numba, Pandas
- Landmark output files: spectrum_documents.json, peak_word_list.txt, spectrum_vectors_raw.csv, missing_fraction_qc.csv
- Primary expected artifact: `spectrum_vectors.h5`

### Step `task_004`
- Depends on: `task_002`
- Title: Analyze missing-fraction metric as a function of training corpus size using the AllPositive dataset
- Task kind: `analysis`
- Task: Compute the missing-fraction statistic across the AllPositive dataset (95,320 spectra) using a Spec2Vec Word2Vec model trained on 15 epochs, measuring the fraction of weighted spectrum intensity not represented in the model as corpus size varies, and reproduce the reported 97% peak coverage result.
- Inputs:
  - AllPositive dataset (95,320 positive ionization mode spectra with InChIKey), filtered to m/z ∈ [0, 1000] and ≥10 peaks
  - Pre-trained Word2Vec model (gensim, CBOW, window-size=500, negative=5, 15 epochs) trained on AllPositive dataset
  - Spec2Vec library (Python package) and matchms ≥0.6.0 for spectrum document conversion and word embedding lookup
- Expected outputs:
  - Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size
  - Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra
  - Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent
- Tools: Spec2Vec, Word2Vec, matchms, gensim, NumPy, Numba, Pandas
- Landmark output files: spectrum_embeddings.npy, missing_fraction_per_spectrum.csv, coverage_vs_corpus_size.csv, coverage_curve.png, coverage_summary_metrics.json
- Primary expected artifact: `missing_fraction_coverage_stats.csv`

## Final expected outputs

- `Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum)` (type: file, tolerance: hash)
- `Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 − missing_fraction), cumulative_corpus_size` (type: file, tolerance: hash)
- `Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra` (type: file, tolerance: hash)
- `Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "spec2vec_grounded_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum)": "<locator>",
    "Missing-fraction statistics table (CSV) with columns: spectrum_id, missing_fraction, coverage (1 \u2212 missing_fraction), cumulative_corpus_size": "<locator>",
    "Coverage-vs-corpus-size curve (PNG/PDF) showing mean peak/loss coverage increasing from 0 to 97% as corpus size grows to 95,320 spectra": "<locator>",
    "Summary metrics JSON: mean_missing_fraction, median_missing_fraction, final_coverage_percent, spectra_with_coverage_above_95_percent": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._

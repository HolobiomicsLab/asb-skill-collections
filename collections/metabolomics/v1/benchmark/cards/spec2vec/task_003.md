# SciTask Card: Reconstruct the Spec2Vec spectrum-document construction and weighted vector aggregation step

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T06:52:35.005391+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_spec2vec`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- DOI: `10.1371/journal.pcbi.1008724`
- GitHub: `matchms/matchms`
- Input from: `task_002`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`, `artificial-intelligence`
- Techniques: `spectral-library-matching`, `molecular-networking`, `tandem-ms`, `machine-learning`, `natural-language-processing`, `cosine-similarity-scoring`
- Keywords: `mass spectrometry fragmentation` · `spectral similarity scoring` · `untargeted metabolomics` · `metabolite identification` · `lc-ms/ms` · `word embeddings` · `natural language processing` · `molecular networks` · `database searching` · `structural annotation` · `cosine similarity` · `ms2 spectra`

## Research Question
How does the Spec2Vec method convert a pre-processed MS/MS spectrum into a fixed-length vector representation suitable for efficient similarity comparisons?

## Connected Finding
Spec2Vec converts spectra into documents by representing each peak as a word ("peak@xxx.xx") and adding neutral losses ("loss@xxx.xx") between 5.0–200.0 Da calculated as precursor − peak. The spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model.

## Task Description
Convert pre-processed MS/MS spectra into spectrum documents by representing peaks and neutral losses as words, then aggregate pre-trained Word2Vec word vectors into single spectrum vectors via weighted summation, outputting one vector file per spectrum.

## Inputs
- Pre-processed MS/MS spectra in mzML, mzXML, or tabular format (m/z, intensity, precursor m/z per spectrum)
- Pre-trained Word2Vec model (gensim format) from reference dataset (e.g., AllPositive or UniqueInchikey)

## Expected Outputs
- Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum)

## Expected Output File

- `spectrum_vectors.h5`

## Landmark Outputs

- `spectrum_documents.json`
- `peak_word_list.txt`
- `spectrum_vectors_raw.csv`
- `missing_fraction_qc.csv`

## Tools
- Word2Vec
- gensim
- matchms
- spec2vec
- Numpy
- Numba
- Pandas

## Skills
- mass-spectrometry-spectrum-tokenization
- word-embedding-aggregation-for-spectral-data
- neutral-loss-calculation-from-precursor
- word2vec-vocabulary-matching-and-unknown-peak-handling
- spectral-vector-normalization-by-intensity
- missing-fraction-quality-filtering-for-embeddings

## Workflow Description
1. Load pre-processed MS/MS spectra and a pre-trained Word2Vec model (trained on reference dataset). 2. For each spectrum, represent every peak as a word in the form 'peak@xxx.xx' using 2-decimal binning of m/z values. 3. Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0 and 200.0 Da and represent each as 'loss@xxx.xx'. 4. Assemble all peak and loss words into a spectrum document. 5. For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity. 6. Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05. 7. Save the resulting spectrum vectors to a named output file (e.g., CSV or HDF5 with spectrum identifier and vector components).

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `spec2vec.pdf` | main_article | True |

## Missing Information
- Exact Word2Vec embedding dimensionality is not specified; article refers to pre-trained models but does not state vector dimension
- Precise weighted summation formula for aggregating word vectors into spectrum vector is not provided; method description states aggregation occurs but does not give mathematical formulation
- Specification of peak decimal precision for peak@xxx.xx token generation is not stated numerically; only that peaks are represented 'up to a defined decimal precision'
- Handling of spectrum vectors with unknown peaks (peaks absent from trained Word2Vec model) during aggregation is described qualitatively but no algorithm for missing word imputation is provided

## Domain Knowledge
- Spectrum documents represent MS/MS spectra as ordered word lists; peaks are discretized to 2 decimal places (e.g., m/z 200.445 becomes 'peak@200.45') to create vocabulary consistency across spectra.
- Neutral losses encode fragmentation pathways as words ('loss@xxx.xx') and are calculated only within the range 5.0–200.0 Da to exclude noise and background; losses outside this range are discarded.
- Spectrum vectors aggregate word embeddings using weighted summation where weights are the square root of normalized peak intensity; this non-linear weighting emphasizes high-intensity ions while avoiding saturation.
- The missing fraction threshold (typically 0.05) filters out spectra whose unknown peaks comprise ≥5% of total weighted intensity, ensuring reliable similarity scoring when peaks fall outside the trained Word2Vec vocabulary.
- Word2Vec window size is set to 500 (effectively the entire spectrum) because peaks in mass spectra have no inherent order comparable to natural language, unlike sequential text documents.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] How does the Spec2Vec method convert a pre-processed MS/MS spectrum into a fixed-length vector representation suitable for efficient similarity comparisons?: 'A spectrum can then be represented by a low-dimensional vector calculated as the weighted sum of all its fragment (and loss) vectors'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] Spec2Vec converts spectra into documents by representing each peak as a word ("peak@xxx.xx") and adding neutral losses ("loss@xxx.xx") between 5.0–200.0 Da calculated as precursor − peak. The spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model.: 'every peak is represented by a word that contains its position up to a defined decimal precision ("peak@xxx.xx"). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Pre-processed MS/MS spectra in mzML, mzXML, or tabular format (m/z, intensity, precursor m/z per spectrum): 'After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained Word2Vec model (gensim format) from reference dataset (e.g., AllPositive or UniqueInchikey): 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Spectrum vector file containing spectrum identifiers and their corresponding Word2Vec-aggregated embedding vectors (one vector per spectrum): 'v_S = ∑_{i=1}^{n} √w_i · v_i, with w_i the intensity (normalized to maximum intensity = 1) and v_i the word vector of peak i'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Word2Vec: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31]'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] spec2vec: 'spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Numpy: 'by making extensive use of Numpy [24] and Numba [25]'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Numba: 'by making extensive use of Numpy [24] and Numba [25]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Pandas: 'using Pandas [40]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] Exact Word2Vec embedding dimensionality is not specified; article refers to pre-trained models but does not state vector dimension: 'The two most important trained Word2Vec models used in this work can be downloaded from https://doi.org/10.5281/zenodo.3978054'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Precise weighted summation formula for aggregating word vectors into spectrum vector is not provided; method description states aggregation occurs but does not give mathematical formulation: 'After processing, spectra are converted to documents. For this, every peak is represented by a word'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Specification of peak decimal precision for peak@xxx.xx token generation is not stated numerically; only that peaks are represented 'up to a defined decimal precision': 'every peak is represented by a word that contains its position up to a defined decimal precision'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] Handling of spectrum vectors with unknown peaks (peaks absent from trained Word2Vec model) during aggregation is described qualitatively but no algorithm for missing word imputation is provided: 'In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact'

## Evaluation Strategy
### Direct Checks
- verify file exists: spec2vec repository (https://github.com/iomega/spec2vec) contains source code for spectrum-to-vector encoding
- verify file exists: matchms repository (https://github.com/matchms/matchms) contains peak and neutral-loss word generation implementations
- script_runs: execute spectrum preprocessing and document generation on sample spectrum from AllPositive dataset (10.5281/zenodo.3978118) using spec2vec package; verify output contains peak@xxx.xx and loss@xxx.xx word tokens
- output_matches_reference: generated spectrum document tokens match expected format (peak@xxx.xx with precision and loss@xxx.xx with range 5.0–200.0 Da), multiple defensible precision choices robust to parameter choices
- file_format_is: trained Word2Vec model file downloaded from 10.5281/zenodo.3978054 or zenodo.org/record/4173596 is in standard gensim/word2vec format readable by Python Word2Vec libraries
- value_in_range: spectrum vector dimensionality matches Word2Vec embedding dimension (no canonical answer; article does not specify, requires parameter specification)
- file_exists: output spectrum vector file per input spectrum exists with consistent naming convention and format (e.g., .npy, .csv, or binary vector)

### Expert Review
- verify that weighted summation aggregation strategy (sum of word vectors weighted by peak intensity) is correctly implemented according to methods description and produces interpretable spectrum embeddings
- assess whether treatment of unknown peaks (peaks not in trained Word2Vec vocabulary) is correctly implemented via missing fraction assessment as described in methods
- evaluate whether maximum peak filtering (max(n_peaks) = 0.5 × parentmass) is correctly applied during document generation and does not remove peaks incorrectly
- assess correctness of neutral loss calculation (precursor − peak) and filtering (5.0–200.0 Da range) in document generation stage
- verify that spectrum vector aggregation preserves structural relationship information required for downstream similarity scoring, e.g., by spot-checking similarity between structurally similar pairs

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load pre-processed spectra and pre-trained Word2Vec model into memory
2. Tokenize each spectrum: convert peaks to 'peak@xxx.xx' words (2-decimal binning) and neutral losses (5.0–200.0 Da range) to 'loss@xxx.xx' words
3. Retrieve Word2Vec embeddings for all peak and loss words; track unknown words not in vocabulary
4. Compute weighted spectrum vector as sum of embeddings scaled by square root of normalized peak intensity
5. Calculate missing fraction (ratio of intensity from unknown peaks to total intensity) and filter spectra with missing fraction ≥0.05
6. Validation: confirm spectrum vectors have correct dimensionality (matching Word2Vec embedding size), all vectors are non-zero, and missing fraction metric is computed for every spectrum
7. References: source article (DOI: 10.1371/journal.pcbi.1008724)

## Workflow Ports

**Inputs:**

- `preprocessed_spectra` — Pre-processed MS/MS spectra ← `task_002/library_matching_results`
- `trained_word2vec_model` — Pre-trained Word2Vec model

**Outputs:**

- `spectrum_vectors` — Spectrum vector embeddings

**Used:** `urn:asb:port:task_002/library_matching_results`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

# SciTask Card: Reproduce Spec2Vec vs. cosine score structural similarity correlation (Fig 3B average Tanimoto at top 0.1%)

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T06:52:35.005391+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_spec2vec`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`, `modeling`
- DOI: `10.1371/journal.pcbi.1008724`
- GitHub: `matchms/matchms`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`, `artificial-intelligence`
- Techniques: `spectral-library-matching`, `molecular-networking`, `tandem-ms`, `machine-learning`, `natural-language-processing`, `cosine-similarity-scoring`
- Keywords: `mass spectrometry fragmentation` · `spectral similarity scoring` · `untargeted metabolomics` · `metabolite identification` · `lc-ms/ms` · `word embeddings` · `natural language processing` · `molecular networks` · `database searching` · `structural annotation` · `cosine similarity` · `ms2 spectra`

## Research Question
How do Spec2Vec, cosine, and modified cosine similarity scores compare in their correlation with structural similarity when computed across all spectral pairs in the UniqueInchikey dataset?

## Connected Finding
Spec2Vec similarity scores correlate stronger with structural similarity than cosine or modified cosine scores when evaluated at the top 0.1% of scoring pairs in the UniqueInchikey dataset.

## Task Description
Compute all-pairs Spec2Vec, cosine, and modified cosine similarity scores for the AllPositive (95,320 spectra) and UniqueInchiKeys (12,797 spectra) datasets, then extract and report the average Tanimoto structural similarity at the top 0.1% of scores for each method to reproduce Figure 3B.

## Inputs
- AllPositive dataset (95,320 spectra with positive ionization mode)
- UniqueInchiKeys dataset (12,797 spectra with unique InChIKeys, one spectrum per InChIKey)
- Pre-trained Word2Vec model trained on UniqueInchiKeys dataset
- Pre-trained Word2Vec model trained on AllPositive dataset

## Expected Outputs
- All-pairs Spec2Vec similarity score matrix for AllPositive dataset
- All-pairs cosine similarity score matrix for AllPositive dataset
- All-pairs modified cosine similarity score matrix for AllPositive dataset
- All-pairs Spec2Vec similarity score matrix for UniqueInchiKeys dataset
- All-pairs cosine similarity score matrix for UniqueInchiKeys dataset
- All-pairs modified cosine similarity score matrix for UniqueInchiKeys dataset
- Table reporting average Tanimoto structural similarity at top 0.1% of scores for each method (Spec2Vec, cosine, modified cosine) on both datasets

## Expected Output File

- `top_0p1_percent_tanimoto_comparison.csv`

## Landmark Outputs

- `allpositive_spectrum_documents.pkl`
- `uniqueinchikeys_spectrum_documents.pkl`
- `spec2vec_similarity_allpositive.npy`
- `cosine_similarity_allpositive.npy`
- `modcos_similarity_allpositive.npy`
- `tanimoto_structural_similarity_allpositive.npy`

## Tools
- Spec2Vec
- Word2Vec
- matchms
- gensim
- RDKit
- NumPy
- Numba
- Pandas
- scipy

## Skills
- spectral-similarity-scoring-computation
- word2vec-embedding-training-mass-spectrometry
- peak-intensity-normalization-weighted-aggregation
- molecular-fingerprint-structural-similarity-tanimoto
- spectrum-document-conversion-peak-loss-representation
- neutral-loss-annotation-interpretation
- large-scale-all-pairs-similarity-benchmarking

## Workflow Description
1. Load pre-processed AllPositive and UniqueInchiKeys spectral datasets from Zenodo (10.5281/zenodo.3978118). 2. Load or train Word2Vec models: retrieve pre-trained models from Zenodo (10.5281/zenodo.3978054 for UniqueInchiKeys, zenodo.org/record/4173596 for AllPositive) or train from scratch using CBOW with window-size 500, negative sampling (negative=5), 15–50 epochs on spectrum documents. 3. Convert all spectra to documents by representing peaks as 'peak@xxx.xx' words (binning 2 decimals) and adding neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words. 4. For Spec2Vec: compute all-pairs spectrum vector similarities using weighted sum of word embeddings (weight = normalized intensity, sqrt applied), then cosine distance; filter peaks by parent mass scaling (max_peaks = 0.5 × parent_mass) and apply missing-fraction threshold (<0.05). 5. For cosine and modified cosine scores: remove peaks with relative intensity <0.01 of highest peak and compute using matchms; modified cosine additionally matches peaks shifted by precursor m/z difference. 6. Compute structural similarity (Tanimoto/Jaccard) on daylight-like fingerprints (RDKit, 2048 bits) for all spectrum pairs with InChIKey annotations. 7. Rank all-pairs similarities by score descending, extract top 0.1% of pairs, and calculate mean Tanimoto similarity for each method; output results as comparison table.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `spec2vec.pdf` | main_article | True |

## Missing Information
- Exact spectral count and composition details for the AllPositive dataset used in this specific analysis (e.g., confirmation that 95,320 spectra were used and breakdown by ionization mode, source, or acquisition instrument)
- Explicit description of how the Tanimoto similarity ground-truth labels were generated from InChIKeys or molecular structures for evaluating Figure 3B results
- Confirmation that the Word2Vec embedding dimensionality, window size, and other hyperparameters used for training on both AllPositive and UniqueInchiKeys datasets are documented and reproducible
- Detailed specification of the threshold or method used to determine which spectra pairs constitute the 'top 0.1%' of similarity scores and whether this is computed separately for each method or using a unified ranking
- Documentation of any post-processing steps, outlier removal, or filtering applied to the computed similarity scores before computing average Tanimoto similarity at the top 0.1% threshold

## Domain Knowledge
- Spec2Vec weights spectrum vectors as weighted sums of word embeddings using square-root-normalized peak intensities to account for the dependency between peak relevance and signal magnitude.
- Neutral losses are calculated as precursor m/z minus fragment peak m/z and must fall within 5.0–200.0 Da to be added as informative contextual features to spectrum documents.
- Peak filtering differs between Spec2Vec (parent-mass-scaled to max_peaks=0.5×parent_mass) and cosine-based scores (intensity threshold <0.01 of max) because Spec2Vec models larger molecules as producing more meaningful fragmentation peaks; this difference is necessary to avoid unfair comparison.
- Tanimoto similarity (Jaccard index) on daylight-like molecular fingerprints (2048 bits) serves as ground truth for structural similarity and is computed only for spectrum pairs with valid InChIKey annotations.
- The top 0.1% percentile of similarity scores is the target high-confidence subset for measuring correlation with structural similarity; this threshold reflects the most confident candidate matches in library searching.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: All-pairs Spec2Vec similarity score matrix for AllPositive dataset, All-pairs cosine similarity score matrix for AllPositive dataset, All-pairs modified cosine similarity score matrix for AllPositive dataset.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How do Spec2Vec, cosine, and modified cosine similarity scores compare in their correlation with structural similarity when computed across all spectral pairs in the UniqueInchikey dataset?: 'Comparing the average structural similarity over the highest 0.1% of each respective spectra similarity score, with 0.1% corresponding to about 80,000 spectra pairs.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Spec2Vec similarity scores correlate stronger with structural similarity than cosine or modified cosine scores when evaluated at the top 0.1% of scoring pairs in the UniqueInchikey dataset.: 'This reveals that a high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores (Fig 3).'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AllPositive dataset (95,320 spectra with positive ionization mode): 'The here used subset contains all spectra with positive ionization mode containing 112,956 spectra, out of which 92,954 with InChIKey'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] UniqueInchiKeys dataset (12,797 spectra with unique InChIKeys, one spectrum per InChIKey): 'We also worked with the considerably smaller subset UniqueInchiKeys which was reduced on purpose to be accessible for extensive benchmarking. It contains only one spectrum for every unique InChIKey'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained Word2Vec model trained on UniqueInchiKeys dataset: 'The two most important trained Word2Vec models used in this work can be downloaded from https://doi.org/10.5281/zenodo.3978054 (trained on UniqueInchikey dataset)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Pre-trained Word2Vec model trained on AllPositive dataset: 'https://zenodo.org/record/4173596 (trained on AllPositive dataset)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] All-pairs Spec2Vec similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] All-pairs cosine similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] All-pairs modified cosine similarity score matrix for AllPositive dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] All-pairs Spec2Vec similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset can be found on'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] All-pairs cosine similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] All-pairs modified cosine similarity score matrix for UniqueInchiKeys dataset: 'Calculated all-vs-all similarity score matrices for cosine score, modified cosine score, and fingerprint-based similarity y (Tanimoto) for the UniqueInchikey dataset'
- `ev_013` from `agent2_synthesis` (agent2_traced): [results] Table reporting average Tanimoto structural similarity at top 0.1% of scores for each method (Spec2Vec, cosine, modified cosine) on both datasets: 'high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores'
- `ev_014` from `agent2_synthesis` (agent2_traced): [abstract] Spec2Vec: 'we introduce Spec2Vec, a novel spectral similarity score'
- `ev_015` from `agent2_synthesis` (agent2_traced): [abstract] Word2Vec: 'inspired by a natural language processing algorithm—Word2Vec'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] matchms: 'the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] gensim: 'A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]'
- `ev_018` from `agent2_synthesis` (agent2_traced): [methods] RDKit: 'Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints, version 2020.03.2, 2048 bits, derived using rdkit'
- `ev_019` from `agent2_synthesis` (agent2_traced): [methods] NumPy: 'Spec2Vec was optimised by making extensive use of Numpy [24]'
- `ev_020` from `agent2_synthesis` (agent2_traced): [methods] Numba: 'making extensive use of Numpy [24] and Numba [25]'
- `ev_021` from `agent2_synthesis` (agent2_traced): [methods] Pandas: 'Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]'
- `ev_022` from `agent2_synthesis` (agent2_traced): [methods] scipy: 'An additional cosine score implementation [in S3 Text] relies on scipy [41]'
- `ev_023` from `agent2_synthesis` (agent2_traced): [discussion] Exact spectral count and composition details for the AllPositive dataset used in this specific analysis (e.g., confirmation that 95,320 spectra were used and breakdown by ionization mode, source, or acquisition instrument): 'the remaining AllPositive dataset comprised 95,320 positive ionization mode mass spectra'
- `ev_024` from `agent2_synthesis` (agent2_traced): [discussion] Explicit description of how the Tanimoto similarity ground-truth labels were generated from InChIKeys or molecular structures for evaluating Figure 3B results: 'No explicit reference in provided discussion text to Tanimoto similarity computation method; EnrichedIndex references structural similarity but not Tanimoto derivation specifics'
- `ev_025` from `agent2_synthesis` (agent2_traced): [discussion] Confirmation that the Word2Vec embedding dimensionality, window size, and other hyperparameters used for training on both AllPositive and UniqueInchiKeys datasets are documented and reproducible: 'No explicit statement of Word2Vec hyperparameters in provided discussion section'
- `ev_026` from `agent2_synthesis` (agent2_traced): [discussion] Detailed specification of the threshold or method used to determine which spectra pairs constitute the 'top 0.1%' of similarity scores and whether this is computed separately for each method or using a unified ranking: 'Discussion section does not explicitly define the top 0.1% selection criterion or percentile computation methodology'
- `ev_027` from `agent2_synthesis` (agent2_traced): [discussion] Documentation of any post-processing steps, outlier removal, or filtering applied to the computed similarity scores before computing average Tanimoto similarity at the top 0.1% threshold: 'Discussion section does not detail post-scoring filtering or outlier handling for Figure 3B analysis'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that AllPositive dataset is accessible at https://doi.org/10.5281/zenodo.3978118 or https://zenodo.org/record/4173596
- file_exists: verify that UniqueInchiKeys dataset is accessible at https://doi.org/10.5281/zenodo.3978118
- file_exists: verify that pre-trained Word2Vec models are accessible at https://doi.org/10.5281/zenodo.3978054 (UniqueInchikey) and https://zenodo.org/record/4173596 (AllPositive)
- file_exists: verify that matchms package implementation is accessible at https://github.com/matchms/matchms
- file_exists: verify that spec2vec package is accessible at https://github.com/iomega/spec2vec
- script_runs: verify that cosine, modified cosine, and Spec2Vec similarity score calculations execute without error on both AllPositive and UniqueInchiKeys datasets
- value_in_range: verify that computed similarity scores fall within [0.0, 1.0] for all three methods
- row_count_equals: verify that the number of spectral pairs evaluated matches the expected pairwise combinations for each dataset (robust to parameter choices in preprocessing)
- output_matches_reference: verify that average Tanimoto similarity at top 0.1% of scores for cosine, modified cosine, and Spec2Vec methods matches the values reported in Figure 3B of the published article (exact byte-for-byte match for reported numerical values)
- field_present: verify that output similarity matrices or score rankings contain at least three columns corresponding to cosine score, modified cosine score, and Spec2Vec score

### Expert Review
- Confirm that the filtering strategy applied to both datasets (removal of spectra with <10 fragments, filtering by m/z range [0, 1000], relative intensity threshold <0.01, and parent mass scaling for peak retention) matches the methods described in the paper
- Confirm that the top 0.1% percentile threshold is correctly computed and applied identically across all three similarity scoring methods
- Confirm that Tanimoto similarity values computed from structural fingerprints (InChIKey-based or RDKit-derived) represent the ground-truth structural similarity metric and are correctly paired with spectra
- Assess whether observed Tanimoto similarity distributions at top 0.1% of scores demonstrate the expected pattern: Spec2Vec scores should show higher average Tanimoto than cosine and modified cosine, consistent with the paper's reported advantage in capturing structural relationships
- Confirm that neutral losses are correctly calculated as precursor m/z minus peak m/z and are properly encoded as 'loss@xxx.xx' features in the Word2Vec training corpus

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Load pre-processed spectral datasets (AllPositive: 95,320 spectra; UniqueInchiKeys: 12,797 spectra) from Zenodo.
2. Obtain or train Word2Vec models using gensim (CBOW, window 500, 15–50 epochs, negative sampling=5).
3. Convert all spectra to documents: represent peaks as 'peak@xxx.xx' (2-decimal binning) and add neutral losses ('loss@xxx.xx') between 5.0–200.0 Da.
4. Compute all-pairs Spec2Vec similarities via weighted spectrum vectors (weight = sqrt-normalized intensity) and cosine distance; filter peaks by parent-mass scaling (max_peaks=0.5×parent_mass).
5. Compute all-pairs cosine and modified cosine similarities using matchms with intensity threshold <0.01.
6. Compute all-pairs Tanimoto structural similarity from RDKit daylight fingerprints (2048 bits) for annotated pairs.
7. Rank similarities in descending order, select top 0.1% of pairs, and calculate mean Tanimoto for each method.
8. Validation: mean Tanimoto values for Spec2Vec must exceed those for cosine and modified cosine at top 0.1% percentile, confirming stronger correlation with structural similarity.
9. References: source article (DOI: 10.1371/journal.pcbi.1008724)

## Workflow Ports

**Inputs:**

- `allpositive_spectra` — AllPositive dataset (95,320 spectra with positive ionization mode)
- `uniqueinchikeys_spectra` — UniqueInchiKeys dataset (12,797 spectra with unique InChIKeys)
- `word2vec_model_uniqueinchikeys` — Pre-trained Word2Vec model (UniqueInchiKeys)
- `word2vec_model_allpositive` — Pre-trained Word2Vec model (AllPositive)

**Outputs:**

- `spec2vec_scores_allpositive` — All-pairs Spec2Vec similarity matrix (AllPositive)
- `cosine_scores_allpositive` — All-pairs cosine similarity matrix (AllPositive)
- `modcos_scores_allpositive` — All-pairs modified cosine similarity matrix (AllPositive)
- `spec2vec_scores_uniqueinchikeys` — All-pairs Spec2Vec similarity matrix (UniqueInchiKeys)
- `cosine_scores_uniqueinchikeys` — All-pairs cosine similarity matrix (UniqueInchiKeys)
- `modcos_scores_uniqueinchikeys` — All-pairs modified cosine similarity matrix (UniqueInchiKeys)
- `structural_similarity_scores` — All-pairs Tanimoto structural similarity (fingerprint-based)
- `top_percentile_comparison` — Mean Tanimoto similarity at top 0.1% of scores for each method

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

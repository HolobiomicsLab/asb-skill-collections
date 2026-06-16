# SciTask Card: Reproduce the IOKR BGC-spectrum scoring on the MIBiG-GNPS paired dataset

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:56:40.523217+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_nplinker`
- Domain: `bioinformatics`
- Subtask categories: `model-training`, `benchmark-evaluation`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1008920`
- GitHub: `NPLinker/nplinker`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `natural-products`, `microbiome-metabolomics`, `multi-omics-integration`
- Techniques: `correlation-analysis`, `machine-learning`, `database-annotation`, `network-annotation-propagation`

## Research Question
What is the distribution of IOKR scores across all 2966 MIBiG-GNPS BGC-spectrum pairs, and how do validated links rank within this distribution?

## Connected Finding
IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534 compared to a random baseline AUC of 0.5209.

## Task Description
Train the Input-Output Kernel Regression (IOKR) model on 4138 GNPS library spectra with structural annotations, apply it to score 2966 MIBiG-GNPS BGC-spectrum pairs, and reproduce the distribution of IOKR scores showing the position of validated links as reported in Table 3 and supplementary figures.

## Inputs
- GNPS library MS2 spectra with structural annotations (4138 spectra)
- MIBiG database entries with structural annotations (SMILES/InChI format)
- MIBiG-GNPS paired BGC-spectrum dataset (2966 pairs)
- MS2 spectral data from GNPS for evaluation (6246 spectra restricted to those with structure predictions)

## Expected Outputs
- IOKR model object with learned mapping from MS2 spectrum kernel space to molecular fingerprint space
- Ranked list of candidate BGCs for each of 2966 MS2 spectra with IOKR scores
- Top-n accuracy metrics (top-1, top-5, top-10, top-20, top-200) and AUC score for IOKR on MIBiG-GNPS pairs
- Distribution histogram of IOKR scores for all 2966 BGC-spectrum pairs with validated links highlighted
- Mean IOKR score for all links (0.0105) and for validated links (0.0364) with statistical significance (p-value)

## Expected Output File

- `iokr_performance_table.csv`

## Landmark Outputs

- `fingerprints_extracted.csv`
- `iokr_model_trained.pkl`
- `ranked_bgcs_per_spectrum.csv`
- `top_n_accuracy_metrics.csv`
- `iokr_score_distribution.png`

## Tools
- GNPS
- MIBiG
- Chemistry Development Kit (CDK)
- Probability Product Kernel (PPK)
- antiSMASH

## Skills
- kernel-regression-learning-from-spectral-fingerprint-pairs
- molecular-fingerprint-extraction-and-vectorization
- bgc-spectrum-ranking-by-kernel-similarity
- spectral-denoising-via-training-data-filtering
- top-n-accuracy-and-auc-metric-calculation
- score-distribution-analysis-and-statistical-significance-testing

## Workflow Description
1. Load the GNPS library training set (4138 spectra with structural annotations) and extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for each annotated metabolite. 2. Construct the IOKR model by learning a mapping from the spectrum kernel space (X, with kernel K_x) to the molecular fingerprint space (F) using the training pairs, implementing operator-valued kernel regression with the paired spectrum-fingerprint training sets. 3. Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step. 4. For the 6246 MS2 spectra in the MIBiG/GNPS evaluation set, apply the trained IOKR model to predict molecular fingerprints and rank candidate BGCs (restricted to 2242 BGCs with MIBiG homology assignments) by computing the inner product ⟨ĥ(spectrum), φ(BGC_candidate)⟩ in fingerprint space. 5. Construct 2966 BGC-spectrum pairs by matching MIBiG entries to GNPS spectra using the first part of the InChIKey to avoid confounding by stereoisomerism. 6. Calculate top-n accuracy (n=1,5,10,20,200) and area-under-curve (AUC) by comparing the rank of the correct BGC relative to all ranked candidates for each spectrum, and compare against a randomized baseline. 7. Generate distribution histograms of IOKR scores for all 2966 pairs and overlay positions of validated links, reporting mean scores, p-values, and visual confirmation against reported S2 Fig and Table 3 results.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `nplinker.pdf` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000078836` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836 | Cs a number of strains for the st From this platform we con MSV000078836 [38], MSV Cru¨semann, Gross and Leã The Cru¨semann data set |
| massive | `MSV000085038` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038 | ets each with numerous validated links: V000085018 [39] and MSV000085038 [40], hereafter referred to as ão, respectively. et consist |

## Missing Information
- exact kernel function type (e.g., Probability Product Kernel, polynomial, RBF) and hyperparameter values (bandwidth, degree) used for IOKR model training on GNPS 4138-spectrum set
- specific molecular fingerprint type, dimensionality, and construction method (e.g., Morgan fingerprints, MACCS keys, CDK fingerprints, radius/bit-length parameters) used in IOKR scoring
- detailed denoising/filtering procedure applied to spectra before IOKR training and scoring (peak intensity threshold, noise removal method, spectral normalization protocol)
- number of training spectra retained after peak filtering step (spectra with peaks found in training data only) before IOKR model fitting
- exact cross-validation or train-test split strategy used for IOKR model development on GNPS training set; whether performance metrics in Table 3 are from held-out test set or resubstitution
- computational resource requirements and runtime for IOKR model training on 4138-spectrum set and scoring 2966 pairs (memory, CPU/GPU time, software version specifics)

## Domain Knowledge
- IOKR maps input spectra to fingerprint space via kernel functions; the rank of the correct BGC candidate among all ranked candidates determines top-n accuracy.
- Molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) are binary vectors encoding presence/absence of chemical substructures and must be concatenated to form the composite feature representation.
- The Probability Product Kernel (PPK) filters training spectra to include only peaks found in the GNPS training library, reducing noise and potential bias toward the training set composition.
- InChIKey matching (first part only) is used to avoid spurious distinctions based on stereoisomerism when pairing MIBiG entries to GNPS spectra; this yields 2966 pairs from 2069 unique spectra and 242 unique BGCs.
- Statistical significance is assessed by comparing IOKR's top-n accuracy (e.g., 0.1208 at top-1) against a randomized baseline (0.0 at top-1), with AUC of 0.6534 versus 0.5209 for the baseline indicating substantial model performance.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] What is the distribution of IOKR scores across all 2966 MIBiG-GNPS BGC-spectrum pairs, and how do validated links rank within this distribution?: 'The MIBiG/GNPS data set consists of sets of associated BGC, metabolite and spectrum... we tested the method on the paired MIBiG/GNPS data by matching each spectrum to the candidate set consisting of'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9), with top-1 accuracy of 0.1208, top-5 accuracy of 0.1708, and AUC of 0.6534 compared to a random baseline AUC of 0.5209.: 'IOKR: 0.0105 (all), 0.0364 (validated), p-value 1.7968 × 10−9... Table 3 shows the top-n performance of IOKR: top-1: 0.1208, top-5: 0.1708, top-10: 0.1870... AUC of 0.6534 compared to 0.5209 for the'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] GNPS library MS2 spectra with structural annotations (4138 spectra): 'we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model. We use the same training data set as Brouard and co-workers [26], which'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] MIBiG database entries with structural annotations (SMILES/InChI format): 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]. The fingerprint vector is composed of three concatenated sets of fingerprints: CDK Substructure,'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] MIBiG-GNPS paired BGC-spectrum dataset (2966 pairs): 'This yields 2966 BGC-spectrum pairs, each with an associated metabolite, which can be used to evaluate the IOKR model proposed in this paper. These pairs include 2069 unique spectra and 242 unique'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] MS2 spectral data from GNPS for evaluation (6246 spectra restricted to those with structure predictions): 'Out of 3316 BGCs in the data set, 2242 could be assigned structure based on similarity to MIBiG entries, and used as candidate set for the 6246 MS2 spectra in the data set'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] IOKR model object with learned mapping from MS2 spectrum kernel space to molecular fingerprint space: 'This mapping, along with the function mapping molecular structures to fingerprints, is then used to project similarities in the input space of spectra and the output space (molecular structures) to'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Ranked list of candidate BGCs for each of 2966 MS2 spectra with IOKR scores: 'For each spectrum, IOKR returns an ordered list of all metabolites in the candidate set'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Top-n accuracy metrics (top-1, top-5, top-10, top-20, top-200) and AUC score for IOKR on MIBiG-GNPS pairs: 'Table 3 shows the top-n performance of IOKR, i.e. how often the 'true' BGC match for a given spectrum is among the top n matches returned by IOKR, for a selection of n'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Distribution histogram of IOKR scores for all 2966 BGC-spectrum pairs with validated links highlighted: 'we can observe the distribution of the scores for the validated links among the scores for all potential links. The upper end of the distribution for the IOKR score contains a relatively high'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Mean IOKR score for all links (0.0105) and for validated links (0.0364) with statistical significance (p-value): 'the mean score of 0.0105 for all links and 0.0364 for validated links (Table 1). Results for other data sets can be found in Table C in S1 Text'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] GNPS: 'we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] MIBiG: 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Chemistry Development Kit (CDK): 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Probability Product Kernel (PPK): 'we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] antiSMASH: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] exact kernel function type (e.g., Probability Product Kernel, polynomial, RBF) and hyperparameter values (bandwidth, degree) used for IOKR model training on GNPS 4138-spectrum set: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] specific molecular fingerprint type, dimensionality, and construction method (e.g., Morgan fingerprints, MACCS keys, CDK fingerprints, radius/bit-length parameters) used in IOKR scoring: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'
- `ev_019` from `agent2_synthesis` (agent2_traced): [abstract] detailed denoising/filtering procedure applied to spectra before IOKR training and scoring (peak intensity threshold, noise removal method, spectral normalization protocol): 'As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra'
- `ev_020` from `agent2_synthesis` (agent2_traced): [abstract] number of training spectra retained after peak filtering step (spectra with peaks found in training data only) before IOKR model fitting: 'we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)'
- `ev_021` from `agent2_synthesis` (agent2_traced): [results] exact cross-validation or train-test split strategy used for IOKR model development on GNPS training set; whether performance metrics in Table 3 are from held-out test set or resubstitution: 'The training set used to build the IOKR model includes metabolites from sources other than microbial'
- `ev_022` from `agent2_synthesis` (agent2_traced): [methods] computational resource requirements and runtime for IOKR model training on 4138-spectrum set and scoring 2966 pairs (memory, CPU/GPU time, software version specifics): '[not present in provided section text]'

## Evaluation Strategy
### Direct Checks
- verify file exists: NPLinker repository at https://github.com/sdrogers/nplinker or Zenodo deposit http://doi.org/10.5281/zenodo.4680579
- verify input dataset exists: GNPS training set with 4138 spectra (accessible via GNPS public library or supplementary data S1 Data)
- verify input dataset exists: MIBiG-GNPS paired dataset with 2966 validated BGC-spectrum links from S1 Data
- script_runs: IOKR model training pipeline on GNPS 4138-spectrum training set with default or specified kernel parameters completes without error
- file_exists and file_format_is: IOKR model checkpoint or serialized object (e.g., pickle, joblib, HDF5) produced after training
- script_runs: IOKR scoring script applied to 2966 MIBiG-GNPS BGC-spectrum pairs produces score matrix with shape (2966,) or equivalent
- file_format_is: output score vector is numeric array or table (CSV/TSV) with one score per pair, no missing values
- row_count_equals: output score table has exactly 2966 rows (one per BGC-spectrum pair)
- field_present: score table includes spectrum identifier, BGC identifier, and IOKR score columns
- value_in_range: IOKR scores are continuous values; robust to parameter choices (no exact byte-for-byte match required, kernel and fingerprint function choices may produce slightly different score distributions)
- output_matches_reference: reproduce histogram plot from S2 Fig showing IOKR score distribution with validated-link positions marked; check that validated-link positions are visibly enriched at higher scores relative to all-link distribution (no canonical answer for exact bin edges, but visual enrichment pattern must match figure)
- output_matches_reference: reproduce summary statistics from Table 3 or results text: mean IOKR score for all links ≈ 0.0105, mean for validated links ≈ 0.0364, p-value ≈ 1.7968 × 10⁻⁹ (robust to small numerical precision differences)
- output_matches_reference: reproduce top-n accuracy metrics from Table 3 (top-1: 0.1208, top-5: 0.1708, top-10: 0.1870, top-20: 0.2121, top-200: 0.2946, AUC: 0.6534), parameter-sensitive to model hyperparameters and kernel choice

### Expert Review
- verify that IOKR kernel function (Probability Product Kernel applied to molecular fingerprints) is correctly instantiated and hyperparameters match published method description in Methods or supplementary text
- verify that molecular fingerprint representation (type and dimensionality, e.g. Morgan, MACCS, or other) matches the published protocol
- verify that training set of 4138 spectra is correctly filtered (denoising step, peak filtering to training-set peaks only) before IOKR model training
- verify that scoring procedure correctly handles the 2966 MIBiG-GNPS pairs: each spectrum is matched against candidate set of BGC structures with MIBiG homology assignment
- expert assessment: enrichment of validated links in high-scoring region is statistically significant and visually consistent with S2 Fig distribution shape and marked positions
- expert assessment: IOKR score distribution shape, spread, and skewness are reasonable and consistent with reported mean and standard deviation estimates

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for all 4138 GNPS training spectra and their paired metabolite structures.
2. Train IOKR by learning a kernel-based mapping from the input MS2 spectrum kernel space to the output molecular fingerprint space using the paired spectrum-fingerprint training set.
3. Filter evaluation MS2 spectra (6246 total) to retain only peaks present in the GNPS training data using the Probability Product Kernel (PPK) as a denoising step.
4. For each of 6246 evaluation spectra, apply the trained IOKR model to predict a fingerprint and rank candidate BGCs (2242 with MIBiG structure assignments) by computing ⟨ĥ(spectrum), φ(BGC)⟩ in fingerprint space.
5. Evaluate top-n accuracy (n ∈ {1,5,10,20,200}) and AUC by determining the rank of the correct BGC in each ranked list; compare against randomized baseline.
6. Calculate and report mean IOKR scores for all 2966 BGC-spectrum pairs and for validated pairs, compute p-values, and generate distribution histograms with validated-link overlay.
7. Validation: reproduce top-n accuracy values (top-1=0.1208, top-5=0.1708, top-200=0.2946, AUC=0.6534) from Table 3 and visual alignment with S2 Fig distribution, confirming mean validated-link score (0.0364) significantly exceeds mean all-links score (0.0105, p=1.8×10⁻⁹).
8. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

## Workflow Ports

**Inputs:**

- `gnps_training_spectra` — GNPS library MS2 spectra with structural annotations (4138 spectra) ← `task_001/standardised_scores_all_datasets`
- `mibig_structures` — MIBiG database entries with SMILES/InChI structural annotations
- `mibig_gnps_pairs` — MIBiG-GNPS paired BGC-spectrum dataset (2966 validated pairs)
- `gnps_eval_spectra` — MS2 spectral data from GNPS for evaluation (6246 spectra with 2242 structure-assigned BGCs)

**Outputs:**

- `iokr_model` — Trained IOKR model with learned mapping from spectrum space to fingerprint space
- `ranked_bgc_lists` — Ranked candidate BGCs for each MS2 spectrum with IOKR scores
- `performance_metrics` — Top-n accuracy (top-1 through top-200) and AUC for IOKR on MIBiG-GNPS pairs
- `score_distribution` — Distribution histogram of IOKR scores with validated link positions
- `mean_scores_table` — Table of mean IOKR scores for all links and validated links with p-values

**Used:** `urn:asb:port:task_001/standardised_scores_all_datasets`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

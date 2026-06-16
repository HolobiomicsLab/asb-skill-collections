# Workflow Challenge: `coll_nplinker_workflow`


> NPLinker is a software framework that links microbial metabolomic and genomic data by combining complementary scoring functions—a standardised strain correlation score and an Input-Output Kernel Regression (IOKR) score—to prioritize true biosynthetic gene cluster–metabolite associations.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Establishing links between Biosynthetic Gene Clusters (BGCs) and specialized metabolites is crucial for discovering novel natural products, but current automated approaches are ineffective and manual verification remains a bottleneck. This work demonstrates that multiple scoring functions are complementary when used together to rank candidate links. The authors standardize a widely used strain correlation score, introduce a novel IOKR-based scoring approach, and present NPLinker, a software framework for linking genomic and metabolomic data. Validation on publicly available paired datasets shows that the standardised correlation score achieves means of −0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), while IOKR achieves means of 0.0105 and 0.0364 respectively (p=1.7968 × 10−9) with top-1 accuracy of 0.1208 and AUC of 0.6534. Links scoring above the 90th percentile for both scores show significantly higher enrichment for validated links (p=2.633 × 10−4 and p=0.0208) compared to either individual score alone, demonstrating their utility when combined for prioritizing metabolite–BGC associations.

## Research questions

- Does standardising the raw strain correlation score by its hypergeometric expectation and variance improve comparability of scores across GCF-MF links of different sizes?
- What is the distribution of IOKR scores across all 2966 MIBiG-GNPS BGC-spectrum pairs, and how do validated links rank within this distribution?
- When combining standardised strain correlation and IOKR scores, does the joint top percentile enrichment of validated links exceed that of either individual scoring function alone?
- How does NPLinker orchestrate the integration of antiSMASH/BiG-SCAPE genomic outputs and GNPS metabolomic outputs to create and rank hypothetical BGC-metabolite links?
- How does the choice of exponent p in the ℓp-norm combination function affect the enrichment of validated links in the top-ranking BGC-metabolite predictions?

## Methods overview

Load GCF-MF pairs for each dataset (Crüsemann, Gross, Leão) and extract GCF size, MF size, overlap size, and population size parameters. Compute hypergeometric expected value E[σ_corr] and variance Var[σ_corr] for each pair by summing over all possible overlap sizes weighted by hypergeometric probabilities. Calculate standardised score s*_corr = (raw_score − E[σ_corr]) / √Var[σ_corr] for all GCF-MF pairs. Generate distribution histograms and summary statistics (mean, p-value) for validated versus all links under both raw and standardised scoring. Determine enrichment of validated links at 90th percentile for each dataset and pool across datasets to compute significance. Validation: standardised score demonstrates significantly higher p-value for separation of validated from non-validated links (p < 2.5 × 10⁻¹¹) and higher proportion of validated links in top 90th percentile, consistent with reported Table 1 and Table 2 values. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038) Extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for all 4138 GNPS training spectra and their paired metabolite structures. Train IOKR by learning a kernel-based mapping from the input MS2 spectrum kernel space to the output molecular fingerprint space using the paired spectrum-fingerprint training set. Filter evaluation MS2 spectra (6246 total) to retain only peaks present in the GNPS training data using the Probability Product Kernel (PPK) as a denoising step. For each of 6246 evaluation spectra, apply the trained IOKR model to predict a fingerprint and rank candidate BGCs (2242 with MIBiG structure assignments) by computing ⟨ĥ(spectrum), φ(BGC)⟩ in fingerprint space. Evaluate top-n accuracy (n ∈ {1,5,10,20,200}) and AUC by determining the rank of the correct BGC in each ranked list; compare against randomized baseline. Calculate and report mean IOKR scores for all 2966 BGC-spectrum pairs and for validated pairs, compute p-values, and generate distribution histograms with validated-link overlay. Validation: reproduce top-n accuracy values (top-1=0.1208, top-5=0.1708, top-200=0.2946, AUC=0.6534) from Table 3 and visual alignment with S2 Fig distribution, confirming mean validated-link score (0.0364) significantly exceeds mean all-links score (0.0105, p=1.8×10⁻⁹). References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038) Load GCF-MF link data with strain membership and validated annotations from three curated microbial datasets. Compute standardised strain correlation score for each GCF-MF pair by calculating raw correlation score and adjusting for expected value and variance under hypergeometric null hypothesis. Compute IOKR scores for BGC-spectrum links via molecular fingerprint space projection, then propagate maximum IOKR score to GCF-MF level. Standardise IOKR scores using expected value and variance computed over all potential links in the dataset. Identify the 90th percentile threshold independently for standardised correlation and IOKR scores, then categorise links as: above neither, above only standardised correlation, above only IOKR, or above both (joint). Calculate the proportion of validated links within each category (total, top raw correlation, top standardised correlation, top IOKR, top combined) for each of the three datasets. Pool validated and unvalidated link counts across the three datasets and apply Fisher exact test to compare enrichment of the joint top-percentile group versus individual top-percentile groups. Validation: Demonstrate that the p-value for enrichment of validated links in the joint top percentile (both scores ≥90th percentile) is significantly lower than the p-values for either score alone (p < 0.05 after Bonferroni correction if multiple tests), confirming complementarity of the two scoring functions. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038) Cluster detected BGCs into Gene Cluster Families (GCFs) using BiG-SCAPE, grouping by product class and similarity distance. Generate the complete set of hypothetical GCF–Molecular Family (MF) link combinations from input genomic and metabolomic data. Compute standardised strain correlation score for each link by calculating hypergeometric expected value and variance and z-normalising. Score BGC–spectrum links using Input-Output Kernel Regression (IOKR) on molecular fingerprints for BGCs with MIBiG structural homology; aggregate to GCF–MF level. Standardise IOKR scores and combine both standardised scores using ℓ₁/₂-norm with sign adjustment to produce a single ranking. Rank all hypothetical links and export table with filtering and sorting options; calculate enrichment statistics for validated links at 90th percentile. Validation: confirm that joint 90th-percentile links show significantly higher proportion of validated links (p < 0.05) than either score alone. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038) Load pre-computed standardised strain correlation and IOKR scores for all links across the three microbial datasets (Crüsemann, Gross, Leão) and their validated-link annotations. Compute combined scores using the ℓ_p-norm with sign adjustment across a systematic range of p values (0.5 to 3.0 in 0.1 increments, plus fractional values 0 < p < 1) and alternative function forms (weighted linear, Chebyshev, harmonic mean, geometric mean). For each combination function and parameter set, rank all GCF-MF links and calculate validated-link enrichment ratios at the 90th and 95th percentile thresholds. Pool results across the three datasets and perform chi-square contingency tests to determine statistical significance (p < 0.05) of enrichment for each function relative to baseline (individual scores alone) and to the reported ℓ₁/₂ function. Visualise enrichment and rank metrics as heatmaps and line plots indexed by function type and exponent p. Validation: verify that ℓ₁/₂ enrichment ratios match Table 4 and Table D of supplementary text; confirm that the best-performing alternative function achieves equal or superior enrichment compared to the three originally reported functions. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

**Domain:** multi-omics

**Techniques:** correlation-analysis, machine-learning, database-annotation, network-annotation-propagation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Using multiple link-scoring functions together makes it easier to prioritise true links relative to others.
- **(finding)** The raw strain correlation score has a mean of 83.5144 for all links. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The raw strain correlation score has a mean of 14.667 for validated links. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** Standardising the strain correlation score gives a mean of -0.006 for all links. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** Standardising the strain correlation score gives a mean of 3.6717 for validated links. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The raw strain correlation score mean for validated links is lower than for all links, opposite to what would be expected. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The raw strain correlation score is highly dependent on both total population size and the size of the GCF and number of strains that produce the metabolite. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** A larger GCF with perfect strain correspondence can outscore a smaller GCF and MF pair even when the latter has stronger evidence.
- **(finding)** IOKR top-1 accuracy on MIBiG data is 0.1208. _[grounded: DS_MIBIG]_
- **(finding)** Random baseline top-1 accuracy on MIBiG data is 0.0. _[grounded: DS_MIBIG]_
- **(finding)** Random baseline top-5 accuracy on MIBiG data is 0.0014. _[grounded: DS_MIBIG]_
- **(finding)** Random baseline AUC on MIBiG data is 0.5209. _[grounded: DS_MIBIG]_
- **(finding)** IOKR mean score for all links is 0.0105.
- **(finding)** IOKR mean score for validated links is 0.0364.
- **(finding)** The standardised strain correlation score is significantly enriched for validated links at the 90th percentile with a p-value of 2.483 × 10−11. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The IOKR score is significantly enriched for validated links at the 90th percentile with a p-value of 0.0139. _[grounded: COMP_IOKR_SCORE]_
- **(finding)** Links scoring above the 90th percentile on both IOKR and standardised strain correlation scores are significantly enriched for validated links with a p-value of 2.633 × 10−4.
- **(finding)** The combined scoring function assigns the best rank to the validated link in 10 out of 15 cases tested. _[grounded: COMP_COMBINED_SCORE]_
- **(finding)** IOKR does not directly depend on natural product compound class.
- **(finding)** The strain correlation score cannot distinguish between potential links showing the same pattern of strain presence or absence. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** NPLinker accepts genomic outputs from antiSMASH and BiG-SCAPE. _[grounded: SYS_NPLINKER]_
- **(finding)** NPLinker accepts metabolomic output from GNPS knowledge base. _[grounded: SYS_NPLINKER]_
- **(finding)** NPLinker has been used to putatively link ectoine and chloramphenicol to their producing BGCs. _[grounded: SYS_NPLINKER]_
- **(finding)** The IOKR model is trained on 4138 spectra from GNPS with structural annotations. _[grounded: TOOL_GNPS]_
- **(finding)** The Crüsemann dataset consists of 120 microbial strains with 8 validated links between a BGC and a MF. _[grounded: DS_CRUSEMANN]_
- **(finding)** The Gross dataset consists of 7 strains with 9 validated links between a BGC and a MF. _[grounded: DS_GROSS]_
- **(finding)** The Leão dataset contains 4 strains with 5 validated links between a BGC and a specific MS2 spectrum. _[grounded: DS_LEAO]_
- **(finding)** The standardised strain correlation score has mean 0 and variance 1. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** A standardised strain correlation score of zero indicates that the degree of overlap between the two strain sets is the same as would be expected if they were chosen at random. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** Standardised scores make comparison between links involving different sizes of GCFs and MFs possible.
- **(finding)** IOKR requires only spectra and predicted molecular structures as input.
- **(finding)** IOKR's performance depends heavily on the choice of kernel function on the spectra and on the choice of molecular fingerprint. _[grounded: COMP_MOLECULAR_FINGERPRINT]_
- **(finding)** The strain correlation scoring approach clusters BGCs from different strains into Gene Cluster Families based on similarity-based distances.
- **(finding)** BiG-SCAPE is the state-of-the-art tool for microbial BGC clustering. _[grounded: TOOL_BIGSCAPE]_
- **(finding)** The strain correlation score formula assigns +10 for strains that produce metabolites and have BGCs in the GCF. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The strain correlation score formula assigns -10 for strains that produce metabolites but lack BGCs in the GCF. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The strain correlation score formula assigns +1 for strains that neither produce metabolites nor have BGCs in the GCF. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The strain correlation score formula leaves the score unchanged for strains that have BGCs in the GCF but do not produce metabolites. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The expected value and variance of the raw strain correlation score depend greatly on both the total population size and the number of strains producing the metabolite. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** The proportion of validated links among all links in the Crüsemann dataset is enriched above the 90th percentile for the standardised correlation score. _[grounded: DS_CRUSEMANN]_
- **(finding)** IOKR outperforms a randomised baseline by a considerable margin in top-n accuracy on MIBiG data. _[grounded: DS_MIBIG]_
- **(finding)** The standardised IOKR score is defined by subtracting the expected value from the IOKR score and dividing by its variance. _[grounded: COMP_IOKR_SCORE]_
- **(finding)** The combined scoring function ℓ1/2 ranks validated link for BGC0001228 (retimycin A) at number 253. _[grounded: COMP_COMBINED_SCORE]_
- **(finding)** The combined scoring function ℓ1/2 ranks validated link for BGC0000241 (lomaiviticin A) at number 5. _[grounded: COMP_COMBINED_SCORE]_
- **(finding)** In the case of BGC0000241 (lomaiviticin A), neither scoring function alone assigns an equal or higher score than the correct link. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** Standardisation of the strain correlation score improves its effectiveness at prioritising validated links relative to all links. _[grounded: COMP_STRAIN_CORR_SCORE]_
- **(finding)** Combining strain correlation and IOKR scores increases the ratio of validated links among high-scoring links.
- **(finding)** A drawback of IOKR is its reliance on MIBiG homology to assign molecular structures to BGCs. _[grounded: DS_MIBIG]_
- **(finding)** The molecular fingerprint vector is composed of three concatenated sets of fingerprints: CDK Substructure, PubChem Substructure, and Klekota-Roth fingerprints. _[grounded: COMP_MOLECULAR_FINGERPRINT]_
- **(finding)** 2966 BGC-spectrum pairs were created by matching MIBiG and GNPS databases. _[grounded: TOOL_GNPS]_
- **(finding)** The validated links in the MIBiG/GNPS dataset include 2069 unique spectra and 242 unique MIBiG BGCs. _[grounded: TOOL_GNPS]_
- **(finding)** BGCs in the validated links are primarily polyketides and nonribosomal peptides, with sizes ranging from 7000 to 20000 nucleotides.
- **(finding)** Strain correlation and IOKR scores are complementary methods for linking BGCs to metabolites.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- BiG-SLICE could be used instead of BiG-SCAPE for BGC clustering, though BiG-SCAPE offers higher precision
- Instead of ℓ2 (Euclidean norm), can use ℓp-norm with varying p values to combine scores
- Can use IOKR score or standardised strain correlation score individually, or vice versa, to order links
- Vector embeddings as alternative to Multiple Kernel Learning for kernel optimization
- Predicting molecular fingerprints directly from BGCs instead of relying on MIBiG homology
- Alternative fingerprints targeting specific molecular substructures

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- IOKR can only rank links involving BGCs that have predicted molecular structures with significant homology to known BGCs
- Strain correlation score requires strain information while IOKR requires structural predictions

## Steps

### Step `task_001`
- Title: Reproduce the size-bias demonstration and standardised strain correlation score computation on microbial datasets
- Task kind: `reproduction`
- Task: Implement the standardised strain correlation score (σ*_corr) by computing hypergeometric expectation and variance of raw scores, then apply it to Crüsemann, Gross, and Leão datasets to reproduce reported score distributions and validated-link positions shown in S1 Fig.
- Inputs:
  - Crüsemann dataset: genomic data (antiSMASH-predicted BGCs and BiG-SCAPE GCFs) and metabolomic data (MS2 spectra grouped into MFs) with 120 strains and 8 validated links
  - Gross dataset: genomic and metabolomic data with 7 strains and 9 validated links between a BGC and a MF
  - Leão dataset: genomic and metabolomic data with 4 strains and 5 validated links between a BGC and a specific MS2 spectrum
  - Raw strain correlation scores computed for all GCF-MF pairs in each dataset using the scoring function: start at zero; add 10 if strain produces metabolite and has BGC in GCF; subtract 10 if strain produces metabolite but no BGC in GCF; add 1 if strain has BGC but no metabolite; leave unchanged otherwise
- Expected outputs:
  - Standardised strain correlation scores (s*_corr) for all GCF-MF pairs in the three datasets, including mean score for all links and validated links with p-value
  - Distribution histograms and scatter plots (Figure 5 / S1 Fig) showing raw versus standardised strain correlation scores for validated links relative to all links in the three datasets
  - Statistical test results (t-test p-values) comparing mean scores for validated links versus all links under both raw and standardised scoring, demonstrating that standardisation enables reliable comparison
  - Table of proportions of validated links among top-scoring links (90th percentile and above) for raw, standardised, and combined scores across all three datasets
- Tools: antiSMASH, BiG-SCAPE, GNPS, MIBiG
- Landmark output files: raw_correlation_scores.csv, hypergeometric_expectation_variance.csv, standardised_correlation_scores.csv, score_distributions.png, validated_vs_all_links_statistics.csv, 90th_percentile_enrichment_table.csv
- Primary expected artifact: `standardised_strain_correlation_scores.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the IOKR BGC-spectrum scoring on the MIBiG-GNPS paired dataset
- Task kind: `reproduction`
- Task: Train the Input-Output Kernel Regression (IOKR) model on 4138 GNPS library spectra with structural annotations, apply it to score 2966 MIBiG-GNPS BGC-spectrum pairs, and reproduce the distribution of IOKR scores showing the position of validated links as reported in Table 3 and supplementary figures.
- Inputs:
  - GNPS library MS2 spectra with structural annotations (4138 spectra)
  - MIBiG database entries with structural annotations (SMILES/InChI format)
  - MIBiG-GNPS paired BGC-spectrum dataset (2966 pairs)
  - MS2 spectral data from GNPS for evaluation (6246 spectra restricted to those with structure predictions)
- Expected outputs:
  - IOKR model object with learned mapping from MS2 spectrum kernel space to molecular fingerprint space
  - Ranked list of candidate BGCs for each of 2966 MS2 spectra with IOKR scores
  - Top-n accuracy metrics (top-1, top-5, top-10, top-20, top-200) and AUC score for IOKR on MIBiG-GNPS pairs
  - Distribution histogram of IOKR scores for all 2966 BGC-spectrum pairs with validated links highlighted
  - Mean IOKR score for all links (0.0105) and for validated links (0.0364) with statistical significance (p-value)
- Tools: GNPS, MIBiG, Chemistry Development Kit (CDK), Probability Product Kernel (PPK), antiSMASH
- Landmark output files: fingerprints_extracted.csv, iokr_model_trained.pkl, ranked_bgcs_per_spectrum.csv, top_n_accuracy_metrics.csv, iokr_score_distribution.png
- Primary expected artifact: `iokr_performance_table.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the complementarity analysis combining standardised strain correlation and IOKR scores on microbial datasets
- Task kind: `reproduction`
- Task: Reproduce the complementarity analysis of standardised strain correlation and IOKR scoring functions on three microbial datasets (Crüsemann, Gross, Leão), demonstrating that links scoring in the joint top percentiles show higher enrichment of validated links than either score alone.
- Inputs:
  - Crüsemann dataset: GCF-MF links with strain membership and validated link annotations from MSV000078836
  - Gross dataset: GCF-MF links with strain membership and validated link annotations from MSV000085018
  - Leão dataset: BGC-spectrum links with strain membership and validated link annotations from MSV000085038
  - antiSMASH v5.0.0 output for BGC detection in strain assemblies
  - BiG-SCAPE v1.0.0 output for GCF clustering
  - GNPS MS2 spectra with strain association for metabolomic data
- Expected outputs:
  - Table reporting proportion of validated links for each dataset at total, top raw correlation (90th percentile), top standardised correlation (90th percentile), top IOKR (90th percentile), and top combined (both ≥90th percentile) link sets
  - P-values and effect size comparison demonstrating significant enrichment of validated links in joint top percentile versus individual score top percentiles across pooled datasets
  - Distribution plots (histograms or scatter plots) showing the relative position of validated links within score distributions for all three datasets
  - List of top-scoring links for each dataset ranked by combined score with their individual standardised correlation and IOKR scores
- Tools: antiSMASH, BiG-SCAPE, NPLinker, GNPS, MIBiG
- Landmark output files: standardised_correlation_scores.csv, iokr_scores.csv, validated_links_per_dataset.csv, percentile_enrichment_table.csv, statistical_comparison_pvalues.txt, score_distribution_plots.png
- Primary expected artifact: `complementarity_analysis_results.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the NPLinker pipeline fixed processing architecture for loading, scoring, and filtering GCF-MF hypothetical links
- Task kind: `component_reconstruction`
- Task: Implement the NPLinker framework orchestration layer that ingests antiSMASH-predicted BGCs and BiG-SCAPE-clustered GCFs from genomic data, GNPS metabolomic outputs (spectra and molecular families), and produces a filterable ranked table of GCF–MF (or BGC–spectrum) hypothetical links scored by standardised strain correlation and IOKR functions.
- Inputs:
  - antiSMASH v5.0.0 BGC predictions (JSON or GenBank format) from microbial genome assemblies
  - GNPS metabolomic data: MS2 spectra with strain annotations and molecular families from spectral clustering
  - MIBiG database reference BGCs with structural annotations for homology scoring
- Expected outputs:
  - Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score
  - NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF–MF and BGC–spectrum relationships with associated scores
  - Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections
- Tools: antiSMASH, BiG-SCAPE, NPLinker, GNPS, MIBiG
- Landmark output files: gcfs_clustered.txt, hypothetical_links_raw.csv, strain_correlation_scores.csv, iokr_scores.csv, ranked_links.csv, percentile_enrichment_stats.json
- Primary expected artifact: `ranked_links.csv`

### Step `task_005`
- Depends on: `task_003`
- Title: Analyze the effect of varying combination function parameters on validated-link enrichment beyond reported p values
- Task kind: `analysis`
- Task: Systematically evaluate how the choice of exponent p and alternative combination function forms (beyond ℓ₁, ℓ₂, ℓ₁/₂ evaluated in Table 4) affect the enrichment ratio of validated links in the top-scoring percentiles across three microbial datasets. Produce a sensitivity analysis report quantifying validated-link enrichment as a function of combination function parameters.
- Inputs:
  - task_003.expected_outputs[0]: Table reporting proportion of validated links for each dataset at total, top raw correlation (90th percentile), top standardised correlation (90th percentile), top IOKR (90th percentile), and top combined (both ≥90th percentile) link sets
  - Standardised strain correlation scores (s'_corr) and standardised IOKR scores (s'_IOKR) for all GCF-MF links in Crüsemann, Gross, and Leão datasets
  - Validated link ground truth annotations for Crüsemann (8 validated links), Gross (9 validated links), and Leão (5 validated links) datasets
- Expected outputs:
  - Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets
  - Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio
  - Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function
  - Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms
- Tools: antiSMASH, Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
- Landmark output files: enrichment_by_p.csv, enrichment_heatmap.png, rank_percentile_vs_p.png, significance_test_matrix.csv
- Primary expected artifact: `combination_function_sensitivity_report.csv`

## Final expected outputs

- `Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score` (type: file, tolerance: hash)
- `NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF–MF and BGC–spectrum relationships with associated scores` (type: file, tolerance: hash)
- `Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections` (type: file, tolerance: hash)
- `Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets` (type: file, tolerance: hash)
- `Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio` (type: file, tolerance: hash)
- `Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function` (type: file, tolerance: hash)
- `Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

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
  "workflow_id": "coll_nplinker_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
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
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined \u2113\u2081/\u2082 score, and metadata (strain count, BGC size, product type) sorted by combined score": "<locator>",
    "NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF\u2013MF and BGC\u2013spectrum relationships with associated scores": "<locator>",
    "Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections": "<locator>",
    "Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets": "<locator>",
    "Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5\u20133.0) and combination function type, with colour intensity proportional to enrichment ratio": "<locator>",
    "Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported \u2113\u2081/\u2082 function": "<locator>",
    "Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the \u2113_p family of norms": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._

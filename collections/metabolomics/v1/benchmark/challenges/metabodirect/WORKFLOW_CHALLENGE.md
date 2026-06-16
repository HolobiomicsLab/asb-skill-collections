# Workflow Challenge: `coll_metabodirect_workflow`


> MetaboDirect is an open-source, command-line pipeline that automates analysis, visualization, and statistical interpretation of direct injection FT-ICR MS metabolomic data with minimal coding requirements. The tool uniquely generates ab initio biochemical transformation networks from mass differences and demonstrated superior computational efficiency compared to existing FT-ICR MS software.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MetaboDirect addresses a critical gap in FT-ICR MS data analysis by providing a fully automated, single-command-line pipeline for processing high-resolution mass spectrometry datasets. The software performs data pre-processing, filtering, normalization, chemodiversity analysis, multivariate statistical analysis (PERMANOVA, NMDS, PCA), and transformation network construction. MetaboDirect generates standard visualizations including Van Krevelen diagrams, molecular composition plots, and pairwise comparisons, while requiring minimal programming expertise through a command-line interface that also allows customization for advanced users. The pipeline was benchmarked on two real FT-ICR MS datasets: a marine phage-bacterial infection experiment (36 samples, ~495 assigned molecular formulas per sample) completed in <1 min for core analysis steps, and a Sphagnum leachate microbial degradation study (4 samples, ~1793 assigned formulas) completed in ~30 s. A unique feature is the ab initio generation of mass-difference-based biochemical transformation networks that identify putative metabolic connections and hub metabolites without requiring compound identification. Comparative evaluation shows MetaboDirect performs all analyses available in competing tools (MetaboAnalyst, PyKrev, ftmsRanalysis, UltraMassExplorer) except raw spectra processing and molecular formula assignment, while standing apart in automated network generation and ease of access for non-programmers. Application to the S. fallax leachate study demonstrated that microbial inoculation increased metabolite richness but decreased functional diversity, indicating samples contained greater overall diversity but reduced diversity in decomposability and chemical reactivity.

## Research questions

- Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data filtering, statistical analysis, and transformation network generation?
- Do the wall-clock runtimes of MetaboDirect's main pipeline on real FT-ICR MS datasets match the reported performance benchmarks of <1 min for 40 samples and ~2 min for 120 samples?
- Does the phage-type factor (HP1 vs. HS2 vs. control) produce a statistically significant difference in metabolite content in the marine bacterium-phage system according to PERMANOVA analysis?
- How does MetaboDirect construct biochemical transformation networks from FT-ICR MS peak data, and what are the input requirements and output formats for this mass-difference network generation step?
- Does inoculation of S. fallax leachate with microorganisms increase metabolite richness but decrease functional diversity compared to uninoculated control samples?

## Methods overview

Inspect MetaboDirect codebase (Python/R) and ReadTheDocs documentation to enumerate all implemented analytical features across six pipeline steps. Systematically extract feature specifications from source code: filtering thresholds (m/z, isotopic, formula error ≤0.5 ppm, sample prevalence), normalization methods (max, minmax, mean, median, total sum, zscore), molecular indices (NOSC, GFE, AImod, DBE), statistical tests (PERMANOVA, NMDS, PCA), chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation network construction. Query published documentation for UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, and i-van Krevelen to determine which features each tool supports. Cross-reference MetaboDirect dependencies (vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape) to confirm implementation of statistical and network visualization features. Construct binary comparison table with tools as rows and features as columns, marking ✔ for present and ✖ for absent. Validation: Comparison table matches the binary feature matrix reported in the paper's tool comparison figure/table, with all six MetaboDirect pipeline steps and all cited comparison tools represented. Install MetaboDirect v0.3.4 with Python (NumPy, pandas, seaborn, matplotlib) and R (vegan, SYNCSA) dependencies from GitHub and Zenodo sources. Retrieve phage-infected bacterium (36 samples, ~1025 peaks, ~495 assigned formulas) and S. fallax leachate (4 samples) peak-abundance CSV files from OSF deposit. Execute MetaboDirect main pipeline (data pre-processing, diagnostics, exploration, chemodiversity analysis) excluding KEGG mapping and transformation networks via command-line interface. Measure and record wall-clock runtime for phage dataset and S. fallax dataset using system timing tools; generate all intermediate CSV outputs (filtered peaks, thermodynamic indices, normalized intensities, diversity metrics). Validation: Compare observed runtimes (phage expected <36 seconds; S. fallax per reported value) against benchmarks; verify all expected CSV and visualization output files exist and contain non-empty tables with correct column headers matching pipeline documentation. Load normalized peak-intensity matrix and sample metadata (phage type grouping) from preprocessed MetaboDirect outputs for the 36-sample marine phage-host dataset. Calculate pairwise distances (Bray-Curtis, Euclidean, or Jaccard) between all samples using the vegdist function from the vegan package on normalized peak intensities. Execute PERMANOVA (permutational analysis of variance) with phage type as the grouping factor and 999 permutations to test the null hypothesis of no difference in metabolite composition between HP1, HS2, and control groups. Generate NMDS ordination using the selected distance metric, extracting the first two principal components as axes for visualization. Export PERMANOVA results (p-value, F-statistic, R²) and NMDS scores to CSV; generate NMDS scatterplot with samples colored by phage type. Validation: Confirm that the PERMANOVA p-value matches the non-significant result (p > 0.05) reported in Supplementary Fig. S7C; verify NMDS plot shows no clear separation of samples by phage type. Load filtered peak list and reference biochemical transformation key into memory Calculate all pairwise mass differences between detected peaks within each sample Match mass differences to reference transformation key, retaining matches with ≤1 ppm error tolerance Classify matched transformations as biotic or abiotic based on prior biochemical categorization Generate node CSV (peaks with m/z, formula, compound class) and edge CSV files (transformations with source, target, type, error) formatted for Cytoscape Compute and export transformation summary statistics (count per sample, frequency distribution) as CSV tables and bar plots Validation: verify edge files contain no transformations with mass error >1 ppm, confirm all nodes reference detected peaks in input list, and confirm all transformations are classified (biotic or abiotic) Load S. fallax leachate peak-abundance matrix (CSV) and sample metadata with inoculation status annotations. Apply sum-normalization to raw peak intensities within each sample to standardize total abundance across samples. Compute abundance-based richness and diversity indices (Shannon, Gini-Simpson, Chao1) from normalized peak intensities using vegan package functions. Compute functional-based diversity (Rao's quadratic entropy) using SYNCSA package, integrating elemental composition, decomposability indices (NOSC, GFE, AImod, DBE), and aromaticity traits. Stratify all diversity metrics by inoculation status (inoculated vs. control) and generate grouped box plot visualizations. Export diversity metric values and grouped summary statistics to CSV and export visualizations as PNG/PDF. Validation: Verify that median/mean values of abundance-based richness indices (Chao1, Shannon) are higher in inoculated samples and that Rao's quadratic entropy is lower in inoculated samples relative to controls, consistent with reported patterns in the paper.

**Domain:** metabolomics

**Techniques:** direct-infusion-ms, high-resolution-ms, feature-detection, metabolite-identification, multivariate-statistics, molecular-networking

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MetaboDirect requires a single line of code to launch a fully automated framework for the generation and visualization of a wide range of plots. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect is uniquely able to automatically generate biochemical transformation networks based on mass differences. _[grounded: MetaboDirect]_
- **(finding)** DI-MS drawbacks include inability to separate chemical isomers, lack of fine resolving power, and signal suppression or enhancement.
- **(finding)** FT-ICR MS has evolved into a powerful tool to study molecular composition of small-molecule organic complex mixtures in diverse ecosystems. _[grounded: FT_ICR_MS]_
- **(finding)** 40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min by MetaboDirect. _[grounded: MetaboDirect]_
- **(finding)** The bacterium-phage data set had an average of 1025 peaks detected across 36 samples.
- **(finding)** An average of 495 peaks in the bacterium-phage data set received molecular formula assignment.
- **(finding)** The main steps of the MetaboDirect pipeline took less than 1 min (~36 s) for the bacterium-phage data set. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect analysis including KEGG mapping and biochemical transformations took around 10 min for the bacterium-phage data set. _[grounded: MetaboDirect]_
- **(finding)** Full MetaboDirect analysis including KEGG mapping, biochemical transformations, and network creation took about 21 min for the bacterium-phage data set. _[grounded: MetaboDirect]_
- **(finding)** The S. fallax data set consisted of 4 samples with an average of 1793 assigned molecular formulas.
- **(finding)** The main MetaboDirect pipeline steps for the S. fallax data set were clocked at around 30 s. _[grounded: MetaboDirect]_
- **(finding)** Full analysis of the S. fallax data set including KEGG mapping and network construction took about 32 min. _[grounded: KEGG_Database]_
- **(finding)** Approximately 200 masses were filtered out from the bacterium-phage data set because they contained isotopic carbon.
- **(finding)** One sample in the bacterium-phage data set was identified as a potential outlier with very low assigned molecular formulas.
- **(finding)** The chemical composition of the exometabolome of cells infected with HS2 phage changed at 30 min post-inoculation, then returned to uninfected similarity.
- **(finding)** The molecular composition of exometabolome from cells infected with HP1 phage did not change throughout the experiment.
- **(finding)** Most detected metabolites were shared between infected and uninfected cells in the bacterium-phage data set.
- **(finding)** Unique metabolites in the bacterium-phage data set were mostly protein-like, lignin-like, and lipid-like.
- **(finding)** In the S. fallax data set, the number of unique metabolites in control and inoculated samples was almost the same as shared metabolites.
- **(finding)** Lignin-like metabolites were most abundant in unique metabolites in inoculated S. fallax samples.
- **(finding)** Tannins were present only in control samples of the S. fallax data set.
- **(finding)** Inoculating S. fallax leachate with microorganisms increased the diversity of metabolites in richness. _[grounded: Cond_Sphagnum_Inoculated]_
- **(finding)** Inoculation decreased functional diversity of metabolites in S. fallax samples.
- **(finding)** MetaboDirect was developed in Python 3.8 and R 4.0.2. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect requires Python dependencies including NumPy, pandas, seaborn, py4cytoscape, and matplotlib. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect consists of 6 major steps: data pre-processing, data diagnostics, data exploration, chemodiversity analysis, statistical analysis, and transformation network analysis. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect can work with molecular formulas generated by software such as DataAnalysis, Xcalibur, CoreMS, or MassSpecWavelet followed by MFAssignR. _[grounded: MetaboDirect]_
- **(finding)** The normalization methods available in MetaboDirect include max, minmax, mean, median, total sum, and zscore. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect calculates thermodynamic indices including NOSC, GFE, AImod, and DBE. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect generates Van Krevelen diagrams during data exploration. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect can query the KEGG database to provide putative KEGG Pathway, Module, and Brite annotations. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect calculates diversity metrics including Shannon diversity index, Gini-Simpson index, and Chao1 richness estimator. _[grounded: MetaboDirect]_
- **(finding)** Rao's quadratic entropy is used by MetaboDirect to measure functional-based diversity. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect performs PERMANOVA for statistical analysis of FT-ICR MS data. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect generates NMDS ordination plots for metabolomic data visualization. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect creates PCA scree plots and biplots based on molecular composition and thermodynamic indices. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect uses mass difference network-based approach to generate molecular transformation networks. _[grounded: MetaboDirect]_
- **(finding)** Mass differences with a maximum error of 1 ppm are kept as putative mass-based transformations in MetaboDirect. _[grounded: MetaboDirect]_
- **(finding)** Microorganisms are responsible for mobilization, transformation, and storage of natural organic matter.
- **(finding)** Microorganisms can directly assimilate low molecular weight DOM less than 600 Da for metabolic processes.
- **(finding)** Environmental conditions such as temperature and water availability influence microbial community structure and its interaction with NOM.
- **(finding)** High-resolution mass spectrometry has allowed high-precision formula assignment of diverse organic compounds based on ultra-high mass accuracy.
- **(finding)** MetaboDirect is a command-line-based pipeline requiring minimal coding experience. _[grounded: MetaboDirect]_
- **(finding)** The most abundant chemical transformation in the bacterium-phage data set was methylation.
- **(finding)** MetaboDirect provides all R scripts used in the generation of tables and visualizations for customization. _[grounded: MetaboDirect]_
- **(finding)** MetaboDirect can perform all analyses offered by other FT-ICR MS software except raw spectra processing and molecular formula assignment. _[grounded: MetaboDirect]_
- **(finding)** Chemodiversity analysis for the bacterium-phage data set found little differences in metabolite diversity between infected and uninfected cells.
- **(finding)** PERMANOVA analysis showed the phage type produces a significant difference in metabolite content.

**Speculative claims (excluded from scoring):**
- **(finding)** MetaboDirect integrates metabolomics within microbiome studies to advance understanding of microbial-chemical interactions. _[grounded: MetaboDirect]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Direct injection mass spectrometry (DI-MS) and FT-ICR MS are alternatives to low-resolution mass spectrometers for analyzing NOM components
- Formularity alternative: DataAnalysis, Xcalibur, CoreMS, or combination of MassSpecWavelet and MFAssignR for raw spectra processing
- Alternative normalization methods: Probabilistic Quotient Normalization (PQN), Quantile Normalization, and Variance Stabilization
- User-specific biochemical transformation list as alternative to predefined biochemical transformation key
- User may test various normalization strategies and choose the best one when SPANS may not be appropriate for data sets with systematic differences

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- No coding experience is required to run MetaboDirect, but some experience in R is needed if fully customized plots are desired
- PQN requires a conscious selection of a reference spectrum, which are not often available for complex samples or present in exploratory analysis
- Chemodiversity analysis depends on the total number of peaks detected and validity requires all spectra within a dataset collected using the same instrument parameters
- SPANS may not be appropriate for data sets with systematic differences in intensity distributions among groups

## Steps

### Step `task_001`
- Title: Reproduce the feature-comparison table of MetaboDirect versus MetaboAnalyst, PyKrev, ftmsRanalysis, and UME
- Task kind: `reproduction`
- Task: Verify the presence or absence of analytical features (data filtering, normalization methods, visualization types, statistical tests, transformation network analysis) across five FT-ICR MS analysis tools by inspecting the MetaboDirect codebase and documentation, then reconstruct the binary comparison table reported in the paper.
- Inputs:
  - MetaboDirect GitHub repository code and documentation
  - MetaboDirect ReadTheDocs webpage with full pipeline documentation
  - Published documentation or repositories for UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, and i-van Krevelen
- Expected outputs:
  - Structured comparison table (CSV or TSV format) with rows for each of five tools and columns for analytical features, with binary ✔/✖ entries indicating presence or absence of each feature
- Tools: MetaboDirect, UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen, vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape
- Landmark output files: metabodirect_features.txt, ume_freda_metaboanalyst_dropms_ivankrevel_docs_parsed.txt, feature_matrix_raw.csv, tool_feature_comparison.csv
- Primary expected artifact: `tool_feature_comparison.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the runtime benchmark metrics for the MetaboDirect main pipeline across sample-size conditions
- Task kind: `reproduction`
- Task: Execute the MetaboDirect v0.3.4 pipeline (main steps only, excluding KEGG and transformation networks) on two FT-ICR MS datasets (phage-infected bacterium and S. fallax leachate) from the deposited OSF repository and measure wall-clock runtime for each dataset, then compare observed times against the reported benchmarks.
- Inputs:
  - Peak-abundance and molecular formula .csv files for bacterium-phage model system (36 samples) and S. fallax leachate incubation (4 samples) from OSF repository
  - MetaboDirect v0.3.4 source code from GitHub repository and Zenodo deposit
- Expected outputs:
  - Wall-clock runtime (in seconds) for phage dataset main pipeline execution
  - Wall-clock runtime (in seconds) for S. fallax leachate dataset main pipeline execution
  - CSV files containing filtered peaks, thermodynamic indices, normalized intensities, diagnostic tables, and diversity metrics for each dataset
  - Comparison table or report documenting observed runtimes vs. reported benchmarks with percent deviation
- Tools: MetaboDirect, Python 3.8, R 4.0.2, NumPy, pandas, seaborn, matplotlib, vegan, SYNCSA
- Landmark output files: phage_filtered_peaks.csv, phage_thermodynamic_indices.csv, phage_normalized_intensities.csv, phage_diversity_metrics.csv, sfallax_filtered_peaks.csv, sfallax_thermodynamic_indices.csv
- Primary expected artifact: `runtime_benchmark_report.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce the PERMANOVA result for phage-type effect on the marine phage-host exometabolome
- Task kind: `reproduction`
- Task: Run MetaboDirect's statistical analysis step (Step 5) on the marine phage-host dataset to calculate PERMANOVA p-values and NMDS ordination scores stratified by phage type (HP1, HS2, control), and verify the non-significant result reported in Supplementary Fig. S7C.
- Inputs:
  - Normalized peak intensity CSV table (post-preprocessing) from MetaboDirect output for marine phage-host dataset (36 samples, ~495 molecular formulas)
  - Sample metadata with phage type assignments (HP1, HS2, control) for 36 samples
  - Reference PERMANOVA and NMDS results from Supplementary Fig. S7C showing non-significant phage-type effect
- Expected outputs:
  - PERMANOVA results table (CSV) containing p-value, F-statistic, and R² for phage-type factor
  - NMDS ordination scores (CSV) for all 36 samples with first two principal components
  - NMDS scatterplot (PNG/PDF) with samples colored by phage type (HP1, HS2, control)
- Tools: MetaboDirect, vegan (R package), Python 3.8, R 4.0.2
- Landmark output files: normalized_peak_intensities.csv, distance_matrix.csv, nmds_scores.csv, permanova_results.csv, nmds_ordination.png
- Primary expected artifact: `permanova_results.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the per-sample molecular transformation network generation step of the MetaboDirect pipeline
- Task kind: `component_reconstruction`
- Task: Implement a standalone mass-difference network construction module that accepts a filtered peak list with assigned molecular formulas and reference biochemical transformation keys, computes pairwise mass differences with 1 ppm error tolerance, matches them to known transformations, and outputs Cytoscape-compatible node and edge CSV files.
- Inputs:
  - Filtered peak list CSV containing peak identifiers, m/z values, assigned molecular formulas, compound class, and normalized intensities from preprocessing step
  - Reference biochemical transformation key containing predefined masses of common metabolic reactions, optionally user-specific for analyzed system
- Expected outputs:
  - Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error
  - Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence
  - Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency
  - Network visualization files and statistics tables exported as CSV and bar plots
- Tools: MetaboDirect, Cytoscape
- Landmark output files: pairwise_mass_differences.csv, matched_transformations_raw.csv, transformation_classifications_filtered.csv, cytoscape_nodes.csv, transformation_frequency_per_sample.csv, network_statistics.csv
- Primary expected artifact: `transformation_networks_edges.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Analyze chemodiversity differences between inoculated and control S. fallax leachate samples using MetaboDirect outputs
- Task kind: `analysis`
- Task: Run MetaboDirect's chemodiversity analysis step on S. fallax leachate peak-abundance data to compute richness (Shannon, Gini-Simpson, Chao1) and functional diversity (Rao's quadratic entropy) metrics stratified by inoculation status (inoculated vs. control). Export diversity indices as CSV tables and box plots; verify that inoculated samples exhibit higher metabolite richness but lower functional diversity relative to controls.
- Inputs:
  - S. fallax leachate peak-abundance matrix (CSV): rows = detected peaks with assigned molecular formulas, columns = samples; metadata table mapping sample identifiers to inoculation status (inoculated vs. control)
- Expected outputs:
  - CSV table containing Shannon diversity index, Gini-Simpson index, Chao1 richness estimator, and Rao's quadratic entropy values for each sample, stratified by inoculation status (inoculated vs. control)
  - Box plot visualization (PNG/PDF) showing distribution of abundance-based (Shannon, Gini-Simpson, Chao1) and functional-based (Rao's quadratic entropy) diversity metrics grouped by inoculation status
- Tools: MetaboDirect, vegan, SYNCSA
- Landmark output files: normalized_peak_abundances.csv, richness_indices.csv, functional_diversity_rao_entropy.csv, diversity_metrics_boxplots.png
- Primary expected artifact: `s_fallax_chemodiversity_metrics.csv`

## Final expected outputs

- `PERMANOVA results table (CSV) containing p-value, F-statistic, and R² for phage-type factor` (type: file, tolerance: hash)
- `NMDS ordination scores (CSV) for all 36 samples with first two principal components` (type: file, tolerance: hash)
- `NMDS scatterplot (PNG/PDF) with samples colored by phage type (HP1, HS2, control)` (type: file, tolerance: hash)
- `Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error` (type: file, tolerance: hash)
- `Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence` (type: file, tolerance: hash)
- `Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency` (type: file, tolerance: hash)
- `Network visualization files and statistics tables exported as CSV and bar plots` (type: file, tolerance: hash)
- `CSV table containing Shannon diversity index, Gini-Simpson index, Chao1 richness estimator, and Rao's quadratic entropy values for each sample, stratified by inoculation status (inoculated vs. control)` (type: file, tolerance: hash)
- `Box plot visualization (PNG/PDF) showing distribution of abundance-based (Shannon, Gini-Simpson, Chao1) and functional-based (Rao's quadratic entropy) diversity metrics grouped by inoculation status` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** concrete

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
  "workflow_id": "coll_metabodirect_workflow",
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
    "PERMANOVA results table (CSV) containing p-value, F-statistic, and R\u00b2 for phage-type factor": "<locator>",
    "NMDS ordination scores (CSV) for all 36 samples with first two principal components": "<locator>",
    "NMDS scatterplot (PNG/PDF) with samples colored by phage type (HP1, HS2, control)": "<locator>",
    "Edge CSV file(s) per sample containing source peak m/z, target peak m/z, mass difference, transformation type (biotic/abiotic), and ppm error": "<locator>",
    "Node CSV file containing all detected peaks with m/z, molecular formula, compound class, and sample presence": "<locator>",
    "Transformation statistics CSV reporting number of transformations occurring per sample and transformation frequency": "<locator>",
    "Network visualization files and statistics tables exported as CSV and bar plots": "<locator>",
    "CSV table containing Shannon diversity index, Gini-Simpson index, Chao1 richness estimator, and Rao's quadratic entropy values for each sample, stratified by inoculation status (inoculated vs. control)": "<locator>",
    "Box plot visualization (PNG/PDF) showing distribution of abundance-based (Shannon, Gini-Simpson, Chao1) and functional-based (Rao's quadratic entropy) diversity metrics grouped by inoculation status": "<locator>"
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

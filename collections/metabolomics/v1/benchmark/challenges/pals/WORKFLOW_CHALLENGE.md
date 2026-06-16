# Workflow Challenge: `coll_pals_workflow`


> PALS is a pathway analysis tool that decomposes activity levels via the PLAGE method and demonstrates greater robustness to noise and missing peaks compared to ORA and GSEA alternatives in metabolomics data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This work introduces PALS (Pathway Activity Level Scoring), a complete tool for pathway analysis that performs database queries, decomposes activity levels in pathways via the PLAGE method, and presents results through an interactive web application. The paper reports that PALS exhibits greater robustness to noise and missing peaks compared to ORA and GSEA alternatives, with particular importance for metabolomics peak data where such artifacts are prevalent. The authors demonstrate that PALS's decomposition approach is amenable to analysis of any group of metabolite sets beyond pathways, including Molecular Families from GNPS and Mass2Motifs from MS2LDA. Analysis of sensitivity under simulated noise and peak dropout confirms that PALS outperforms ORA and GSEA alternatives on these robustness dimensions.

## Research questions

- Does PALS demonstrate greater robustness to noise and missing peaks in metabolomics peak data compared to ORA and GSEA methods?
- How does the PLAGE decomposition method in PALS convert a metabolite intensity matrix and pathway database into quantitative pathway activity level scores?
- Does the PLAGE decomposition method in PALS generalise to non-pathway metabolite groupings such as Molecular Families from GNPS and Mass2Motifs from MS2LDA?
- How does the rank-order stability of top-scoring pathways in PALS degrade as Gaussian noise and random peak removal increase in severity across a metabolomics dataset?
- Can the PLAGE decomposition method in PALS be extended to score user-uploaded custom metabolite sets beyond the three currently supported set types (pathways, Molecular Families, and Mass2Motifs)?

## Methods overview

Load metabolomics peak intensity matrix and pathway/metabolite set annotations. Compute pathway activity scores using PALS (PLAGE decomposition), ORA (hypergeometric test), and GSEA (ranked enrichment). Generate in-silico noise-perturbed datasets by randomly removing peaks at controlled rates (e.g., 10%, 25%, 50%). Re-run all three methods on each perturbed dataset variant. Calculate robustness metrics (e.g., Spearman rank correlation, or fraction of pathways with consistent effect-size direction) comparing original vs. perturbed results. Validation: PALS exhibits higher rank-correlation stability and effect-size preservation across all noise levels compared to ORA and GSEA, reproducing the reported robustness advantage. References: source article (DOI: 10.1186/1471-2105-6-225) Load metabolite intensity matrix (metabolites × samples) and pathway definitions from database. For each pathway, extract the subset of metabolites belonging to that pathway from the intensity matrix. Apply singular value decomposition (SVD) to each pathway-specific metabolite intensity submatrix. Extract the first left singular vector (first principal component) as the pathway activity score. Normalize and scale pathway activity scores across all pathways to enable cross-pathway comparison. Rank pathways by absolute activity level magnitude and assemble into a ranked results table. Validation: Verify that output table contains one row per pathway with activity scores; confirm pathway ranking is monotonic by magnitude; assess robustness to simulated noise and missing values as reported in paper findings. References: source article (DOI: 10.1186/1471-2105-6-225) Load metabolomics data and non-pathway metabolite groupings (Molecular Families and Mass2Motifs). Apply PALS decomposition using PLAGE algorithm to calculate activity scores for each metabolite set across samples. Assess robustness of PLAGE scores by introducing noise or simulating missing peaks and comparing stability to pathway-based results. Validation: PLAGE successfully decomposes non-pathway metabolite sets with comparable or superior robustness to noise/missing peaks as pathway-based analyses, confirming generalisation beyond curated pathway annotations. References: source article (DOI: 10.1186/1471-2105-6-225) Load reference metabolomics dataset and pathway annotations. Run PALS on clean unperturbed data; record and rank pathway activity scores as baseline. Systematically generate perturbed datasets by injecting Gaussian noise and removing random peaks across multiple intensity levels. Run PALS on each perturbed dataset using identical decomposition parameters; record ranked pathway scores. Compute rank-order correlations (Spearman ρ, Kendall τ) and top-K retention percentages between perturbed and baseline rankings. Validation: confirm that pathway rank-order correlation remains ≥ 0.80 and top-5 pathway retention ≥ 80% under combined noise and peak-removal up to 10% intensity threshold, consistent with reported PALS robustness advantage. References: source article (DOI: 10.1186/1471-2105-6-225) Parse and validate user-uploaded metabolite set file structure and identifiers Integrate validated set into PALS pipeline as a new set type Execute PLAGE decomposition to compute activity level scores Compile results into scored output table with statistical metrics Validation: Verify output table contains all input metabolite sets with non-null activity scores and statistical confidence intervals References: source article (DOI: 10.1186/1471-2105-6-225)

**Domain:** transcriptomics

**Techniques:** dimensionality-reduction, pathway-analysis, enrichment-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** PALS (Pathway Activity Level Scoring) is a tool that performs database queries of pathways. _[grounded: PALS_system]_
- **(finding)** PALS decomposes activity levels in pathways via the PLAGE method. _[grounded: PALS_system]_
- **(finding)** PALS results are more robust to noise and missing peaks compared to ORA and GSEA. _[grounded: PALS_system]_
- **(finding)** Noise and missing peaks are prevalent in metabolomics peak data.
- **(finding)** The decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways. _[grounded: PALS_system]_
- **(finding)** Metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can be analysed with PALS. _[grounded: PALS_system]_
- **(finding)** PALS can analyse Molecular Families from GNPS. _[grounded: PALS_system]_
- **(finding)** PALS can analyse Mass2Motifs from MS2LDA. _[grounded: PALS_system]_
- **(finding)** PALS Viewer presents results in a user-friendly manner. _[grounded: PALS_system]_
- **(finding)** Pathway analysis is an important task in understanding complex metabolomic data.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- ORA (Overrepresentation Analysis)
- GSEA (Gene Set Enrichment Analysis)

## Steps

### Step `task_001`
- Title: Reproduce PALS robustness comparison against ORA and GSEA baselines
- Task kind: `reproduction`
- Task: Re-run PALS (PLAGE-based pathway activity scoring) alongside ORA and GSEA on the same metabolomics peak dataset and reproduce the reported finding that PALS is more robust to noise and missing peaks than either baseline method. Output a comparison report with robustness metrics.
- Inputs:
  - Metabolomics peak dataset (intensity matrix: peaks × samples)
  - Pathway or metabolite set database (e.g., KEGG, HMDB, or custom collection)
- Expected outputs:
  - Robustness comparison table (methods × noise-level × robustness-metric)
  - Robustness metric visualization (e.g., line plot or heatmap showing PALS vs. ORA vs. GSEA performance under noise)
- Tools: PALS (Pathway Activity Level Scoring)
- Landmark output files: pals_original_scores.csv, ora_original_scores.csv, gsea_original_scores.csv, pals_noise_perturbed_scores.csv, ora_noise_perturbed_scores.csv, gsea_noise_perturbed_scores.csv
- Primary expected artifact: `robustness_comparison.csv`

### Step `task_002`
- Title: Reconstruct PLAGE-based pathway activity level scoring component of PALS
- Task kind: `component_reconstruction`
- Task: Implement the PLAGE decomposition step within PALS to convert a metabolite intensity matrix and pathway database into pathway activity level scores, producing a ranked pathway results table.
- Inputs:
  - Metabolite intensity matrix (metabolites × samples)
  - Pathway database with metabolite set definitions
- Expected outputs:
  - Ranked pathway results table with pathway identifiers, PLAGE activity scores, and ranking
- Tools: PALS (Pathway Activity Level Scoring)
- Landmark output files: pathway_metabolite_assignments.txt, svd_singular_vectors_per_pathway.npz, pathway_activity_scores.csv
- Primary expected artifact: `pathway_activity_scores.csv`

### Step `task_003`
- Title: Reproduce metabolite set analysis generality: Molecular Families and Mass2Motifs inputs
- Task kind: `reproduction`
- Task: Demonstrate that PALS decomposition using PLAGE generalises beyond pathway analysis to non-pathway metabolite groupings (Molecular Families from GNPS and Mass2Motifs from MS2LDA). Reproduce reported results showing that the approach successfully decomposes activity levels across these spectrum-derived metabolite sets.
- Inputs:
  - Metabolomics expression data (e.g., peak intensity or abundance matrix with samples × metabolites)
  - Non-pathway metabolite set definitions: Molecular Families from GNPS
  - Non-pathway metabolite set definitions: Mass2Motifs from MS2LDA
- Expected outputs:
  - Activity score matrix decomposed by PLAGE for Molecular Families (samples × families with PLAGE scores)
  - Activity score matrix decomposed by PLAGE for Mass2Motifs (samples × motifs with PLAGE scores)
  - Comparative results demonstrating robustness of non-pathway decomposition to noise and missing peaks
  - Results presentation confirming PLAGE generalisation to non-pathway metabolite groupings
- Tools: PALS (Pathway Activity Level Scoring), GNPS, MS2LDA
- Landmark output files: gnps_families_activity_scores.csv, ms2lda_motifs_activity_scores.csv, robustness_noise_comparison.csv
- Primary expected artifact: `plage_generalization_results.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Analyze sensitivity of PALS pathway rankings under simulated noise and peak dropout
- Task kind: `analysis`
- Task: Inject systematically increasing levels of Gaussian noise and random peak removal into a reference metabolomics dataset, process each perturbed dataset through PALS, and quantify the rank-order stability of top-scoring pathways relative to the clean-data baseline to assess robustness.
- Inputs:
  - Reference metabolomics dataset: peak intensity matrix (samples × features) and associated pathway annotations (metabolite-to-pathway membership table)
- Expected outputs:
  - Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns
  - Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation
- Tools: PALS (Pathway Activity Level Scoring)
- Landmark output files: clean_baseline_pathway_scores.csv, perturbed_datasets_pathways_scores_*.csv, rank_correlation_matrix.csv, top_k_retention_table.csv
- Primary expected artifact: `pathway_stability_metrics.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Extend PALS to support user-supplied custom metabolite set collections via PALS Viewer API
- Task kind: `extension`
- Task: Implement an extension to PALS Viewer that accepts user-uploaded metabolite set files (CSV/JSON format) and processes them through the PLAGE scoring pipeline to return a scored results table, extending beyond the three currently shipped set types (pathways, Molecular Families, Mass2Motifs).
- Inputs:
  - User-uploaded metabolite set file in CSV or JSON format containing metabolite identifiers and groupings
  - PALS Viewer application and existing PLAGE scoring pipeline infrastructure
- Expected outputs:
  - Scored results table with metabolite set names, activity level scores, and associated statistics
- Tools: PALS Viewer, PALS (Pathway Activity Level Scoring)
- Landmark output files: parsed_metabolite_set.json, validated_metabolite_set.json, activity_scores_intermediate.csv
- Primary expected artifact: `scored_metabolite_sets.csv`

## Final expected outputs

- `Robustness comparison table (methods × noise-level × robustness-metric)` (type: file, tolerance: hash)
- `Robustness metric visualization (e.g., line plot or heatmap showing PALS vs. ORA vs. GSEA performance under noise)` (type: file, tolerance: hash)
- `Activity score matrix decomposed by PLAGE for Molecular Families (samples × families with PLAGE scores)` (type: file, tolerance: hash)
- `Activity score matrix decomposed by PLAGE for Mass2Motifs (samples × motifs with PLAGE scores)` (type: file, tolerance: hash)
- `Comparative results demonstrating robustness of non-pathway decomposition to noise and missing peaks` (type: file, tolerance: hash)
- `Results presentation confirming PLAGE generalisation to non-pathway metabolite groupings` (type: file, tolerance: hash)
- `Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns` (type: file, tolerance: hash)
- `Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation` (type: file, tolerance: hash)
- `Scored results table with metabolite set names, activity level scores, and associated statistics` (type: file, tolerance: hash)

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
  "workflow_id": "coll_pals_workflow",
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
    "Robustness comparison table (methods \u00d7 noise-level \u00d7 robustness-metric)": "<locator>",
    "Robustness metric visualization (e.g., line plot or heatmap showing PALS vs. ORA vs. GSEA performance under noise)": "<locator>",
    "Activity score matrix decomposed by PLAGE for Molecular Families (samples \u00d7 families with PLAGE scores)": "<locator>",
    "Activity score matrix decomposed by PLAGE for Mass2Motifs (samples \u00d7 motifs with PLAGE scores)": "<locator>",
    "Comparative results demonstrating robustness of non-pathway decomposition to noise and missing peaks": "<locator>",
    "Results presentation confirming PLAGE generalisation to non-pathway metabolite groupings": "<locator>",
    "Rank-order stability metrics: a table with noise level (% Gaussian + % peak removal) as rows and Spearman/Kendall correlation coefficient and top-K retention percentage as columns": "<locator>",
    "Stability curve plot: x-axis = noise/peak-removal level, y-axis = correlation coefficient or retention %; separate lines for noise alone, peak removal alone, and combined perturbation": "<locator>",
    "Scored results table with metabolite set names, activity level scores, and associated statistics": "<locator>"
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

# SciTask Card: Reproduce metabolite set analysis generality: Molecular Families and Mass2Motifs inputs

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T21:26:46.708623+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pals/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`
- DOI: `10.1186/1471-2105-6-225`
- GitHub: `glasgowcompbio/PALS`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `differential-expression`, `gene-regulation`
- Techniques: `dimensionality-reduction`, `pathway-analysis`, `enrichment-analysis`
- Keywords: `pathway activity scoring` · `plage method` · `metabolomics peak detection` · `untargeted metabolomics` · `molecular families` · `mass2motifs` · `fragmentation spectra analysis`

## Research Question
Does the PLAGE decomposition method in PALS generalise to non-pathway metabolite groupings such as Molecular Families from GNPS and Mass2Motifs from MS2LDA?

## Connected Finding
PALS's decomposition approach is amenable to analysis of any group of metabolite sets beyond pathways, including Molecular Families from GNPS and Mass2Motifs from MS2LDA.

## Task Description
Demonstrate that PALS decomposition using PLAGE generalises beyond pathway analysis to non-pathway metabolite groupings (Molecular Families from GNPS and Mass2Motifs from MS2LDA). Reproduce reported results showing that the approach successfully decomposes activity levels across these spectrum-derived metabolite sets.

## Inputs
- Metabolomics expression data (e.g., peak intensity or abundance matrix with samples × metabolites)
- Non-pathway metabolite set definitions: Molecular Families from GNPS
- Non-pathway metabolite set definitions: Mass2Motifs from MS2LDA

## Expected Outputs
- Activity score matrix decomposed by PLAGE for Molecular Families (samples × families with PLAGE scores)
- Activity score matrix decomposed by PLAGE for Mass2Motifs (samples × motifs with PLAGE scores)
- Comparative results demonstrating robustness of non-pathway decomposition to noise and missing peaks
- Results presentation confirming PLAGE generalisation to non-pathway metabolite groupings

## Expected Output File

- `plage_generalization_results.csv`

## Landmark Outputs

- `gnps_families_activity_scores.csv`
- `ms2lda_motifs_activity_scores.csv`
- `robustness_noise_comparison.csv`

## Tools
- PALS (Pathway Activity Level Scoring)
- GNPS
- MS2LDA

## Skills
- metabolite-set-decomposition-plage
- spectral-fragmentation-motif-analysis
- molecular-family-grouping-analysis
- activity-score-robustness-assessment
- non-pathway-metabolite-classification

## Workflow Description
1. Load metabolomics expression data and non-pathway metabolite sets (Molecular Families from GNPS and Mass2Motifs from MS2LDA) into PALS. 2. Apply PALS decomposition using the PLAGE method to compute activity scores for each metabolite grouping across samples. 3. Evaluate robustness of PLAGE-derived activity scores against noise and missing peaks, comparing qualitatively to pathway-based results. 4. Present decomposed activity levels and comparative results in output tables or figures confirming generalisation beyond pathway analysis.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/annot_df.png` | figure | False |
| `figures/int_df.png` | figure | False |
| `figures/logo.png` | figure | False |
| `figures/logo_transparent.png` | figure | False |
| `figures/output.png` | figure | False |
| `figures/overall_schematic.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found
- specific published results (tables, figures, or supplementary files) demonstrating PLAGE decomposition applied to GNPS Molecular Families
- specific published results (tables, figures, or supplementary files) demonstrating PLAGE decomposition applied to MS2LDA Mass2Motifs
- reference to or location of the exact test dataset(s) used to validate decomposition on these non-pathway metabolite sets

## Domain Knowledge
- PLAGE (Pathway Level Analysis using Gene Expression) decomposes multivariate activity across groups via singular value decomposition of normalised expression within each group; when applied to non-pathway sets, it extracts dominant activity patterns in the same manner.
- Molecular Families (GNPS) are co-occurrence groups of metabolite fragmentation patterns detected through spectral networking, representing metabolite relationships derived from MS/MS fragmentation data rather than curated pathway databases.
- Mass2Motifs (MS2LDA) represent latent fragmentation patterns learned via probabilistic topic modelling on MS/MS spectra, capturing recurring fragmentation themes that may cut across traditional metabolite classifications.
- Robustness to noise and missing peaks in metabolomics is critical because peak detection can be incomplete or error-prone; PLAGE's multivariate approach tolerates missing data better than set-overlap methods (ORA) or single-feature statistics (GSEA).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the PLAGE decomposition method in PALS generalise to non-pathway metabolite groupings such as Molecular Families from GNPS and Mass2Motifs from MS2LDA?: 'the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways. As demonstrated in PALS Viewer, metabolite sets obtained from the grouping of'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] PALS's decomposition approach is amenable to analysis of any group of metabolite sets beyond pathways, including Molecular Families from GNPS and Mass2Motifs from MS2LDA.: 'the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways. As demonstrated in PALS Viewer, metabolite sets obtained from the grouping of'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Metabolomics expression data (e.g., peak intensity or abundance matrix with samples × metabolites): 'No usage/docs found.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] Non-pathway metabolite set definitions: Molecular Families from GNPS: 'Molecular Families from GNPS'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Non-pathway metabolite set definitions: Mass2Motifs from MS2LDA: 'Mass2Motifs from MS2LDA'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Activity score matrix decomposed by PLAGE for Molecular Families (samples × families with PLAGE scores): 'decomposes activity levels in pathways via the PLAGE method'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Activity score matrix decomposed by PLAGE for Mass2Motifs (samples × motifs with PLAGE scores): 'decomposes activity levels in pathways via the PLAGE method'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Comparative results demonstrating robustness of non-pathway decomposition to noise and missing peaks: 'more robust to noise and missing peaks compared to the alternatives'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] Results presentation confirming PLAGE generalisation to non-pathway metabolite groupings: 'presents the results in a user-friendly manner'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] PALS (Pathway Activity Level Scoring): 'we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways'
- `ev_011` from `agent2_synthesis` (agent2_traced): [intro] GNPS: 'Molecular Families from GNPS'
- `ev_012` from `agent2_synthesis` (agent2_traced): [intro] MS2LDA: 'Mass2Motifs from MS2LDA'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] specific published results (tables, figures, or supplementary files) demonstrating PLAGE decomposition applied to GNPS Molecular Families: 'N/A — section text does not report quantitative results or point to supplementary data for this generalization'
- `ev_015` from `agent2_synthesis` (agent2_traced): [other] specific published results (tables, figures, or supplementary files) demonstrating PLAGE decomposition applied to MS2LDA Mass2Motifs: 'N/A — section text does not report quantitative results or point to supplementary data for this generalization'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] reference to or location of the exact test dataset(s) used to validate decomposition on these non-pathway metabolite sets: 'N/A — no concrete accession, URL, or file path is cited in the discussion section'

## Evaluation Strategy
### Direct Checks
- Verify that PALS repository (github:glasgowcompbio/PALS) contains documented implementation of PLAGE decomposition method
- Verify file_exists: locate example or test data in PALS repository using GNPS Molecular Families format
- Verify file_exists: locate example or test data in PALS repository using MS2LDA Mass2Motifs format
- Script_runs: execute PALS decomposition on GNPS Molecular Families input and confirm output artifact is produced
- Script_runs: execute PALS decomposition on MS2LDA Mass2Motifs input and confirm output artifact is produced
- Verify output_matches_reference: compare decomposition scores/loadings from both non-pathway metabolite sets against any published reference results or supplementary tables reporting PLAGE application to these data types

### Expert Review
- Confirm that reported decomposition results for Molecular Families and Mass2Motifs demonstrate statistically and biologically meaningful variance decomposition consistent with the PLAGE method's theoretical properties
- Assess whether the generalization to fragmentation-spectrum-derived groupings (GNPS and MS2LDA) is substantively different from pathway-based analysis and whether results validate the claim of generalization
- Evaluate robustness claims: verify that PLAGE scores on these non-pathway metabolite sets show comparable or superior noise tolerance relative to ORA/GSEA baselines if such comparisons are reported

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load metabolomics data and non-pathway metabolite groupings (Molecular Families and Mass2Motifs).
2. Apply PALS decomposition using PLAGE algorithm to calculate activity scores for each metabolite set across samples.
3. Assess robustness of PLAGE scores by introducing noise or simulating missing peaks and comparing stability to pathway-based results.
4. Validation: PLAGE successfully decomposes non-pathway metabolite sets with comparable or superior robustness to noise/missing peaks as pathway-based analyses, confirming generalisation beyond curated pathway annotations.
5. References: source article (DOI: 10.1186/1471-2105-6-225)

## Workflow Ports

**Inputs:**

- `metabolomics_data` — Metabolomics expression data (peak intensity or abundance matrix)
- `gnps_families` — Molecular Families from GNPS
- `ms2lda_motifs` — Mass2Motifs from MS2LDA

**Outputs:**

- `gnps_plage_scores` — PLAGE activity scores for GNPS Molecular Families
- `ms2lda_plage_scores` — PLAGE activity scores for MS2LDA Mass2Motifs
- `robustness_comparison` — Robustness evaluation against noise and missing peaks
- `generalization_results` — Results confirming PLAGE generalisation beyond pathways

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:glasgowcompbio__PALS`
- **Synthesized at:** 2026-06-15T21:33:33+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

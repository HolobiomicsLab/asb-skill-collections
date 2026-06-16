# SciTask Card: Reconstruct the paired scATAC-seq and scRNA-seq multiome analysis pipeline in ArchR

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T18:08:30.308650+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_archr/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`
- GitHub: `GreenleafLab/ArchR`
- Quality: Score 2/5 — Coherent: false, placeholder, 7 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `genomics`
- Subdomains: `gene-regulation`, `multi-omics-integration`
- Techniques: `clustering`, `dimensionality-reduction`

## Research Question
How does ArchR ingest paired scRNA-seq gene expression data alongside scATAC-seq chromatin accessibility data and produce a unified reduced-dimension embedding for joint analysis?

## Connected Finding
The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces the joint reduced-dimension embedding integrating both modalities.

## Task Description
Ingest paired scRNA-seq and scATAC-seq data into ArchR using importFeatureMatrix and addGeneExpressionMatrix, then compute joint reduced-dimension embeddings via addIterativeLSI and addCombinedDims to enable integrated multiome analysis.

## Inputs
- scATAC-seq peak matrix and cell metadata
- scRNA-seq gene expression matrix aligned to the same cells

## Expected Outputs
- ArchR project object containing both scATAC-seq and scRNA-seq data with joint LSI reduction and combined dimensional embedding

## Landmark Outputs

- `archR_project_with_scatac.rds`
- `archR_project_with_scrna.rds`
- `archR_project_with_lsi.rds`

## Tools
- ArchR
- R

## Skills
- multiome-data-ingestion-paired-modalities
- iterative-lsi-dimensionality-reduction
- cross-modality-embedding-integration
- atac-seq-feature-matrix-construction
- rna-seq-expression-alignment-across-cells

## Workflow Description
1. Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. 2. Load scRNA-seq gene expression matrix and call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities. 3. Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. 4. Call addCombinedDims to generate a unified reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a single coordinate space.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ArchRProject_Schematic.png` | figure | False |
| `figures/ArchR_FunctionSchematic.png` | figure | False |
| `figures/ArchR_Logo_Integrated.png` | figure | False |
| `figures/ArchR_Workflow_Horizontal.png` | figure | False |
| `figures/Cluster6-Cluster10-Marker-Peaks_1.png` | figure | False |
| `figures/Cluster6-Cluster10-Marker-Peaks_2.png` | figure | False |
| `figures/Cluster6-Cluster10-Motifs-Down_1.png` | figure | False |
| `figures/Cluster6-Cluster10-Motifs-Up_1.png` | figure | False |
| `figures/Cluster6-Marker-Peaks_1.png` | figure | False |
| `figures/FRIP-TSS-Enrichment_1.png` | figure | False |
| `figures/FRIP-TSS-Enrichment_2.png` | figure | False |
| `figures/Footprints-Divide-Bias_1.png` | figure | False |
| `figures/Frags_vs_TSS.png` | figure | False |
| `figures/GeneActivityScore_Schematic.png` | figure | False |
| `figures/TSS_vs_FRiP.png` | figure | False |
| `figures/UMAP-Samples-Clusters_1.png` | figure | False |
| `figures/UMAP-Samples-Clusters_2.png` | figure | False |
| `figures/UMAP-Samples-Clusters_3.png` | figure | False |
| `figures/favicon-16x16.png` | figure | False |
| `figures/favicon-32x32.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting the features, bug fixes, or version history of the paired multiome workflow functions (importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims) is available

## Domain Knowledge
- importFeatureMatrix registers a pre-computed peak matrix (typically sparse matrix format from tools like Signac or MAESTRO) into ArchR as the primary accessibility assay.
- addGeneExpressionMatrix requires cell barcodes to be matched exactly between scATAC and scRNA datasets; misalignment will cause silent data loss or errors.
- Iterative LSI (latent semantic indexing) is an unsupervised dimensionality reduction tailored for sparse, high-dimensional accessibility and expression data, typically reducing to 30–50 dimensions per iteration.
- addCombinedDims fuses the LSI embeddings from both modalities using canonical correlation or weighted averaging to create a single joint embedding space suitable for clustering and visualization.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: ArchR project object containing both scATAC-seq and scRNA-seq data with joint LSI reduction and combined dimensional embedding.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does ArchR ingest paired scRNA-seq gene expression data alongside scATAC-seq chromatin accessibility data and produce a unified reduced-dimension embedding for joint analysis?: 'ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces the joint reduced-dimension embedding integrating both modalities.: 'See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] scATAC-seq peak matrix and cell metadata: 'importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] scRNA-seq gene expression matrix aligned to the same cells: 'importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] ArchR project object containing both scATAC-seq and scRNA-seq data with joint LSI reduction and combined dimensional embedding: 'ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] ArchR: 'ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] R: 'ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting the features, bug fixes, or version history of the paired multiome workflow functions (importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims) is available: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that github:GreenleafLab__ArchR repository is accessible and contains ArchR package source code
- verify that ArchR package documentation or vignettes include functions importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims
- script_runs: execute a minimal R script that loads ArchR, calls importFeatureMatrix on a test scRNA-seq matrix, calls addGeneExpressionMatrix on a test ArchRProject with paired scATAC-seq data, calls addIterativeLSI, and calls addCombinedDims without errors
- verify that the R script output includes a ArchRProject object or SummarizedExperiment with dimensionality-reduction slots populated (e.g., containing LSI or combined embedding matrices)
- verify that the combined embedding produced has multiple dimensions (parameter-sensitive: exact dimensionality may vary by LSI iteration count, but must be ≥ 2)

### Expert Review
- assess whether the joint reduced-dimension embedding produced by addCombinedDims meaningfully integrates information from both scATAC-seq and scRNA-seq modalities (e.g., by examining correlation structure, variance explained, or cross-modality clustering concordance)
- evaluate whether the paired multiome workflow as implemented follows best practices for joint dimensionality reduction in the scATAC-seq and scRNA-seq literature

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load scATAC-seq peak matrix and cell metadata into ArchR project object via importFeatureMatrix.
2. Append scRNA-seq gene expression matrix to the same project via addGeneExpressionMatrix, aligning cells across modalities.
3. Compute joint iterative LSI decomposition on accessibility and expression data via addIterativeLSI.
4. Generate unified reduced-dimension embedding integrating both modalities via addCombinedDims.
5. Validation: Confirm multiome project object contains both scATAC-seq and scRNA-seq assays with non-null LSI and combined dimension slots.

## Workflow Ports

**Inputs:**

- `scatac_peak_matrix` — scATAC-seq peak matrix and metadata
- `scrna_expr_matrix` — scRNA-seq gene expression matrix

**Outputs:**

- `multiome_project` — ArchR project with integrated scATAC and scRNA-seq embeddings

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:GreenleafLab__ArchR`
- **Synthesized at:** 2026-06-15T18:11:26+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (7):
  - research_question: evidence_span ('ArchR now supports paired scATAC-seq and scRNA-seq Analysis!') does not substantively answer the 'How does ArchR ingest...' question—it announces support but does not explain the mechanism or workflow
  - finding: evidence_span ('See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims') is a function list only; it does not explain the four-step process or validate that these functions operate in the described sequence
  - expected_outputs[0]: evidence_span does not describe the output format, contents, or structure of the ArchR project object; it only announces multiome support
  - inputs[0]: evidence_span is function names only; it does not ground what 'scATAC-seq peak matrix and cell metadata' concretely are or how they are formatted
  - inputs[1]: evidence_span is function names only; does not ground 'scRNA-seq gene expression matrix aligned to the same cells' or describe alignment mechanism
  - tools[0]: evidence_span ('ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data') does not mention scRNA-seq or multiome capabilities—potentially outdated or incomplete grounding
  - missing_information[0]: evidence_span ('_No changelog found._') is not a valid span; it is a placeholder indicating absence of evidence
- Notes: This task card exhibits significant coherence and grounding gaps. The research_question is mechanistic ('How does ArchR ingest...') but the evidence is purely declarative ('ArchR now supports...'). The finding narrates a detailed four-step workflow but the evidence_span is only a function list, lacking any temporal or causal sequence. Inputs and outputs are generic placeholders without concrete data formats or file references. The grounding for tools[0] describes only ATAC-seq capabilities, ignoring the multiome focus. The missing_information entry uses a meta-statement ('No changelog found.') rather than an actual text span. For a task of this complexity, substantially richer grounding (e.g., links to ArchR documentation, worked examples, or API signatures) is required. Recommend: (1) obtain and cite specific ArchR vignette or documentation sections that explain the workflow; (2) replace generic descriptions with concrete artifact names and formats; (3) ground the four-step narrative with step-by-step code or pseudocode; (4) verify tools[0] description includes multiome support or cite updated source; (5) remove meta-statements from evidence_span fields.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

# SciTask Card: Analyze the distribution of Tn5 insertion events around known transcription factor binding sites from a public ATAC-seq dataset

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:12:11.236771+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_tobias/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `visualization`
- DOI: `10.1038/s41467-020-18035-1`
- GitHub: `loosolab/TOBIAS`
- Input from: `task_003`

## Classification

- Task kind: `analysis`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `gene-regulation`, `functional-genomics`
- Techniques: `enrichment-analysis`, `statistical-analysis`

## Research Question
What is the characteristic pattern of Tn5 insertion depletion around transcription factor binding sites versus non-binding sites across a genomic region?

## Connected Finding
ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound motif locations.

## Task Description
Using a public ATAC-seq dataset and a reference set of transcription factor (TF) motif coordinates, quantify and tabulate Tn5 insertion counts in flanking windows (e.g. ±100 bp) around bound versus unbound motif sites to empirically characterize the footprint signal—regions of nucleotide depletion marking protein occupancy.

## Inputs
- ATAC-seq BAM alignment file from a public repository (GEO/SRA accession or direct URL)
- Reference set of transcription factor motif genomic coordinates (BED format or similar)

## Expected Outputs
- Tabulated positional distribution of Tn5 insertion counts for bound and unbound motif sites
- Visualization (line plot or heatmap) of insertion profiles showing footprint signal (depletion at bound sites)

## Expected Output File

- `tn5_insertion_distribution_table.csv`

## Landmark Outputs

- `motif_sites_classified.bed`
- `tn5_insertions_per_site.txt`
- `insertion_counts_by_position.csv`
- `footprint_profile_bound_vs_unbound.png`

## Tools
- TOBIAS

## Skills
- atac-seq-bam-read-alignment-processing
- transcription-factor-motif-genomic-coordinate-annotation
- tn5-insertion-position-extraction-and-counting
- nucleotide-footprint-pattern-recognition
- chromatin-accessibility-binding-status-classification
- positional-distribution-profile-aggregation-and-visualization

## Workflow Description
1. Download ATAC-seq BAM file and TF motif coordinate annotations from a public repository (GEO/SRA). 2. Classify motif sites as bound or unbound based on chromatin accessibility or binding signal thresholds. 3. Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). 4. Aggregate insertion counts per position bin across all sites within each class (bound/unbound). 5. Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position. 6. Tabulate results as a matrix of insertion counts by position and site class; generate visualization showing insertion profiles across bound and unbound sites to confirm footprint depletion signal in bound sites.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/BATF_footprint_comparison_all.png` | figure | False |
| `figures/BATF_footprint_comparison_subsets.png` | figure | False |
| `figures/BATF_heatmap.png` | figure | False |
| `figures/IRF1_footprint.png` | figure | False |
| `figures/atacorrect.png` | figure | False |
| `figures/bindetect.png` | figure | False |
| `figures/chr4-119628321-119629356.png` | figure | False |
| `figures/chr4-163701830-163702617.png` | figure | False |
| `figures/footprinting.png` | figure | False |
| `figures/network.png` | figure | False |
| `figures/tobias.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history provided for TOBIAS repository or methods

## Domain Knowledge
- ATAC-seq footprints manifest as local depletion (or reduced insertion density) of Tn5 transposase insertions in flanking windows around TF-bound motif sites, arising from protein-DNA occupancy that physically blocks transposase access.
- Bound versus unbound motif classification typically relies on peak signal from aligned reads (e.g. pileup height, accessibility score) or external TF ChIP-seq/binding data; unbound sites serve as negative control with expected uniform or near-uniform insertion distribution.
- Window size and position bin resolution (e.g. ±100 bp around motif center, 1 bp or 5 bp bins) directly affect visibility and quantification of footprint depth; smaller bins reveal fine structure while larger bins reduce noise.
- Tn5 transposase shows a known insertion bias (preferential cutting at certain dinucleotide motifs); correcting for intrinsic sequence bias may be necessary when comparing insertion rates across genomic regions.
- Aggregation across many sites (hundreds to thousands of motif instances) is essential to reveal the footprint signal; single-site insertion patterns are typically noisy.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the characteristic pattern of Tn5 insertion depletion around transcription factor binding sites versus non-binding sites across a genomic region?: 'the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound motif locations.: 'the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] ATAC-seq BAM alignment file from a public repository (GEO/SRA accession or direct URL): 'Using a publicly deposited ATAC-seq dataset (e.g. GEO/SRA)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Reference set of transcription factor motif genomic coordinates (BED format or similar): 'reference set of TF motif coordinates'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Tabulated positional distribution of Tn5 insertion counts for bound and unbound motif sites: 'compute and tabulate the positional distribution of Tn5 insertion counts in windows flanking bound versus unbound motif sites'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Visualization (line plot or heatmap) of insertion profiles showing footprint signal (depletion at bound sites): 'empirically characterise the footprint signal described in the article'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] TOBIAS: '**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history provided for TOBIAS repository or methods: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that a publicly deposited ATAC-seq dataset (GEO or SRA accession) is retrievable and contains aligned reads in standard format (BAM/bedGraph)
- verify that a reference set of TF motif coordinates is provided as a structured file (BED or tabular format) with chromosome, start, end, and motif identity fields
- verify that the computed positional distribution table exists as a named artifact (TSV, CSV, or structured data frame)
- verify that the table contains at least two distinct categories (bound vs. unbound motif sites) and position-indexed Tn5 insertion count columns
- verify that insertion counts are numeric, non-negative, and row_count_equals the number of distinct position windows analyzed
- verify that script or pipeline used to compute positional distributions runs without fatal errors on the specified inputs
- verify output matches reference footprint signal: depletion of insertions at bound motif sites should be visually or statistically distinguishable from unbound sites (no canonical answer for exact magnitude; expert review required for biological interpretation)

### Expert Review
- confirm that the positional distribution pattern (insertion depletion at bound sites) is consistent with the ATAC-seq footprinting phenomenon described in the article and literature
- assess whether the magnitude and width of the observed footprint signal is biologically plausible for the TF(s) and cell type(s) under study
- evaluate whether the bound versus unbound site comparison is appropriately controlled (e.g., background chromatin accessibility, motif quality thresholds, statistical significance)
- judge whether the tabulation method and window definitions are methodologically sound and clearly documented

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load ATAC-seq BAM file and extract Tn5 insertion positions from aligned read 5' ends (or start coordinates).
2. Annotate motif sites as bound or unbound based on chromatin accessibility signal or external binding data.
3. For each motif instance, extract Tn5 insertion counts in fixed-width flanking windows (e.g. ±100 bp) at single-nucleotide or fine-grain bin resolution.
4. Aggregate insertion counts across all motif sites within each binding class and compute positional statistics (mean, standard deviation).
5. Tabulate positional insertion distributions and generate comparative visualization (e.g. line plot) of bound versus unbound profiles to confirm footprint depletion.
6. Validation: footprint signal is confirmed by visual inspection of depletion pattern at bound sites (reduced insertion density flanking the motif) and absence of depletion at unbound sites.
7. References: source article (DOI: 10.1038/s41467-020-18035-1)

## Workflow Ports

**Inputs:**

- `atac_bam` — ATAC-seq BAM alignment file ← `task_003/tf_occupancy_table`
- `motif_coords` — Transcription factor motif coordinate annotations

**Outputs:**

- `insertion_table` — Tabulated Tn5 insertion counts by position and motif-binding status
- `footprint_plot` — Visualization of Tn5 insertion distribution at bound versus unbound sites

**Used:** `urn:asb:port:task_003/tf_occupancy_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:loosolab__TOBIAS`
- **Synthesized at:** 2026-06-15T19:17:04+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

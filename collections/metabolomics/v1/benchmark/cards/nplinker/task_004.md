# SciTask Card: Reconstruct the NPLinker pipeline fixed processing architecture for loading, scoring, and filtering GCF-MF hypothetical links

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:56:40.523217+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_nplinker`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1008920`
- GitHub: `NPLinker/nplinker`
- Input from: `task_002`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `natural-products`, `microbiome-metabolomics`, `multi-omics-integration`
- Techniques: `correlation-analysis`, `machine-learning`, `database-annotation`, `network-annotation-propagation`

## Research Question
How does NPLinker orchestrate the integration of antiSMASH/BiG-SCAPE genomic outputs and GNPS metabolomic outputs to create and rank hypothetical BGC-metabolite links?

## Connected Finding
NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations, then generates hypothetical links between metabolomic and genomic objects that can be evaluated using various scoring functions (both built-in and custom) and sorted, filtered, and visualized in tabular format.

## Task Description
Implement the NPLinker framework orchestration layer that ingests antiSMASH-predicted BGCs and BiG-SCAPE-clustered GCFs from genomic data, GNPS metabolomic outputs (spectra and molecular families), and produces a filterable ranked table of GCF–MF (or BGC–spectrum) hypothetical links scored by standardised strain correlation and IOKR functions.

## Inputs
- antiSMASH v5.0.0 BGC predictions (JSON or GenBank format) from microbial genome assemblies
- GNPS metabolomic data: MS2 spectra with strain annotations and molecular families from spectral clustering
- MIBiG database reference BGCs with structural annotations for homology scoring

## Expected Outputs
- Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score
- NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF–MF and BGC–spectrum relationships with associated scores
- Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections

## Expected Output File

- `ranked_links.csv`

## Landmark Outputs

- `gcfs_clustered.txt`
- `hypothetical_links_raw.csv`
- `strain_correlation_scores.csv`
- `iokr_scores.csv`
- `ranked_links.csv`
- `percentile_enrichment_stats.json`

## Tools
- antiSMASH
- BiG-SCAPE
- NPLinker
- GNPS
- MIBiG

## Skills
- biosynthetic-gene-cluster-detection-and-annotation
- gene-cluster-family-formation-and-similarity-clustering
- strain-correlation-scoring-and-hypergeometric-standardisation
- input-output-kernel-regression-for-metabolite-matching
- multi-criterion-score-combination-and-ranking
- metabolomic-spectral-annotation-and-molecular-family-clustering
- cross-database-structural-homology-matching

## Workflow Description
1. Load antiSMASH v5.0.0 BGC predictions from input microbial genomes and run BiG-SCAPE v1.0.0 to cluster BGCs into Gene Cluster Families (GCFs), grouping BGCs by product class and similarity distance. 2. Import GNPS metabolomic data: MS2 spectra, molecular families (MFs) from spectral clustering, and strain annotations for each spectrum and MF. 3. Create NPLinker in-memory objects (Spectrum, MF, BGC, GCF entities) maintaining hierarchical relationships and strain IDs; construct the complete set of hypothetical GCF–MF link combinations. 4. For each hypothetical link, compute standardised strain correlation score by calculating hypergeometric expected value and variance of the raw correlation score across all links, then z-normalise: s*_corr = (s_corr − E[s_corr]) / √Var[s_corr]. 5. For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints from predicted metabolite structures and score BGC–spectrum links using Input-Output Kernel Regression (IOKR) with CDK substructure, PubChem, and Klekota-Roth fingerprints and probability product kernel filtering. 6. Standardise IOKR scores using expected value and variance over the set of all potential links: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]; aggregate BGC–spectrum IOKR scores to GCF–MF level by taking the maximum. 7. Combine standardised scores using ℓ₁/₂-norm with sign adjustment: s_combined = sgn(s*_corr)|s*_corr|^(1/2) + sgn(s*_IOKR)|s*_IOKR|^(1/2). 8. Rank all hypothetical links by combined score and export as filterable table with sortable columns for each scoring function and complementary filtering options (strain, MIBiG inclusion, product type). Validation: confirm that links scoring in the joint 90th percentile for both standardised strain correlation and IOKR show significantly higher enrichment of validated links (p < 0.05) compared to either score alone.

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
- Specific file format and schema for antiSMASH output ingested by NPLinker (GenBank, JSON, or other)
- Specific file format and schema for BiG-SCAPE output ingested by NPLinker (cluster assignment table or other)
- Specific file format and schema for GNPS metabolomic data ingested by NPLinker (spectrum library metadata, MS/MS spectra in mzXML/mzML or other)
- Details on how NPLinker resolves the 'antiSMASH mapping the same ID to multiple GCFs' edge case during orchestration
- Computational time complexity and memory requirements for the NPLinker orchestration loop (BGC-spectrum enumeration, strain correlation computation, IOKR scoring)
- Quantitative measure of homology threshold used to assign MIBiG structures to BGCs for IOKR candidate set filtering
- Specific kernel function (PPK parameters, bandwidth, or other hyperparameters) used in the IOKR component of NPLinker
- Specific molecular fingerprint algorithm and parameters used in the IOKR component of NPLinker
- Documented validation workflow or test suite for verifying NPLinker orchestration correctness on known positive and negative link sets

## Domain Knowledge
- Biosynthetic Gene Clusters (BGCs) are contiguous genomic regions whose genes collectively encode enzymes for production of one or more structurally related specialised metabolites; antiSMASH prediction yields a large fraction of unknown products requiring correlation with metabolomic data for validation.
- Gene Cluster Families (GCFs) group related BGCs across strains by similarity distance; the assumption underlying GCF-level scoring is that BGCs close in GCF space encode structurally or functionally similar metabolites.
- Strain correlation scoring relies on the overlap of strain sets contributing to a GCF and a Molecular Family; raw overlap counts are biased by dataset size, necessitating hypergeometric standardisation to make scores comparable across links of different GCF and MF sizes.
- Input-Output Kernel Regression (IOKR) projects MS2 spectra into molecular fingerprint space to rank candidate BGC structures without requiring product-class-specific models, but requires considerable MIBiG homology (cumulative BLAST score ≥10,000) to assign structural predictions.
- The complementarity of strain correlation (correlation-based) and IOKR (feature-based) scores arises because strain correlation is invariant to molecular structure and sensitive only to presence/absence patterns, while IOKR is sensitive to chemical features independent of strain content; combining both scores increases enrichment of validated links in the top percentile.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] How does NPLinker orchestrate the integration of antiSMASH/BiG-SCAPE genomic outputs and GNPS metabolomic outputs to create and rank hypothetical BGC-metabolite links?: 'NPLinker accepts genomic outputs from antiSMASH and BiG-SCAPE (including reference BGCs from the MIBiG database [32]), and metabolomic output from the public, community-driven Global Natural Products'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] NPLinker creates objects for spectra, MFs, BGCs and GCFs from input data while maintaining hierarchical relationships and strain associations, then generates hypothetical links between metabolomic and genomic objects that can be evaluated using various scoring functions (both built-in and custom) and sorted, filtered, and visualized in tabular format.: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them, and keeps track of strain ID or IDs associated with each object.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] antiSMASH v5.0.0 BGC predictions (JSON or GenBank format) from microbial genome assemblies: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] GNPS metabolomic data: MS2 spectra with strain annotations and molecular families from spectral clustering: 'metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base [33]'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] MIBiG database reference BGCs with structural annotations for homology scoring: 'BGCs from the relevant strains show significant homology to the MIBiG BGC. Because both of them belong to the product class'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Ranked hypothetical link table (CSV or TSV) with GCF ID, MF ID, standardised strain correlation score, IOKR score, combined ℓ₁/₂ score, and metadata (strain count, BGC size, product type) sorted by combined score: 'links can be sorted, inspected and filtered by various scoring functions or combinations thereof, and visualised as tables'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] NPLinker link objects and metadata structure (JSON or Python pickle) persisting GCF–MF and BGC–spectrum relationships with associated scores: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Filtering and ranking statistics: count of links scoring above 90th percentile for each scoring function and their intersections: 'links scoring above the 90th percentile for raw correlation, standardised correlation and IOKR scores'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] antiSMASH: 'the genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] BiG-SCAPE: 'and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] NPLinker: 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] GNPS: 'metabolomic output from the public, community-driven Global Natural Products Social (GNPS) knowledge base'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] MIBiG: 'MIBiG database [32] most of which have structural annotations'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] Specific file format and schema for antiSMASH output ingested by NPLinker (GenBank, JSON, or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] Specific file format and schema for BiG-SCAPE output ingested by NPLinker (cluster assignment table or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Specific file format and schema for GNPS metabolomic data ingested by NPLinker (spectrum library metadata, MS/MS spectra in mzXML/mzML or other): 'By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Details on how NPLinker resolves the 'antiSMASH mapping the same ID to multiple GCFs' edge case during orchestration: 'antiSMASH mapping the same ID to multiple GCFs, as discussed earlier'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Computational time complexity and memory requirements for the NPLinker orchestration loop (BGC-spectrum enumeration, strain correlation computation, IOKR scoring): 'As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] Quantitative measure of homology threshold used to assign MIBiG structures to BGCs for IOKR candidate set filtering: 'restricts its use to those BGCs which show considerable homology with MIBiG entries'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] Specific kernel function (PPK parameters, bandwidth, or other hyperparameters) used in the IOKR component of NPLinker: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'
- `ev_021` from `agent2_synthesis` (agent2_traced): [discussion] Specific molecular fingerprint algorithm and parameters used in the IOKR component of NPLinker: 'IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints'
- `ev_022` from `agent2_synthesis` (agent2_traced): [discussion] Documented validation workflow or test suite for verifying NPLinker orchestration correctness on known positive and negative link sets: 'As an additional level of validation, we tested some high scoring links by exploring whether it was possible to manually match peaks in the MS2 spectra to the chemical structures'

## Evaluation Strategy
### Direct Checks
- verify file exists at https://github.com/sdrogers/nplinker (GitHub repository root)
- verify file exists at http://doi.org/10.5281/zenodo.4680579 (Zenodo release archive)
- script_runs: clone NPLinker repository and execute setup.py or equivalent package installation without errors
- file_format_is: NPLinker source tree contains nplinker/ module directory with __init__.py
- file_exists: NPLinker repository contains documented integration point for antiSMASH output (file path or module name)
- file_exists: NPLinker repository contains documented integration point for BiG-SCAPE output (file path or module name)
- file_exists: NPLinker repository contains documented integration point for GNPS output (file path or module name)
- contains_substring: NPLinker codebase or documentation references 'GCF' and 'MF' (molecular feature) as object types
- contains_substring: NPLinker codebase or documentation describes strain correlation scoring function or method
- contains_substring: NPLinker codebase or documentation describes IOKR (Input-Output Kernel Regression) scoring function or integration
- file_exists: NPLinker source tree contains implementation of combined scoring function (strain correlation + IOKR)
- output_matches_reference: run NPLinker on a small test dataset (subset of Crüsemann or similar public paired omics data) and verify output table structure contains columns for GCF identifier, spectrum identifier, strain correlation score, IOKR score, and combined rank
- file_format_is: NPLinker primary output artifact is a table (CSV, TSV, JSON, or database format) with filterable ranked link records
- field_present: output link table contains at least the following fields: GCF_ID, spectrum_ID, strain_correlation_score, IOKR_score, combined_score, rank
- script_runs: NPLinker orchestration layer accepts antiSMASH BGC annotations (GenBank or JSON format) without format conversion errors
- script_runs: NPLinker orchestration layer accepts BiG-SCAPE GCF clustering output without format conversion errors
- script_runs: NPLinker orchestration layer accepts GNPS MS/MS spectrum library metadata without format conversion errors
- value_in_range: combined scoring function applies ℓp-norm with p=0.5 and sign-adjusted absolute values (robust to parameter choices in combining function)
- contains_substring: NPLinker documentation or code comments explain the control loop: input → GCF-MF hypothetical link enumeration → score application → filtering → ranked output
- file_exists: NPLinker repository includes example or demo configuration file showing how to chain antiSMASH → BiG-SCAPE → GNPS inputs

### Expert Review
- Verify that the NPLinker orchestration logic correctly maps antiSMASH-detected BGCs into BiG-SCAPE GCF clusters (no misalignment of identifiers or lost BGCs)
- Verify that strain correlation score computation accurately reflects the presence/absence of shared strains between GCF and MF (biological correctness of the metric)
- Verify that IOKR scoring function is correctly applied: molecular fingerprints are derived from structures, kernel is applied to spectra, predictions are bounded in expected range
- Verify that the combined scoring function (ℓp-norm with p=0.5) preserves directionality and relative ranking of both component scores
- Verify that the output ranked link table is filterable by percentile threshold (e.g., 90th percentile) and that filtered results match the proportions and p-values reported in Table 2 of the article
- Verify that NPLinker handles edge cases correctly: BGCs with no MIBiG homology (should be excluded from IOKR scoring), spectra with insufficient peaks (should be denoised or excluded), multiple GCFs mapping to the same BGC (antiSMASH edge case mentioned in results)
- Verify that the control loop terminates gracefully and produces interpretable error messages when inputs are malformed or incomplete

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Cluster detected BGCs into Gene Cluster Families (GCFs) using BiG-SCAPE, grouping by product class and similarity distance.
2. Generate the complete set of hypothetical GCF–Molecular Family (MF) link combinations from input genomic and metabolomic data.
3. Compute standardised strain correlation score for each link by calculating hypergeometric expected value and variance and z-normalising.
4. Score BGC–spectrum links using Input-Output Kernel Regression (IOKR) on molecular fingerprints for BGCs with MIBiG structural homology; aggregate to GCF–MF level.
5. Standardise IOKR scores and combine both standardised scores using ℓ₁/₂-norm with sign adjustment to produce a single ranking.
6. Rank all hypothetical links and export table with filtering and sorting options; calculate enrichment statistics for validated links at 90th percentile.
7. Validation: confirm that joint 90th-percentile links show significantly higher proportion of validated links (p < 0.05) than either score alone.
8. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

## Workflow Ports

**Inputs:**

- `antismash_bgc_predictions` — antiSMASH v5.0.0 BGC predictions ← `task_002/iokr_model`
- `gnps_spectra_mf` — GNPS MS2 spectra and molecular families with strain annotations
- `mibig_reference` — MIBiG database reference BGCs

**Outputs:**

- `ranked_link_table` — Ranked GCF–MF hypothetical link table with all scores
- `nplinker_link_objects` — Persisted NPLinker link objects and metadata
- `percentile_statistics` — Filtering and ranking enrichment statistics at 90th percentile

**Used:** `urn:asb:port:task_002/iokr_model`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

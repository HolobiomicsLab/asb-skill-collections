# SciTask Card: Analyze database search pipeline tool dispatch across Dereplicator, VarQuest, and Dereplicator+ on test spectra

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:40:21.538092+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_dereplicator/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `benchmark-evaluation`
- GitHub: `ablab/npdtools`
- Input from: `task_003`

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `natural-products`, `computational-metabolomics`
- Techniques: `dereplication`, `database-annotation`, `in-silico-fragmentation`

## Research Question
Which of the three NPDtools database search pipelines (Dereplicator, VarQuest, Dereplicator+) successfully identify matches in MSV000080102-derived test spectra, and how do their hit patterns differ across search modes?

## Connected Finding
NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit for natural product mass spectrometry analysis.

## Task Description
Run MetaMiner, Dereplicator, and VarQuest pipelines independently on MSV000080102-derived test spectra with the same RiPP sequences; compare significant_matches.tsv outputs to characterize tool-specific hit patterns across standard and blind search modes.

## Inputs
- Three LC-MS/MS spectra files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) from MSV000080102 dataset
- Example RiPP sequence file (example_RiPP.fasta) containing predicted amino acid sequences
- Precomputed spectral network output files from GNPS (MSV000080102 clustered spectra data)

## Expected Outputs
- significant_matches.tsv from MetaMiner standard mode run
- significant_matches.tsv from MetaMiner blind mode run
- Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence)
- VarQuest match results table (format: tab-separated value file with standardized columns for comparison)
- Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences

## Expected Output File

- `tool_comparison_summary.tsv`

## Landmark Outputs

- `metaminer_standard_mode/significant_matches.tsv`
- `metaminer_blind_mode/significant_matches.tsv`
- `dereplicator_output/matches.tsv`
- `varquest_output/matches.tsv`

## Tools
- NPDtools 2.5.0
- MetaMiner
- Dereplicator
- ProteoWizard
- Python

## Skills
- ripp-peptide-sequence-database-construction
- tandem-mass-spectra-peptide-matching
- post-translational-modification-mass-shift-detection
- spectral-scoring-and-significance-assessment
- cross-tool-result-concordance-analysis
- false-discovery-rate-interpretation
- blind-search-mode-parameter-optimization

## Workflow Description
1. Prepare test spectra (three .mzML files from MSV000080102 converted to MGF using ProteoWizard msconvert) and example RiPP sequence file (example_RiPP.fasta). 2. Execute MetaMiner with standard parameters (default lantibiotic class) on test spectra and RiPP sequences, generate significant_matches.tsv. 3. Execute MetaMiner again with --blind flag enabled to search for arbitrary post-translational modifications. 4. Execute Dereplicator pipeline on the same test spectra and RiPP structure database, output match results. 5. Execute VarQuest pipeline on the same inputs with standard parameters. 6. Parse and tabulate significant_matches.tsv outputs from all three tools, recording scan identifiers, match scores, p-values, and false discovery rates. 7. Cross-compare hit sets to identify tool-specific detections, common identifications, and mode-dependent sensitivity differences.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/MetaMiner_fig.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000080102` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102 | twork of identified RiPP.  It is based on a few files from [MSV000080102 dataset](https://gnps.ucsd.edu/ProteoSAFe/result.jsp?task=6 |
| sra_run | `SRR3309439` | https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439 | ces griseus ATCC 12648](https://www.ebi.ac.uk/ena/data/view/SRR3309439)),  and `spades_outdir` is the directory containing the gen |

## Missing Information
- No changelog found

## Domain Knowledge
- RiPP metabolites are ribosomally synthesized and post-translationally modified peptides requiring specialized peptide-mass databases and spectral matching algorithms distinct from small-molecule compound identification.
- Blind mode search enables detection of unanticipated post-translational modifications by allowing arbitrary mass shifts during spectral matching, at the cost of substantially increased computational time and false-positive rate.
- Significant_matches.tsv output format standardizes compound–spectrum match reporting across NPDtools pipelines with mandatory columns for scan number, spectrum mass, score, p-value, FDR, peptide mass, and modified sequence annotation.
- Mass spectrometry data must be centroided (not profile mode) and in open formats (MGF, mzXML, mzML, or mzData) for accurate spectral matching; unconverted raw proprietary formats cannot be processed.
- Tool concordance analysis requires normalized scoring schemes across pipelines; direct score comparison is invalid because Dereplicator, VarQuest, and MetaMiner may use different scoring metrics despite outputting standardized TSV columns.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: MetaMiner, ProteoWizard, Python, significant_matches.tsv from MetaMiner standard mode run, significant_matches.tsv from MetaMiner blind mode run, Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence), VarQuest match results table (format: tab-separated value file with standardized columns for comparison), Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Which of the three NPDtools database search pipelines (Dereplicator, VarQuest, Dereplicator+) successfully identify matches in MSV000080102-derived test spectra, and how do their hit patterns differ across search modes?: 'NPDtools – Natural Product Discovery tools – is a toolkit containing various pipelines for _in silico_ analysis of natural product mass spectrometry data'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] NPDtools version 2.5.0 includes multiple database search pipelines (Dereplicator, VarQuest, Dereplicator+) within its toolkit for natural product mass spectrometry analysis.: 'NPDtools version 2.5.0 was released under the Apache 2.0 License on November 28, 2019 and can be downloaded from <https://github.com/ablab/npdtools/releases>'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Three LC-MS/MS spectra files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) from MSV000080102 dataset: 'Download `C18p_5uL_NASA_Sample_BB2_01_25958.mzML`, `C18p_5uL_NASA_Sample_BB3_01_25959.mzML` and `C18p_5uL_NASA_Sample_BB4_01_25960.mzML` files from [MSV000080102]'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Example RiPP sequence file (example_RiPP.fasta) containing predicted amino acid sequences: 'an example RiPP `DATITTVTVTSTSIWASTVSNHC` (available in `test_data/metaminer/molnet/example_RiPP.fasta`)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Precomputed spectral network output files from GNPS (MSV000080102 clustered spectra data): 'Run spectral networks on the downloaded spectra or download their precomputed spectral network from [GNPS]'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] significant_matches.tsv from MetaMiner standard mode run: 'The identification results will be saved in `metaminer_outdir`. ... you will see identification ... in `metaminer_outdir/significant_matches.tsv`'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] significant_matches.tsv from MetaMiner blind mode run: 'Enable search in a blind mode, i.e. search for new PTMs with arbitrary mass shifts'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence): 'matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] VarQuest match results table (format: tab-separated value file with standardized columns for comparison): 'All the detected RiPPs are reported in plain text tab-separated value files (`.tsv`). Each file starts with a header line containing column descriptions.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences: 'Each file starts with a header line containing column descriptions. The rest lines represent compound–spectrum matches'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] MetaMiner: 'MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] Dereplicator: 'matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] ProteoWizard: 'uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] Python: 'MetaMiner requires a 64-bit Linux system or macOS and Python (versions 2.6-2.7, 3.3 and higher are supported)'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file significant_matches.tsv exists in Dereplicator output directory
- verify file significant_matches.tsv exists in VarQuest output directory
- verify file significant_matches.tsv exists in Dereplicator+ output directory
- file_format_is: each significant_matches.tsv is tab-separated with at least columns for match_id, score, and query_spectrum
- row_count_equals or value_in_range: compare row counts across three pipelines' significant_matches.tsv outputs (no canonical answer — different tools may return different numbers of hits)
- contains_substring: verify each significant_matches.tsv contains at least one row of hit data (not header-only)
- verify input spectra MSV000080102-derived test dataset is accessible and identical across all three pipeline runs
- script_runs: NPDtools 2.5.0 Dereplicator pipeline executes without error on test spectra
- script_runs: NPDtools 2.5.0 VarQuest pipeline executes without error on test spectra
- script_runs: NPDtools 2.5.0 Dereplicator+ pipeline executes without error on test spectra

### Expert Review
- assess whether differences in significant_matches.tsv hit counts across pipelines reflect genuine algorithmic differences or implementation artifacts
- evaluate whether blind mode vs. standard mode differences in hit detection are consistent with documented tool design goals
- judge whether the three pipelines' hit signatures (which compounds are detected under which conditions) are chemically and statistically reasonable given the spectra source material

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Convert MSV000080102 spectra from mzML to MGF format using ProteoWizard msconvert to ensure compatibility across all three pipelines.
2. Index and validate the RiPP sequence database (example_RiPP.fasta) for consistency before parallel pipeline execution.
3. Execute MetaMiner in standard mode (default lantibiotic class) on test spectra and sequences, capturing all significant_matches.tsv records with scan IDs, scores, p-values, and FDRs.
4. Re-execute MetaMiner with --blind flag to enable arbitrary post-translational modification detection and compare output cardinality and score distributions to standard mode.
5. Run Dereplicator and VarQuest pipelines independently on the same spectral and sequence inputs, standardizing output to TSV format with equivalent columns.
6. Merge and deduplicate match records across all three tools by scan identifier, score rank, and peptide sequence identity.
7. Validation: Cross-tool comparison table correctly enumerates per-tool hit counts, identifies scans with tool-specific vs. shared identifications, and confirms that blind-mode MetaMiner results are a superset or equal-cardinality to standard-mode results.
8. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439)

## Workflow Ports

**Inputs:**

- `spectra_files` — Three centroided LC-MS/MS spectra files in mzML format ← `task_003/rippp_candidate_db`
- `ripp_sequences` — Predicted RiPP amino acid sequences in FASTA format
- `spectral_network_data` — Precomputed GNPS spectral network output directory

**Outputs:**

- `metaminer_standard_matches` — MetaMiner significant_matches.tsv from standard mode
- `metaminer_blind_matches` — MetaMiner significant_matches.tsv from blind mode
- `dereplicator_matches` — Dereplicator match results table
- `varquest_matches` — VarQuest match results table
- `comparison_table` — Cross-tool comparison summary of hits and detection patterns

**Used:** `urn:asb:port:task_003/rippp_candidate_db`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:ablab__npdtools`
- **Synthesized at:** 2026-06-16T05:51:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

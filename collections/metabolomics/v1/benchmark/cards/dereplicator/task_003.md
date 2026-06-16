# SciTask Card: Reconstruct the MetaMiner BGC Identifier and RiPP Structure Database Builder pipeline stage

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:40:21.538092+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_dereplicator/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `ablab/npdtools`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `natural-products`, `computational-metabolomics`
- Techniques: `dereplication`, `database-annotation`, `in-silico-fragmentation`

## Research Question
How does MetaMiner's BGC Identifier scan a genome FASTA file to identify putative biosynthetic gene clusters and their corresponding precursor peptides?

## Connected Finding
MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases, before matching spectra against the constructed database.

## Task Description
Scan a genome FASTA file to identify putative biosynthetic gene clusters (BGCs) and their corresponding RiPP precursor peptides, then construct a RiPP structure database for a specified RiPP class by generating all putative post-translationally modified candidate structures. Output per-class intermediate candidate database files before spectral matching.

## Inputs
- Assembled genome sequence file in FASTA format (.fasta, .fna, or .fa extension)

## Expected Outputs
- Per-class RiPP structure database containing enumerated putative post-translationally modified peptide candidates with precursor sequences and modification states, formatted as tab-separated values

## Expected Output File

- `rippp_candidate_database.tsv`

## Landmark Outputs

- `bgc_predictions.txt`
- `precursor_peptides.fasta`
- `class_specific_modifications.txt`

## Tools
- MetaMiner
- NPDtools 2.5.0

## Skills
- bgc-identification-from-genomic-sequence
- precursor-peptide-extraction-from-clusters
- post-translational-modification-enumeration
- rippp-candidate-structure-generation
- class-specific-modification-rule-application
- metabologenomic-database-construction

## Workflow Description
1. Load genome assembly in FASTA format and parse nucleotide sequences. 2. Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide, cyanobactin, or specified class via --class parameter). 3. For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules. 4. Aggregate all generated candidate structures into a per-class RiPP structure database. 5. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream spectral matching by Dereplicator.

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
- No changelog documenting version history or updates to the fixed-architecture BGC Identifier and RiPP Structure Database Builder stages

## Domain Knowledge
- RiPP classes (lantibiotic, lassopeptide, cyanobactin, etc.) each have distinct post-translational modification signatures and biosynthetic gene cluster architectures that drive candidate structure generation.
- BGC identification in MetaMiner scans for clusters containing characteristic biosynthetic genes (e.g., dehydratase, cyclase for lanthipeptides) and extracts the upstream precursor peptide-encoding gene product as the substrate for modification.
- Post-translational modifications alter peptide masses and fragmentation patterns; the structure database must enumerate plausible modification states (e.g., dehydration, cyclization, oxidation) to enable subsequent spectral matching.
- The output database is intermediate—it feeds directly into Dereplicator for tandem mass spectrum matching and must preserve both original and modified sequence information with mass annotations.
- Class parameter (--class) determines which modification rules and BGC gene signatures are applied; default is lantibiotic; 'all' runs all classes sequentially.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: MetaMiner, NPDtools 2.5.0, Per-class RiPP structure database containing enumerated putative post-translationally modified peptide candidates with precursor sequences and modification states, formatted as tab-separated values.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does MetaMiner's BGC Identifier scan a genome FASTA file to identify putative biosynthetic gene clusters and their corresponding precursor peptides?: 'identifies putative BGCs and the corresponding precursor peptides'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases, before matching spectra against the constructed database.: 'Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides (ii) constructs putative RiPP structure databases'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Assembled genome sequence file in FASTA format (.fasta, .fna, or .fa extension): 'raw nucleotide sequences `.fasta` format (a high-quality reference or a draft assembly)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Per-class RiPP structure database containing enumerated putative post-translationally modified peptide candidates with precursor sequences and modification states, formatted as tab-separated values: 'constructs putative RiPP structure databases'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] MetaMiner: 'MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] NPDtools 2.5.0: 'The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools'
- `ev_007` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history or updates to the fixed-architecture BGC Identifier and RiPP Structure Database Builder stages: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that the MetaMiner BGC Identifier stage can be isolated and executed independently on a genome FASTA file (input: test_data/metaminer/fasta/ or equivalent FASTA files from github:ablab__npdtools) without requiring prior spectral data or Dereplicator matching
- verify that intermediate per-class RiPP candidate database files are produced and exist in the output directory after BGC Identifier and RiPP Structure Database Builder stages complete (file_exists check for output files with naming pattern matching RiPP class assignments)
- verify that the fixed-architecture pipeline stages (BGC identification and structure database construction) complete without errors when run on Streptomyces griseus ATCC 12648 test contigs.fasta (script_runs check: MetaMiner BGC/structure stages execute to completion with zero non-zero exit codes)
- verify that candidate database output is produced before any spectral matching occurs (file_format_is check: output files must be in intermediate format prior to Dereplicator matching phase, robust to parameter choices in BGC detection sensitivity)

### Expert Review
- assess whether the intermediate RiPP candidate structure databases are chemically and biosynthetically coherent (i.e., whether predicted post-translational modifications and structure class assignments reflect known RiPP biology)
- evaluate whether BGC boundaries identified by the fixed-architecture stage align with expert expectations for Streptomyces griseus precursor peptides and biosynthetic gene organization

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load assembled genome in FASTA format and initialize MetaMiner BGC scanner for the specified RiPP class.
2. Scan genome sequences to detect putative biosynthetic gene clusters via signature gene detection and extract corresponding precursor peptide sequences.
3. Apply class-specific post-translational modification rules (e.g., dehydration, cyclization, oxidation) to enumerate plausible candidate structures for each precursor.
4. Aggregate all generated candidate structures with original and modified sequences, masses, and metadata into a structured per-class RiPP database.
5. Validation: confirm that the output database file exists, contains the expected RiPP class identifier in the header, lists all identified precursor peptides with their enumerated modified forms, and includes required fields (original sequence, modified sequence, mass) for each candidate ready for spectral matching.
6. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439)

## Workflow Ports

**Inputs:**

- `genome_fasta` — Assembled genome sequence file in FASTA format

**Outputs:**

- `rippp_candidate_db` — Per-class RiPP structure database with enumerated post-translationally modified candidates

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:ablab__npdtools`
- **Synthesized at:** 2026-06-16T05:51:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

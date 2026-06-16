# SciTask Card: Reproduce AmfS lantibiotic identification via MetaMiner on S. griseus FASTA input

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:40:21.538092+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_dereplicator/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `information-extraction`, `benchmark-evaluation`
- GitHub: `ablab/npdtools`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `natural-products`, `computational-metabolomics`
- Techniques: `dereplication`, `database-annotation`, `in-silico-fragmentation`

## Research Question
Does MetaMiner successfully identify the AmfS lantibiotic (core peptide TGSQVSLLVCEYSSLSVVLCTP) when run on S. griseus genomic data with MSV000080102 spectral data in lantibiotic class search mode?

## Connected Finding
MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.

## Task Description
Run MetaMiner on S. griseus_fragment.fasta genome with MSV000080102 spectral data under lantibiotic class search to identify RiPP compounds, and verify that AmfS (core peptide TGSQVSLLVCEYSSLSVVLCTP with modifications T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP) is reported in significant_matches.tsv.

## Inputs
- S.griseus_fragment.fasta reference genome sequence file
- LC-MS/MS spectral data from MSV000080102 in centroided MGF, mzXML, mzML, or mzData format

## Expected Outputs
- significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq
- Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP

## Expected Output File

- `significant_matches.tsv`

## Landmark Outputs

- `metaminer_outdir/significant_matches.tsv`
- `metaminer_outdir/all_matches.tsv`

## Tools
- NPDtools 2.5.0
- MetaMiner
- Dereplicator
- ProteoWizard
- NPDtools
- joblib

## Skills
- ribosomally-synthesized-peptide-identification
- mass-spectrometry-database-matching
- post-translational-modification-detection
- genome-sequence-mining
- lantibiotic-structure-annotation
- spectral-library-matching-ripp

## Workflow Description
1. Download and extract NPDtools 2.5.0 binaries for the target platform (Linux or macOS), ensuring Python 2.6–3.3+ and joblib are available for parallel processing. 2. Prepare input files: obtain S.griseus_fragment.fasta from test_data/metaminer/fasta/ and download MSV000080102 spectral files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, BB3_01_25959.mzML, BB4_01_25960.mzML) or use centroided spectra in MGF format. 3. Run MetaMiner via 'python metaminer.py <spectra_directory_or_files> -s <path_to_S.griseus_fragment.fasta> -c lantibiotic -o <output_directory>', using default parameters (lantibiotic RiPP class, standard scoring). 4. Parse the tab-separated significant_matches.tsv output file to extract compound identifications, verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications (T-18 and S-18 mass shifts).

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
- No changelog documenting what versions or features are bundled in this NPDtools distribution

## Domain Knowledge
- RiPPs (Ribosomally synthesized and Post-translationally modified Peptides) are secondary metabolites synthesized from ribosomal precursor peptides that undergo enzymatic modification (e.g., dehydration, cyclization, glycosylation) to produce bioactive compounds like lantibiotics, lassopeptides, and cyanobactins.
- Lantibiotics are RiPPs characterized by thioether-cross-linked amino acids (lanthipeptides) and dehydrated residues (dehydroalanine, dehydrobutyrine), which appear in mass spectra as mass shifts of −18 Da per modification.
- AmfS (from Streptomyces griseus) is a model lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP that undergoes dehydration at T and S residues, producing the fully modified form T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP; this compound serves as a reference standard for validating RiPP detection pipelines.
- MetaMiner's four-stage workflow (BGC identification → RiPP database construction → spectral matching via Dereplicator → spectral network propagation) integrates genomic context with untargeted mass spectrometry to prioritize true RiPP identifications over false positives from chemical databases.
- Centroided (profile-mode processed) tandem mass spectra in open formats (MGF, mzXML, mzML, mzData) are required inputs; antiSMASH .gbk output may lose gene context information critical for precursor peptide extraction, explaining AmfS detection failure observed with antiSMASH input versus raw .fasta.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: MetaMiner, ProteoWizard, NPDtools, joblib, significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq, Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does MetaMiner successfully identify the AmfS lantibiotic (core peptide TGSQVSLLVCEYSSLSVVLCTP) when run on S. griseus genomic data with MSV000080102 spectral data in lantibiotic class search mode?: 'NPDtools – Natural Product Discovery tools – is a toolkit containing various pipelines for _in silico_ analysis of natural product mass spectrometry data'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.: 'While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] S.griseus_fragment.fasta reference genome sequence file: 'a search of `test_data/metaminer/msms/AmfS.mgf` spectrum against `test_data/metaminer/fasta/S.griseus_fragment.fasta` genome fragment'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] LC-MS/MS spectral data from MSV000080102 in centroided MGF, mzXML, mzML, or mzData format: 'For metabolomic data, MetaMiner works with liquid chromatography–tandem mass spectrometry data (LS-MS/MS). Spectra files must be centroided and in an open spectrum format (MGF, mzXML, mzML or mzData)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq: 'All the detected RiPPs are reported in plain text tab-separated value files (`.tsv`). Each file starts with a header line containing column descriptions'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP: 'you will see identification of a lantibiotic with "TGSQVSLLVCEYSSLSVVLCTP" original sequence and "T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP" sequence after modifications in'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] MetaMiner: 'MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Dereplicator: 'matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] ProteoWizard: 'MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] NPDtools: 'The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] joblib: 'For parallel processing of multiple spectra or/and sequence files, MetaMiner requires `joblib` Python library'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting what versions or features are bundled in this NPDtools distribution: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file S.griseus_fragment.fasta exists in package
- verify file significant_matches.tsv exists in MetaMiner output directory after execution
- verify significant_matches.tsv contains substring 'AmfS'
- verify significant_matches.tsv contains substring 'TGSQVSLLVCEYSSLSVVLCTP' (AmfS core peptide)
- script_runs: MetaMiner command executes without fatal errors on bundled inputs with lantibiotic class search mode
- verify output file format_is TSV (tab-separated values) with header row present

### Expert Review
- AmfS entry in significant_matches.tsv has statistically significant score threshold appropriate for lantibiotic RiPP detection
- reported AmfS match quality and e-value are consistent with true positive RiPP identification

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load centroided LC-MS/MS spectral data (MSV000080102) from open formats and convert to MGF via ProteoWizard if needed.
2. Scan S.griseus_fragment.fasta genome to identify putative biosynthetic gene clusters and extract ribosomal precursor peptide sequences.
3. Construct in silico RiPP structure database by enumerating post-translationally modified variants (dehydroalanine, dehydrobutyrine, lanthipeptide cross-links) from precursor peptides.
4. Match all tandem mass spectra against the RiPP database using Dereplicator, computing similarity scores and P-values for each compound–spectrum pair under lantibiotic class constraints.
5. Filter matches by FDR threshold and output identified RiPPs with original and modified sequences, retention time, charge, and genomic source in significant_matches.tsv.
6. Validation: verify that AmfS is present in significant_matches.tsv with FragmentSeq exactly matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq containing dehydration modifications (T-18 and S-18 mass shifts), confirming detection sensitivity at default parameters.
7. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439)

## Workflow Ports

**Inputs:**

- `genome_fasta` — S. griseus_fragment.fasta reference genome
- `spectra_files` — LC-MS/MS spectral data (MSV000080102)

**Outputs:**

- `ripp_matches` — RiPP identifications in significant_matches.tsv
- `amfs_verification` — Confirmation of AmfS detection with FragmentSeq and ModifiedSeq

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:ablab__npdtools`
- **Synthesized at:** 2026-06-16T05:51:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

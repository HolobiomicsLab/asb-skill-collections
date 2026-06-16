# SciTask Card: Reconstruct spectral networking output generation via MetaMiner Spectral Networking component

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:40:21.538092+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_dereplicator/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `visualization`, `information-extraction`
- GitHub: `ablab/npdtools`
- Input from: `task_003`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`
- Subdomains: `natural-products`, `computational-metabolomics`
- Techniques: `dereplication`, `database-annotation`, `in-silico-fragmentation`

## Research Question
What output files does the Spectral Networking stage of the MetaMiner pipeline produce when run on test mass spectrometry data?

## Connected Finding
The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs.

## Task Description
Run the spectral networking stage of MetaMiner on MSV000080102 test spectra paired with an example RiPP sequence to generate and verify the spec_nets output folder containing propagations.pdf, propagations_detailed.txt, and propagations_short.txt files.

## Inputs
- Three mzML spectra files from MSV000080102 dataset (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) or downloaded precomputed spectral network output from GNPS
- Example RiPP FASTA file containing sequence DATITTVTVTSTSIWASTVSNHC (test_data/metaminer/molnet/example_RiPP.fasta)
- Unpacked GNPS spectral network output directory (ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked) containing clustered spectra and network files

## Expected Outputs
- propagations.pdf – graphical report with each page corresponding to a connected component of a significant PSM
- propagations_detailed.txt – detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM
- propagations_short.txt – same as detailed report but listing only one representative per each cluster

## Expected Output File

- `propagations.pdf`

## Landmark Outputs

- `metaminer_outdir/spec_nets/propagations.pdf`
- `metaminer_outdir/spec_nets/propagations_detailed.txt`
- `metaminer_outdir/spec_nets/propagations_short.txt`

## Tools
- MetaMiner
- NPDtools 2.5.0
- GNPS Spectral Networking / Molecular Networking
- matplotlib
- networkx

## Skills
- spectral-network-propagation-analysis
- mass-spectrometry-metadata-interpretation
- rippp-structure-database-matching
- gnps-workflow-result-processing
- spectral-cluster-connectivity-assessment

## Workflow Description
1. Download the three mzML spectra files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) from MSV000080102 or retrieve the precomputed spectral network output files from GNPS and unpack the ProteoSAFe-METABOLOMICS-SNETS-V2 archive. 2. Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory, the example RiPP FASTA file (DATITTVTVTSTSIWASTVSNHC), and the --blind flag for demonstration purposes: python metaminer.py <spectra_files> -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir. 3. Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2), and propagations_short.txt (same as detailed but with one representative per cluster).

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
- The exact filenames and descriptions of the two required output files (in addition to propagations.pdf) produced by the Spectral Networking stage are not specified in the provided discussion section

## Domain Knowledge
- RiPPs (Ribosomally synthesized and Post-translationally modified Peptides) are natural product compounds encoded by biosynthetic gene clusters that undergo post-translational modifications affecting their mass spectrometry signatures.
- GNPS Molecular Networking clusters related mass spectra into connected components based on cosine similarity, allowing propagation of identifications across spectral families with related structures.
- A 'significant PSM' (Peptide-Spectrum Match) in the context of spectral networking requires both high-confidence matching and cluster-level propagation evidence to warrant reporting in the graphical output.
- The --blind flag enables search for arbitrary mass shifts representing novel post-translational modifications not in the predefined RiPP modification database, substantially increasing computational cost.
- Distance 1 and 2 clustering metrics in spectral networks indicate direct neighbors and second-order connections in the similarity graph, used to distinguish high-confidence propagations from distant spurious matches.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: MetaMiner, NPDtools 2.5.0, matplotlib, networkx, propagations.pdf – graphical report with each page corresponding to a connected component of a significant PSM, propagations_detailed.txt – detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM, propagations_short.txt – same as detailed report but listing only one representative per each cluster.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What output files does the Spectral Networking stage of the MetaMiner pipeline produce when run on test mass spectrometry data?: 'NPDtools – Natural Product Discovery tools – is a toolkit containing various pipelines for _in silico_ analysis of natural product mass spectrometry data'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs.: 'After identifying some RiPPs, users can further enlarge the set of RiPP identifications via spectral network and visualize the results'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Three mzML spectra files from MSV000080102 dataset (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) or downloaded precomputed spectral network output from GNPS: 'Download `C18p_5uL_NASA_Sample_BB2_01_25958.mzML`, `C18p_5uL_NASA_Sample_BB3_01_25959.mzML` and `C18p_5uL_NASA_Sample_BB4_01_25960.mzML` files from [MSV000080102] or download their precomputed'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Example RiPP FASTA file containing sequence DATITTVTVTSTSIWASTVSNHC (test_data/metaminer/molnet/example_RiPP.fasta): 'and an example RiPP `DATITTVTVTSTSIWASTVSNHC` (available in `test_data/metaminer/molnet/example_RiPP.fasta`)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Unpacked GNPS spectral network output directory (ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked) containing clustered spectra and network files: 'use the minimal subset of this spectral network output files available in `test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked/`. If using an archive downloaded from GNPS, please'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] propagations.pdf – graphical report with each page corresponding to a connected component of a significant PSM: '`propagations.pdf` (graphical report, each page corresponds to a connected component of a significant PSM)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] propagations_detailed.txt – detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM: '`propagations_detailed.txt`  (detailed text report: for each significant PSM, lists all spectra from the same cluster and from clusters at distance 1 and 2)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] propagations_short.txt – same as detailed report but listing only one representative per each cluster: '`propagations_short.txt` (the same as above but lists only one representative per each cluster)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] MetaMiner: 'MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] NPDtools 2.5.0: 'The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] GNPS Spectral Networking / Molecular Networking: 'Spectral network can be easily run through GNPS. Detailed instructions can be found in the [GNPS documentation]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] matplotlib: 'For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib` and `networkx` Python libraries'
- `ev_013` from `agent2_synthesis` (agent2_traced): [other] networkx: 'For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib` and `networkx` Python libraries'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] The exact filenames and descriptions of the two required output files (in addition to propagations.pdf) produced by the Spectral Networking stage are not specified in the provided discussion section: 'No information provided about spec_nets output file requirements beyond the GitHub repository reference'

## Evaluation Strategy
### Direct Checks
- verify file_exists: spec_nets/propagations.pdf in output directory
- verify file_exists: spec_nets output folder is created
- verify file_format_is: propagations.pdf is a valid PDF file (byte-for-byte magic number check)
- verify row_count_equals or field_present: two additional named output files are present in spec_nets folder with names matching manual documentation

### Expert Review
- inspect propagations.pdf visually to confirm spectral network visualization content is sensible and non-empty
- confirm the two additional named output files match the exact filenames and purposes documented in the NPDtools 2.5.0 manual for Spectral Networking stage

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load and prepare spectral data: obtain or download the three mzML spectra files from MSV000080102 and the precomputed GNPS spectral network output (or compute spectral networks de novo via GNPS).
2. Configure spectral networking input: unpack the GNPS ProteoSAFe output archive and prepare the example RiPP FASTA file containing the target sequence DATITTVTVTSTSIWASTVSNHC.
3. Execute MetaMiner with spectral networking: run the pipeline with the --spec-network flag pointing to the network directory, enabling blind mode for demonstration of novel PTM detection.
4. Generate propagation reports: MetaMiner identifies connected components in the spectral network related to significant RiPP identifications and generates graphical (PDF) and text (detailed and condensed) outputs.
5. Validation: verify that all three required output files (propagations.pdf, propagations_detailed.txt, propagations_short.txt) are present in metaminer_outdir/spec_nets/ directory and contain non-empty content.
6. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439)

## Workflow Ports

**Inputs:**

- `spectra_files` — mzML spectral data files from MSV000080102 ← `task_003/rippp_candidate_db`
- `rippp_fasta` — Example RiPP FASTA sequence file
- `spectral_network_dir` — Unpacked GNPS spectral network output directory

**Outputs:**

- `propagations_pdf` — Graphical spectral network propagation report
- `propagations_detailed_txt` — Detailed text report of spectral propagations
- `propagations_short_txt` — Condensed text report of spectral propagations

**Used:** `urn:asb:port:task_003/rippp_candidate_db`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:ablab__npdtools`
- **Synthesized at:** 2026-06-16T05:51:28+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

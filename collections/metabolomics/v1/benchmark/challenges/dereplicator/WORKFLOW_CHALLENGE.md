# Workflow Challenge: `coll_dereplicator_workflow`


> MetaMiner is a metabologenomic pipeline that integrates tandem mass spectrometry and genomic data to identify ribosmally synthesized and post-translationally modified peptides (RiPPs) and their biosynthetic gene clusters. The pipeline demonstrates input format-dependent detection performance, successfully identifying lantibiotics from raw nucleotide sequences but failing with antiSMASH-processed genome annotations.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MetaMiner, distributed as part of NPDtools version 2.5.0, operates through a multi-stage workflow that identifies putative biosynthetic gene clusters and corresponding precursor peptides from genome assemblies, constructs putative RiPP structure databases, and matches tandem mass spectra against the constructed post-translationally modified RiPP database using Dereplicator before enlarging the set of identified RiPPs via spectral networking. The paper documents successful detection of the lantibiotic AmfS when MetaMiner is run on raw nucleotide sequence files (contigs.fasta format), but reports that detection fails when antiSMASH-annotated genome output (.final.gbk) is used as input, indicating that input format choice affects detection performance. NPDtools 2.5.0 integrates multiple database search pipelines (Dereplicator, VarQuest, and Dereplicator+) for natural product mass spectrometry analysis and provides mechanisms to visualize spectral network results and propagation graphs after RiPP identification.

## Research questions

- Does MetaMiner successfully identify the AmfS lantibiotic (core peptide TGSQVSLLVCEYSSLSVVLCTP) when run on S. griseus genomic data with MSV000080102 spectral data in lantibiotic class search mode?
- Does MetaMiner fail to detect the AmfS RiPP when using antiSMASH .gbk output instead of FASTA sequences for the S. griseus dataset?
- How does MetaMiner's BGC Identifier scan a genome FASTA file to identify putative biosynthetic gene clusters and their corresponding precursor peptides?
- What output files does the Spectral Networking stage of the MetaMiner pipeline produce when run on test mass spectrometry data?
- Which of the three NPDtools database search pipelines (Dereplicator, VarQuest, Dereplicator+) successfully identify matches in MSV000080102-derived test spectra, and how do their hit patterns differ across search modes?

## Methods overview

Load centroided LC-MS/MS spectral data (MSV000080102) from open formats and convert to MGF via ProteoWizard if needed. Scan S.griseus_fragment.fasta genome to identify putative biosynthetic gene clusters and extract ribosomal precursor peptide sequences. Construct in silico RiPP structure database by enumerating post-translationally modified variants (dehydroalanine, dehydrobutyrine, lanthipeptide cross-links) from precursor peptides. Match all tandem mass spectra against the RiPP database using Dereplicator, computing similarity scores and P-values for each compound–spectrum pair under lantibiotic class constraints. Filter matches by FDR threshold and output identified RiPPs with original and modified sequences, retention time, charge, and genomic source in significant_matches.tsv. Validation: verify that AmfS is present in significant_matches.tsv with FragmentSeq exactly matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq containing dehydration modifications (T-18 and S-18 mass shifts), confirming detection sensitivity at default parameters. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439) Download or locate S. griseus test data: LC-MS/MS spectra (AmfS.mgf) and antiSMASH-generated .final.gbk annotation. Execute MetaMiner with antiSMASH input: invoke metaminer.py pointing to spectra directory and antiSMASH .gbk sequence file using default lantibiotic search class. Harvest and inspect significant_matches.tsv output for presence or absence of AmfS peptide in FragmentSeq and ModifiedSeq columns. Validation: Confirm that AmfS peptide (raw sequence TGSQVSLLVCEYSSLSVVLCTP or modified TGSQVSLLVCEYSSLSVVLCTP-with-dehydration marks) does NOT appear in significant_matches.tsv, reproducing the documented antiSMASH input failure mode. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439) Load assembled genome in FASTA format and initialize MetaMiner BGC scanner for the specified RiPP class. Scan genome sequences to detect putative biosynthetic gene clusters via signature gene detection and extract corresponding precursor peptide sequences. Apply class-specific post-translational modification rules (e.g., dehydration, cyclization, oxidation) to enumerate plausible candidate structures for each precursor. Aggregate all generated candidate structures with original and modified sequences, masses, and metadata into a structured per-class RiPP database. Validation: confirm that the output database file exists, contains the expected RiPP class identifier in the header, lists all identified precursor peptides with their enumerated modified forms, and includes required fields (original sequence, modified sequence, mass) for each candidate ready for spectral matching. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439) Load and prepare spectral data: obtain or download the three mzML spectra files from MSV000080102 and the precomputed GNPS spectral network output (or compute spectral networks de novo via GNPS). Configure spectral networking input: unpack the GNPS ProteoSAFe output archive and prepare the example RiPP FASTA file containing the target sequence DATITTVTVTSTSIWASTVSNHC. Execute MetaMiner with spectral networking: run the pipeline with the --spec-network flag pointing to the network directory, enabling blind mode for demonstration of novel PTM detection. Generate propagation reports: MetaMiner identifies connected components in the spectral network related to significant RiPP identifications and generates graphical (PDF) and text (detailed and condensed) outputs. Validation: verify that all three required output files (propagations.pdf, propagations_detailed.txt, propagations_short.txt) are present in metaminer_outdir/spec_nets/ directory and contain non-empty content. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439) Convert MSV000080102 spectra from mzML to MGF format using ProteoWizard msconvert to ensure compatibility across all three pipelines. Index and validate the RiPP sequence database (example_RiPP.fasta) for consistency before parallel pipeline execution. Execute MetaMiner in standard mode (default lantibiotic class) on test spectra and sequences, capturing all significant_matches.tsv records with scan IDs, scores, p-values, and FDRs. Re-execute MetaMiner with --blind flag to enable arbitrary post-translational modification detection and compare output cardinality and score distributions to standard mode. Run Dereplicator and VarQuest pipelines independently on the same spectral and sequence inputs, standardizing output to TSV format with equivalent columns. Merge and deduplicate match records across all three tools by scan identifier, score rank, and peptide sequence identity. Validation: Cross-tool comparison table correctly enumerates per-tool hit counts, identifies scans with tool-specific vs. shared identifications, and confirms that blind-mode MetaMiner results are a superset or equal-cardinality to standard-mode results. References: MSV000080102 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000080102); SRR3309439 (https://www.ncbi.nlm.nih.gov/sra/?term=SRR3309439)

**Domain:** bioinformatics

**Techniques:** dereplication, database-annotation, in-silico-fragmentation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** NPDtools version 2.5.0 was released under the Apache 2.0 License on November 28, 2019. _[grounded: SYS_NPDTOOLS]_
- **(finding)** MetaMiner is a metabologenomic pipeline which integrates metabolomic and genomic data to identify RiPPs and biosynthetic gene clusters encoding them. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner is developed in collaboration of Carnegie Mellon University, Saint Petersburg State University, and University of California San Diego. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner works with liquid chromatography–tandem mass spectrometry data (LS-MS/MS) for metabolomic data. _[grounded: SYS_METAMINER]_
- **(finding)** Spectra files must be centroided and in an open spectrum format (MGF, mzXML, mzML or mzData).
- **(finding)** MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner accepts raw nucleotide sequences in .fasta format as genomic input. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner accepts antiSMASH's .final.gbk or .gbk file as genomic input. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner accepts BOA's .annotated.txt file as genomic input. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner accepts predicted and translated RiPP amino acid sequences in .fasta format as genomic input. _[grounded: SYS_METAMINER]_
- **(finding)** Users can assemble DNA short reads with SPAdes or metaSPAdes before running MetaMiner. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner reports all detected RiPPs in plain text tab-separated value files (.tsv). _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include SpecFile column containing filepath of the spectra file. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include Scan column containing scan number of the identified spectrum. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include SpectrumMass column containing mass of the spectrum in Daltons. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include Retention column containing retention time of the spectrum in seconds. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include Charge column containing charge of the spectrum. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include Score column containing score of the compound–spectrum match. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include P-Value column indicating statistical significance of the compound–spectrum match. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include FDR column containing estimated False Discovery Rate. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include PeptideMass column containing mass of the compound in Daltons. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include SeqFile column containing filepath of the genome sequence file. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include Class column indicating class of the identified RiPP compound. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include FragmentSeq column containing raw initial sequence of the identified compound. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner output files include ModifiedSeq column containing sequence of the identified compound with all applied modifications. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner identifies putative BGCs and corresponding precursor peptides as a first pipeline step. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner constructs putative RiPP structure databases as a second pipeline step. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator as a third pipeline step. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner enlarges the set of described RiPPs via spectral networking as a fourth pipeline step. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner requires a 64-bit Linux system or macOS and Python versions 2.6-2.7, 3.3 and higher. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner requires joblib Python library for parallel processing of multiple spectra or sequence files. _[grounded: SYS_METAMINER]_
- **(finding)** Without joblib installed, MetaMiner processes everything in a single thread. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner requires matplotlib and networkx Python libraries for presenting Spectral Network propagation graphs. _[grounded: SYS_METAMINER]_
- **(finding)** Without matplotlib and networkx, MetaMiner generates propagation in plain text format only. _[grounded: SYS_METAMINER]_
- **(finding)** There is no need for compilation of MetaMiner sources and users can directly download and run the binaries. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner is an integral part of the NPDtools package. _[grounded: SYS_NPDTOOLS]_
- **(finding)** The MetaMiner test data is located in share/npdtools/test_data/ directory. _[grounded: SYS_NPDTOOLS]_
- **(finding)** SPAdes version 3.13.0 is available for download to assemble DNA short reads. _[grounded: TOOL_SPADES]_
- **(finding)** antiSMASH 4 can be installed using conda with Python 2.7. _[grounded: TOOL_ANTISMASH]_
- **(finding)** BOA environment is created in conda with Python 2.7.
- **(finding)** MetaMiner default search mode considers RiPP class as 'lantibiotic'. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner identified a lantibiotic with original sequence TGSQVSLLVCEYSSLSVVLCTP in test data. _[grounded: SYS_METAMINER]_
- **(finding)** The test sequence after modifications shows as T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP in MetaMiner output. _[grounded: SYS_METAMINER]_
- **(finding)** The modifications T-18 and S-18 correspond to dehydrobutyrine and dehydroalanine respectively.
- **(finding)** The test sequences correspond to AmfS peptide. _[grounded: COMP_AMFS]_
- **(finding)** MetaMiner accepts nucleotide or amino acid FASTA files with extensions .fna, .fasta, or .fa. _[grounded: SYS_METAMINER]_
- **(finding)** At least one sequence file is required for MetaMiner unless correspondence file with RefSeq IDs is specified. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner correspondence file should be tab-separated with two columns listing basenames of spectra and sequence files. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner correspondence file may include RefSeq IDs prefixed with #RefSeq: which are automatically downloaded from NCBI. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner performs all-vs-all analysis if correspondence file is not provided. _[grounded: SYS_METAMINER]_
- **(finding)** Valid RiPP classes for MetaMiner include formylated, glycocin, lantibiotic, lap, lassopeptide, linaridin, proteusin, cyanobactin, and methanobactin. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner can specify 'all' to try all RiPP classes one by one. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner --blind option enables search in blind mode for new PTMs with arbitrary mass shifts. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner --spec-network option accepts path to Spectral Network output from GNPS Data Analysis workflow. _[grounded: SYS_METAMINER]_
- **(finding)** MetaMiner with --spec-network option saves results under <outdir>/spec_nets/. _[grounded: SYS_METAMINER]_
- **(finding)** Users should cite Cao et al, Cell Systems, 2019 when using MetaMiner. _[grounded: SYS_METAMINER]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- contigs.fasta or scaffolds.fasta from SPAdes can be used interchangeably as MetaMiner input
- metaSPAdes as alternative to SPAdes for assembly

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Requires 64-bit Linux system or macOS
- Without joblib library, processing occurs in single thread only
- Without matplotlib and networkx, spectral network propagation is in plain text format only

## Steps

### Step `task_001`
- Title: Reproduce AmfS lantibiotic identification via MetaMiner on S. griseus FASTA input
- Task kind: `reproduction`
- Task: Run MetaMiner on S. griseus_fragment.fasta genome with MSV000080102 spectral data under lantibiotic class search to identify RiPP compounds, and verify that AmfS (core peptide TGSQVSLLVCEYSSLSVVLCTP with modifications T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP) is reported in significant_matches.tsv.
- Inputs:
  - S.griseus_fragment.fasta reference genome sequence file
  - LC-MS/MS spectral data from MSV000080102 in centroided MGF, mzXML, mzML, or mzData format
- Expected outputs:
  - significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq
  - Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP
- Tools: NPDtools 2.5.0, MetaMiner, Dereplicator, ProteoWizard, NPDtools, joblib
- Landmark output files: metaminer_outdir/significant_matches.tsv, metaminer_outdir/all_matches.tsv
- Primary expected artifact: `significant_matches.tsv`

### Step `task_002`
- Title: Reproduce antiSMASH input failure for MetaMiner AmfS detection
- Task kind: `reproduction`
- Task: Run MetaMiner on S. griseus LC-MS/MS spectra using antiSMASH .gbk output instead of raw FASTA to reproduce the documented failure mode where AmfS peptide is not detected.
- Inputs:
  - LC-MS/MS spectra in MGF format (AmfS.mgf) from S. griseus test dataset
  - Antibiotic Biosynthetic Gene Cluster GenBank file (.final.gbk) generated from S. griseus contigs by antiSMASH
- Expected outputs:
  - Tab-separated value file (significant_matches.tsv) containing compound–spectrum matches with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq
  - Absence of AmfS peptide (TGSQVSLLVCEYSSLSVVLCTP) in significant_matches.tsv output, confirming the antiSMASH input failure mode
- Tools: NPDtools 2.5.0, MetaMiner, antiSMASH, Dereplicator
- Landmark output files: metaminer_outdir/significant_matches.tsv, metaminer_outdir/all_matches.tsv
- Primary expected artifact: `significant_matches.tsv`

### Step `task_003`
- Title: Reconstruct the MetaMiner BGC Identifier and RiPP Structure Database Builder pipeline stage
- Task kind: `component_reconstruction`
- Task: Scan a genome FASTA file to identify putative biosynthetic gene clusters (BGCs) and their corresponding RiPP precursor peptides, then construct a RiPP structure database for a specified RiPP class by generating all putative post-translationally modified candidate structures. Output per-class intermediate candidate database files before spectral matching.
- Inputs:
  - Assembled genome sequence file in FASTA format (.fasta, .fna, or .fa extension)
- Expected outputs:
  - Per-class RiPP structure database containing enumerated putative post-translationally modified peptide candidates with precursor sequences and modification states, formatted as tab-separated values
- Tools: MetaMiner, NPDtools 2.5.0
- Landmark output files: bgc_predictions.txt, precursor_peptides.fasta, class_specific_modifications.txt
- Primary expected artifact: `rippp_candidate_database.tsv`

### Step `task_004`
- Depends on: `task_003`
- Title: Reconstruct spectral networking output generation via MetaMiner Spectral Networking component
- Task kind: `component_reconstruction`
- Task: Run the spectral networking stage of MetaMiner on MSV000080102 test spectra paired with an example RiPP sequence to generate and verify the spec_nets output folder containing propagations.pdf, propagations_detailed.txt, and propagations_short.txt files.
- Inputs:
  - Three mzML spectra files from MSV000080102 dataset (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) or downloaded precomputed spectral network output from GNPS
  - Example RiPP FASTA file containing sequence DATITTVTVTSTSIWASTVSNHC (test_data/metaminer/molnet/example_RiPP.fasta)
  - Unpacked GNPS spectral network output directory (ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked) containing clustered spectra and network files
- Expected outputs:
  - propagations.pdf – graphical report with each page corresponding to a connected component of a significant PSM
  - propagations_detailed.txt – detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM
  - propagations_short.txt – same as detailed report but listing only one representative per each cluster
- Tools: MetaMiner, NPDtools 2.5.0, GNPS Spectral Networking / Molecular Networking, matplotlib, networkx
- Landmark output files: metaminer_outdir/spec_nets/propagations.pdf, metaminer_outdir/spec_nets/propagations_detailed.txt, metaminer_outdir/spec_nets/propagations_short.txt
- Primary expected artifact: `propagations.pdf`

### Step `task_005`
- Depends on: `task_003`
- Title: Analyze database search pipeline tool dispatch across Dereplicator, VarQuest, and Dereplicator+ on test spectra
- Task kind: `analysis`
- Task: Run MetaMiner, Dereplicator, and VarQuest pipelines independently on MSV000080102-derived test spectra with the same RiPP sequences; compare significant_matches.tsv outputs to characterize tool-specific hit patterns across standard and blind search modes.
- Inputs:
  - Three LC-MS/MS spectra files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) from MSV000080102 dataset
  - Example RiPP sequence file (example_RiPP.fasta) containing predicted amino acid sequences
  - Precomputed spectral network output files from GNPS (MSV000080102 clustered spectra data)
- Expected outputs:
  - significant_matches.tsv from MetaMiner standard mode run
  - significant_matches.tsv from MetaMiner blind mode run
  - Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence)
  - VarQuest match results table (format: tab-separated value file with standardized columns for comparison)
  - Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences
- Tools: NPDtools 2.5.0, MetaMiner, Dereplicator, ProteoWizard, Python
- Landmark output files: metaminer_standard_mode/significant_matches.tsv, metaminer_blind_mode/significant_matches.tsv, dereplicator_output/matches.tsv, varquest_output/matches.tsv
- Primary expected artifact: `tool_comparison_summary.tsv`

## Final expected outputs

- `significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq` (type: file, tolerance: hash)
- `Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP` (type: file, tolerance: hash)
- `Tab-separated value file (significant_matches.tsv) containing compound–spectrum matches with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq` (type: file, tolerance: hash)
- `Absence of AmfS peptide (TGSQVSLLVCEYSSLSVVLCTP) in significant_matches.tsv output, confirming the antiSMASH input failure mode` (type: file, tolerance: hash)
- `propagations.pdf – graphical report with each page corresponding to a connected component of a significant PSM` (type: file, tolerance: hash)
- `propagations_detailed.txt – detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM` (type: file, tolerance: hash)
- `propagations_short.txt – same as detailed report but listing only one representative per each cluster` (type: file, tolerance: hash)
- `significant_matches.tsv from MetaMiner standard mode run` (type: file, tolerance: hash)
- `significant_matches.tsv from MetaMiner blind mode run` (type: file, tolerance: hash)
- `Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence)` (type: file, tolerance: hash)
- `VarQuest match results table (format: tab-separated value file with standardized columns for comparison)` (type: file, tolerance: hash)
- `Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

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
  "workflow_id": "coll_dereplicator_workflow",
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
    "significant_matches.tsv tab-separated report with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq": "<locator>",
    "Verified identification of AmfS lantibiotic with core sequence TGSQVSLLVCEYSSLSVVLCTP and modified sequence T-18GS-18QVS-18LLVCEYS-18SLSVVLCTP": "<locator>",
    "Tab-separated value file (significant_matches.tsv) containing compound\u2013spectrum matches with columns: SpecFile, Scan, SpectrumMass, Retention, Charge, Score, P-Value, FDR, PeptideMass, SeqFile, Class, FragmentSeq, ModifiedSeq": "<locator>",
    "Absence of AmfS peptide (TGSQVSLLVCEYSSLSVVLCTP) in significant_matches.tsv output, confirming the antiSMASH input failure mode": "<locator>",
    "propagations.pdf \u2013 graphical report with each page corresponding to a connected component of a significant PSM": "<locator>",
    "propagations_detailed.txt \u2013 detailed text report listing all spectra from same cluster and clusters at distance 1 and 2 for each significant PSM": "<locator>",
    "propagations_short.txt \u2013 same as detailed report but listing only one representative per each cluster": "<locator>",
    "significant_matches.tsv from MetaMiner standard mode run": "<locator>",
    "significant_matches.tsv from MetaMiner blind mode run": "<locator>",
    "Dereplicator match results table (format: tab-separated value file with columns for scan, spectrum mass, score, p-value, FDR, peptide mass, and sequence)": "<locator>",
    "VarQuest match results table (format: tab-separated value file with standardized columns for comparison)": "<locator>",
    "Cross-tool comparison table summarizing hits per tool, detection concordance, and mode-dependent sensitivity differences": "<locator>"
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

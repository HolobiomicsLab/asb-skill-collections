# SciTask Card: Reconstruct the MS2 Library Compilation Pipeline (read MGF/MSP → complete → assign SMILES → separate polarity → write MSP)

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:31:46.023986+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mspcompiler/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `data-analysis`
- GitHub: `QizhiSu/mspcompiler`
- Input from: `task_001`
- Quality: Score 3/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `database-annotation`, `gc-ms`, `spectral-library-matching`, `tandem-ms`

## Research Question
What is the sequence of operations in the MS2 library compilation pipeline for loading, completing metadata, assigning chemical structures, separating by ionization polarity, and writing polarity-specific MSP files?

## Connected Finding
The mspcompiler system processes MS2 libraries through a sequence of steps: loading libraries from NIST, MoNA, GNPS, or RIKEN sources via read_lib; completing MGF metadata through complete_mgf; assigning SMILES structures via assign_smiles; separating positive and negative ionization modes via separate_polarity; and writing polarity-separated MSP files via write_MS2_msp for use in MS-DIAL.

## Task Description
Load NIST, RIKEN, MoNA, and GNPS MS2 libraries; complete MGF metadata, assign SMILES, separate positive and negative modes, and write polarity-split MSP files suitable for MS-DIAL.

## Inputs
- NIST MS2 library MSP file (NIST_msms.MSP)
- NIST MS2 MOL directory containing structure files (NIST_msms.MOL)
- RIKEN MS2 positive mode library (MSMS-Public-Pos-VS15.msp)
- RIKEN MS2 negative mode library (MSMS-Public-Neg-VS15.msp)
- MoNA MS2 positive mode library (MoNA-export-LC-MS-MS_Positive_Mode.msp)
- MoNA MS2 negative mode library (MoNA-export-LC-MS-MS_Negitive_Mode.msp)
- GNPS library in MGF format (ALL_GNPS.mgf)

## Expected Outputs
- Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp)
- Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp)

## Expected Output File

- `combine_ms2_pos.msp`

## Landmark Outputs

- `nist_msms.sdf`
- `nist_msms_structure.txt`
- `nist_ms2_pos_processed.rda`
- `nist_ms2_neg_processed.rda`
- `gnps_complete.rda`
- `combine_ms2_pos.msp`

## Tools
- mspcompiler
- R
- future
- future.apply
- parallel
- NIST
- RIKEN
- MoNA
- GNPS
- MS-DIAL

## Skills
- mass-spectral-library-format-conversion
- mgf-metadata-completion-from-smiles
- spectral-library-polarity-separation
- chemical-structure-smiles-assignment
- tandem-ms-data-reorganization
- spectral-library-merging-and-deduplication

## Workflow Description
1. Load MS2 libraries from NIST, RIKEN, MoNA, and GNPS sources using read_lib() with type='MS2' or format='mgf' as applicable. 2. For NIST MS2, extract structure from MOL files via combine_mol2sdf() and extract_structure(), then assign SMILES using assign_smiles() with match='name'. 3. For MoNA MS2 libraries (positive and negative), apply reorganize_mona() to relocate SMILES from Comment field to SMILES field. 4. For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing. 5. Separate both NIST and GNPS libraries into positive and negative modes using separate_polarity() with polarity='pos' and polarity='neg'. 6. Combine all four sources (NIST, RIKEN, MoNA, GNPS) into two polarity-specific objects using c(). 7. Write polarity-separated libraries to MSP format using write_MS2_msp() for positive and negative modes. Validation: output MSP files conform to MS-DIAL format specification and contain no mixed polarities within a single file.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/Lib2NIST_configuration.png` | figure | False |
| `figures/Lib2NIST_define_subset.png` | figure | False |
| `figures/check_number_of_spectra_nist.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history available to document updates, bug fixes, or feature changes to the MS2 pipeline components.

## Domain Knowledge
- MS2 libraries from NIST, RIKEN, MoNA, and GNPS may contain overlapping spectra across sources; combining them increases file size but does not affect functional use in MS-DIAL.
- MoNA MS2 libraries store SMILES information in the Comment field rather than a dedicated SMILES field, requiring extraction and relocation via reorganize_mona().
- GNPS library data are distributed in MGF format and lack Molecular Formula fields, necessitating calculation from SMILES via complete_mgf() before format conversion to MSP.
- Both NIST and GNPS MS2 libraries mix positive and negative ionization modes in single files; separation by separate_polarity() is required before writing mode-specific MSP outputs.
- Parallel computing via future and parallel packages reduces processing time for large library integration operations that include structure extraction and SMILES assignment.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: future, future.apply, parallel, NIST, MoNA, Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp), Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp).

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the sequence of operations in the MS2 library compilation pipeline for loading, completing metadata, assigning chemical structures, separating by ionization polarity, and writing polarity-specific MSP files?: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The mspcompiler system processes MS2 libraries through a sequence of steps: loading libraries from NIST, MoNA, GNPS, or RIKEN sources via read_lib; completing MGF metadata through complete_mgf; assigning SMILES structures via assign_smiles; separating positive and negative ionization modes via separate_polarity; and writing polarity-separated MSP files via write_MS2_msp for use in MS-DIAL.: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] NIST MS2 library MSP file (NIST_msms.MSP): 'nist_ms2 <- read_lib("D:/MS_libraries/NIST_msms.MSP", type = "MS2")'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] NIST MS2 MOL directory containing structure files (NIST_msms.MOL): 'combine_mol2sdf("D:/MS_libraries/NIST_msms.MOL", "D:/MS_libraries/nist_msms.sdf")'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] RIKEN MS2 positive mode library (MSMS-Public-Pos-VS15.msp): 'riken_ms2_pos <- read_lib("D:/MS_libraries/MSMS-Public-Pos-VS15.msp")'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] RIKEN MS2 negative mode library (MSMS-Public-Neg-VS15.msp): 'riken_ms2_neg <- read_lib("D:/MS_libraries/MSMS-Public-Neg-VS15.msp")'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] MoNA MS2 positive mode library (MoNA-export-LC-MS-MS_Positive_Mode.msp): 'mona_ms2_pos <- read_lib("D:/MS_libraries/MoNA-export-LC-MS-MS_Positive_Mode.msp")'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] MoNA MS2 negative mode library (MoNA-export-LC-MS-MS_Negitive_Mode.msp): 'mona_ms2_neg <- read_lib("D:/MS_libraries/MoNA-export-LC-MS-MS_Negitive_Mode.msp")'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] GNPS library in MGF format (ALL_GNPS.mgf): 'gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp): 'write_MS2_msp(combine_ms2_pos, "/D:MS_libraries/combine_ms2_pos.msp")'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp): 'write_MS2_msp(combine_ms2_neg, "/D:MS_libraries/combine_ms2_neg.msp")'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] mspcompiler: 'library(mspcompiler)'
- `ev_013` from `agent2_synthesis` (agent2_traced): [other] R: 'library(mspcompiler)'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] future: 'library(future)'
- `ev_015` from `agent2_synthesis` (agent2_traced): [other] future.apply: 'library(future.apply)'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] parallel: 'library(parallel)'
- `ev_017` from `agent2_synthesis` (agent2_traced): [other] NIST: 'The NIST MS2 library can be treated as the same as the NIST EI library'
- `ev_018` from `agent2_synthesis` (agent2_traced): [other] RIKEN: 'The RIKEN MS2 libraries can be download from the MS-DIAL homepage'
- `ev_019` from `agent2_synthesis` (agent2_traced): [other] MoNA: 'The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads'
- `ev_020` from `agent2_synthesis` (agent2_traced): [other] GNPS: 'The GNPS library can be download from https://gnps.ucsd.edu/ProteoSAFe/libraries.jsp'
- `ev_021` from `agent2_synthesis` (agent2_traced): [other] MS-DIAL: 'both positive and negative modes are in a single file as well. Therefore, we need to separated the polarity'
- `ev_022` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history available to document updates, bug fixes, or feature changes to the MS2 pipeline components.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: mspcompiler package source code at github:QizhiSu__mspcompiler
- verify script_runs: load mspcompiler R package with library(mspcompiler) without errors
- verify file_format_is: input MS2 library files conform to expected MGF or MSP format from NIST/MoNA/GNPS/RIKEN sources
- verify output_matches_reference: polarity-split MSP files generated by write_MS2_msp contain expected fields (NAME, PRECURSORMZ, INCHIKEY, SMILES) for each spectrum entry
- verify contains_substring: complete_mgf function output includes populated MGF metadata fields (PEPMASS, CHARGE, RTINSECONDS)
- verify contains_substring: assign_smiles function output includes SMILES field in processed library records
- verify contains_substring: separate_polarity function produces distinct positive and negative mode output files with correct polarity labels
- verify script_runs: ARCH_MS2_PIPELINE orchestrator control loop executes complete sequence (load → complete_mgf → assign_smiles → separate_polarity → write_MS2_msp) without runtime errors, robust to parameter choices

### Expert Review
- chemical correctness: SMILES assignments generated by assign_smiles match the chemical structures in source libraries (NIST/MoNA/GNPS/RIKEN); requires validation against reference compound identifiers
- MS2 spectrum fidelity: m/z and intensity values in polarity-split MSP output maintain accuracy relative to original library entries; no systematic shifts or truncation
- metadata completeness: all required MGF metadata fields are populated by complete_mgf without loss of information from original sources; no field collisions or overwrites
- polarity assignment correctness: separate_polarity correctly classifies spectra into positive and negative ionization modes based on PRECURSORMZ sign and source library metadata

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium
- **Commercial software:** NIST

## Methodology Summary
1. Load MS2 spectral data from four independent sources (NIST, RIKEN, MoNA, GNPS) in their native formats.
2. Extract and assign chemical structure identifiers (SMILES, InChIKey, Molecular Formula) to all entries via structure file conversion and matching.
3. Standardize metadata fields across heterogeneous library formats by extracting SMILES from embedded Comment fields (MoNA) and computing missing Molecular Formula from SMILES (GNPS).
4. Separate mixed-polarity libraries into positive and negative ionization mode subsets.
5. Merge all four library sources into two polarity-specific objects and write as MS-DIAL-compatible MSP files.
6. Validation: Output MSP files contain no mixed polarities, SMILES fields are populated for all entries, and Molecular Formula is present where applicable.

## Workflow Ports

**Inputs:**

- `nist_ms2_msp` — NIST MS2 library MSP file ← `task_001/combined_ei_msp`
- `nist_ms2_mol` — NIST MS2 MOL directory
- `riken_ms2_pos_msp` — RIKEN MS2 positive mode library
- `riken_ms2_neg_msp` — RIKEN MS2 negative mode library
- `mona_ms2_pos_msp` — MoNA MS2 positive mode library
- `mona_ms2_neg_msp` — MoNA MS2 negative mode library
- `gnps_mgf` — GNPS library in MGF format

**Outputs:**

- `combined_ms2_pos_msp` — Combined MS2 positive mode library in MSP format
- `combined_ms2_neg_msp` — Combined MS2 negative mode library in MSP format

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:QizhiSu__mspcompiler`
- **Synthesized at:** 2026-06-15T13:39:11+00:00

## Extraction Quality
- Score: 3/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - research_question evidence_span does not explicitly mention 'loading, completing metadata, assigning chemical structures, separating by ionization polarity, and writing polarity-specific MSP files' as a sequence—it only describes compiling and organizing libraries
  - finding claims specific function names (read_lib, complete_mgf, assign_smiles, separate_polarity, write_MS2_msp) and their sequence, but the evidence_span provides only generic high-level description without mentioning these function names or steps
  - finding references 'RIKEN sources' but RIKEN is not mentioned in the research_question evidence_span
  - finding claims workflow applies reorganize_mona() for MoNA libraries, but this function is not mentioned in any evidence_span
- Notes: This task card shows a systematic gap between high-level evidence (generic description of library compilation) and detailed claims (specific R function names and multi-step pipeline). The research_question and finding do not coherently align—the question asks about 'sequence of operations' but the evidence does not describe a sequence, only an end goal. The workflow_description and task_description contain rich implementation details not supported by the evidence_spans, suggesting they were generated from domain knowledge rather than extracted from source material. The truncated evidence_span ending mid-sentence ('can be') indicates incomplete source extraction. Quality is degraded by: (1) semantic mismatch between RQ and finding, (2) insufficient evidence for specific function names, (3) inclusion of RIKEN in workflow but not in RQ evidence, (4) over-specification in workflow relative to grounding, and (5) apparent inferences presented as facts. Recommend: verify article actually discusses these function names and pipeline steps by name; check for complete evidence_span extraction; clarify whether workflow_description is specification or ground truth.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

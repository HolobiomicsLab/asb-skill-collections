# SciTask Card: Reconstruct the EI Library Compilation Pipeline (read → assign SMILES → assign RI → combine → write MSP)

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:31:46.023986+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mspcompiler/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `QizhiSu/mspcompiler`
- Quality: Score 3/5 — 1 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `database-annotation`, `gc-ms`, `spectral-library-matching`, `tandem-ms`

## Research Question
What is the orchestrated sequence of operations for compiling EI mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, SWGDRUG) into a single MSP file in mspcompiler?

## Connected Finding
The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the consolidated result to a single MSP file via write_EI_msp for use in MS-DIAL.

## Task Description
Compile four EI mass spectral libraries (NIST, RIKEN, MoNA, SWGDRUG) into a single, structure-annotated combined library with Kovats RI assignments, and write the result as an MS-DIAL–compatible MSP file.

## Inputs
- NIST EI library MSP file exported from Lib2NIST
- NIST.MOL folder containing MOL structure files corresponding to NIST library
- RIKEN EI library MSP file with Kovats RI
- MoNA GC-MS Spectra MSP file
- SWGDRUG EI library NIST format (converted to MSP via Lib2NIST) and Agilent format (converted to MOL folder)
- NIST ri.dat and USER.DBU files containing experimental RI data

## Expected Outputs
- Combined EI mass spectral library MSP file containing merged records from all four source libraries with SMILES and Kovats RI annotations

## Expected Output File

- `combine_ei.msp`

## Landmark Outputs

- `nist.sdf`
- `nist_structure.txt`
- `swgdrug.sdf`
- `swgdrug_structure.txt`
- `nist_ri_extracted.txt`

## Tools
- mspcompiler
- R
- future
- future.apply
- parallel
- Lib2NIST
- MS-DIAL
- NIST
- MoNA
- RIKEN

## Skills
- spectral-library-compilation-and-merging
- smiles-structure-annotation-from-molfiles
- retention-index-assignment-and-filtering
- mass-spectral-metadata-harmonization
- msp-file-format-handling-and-validation
- parallel-computation-for-large-library-processing

## Workflow Description
1. Load NIST EI library MSP file using read_lib() with type='EI'; convert NIST.MOL folder to SDF format using combine_mol2sdf(); extract chemical structures from SDF using extract_structure(); assign SMILES to library using assign_smiles() with match='name' parameter. 2. Load RIKEN EI library using read_lib() with type='EI' and remove_ri=FALSE to retain Kovats RI. 3. Load MoNA EI library using read_lib() with type='EI'; reorganize SMILES from Comment field using reorganize_mona(). 4. Load SWGDRUG EI library using read_lib() with type='EI'; convert SWGDRUG.MOL folder to SDF using combine_mol2sdf(); extract structures using extract_structure(); assign SMILES using assign_smiles() with match='name'. 5. Combine all four libraries using c() operator; extract experimental RI data from NIST ri.dat and USER.DBU files using extract_ri(); assign RI to combined library using assign_ri() with polarity='semi-polar', filtering for capillary GC columns only and retaining median RI when standard deviation < 30. 6. Write combined library to MSP file using write_EI_msp(). Validation: output file exists in MSP format with all four source libraries merged, SMILES and RI fields populated for eligible compounds, and no structural duplicates across sources.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/Lib2NIST_configuration.png` | figure | False |
| `figures/Lib2NIST_define_subset.png` | figure | False |
| `figures/check_number_of_spectra_nist.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- EI (electron ionization) libraries are typically distributed in vendor-specific formats (NIST, Agilent) and must be converted to unified MSP (MASCOT Search Format) for use in open-source tools like MS-DIAL.
- Kovats Retention Index (RI) is a normalized GC retention metric; capillary GC columns are standard, and RI values from different column polarities (non-polar, semi-polar, polar) are not interchangeable.
- SMILES (Simplified Molecular Input Line Entry System) are stored in MOL/SDF files but may need extraction and remapping; InChIKey provides an alternative stable identifier for structure matching across sources.
- When combining multiple curated libraries (NIST, RIKEN, MoNA, SWGDRUG), duplicate or near-duplicate spectra can occur; filtering by RI standard deviation (threshold: SD < 30) reduces spurious or outdated records.
- Parallel computation using future/future.apply is essential for processing NIST libraries, which contain tens of thousands of spectra and MOL files; single-threaded processing can take hours.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: future, future.apply, parallel, Lib2NIST, NIST, MoNA, Combined EI mass spectral library MSP file containing merged records from all four source libraries with SMILES and Kovats RI annotations.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the orchestrated sequence of operations for compiling EI mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, SWGDRUG) into a single MSP file in mspcompiler?: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the consolidated result to a single MSP file via write_EI_msp for use in MS-DIAL.: 'compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] NIST EI library MSP file exported from Lib2NIST: 'Once you have the \*.MSP file and the correspondent \*.MOL folder exported'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] NIST.MOL folder containing MOL structure files corresponding to NIST library: 'Once you have the \*.MSP file and the correspondent \*.MOL folder exported'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] RIKEN EI library MSP file with Kovats RI: 'Please download "All records with Kovats RI...EI-MS..." As it contains Kovats RI'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] MoNA GC-MS Spectra MSP file: 'Please download "GC-MS Spectra" in "MSP" form'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] SWGDRUG EI library NIST format (converted to MSP via Lib2NIST) and Agilent format (converted to MOL folder): 'please download both **NIST Format** and **Agilent Format**. Then use *Lib2NIST* to convert'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] NIST ri.dat and USER.DBU files containing experimental RI data: 'Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri"'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Combined EI mass spectral library MSP file containing merged records from all four source libraries with SMILES and Kovats RI annotations: 'write_EI_msp(combine_ei, "/D:MS_libraries/combine_ei.msp")'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] mspcompiler: 'library(mspcompiler)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] R: 'library(mspcompiler)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] future: 'library(future)'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] future.apply: 'library(future.apply)'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] parallel: 'library(parallel)'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] Lib2NIST: 'you can transformed it into a msp file by *Lib2NIST*'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] MS-DIAL: 'MS-DIAL friendly msp file'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] NIST: 'NIST is the most commonly used **commercial** EI library'
- `ev_018` from `agent2_synthesis` (agent2_traced): [methods] MoNA: 'The MassBank of North America (MoNA) has an EI library available'
- `ev_019` from `agent2_synthesis` (agent2_traced): [methods] RIKEN: 'The MS-DIAL developers have compiled an EI library with Kovat RI included'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify that mspcompiler package exists in github:QizhiSu/mspcompiler repository
- verify file_exists for core function definitions: read_lib, read_multilibs, assign_smiles, assign_ri, write_EI_msp in the package source code
- script_runs: load mspcompiler library in R and confirm all five core functions are callable without error
- verify documentation or inline comments describe the ARCH_EI_PIPELINE orchestrator or equivalent fixed control-flow pipeline
- verify write_EI_msp function accepts combined library object and outputs a file with .msp extension

### Expert Review
- assess whether the documented pipeline control flow (load via read_lib/read_multilibs → assign_smiles → assign_ri → combine → write_EI_msp) is complete and free of unspecified intermediate steps or missing transformations
- confirm that the pipeline handles all four library sources (NIST, MoNA, RIKEN, SWGDRUG) as claimed in the scope statement, or identify which sources are actually supported
- review whether assign_ri function correctly assigns Kovats RI values and integrates experimental RI extracted from NIST files, as the scope implies

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy
- **Commercial software:** NIST, Lib2NIST
- **Open-source alternatives:**
  - NIST library (proprietary commercial database) → RIKEN, MoNA, SWGDRUG (open-access spectral libraries)

## Methodology Summary
1. Load and parse four EI libraries (NIST, RIKEN, MoNA, SWGDRUG) from MSP and SDF formats into R objects.
2. Extract and assign chemical structure annotations (SMILES) from MOL/SDF files, handling library-specific metadata fields (e.g., MoNA Comment field).
3. Retrieve and assign experimental Kovats RI values from NIST reference files, filtering for capillary GC columns and median RI with SD < 30.
4. Merge all four annotated libraries into a single combined object using concatenation.
5. Validate merged library completeness and write output as MS-DIAL–compatible MSP file.

## Workflow Ports

**Inputs:**

- `nist_msp` — NIST EI library MSP file
- `nist_mol_folder` — NIST.MOL folder with structure files
- `riken_msp` — RIKEN EI library MSP file
- `mona_msp` — MoNA GC-MS Spectra MSP file
- `swgdrug_msp` — SWGDRUG EI library MSP file
- `swgdrug_mol_folder` — SWGDRUG.MOL folder with structure files
- `nist_ri_files` — NIST ri.dat and USER.DBU files

**Outputs:**

- `combined_ei_msp` — Combined EI library MSP file with SMILES and RI

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:QizhiSu__mspcompiler`
- **Synthesized at:** 2026-06-15T13:38:50+00:00

## Extraction Quality
- Score: 3/5
- Coherent: true
- Placeholder detected: false
- Groundedness failures (1):
  - inputs[5]: evidence_span not found in section 'methods' (value='NIST ri.dat and USER.DBU files containing experimental RI da', span='Extract experimental RI from the "ri.dat" and "USER.DBU" fil')
- Notes: The card demonstrates strong internal consistency between task_objective, task_description, and workflow_description, with detailed methodology and clear expected artifacts. However, there is a critical semantic gap between the research_question (which names four sources) and its evidence_span (which names only three: NIST, MoNA, GPNS—not RIKEN or SWGDRUG as claimed). The finding contains substantial inferred detail (function names, parameter names, pipeline order) that exceeds what is explicitly stated in the evidence_span. The groundedness failure for inputs[5] indicates the RI file input lacks proper source grounding. Domain knowledge is comprehensive and well-articulated. For acceptance, the research_question evidence_span must be updated to include all four sources, or the question must be revised to match the actual evidence.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*

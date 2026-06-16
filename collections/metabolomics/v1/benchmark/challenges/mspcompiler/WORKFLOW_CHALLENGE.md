# Workflow Challenge: `coll_mspcompiler_workflow`


> mspcompiler is an R package that compiles EI and tandem mass spectral libraries from multiple sources (NIST, MoNA, GNPS, RIKEN) into consolidated, MS-DIAL-compatible MSP files. The package provides a systematic workflow for reading, enriching with chemical structures and retention indices, and organizing spectral data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

mspcompiler describes mechanisms for processing mass spectral libraries across two main workflows. The EI library pipeline reads libraries via read_lib or read_multilibs, assigns SMILES structures and Kovats retention indices, combines processed libraries, and writes consolidated output via write_EI_msp for use in MS-DIAL. The MS2 library workflow loads libraries from multiple sources via read_lib, optionally completes MGF metadata via complete_mgf, assigns SMILES structures, separates positive and negative ionization modes via separate_polarity, and writes polarity-separated MSP files via write_MS2_msp. Supporting mechanisms include extract_ri and assign_ri for extracting and assigning experimental retention indices from NIST data, and reorganize_mona for extracting and reorganizing SMILES information from MoNA library comment fields. The package integrates with future and future.apply packages to enable parallel processing during library compilation.

## Research questions

- What is the orchestrated sequence of operations for compiling EI mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, SWGDRUG) into a single MSP file in mspcompiler?
- What is the sequence of operations in the MS2 library compilation pipeline for loading, completing metadata, assigning chemical structures, separating by ionization polarity, and writing polarity-specific MSP files?
- How does extract_ri extract Kovats retention index values from a NIST ri.dat file, and how does assign_ri then populate those RI values into a compiled EI library object?
- How does the reorganize_mona function restructure a downloaded MoNA EI library file into the internal list format required by subsequent mspcompiler pipeline steps?
- Does configuring the future::plan(multisession) parallel backend before calling read_multilibs on a directory of MSP files successfully spawn multiple worker sessions while producing a merged library object identical to the serial result?

## Methods overview

Load and parse four EI libraries (NIST, RIKEN, MoNA, SWGDRUG) from MSP and SDF formats into R objects. Extract and assign chemical structure annotations (SMILES) from MOL/SDF files, handling library-specific metadata fields (e.g., MoNA Comment field). Retrieve and assign experimental Kovats RI values from NIST reference files, filtering for capillary GC columns and median RI with SD < 30. Merge all four annotated libraries into a single combined object using concatenation. Validate merged library completeness and write output as MS-DIAL–compatible MSP file. Load MS2 spectral data from four independent sources (NIST, RIKEN, MoNA, GNPS) in their native formats. Extract and assign chemical structure identifiers (SMILES, InChIKey, Molecular Formula) to all entries via structure file conversion and matching. Standardize metadata fields across heterogeneous library formats by extracting SMILES from embedded Comment fields (MoNA) and computing missing Molecular Formula from SMILES (GNPS). Separate mixed-polarity libraries into positive and negative ionization mode subsets. Merge all four library sources into two polarity-specific objects and write as MS-DIAL-compatible MSP files. Validation: Output MSP files contain no mixed polarities, SMILES fields are populated for all entries, and Molecular Formula is present where applicable. Load a compiled EI library object and NIST RI database files (ri.dat and USER.DBU) into R. Parse NIST RI database files using extract_ri to retrieve experimental retention index records. Filter RI records to retain only those from capillary GC columns; compute median RI for compounds with multiple records and discard records with standard deviation > 30. Assign filtered RI values to the EI library object using assign_ri with semi-polar column polarity specification. Validation: Verify that RI field is populated in the output library object and confirm presence of RI values in MSP output file. Load the MoNA EI MSP file into R using read_lib() to parse the initial msp structure. Apply reorganize_mona() to extract SMILES from the Comment field and populate the SMILES field. Validation: Verify the output object has a populated SMILES field for all records and row count equals input row count. Load mspcompiler, future, future.apply, and parallel packages. Configure multisession parallel backend with worker count set to detectCores() - 1. Ingest all MSP files from the in-house directory using read_multilibs(). Disable parallel execution and return to sequential mode. Validation: Compare merged library object structure, spectrum count, and metadata fields against a serial reference generated from identical input files processed sequentially to confirm equivalence.

**Domain:** metabolomics

**Techniques:** database-annotation, gc-ms, spectral-library-matching, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources such as NIST, MoNA, and GPNS. _[grounded: SYS_MSPCOMPILER]_
- **(finding)** NIST is the most commonly used commercial EI library.
- **(finding)** Lib2NIST can be downloaded from https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17 if not installed with the NIST library. _[grounded: TOOL_LIB2NIST]_
- **(finding)** For Agilent users, the NIST input file for Lib2NIST can be found in, for example, C:/database/NIST14.L. _[grounded: TOOL_LIB2NIST]_
- **(finding)** The total number of spectra in a NIST library can be checked in the MS Search program under Options -> Libraries.
- **(finding)** The *.MOL folder in NIST library export contains a large number of mol files and is time-consuming to move, copy, or delete.
- **(finding)** The RIKEN EI library can be downloaded from http://prime.psc.riken.jp/compms/msdial/main.html#MSP. _[grounded: DS_RIKEN_EI]_
- **(finding)** The RIKEN EI library contains Kovats RI included. _[grounded: TOOL_MSDIAL]_
- **(finding)** The RIKEN EI library already has SMILES and InChIKey well-organized, so no further treatment is needed. _[grounded: DS_RIKEN_EI]_
- **(finding)** The MassBank of North America (MoNA) has an EI library available for download at https://mona.fiehnlab.ucdavis.edu/downloads.
- **(finding)** The MoNA EI library file has SMILES information in the Comment field rather than the SMILES field. _[grounded: DS_MONA_EI]_
- **(finding)** The SMILES in MoNA EI library must be extracted from the Comment field and put into the SMILES field using the reorganize_mona function. _[grounded: TOOL_REORGANIZE_MONA]_
- **(finding)** The Scientific Working Group for the Analysis of Seized Drugs (SWGDRUG) has compiled an EI library with drug or drug-related compounds.
- **(finding)** The SWGDRUG library is available at https://swgdrug.org/ms.html.
- **(finding)** To correctly parse the SWGDRUG library by mspcompiler, both NIST Format and Agilent Format downloads are required. _[grounded: SYS_MSPCOMPILER]_
- **(finding)** The SWGDRUG file does not contain InChIKey information.
- **(finding)** Polarity options for assigning RI to combined EI libraries are semi-polar, non-polar, or polar.
- **(finding)** Capillary GC columns are commonly used in the assign_ri function. _[grounded: TOOL_ASSIGN_RI]_
- **(finding)** When there are multiple RI records for a single compound, the median RI will be used.
- **(finding)** RI values with a standard deviation higher than 30 will be discarded.
- **(finding)** Positive and negative modes in MS2 libraries are normally separated into 2 msp files.
- **(finding)** The NIST MS2 library input file for Lib2NIST can be found in C:/Programs/nist14/mssearch/nist_msms. _[grounded: TOOL_LIB2NIST]_
- **(finding)** The NIST MS2 exported msp file has both positive and negative modes mixed in a single file. _[grounded: DS_NIST_MS2]_
- **(finding)** The RIKEN MS2 libraries can be downloaded from the MS-DIAL homepage at http://prime.psc.riken.jp/compms/msdial/main.html#MSP. _[grounded: TOOL_MSDIAL]_
- **(finding)** The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads. _[grounded: DS_MONA_MS2]_
- **(finding)** The GNPS library is organized in mgf format. _[grounded: COMP_MGF_FORMAT]_
- **(finding)** The GNPS library does not have the Molecular Formula (MF) field.
- **(finding)** The molecular formula in GNPS library can be calculated from SMILES using the complete_mgf function. _[grounded: TOOL_COMPLETE_MGF]_
- **(finding)** Both positive and negative modes are in a single GNPS file.
- **(finding)** The GNPS library can be downloaded from https://gnps.ucsd.edu/ProteoSAFe/libraries.jsp.
- **(finding)** The read_multilibs function allows reading multiple msp files from a folder at once. _[grounded: TOOL_READ_MULTILIBS]_
- **(finding)** The mspcompiler package offers remove_ri and remove_rt functions to remove RI and RT respectively. _[grounded: SYS_MSPCOMPILER]_
- **(finding)** The change_meta function can be used to modify metadata such as comment, collision energy, and instrument type. _[grounded: TOOL_CHANGE_META]_
- **(finding)** The RIKEN, MoNA, and GNPS MS2 libraries might contain identical spectra as they all compile some well-known libraries. _[grounded: DS_GNPS_MS2]_
- **(finding)** It takes a long time to process the NIST libraries.
- **(finding)** Once NIST libraries are organized, they can be saved as .Rda files and reused in subsequent compilations.
- **(finding)** Tandem mass spectral libraries are relatively big and consume high amounts of memory when read into R.
- **(finding)** If a PC does not have enough memory, libraries can be processed separately and combined in a text editor like Notepad++.
- **(finding)** The msp file is basically a text file.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- match = 'inchikey' for Linux-based or Mac OS instead of match = 'name'

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- SWGDRUG file should not use match = 'inchikey' because it does not contain InChIKey information

## Steps

### Step `task_001`
- Title: Reconstruct the EI Library Compilation Pipeline (read → assign SMILES → assign RI → combine → write MSP)
- Task kind: `component_reconstruction`
- Task: Compile four EI mass spectral libraries (NIST, RIKEN, MoNA, SWGDRUG) into a single, structure-annotated combined library with Kovats RI assignments, and write the result as an MS-DIAL–compatible MSP file.
- Inputs:
  - NIST EI library MSP file exported from Lib2NIST
  - NIST.MOL folder containing MOL structure files corresponding to NIST library
  - RIKEN EI library MSP file with Kovats RI
  - MoNA GC-MS Spectra MSP file
  - SWGDRUG EI library NIST format (converted to MSP via Lib2NIST) and Agilent format (converted to MOL folder)
  - NIST ri.dat and USER.DBU files containing experimental RI data
- Expected outputs:
  - Combined EI mass spectral library MSP file containing merged records from all four source libraries with SMILES and Kovats RI annotations
- Tools: mspcompiler, R, future, future.apply, parallel, Lib2NIST, MS-DIAL, NIST, MoNA, RIKEN
- Landmark output files: nist.sdf, nist_structure.txt, swgdrug.sdf, swgdrug_structure.txt, nist_ri_extracted.txt
- Primary expected artifact: `combine_ei.msp`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the MS2 Library Compilation Pipeline (read MGF/MSP → complete → assign SMILES → separate polarity → write MSP)
- Task kind: `component_reconstruction`
- Task: Load NIST, RIKEN, MoNA, and GNPS MS2 libraries; complete MGF metadata, assign SMILES, separate positive and negative modes, and write polarity-split MSP files suitable for MS-DIAL.
- Inputs:
  - NIST MS2 library MSP file (NIST_msms.MSP)
  - NIST MS2 MOL directory containing structure files (NIST_msms.MOL)
  - RIKEN MS2 positive mode library (MSMS-Public-Pos-VS15.msp)
  - RIKEN MS2 negative mode library (MSMS-Public-Neg-VS15.msp)
  - MoNA MS2 positive mode library (MoNA-export-LC-MS-MS_Positive_Mode.msp)
  - MoNA MS2 negative mode library (MoNA-export-LC-MS-MS_Negitive_Mode.msp)
  - GNPS library in MGF format (ALL_GNPS.mgf)
- Expected outputs:
  - Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp)
  - Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp)
- Tools: mspcompiler, R, future, future.apply, parallel, NIST, RIKEN, MoNA, GNPS, MS-DIAL
- Landmark output files: nist_msms.sdf, nist_msms_structure.txt, nist_ms2_pos_processed.rda, nist_ms2_neg_processed.rda, gnps_complete.rda, combine_ms2_pos.msp
- Primary expected artifact: `combine_ms2_pos.msp`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement the NIST RI Extraction and Assignment Step using extract_ri and assign_ri
- Task kind: `component_reconstruction`
- Task: Extract Kovats retention index (RI) data from NIST ri.dat and USER.DBU files using extract_ri, assign those RI values to a compiled EI mass spectral library object using assign_ri with semi-polar column polarity, and verify that the RI field is populated in the resulting library object.
- Inputs:
  - Compiled EI mass spectral library object in R (e.g., result of read_lib or combined libraries via c() operator)
  - NIST ri.dat file (retention index database file from NIST installation)
  - NIST USER.DBU file (user database file from NIST installation)
- Expected outputs:
  - EI library object with RI field populated for each compound based on median experimental RI from capillary columns, excluding records with standard deviation > 30
- Tools: mspcompiler, R, NIST
- Landmark output files: nist_ri_extracted.txt, combine_ei_with_ri.msp

### Step `task_004`
- Depends on: `task_001`
- Title: Implement the MoNA EI Library Reorganization Step using reorganize_mona
- Task kind: `component_reconstruction`
- Task: Apply the reorganize_mona function to a downloaded MoNA EI library MSP file to extract SMILES information from the Comment field and restructure it into the internal mspcompiler list format, producing a properly formatted library object ready for downstream pipeline steps.
- Inputs:
  - MoNA EI library in MSP format (GC-MS Spectra)
- Expected outputs:
  - Reorganized MoNA EI library object with SMILES field properly populated from Comment field
- Tools: NIST, mspcompiler, R, MoNA
- Landmark output files: mona_ei_raw.Rdata, mona_ei_reorganized.Rdata

### Step `task_005`
- Depends on: `task_001`
- Title: Extend mspcompiler to Support Parallel Library Reading via read_multilibs with Multisession Workers
- Task kind: `extension`
- Task: Configure parallel execution using future::plan(multisession) with worker count equal to detectCores() - 1, then ingest multiple MSP spectral library files from a directory using read_multilibs(), and verify that the merged library object matches the output of serial processing.
- Inputs:
  - Directory containing multiple MSP spectral library files from in-house or batch-processed standards
- Expected outputs:
  - Merged library R object containing all spectra from input MSP files, ready for downstream enrichment or export
- Tools: NIST, mspcompiler, R, future, future.apply, parallel
- Landmark output files: in_house_serial_reference.Rdata, in_house_parallel_output.Rdata

## Final expected outputs

- `Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp)` (type: file, tolerance: hash)
- `Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp)` (type: file, tolerance: hash)
- `EI library object with RI field populated for each compound based on median experimental RI from capillary columns, excluding records with standard deviation > 30` (type: file, tolerance: hash)
- `Reorganized MoNA EI library object with SMILES field properly populated from Comment field` (type: file, tolerance: hash)
- `Merged library R object containing all spectra from input MSP files, ready for downstream enrichment or export` (type: file, tolerance: hash)

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

- **Composition modularity:** flat

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
  "workflow_id": "coll_mspcompiler_workflow",
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
    "Combined MS2 positive mode library in MSP format (combine_ms2_pos.msp)": "<locator>",
    "Combined MS2 negative mode library in MSP format (combine_ms2_neg.msp)": "<locator>",
    "EI library object with RI field populated for each compound based on median experimental RI from capillary columns, excluding records with standard deviation > 30": "<locator>",
    "Reorganized MoNA EI library object with SMILES field properly populated from Comment field": "<locator>",
    "Merged library R object containing all spectra from input MSP files, ready for downstream enrichment or export": "<locator>"
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

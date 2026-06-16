# Workflow Challenge: `coll_lotus_workflow`


> LOTUS is a comprehensive collection of 484,174 (2D) and 588,694 (3D) unique referenced structure–organism pairs curated from 31 open databases, designed to enable computational understanding of organisms and their chemistry.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

LOTUS integrates structure–organism pairs from 31 initial open databases through a multi-stage curation pipeline. The dataset comprises 153,956 (2D) and 231,330 (3D) unique curated structures linked to 42,166 unique organisms. The curation workflow standardizes chemical structures through successive transformations including SMILES normalization and sanitization, translates and validates organism names across multiple taxonomic systems, and integrates reference metadata from multiple literature sources. The final curated dataset contains 484,174 (2D) and 588,694 (3D) unique referenced structure–organism pairs, with documented distributions showing that 89,903 2D structures are present in only one organism, 45,640 appear in between 1–10 organisms, 3,990 in 10–100 organisms, and 403 in more than 100 organisms.

## Research questions

- What are the documented headline counts of unique structure-organism pairs, curated structures, organisms, and source databases in the LOTUS dataset?
- What are the distribution counts of unique 2D structures in LOTUS when binned by organism prevalence (appearing in 1, 1–10, 10–100, or >100 distinct organisms)?
- What are the counts of unique organisms binned by the number of distinct 2D structures they contain in the categories: 1 structure, 1–10 structures, 10–100 structures, and >100 structures?
- How do the smiles.py and sanitizing.py scripts transform raw SMILES strings from the gathering layer into standardized, deduplicated structural identifiers?
- How does the 5_addingOTL.R script enrich cleaned organism names with Open Tree of Life identifiers?

## Methods overview

Download and extract LOTUS dataset deposit from Zenodo record 3778405. Load 3D and 2D structure-organism pair tables into memory. Deduplicate and count unique referenced structure-organism pairs per dimension. Count unique curated structure identifiers and unique organism identifiers across all records. Enumerate source database origins from metadata and verify count against 31 reported databases. Validation: All reported counts (588,694 3D pairs, 484,174 2D pairs, 231,330 3D structures, 153,956 2D structures, 42,166 organisms, 31 databases) must match actual file-derived counts with zero absolute difference. References: source article (DOI: 10.1007/s00044-016-1764-y) Load LOTUS flat file containing all unique 2D structure-organism associations. For each unique 2D structure, count the number of distinct organisms in which it appears. Assign each structure to one of four bins based on organism-occurrence count: 1 (singleton), 2–10 (low), 11–100 (medium), >100 (high). Tabulate the number of structures in each bin. Validation: Verify that bin counts match the reported gold standard (89,903 / 45,640 / 3,990 / 403) and that the four bin totals sum to 153,956 unique 2D structures. References: source article (DOI: 10.1007/s00044-016-1764-y) Load the LOTUS flat file as a data frame with structure ID and organism ID columns. For each unique organism, count the number of distinct 2D structures associated with it. Assign each organism to one of four bins: 1 structure, 2–10 structures, 11–100 structures, >100 structures. Tally the organism count within each bin. Validation: compare observed bin counts against reported values (7,354, 21,490, 10,683, 374); confirm all four match or report any deviation. References: source article (DOI: 10.1007/s00044-016-1764-y) Load raw SMILES table from the gathering layer output. Translate and standardise SMILES strings using smiles.py to enforce canonical representation. Validate and sanitise chemical structures using sanitizing.py, removing invalid or malformed entries. Deduplicate the sanitised structure table to generate the final unique SMILES identifier set. Validation: output file exists, contains deduplicated SMILES entries, and maintains row integrity across structure-organism mapping. References: source article (DOI: 10.1007/s00044-016-1764-y) Load the cleaned and taxonomy-verified organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz. Apply OTL name-to-identifier mapping using fuzzy matching and validation heuristics to assign stable taxonomic identifiers to each organism record. Enrich organism records with OTL metadata (identifiers, taxonomic ranks, synonyms, hierarchy). Write the enriched dictionary to interim/dictionaries/organism/otl.sqlite for indexed lookup and validation. Validation: Verify that all records in the cleaned organism table receive OTL identifiers and that the SQLite file is syntactically correct and queryable. References: source article (DOI: 10.1007/s00044-016-1764-y)

**Domain:** cheminformatics

**Techniques:** quantitative-structure-activity

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** LOTUS is a comprehensive collection of documented structure-organism pairs. _[grounded: COMP_STRUCTURE_ORGANISM_PAIRS]_
- **(finding)** The documented structure-organism pairs in LOTUS should allow a more complete understanding of organisms and their chemistry within current computational approaches in Natural Products research. _[grounded: DS_NPLIB]_
- **(finding)** LOTUS requires R to run.
- **(finding)** LOTUS requires Python 3 to run.
- **(finding)** LOTUS requires Java >= 17 to run.
- **(finding)** UNIX systems require Make to be installed for LOTUS.
- **(finding)** LOTUS has a dedicated Wiki for Windows users.
- **(finding)** LOTUS contains 588694 unique referenced structure-organism pairs in 3D. _[grounded: COMP_STRUCTURE_ORGANISM_PAIRS]_
- **(finding)** LOTUS contains 484174 unique referenced structure-organism pairs in 2D. _[grounded: COMP_STRUCTURE_ORGANISM_PAIRS]_
- **(finding)** LOTUS contains 231330 unique curated structures in 3D. _[grounded: RESULT_UNIQUE_STRUCTURES_3D]_
- **(finding)** LOTUS contains 153956 unique curated structures in 2D. _[grounded: RESULT_UNIQUE_STRUCTURES_3D]_
- **(finding)** LOTUS contains 42166 unique organisms. _[grounded: RESULT_UNIQUE_ORGANISMS]_
- **(finding)** LOTUS data originates from 31 initial open databases.
- **(finding)** Among 2D structures in LOTUS, 89903 are present in only 1 organism.
- **(finding)** Among 2D structures in LOTUS, 45640 are present in between 1 and 10 organisms. _[grounded: RESULT_2D_STRUCT_1_10_ORG]_
- **(finding)** Among 2D structures in LOTUS, 3990 are present in between 10 and 100 organisms. _[grounded: RESULT_2D_STRUCT_10_100_ORG]_
- **(finding)** Among 2D structures in LOTUS, 403 are present in more than 100 organisms. _[grounded: RESULT_2D_STRUCT_GT100_ORG]_
- **(finding)** Among organisms in LOTUS, 7354 contain only 1 2D structure.
- **(finding)** Among organisms in LOTUS, 21490 contain between 1 and 10 2D structures. _[grounded: RESULT_ORG_1_10_STRUCT]_
- **(finding)** Among organisms in LOTUS, 10683 contain between 10 and 100 2D structures. _[grounded: RESULT_ORG_10_100_STRUCT]_
- **(finding)** Among organisms in LOTUS, 374 contain more than 100 2D structures. _[grounded: RESULT_ORG_GT100_STRUCT]_

## Steps

### Step `task_001`
- Title: Reproduce the aggregate structure-organism pair statistics reported for the LOTUS dataset
- Task kind: `reproduction`
- Task: Retrieve the LOTUS dataset deposit and verify the reported headline structure-organism pair counts: 588,694 (3D) and 484,174 (2D) unique referenced pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms, and 31 source databases. Produce a verification report documenting actual counts against reported values.
- Inputs:
  - LOTUS dataset deposit from Zenodo (record 3778405)
- Expected outputs:
  - Verification report table with counts of 3D/2D structure-organism pairs, unique structures, unique organisms, and source databases, with reported vs. actual values and differences
- Tools: R, Python 3
- Landmark output files: 3d_structure_organism_pairs.csv, 2d_structure_organism_pairs.csv, unique_structures_inventory.csv, unique_organisms_list.txt, source_databases_enumeration.txt
- Primary expected artifact: `lotus_count_verification.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the organism-count distribution across 2D structure–organism pairs
- Task kind: `reproduction`
- Task: Bin the 153,956 unique 2D structures from the LOTUS database by organism occurrence frequency (1, 1–10, 10–100, >100 organisms per structure) and verify the four reported distribution counts: 89,903 / 45,640 / 3,990 / 403.
- Inputs:
  - LOTUS 2D structure-organism pairs table (published flat file or deposited dataset)
- Expected outputs:
  - Four-bin frequency distribution of 2D structures: singleton (89,903), low-diversity 1–10 (45,640), medium-diversity 10–100 (3,990), high-diversity >100 (403)
  - Verification report confirming counts match or documenting discrepancies
- Tools: R, Python 3
- Landmark output files: lotus_2d_structures_with_organism_counts.tsv, binned_distribution_summary.csv
- Primary expected artifact: `lotus_2d_organism_frequency_bins.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the structure-count distribution across organisms in the 2D dataset
- Task kind: `reproduction`
- Task: Load the LOTUS 2D structure-organism pair dataset, group unique organisms by their distinct structure count (1, 1–10, 10–100, >100), and verify the reported bin sizes: 7,354 / 21,490 / 10,683 / 374.
- Inputs:
  - LOTUS flat file containing 484,174 unique 2D structure-organism pairs and 42,166 unique organisms
- Expected outputs:
  - Table or data frame with organism count per bin: 7,354 organisms with 1 structure, 21,490 with 1–10, 10,683 with 10–100, 374 with >100
- Tools: R
- Landmark output files: organism_structure_counts.csv, binning_summary.txt
- Primary expected artifact: `organism_structure_bins.csv`

### Step `task_004`
- Title: Reconstruct the SMILES-to-InChI structure standardisation step in the curation pipeline
- Task kind: `component_reconstruction`
- Task: Convert raw SMILES identifiers from the gathering layer into a sanitised, standardised unique structure table by applying SMILES translation and chemical sanitization. Produce interim/tables/1_translated/structure/unique.tsv.gz as the canonical output.
- Inputs:
  - interim/tables/0_original/structure/smiles.tsv.gz — raw SMILES table from gathering layer
- Expected outputs:
  - interim/tables/1_translated/structure/unique.tsv.gz — deduplicated, sanitised SMILES table with standardised chemical structures
- Tools: R, Python
- Landmark output files: interim/tables/1_translated/structure/smiles.tsv.gz, interim/tables/1_translated/structure/unique.tsv.gz
- Primary expected artifact: `unique.tsv.gz`

### Step `task_005`
- Depends on: `task_002`
- Title: Reconstruct the organism taxonomy enrichment step via Open Tree of Life integration
- Task kind: `component_reconstruction`
- Task: Execute the 5_addingOTL.R script on the cleaned organism table to enrich organism records with Open Tree of Life (OTL) identifiers and produce the OTL-enhanced organism dictionary.
- Inputs:
  - Cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) containing standardized and verified organism names
- Expected outputs:
  - OTL-enriched organism dictionary in SQLite format (interim/dictionaries/organism/otl.sqlite)
- Tools: R
- Landmark output files: interim/dictionaries/organism/otl.sqlite
- Primary expected artifact: `otl.sqlite`

## Final expected outputs

- `Table or data frame with organism count per bin: 7,354 organisms with 1 structure, 21,490 with 1–10, 10,683 with 10–100, 374 with >100` (type: file, tolerance: hash)
- `interim/tables/1_translated/structure/unique.tsv.gz — deduplicated, sanitised SMILES table with standardised chemical structures` (type: file, tolerance: hash)
- `OTL-enriched organism dictionary in SQLite format (interim/dictionaries/organism/otl.sqlite)` (type: file, tolerance: hash)

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

- **Abstraction level:** concrete

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
  "workflow_id": "coll_lotus_workflow",
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
    "Table or data frame with organism count per bin: 7,354 organisms with 1 structure, 21,490 with 1\u201310, 10,683 with 10\u2013100, 374 with >100": "<locator>",
    "interim/tables/1_translated/structure/unique.tsv.gz \u2014 deduplicated, sanitised SMILES table with standardised chemical structures": "<locator>",
    "OTL-enriched organism dictionary in SQLite format (interim/dictionaries/organism/otl.sqlite)": "<locator>"
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

---
name: jms-compliant-database-querying
description: Use when you have grouped LC-MS features into empirical compounds with inferred molecular formulas and adduct assignments (via khipu), and you need to assign candidate metabolite identities at Level 4 annotation depth by matching against curated reference libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - HMDB
  - LIPID MAP
  - khipu
  - Python
  - JMS (Json's Metabolite Services)
  - HMDB (Human Metabolome Database)
  - LIPID MAPS Structure Database (LMSD)
  - PCPFM (Python-Centric Pipeline for Metabolomics)
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- we recommend that you download the JMS-compliant versions of the HMDB and LMSD using the `download extras` command
- perform MS1 annotation using an authentic compound library, a public database (e.g. HMDB, LIPID MAP), or custom database
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JMS-compliant database querying

## Summary

Query JMS-compliant versions of HMDB and LIPID MAPS Structure Database (LMSD) using inferred molecular formulas from empirical compounds to retrieve matching reference entries for Level 4 MS1 annotation. This skill bridges pre-annotated empirical compound objects (from khipu grouping) to standardized metabolite reference databases without requiring explicit m/z tolerance specification.

## When to use

You have grouped LC-MS features into empirical compounds with inferred molecular formulas and adduct assignments (via khipu), and you need to assign candidate metabolite identities at Level 4 annotation depth by matching against curated reference libraries. Use this skill when your input includes non-singleton empirical compounds (EmpCpds with inferred formulas from multiple grouped features) and you want deterministic, formula-driven retrieval from public JMS-compliant databases rather than tolerance-based m/z searching.

## When NOT to use

- Input contains only singleton empirical compounds (single features with unresolved adducts); their formulas cannot be reliably inferred and will not be annotated at Level 4.
- You require m/z tolerance-based searching (e.g., ppm windows); this skill uses exact formula matching without explicit tolerance parameters.
- Reference databases have not been downloaded or license agreements have not been accepted; `pcpfm download_extras` must be run first.
- Your input is raw feature tables or mzML data; the skill requires pre-grouped empirical compounds from khipu pre-annotation.

## Inputs

- Empirical compound object (JSON, moniker-referenced) with inferred molecular formulas and adduct assignments from khipu
- JMS-compliant HMDB reference database (local, downloaded via pcpfm download_extras)
- JMS-compliant LIPID MAPS Structure Database (LMSD) (local, downloaded via pcpfm download_extras)

## Outputs

- Annotated empirical compound object (JSON) with Level 4 candidate annotations (all database entries matching inferred formula for each EmpCpd)
- Annotation metadata stored in experiment structure under user-specified moniker

## How to apply

First, ensure the JMS-compliant HMDB and LMSD reference databases are downloaded locally via `pcpfm download_extras`, which places them in the correct directory structure and registers their license terms. Load the pre-built empirical compound object (identified by user-specified moniker) containing the grouped features with inferred formulas and adduct assignments output from the khipu pre-annotation step. For each empirical compound in the object, extract its inferred molecular formula (no explicit m/z tolerance is applied—the formula itself defines the search scope). Query both reference databases using exact formula matching, retrieving all database entries with matching molecular composition. Assign all retrieved entries as Level 4 candidate annotations to the corresponding empirical compound. Store the annotated empirical compound object under a new user-specified moniker in the experiment structure (typically in the `annotations/` subdirectory as JSON). Note that singleton empirical compounds (single features with ambiguous adducts) are not annotated at this level because their formulas cannot be reliably inferred.

## Related tools

- **khipu** (Pre-annotation tool that groups LC-MS features and infers molecular formulas and adduct assignments for empirical compounds used as input to formula-based database queries) — https://github.com/shuzhao-li-lab/khipu
- **JMS (Json's Metabolite Services)** (Backend search and annotation framework providing standardized query interface to JMS-compliant reference databases) — https://github.com/shuzhao-li-lab/JMS
- **HMDB (Human Metabolome Database)** (JMS-compliant reference database of human metabolites queried by molecular formula)
- **LIPID MAPS Structure Database (LMSD)** (JMS-compliant reference database of lipid structures queried by molecular formula)
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Pipeline orchestration and data management; provides `download_extras` command to acquire and register JMS-compliant databases and `pcpfm` CLI for database query execution) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Core language for implementing database query logic and empirical compound object manipulation)

## Examples

```
# After running: pcpfm download_extras
# Query Level 4 annotations using inferred formulas from khipu-annotated empirical compounds:
pcpfm annotate --empCpd_input my_experiment/annotations/empCpd_grouped.json --db_type jms --databases hmdb,lmsd --output_moniker empCpd_L4_annotated
```

## Evaluation signals

- All non-singleton empirical compounds in the input object receive Level 4 candidate annotations (no EmpCpds are left unannotated if they have inferred formulas).
- Retrieved candidates match the inferred formula exactly (no partial or approximate formula matches); verify by comparing the monoisotopic mass or formula string of each candidate against the EmpCpd's inferred formula.
- Annotated empirical compound object is valid JSON conforming to the metDataModel schema and can be loaded and queried by downstream tools (e.g., matchms for MS2 annotation).
- Output moniker is correctly registered in the experiment.json file and the annotated object is written to the `annotations/` subdirectory with expected file naming convention.
- Singleton empirical compounds are explicitly excluded from annotation (zero Level 4 candidates assigned); verify by checking EmpCpd metadata for adduct-inference status or filtering logic.

## Limitations

- Singleton empirical compounds (single grouped features) are not annotated at Level 4 because their adducts and formulas cannot be inferred reliably; only multi-feature empirical compounds receive annotations.
- The skill depends on pre-downloaded JMS-compliant databases; if databases are missing or outdated, queries will return incomplete or stale results. License agreement acceptance via `pcpfm download_extras` is required.
- Exact formula matching can lead to false positives if multiple distinct metabolites share the same molecular formula (e.g., isomers); Level 4 annotation does not resolve these ambiguities—downstream MS2 matching or authentic standards are needed.
- Reference databases (HMDB, LMSD) are not redistributed in the PCPFM package and must be downloaded separately, which may require network access and agreement to non-commercial use terms (especially for HMDB).
- No explicit m/z or ppm tolerance is applied; queries retrieve all database entries with exact formula match. If formula inference from khipu was inaccurate, candidate set will be wrong.

## Evidence

- [other] Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd which will be determined by the parameters used for construction.: "Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd"
- [other] Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred.: "Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred."
- [other] Query the JMS-compliant HMDB and LMSD reference databases downloaded via 'pcpfm download_extras' using the inferred formula from each empCpd: "Query the JMS-compliant HMDB and LMSD reference databases downloaded via 'pcpfm download_extras' using the inferred formula from each empCpd"
- [other] Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd.: "Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd."
- [readme] a JMS-compliant version of the HMDB and LMSD can be download and placed in the correct directory by running: `pcpfm download_extras`. After the basic installation is complete. By running this command, you agree to the terms and conditions of those 3rd pary resources.: "a JMS-compliant version of the HMDB and LMSD can be download and placed in the correct directory by running: `pcpfm download_extras`"
- [readme] HMDB, while free for public non-commercial use, is not redistributed in this package.: "HMDB, while free for public non-commercial use, is not redistributed in this package."

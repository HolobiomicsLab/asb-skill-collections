---
name: metabolite-mass-database-matching
description: Use when after features have been grouped into empirical compounds (empCpds)
  with inferred molecular formulas and adduct assignments by khipu, and you need to
  assign putative metabolite identities at the formula level.
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
  - pcpfm
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- we recommend that you download the JMS-compliant versions of the HMDB and LMSD using
  the `download extras` command
- perform MS1 annotation using an authentic compound library, a public database (e.g.
  HMDB, LIPID MAP), or custom database
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-mass-database-matching

## Summary

Match empirical compounds to known metabolites by querying JMS-compliant reference databases (HMDB, LMSD) using inferred molecular formulas. This Level 4 annotation step assigns candidate metabolite identities to grouped features without requiring explicit m/z tolerance specification.

## When to use

After features have been grouped into empirical compounds (empCpds) with inferred molecular formulas and adduct assignments by khipu, and you need to assign putative metabolite identities at the formula level. Use this skill when you have pre-built empCpd objects with assigned adducts and want to retrieve all known compounds matching those inferred formulas from public metabolite databases.

## When NOT to use

- Input empCpds are singletons or lack adduct inference—Level 4 annotation cannot be performed on these.
- You have only raw mzML or feature table data; you must first run khipu pre-annotation to group features and infer formulas.
- Your goal is to annotate individual features rather than grouped empirical compounds; use MS1 annotation on the feature table instead.

## Inputs

- empCpd object (pre-built from khipu, with inferred molecular formulas and adduct assignments)
- JMS-compliant HMDB database (downloaded)
- JMS-compliant LMSD (Lipid Maps Structure Database) (downloaded)

## Outputs

- Annotated empCpd object with Level 4 candidate metabolite annotations
- JSON file representing putative metabolites with formula-based matches

## How to apply

Load the pre-built empCpd object containing grouped features with inferred molecular formulas and adduct assignments from khipu. Query the JMS-compliant HMDB and LMSD reference databases (downloaded via 'pcpfm download_extras') using the inferred formula from each empCpd—no explicit m/z tolerance is applied, as the formula itself constrains the search. Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd. Store the annotated empCpd object under a new user-specified moniker in the experiment structure. Note that singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be reliably inferred.

## Related tools

- **khipu** (Pre-annotation tool that groups features into empirical compounds and infers molecular formulas and adduct assignments prior to database matching) — https://github.com/shuzhao-li-lab/khipu
- **HMDB** (Public metabolite reference database queried using inferred formulas to retrieve matching candidate compounds)
- **LIPID MAP** (Public lipid reference database (LMSD) queried using inferred formulas for lipid candidate matching)
- **JMS (Json's Metabolite Services)** (Provides search and annotation functions; HMDB and LMSD are provided in JMS-compliant format for streamlined querying) — https://github.com/shuzhao-li-lab/JMS
- **pcpfm** (Command-line interface (pcpfm download_extras) downloads JMS-compliant database versions; orchestrates the full annotation pipeline) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Implementation language for the Level 4 annotation workflow within the PCPFM pipeline)

## Evaluation signals

- All empCpds in the output object have a non-empty Level 4 annotation field (except singletons, which should remain unannotated)
- Retrieved candidate compounds match the inferred formula exactly—verify by cross-checking formula fields in the annotated empCpd against database records
- The number of candidates per empCpd is reasonable for the formula complexity (simple formulas may retrieve many candidates; complex formulas fewer)
- Annotated empCpd JSON structure is valid and can be loaded without parsing errors
- Singleton empCpds are explicitly flagged or skipped and do not receive Level 4 annotations

## Limitations

- Singleton empirical compounds (individual, ungrouped features) cannot be annotated at Level 4 because their adducts cannot be inferred.
- Annotation relies on inferred molecular formulas from khipu; errors in formula inference will propagate to database matches.
- No explicit m/z tolerance is applied—matches are formula-exact. This may miss compounds with formula ambiguity or isotope variations.
- The skill is limited to JMS-compliant versions of HMDB and LMSD; other public or proprietary databases require different query interfaces.
- Level 4 annotations are candidates only; further validation via MS2 data (matchms) or authentic standards is recommended for confirmation.

## Evidence

- [other] Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd which will be determined by the parameters used for construction.: "Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd"
- [other] Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred.: "Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred."
- [other] Load the pre-built empCpd object (moniker specified by user) containing grouped features with inferred molecular formulas and adduct assignments from khipu. Query the JMS-compliant HMDB and LMSD reference databases downloaded via 'pcpfm download_extras' using the inferred formula from each empCpd (no explicit mz tolerance applied; formula determines the search). Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd.: "Load the pre-built empCpd object (moniker specified by user) containing grouped features with inferred molecular formulas and adduct assignments from khipu. Query the JMS-compliant HMDB and LMSD"
- [readme] perform MS1 annotation using an authentic compound library, a public database (e.g. HMDB, LIPID MAP), or custom database: "perform MS1 annotation using an authentic compound library, a public database (e.g. HMDB, LIPID MAP), or custom database"
- [readme] a JMS-compliant version of the HMDB and LMSD can be download: "a JMS-compliant version of the HMDB and LMSD can be download"

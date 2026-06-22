---
name: level-4-annotation-assignment
description: Use when after khipu has grouped LC-MS features into empirical compounds with inferred molecular formulas and adduct assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3931
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - HMDB
  - LIPID MAP
  - khipu
  - Python
  - PCPFM
  - JMS (Json's Metabolite Services)
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
---

# Level 4 Annotation Assignment

## Summary

Level 4 annotation maps empirical compounds (EmpCpds) to chemical formulas and structure candidates by querying JMS-compliant HMDB and LMSD reference databases using inferred molecular formulas. This annotation level assigns putative metabolite identities based on exact mass matching without requiring explicit m/z tolerance specification.

## When to use

Apply this skill after khipu has grouped LC-MS features into empirical compounds with inferred molecular formulas and adduct assignments. Use it when you need to annotate EmpCpds against public reference libraries to generate candidate structure lists for metabolite identification, typically as the first structured annotation step before MS/MS matching.

## When NOT to use

- Input EmpCpds are singletons (ungrouped features) whose adducts cannot be inferred from khipu grouping
- You require MS/MS spectral matching; use Level 5+ annotation with matchms against MoNA instead
- The inferred formula from EmpCpd construction is uncertain or spans multiple adduct possibilities without clear consensus

## Inputs

- EmpCpd object (JSON) with grouped features, inferred molecular formulas, and adduct assignments from khipu
- JMS-compliant HMDB database (downloaded via 'pcpfm download_extras')
- JMS-compliant LMSD (Lipid Maps Structure Database) (downloaded via 'pcpfm download_extras')

## Outputs

- Annotated EmpCpd JSON object with Level 4 candidate structure assignments
- Feature-to-candidate mapping with database cross-references (HMDB IDs, LMSD IDs)

## How to apply

Load a pre-built EmpCpd object (JSON) containing grouped features with inferred molecular formulas and adduct assignments from khipu. For each EmpCpd, extract its inferred formula and query the JMS-compliant HMDB and LMSD databases (downloaded via 'pcpfm download_extras') using exact formula matching—no explicit m/z tolerance is applied because the search space is determined by the formula inferred during EmpCpd construction. Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding EmpCpd. Store the annotated EmpCpd object in the experiment's annotations/ directory under a user-specified moniker. Note that singleton EmpCpds (features not grouped with others) are not annotated at Level 4 because their adducts cannot be reliably inferred.

## Related tools

- **khipu** (Generates grouped empirical compounds and infers molecular formulas and adduct assignments prior to Level 4 annotation) — https://github.com/shuzhao-li-lab/khipu
- **HMDB** (JMS-compliant reference database queried for formula-based candidate structure matching)
- **LIPID MAP** (JMS-compliant reference database (LMSD) queried for lipid structure candidates)
- **PCPFM** (Pipeline orchestration tool that invokes the download_extras command to provision HMDB and LMSD, and manages annotation workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **JMS (Json's Metabolite Services)** (Provides search and database query infrastructure for formula-based metabolite lookups) — https://github.com/shuzhao-li-lab/JMS

## Evaluation signals

- All non-singleton EmpCpds in the input object receive at least one Level 4 candidate annotation (formula match found in HMDB or LMSD)
- Candidate structures assigned to each EmpCpd have inferred formulas matching the EmpCpd's formula exactly
- Output JSON validates against the EmpCpd schema (presence of 'annotation' or 'candidates' field at Level 4)
- Singleton EmpCpds are explicitly flagged as unannotated at Level 4 (not silently skipped)
- Database cross-references (HMDB IDs, LMSD lipid accessions) are retrievable and non-empty for matched candidates

## Limitations

- Singleton empirical compounds are not annotated at Level 4 because their adducts cannot be inferred, reducing coverage in sparse datasets
- Formula-based matching is sensitive to correctness of the inferred formula from khipu; errors in formula inference propagate directly to annotation
- No m/z or isotope-pattern refinement is applied at Level 4; annotation relies solely on molecular formula and does not rank candidates by probability
- Commercial use of HMDB is prohibited; users must comply with HMDB license terms when deploying the pipeline in commercial settings
- GC-MS and other ionization/instrument types are not yet fully supported; pipeline is optimized for LC-MS data

## Evidence

- [other] Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd which will be determined by the parameters used for construction.: "Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd which will be determined by"
- [other] Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred.: "Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred."
- [other] Load the pre-built empCpd object (moniker specified by user) containing grouped features with inferred molecular formulas and adduct assignments from khipu.: "Load the pre-built empCpd object (moniker specified by user) containing grouped features with inferred molecular formulas and adduct assignments from khipu."
- [other] Query the JMS-compliant HMDB and LMSD reference databases downloaded via 'pcpfm download_extras' using the inferred formula from each empCpd (no explicit mz tolerance applied; formula determines the search).: "Query the JMS-compliant HMDB and LMSD reference databases downloaded via 'pcpfm download_extras' using the inferred formula from each empCpd (no explicit mz tolerance applied; formula determines the"
- [other] Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd.: "Retrieve all database entries matching the inferred formula and assign them as Level 4 candidate annotations to the corresponding empCpd."
- [readme] Note that annotation sources including the HMDB, while free for public non-commercial use, is not redistributed in this package.: "Note that annotation sources including the HMDB, while free for public non-commercial use, is not redistributed in this package."
- [readme] empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards.: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards."

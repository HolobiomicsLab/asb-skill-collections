---
name: empirical-compound-construction-and-grouping
description: Use when after generating a feature table from mzML data (via Asari)
  and before performing MS1 or MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - HMDB
  - LIPID MAP
  - khipu
  - Python
  - Asari
  - metDataModel
  - mass2chem
  - PCPFM (PythonCentricPipelineForMetabolomics)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
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

# empirical-compound-construction-and-grouping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construction and grouping of LC-MS features into empirical compounds (EmpCpds) with inferred molecular formulas and adduct assignments using the khipu pre-annotation framework. This skill bridges feature detection and MS1/MS2 annotation by organizing co-detected features into putative metabolites before library matching.

## When to use

Apply this skill after generating a feature table from mzML data (via Asari) and before performing MS1 or MS2 annotation. Use it when you have grouped features that share retention time, mass relationships, and adduct signatures, and you need to infer molecular formulas and organize them into coherent empirical compounds for efficient downstream annotation against HMDB/LMSD or custom databases.

## When NOT to use

- Input is already a fully annotated metabolite list with confirmed chemical identities — EmpCpd construction is for pre-annotation grouping, not post-hoc validation.
- Features are singleton ions with no co-detected adducts — these cannot be meaningfully grouped and will not yield reliable formula inference.
- GC-MS or other non-LC data types — the pipeline and khipu currently target LC-MS/MS workflows only; GC support is under development.

## Inputs

- Asari feature table (TSV format with m/z, retention time, and feature intensities)
- mzML mass spectrometry data files
- Feature grouping parameters (retention time window, mass tolerance, adduct definitions)

## Outputs

- Empirical compound (EmpCpd) JSON object with inferred molecular formulas, adduct assignments, and grouped feature IDs
- EmpCpd moniker/identifier for referencing in downstream annotation steps

## How to apply

Load the Asari-processed mzML feature table and use khipu to infer molecular formulas and adduct assignments for grouped features. Khipu clusters features by retention time and mass relationships, assigning adduct types (e.g., [M+H]⁺, [M+Na]⁺) and deriving neutral mass formulas. The algorithm groups co-detected features into a single EmpCpd object, which stores the inferred formula, adduct list, and retention time range. Output the constructed EmpCpd as a JSON file containing all grouped features, their inferred formulas, and adduct hypotheses. This EmpCpd object is then used as input to Level 4 MS1 annotation (formula-based search against HMDB/LMSD) and can be annotated with MS2 spectra. Singleton features (those without co-detected adducts) are flagged as non-groupable and skipped during Level 4 annotation.

## Related tools

- **khipu** (Pre-annotation tool that infers molecular formulas and assigns adducts to grouped features, constructing EmpCpd objects with formula and adduct hypotheses) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Upstream feature detection and table generation from mzML; outputs feature table that serves as input to khipu-based EmpCpd construction) — https://github.com/shuzhao-li/asari
- **metDataModel** (Provides common data model definitions for EmpCpd objects and their serialization/deserialization in JSON format) — https://github.com/shuzhao-li-lab/metDataModel
- **mass2chem** (Utility library for mass-to-formula conversions and adduct mass calculations used during formula inference) — https://github.com/shuzhao-li-lab/mass2chem
- **PCPFM (PythonCentricPipelineForMetabolomics)** (End-to-end pipeline orchestrator that calls khipu for EmpCpd construction as a standard workflow step) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- EmpCpd JSON objects are created with non-null inferred_formula, adduct_list, and grouped_feature_ids fields
- Grouped features within each EmpCpd share consistent retention time (within specified window) and mass relationships matching predicted adduct mass shifts
- Singleton features are flagged or excluded from EmpCpd output; only features with ≥2 co-detected isotopes/adducts are retained
- EmpCpd monikers are consistently referenced in downstream Level 4 annotation queries (formula-based HMDB/LMSD search)
- JSON schema validation confirms EmpCpd object structure conforms to metDataModel specifications

## Limitations

- Singleton empirical compounds (features without co-detected adducts) are not constructed and cannot be annotated at Level 4, limiting annotation coverage in targeted analyses or low-abundance metabolites.
- Formula inference is dependent on accurate adduct parameter definitions; misspecified adduct masses or ionization modes will lead to incorrect formula assignments.
- GC-MS and other data types are not currently supported; only LC-MS/MS data are handled in this pipeline.
- Retention time-based grouping may falsely merge unrelated features from different metabolites if they co-elute; requires appropriate RT window tuning.

## Evidence

- [intro] Pre-annotation to group features to empirical compounds using khipu with inferred molecular formulas and adduct assignments: "pre-annotation to group featues to empirical compounds (khipu)"
- [other] EmpCpd parameters determine formula inference without requiring explicit mass tolerance specification: "Level 4 annotation infers formulas from EmpCpd parameters without requiring explicit mz tolerance specification, as the search uses the inferred formula from the EmpCpd which will be determined by"
- [other] Singleton empirical compounds cannot be annotated at Level 4: "Singleton empirical compounds are not currently annotated at Level 4 since their adducts cannot be inferred."
- [other] EmpCpd object workflow: load pre-built object, infer formulas, store under new moniker: "Load the pre-built empCpd object (moniker specified by user) containing grouped features with inferred molecular formulas and adduct assignments from khipu."
- [readme] EmpCpd JSON output structure for downstream analysis: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards."

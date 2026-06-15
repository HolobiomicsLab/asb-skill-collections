---
name: reproducibility-gap-detection
description: 'Use when evaluating whether a published computational method can be independently executed: (1) source code is claimed to be available but repository structure, build instructions, or dependency specifications are incomplete;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_0091
  tools:
  - GitHub
  - GNPS (Global Natural Products Social Molecular Networking)
  - Sirius 6
  - ISDB-LOTUS
  - MatchMS
  - MZmine 4
  - npanalyst
derived_from:
- doi: 10.1002/cmtd.202400088
  title: ms2decide
- doi: 10.5281/zenodo.5607185
  title: ''
- doi: 10.5281/zenodo.5794106
  title: ''
- doi: 10.1021/acscentsci.1c01108
  title: ''
- doi: 10.1021/acs.analchem.2c02093
  title: ''
- doi: 10.1021/acs.analchem.5c03730
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_13c_spacem
    doi: 10.1038/s42255-024-01118-4
    title: 13C-SpaceM
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_hexpmetdb
    doi: 10.1289/EHP7722
    title: HExpMetDB
  - build: coll_ms2decide
    doi: 10.1002/cmtd.202400088
    title: ms2decide
  - build: coll_np_analyst
    doi: 10.1021/acscentsci.1c01108
    title: NP Analyst
  - build: coll_rassp
    doi: 10.1021/acs.analchem.2c02093
    title: rassp
  - build: coll_rtmsecho
    doi: 10.1021/acs.analchem.5c03730
    title: rtmsecho
  dedup_kept_from: coll_ms2decide
schema_version: 0.2.0
---

# reproducibility_gap_detection

## Summary

Identify and document missing artifacts, documentation, and execution details that prevent independent reproduction of a computational scientific workflow. This skill surfaces gaps in code availability, parameter specification, data access, and provenance tracking that must be resolved to enable third-party verification.

## When to use

Apply this skill when evaluating whether a published computational method can be independently executed: (1) source code is claimed to be available but repository structure, build instructions, or dependency specifications are incomplete; (2) a workflow integrates multiple external tools (GNPS, Sirius, ISDB-LOTUS) but does not document authentication, version pinning, or failure-handling strategies; (3) the article describes input file formats and processing logic but provides no changelog, version history, or test data to validate correct implementation.

## When NOT to use

- The article does not describe a computational workflow or software implementation (e.g., purely theoretical or empirical-only studies).
- Source code is not publicly available and the article makes no claim of reproducibility or code release.
- The task is to verify correctness of results, not to assess whether execution is possible—use computational validation or benchmarking instead.

## Inputs

- GitHub repository URL (e.g., https://github.com/MejriY/MS2DECIDE)
- Article text describing the workflow and tool integration
- Repository README and installation/usage documentation
- Tool documentation references (GNPS, Sirius, ISDB-LOTUS, MatchMS)
- Source code files (setup.py, __init__.py, main module)

## Outputs

- Reproducibility gap report (structured list of missing or underspecified components)
- Artifact inventory (repository structure, license, dependency list)
- Parameter specification audit (defaults, ranges, thresholds used in workflow)
- Workflow execution checklist (required files, authentication, error-handling paths)
- Missing materials list (changelog, test data, example invocations, validation rules)

## How to apply

Systematically inspect four categories of reproducibility signals: (1) **Artifact Inventory**: locate the source repository (GitHub URL), verify presence of setup scripts (setup.py, environment.yml, requirements.txt), and confirm licensing metadata; (2) **Dependency & Version Specification**: check for pinned versions of integrating tools (GNPS, Sirius 6, ISDB-LOTUS, MatchMS, MZmine4) and runtime requirements (Python ≥3.8); (3) **Workflow Documentation**: trace parameter defaults (e.g., mass tolerance ≤0.5 Da for ISDB-LOTUS, cosine score threshold 0.001 vs. 0.1 for GNPS strict vs. iterative), decision logic (e.g., default Tanimoto=0.7 when matches missing), and handling of annotation failures; (4) **Execution Evidence**: identify missing changelog, test invocations, or example input/output pairs. Record each gap with its location (section, code path, or documentation file) and severity (blocks execution, complicates reproducibility, or is advisory). Use the article's own terminology (K-values, FBMN, feature annotations) and note deviations from cited tool documentation.

## Related tools

- **GitHub** (Source code repository and version control tracking; used to inspect repository structure, licensing, and commit history for reproducibility signals) — https://github.com/
- **GNPS (Global Natural Products Social Molecular Networking)** (Spectral library matching and FBMN (Feature-Based Molecular Networking) workflow; requires authentication (username, password, email), supports strict (0.02 Da, threshold 0.001) and iterative weighted analog search modes) — https://ccms-ucsd.github.io/GNPSDocumentation/
- **Sirius 6** (Molecular structure annotation from MS/MS spectra using CSI:FingerId and COSMIC; requires structure_identifications.tsv output file and choice of confidence score mode (exact vs. approximate))
- **ISDB-LOTUS** (Natural products spectral database matching using CFM-ID 4.0 and MatchMS; requires ionization mode (POS/NEG) and mass tolerance (<0.5 Da) specification) — https://zenodo.org/records/8287341
- **MatchMS** (Spectral similarity matching library used by ISDB-LOTUS annotation function (get_cfm_annotation)) — https://github.com/matchms/matchms
- **MZmine 4** (Mass spectrometry data processing; referenced for export format compatibility (≥2.53) for FBMN quantitative tables (.csv) and MGF files)

## Examples

```
from ms2decide.K_estimation import K_estimation
K_estimation()
```

## Evaluation signals

- Repository structure includes setup.py or pyproject.toml with all declared dependencies; pip/conda install succeeds without manual intervention.
- All integrating tools (GNPS, Sirius, ISDB-LOTUS, MatchMS, MZmine) are pinned to specific versions or version ranges; authentication and API endpoints are documented.
- Default parameter values (mass tolerance, cosine threshold, Tanimoto fallback values) are hardcoded or configurable in the code and match README specifications.
- Error-handling rules for tool failures are explicitly stated (e.g., Tanimoto default 0.7 when GNPS/Sirius match absent; Sirius score 0.5 when no annotation; ISDB-LOTUS zero answer treated as novelty signal).
- At least one complete example invocation (Python command or CLI) is provided with sample input files and expected output schema; a changelog or version history exists documenting API/parameter changes.

## Limitations

- When GNPS finds no match or Sirius provides no annotation, Tanimoto similarity cannot be calculated; a default value of 0.7 is assigned, which is a heuristic fallback that may not reflect true similarity.
- Sirius 6 batch mode occasionally fails to propose annotations; a fixed score of 0.5 is assigned as remediation, potentially masking genuine annotation uncertainty or tool version incompatibility.
- ISDB-LOTUS uses strict library search (0.02 Da tolerance); zero-result answers are treated as evidence of novelty, which may conflate true novel compounds with annotation search space limitations.
- GNPS iterative weighted analog search can require up to three hours and launches 27 FBMN jobs; users may face rate limits, authentication timeouts, or job failures not fully documented.
- The K_estimation function requires live internet connectivity and valid GNPS credentials; offline execution or batch processing without real-time prompts is not described.
- No changelog is present in the repository; version compatibility with updated GNPS/Sirius/LOTUS APIs cannot be tracked.

## Evidence

- [readme] GitHub repository presence and tool integration: "MS2DECIDE is a Python library that leverages decision theory to assist chemists in natural products multiannotation and prioritization... integrates GNPS (enhanced with a iterative weighted analog"
- [readme] Python version and dependency specification: "Ensure Python is installed (version 3.8 or higher)"
- [readme] Installation from GitHub with pip and conda commands: "pip install git+https://github.com/MejriY/MS2DECIDE.git"
- [readme] Input file format requirements and verification: "Ensure that your input files follow the required format (.csv for quantitative data, .mgf for mass spectrometry data). If you use the export file module of MZmine (>2.53) for FBMN, the format will be"
- [readme] GNPS authentication and workflow options: "The function will prompt you to provide your GNPS username, password, and email... Choose the type of GNPS library search: strict (0.02 Da, threshold 0.001) or iterative (up to three hours, 27 FBMN"
- [readme] Default parameter fallback for missing GNPS/Sirius matches: "In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi"
- [readme] Sirius failure remediation and score assignment: "Sirius annotations were performed in batch mode by using Sirius 6... in some cases, Sirius was not able to propose an annotation. To remedy, we associated a value of 0.5 to Sirius matching score."
- [readme] ISDB-LOTUS mass tolerance and novelty interpretation: "For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty."
- [readme] License declaration: "ms2decide is distributed under the terms of the MIT license."
- [readme] Tool version citations: "LOTUS... Version used: https://doi.org/10.5281/zenodo.5794106... ISDB... Version used: https://doi.org/10.5281/zenodo.5607185"

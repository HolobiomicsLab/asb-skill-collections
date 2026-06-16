---
name: expert-review-preparation
description: Use when you have a published scientific article describing a computational method (e.g., natural products annotation, MS/MS data processing) and need to assess reproducibility before expert scrutiny.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0334
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - GitHub
  - GNPS (Global Natural Products Social Molecular Networking)
  - ISDB-LOTUS
  - Sirius 6
  - MatchMS
  - MZmine 4
  - MZmine 2
  - mzmine2
  - MZmine
  - mzmine
  - GitHub Actions (CI/CD)
  - npanalyst
  - PyTorch
  - Conda/Mamba
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - COSMIC
  - ZODIAC
derived_from:
- doi: 10.1002/cmtd.202400088
  title: ms2decide
- doi: 10.1038/s41587-023-01690-2
  title: ''
- doi: 10.21105/joss.02411
  title: ''
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1021/acscentsci.1c01108
  title: ''
- doi: 10.1021/acs.analchem.2c02093
  title: ''
- doi: 10.1021/acs.analchem.5c03730
  title: ''
- doi: 10.1038/s41592-019-0344-8
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
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_hexpmetdb
    doi: 10.1289/EHP7722
    title: HExpMetDB
  - build: coll_ms2decide
    doi: 10.1002/cmtd.202400088
    title: ms2decide
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_np_analyst
    doi: 10.1021/acscentsci.1c01108
    title: NP Analyst
  - build: coll_rassp
    doi: 10.1021/acs.analchem.2c02093
    title: rassp
  - build: coll_rtmsecho
    doi: 10.1021/acs.analchem.5c03730
    title: rtmsecho
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_ms2decide
schema_version: 0.2.0
---

# expert_review_preparation

## Summary

Prepare a scientific computational workflow for expert review by systematically indexing article artifacts, tracing claims to reproducible outputs, and documenting missing materials or metadata. This skill bridges the gap between published claims and verifiable code/data by creating a structured inventory of tools, workflow steps, findings, and reproducibility gaps.

## When to use

Apply this skill when you have a published scientific article describing a computational method (e.g., natural products annotation, MS/MS data processing) and need to assess reproducibility before expert scrutiny. Specifically, use it when the article cites a GitHub repository and you want to systematically verify that the article's claims are grounded in working code, documented inputs/outputs, and traceable decisions.

## When NOT to use

- Article is purely theoretical with no software implementation or GitHub repository.
- Repository code is unavailable, archived, or has no README documentation.
- Your task is to execute the workflow yourself rather than prepare it for expert review—use the skill only for review preparation, not active data processing.

## Inputs

- Published article with computational method description
- GitHub repository URL cited in the article
- Repository README or documentation
- Article discussion/methods sections describing tools and workflow steps

## Outputs

- Indexed artifact inventory (tools, workflow steps, filter steps)
- Structured mapping of claims to code/documentation
- Missing signals report (missing changelog, undocumented parameters, absent data files)
- Evidence index linking article sections to repository material

## How to apply

First, extract and index the core artifacts: repository URLs, tool names (GNPS, Sirius, ISDB-LOTUS), workflow steps (FBMN job setup, annotation merging, K-value ranking), and claimed findings. Second, inspect the repository README for installation instructions, usage examples, input/output file formats (.csv, .mgf, .tsv), and parameter thresholds (e.g., cosine score 0.001, mass tolerance 0.02 Da). Third, trace each major claim in the article to a concrete function, file format, or workflow decision in the code—e.g., map 'multiannotation integration' to the K_estimation() function signature and its input prompts. Fourth, identify and document explicit gaps: missing changelogs, undocumented default values (e.g., T_gs = 0.7 when no match), or missing data artifacts. Finally, compile this inventory into a structured index with evidence spans linking article text directly to repository documentation.

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Spectral annotation engine integrated via FBMN workflow; requires username/password authentication and produces library search matches (strict or iterative weighted analog search modes)) — https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- **ISDB-LOTUS** (Natural products spectral library matching; applies strict mass tolerance (0.02 Da) for annotation candidates and reports zero matches as novelty signal) — https://zenodo.org/records/8287341
- **Sirius 6** (Structure identification and confidence scoring (exact vs. approximate modes); requires structure_identifications.tsv output file as input to K_estimation workflow) — https://v6.docs.sirius-ms.io/methods-background/#confidence-score-modes
- **MatchMS** (Spectral similarity matching library used internally by get_cfm_annotation() for ISDB-LOTUS spectral matching) — https://doi.org/10.21105/joss.02411
- **MZmine 4** (Exports quantitative feature tables (.csv) and MGF files in format compatible with MS2DECIDE K_estimation input (version >2.53 required)) — https://doi.org/10.1038/s41587-023-01690-2
- **GitHub** (Version control and artifact repository hosting; enables reproducibility verification and change tracking) — https://github.com/MejriY/MS2DECIDE

## Examples

```
from ms2decide.K_estimation import K_estimation; K_estimation()
```

## Evaluation signals

- All article claims about workflow structure (FBMN job creation, annotation merging, K-value sorting) have corresponding function signatures and parameter documentation in the README.
- Input file formats (.csv quantitative table, .mgf mass spectrometry data, structure_identifications.tsv Sirius output) and required directory structures are explicitly documented with example paths.
- Default/fallback parameter values mentioned in the article (e.g., T_gs = 0.7 when no GNPS match, Sirius matching score = 0.5 on failure) appear in the code or README with rationale.
- Installation and verification steps (conda environment creation, pip install, import check) are executable without external dependencies beyond listed tools.
- Output schema (.tsv file with K-values, column names, sorting order) is documented or illustrated in usage examples.

## Limitations

- GNPS matching is sensitive to library score threshold (0.001 default can cause failures; user may need to increase to 0.1); iterative weighted analog search can take up to three hours with 27 parallel jobs.
- Sirius batch annotation in Approximate mode may fail entirely for some features, requiring fallback confidence score assignment (0.5) without notification mechanism.
- Tanimoto similarity calculation between GNPS and Sirius/ISDB-LOTUS cannot be computed when either tool reports no match; default similarity 0.7 is assigned without data-driven justification.
- ISDB-LOTUS strict library search (0.02 Da tolerance) treats zero matches as novelty signal but may miss true annotations in highly congested mass regions.
- Redundant feature IDs in Sirius structure_identifications.tsv cause ValueError ('DataFrame index must be unique'); user must manually filter duplicates in external editor.

## Evidence

- [readme] MS2DECIDE is a Python library that leverages decision theory to assist chemists in natural products multiannotation and prioritization.: "MS2DECIDE is a Python library that leverages decision theory to assist chemists in natural products multiannotation and prioritization."
- [readme] The K_estimation function integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius. Processes user-provided input files such as quantitative data and MGF files. Generates a filtered dataframe based on the estimated K-values.: "The K_estimation function: Integrates annotation data from multiple sources: GNPS, ISDB-LOTUS, and Sirius. Processes user-provided input files such as quantitative data and MGF files. Generates a"
- [readme] Ensure that your input files follow the required format (.csv for quantitative data, .mgf for mass spectrometry data). If you use the export file module of MZmine (>2.53) for FBMN, the format will be accepted.: "Ensure that your input files follow the required format (.csv for quantitative data, .mgf for mass spectrometry data). If you use the export file module of MZmine (>2.53) for FBMN, the format will be"
- [readme] In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi in these instances.: "In scenarios where there is no match with GNPS or no match with Sirius, the tanimoto between GNPS and Sirius cannot be calculated. Hence, a default value of 0.7 was assigned to T_gs and T_gi in these"
- [readme] We recommend to increase the threshold value (for e.g., 0.1). Since, these workflows use a library score threshold of 0.001 some failures can occur with the FBMN GNPS workflow.: "Since, these workflows use a library score threshold of 0.001 some failures can occur with the FBMN GNPS workflow. We recommend to increase the threshold value (for e.g., 0.1)."
- [readme] For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty.: "For ISDB-LOTUS, since a strict library search was applied (0.02 Da), we considered a zero answer as an important information regarding our definition of novelty."
- [readme] We recommend to check this file for redundant features that can be generated in the Sirius annotation process. You can open the structure_identifications.tsv on Excel for example and highlight the redundant values in the 'mappingFeatureId' column.: "We recommend to check this file for redundant features that can be generated in the Sirius annotation process. You can open the structure_identifications.tsv on Excel for example and highlight the"

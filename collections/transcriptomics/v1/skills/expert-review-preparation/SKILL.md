---
name: expert-review-preparation
description: Use when when a paper describes a computational or statistical method and you need to verify that claims are supported by available code, data, or documentation before human expert evaluation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3316
  - http://edamontology.org/topic_0081
  tools:
  - GitHub
  - sctransform
  - Seurat
  - WGCNA (R package)
derived_from:
- doi: 10.1186/s13059-019-1874-1
  title: sctransform
- doi: 10.1186/1471-2105-9-559
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sctransform
    doi: 10.1186/s13059-019-1874-1
    title: sctransform
  - build: coll_wgcna
    doi: 10.1186/1471-2105-9-559
    title: wgcna
  dedup_kept_from: coll_sctransform
schema_version: 0.2.0
---

# expert_review_preparation

## Summary

Prepare a scientific task for expert review by systematically indexing article artifacts, connecting claims to computational outputs, inspecting available materials, and documenting missing information. This skill ensures reproducibility assessments have a complete, traceable evidence base.

## When to use

When a paper describes a computational or statistical method and you need to verify that claims are supported by available code, data, or documentation before human expert evaluation. Specifically: when no strong finding sentence is automatically detected, when reproducibility context is unclear, or when the gap between published claims and accessible artifacts needs systematic mapping.

## When NOT to use

- The article is purely theoretical with no computational code or reproducible artifacts to assess.
- Expert review has already been completed and validated; use this skill only to prepare for review, not after.
- The goal is to execute or run the method yourself; this skill is for *assessment*, not implementation.

## Inputs

- Article text (abstract, methods, results, discussion, supplementary materials)
- Cited repository URLs or package identifiers
- README and documentation files from referenced repositories
- Published paper metadata (DOI, title, authors, journal, year)

## Outputs

- Indexed artifact inventory (repositories, tools, versions cited)
- Claim-to-output traceability map
- Missing signals report (absent changelogs, undocumented workflows, unavailable data)
- Structured review brief ready for expert human evaluation

## How to apply

Perform a structured review workflow: (1) Index all referenced code repositories and artifacts (e.g., GitHub URLs, package names), noting the section in which each is cited. (2) For each repository, extract and review the README, installation instructions, and quick-start examples to understand scope and entry points. (3) Map each major claim in the paper to a corresponding output or tool function (e.g., 'normalization' → vst() function, 'variance stabilization' → regularized negative binomial regression). (4) Cross-check the availability of supporting materials: vignettes, worked examples, test data, and version history (changelog). (5) Document all missing signals—absent changelogs, undocumented parameters, missing test cases—as gaps for expert review. (6) Compile a summary record linking claims, tools, workflow steps, and missing information in a structured index.

## Related tools

- **GitHub** (Central platform for indexing and inspecting source code repositories, READMEs, changelogs, and release history referenced in the article)
- **sctransform** (Example R package that implements normalization and variance stabilization; serves as a concrete artifact to trace claims against documented functions (vst, SCTransform)) — https://github.com/satijalab/sctransform
- **Seurat** (Downstream R package that integrates sctransform core functionality; used to validate method integration and document alternative entry points) — https://satijalab.org/seurat/

## Examples

```
# Index and trace the sctransform claim from paper to repository
# 1. Retrieve README from https://github.com/satijalab/sctransform
# 2. Map claim 'normalization via regularized negative binomial regression' to function sctransform::vst()
# 3. Verify quick-start examples exist: normalized_data <- sctransform::vst(umi_count_matrix)$y
# 4. Record missing signal: 'No changelog found'
# 5. Output structured review brief for expert assessment
```

## Evaluation signals

- All major methodological claims in the paper are mapped to a specific function, parameter, or code section in the cited repository.
- Installation and quick-start instructions from README are complete and syntactically valid (e.g., R `install.packages()` or GitHub URL format).
- Each vignette, example, or workflow mentioned in the paper is present and accessible in the repository (e.g., variance_stabilizing_transformation.html, seurat.html).
- Missing signals are explicitly enumerated: changelogs, versioning history, test data availability, and undocumented parameters are clearly flagged.
- The traceability index is structured consistently (e.g., claim → tool → section → evidence) and ready for expert review without requiring additional retrieval.

## Limitations

- No changelog found in the sctransform repository, limiting ability to trace historical changes and version-specific behavior for reproducibility assessment.
- The MVP workflow does not execute the indexed code or validate computational outputs; it only maps claims to artifacts and flags gaps.
- Reproducibility context may be incomplete if key materials (test datasets, environment specifications, hardware requirements) are not mentioned in README or supplementary materials.
- Expert review signal strength depends on the completeness of repository documentation; minimally documented packages may require direct contact with authors.

## Evidence

- [other] Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information.: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information."
- [other] The finding should be confirmed by expert review; no strong finding sentence was detected heuristically.: "The finding should be confirmed by expert review; no strong finding sentence was detected heuristically."
- [readme] For usage examples see vignettes in inst/doc or use the built-in help after installation: "For usage examples see vignettes in inst/doc or use the built-in help after installation"
- [readme] Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data.: "Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data."

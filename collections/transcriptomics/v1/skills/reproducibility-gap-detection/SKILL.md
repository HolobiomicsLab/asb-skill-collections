---
name: reproducibility-gap-detection
description: Use when when evaluating a computational method described in a peer-reviewed article, particularly when the work references a public repository or provides supplementary code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0084
  - http://edamontology.org/topic_3071
  tools:
  - GitHub
  - sctransform
  - WGCNA
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

# reproducibility_gap_detection

## Summary

Detect and document gaps in scientific reproducibility by systematically reviewing article artifacts, connecting claims to available outputs, and recording missing materials or documentation. This skill identifies barriers to replicating published computational workflows.

## When to use

When evaluating a computational method described in a peer-reviewed article, particularly when the work references a public repository or provides supplementary code. Use this skill if you need to assess whether a reader could independently reproduce the reported results, or if you are curating methodological resources and must flag incomplete documentation.

## When NOT to use

- Input is a purely theoretical or mathematical paper with no computational implementation or code artifact.
- The article explicitly states code and data are not available and no repository exists.

## Inputs

- Peer-reviewed article manuscript or preprint
- Associated GitHub repository (or public code repository)
- Repository README and documentation
- Supplementary materials or vignettes

## Outputs

- Reproducibility gap report (structured list of missing signals)
- Indexed artifact inventory (tools, workflow steps, findings)
- Material availability checklist (code, data, documentation)
- Reproducibility confidence assessment

## How to apply

Review indexed article artifacts (methods, results, supplementary materials) and cross-reference them against the corresponding public repository (e.g., GitHub). Connect specific claims in the paper (e.g., 'we normalized using regularized negative binomial regression') to concrete outputs or implementation details in the repo (code, vignettes, examples). Inspect available materials for key reproducibility signals: README documentation, installation instructions, runnable code examples, test data, parameter specifications, and change logs. Document missing information systematically (e.g., 'No changelog found') and record which signals are absent or unclear. The absence of a changelog, incomplete vignettes, or missing parameter defaults are specific red flags.

## Related tools

- **GitHub** (Repository hosting and version control platform for indexing code artifacts, inspecting materials, and connecting article claims to implementation) — https://github.com/satijalab/sctransform
- **sctransform** (Example R package whose reproducibility gaps (missing changelog) were surfaced by this skill during evaluation) — https://github.com/satijalab/sctransform

## Examples

```
# Review GitHub repository for reproducibility artifacts
# Connect claim 'variance stabilization via regularized negative binomial regression' 
# to sctransform::vst() implementation in README.
# Record finding: 'No changelog found' in missing_signals inventory.
```

## Evaluation signals

- Presence of executable installation instructions (e.g., CRAN or remotes::install_github syntax) that match paper authorship.
- Runnable code examples or vignettes that reproduce reported analyses or figures mentioned in the paper.
- Clear parameter documentation matching method descriptions (e.g., 'vst.flavor' regularization versions).
- Version control history or changelog documenting updates, especially between cited references (e.g., 2019 vs. 2022 versions).
- Absence of documented gaps (e.g., 'No changelog found') in structured artifact inventory.

## Limitations

- Detection is heuristic and depends on the availability of public repositories; closed-source implementations cannot be assessed.
- Absence of a signal (e.g., no changelog) does not prove irreproducibility—only that documentation is incomplete or absent.
- Does not validate correctness of code or outputs, only completeness of reproducibility-enabling materials.
- Skill is labor-intensive in MVP form and requires expert review to confirm findings.

## Evidence

- [other] Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information.: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information. No workflow is executed in the MVP."
- [other] No changelog found.: "No changelog found  [section=discussion; evidence='No changelog found.']"
- [readme] Normalization and variance stabilization of single-cell RNA-seq data using regularized negative binomial regression.: "R package for normalization and variance stabilization of single-cell RNA-seq data using regularized negative binomial regression"
- [readme] Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data.: "Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data."
- [readme] Installation instructions from CRAN and GitHub development branch are documented.: "# Install sctransform from CRAN
install.packages("sctransform")

# Or the development version from GitHub:
remotes::install_github("satijalab/sctransform", ref="develop")"

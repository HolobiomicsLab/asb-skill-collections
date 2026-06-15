---
name: output-grounding
description: Use when when you have a scientific article describing a computational analysis, meta-analysis tool, or data processing workflow and need to verify that reported findings, output tables, or visualizations are traceable to a public repository, executable code, or documented methodology.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - GitHub
  - BinDiscover
derived_from:
- doi: 10.1186/s13321-023-00734-8
  title: bindiscover
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  dedup_kept_from: coll_bindiscover
schema_version: 0.2.0
---

# output_grounding

## Summary

Grounding of scientific outputs (claims, findings, visualizations) to concrete source artifacts (code repositories, data files, methodology documentation) to enable reproducibility assessment and traceability. This skill validates that a published claim or result can be traced to executable workflows, versioned code, and accessible data inputs.

## When to use

When you have a scientific article describing a computational analysis, meta-analysis tool, or data processing workflow and need to verify that reported findings, output tables, or visualizations are traceable to a public repository, executable code, or documented methodology. Trigger on: (1) presence of GitHub/GitLab repos cited in methods or data availability statements; (2) claims about hypothesis generation, statistical results, or feature discovery; (3) availability of source code or supplementary materials that could be inspected for alignment with claims.

## When NOT to use

- The article is a pure theory or review paper with no computational claims or no repository references.
- The source repositories are private, deleted, or behind institutional access walls and cannot be retrieved.
- The article makes only high-level conceptual claims without quantitative findings or executable workflows to ground.

## Inputs

- Scientific article text with research question and findings
- GitHub repository URL(s) and README content
- Claims, hypotheses, or output descriptions from the article

## Outputs

- Indexed artifact catalog (repositories, tool documentation, code references)
- Traceability matrix linking claims to code/data artifacts
- Gap report (missing code, undocumented workflow steps, inaccessible data)
- Reproducibility assessment (claim-to-output verification status)

## How to apply

Locate and index repository references mentioned in the article (e.g., 'metabolomics-us/bindiscover'). Retrieve and parse the repository README and code structure to identify tool purpose, input/output specifications, and workflow steps. Cross-reference the article's stated research question, methodology, and findings against the documented tool behavior and available code. Record matches (claim supported by indexed artifact), gaps (claim lacks supporting code/data), and missing materials (e.g., no deposited feature tables, no workflow script). Use GitHub URLs and README text as primary evidence. Flag findings that lack heuristically detectable supporting statements in either the article or repository documentation.

## Related tools

- **BinDiscover** (Meta-analysis tool for rapid hypothesis generation on gas chromatography / mass spectrometry sample data; serves as indexed artifact example in this skill's application) — https://github.com/metabolomics-us/bindiscover

## Evaluation signals

- All cited repositories are locatable and publicly accessible via GitHub/documentation URLs.
- README or code comments describe input file formats, parameters, and output schemas that align with article methodology.
- Key findings or claims from the article can be traced to a specific workflow step, code function, or output variable name in the indexed repository.
- Data availability statement or supplementary materials link to deposited input/output datasets or example files.
- Absence of contradictions between article claims and repository documentation (e.g., stated tool purpose matches README description).

## Limitations

- No strong finding sentence was detected heuristically in the provided MVP context; expert review is required to confirm reproducibility.
- Repository README alone may not document all parameter choices, thresholds, or filtering steps actually used in the analysis.
- Traceability cannot be confirmed if source code or intermediate outputs are not publicly deposited alongside the article.
- GitHub repository snapshots may differ from the version used at publication time if no release tag or commit hash is specified in the article.

## Evidence

- [readme] BinDiscover is a meta analysis tool that enables rapid hypothesis generation based on biological samples analyzed via gas chromatography / mass spectrometry: "BinDiscover is a meta analysis tool that enables rapid hypothesis generation based on biological samples analyzed via gas chromatography / mass spectrometry"
- [other] Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information.: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information"

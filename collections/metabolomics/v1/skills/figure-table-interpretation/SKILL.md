---
name: figure-table-interpretation
description: Use when when assessing the scientific validity and reproducibility of a computational method or tool, and the article lacks explicit workflow descriptions, methodology narratives, or clear finding statements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# figure_table_interpretation

## Summary

Systematic extraction and interpretation of findings, tool applications, and workflow decisions from scientific article figures, tables, and repository documentation to reconstruct the reproducibility and analytical context of a scientific study.

## When to use

When assessing the scientific validity and reproducibility of a computational method or tool, and the article lacks explicit workflow descriptions, methodology narratives, or clear finding statements. Use this skill to reverse-engineer method application by examining indexed artifacts (repository code, README materials, supplementary outputs) and connecting implicit claims to documented outputs.

## When NOT to use

- Input is a fully documented, peer-reviewed methods paper with explicit parameter tables and pseudocode — use direct method transcription instead.
- No indexed repository or supplementary artifacts are available; the article is text-only with no external materials to cross-reference.
- The skill is intended as a replacement for contacting authors or conducting a full re-implementation; it surfaces gaps but does not resolve them.

## Inputs

- Article package with indexed repository references
- GitHub repository URLs and README files
- Article text sections (abstract, methods, results, discussion)
- Supplementary materials and data artifacts
- Tool documentation and parameter listings

## Outputs

- Structured reproducibility assessment report
- Mapped claims-to-outputs traceability matrix
- List of missing or unavailable materials
- Identified gaps in explicit finding statements
- Workflow reconstruction (where evidence permits)

## How to apply

Review all indexed article artifacts (GitHub repositories, README documentation, supplementary materials) to identify tool mentions, workflow steps, and claimed findings. Connect stated research questions to available outputs and tool evidence. Inspect repository metadata and documentation for concrete parameter settings, input/output file formats, and analytical decisions. Record gaps between claimed findings and available supporting evidence. Document which materials are missing or incomplete, and flag sections where heuristic finding detection failed (i.e., no explicit finding sentence structure present). Ground all conclusions in verbatim evidence from the indexed sources rather than inferring methodology.

## Related tools

- **BinDiscover** (Meta-analysis tool for rapid hypothesis generation from gas chromatography/mass spectrometry metabolomics data; serves as case study for reproducibility assessment) — https://github.com/metabolomics-us/bindiscover

## Evaluation signals

- All tool mentions in the article are linked to corresponding GitHub repositories or official documentation URLs.
- For each indexed repository, README content is retrieved and cross-checked against article descriptions.
- Claimed analytical outputs (figures, tables, derived datasets) have corresponding code or configuration files in the repository.
- Gaps between research question and available evidence are explicitly listed (e.g., 'No explicit finding sentence detected' indicates incomplete reporting).
- Workflow steps are reconstructed from sequential tool applications and can be traced through both article text and repository artifacts.

## Limitations

- README and repository documentation are marked UNTRUSTED and may contain incomplete, inaccurate, or outdated descriptions of the actual method.
- The MVP workflow does not execute code or validate computational outputs; assessment is limited to document inspection.
- Absence of explicit finding sentences in article text cannot be resolved by document review alone; expert review is required for confirmation.
- Reproducibility assessment cannot fully validate method correctness without access to raw data, compute environment, and parameter values beyond what is documented.

## Evidence

- [other] Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information.: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information."
- [readme] Bindiscover is a meta analysis tool that enables rapid hypothesis generation based on biological samples analyzed via gas chromatography / mass spectrometry: "Bindiscover is a meta analysis tool that enables rapid hypothesis generation based on biological samples analyzed via gas chromatography / mass spectrometry"
- [other] The finding should be confirmed by expert review; no strong finding sentence was detected heuristically.: "The finding should be confirmed by expert review; no strong finding sentence was detected heuristically."

---
name: chemical-structure-annotation-and-export
description: Use when after executing BioTransformer's environmental microbial degradation
  module on a small-molecule input, when you need to capture predicted metabolites
  alongside the specific transformation rules applied and degradation pathway information
  in a format suitable for subsequent analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2814
  tools:
  - BioTransformer
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab). Env. module data CC-BY-NC-SA (enviPath/EAWAG).
    url: https://bitbucket.org/wishartlab/biotransformer.git
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-019-0375-2
  title: BioTransformer 1.0
evidence_spans:
- This is version 3.0.0 of BioTransformer. BioTransformer is a software tool that
  predicts small molecule metabolism
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_1_0_2_cq
    doi: 10.1186/s13321-019-0375-2
    title: BioTransformer 1.0
  dedup_kept_from: coll_biotransformer_1_0_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-019-0375-2
  all_source_dois:
  - 10.1186/s13321-019-0375-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-annotation-and-export

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Export predicted metabolite structures and their associated biotransformation annotations from BioTransformer's environmental microbial degradation module into a structured output file. This skill enables systematic capture and organization of metabolism prediction results for downstream metabolite identification and pathway analysis.

## When to use

After executing BioTransformer's environmental microbial degradation module on a small-molecule input, when you need to capture predicted metabolites alongside the specific transformation rules applied and degradation pathway information in a format suitable for subsequent analysis, comparison, or publication.

## When NOT to use

- Input is mammalian or gut microbiota metabolism predictions rather than soil/aquatic microbial degradation; use the appropriate BioTransformer module instead.
- You have only a single predicted metabolite or do not need systematic organization; manual documentation may be more efficient.
- The downstream tool expects a different schema or metabolite representation format not supported by the export step.

## Inputs

- predicted metabolites from BioTransformer environmental microbial degradation module execution
- transformation rules applied (from EAWAG-BBD or EnviPath)
- degradation pathway information

## Outputs

- structured output file listing predicted metabolites with chemical structures
- transformation rule annotations per metabolite
- degradation pathway annotations per metabolite

## How to apply

Following retrieval of predicted metabolites from the EAWAG-BBD and EnviPath metabolic transformation data, systematically format the output to include three components for each predicted metabolite: (1) chemical structure (typically as SMILES or MOL format), (2) the specific transformation rule(s) applied by BioTransformer, and (3) the degradation pathway annotation. Export this annotated data as a structured output file (e.g., CSV, JSON, or SDF with metadata fields) that preserves the linkage between structure, rule, and pathway. The choice of export format should depend on downstream use—SDF with embedded metadata for visualization tools, CSV for tabular analysis, or JSON for computational integration.

## Related tools

- **BioTransformer** (Predicts small-molecule metabolism and generates metabolite structures and transformation rules for the environmental microbial degradation module) — bitbucket.org/wishartlab/biotransformer

## Evaluation signals

- Output file is well-formed and parseable in its declared format (CSV, JSON, SDF, etc.)
- Each predicted metabolite entry contains all three required components: structure, transformation rule(s), and pathway annotation
- Chemical structures in output are valid and represent distinct molecular entities
- Transformation rule annotations are traceable to EAWAG-BBD or EnviPath identifiers or rule names
- Row/entry count in output matches the number of unique predicted metabolites returned by BioTransformer

## Limitations

- Export fidelity depends on BioTransformer's completeness of metadata export; some transformation metadata may be lost if BioTransformer does not expose it in programmatic output.
- Degradation pathway annotations from EAWAG-BBD may be incomplete or absent for novel or understudied compounds, limiting the utility of pathway-level annotations.
- No changelog available for BioTransformer versions, making it difficult to assess whether export format or annotation completeness has changed between releases.

## Evidence

- [other] Retrieve predicted metabolites, including chemical structures, transformation rules applied, and degradation pathway information.: "Retrieve predicted metabolites, including chemical structures, transformation rules applied, and degradation pathway information."
- [other] Format and export the prediction results as a structured output file listing all predicted metabolites with their structures and transformation annotations.: "Format and export the prediction results as a structured output file listing all predicted metabolites with their structures and transformation annotations."
- [intro] BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database: "BioTransformer's environmental microbial degradation module uses data from the EAWAG's Biodegradation and Biocatalysis Database"
- [intro] BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction: "BioTransformer also assists scientists in metabolite identification, based on the metabolism prediction"

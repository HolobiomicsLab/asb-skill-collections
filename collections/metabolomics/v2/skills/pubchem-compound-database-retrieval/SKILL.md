---
name: pubchem-compound-database-retrieval
description: Use when you need to supply candidate metabolite structures for mass spectrometry annotation when working within an integrative metabolomics data analysis workflow (such as MAGMa).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3095
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MAGMa
  - PubChem
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma_cq
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pubchem-compound-database-retrieval

## Summary

Extract, parse, and standardize chemical structures from the PubChem database to generate a validated candidate structure set for metabolite annotation workflows. This skill bridges public chemical data repositories with chemo-informatics pipelines by ensuring structural compatibility and format compliance.

## When to use

You need to supply candidate metabolite structures for mass spectrometry annotation when working within an integrative metabolomics data analysis workflow (such as MAGMa). Apply this skill when your metabolite identification pipeline requires a curated, standardized lookup database of known compounds indexed by molecular mass or other chemical properties.

## When NOT to use

- Your metabolite annotation workflow already includes a pre-built, validated structure database—skip direct PubChem retrieval and validation.
- You are working with a specialized metabolite subset (e.g., only lipids, only natural products) that requires a domain-specific repository instead of the full PubChem dataset.
- Real-time structure lookup is required; batch pre-processing and static database export are insufficient for your use case.

## Inputs

- PubChem compound records (via API or bulk download)
- Target annotation tool specification (e.g., MAGMa job input format requirements)
- Filtering criteria (optional: mass range, structure class, data completeness threshold)

## Outputs

- Standardized candidate structure database
- Indexed lookup table (compound ID → molecular properties)
- Processed structures in tool-specific format (e.g., MAGMa-compatible structure file)

## How to apply

Begin by extracting and parsing compound records from the public PubChem database using available PubChem APIs or bulk download facilities. Filter and standardize the retrieved chemical structures to ensure compatibility with your downstream annotation tool's expected input format (e.g., MAGMa's structure representation). Generate or compile candidate structure identifiers and relevant molecular properties (e.g., exact mass, molecular formula, InChI). Validate the processed candidate set for completeness (coverage of expected mass ranges) and format compliance (schema adherence, required fields present). Finally, export the validated structures in the format required by your job calculation pipeline—this intermediate database becomes the lookup resource for candidate mass matching during annotation.

## Related tools

- **MAGMa** (Accepts standardized candidate structures for MS annotation and in silico metabolite matching) — https://github.com/NLeSC/MAGMa
- **PubChem** (Source database from which compound records are extracted and parsed)

## Evaluation signals

- All exported structures conform to the target tool's input schema (e.g., required fields, allowed stereochemistry formats).
- Molecular properties (exact mass, molecular formula) are internally consistent and chemically valid.
- The candidate set includes expected mass range coverage (e.g., no large gaps in m/z bins relevant to the experimental data).
- Duplicate or redundant structures are eliminated; structure IDs are unique and traceable to PubChem source records.
- Format validation passes without error when ingested by the downstream annotation job (e.g., MAGMa job launcher accepts the structure file).

## Limitations

- PubChem includes structures of varying experimental validation quality; no filtering by experimental evidence level is applied in the base workflow.
- Standardization may alter or lose stereochemical information if the target tool does not support full 3D structure representation.
- Mass-based candidate filtering requires precomputation; real-time queries against the full PubChem dataset are not addressed by this batch-oriented skill.
- The workflow does not explicitly address PubChem record updates or versioning—reproducibility depends on archiving the export date and record subset used.

## Evidence

- [other] The workflow and rationale for structure extraction and standardization: "Extract and parse PubChem compound records from the public PubChem database. 2. Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline. 3. Generate or"
- [readme] Project context and role of PubChem processing: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [readme] Broader scientific context of metabolite identification: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [other] Subproject purpose in the eMetabolomics workflow: "The eMetabolomics project includes a pubchem subproject as one of its component subprojects that processes PubChem data to supply candidate structures for the metabolite identification workflow."

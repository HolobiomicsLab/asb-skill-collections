---
name: annotation-pipeline-data-preparation
description: Use when when you have raw PubChem compound records or other public chemical structure databases and need to supply candidate metabolite structures to a mass spectrometry annotation workflow like MAGMa.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - MAGMa
  - pubchem (subproject)
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

# annotation-pipeline-data-preparation

## Summary

Prepare and standardize chemical structure data from public databases (PubChem) into a validated candidate set formatted for metabolite annotation pipelines (MAGMa). This skill bridges raw compound record extraction and annotation-ready structure libraries by filtering, standardizing molecular representations, and validating schema compliance.

## When to use

When you have raw PubChem compound records or other public chemical structure databases and need to supply candidate metabolite structures to a mass spectrometry annotation workflow like MAGMa. Specifically: you are starting a metabolite identification project, you have liquid chromatography–mass spectrometry (LC-MS) data without pre-filtered candidates, and you need to generate or compile a validated lookup database that MAGMa's in silico annotation engine can query by mass and chemical properties.

## When NOT to use

- Input is already a curated, experiment-specific metabolite reference library (skip to direct annotation rather than re-standardizing).
- You have in vitro or synthetic standards data from a standards repository with guaranteed quality control (PubChem may introduce spurious or outdated structures).
- The annotation tool does not require a pre-built candidate database and instead queries PubChem or other public APIs on-the-fly during annotation.

## Inputs

- PubChem compound records (raw database dump or API export)
- chemical structure file (SDF, MOL, SMILES, or InChI format)
- PubChem identifiers (CID list or batch export)

## Outputs

- validated candidate structure library (format compatible with MAGMa)
- candidate structure identifiers with molecular properties
- PubChem lookup database (binary or indexed format for MAGMa job calculation)

## How to apply

Extract and parse PubChem compound records from the public PubChem database using the PubChem API or bulk downloads. Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline—this includes normalizing molecular representations, removing duplicates, and reconciling stereochemistry and ionization states. Generate or compile candidate structure identifiers and molecular properties (e.g., monoisotopic mass, formula, InChI). Validate the candidate set for completeness (no missing critical fields) and format compliance against MAGMa's expected input schema. Finally, export the processed candidate structures to the binary or text format required by MAGMa job calculation. The rationale is that MAGMa's accuracy depends on the quality and coverage of its input candidate pool; standardization ensures structures are correctly parseable by the annotation engine and reduces false negatives in metabolite identification.

## Related tools

- **MAGMa** (annotation engine that consumes the standardized candidate structure library to perform MS annotation based on in silico generated metabolites) — https://github.com/NLeSC/MAGMa
- **pubchem (subproject)** (processes and standardizes PubChem database into candidate structure lookup for MAGMa) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- All candidate structures parse without error in MAGMa's input validator; no malformed SMILES, InChI, or chemical structure files.
- Molecular property fields (mass, formula, charge state) are populated for ≥95% of candidates; missing values are logged and reviewed.
- Duplicate structures (identical InChI or canonicalized SMILES) are identified and deduplicated; candidate set size is stable across re-runs.
- Candidate set completeness: coverage of known endogenous metabolites in a test organism (e.g., humans, model organism) is ≥80% based on reference metabolome (e.g., HMDB, KEGG).
- MAGMa job runs successfully on annotated spectra using the prepared candidate library with no schema or format errors; annotation hit rates (identified compounds per spectrum) are within expected range for instrument and organism.

## Limitations

- PubChem contains both curated and user-submitted structures; data quality and chemical accuracy vary; deprecated or erroneous structures may persist.
- Standardization decisions (e.g., protonation state, stereochemistry resolution) are lossy; some chemical information may be discarded to ensure pipeline compatibility.
- Large-scale PubChem exports (millions of compounds) can be computationally expensive to parse and filter; filtering and standardization steps may need parallelization or incremental processing.
- MAGMa annotation accuracy depends on the candidate pool; incomplete or biased PubChem subsets (e.g., excluding rare metabolites or non-human organisms) may miss true metabolite identifications.

## Evidence

- [readme] pubchem subproject processes PubChem data: "pubchem - Processing of PubChem database, used to find mass candidates"
- [other] workflow steps for candidate preparation: "Extract and parse PubChem compound records from the public PubChem database. 2. Filter and standardize chemical structures to ensure compatibility with MAGMa's annotation pipeline. 3. Generate or"
- [readme] MAGMa dependency on pubchem module: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [readme] project goal in metabolite identification: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."

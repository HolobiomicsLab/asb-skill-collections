---
name: knowledge-graph-generation-and-validation
description: Use when after completing all per-sample annotation steps (molecular networking, ISDB/spectral matching, SIRIUS/CSI:FingerID, and compounds metadata enhancement with Wikidata IDs and NPClassifier ontology).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2258
  tools:
  - ENPKG
  - ENPKG graph builder
  - GraphDB
  - Open Tree of Life (OTT)
  - Wikidata
  - NPClassifier
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# knowledge-graph-generation-and-validation

## Summary

Construct a sample-specific RDF knowledge graph by integrating metabolomics annotations, taxonomic metadata, and structural predictions, then validate graph integrity and schema compliance before merging with existing knowledge bases. This skill bridges processed experimental data (molecular networks, spectral matches, SIRIUS predictions) into a queryable, Wikidata-connected semantic resource suitable for multi-sample comparative analysis.

## When to use

Apply this skill after completing all per-sample annotation steps (molecular networking, ISDB/spectral matching, SIRIUS/CSI:FingerID, and compounds metadata enhancement with Wikidata IDs and NPClassifier ontology). Use when the goal is to integrate heterogeneous metabolomics outputs into a unified, SPARQL-queryable knowledge graph that can be merged with other samples or external knowledge bases, or when you need to enable cross-sample queries on spectral fingerprints, taxonomic provenance, and chemical structure relationships.

## When NOT to use

- Input data are not yet fully annotated (e.g., raw spectral features lack molecular network assignment or structural predictions). Complete annotation steps first.
- Sample metadata does not include verified taxon information or has unresolved taxonomy against Open Tree of Life. Taxonomic enhancement must precede graph construction.
- The objective is exploratory data visualization of a single sample's spectra or molecular network in isolation; use MZmine outputs or Cytoscape instead of building a full knowledge graph.

## Inputs

- Feature table with detected compounds and intensity values
- Molecular network edges (cosine similarity adjacency data)
- Spectral matches to in silico database (ISDB) with taxonomic reweighting scores
- SIRIUS/CSI:FingerID structural predictions (formula, fingerprint, CANOPUS class probabilities)
- Sample metadata (originating taxon, collection site, processing date)
- Compound metadata with resolved Wikidata IDs and NPClassifier ontology classes
- Optional: ChEMBL bioactivity records for annotated compounds

## Outputs

- Sample-specific RDF knowledge graph (TTL serialization)
- Named graph triples integrating spectral, structural, taxonomic, and bioactivity data
- Graph validation report (schema compliance, integrity checks, entity coverage statistics)
- SPARQL-queryable knowledge graph compatible with GraphDB import

## How to apply

Aggregate all processed annotation outputs for a given sample (feature tables with molecular network, spectral matches to in silico databases with taxonomic reweighting scores, SIRIUS/CANOPUS predictions, and compound metadata including Wikidata IDs, NPClassifier classes, and optional ChEMBL bioactivity links) into a structured intermediate representation. Use the ENPKG graph builder to translate this heterogeneous data into RDF triples following the ENPKG vocabulary schema, creating sample-specific named graphs that encode sample metadata (taxon, collection provenance), spectral observations, chemical structures, and their external cross-references. Validate the generated RDF/TTL files for: (1) graph syntax correctness and subject–predicate–object triple well-formedness; (2) schema compliance against the ENPKG vocabulary (presence of required predicates, correct data types, valid URIs for external resources); (3) logical consistency (no orphaned nodes, proper cardinality of relationships, taxonomy resolution against Open Tree of Life and Wikidata); and (4) data completeness relative to input annotations (spot-check that high-confidence features from molecular networking are represented, that spectral library matches include reweighting scores, and that all annotated compounds have resolved Wikidata and NPClassifier entries). The resulting graph is then suitable for import into GraphDB or similar RDF stores and for merging with sample-independent knowledge layers (e.g., ChEMBL bioactivity networks).

## Related tools

- **ENPKG graph builder** (Translates aggregated annotation outputs (features, spectra, predictions, metadata) into RDF triples and encodes them according to ENPKG vocabulary schema) — https://github.com/enpkg/enpkg_graph_builder
- **GraphDB** (RDF triple store for importing, validating, and querying generated knowledge graphs via SPARQL) — https://graphdb.ontotext.com/download/
- **Open Tree of Life (OTT)** (Validates and resolves sample taxonomy to ottID, ensuring consistent taxon linking across graph instances) — https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5
- **Wikidata** (External URI source for compound identifiers and chemical metadata integrated into graph entities) — https://www.wikidata.org/wiki/Wikidata:Main_Page
- **NPClassifier** (Provides natural product classification ontology integrated into compound metadata within the graph) — https://npclassifier.ucsd.edu/

## Examples

```
bash workflow/00_workflow_all.sh
```

## Evaluation signals

- RDF/TTL file syntax is valid (can be parsed without errors; all triples have subject, predicate, object with correct URI or literal formatting)
- Graph schema compliance: all sample entities include required metadata predicates (originating taxon, sample provenance); all features are linked to molecular network, spectral matches, and structural predictions; all compounds resolve to Wikidata IDs and NPClassifier classes
- Referential integrity: no orphaned subject URIs; all inter-triple links are consistent (e.g., feature nodes link to valid network edges; network edges link to features with consistent cosine similarity scores)
- Data completeness relative to input: percentage of features from molecular network represented in graph; percentage of annotated compounds with resolved Wikidata and NPClassifier entries; presence of reweighting scores for all ISDB matches
- Graph can be successfully imported into GraphDB and queried via SPARQL without timeouts; sample-specific queries on taxon, spectral similarity, or chemical structure return expected results

## Limitations

- Graph generation assumes all prior annotation steps (taxonomic enhancement, molecular networking, ISDB/spectral matching with reweighting, SIRIUS/CSI:FingerID) have been completed with high-confidence outputs. Missing or low-confidence annotations will result in sparse or incomplete graph layers.
- The RDF schema is tightly coupled to the ENPKG vocabulary; any changes to annotation workflows or external resources (e.g., updated Wikidata mappings, new NPClassifier versions) may require schema updates or data remapping.
- Multi-sample graph merging requires careful namespace management and entity reconciliation (e.g., identical compounds detected in different samples must be unified as single nodes); no automated deduplication is provided in the current workflow.
- SPARQL query performance on very large graphs (thousands of samples, millions of features) may degrade; the documentation does not specify benchmarks or optimization strategies for large-scale deployments.
- Validation signals depend on external service availability (Open Tree of Life, Wikidata, NPClassifier, ChEMBL); network outages or API changes during graph construction may cause missing or stale annotations.

## Evidence

- [readme] Finally, all of the data previously generated is integrated into a sample-specific RDF knowledge graph.: "Finally, all of the data previously generated is integrated into a sample-specific RDF knowledge graph."
- [readme] These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data.: "These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data."
- [readme] The graph structure allow for optimal query using the SPARQL language and is fully compatible for subsequent addition of samples.: "The graph structure allow for optimal query using the SPARQL language and is fully compatible for subsequent addition of samples."
- [readme] 5) Graph building: Build a knowledge graph for each sample integrating the data generated above.: "5) Graph building: Build a knowledge graph for each sample integrating the data generated above."
- [full_text] Validate the final annotated output files (molecular annotations, spectral matches, knowledge-graph triples) against the expected output schema and integrity checks.: "Validate the final annotated output files (molecular annotations, spectral matches, knowledge-graph triples) against the expected output schema and integrity checks."
- [readme] You can use GraphDB to explore the generated Knowledge Graph. To do so, you will need to install GraphDB and import the generated .ttl files.: "You can use GraphDB to explore the generated Knowledge Graph. To do so, you will need to install GraphDB and import the generated .ttl files."

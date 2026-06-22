---
name: natural-products-workflow-orchestration
description: Use when you have LC-MS/MS DDA metabolomics data (positive and/or negative ionization modes) and sample metadata (originating taxon) for one or more samples, and you need to generate a Wikidata-connected RDF knowledge graph for integrated natural products analysis, taxonomy-aware compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ENPKG
  - MZmine
  - Sirius/CSI:FingerID/CANOPUS
  - Open Tree of Life
  - NPClassifier
  - ChEMBL
  - Wikidata
  - GraphDB
  - enpkg_full
  - enpkg_data_organization
  - enpkg_taxo_enhancer
  - enpkg_mn_isdb_taxo
  - enpkg_sirius_canopus
  - enpkg_meta_analysis
  - enpkg_graph_builder
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-products-workflow-orchestration

## Summary

Execute the ENPKG full computational workflow to transform raw LC-MS/MS metabolomics data into sample-specific RDF knowledge graphs integrated with taxonomic, chemical, and activity metadata. This skill chains sample-level processing (taxonomy resolution, molecular networking, spectral/structure annotation) with knowledge-graph construction to enable SPARQL-queryable linked data on natural products.

## When to use

You have LC-MS/MS DDA metabolomics data (positive and/or negative ionization modes) and sample metadata (originating taxon) for one or more samples, and you need to generate a Wikidata-connected RDF knowledge graph for integrated natural products analysis, taxonomy-aware compound annotation, or downstream SPARQL querying and cross-sample comparison.

## When NOT to use

- Input data are already processed into a knowledge graph or RDF triples — use this skill only on raw or MZmine-processed LC-MS/MS data.
- Sample metadata does not include or cannot be resolved to a taxonomic origin — the workflow requires valid taxon input for Open Tree of Life integration.
- You need only spectral feature detection or molecular networking without knowledge-graph integration or linked-data annotation — use individual ENPKG sub-workflows (e.g., enpkg_mn_isdb_taxo) instead.

## Inputs

- LC-MS/MS DDA raw data files (positive and/or negative ionization modes)
- Sample metadata file with originating taxon information
- MZmine-processed feature tables (from preceding MZmine step)
- params/user.yml configuration file (dataset record_id, record_name, processing parameters)

## Outputs

- Sample-specific RDF knowledge graph (.ttl files)
- Annotated feature table with spectral and structural identifications
- Molecular network (MN) files
- Wikidata IDs and NPClassifier ontology mappings for compounds
- SPARQL-queryable graph compatible with GraphDB or equivalent triple stores

## How to apply

Clone the enpkg_full repository and install dependencies using uv (Python 3.11+). Configure the .env file with absolute paths to the Sirius executable and account credentials, and edit params/user.yml to specify the input dataset (e.g., Zenodo record ID for test data). Place raw LC-MS/MS DDA files and minimal sample metadata (originating taxon) in the designated input directory following the expected directory structure. Execute the full workflow orchestrator (workflow/00_workflow_all.sh), which automatically sequences data organization, taxonomical enhancement (via Open Tree of Life ottID resolution), MZmine processing, molecular network generation, dual annotation (spectral matching to in silico DB with taxonomical reweighting and Sirius/CSI:FingerID), Wikidata ID retrieval, NPClassifier ontology annotation, and final RDF knowledge-graph construction. Monitor logs for successful completion of all intermediate steps and validate output .ttl files against the expected RDF schema and graph structure integrity.

## Related tools

- **MZmine** (Feature detection and peak picking from LC-MS/MS DDA raw data) — http://mzmine.github.io/
- **Sirius/CSI:FingerID/CANOPUS** (In silico structure annotation and molecular fingerprinting for spectral features) — https://boecker-lab.github.io/docs.sirius.github.io/install/
- **Open Tree of Life** (Taxonomic resolution and standardization of sample origin taxa to ottID) — https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5
- **NPClassifier** (Ontological classification of natural product structures) — https://npclassifier.ucsd.edu/
- **ChEMBL** (Optional: retrieve compounds with reported bioactivity against biological targets) — https://www.ebi.ac.uk/chembl/
- **Wikidata** (Linked-data chemical and taxonomic identifiers integrated into the knowledge graph) — https://www.wikidata.org/wiki/Wikidata:Main_Page
- **GraphDB** (RDF triple store for loading, querying, and exploring the final knowledge graph via SPARQL) — https://graphdb.ontotext.com/download/
- **enpkg_full** (Master orchestrator repository that coordinates all sub-workflows into a single end-to-end pipeline) — https://github.com/enpkg/enpkg_full
- **enpkg_data_organization** (Organize MZmine output into per-sample folder structure) — https://github.com/enpkg/enpkg_data_organization
- **enpkg_taxo_enhancer** (Resolve and link sample taxa to Wikidata via Open Tree of Life) — https://github.com/enpkg/enpkg_taxo_enhancer
- **enpkg_mn_isdb_taxo** (Generate molecular networks and perform spectral-matching annotation with taxonomical reweighting) — https://github.com/enpkg/enpkg_mn_isdb_taxo
- **enpkg_sirius_canopus** (Execute Sirius/CSI:FingerID/CANOPUS annotation on each sample) — https://github.com/enpkg/enpkg_sirius_canopus
- **enpkg_meta_analysis** (Retrieve NPClassifier and Wikidata IDs for annotated compounds; optional ChEMBL integration) — https://github.com/enpkg/enpkg_meta_analysis
- **enpkg_graph_builder** (Construct the sample-specific RDF knowledge graph integrating all upstream results) — https://github.com/enpkg/enpkg_graph_builder

## Examples

```
cd enpkg_full && uv sync && set -a && source .env && set +a && sh workflow/00_workflow_all.sh
```

## Evaluation signals

- All six core workflow steps complete without critical errors: data organization, taxonomical enhancement, MN/ISDB annotation, Sirius/CSI:FingerID/CANOPUS, metadata enhancement, and graph building.
- Output .ttl RDF files conform to the ENPKG vocabulary schema and pass RDF syntax validation (e.g., via rapper or GraphDB import).
- Molecular network contains expected number of nodes (spectral features) and edges; feature annotations match the input LC-MS/MS feature count with no >20% loss.
- SPARQL queries over the loaded knowledge graph return non-empty result sets for expected patterns (e.g., samples linked to taxa via ottID, compounds linked to Wikidata IDs, spectral matches with confidence scores).
- Multi-sample knowledge graphs can be merged without URI/namespace conflicts, and cross-sample SPARQL queries execute without errors.

## Limitations

- Workflow is sample-centric: each sample is processed individually; merging large numbers of samples into a single KG may require additional optimization and SPARQL federation tuning.
- Taxonomical resolution depends on valid input taxa resolvable against Open Tree of Life (ott3.5); unrecognized or misspelled taxa will fail enhancement.
- Sirius/CSI:FingerID annotation requires a valid Sirius license and account credentials; community licenses may have feature or database limitations.
- Spectral matching quality depends on the completeness and accuracy of the in silico database (ISDB); rare or novel metabolites may not be annotated.
- Knowledge graph query performance scales with total number of samples and compounds; very large collections (>5000 samples) may benefit from partitioning or federation strategies not detailed in the current documentation.

## Evidence

- [readme] The **Experimental Natural Products Knowledge Graph** workflow aims at integrating experimental LC-MS/MS DDA metabolomics data into a Wikidata-connected knowledge graph.: "The **Experimental Natural Products Knowledge Graph** workflow aims at integrating experimental LC-MS/MS DDA metabolomics data into a Wikidata-connected knowledge graph."
- [readme] For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes).: "For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes)."
- [readme] After [MZmine](http://mzmine.github.io/) processing, the workflow automatically resolves the species taxonomy against [Open Tree of Life](https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5) (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates features using two different methods (spectral matching to *in silico* DB coupled to taxonomical reweighting and [Sirius/CSI:FingerID](https://bio.informatik.uni-jena.de/software/sirius/)).: "After [MZmine](http://mzmine.github.io/) processing, the workflow automatically resolves the species taxonomy against [Open Tree of Life](https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5)"
- [readme] Finally, all of the data previously generated is integrated into a sample-specific [RDF knowledge graph](https://en.wikipedia.org/wiki/Knowledge_graph). These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data.: "Finally, all of the data previously generated is integrated into a sample-specific [RDF knowledge graph](https://en.wikipedia.org/wiki/Knowledge_graph)."
- [readme] This guide will walk you through the installation, setup, and execution of the ENPKG full workflow.: "This guide will walk you through the installation, setup, and execution of the ENPKG full workflow."
- [readme] sh workflow/00_workflow_all.sh: "From the root of the repository, run: sh workflow/00_workflow_all.sh"
- [other] ENPKG full workflow comprises three primary operational stages: installation, setup, and execution, which together transform raw input into annotated outputs ready for knowledge-graph integration.: "ENPKG full workflow comprises three primary operational stages: installation, setup, and execution, which together transform raw input into annotated outputs ready for knowledge-graph integration."

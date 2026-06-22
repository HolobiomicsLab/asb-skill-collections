---
name: sample-centric-metabolite-annotation
description: Use when after MZmine feature detection and molecular networking on a single LC-MS/MS DDA sample, when you have a feature table (with retention time, m/z, fragmentation spectra) and sample-level taxonomical metadata, and you want to assign both spectral identity and predicted chemical structure to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - ENPKG
  - MZmine
  - enpkg_mn_isdb_taxo
  - enpkg_sirius_canopus
  - enpkg_meta_analysis
  - SIRIUS
  - Open Tree of Life
  - Wikidata
  - NPClassifier
  - ChEMBL
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

# Sample-Centric Metabolite Annotation

## Summary

Annotate LC-MS/MS metabolites within individual samples using parallel spectral matching (ISDB with taxonomical reweighting) and structure prediction (SIRIUS/CSI:FingerID/CANOPUS), then enrich annotations with Wikidata IDs and NPClassifier ontology. This skill processes each sample independently to enable iterative knowledge-graph assembly.

## When to use

After MZmine feature detection and molecular networking on a single LC-MS/MS DDA sample, when you have a feature table (with retention time, m/z, fragmentation spectra) and sample-level taxonomical metadata, and you want to assign both spectral identity and predicted chemical structure to observed features before integrating them into a knowledge graph.

## When NOT to use

- Input spectral data has not been processed by MZmine (feature detection, peak alignment, and deconvolution must precede annotation).
- Sample taxon is unknown or cannot be resolved against Open Tree of Life; taxonomical reweighting will not improve annotation accuracy.
- You only have MS1 precursor masses without fragmentation spectra; ISDB and SIRIUS both require MS/MS fragmentation data.

## Inputs

- MZmine feature table (containing m/z, retention time, feature intensity across samples)
- LC-MS/MS fragmentation spectra in mzML or mzXML format
- Sample metadata file with originating taxon (resolved to Open Tree of Life ottID)
- Molecular network file (GraphML or similar from MZmine)
- SIRIUS executable (absolute path to binary) and valid Sirius account credentials

## Outputs

- Annotated feature table with ISDB matches (compound name, InChI, cosine similarity score)
- SIRIUS/CSI:FingerID predictions with confidence scores and CANOPUS chemical class assignments
- Unified compound metadata table with Wikidata IDs, NPClassifier taxonomy, and ChEMBL activity flags
- RDF triples for knowledge graph integration (sample-specific compound assertions)
- Annotation report with matching statistics and reweighting confidence metrics

## How to apply

Run the ENPKG annotation workflow on each sample individually: (1) execute enpkg_mn_isdb_taxo to perform molecular networking, ISDB spectral matching, and taxonomical/chemical consistency reweighting on the feature set; (2) execute enpkg_sirius_canopus to run SIRIUS/CSI:FingerID/CANOPUS for de novo structure prediction and NPClassifier assignment on unannotated or high-confidence features; (3) execute enpkg_meta_analysis to retrieve Wikidata IDs and NPClassifier ontology terms for all annotated compounds, creating a unified annotation table. The order matters: spectral matching (ISDB) coupled to taxonomical filtering should precede de novo prediction (SIRIUS) to avoid redundant computation. Use the sample's resolved taxon ID (from enpkg_taxo_enhancer) as input to the reweighting step to increase annotation confidence for plausible natural products.

## Related tools

- **MZmine** (Prerequisite feature detection and molecular networking; ENPKG annotation begins downstream of MZmine output.) — http://mzmine.github.io/
- **enpkg_mn_isdb_taxo** (Executes molecular networking, ISDB spectral matching, and taxonomical/chemical consistency reweighting for the sample.) — https://github.com/enpkg/enpkg_mn_isdb_taxo
- **enpkg_sirius_canopus** (Runs SIRIUS/CSI:FingerID/CANOPUS for de novo structure prediction and natural product classification.) — https://github.com/enpkg/enpkg_sirius_canopus
- **enpkg_meta_analysis** (Retrieves Wikidata IDs, NPClassifier taxonomy, and optionally ChEMBL activity data for annotated compounds.) — https://github.com/enpkg/enpkg_meta_analysis
- **SIRIUS** (Underlying tool for CSI:FingerID molecular fingerprinting and CANOPUS natural product classification; must be installed locally.) — https://boecker-lab.github.io/docs.sirius.github.io/install/
- **Open Tree of Life** (Taxonomical reference for resolving sample origin taxon to ottID; provides consistent taxonomy for reweighting.) — https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5
- **Wikidata** (External linked-data source for compound identifiers and metadata enrichment.) — https://www.wikidata.org/wiki/Wikidata:Main_Page
- **NPClassifier** (Natural product ontology used to classify annotated compounds by structural family and bioactivity potential.) — https://npclassifier.ucsd.edu/
- **ChEMBL** (Optional bioactivity database for filtering or prioritizing annotated compounds with reported biological activity.) — https://www.ebi.ac.uk/chembl/

## Examples

```
bash src/install_sirius.sh /opt/sirius && source .env && uv run enpkg_mn_isdb_taxo --input sample_features.csv --metadata sample_taxon.yaml --output annotated_features.csv
```

## Evaluation signals

- Verify that all detected features with m/z and retention time are matched against ISDB; check annotation coverage (% of features with cosine similarity > 0.7 threshold, if specified in reweighting config).
- For SIRIUS predictions, confirm that confidence scores (e.g., CSI:FingerID probability or CANOPUS predicted class probability) meet the workflow's acceptance threshold and are recorded in the output table.
- Cross-validate ISDB and SIRIUS annotations: features annotated by both methods should show structural consistency (e.g., same or closely related InChI); large divergences may indicate poor spectral quality or misassignment.
- Check that Wikidata IDs and NPClassifier ontology terms are successfully attached to all annotated compounds; absence of enrichment metadata indicates API failure or missing compound records.
- Validate RDF triples against the ENPKG vocabulary schema (ontology at https://enpkg.commons-lab.org/doc/index.html); verify that sample-compound assertions include appropriate confidence or provenance metadata.
- Confirm that the sample-specific annotation output is compatible with downstream knowledge-graph builder (enpkg_graph_builder) by checking file format and required column names.

## Limitations

- Annotation accuracy depends critically on the quality and completeness of ISDB spectral library and SIRIUS model coverage; natural products not represented in either database will remain unannotated.
- Taxonomical reweighting assumes the sample taxon is correctly identified and resolved to Open Tree of Life; misidentified or extinct taxa will not improve annotation specificity.
- SIRIUS predictions require significant computational resources and valid commercial license credentials (Sirius account); inference time scales nonlinearly with the number of unannotated features.
- Wikidata and ChEMBL enrichment depend on external API availability and compound name harmonization; rate limiting or network failures may cause incomplete metadata retrieval.
- The workflow is designed for individual sample processing; batch effects, ion suppression, or contamination within a sample are not addressed by annotation and will propagate into the knowledge graph.

## Evidence

- [readme] For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes).: "For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes)."
- [readme] After MZmine processing, the workflow automatically resolves the species taxonomy against Open Tree of Life (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates features using two different methods (spectral matching to in silico DB coupled to taxonomical reweighting and Sirius/CSI:FingerID).: "After MZmine processing, the workflow automatically resolves the species taxonomy against Open Tree of Life (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates"
- [readme] Once the processing on individual samples is done, for annotated compounds, Wikidata ID and NPClassifier ontology is automatically retrieved and it is possible to integrate compounds with activity reported against one (or more) selected biological target in ChEMBL DB.: "Once the processing on individual samples is done, for annotated compounds, Wikidata ID and NPClassifier ontology is automatically retrieved and it is possible to integrate compounds with activity"
- [readme] To allow for iterative addition of samples over time, data from each sample is processed individually.: "To allow for iterative addition of samples over time, data from each sample is processed individually."
- [readme] These steps needs to be run only once for each sample. 🚀 1) Organize data ... 2) Taxonomical enhancement ... 3) MN, ISDB annotation and taxonomical/chemical consistency reweighting ... 4) SIRIUS/CSI:FingerID/CANOPUS annotation ... 5) Compounds metadata enhancement: "3) MN, ISDB annotation and taxonomical/chemical consistency reweighting on each sample. Repository: https://github.com/enpkg/enpkg_mn_isdb_taxo 4) SIRIUS/CSI:FingerID/CANOPUS annotation. Aim: Perform"

---
name: spectral-data-processing-and-annotation
description: Use when when you have raw LC-MS/MS DDA spectral data (positive and/or negative ionization modes) paired with sample metadata (originating taxon), and you need to detect molecular features, build a molecular network from fragmentation spectra, and annotate those features using both spectral.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - ENPKG
  - MZmine
  - Sirius/CSI:FingerID/CANOPUS
  - Open Tree of Life
  - Wikidata
  - NPClassifier
  - ChEMBL
  - enpkg_data_organization
  - enpkg_taxo_enhancer
  - enpkg_mn_isdb_taxo
  - enpkg_sirius_canopus
  - enpkg_meta_analysis
  - enpkg_graph_builder
  - ENPKG Full Workflow
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
---

# spectral-data-processing-and-annotation

## Summary

End-to-end processing of LC-MS/MS DDA metabolomics data through feature detection, molecular networking, and multi-method compound annotation to produce knowledge-graph-ready annotated outputs. This skill transforms raw mass spectrometry and metadata inputs into structurally and taxonomically contextualized molecular annotations.

## When to use

When you have raw LC-MS/MS DDA spectral data (positive and/or negative ionization modes) paired with sample metadata (originating taxon), and you need to detect molecular features, build a molecular network from fragmentation spectra, and annotate those features using both spectral matching and ab initio structure prediction methods to integrate into a knowledge graph.

## When NOT to use

- Input data are already fully annotated and integrated into a knowledge graph — this skill is for raw spectral processing, not refinement of completed annotations.
- Spectral data lack associated metadata (e.g., taxon information) — taxonomical reweighting and ChEMBL integration depend on this context.
- Only untargeted MS1 data (precursor ions) are available without MS/MS fragmentation spectra — Molecular Networking and Sirius annotation require fragmentation patterns.

## Inputs

- LC-MS/MS DDA raw spectral data files (positive and/or negative ionization modes)
- Sample metadata file containing originating taxon information
- MZmine feature table (after peak detection and alignment)
- Fragmentation spectra in standardized format (mzML or proprietary MZmine output)

## Outputs

- Detected molecular features with retention time and m/z values
- Molecular Network in GraphML or similar format
- Annotated feature table with spectral matches and confidence scores
- Sirius/CSI:FingerID/CANOPUS predictions (structure, class, probability)
- Compound metadata enrichment (Wikidata ID, NPClassifier ontology)
- Sample-specific RDF knowledge graph (TTL format) ready for graph database import

## How to apply

The ENPKG workflow processes each sample individually through a defined sequence: (1) organize raw LC-MS/MS data and metadata into sample-specific directories; (2) run MZmine feature detection to identify and quantify peaks; (3) resolve the sample's taxonomic origin against Open Tree of Life (ottID) for downstream reweighting; (4) generate a Molecular Network from fragmentation spectra and annotate features via spectral matching to an in silico database coupled with taxonomical reweighting; (5) perform orthogonal Sirius/CSI:FingerID/CANOPUS annotation for structure prediction and chemical class assignment; (6) retrieve Wikidata IDs and NPClassifier ontology terms for all annotated compounds; and (7) integrate all processed data into an RDF knowledge graph. The workflow is orchestrated by shell scripts and Python modules that enforce dependency order and manage intermediate output schemas.

## Related tools

- **MZmine** (Feature detection, peak alignment, and LC-MS/MS data preprocessing prior to networking and annotation) — http://mzmine.github.io/
- **Sirius/CSI:FingerID/CANOPUS** (Ab initio structure prediction, molecular fingerprinting, and chemical class assignment from MS/MS fragmentation patterns) — https://bio.informatik.uni-jena.de/software/sirius/
- **Open Tree of Life** (Taxonomic reference and ottID resolution for sample-level taxonomy validation and reweighting) — https://tree.opentreeoflife.org/about/taxonomy-version/ott3.5
- **Wikidata** (Linked identifiers and structured metadata retrieval for annotated compounds) — https://www.wikidata.org/wiki/Wikidata:Main_Page
- **NPClassifier** (Natural product chemical class ontology assignment for annotated compounds) — https://npclassifier.ucsd.edu/
- **ChEMBL** (Optional bioactivity integration: retrieve compounds with reported activity against biological targets) — https://www.ebi.ac.uk/chembl/
- **enpkg_data_organization** (Step 1: Organize MZmine output into individual sample folders) — https://github.com/enpkg/enpkg_data_organization
- **enpkg_taxo_enhancer** (Step 2: Resolve taxonomy for each sample and link to Wikidata) — https://github.com/enpkg/enpkg_taxo_enhancer
- **enpkg_mn_isdb_taxo** (Step 3: Molecular Network generation, in silico database annotation, and taxonomical/chemical reweighting) — https://github.com/enpkg/enpkg_mn_isdb_taxo
- **enpkg_sirius_canopus** (Step 4: Sirius/CSI:FingerID/CANOPUS annotation execution) — https://github.com/enpkg/enpkg_sirius_canopus
- **enpkg_meta_analysis** (Step 5: Retrieve NPClassifier taxonomy and Wikidata ID; optional MEMO and ChEMBL integration) — https://github.com/enpkg/enpkg_meta_analysis
- **enpkg_graph_builder** (Step 6: Integrate all processed data into RDF knowledge graph (TTL output)) — https://github.com/enpkg/enpkg_graph_builder
- **ENPKG Full Workflow** (Orchestration and execution of the complete end-to-end pipeline) — https://github.com/enpkg/enpkg_full

## Examples

```
sh workflow/00_workflow_all.sh
```

## Evaluation signals

- All intermediate workflow outputs are present and non-empty: feature tables, molecular network, annotation results from both spectral matching and Sirius/CSI:FingerID methods.
- Feature annotations show agreement between two independent methods (spectral matching + Sirius) — overlapping compound hits indicate robust predictions.
- Molecular Network exhibits expected topology: degree distribution, connected components, and cluster sizes are consistent with known metabolomic datasets (referenced in paper: 1600 tropical plants, 337 medicinal plants).
- Final RDF knowledge graph passes structural validation: TTL syntax is valid, triples conform to ENPKG vocabulary schema, and entity links to Wikidata and NPClassifier resolve correctly.
- Taxonomical reweighting reduces false annotations: spectral matches that conflict with sample taxonomy are downranked or flagged; annotations for closely related taxa are preferred.

## Limitations

- Workflow processes each sample individually; cross-sample metabolite comparison and consensus annotation require post-processing via MEMO analysis or custom SPARQL queries.
- Sirius/CSI:FingerID predictions depend on the quality and mass accuracy of MS/MS fragmentation spectra; low-resolution or noisy spectra may yield unreliable structure predictions.
- Spectral matching annotation relies on in silico database completeness; natural products absent from the ISDB or custom spectral library will be unannotated or misannotated.
- Taxonomical reweighting improves precision but assumes accurate sample metadata (originating taxon); incorrect or ambiguous taxonomy can introduce systematic annotation bias.
- Knowledge graph integration requires stable Wikidata and Open Tree of Life identifiers; identifier changes or deprecations may disrupt linked data integrity over time.

## Evidence

- [readme] For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes).: "For each sample, the required input data are 1) A minimal metadata file containing the sample's originating taxon. 2) The LC-MS/MS DDA data (positive and/or negative ionization modes)."
- [readme] After MZmine processing, the workflow automatically resolves the species taxonomy against Open Tree of Life (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates features using two different methods (spectral matching to in silico DB coupled to taxonomical reweighting and Sirius/CSI:FingerID).: "After MZmine processing, the workflow automatically resolves the species taxonomy against Open Tree of Life (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates"
- [readme] Once the processing on individual samples is done, for annotated compounds, Wikidata ID and NPClassifier ontology is automatically retrieved and it is possible to integrate compounds with activity reported against one (or more) selected biological target in ChEMBL DB.: "Once the processing on individual samples is done, for annotated compounds, Wikidata ID and NPClassifier ontology is automatically retrieved and it is possible to integrate compounds with activity"
- [readme] Finally, all of the data previously generated is integrated into a sample-specific RDF knowledge graph. These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data.: "Finally, all of the data previously generated is integrated into a sample-specific RDF knowledge graph. These sample-specific KG from multiple specific can be combined to effectively compare samples"
- [other] The ENPKG full workflow comprises three primary operational stages: installation, setup, and execution, which together transform raw input into annotated outputs ready for knowledge-graph integration.: "The ENPKG full workflow comprises three primary operational stages: installation, setup, and execution, which together transform raw input into annotated outputs ready for knowledge-graph integration."
- [other] Validate the final annotated output files (molecular annotations, spectral matches, knowledge-graph triples) against the expected output schema and integrity checks.: "Validate the final annotated output files (molecular annotations, spectral matches, knowledge-graph triples) against the expected output schema and integrity checks."
- [readme] These steps needs to be run only once for each sample. Individual sample scale processing: (1) Organize data, (2) Taxonomical enhancement, (3) MN, ISDB annotation and taxonomical/chemical consistency reweighting, (4) SIRIUS/CSI:FingerID/CANOPUS annotation, (5) Compounds metadata enhancement, (6) Graph building.: "These steps needs to be run only once for each sample. Individual sample scale processing includes: data organization, taxonomical enhancement, MN and ISDB annotation with reweighting, Sirius/CSI"

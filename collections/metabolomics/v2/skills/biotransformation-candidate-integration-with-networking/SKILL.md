---
name: biotransformation-candidate-integration-with-networking
description: Use when you have output from a biotransformation rules module (candidate transformed structures linked to anchor molecules) and untargeted MS/MS spectral data, and you want to identify molecular families and annotate features with predicted structures by leveraging spectral similarity and network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - BAM
  - PROXIMAL2
  - GNN-SOM
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biotransformation-candidate-integration-with-networking

## Summary

Integrates candidate structures predicted by biotransformation rules with untargeted MS/MS data via global molecular networking to construct a spectral similarity network and assign putative molecular structures to MS features. This combines rule-based structure prediction with graph-based clustering to annotate metabolomics features with both predicted structures and network community membership.

## When to use

You have output from a biotransformation rules module (candidate transformed structures linked to anchor molecules) and untargeted MS/MS spectral data, and you want to identify molecular families and annotate features with predicted structures by leveraging spectral similarity and network topology rather than database matching alone.

## When NOT to use

- Input spectral data lacks MS/MS fragmentation spectra or contains only MS1 (precursor m/z) data.
- No biotransformation rules output is available; the skill requires pre-computed candidate structures.
- Anchor molecules are not known or cannot be reliably identified from the molecular network.

## Inputs

- Candidate transformed structures (SMILES format, linked to anchor molecules)
- MS/MS spectral data (MS1 feature list with precursor m/z, retention time; MS2 spectra with fragment peaks and intensities)
- Biotransformation rules output (structure-anchor pairs with predicted transformations)

## Outputs

- Molecular network file (GraphML, JSON, or GXF format)
- Feature annotation table (CSV/TSV mapping MS features to predicted structures and network clusters)
- Network nodes with annotated structures and cluster membership

## How to apply

Load candidate transformed structures from the biotransformation rules output alongside MS/MS spectral data. Compute pairwise spectral similarity scores (e.g., cosine similarity) across all features and construct a similarity network graph. Apply a similarity threshold to filter edges and retain only high-confidence spectral matches. Perform graph-based clustering or community detection to identify connected components representing putative molecular families. Annotate each network node by mapping MS features to their corresponding candidate structures from the biotransformation rules output and recording cluster membership. Finally, export the network in a standard format (GraphML, JSON, or GXF) and generate a feature annotation table linking each MS feature to its predicted structures and network cluster ID.

## Related tools

- **PROXIMAL2** (Generates biotransformation rules and predicts candidate transformed structures for input to the networking step) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Performs site-of-metabolism prediction and ranking of enzymatic products to refine candidate structure generation) — https://github.com/HassounLab/GNN-SOM
- **BAM** (Orchestrates the complete pipeline integrating biotransformation rules and global molecular networking) — https://github.com/HassounLab/BAM

## Examples

```
sh runBAM.sh
```

## Evaluation signals

- Network edges are generated only between feature pairs with spectral similarity above the specified threshold; verify by comparing cosine similarity scores to threshold cutoff.
- All candidate structures from biotransformation output are mapped to at least one MS feature node; audit the annotation table for completeness.
- Connected components form coherent molecular families (e.g., parent compounds and predicted metabolites cluster together); inspect subgraph topology visually or via edge density metrics.
- Network node annotations include both predicted SMILES structure(s) and cluster ID; schema validation confirms no missing or malformed structure strings.
- Exported network format is valid (GraphML/JSON parseable) and annotation table is a valid CSV/TSV with required columns (feature ID, SMILES, cluster ID).

## Limitations

- Requires high-quality MS/MS spectra; low-intensity or noisy fragmentation spectra may produce unreliable similarity scores and fragmented networks.
- Performance depends on the completeness and accuracy of the biotransformation rules dataset (KEGG, RetroRules, or custom); missing reactions will omit candidate structures.
- Spectral similarity thresholds and clustering parameters are data- and instrument-dependent; threshold selection is not explicitly automated and may require empirical tuning.
- Network topology reflects spectral similarity, not necessarily true biochemical relationships; isomeric or structurally similar compounds may cluster incorrectly.
- Annotation completeness is limited by coverage of candidate structures in the biotransformation output; novel or unexpected transformations will not be captured.

## Evidence

- [other] Load candidate transformed structures from biotransformation-rules module output and MS/MS spectral data. Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs in the dataset.: "Load candidate transformed structures from biotransformation-rules module output and MS/MS spectral data. Construct a similarity network by computing spectral similarity scores"
- [other] Filter edges based on a similarity threshold to retain only high-confidence spectral matches. Apply graph-based clustering or community detection to identify connected components representing putative molecular families.: "Filter edges based on a similarity threshold to retain only high-confidence spectral matches. Apply graph-based clustering or community detection to identify connected components representing"
- [other] Annotate each network node with the corresponding candidate structures from the biotransformation rules output and associate with MS1/MS2 features. Export the molecular network in a standard format (e.g., GraphML, JSON, or GXF) and generate a feature annotation table linking each MS feature to its predicted structure(s) and network cluster membership.: "Annotate each network node with the corresponding candidate structures from the biotransformation rules output and associate with MS1/MS2 features. Export the molecular network in a standard format"
- [readme] BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included under the BAM-main directory.: "BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included"
- [readme] Once the code and conda environments are structured as specified, run the runBAM.sh file. Note that no conda environment needs to be activated.: "Once the code and conda environments are structured as specified, run the runBAM.sh file"

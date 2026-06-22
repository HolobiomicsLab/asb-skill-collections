---
name: molecular-network-construction-for-metabolomics
description: Use when you have untargeted metabolomics data (e.g., LC-MS/MS spectra) and need to organize compounds by structural relatedness to enable structure discovery for unknown metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - HassounLab/BAM
  - GNN-SOM
  - PROXIMAL2
  - BAM
  techniques:
  - LC-MS
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

# molecular-network-construction-for-metabolomics

## Summary

Construct global molecular networks from untargeted metabolomics data to link structurally related compounds and enable propagation of molecular structure annotations. This skill bridges suspect discovery with biotransformation-based annotation by organizing metabolites into networks where anchor compounds with known structures seed annotation of unknown suspects.

## When to use

You have untargeted metabolomics data (e.g., LC-MS/MS spectra) and need to organize compounds by structural relatedness to enable structure discovery for unknown metabolites. Specifically, use this skill when you have anchor compounds with known SMILES/InChI and want to infer structures of suspects by finding those suspects in a molecular network derived from the same sample cohort or biological condition.

## When NOT to use

- Input is already a curated, single-compound reference spectral library rather than a discovery dataset—molecular networks require many interconnected spectra to build meaningful pathways.
- You have only targeted metabolomics data (focused on a few known compounds)—the strength of networks comes from global scope; targeted data will yield sparse, uninformative networks.
- Your suspects and anchors are not in the same sample cohort or experiment—network edges require spectral similarity; suspects and anchors from unrelated datasets will not appear as neighbors.

## Inputs

- Untargeted metabolomics MS/MS spectra (mzML, mzXML, or vendor format)
- Anchor compound reference library (with SMILES/InChI and identifiers)
- Sample metadata and grouping (optional, for network stratification)
- Spectral similarity scoring parameters (cosine function, m/z tolerance)

## Outputs

- Global molecular network (node and edge tables)
- Anchor-suspect pair CSV (identifier, mass, anchor ID, anchor SMILES)
- Network visualization (GraphML, GexF, or adjacency matrix)
- Network statistics (degree distribution, connected components, path lengths)

## How to apply

Construct a global molecular network by computing spectral similarity (e.g., cosine similarity) between all MS/MS spectra in your metabolomics dataset and connecting spectra above a similarity threshold. Retain both edges (spectral pairs) and node attributes (m/z, retention time, spectral data). Identify known anchor compounds in the network and mark them with their reference SMILES. For each suspect in the molecular network, record its identifier, precursor m/z, and network neighbors (anchors or suspect-neighbor paths). Export anchor-suspect pairs as a CSV with columns: identifier, mass, anchor (compound ID with known structure), and SMILES (the anchor's structure). This organized network becomes the input for biotransformation-based annotation methods, which will rank candidate structures for suspects based on biotransformation rules connecting them to their anchor neighbors.

## Related tools

- **GNN-SOM** (Ranks candidate molecular structures and site-of-metabolism predictions for suspects identified in the molecular network, leveraging graph neural networks trained on biotransformation patterns) — https://github.com/HassounLab/GNN-SOM
- **PROXIMAL2** (Generates biotransformation operators that define chemical transformations between anchor and suspect pairs, constraining the chemical feasibility of structure candidates) — https://github.com/HassounLab/PROXIMAL2
- **BAM** (Orchestrates end-to-end molecular structure discovery using the constructed network of anchor-suspect pairs combined with biotransformation rules and GNN-SOM ranking) — https://github.com/HassounLab/BAM

## Evaluation signals

- Network connectivity: molecular network contains ≥1 connected component linking anchors to suspects; no isolated anchor or suspect nodes (degree ≥1 expected for annotatable suspects)
- Anchor-suspect pair CSV completeness: every row has non-null identifier, mass, anchor ID, and valid SMILES; anchor compounds match reference library entries
- Network topology validation: edge-weighting (spectral similarity scores) are within plausible range (e.g., 0–1 for cosine); suspect-to-anchor paths exist and have biologically plausible lengths (≤5–10 edges typical for connected metabolome regions)
- Reproducibility: re-running the network construction with identical parameters on the same spectra produces identical node and edge lists (deterministic spectral similarity scoring)
- Downstream annotation agreement: candidates for suspects rank known correct structures higher than false positives when biotransformation rules are applied to the network-derived anchor-suspect pairs

## Limitations

- Network quality depends critically on spectral similarity threshold; too-low thresholds create spurious edges, too-high thresholds fragment the network and isolate suspects from anchors.
- Suspects present in low abundance or with poor-quality MS/MS spectra may have weak or missing spectral similarity edges, becoming unannotatable even if structural neighbors exist.
- Global molecular networks scale computationally with sample size (spectral similarity is O(n²) in the number of spectra); very large untargeted experiments may require sub-sampling or parallelization.
- Network topology alone does not guarantee correct annotation; suspects may be network-connected to anchors via off-target spectral similarity or noise, requiring validation against reference standards or orthogonal evidence.
- The approach requires that suspects and anchors co-occur in the same sample cohort for network linkage; cross-sample or cross-species network merging can introduce artifactual connections.

## Evidence

- [other] Open access repository-scale propagated nearest neighbor suspect spectral library for untargeted metabolomics: "Open access repository-scale propagated nearest neighbor suspect spectral library for untargeted metabolomics"
- [readme] the anchor-suspect pairs of interest need to be specified. We have used a set of pairs derived from the molecular network used to create the suspect library: "the anchor-suspect pairs of interest need to be specified. We have used a set of pairs derived from the molecular network used to create the suspect library"
- [readme] molecules_of_interest = csv file of list of queries. It must have an identifier and mass for the suspect as well as anchor and a SMILES that represents the anchor.: "molecules_of_interest = csv file of list of queries. It must have an identifier and mass for the suspect as well as anchor and a SMILES that represents the anchor"
- [other] Molecular structure discovery from untargeted metabolomics data using biotransformation rules and global molecular networking: "Molecular structure discovery from untargeted metabolomics data using biotransformation rules and global molecular networking"
- [readme] BAM checks if the suspect molecule is known by checking whether the SMILES or InChI is specified in the molecules_of_interest csv file: "BAM checks if the suspect molecule is known by checking whether the SMILES or InChI is specified in the molecules_of_interest csv file"
